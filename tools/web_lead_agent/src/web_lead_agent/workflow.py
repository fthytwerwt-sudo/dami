"""LangGraph 获客最小闭环。"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from web_lead_agent.approval import build_approval_request, evaluate_approval_payload
from web_lead_agent.channels.website_contact_form import WebsiteContactFormAdapter
from web_lead_agent.contracts import (
    ApprovalRequest,
    RuntimeConfig,
    SendReceipt,
    to_plain,
)
from web_lead_agent.discovery import assert_target_allowed
from web_lead_agent.drafting import TemplateDraftAdapter
from web_lead_agent.idempotency import SQLiteIdempotencyStore
from web_lead_agent.knowledge import SQLiteKnowledgeStore
from web_lead_agent.policy import DeterministicPolicyEngine
from web_lead_agent.runtime import RuntimeStore
from web_lead_agent.scoring import score_lead


class WebLeadState(TypedDict, total=False):
    """LangGraph state。"""

    run_id: str
    target_url: str
    status: str
    page: dict[str, Any]
    lead: dict[str, Any]
    scored_lead: dict[str, Any]
    knowledge: dict[str, Any]
    draft: dict[str, Any]
    policy: dict[str, Any]
    approval_request: dict[str, Any]
    approval_payload: dict[str, Any]
    approval_decision: dict[str, Any]
    send_action: dict[str, Any]
    receipt: dict[str, Any]
    final_status: str
    stopped: bool


def build_web_lead_graph(
    *,
    config: RuntimeConfig,
    runtime: RuntimeStore,
    knowledge_store: SQLiteKnowledgeStore,
    idempotency: SQLiteIdempotencyStore,
    adapter: WebsiteContactFormAdapter | None = None,
):
    """构建可 checkpoint 的 LangGraph StateGraph。"""

    adapter = adapter or WebsiteContactFormAdapter()
    drafter = TemplateDraftAdapter()
    policy_engine = DeterministicPolicyEngine()

    def discover_target_node(state: WebLeadState) -> WebLeadState:
        discovery = assert_target_allowed(state["target_url"], config)
        runtime.record_event(state["run_id"], "target_discovered", asdict(discovery))
        return {"status": "TARGET_DISCOVERED"}

    def crawl_public_site_node(state: WebLeadState) -> WebLeadState:
        page = adapter.crawl_public_site(state["target_url"], config)
        runtime.record_event(state["run_id"], "page_crawled", {"url": page.url})
        return {"page": to_plain(page), "status": "PAGE_CRAWLED"}

    def extract_company_node(state: WebLeadState) -> WebLeadState:
        page_obj = _page_from_dict(state["page"])
        lead = adapter.extract_company(page_obj)
        runtime.record_event(state["run_id"], "lead_extracted", to_plain(lead))
        return {"lead": to_plain(lead), "status": "LEAD_EXTRACTED"}

    def normalize_lead_node(state: WebLeadState) -> WebLeadState:
        lead = _lead_from_dict(state["lead"])
        return {"lead": to_plain(lead), "status": "LEAD_NORMALIZED"}

    def deduplicate_lead_node(state: WebLeadState) -> WebLeadState:
        runtime.record_event(state["run_id"], "lead_deduplicated", {"dedupe_count": 1})
        return {"status": "LEAD_DEDUPED"}

    def score_lead_node(state: WebLeadState) -> WebLeadState:
        scored = score_lead(_lead_from_dict(state["lead"]))
        runtime.record_event(state["run_id"], "lead_scored", to_plain(scored))
        return {"scored_lead": to_plain(scored), "status": "LEAD_SCORED"}

    def retrieve_knowledge_node(state: WebLeadState) -> WebLeadState:
        result = knowledge_store.retrieve(query=state["lead"].get("company_name", ""))
        runtime.record_event(state["run_id"], "knowledge_retrieved", to_plain(result))
        return {"knowledge": to_plain(result), "status": "KNOWLEDGE_RETRIEVED"}

    def generate_draft_node(state: WebLeadState) -> WebLeadState:
        draft = drafter.generate(_scored_from_dict(state["scored_lead"]), _knowledge_from_dict(state["knowledge"]))
        runtime.record_event(state["run_id"], "draft_generated", to_plain(draft))
        return {"draft": to_plain(draft), "status": "DRAFT_GENERATED"}

    def evaluate_policy_node(state: WebLeadState) -> WebLeadState:
        policy = policy_engine.evaluate(_draft_from_dict(state["draft"]), config)
        runtime.record_event(state["run_id"], "policy_evaluated", to_plain(policy))
        return {"policy": to_plain(policy), "status": "POLICY_EVALUATED"}

    def request_approval_node(state: WebLeadState) -> WebLeadState | Command:
        request = build_approval_request(
            _scored_from_dict(state["scored_lead"]),
            _draft_from_dict(state["draft"]),
            _policy_from_dict(state["policy"]),
            config,
        )
        request_payload = to_plain(request)
        runtime.save_state(
            state["run_id"],
            "READY_PENDING_HUMAN_APPROVAL",
            {**state, "approval_request": request_payload},
        )
        if config.mode == "draft_only":
            return {
                "approval_request": request_payload,
                "approval_decision": {"approved": False, "reason": "draft_only_mode"},
                "status": "READY_PENDING_HUMAN_APPROVAL",
            }
        approval_payload = state.get("approval_payload")
        if approval_payload is None:
            approval_payload = interrupt(request_payload)
        decision = evaluate_approval_payload(approval_payload, request, config)
        runtime.record_event(state["run_id"], "approval_decision", to_plain(decision))
        return {
            "approval_request": request_payload,
            "approval_payload": approval_payload,
            "approval_decision": to_plain(decision),
            "status": "APPROVAL_EVALUATED",
        }

    def fill_contact_form_node(state: WebLeadState) -> WebLeadState:
        page_obj = _page_from_dict(state["page"])
        form = adapter.locate_contact_form(page_obj)
        action = adapter.fill_contact_form(
            form,
            _scored_from_dict(state["scored_lead"]),
            _draft_from_dict(state["draft"]),
        )
        runtime.record_event(state["run_id"], "contact_form_filled", to_plain(action))
        return {"send_action": to_plain(action), "status": "FORM_FILLED_PENDING_SUBMIT"}

    def submit_once_node(state: WebLeadState) -> WebLeadState:
        receipt = adapter.submit_once(
            state["run_id"],
            _send_action_from_dict(state["send_action"]),
            _approval_decision_from_dict(state["approval_decision"]),
            config,
            runtime,
            idempotency,
        )
        return {"receipt": to_plain(receipt), "status": f"SUBMIT_{receipt.status}"}

    def capture_receipt_node(state: WebLeadState) -> WebLeadState:
        receipt = state.get("receipt") or to_plain(
            SendReceipt(
                status="BLOCKED",
                http_status=None,
                target_url=state.get("approval_request", {}).get("target_url", ""),
                idempotency_key="not_created",
                reason="not_approved_or_not_sent",
            )
        )
        runtime.record_event(state["run_id"], "receipt_captured", receipt)
        return {"receipt": receipt, "status": "RECEIPT_CAPTURED"}

    def persist_state_node(state: WebLeadState) -> WebLeadState:
        receipt = state.get("receipt", {})
        receipt_status = receipt.get("status") if isinstance(receipt, dict) else None
        if receipt_status == "SUCCESS":
            final_status = "COMPLETED_SYNTHETIC_SUPERVISED_SEND"
        elif state.get("approval_decision", {}).get("approved"):
            final_status = f"STOPPED_WITH_{receipt_status or 'UNKNOWN_RECEIPT'}"
        else:
            final_status = "READY_PENDING_HUMAN_APPROVAL"
        return runtime.stop_run(state["run_id"], final_status, state)

    graph = StateGraph(WebLeadState)
    graph.add_node("discover_target", discover_target_node)
    graph.add_node("crawl_public_site", crawl_public_site_node)
    graph.add_node("extract_company", extract_company_node)
    graph.add_node("normalize_lead", normalize_lead_node)
    graph.add_node("deduplicate_lead", deduplicate_lead_node)
    graph.add_node("score_lead", score_lead_node)
    graph.add_node("retrieve_knowledge", retrieve_knowledge_node)
    graph.add_node("generate_draft", generate_draft_node)
    graph.add_node("evaluate_policy", evaluate_policy_node)
    graph.add_node("request_approval", request_approval_node)
    graph.add_node("fill_contact_form", fill_contact_form_node)
    graph.add_node("submit_once", submit_once_node)
    graph.add_node("capture_receipt", capture_receipt_node)
    graph.add_node("persist_state", persist_state_node)

    graph.add_edge(START, "discover_target")
    graph.add_edge("discover_target", "crawl_public_site")
    graph.add_edge("crawl_public_site", "extract_company")
    graph.add_edge("extract_company", "normalize_lead")
    graph.add_edge("normalize_lead", "deduplicate_lead")
    graph.add_edge("deduplicate_lead", "score_lead")
    graph.add_edge("score_lead", "retrieve_knowledge")
    graph.add_edge("retrieve_knowledge", "generate_draft")
    graph.add_edge("generate_draft", "evaluate_policy")
    graph.add_edge("evaluate_policy", "request_approval")
    graph.add_conditional_edges(
        "request_approval",
        _route_after_approval,
        {
            "fill": "fill_contact_form",
            "persist": "persist_state",
        },
    )
    graph.add_edge("fill_contact_form", "submit_once")
    graph.add_edge("submit_once", "capture_receipt")
    graph.add_edge("capture_receipt", "persist_state")
    graph.add_edge("persist_state", END)
    return graph


def compile_web_lead_graph(*args: Any, checkpointer: Any = None, **kwargs: Any):
    """编译 LangGraph；外部可传 SQLite checkpointer。"""

    graph = build_web_lead_graph(*args, **kwargs)
    return graph.compile(checkpointer=checkpointer)


def make_sqlite_checkpointer(path: Path):
    """创建 SQLite checkpointer。"""

    from langgraph.checkpoint.sqlite import SqliteSaver

    return SqliteSaver.from_conn_string(str(path))


def run_minimal_loop(
    *,
    target_url: str,
    run_id: str,
    config: RuntimeConfig,
    runtime: RuntimeStore,
    knowledge_store: SQLiteKnowledgeStore,
    idempotency: SQLiteIdempotencyStore,
    approval_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """非交互执行入口：测试/CLI 可直接传入审批 payload。"""

    graph = build_web_lead_graph(
        config=config,
        runtime=runtime,
        knowledge_store=knowledge_store,
        idempotency=idempotency,
    )
    app = graph.compile()
    initial: WebLeadState = {"run_id": run_id, "target_url": target_url}
    if approval_payload:
        initial["approval_payload"] = approval_payload
    return app.invoke(initial)


def _route_after_approval(state: WebLeadState) -> str:
    if state.get("approval_decision", {}).get("approved") is True:
        return "fill"
    return "persist"


def _page_from_dict(data: dict[str, Any]):
    from web_lead_agent.contracts import PageEvidence

    return PageEvidence(**data)


def _lead_from_dict(data: dict[str, Any]):
    from web_lead_agent.contracts import LeadRecord

    return LeadRecord(**data)


def _scored_from_dict(data: dict[str, Any]):
    from web_lead_agent.contracts import ScoredLead

    lead = _lead_from_dict(data["lead"])
    return ScoredLead(lead=lead, score=data["score"], qualified=data["qualified"], reasons=data.get("reasons", []))


def _knowledge_from_dict(data: dict[str, Any]):
    from web_lead_agent.contracts import KnowledgeItem, KnowledgeResult

    return KnowledgeResult(
        status=data["status"],
        items=[KnowledgeItem(**item) for item in data.get("items", [])],
        missing_topics=data.get("missing_topics", []),
        conflicts=data.get("conflicts", []),
    )


def _draft_from_dict(data: dict[str, Any]):
    from web_lead_agent.contracts import MessageDraft

    return MessageDraft(**data)


def _policy_from_dict(data: dict[str, Any]):
    from web_lead_agent.contracts import PolicyResult

    return PolicyResult(**data)


def _approval_decision_from_dict(data: dict[str, Any]):
    from web_lead_agent.contracts import ApprovalDecision

    return ApprovalDecision(**data)


def _send_action_from_dict(data: dict[str, Any]):
    from web_lead_agent.contracts import SendAction

    return SendAction(**data)

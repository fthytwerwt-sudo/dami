"""LangGraph 客户沟通草稿流程：检索、政策、审批、填表、阻断发送。"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from .contracts import KnowledgeAdapter, WebAdapter
from .policy import DeterministicPolicyGate, generate_draft
from .runtime import JsonlTraceRecorder, SQLiteRuntimeStore


class ConversationState(TypedDict, total=False):
    """可持久化的会话状态。"""

    thread_id: str
    message: str
    knowledge_scope: str
    form_url: str
    runtime_mode: str
    knowledge: dict[str, Any]
    draft: dict[str, Any]
    policy: dict[str, Any]
    approval: dict[str, Any]
    dom_action: dict[str, Any]
    stage: str
    send_status: str


def request_approval(state: ConversationState) -> dict[str, Any]:
    """构造最小人工审批请求，不代替人工做决定。"""

    return {
        "type": "SYNTHETIC_HUMAN_APPROVAL",
        "thread_id": state["thread_id"],
        "draft": state.get("draft", {}),
        "allowed_actions": ["approve", "reject"],
    }


def build_conversation_graph(
    *,
    knowledge: KnowledgeAdapter,
    policy: DeterministicPolicyGate,
    web: WebAdapter,
    runtime: SQLiteRuntimeStore,
    trace: JsonlTraceRecorder,
    checkpointer: BaseCheckpointSaver,
):
    """构建只允许 ``draft_only`` 且必须人工恢复的流程图。"""

    def _record(state: ConversationState, node: str, details: dict[str, Any]) -> None:
        thread_id = state["thread_id"]
        trace.record(thread_id, node, details)
        runtime.record_event(thread_id, node, details)

    def retrieve_node(state: ConversationState) -> dict[str, Any]:
        if state.get("runtime_mode") != "draft_only":
            raise ValueError("当前仅允许 draft_only")
        result = knowledge.retrieve_knowledge(state["message"], state["knowledge_scope"])
        _record(state, "retrieve", {"status": result.status, "item_count": len(result.items)})
        return {"knowledge": result.to_dict(), "stage": "KNOWLEDGE_RETRIEVED"}

    def draft_node(state: ConversationState) -> dict[str, Any]:
        raw = state["knowledge"]
        from .contracts import KnowledgeResult

        result = KnowledgeResult(**raw)
        if result.status != "FOUND":
            _record(state, "draft", {"status": "SKIPPED", "reason": result.status})
            return {"stage": "DRAFT_SKIPPED", "send_status": "BLOCKED"}
        draft = generate_draft(state["message"], result)
        _record(state, "draft", {"status": draft.status, "source_count": len(draft.source_urls)})
        return {"draft": draft.to_dict(), "stage": "DRAFT_CREATED"}

    def policy_node(state: ConversationState) -> dict[str, Any]:
        from .contracts import KnowledgeResult

        result = policy.evaluate_policy(state["message"], KnowledgeResult(**state["knowledge"]))
        _record(state, "policy", {"decision": result.decision, "reasons": result.reasons})
        return {"policy": result.to_dict(), "stage": "POLICY_EVALUATED"}

    def route_after_policy(state: ConversationState) -> Literal["approval", "blocked"]:
        return "blocked" if state["policy"]["decision"] in {"BLOCK_REPLY", "ESCALATE_HUMAN"} else "approval"

    def blocked_node(state: ConversationState) -> dict[str, Any]:
        _record(state, "blocked", {"decision": state["policy"]["decision"]})
        final = {"stage": "BLOCKED_BY_POLICY", "send_status": "BLOCKED"}
        runtime.save_checkpoint(state["thread_id"], {**state, **final})
        return final

    def approval_node(state: ConversationState) -> dict[str, Any]:
        _record(state, "approval", {"status": "WAITING_APPROVAL"})
        waiting = {**state, "stage": "WAITING_APPROVAL", "send_status": "NOT_SENT"}
        runtime.save_checkpoint(state["thread_id"], waiting)
        decision = interrupt(request_approval(state))
        approved = bool(decision.get("approved")) if isinstance(decision, dict) else False
        return {"approval": {"approved": approved}, "stage": "APPROVED" if approved else "REJECTED"}

    def route_after_approval(state: ConversationState) -> Literal["dom_fill", "rejected"]:
        return "dom_fill" if state.get("approval", {}).get("approved") else "rejected"

    def rejected_node(state: ConversationState) -> dict[str, Any]:
        _record(state, "rejected", {"status": "HUMAN_REJECTED"})
        final = {"stage": "HUMAN_REJECTED", "send_status": "BLOCKED"}
        runtime.save_checkpoint(state["thread_id"], {**state, **final})
        return final

    def dom_fill_node(state: ConversationState) -> dict[str, Any]:
        action = web.fill_web_form(state["form_url"], {"Message": state["draft"]["text"]})
        send_guard = web.submit_message(action)
        _record(
            state,
            "dom_fill",
            {"status": action.status, "submit_count": action.details.get("submit_count", -1)},
        )
        final = {
            "dom_action": action.to_dict(),
            "stage": "FILLED_PENDING_SUBMIT",
            "send_status": "BLOCKED" if send_guard.status == "BLOCK_SEND" else "UNKNOWN",
        }
        runtime.save_checkpoint(state["thread_id"], {**state, **final})
        return final

    builder = StateGraph(ConversationState)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("draft", draft_node)
    builder.add_node("policy", policy_node)
    builder.add_node("blocked", blocked_node)
    builder.add_node("approval", approval_node)
    builder.add_node("rejected", rejected_node)
    builder.add_node("dom_fill", dom_fill_node)
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "draft")
    builder.add_edge("draft", "policy")
    builder.add_conditional_edges("policy", route_after_policy)
    builder.add_edge("blocked", END)
    builder.add_conditional_edges("approval", route_after_approval)
    builder.add_edge("rejected", END)
    builder.add_edge("dom_fill", END)
    return builder.compile(checkpointer=checkpointer)

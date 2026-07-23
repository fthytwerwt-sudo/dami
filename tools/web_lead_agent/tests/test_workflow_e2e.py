from __future__ import annotations

from pathlib import Path

from langgraph.types import Command

from web_lead_agent.contracts import RuntimeConfig
from web_lead_agent.idempotency import SQLiteIdempotencyStore
from web_lead_agent.knowledge import SQLiteKnowledgeStore
from web_lead_agent.runtime import RuntimeStore
from web_lead_agent.workflow import build_web_lead_graph, make_sqlite_checkpointer, run_minimal_loop


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures"


def _stores(tmp_path):
    runtime = RuntimeStore(tmp_path / "runtime")
    knowledge = SQLiteKnowledgeStore(tmp_path / "knowledge.sqlite3")
    knowledge.load_fixture(FIXTURE_ROOT / "synthetic_knowledge.json")
    idempotency = SQLiteIdempotencyStore(tmp_path / "idem.sqlite3")
    return runtime, knowledge, idempotency


def test_draft_only_e2e_stops_before_submit(tmp_path, synthetic_server):
    runtime, knowledge, idempotency = _stores(tmp_path)
    config = RuntimeConfig(
        workspace_path=tmp_path,
        mode="draft_only",
        real_send_enabled=False,
        allowed_domains=("127.0.0.1",),
    )
    result = run_minimal_loop(
        target_url=f"{synthetic_server}/index.html",
        run_id="e2e-draft",
        config=config,
        runtime=runtime,
        knowledge_store=knowledge,
        idempotency=idempotency,
    )
    assert result["final_status"] == "READY_PENDING_HUMAN_APPROVAL"
    assert "send_action" not in result
    assert runtime.send_count("e2e-draft", "127.0.0.1") == 0


def test_supervised_synthetic_e2e_submits_once_and_stops(tmp_path, synthetic_server):
    draft_runtime, draft_knowledge, draft_idem = _stores(tmp_path / "draft")
    draft_config = RuntimeConfig(
        workspace_path=tmp_path / "draft",
        mode="draft_only",
        real_send_enabled=False,
        allowed_domains=("127.0.0.1",),
    )
    draft_result = run_minimal_loop(
        target_url=f"{synthetic_server}/index.html",
        run_id="e2e-draft-for-approval",
        config=draft_config,
        runtime=draft_runtime,
        knowledge_store=draft_knowledge,
        idempotency=draft_idem,
    )
    request = draft_result["approval_request"]
    approval_payload = {
        "approved": True,
        "human_approval": True,
        "approved_target_domain": request["target_domain"],
        "approved_channel": request["channel"],
        "approved_account": "synthetic_local_account",
        "approved_message": request["message"],
        "send_limit": 1,
        "approved_action": "submit_once",
    }

    runtime, knowledge, idempotency = _stores(tmp_path / "approved")
    config = RuntimeConfig(
        workspace_path=tmp_path / "approved",
        mode="supervised_single_send",
        real_send_enabled=True,
        allowed_domains=("127.0.0.1",),
        approved_account="synthetic_local_account",
    )
    result = run_minimal_loop(
        target_url=f"{synthetic_server}/index.html",
        run_id="e2e-approved",
        config=config,
        runtime=runtime,
        knowledge_store=knowledge,
        idempotency=idempotency,
        approval_payload=approval_payload,
    )
    assert result["final_status"] == "COMPLETED_SYNTHETIC_SUPERVISED_SEND"
    assert result["receipt"]["status"] == "SUCCESS"
    assert runtime.send_count("e2e-approved", "127.0.0.1") == 1
    assert result["stopped"] is True


def test_langgraph_sqlite_checkpoint_interrupt_resume(tmp_path, synthetic_server):
    runtime, knowledge, idempotency = _stores(tmp_path / "checkpoint")
    config = RuntimeConfig(
        workspace_path=tmp_path / "checkpoint",
        mode="supervised_single_send",
        real_send_enabled=True,
        allowed_domains=("127.0.0.1",),
        approved_account="synthetic_local_account",
    )
    graph = build_web_lead_graph(
        config=config,
        runtime=runtime,
        knowledge_store=knowledge,
        idempotency=idempotency,
    )
    with make_sqlite_checkpointer(tmp_path / "checkpoint.sqlite3") as checkpointer:
        app = graph.compile(checkpointer=checkpointer)
        thread_config = {"configurable": {"thread_id": "checkpoint-thread"}}
        first = app.invoke(
            {
                "run_id": "checkpoint-run",
                "target_url": f"{synthetic_server}/index.html",
            },
            config=thread_config,
        )
        request = first["__interrupt__"][0].value
        approval_payload = {
            "approved": True,
            "human_approval": True,
            "approved_target_domain": request["target_domain"],
            "approved_channel": request["channel"],
            "approved_account": "synthetic_local_account",
            "approved_message": request["message"],
            "send_limit": 1,
            "approved_action": "submit_once",
        }
        final = app.invoke(Command(resume=approval_payload), config=thread_config)
    assert first["__interrupt__"]
    assert final["final_status"] == "COMPLETED_SYNTHETIC_SUPERVISED_SEND"
    assert final["receipt"]["status"] == "SUCCESS"
    assert runtime.send_count("checkpoint-run", "127.0.0.1") == 1

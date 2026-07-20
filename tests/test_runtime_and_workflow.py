"""运行时持久化、LangGraph 中断恢复和 Trace 测试。"""

from __future__ import annotations

import json
from pathlib import Path

from langgraph.types import Command

from web_agent_toolkit.knowledge import SQLiteKnowledgeAdapter
from web_agent_toolkit.policy import DeterministicPolicyGate
from web_agent_toolkit.runtime import JsonlTraceRecorder, SQLiteRuntimeStore
from web_agent_toolkit.web import PlaywrightWebAdapter
from web_agent_toolkit.workflow import build_conversation_graph


def _knowledge_records() -> list[dict[str, object]]:
    fixture = Path(__file__).parent / "fixtures" / "synthetic_knowledge.json"
    return json.loads(fixture.read_text(encoding="utf-8"))


def test_runtime_checkpoint_survives_reopen(tmp_path: Path) -> None:
    """自有运行时状态必须可在 SQLite 重开后恢复。"""

    db_path = tmp_path / "runtime.sqlite"
    store = SQLiteRuntimeStore(db_path)
    store.save_checkpoint("thread-1", {"stage": "WAITING_APPROVAL", "send_status": "NOT_SENT"})
    store.close()

    reopened = SQLiteRuntimeStore(db_path)
    state = reopened.resume_run("thread-1")
    assert state["stage"] == "WAITING_APPROVAL"
    assert state["send_status"] == "NOT_SENT"
    reopened.close()


def test_langgraph_interrupt_resume_fills_dom_without_submit(
    tmp_path: Path, synthetic_site_url: str
) -> None:
    """流程应在人工点中断，恢复后仅填入本地表单并阻断提交。"""

    knowledge = SQLiteKnowledgeAdapter(tmp_path / "knowledge.sqlite")
    knowledge.replace_all(_knowledge_records())
    runtime = SQLiteRuntimeStore(tmp_path / "runtime.sqlite")
    trace = JsonlTraceRecorder(tmp_path / "trace.jsonl")
    config = {"configurable": {"thread_id": "thread-graph-1"}}

    with runtime.langgraph_checkpointer() as checkpointer:
        graph = build_conversation_graph(
            knowledge=knowledge,
            policy=DeterministicPolicyGate(),
            web=PlaywrightWebAdapter(),
            runtime=runtime,
            trace=trace,
            checkpointer=checkpointer,
        )
        interrupted = graph.invoke(
            {
                "thread_id": "thread-graph-1",
                "message": "Please share product information",
                "knowledge_scope": "sandbox_only",
                "form_url": synthetic_site_url,
                "runtime_mode": "draft_only",
            },
            config=config,
        )
        assert interrupted["__interrupt__"]

    with runtime.langgraph_checkpointer() as checkpointer:
        resumed_graph = build_conversation_graph(
            knowledge=knowledge,
            policy=DeterministicPolicyGate(),
            web=PlaywrightWebAdapter(),
            runtime=runtime,
            trace=trace,
            checkpointer=checkpointer,
        )
        completed = resumed_graph.invoke(Command(resume={"approved": True}), config=config)

    assert completed["stage"] == "FILLED_PENDING_SUBMIT"
    assert completed["dom_action"]["details"]["submit_count"] == 0
    assert completed["send_status"] == "BLOCKED"
    trace_events = [json.loads(line) for line in (tmp_path / "trace.jsonl").read_text().splitlines()]
    assert {event["node"] for event in trace_events} >= {"retrieve", "policy", "approval", "dom_fill"}
    runtime.close()

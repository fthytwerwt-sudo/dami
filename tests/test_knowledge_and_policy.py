"""知识召回、事实冲突和确定性政策闸门测试。"""

from __future__ import annotations

import json
from pathlib import Path

from web_agent_toolkit.knowledge import SQLiteKnowledgeAdapter
from web_agent_toolkit.policy import DeterministicPolicyGate, generate_draft


def _load_records() -> list[dict[str, object]]:
    fixture = Path(__file__).parent / "fixtures" / "synthetic_knowledge.json"
    return json.loads(fixture.read_text(encoding="utf-8"))


def test_retrieval_returns_source_and_scope(tmp_path: Path) -> None:
    """召回必须返回来源、日期、范围、状态和置信度。"""

    adapter = SQLiteKnowledgeAdapter(tmp_path / "knowledge.sqlite")
    adapter.replace_all(_load_records())
    result = adapter.retrieve_knowledge("product information", scope="sandbox_only")

    assert result.status == "FOUND"
    assert result.items[0]["source_url"].startswith("https://knowledge.synthetic.example/")
    assert result.items[0]["scope"] == "sandbox_only"
    assert result.requires_human is False


def test_missing_or_conflicting_knowledge_fails_closed(tmp_path: Path) -> None:
    """知识缺失必须阻断，冲突必须升级人工。"""

    adapter = SQLiteKnowledgeAdapter(tmp_path / "knowledge.sqlite")
    adapter.replace_all(_load_records())

    missing = adapter.retrieve_knowledge("unknown fact", scope="sandbox_only")
    conflict = adapter.retrieve_knowledge("delivery conflict", scope="sandbox_only")

    assert missing.status == "MISSING"
    assert missing.requires_human is True
    assert conflict.status == "CONFLICT"
    assert conflict.requires_human is True


def test_policy_is_deterministic_and_draft_uses_only_sources(tmp_path: Path) -> None:
    """价格问题必须人审；安全问题可生成带来源草稿。"""

    adapter = SQLiteKnowledgeAdapter(tmp_path / "knowledge.sqlite")
    adapter.replace_all(_load_records())
    gate = DeterministicPolicyGate()

    safe = adapter.retrieve_knowledge("product information", scope="sandbox_only")
    price = adapter.retrieve_knowledge("price quotation", scope="sandbox_only")

    assert gate.evaluate_policy("Please share product information", safe).decision == "ALLOW_DRAFT"
    assert gate.evaluate_policy("What is the price?", price).decision == "REQUIRE_REVIEW"
    draft = generate_draft("Please share product information", safe)
    assert "SYNTHETIC" in draft.text
    assert draft.source_urls == [safe.items[0]["source_url"]]

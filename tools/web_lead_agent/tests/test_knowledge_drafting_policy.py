from __future__ import annotations

from pathlib import Path

from web_lead_agent.contracts import KnowledgeItem, LeadRecord, MessageDraft, RuntimeConfig
from web_lead_agent.drafting import TemplateDraftAdapter
from web_lead_agent.knowledge import SQLiteKnowledgeStore
from web_lead_agent.policy import DeterministicPolicyEngine
from web_lead_agent.scoring import score_lead


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures"


def test_found_knowledge_generates_clean_draft(tmp_path):
    store = SQLiteKnowledgeStore(tmp_path / "knowledge.sqlite3")
    store.load_fixture(FIXTURE_ROOT / "synthetic_knowledge.json")
    result = store.retrieve()
    lead = score_lead(
        LeadRecord(
            company_name="Pacific Pantry Imports",
            domain="127.0.0.1",
            source_url="http://127.0.0.1/index.html",
            contact_url="http://127.0.0.1/submit/success",
            country="Singapore",
            business_type="Food import and wholesale distributor",
        )
    )
    draft = TemplateDraftAdapter().generate(lead, result)
    policy = DeterministicPolicyEngine().evaluate(
        draft,
        RuntimeConfig(workspace_path=tmp_path),
    )
    assert result.status == "FOUND"
    assert draft.status == "DRAFT_READY"
    assert policy.status == "ALLOW_DRAFT"


def test_missing_knowledge_blocks_draft(tmp_path):
    store = SQLiteKnowledgeStore(tmp_path / "knowledge.sqlite3")
    store.replace_all(
        [
            KnowledgeItem(
                source_id="only-one",
                topic="product_positioning",
                statement="A specialty rice project.",
            )
        ]
    )
    result = store.retrieve()
    lead = score_lead(LeadRecord("Buyer", "example.com", "http://example.com", "http://example.com/contact"))
    draft = TemplateDraftAdapter().generate(lead, result)
    policy = DeterministicPolicyEngine().evaluate(draft, RuntimeConfig(workspace_path=tmp_path))
    assert result.status == "MISSING"
    assert draft.status == "BLOCKED_MISSING_KNOWLEDGE"
    assert policy.status == "BLOCK_REPLY"


def test_conflicting_knowledge_escalates(tmp_path):
    store = SQLiteKnowledgeStore(tmp_path / "knowledge.sqlite3")
    store.replace_all(
        [
            KnowledgeItem("p1", "product_positioning", "Position A", conflict_group="positioning"),
            KnowledgeItem("p2", "product_positioning", "Position B", conflict_group="positioning"),
            KnowledgeItem("b1", "business_intent", "Intent", conflict_group="intent"),
            KnowledgeItem("c1", "approved_cta", "CTA", conflict_group="cta"),
        ]
    )
    result = store.retrieve()
    lead = score_lead(LeadRecord("Buyer", "example.com", "http://example.com", "http://example.com/contact"))
    draft = TemplateDraftAdapter().generate(lead, result)
    policy = DeterministicPolicyEngine().evaluate(draft, RuntimeConfig(workspace_path=tmp_path))
    assert result.status == "CONFLICT"
    assert draft.status == "BLOCKED_CONFLICTING_KNOWLEDGE"
    assert policy.status == "ESCALATE_HUMAN"


def test_restricted_terms_require_review(tmp_path):
    draft = MessageDraft(
        subject="Price and MOQ",
        body="Can we discuss low GI certification and delivery?",
        knowledge_source_ids=["x"],
    )
    policy = DeterministicPolicyEngine().evaluate(draft, RuntimeConfig(workspace_path=tmp_path))
    assert policy.status == "REQUIRE_REVIEW"
    assert {"price", "moq", "low gi"}.issubset(set(policy.risk_items))

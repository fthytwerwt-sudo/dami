from __future__ import annotations

from web_lead_agent.approval import build_approval_request, evaluate_approval_payload
from web_lead_agent.contracts import LeadRecord, MessageDraft, PolicyResult, RuntimeConfig
from web_lead_agent.idempotency import SQLiteIdempotencyStore, make_idempotency_key
from web_lead_agent.runtime import RuntimeStore
from web_lead_agent.scoring import score_lead


def _approval_request(tmp_path):
    lead = score_lead(
        LeadRecord(
            company_name="Pacific Pantry Imports",
            domain="127.0.0.1",
            source_url="http://127.0.0.1/index.html",
            contact_url="http://127.0.0.1/submit/success",
            business_type="Food import distributor",
        )
    )
    draft = MessageDraft("Subject", "Body", ["source-1"])
    config = RuntimeConfig(
        workspace_path=tmp_path,
        mode="supervised_single_send",
        approved_account="synthetic_local_account",
    )
    return build_approval_request(lead, draft, PolicyResult("ALLOW_DRAFT"), config), config


def test_approval_requires_all_flags(tmp_path):
    request, config = _approval_request(tmp_path)
    missing = evaluate_approval_payload({}, request, config)
    assert missing.approved is False
    payload = {
        "approved": True,
        "human_approval": True,
        "approved_target_domain": request.target_domain,
        "approved_channel": request.channel,
        "approved_account": "synthetic_local_account",
        "approved_message": request.message,
        "send_limit": 1,
        "approved_action": "submit_once",
    }
    decision = evaluate_approval_payload(payload, request, config)
    assert decision.approved is True


def test_idempotency_duplicate_blocks(tmp_path):
    store = SQLiteIdempotencyStore(tmp_path / "idem.sqlite3")
    key = make_idempotency_key("127.0.0.1", "http://127.0.0.1/submit", "hello", "task")
    assert store.claim_or_block(key, "127.0.0.1", "http://127.0.0.1/submit") is True
    assert store.claim_or_block(key, "127.0.0.1", "http://127.0.0.1/submit") is False


def test_runtime_state_can_resume_after_reopen_and_send_count_caps(tmp_path):
    runtime = RuntimeStore(tmp_path)
    runtime.save_state("run-1", "READY_PENDING_HUMAN_APPROVAL", {"value": 1})
    assert runtime.claim_send_slot("run-1", "127.0.0.1", max_send=1) is True
    assert runtime.claim_send_slot("run-1", "127.0.0.1", max_send=1) is False
    assert runtime.send_count("run-1", "127.0.0.1") == 1
    runtime.close()
    reopened = RuntimeStore(tmp_path)
    assert reopened.resume_state("run-1") == {"value": 1}
    assert reopened.send_count("run-1", "127.0.0.1") == 1

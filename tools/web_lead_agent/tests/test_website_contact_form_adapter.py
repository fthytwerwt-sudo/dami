from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from web_lead_agent.approval import build_approval_request, evaluate_approval_payload
from web_lead_agent.channels.website_contact_form import WebsiteContactFormAdapter
from web_lead_agent.contracts import MessageDraft, PolicyResult, PolicyViolation, RuntimeConfig
from web_lead_agent.discovery import assert_public_page_safe
from web_lead_agent.extract import extract_page
from web_lead_agent.idempotency import SQLiteIdempotencyStore, make_idempotency_key
from web_lead_agent.runtime import RuntimeStore
from web_lead_agent.scoring import score_lead


SITE_ROOT = Path(__file__).resolve().parents[1] / "fixtures/synthetic_site"


def _prepared_send(tmp_path, synthetic_server, *, enabled=True, approved=True):
    adapter = WebsiteContactFormAdapter()
    config = RuntimeConfig(
        workspace_path=tmp_path,
        mode="supervised_single_send",
        real_send_enabled=enabled,
        allowed_domains=("127.0.0.1",),
        approved_account="synthetic_local_account",
    )
    page = adapter.crawl_public_site(f"{synthetic_server}/index.html", config)
    lead = score_lead(adapter.extract_company(page))
    form = adapter.locate_contact_form(page)
    draft = MessageDraft("Subject", "Body", ["source-1"])
    request = build_approval_request(lead, draft, PolicyResult("ALLOW_DRAFT"), config)
    payload = {
        "approved": approved,
        "human_approval": approved,
        "approved_target_domain": request.target_domain,
        "approved_channel": request.channel,
        "approved_account": "synthetic_local_account",
        "approved_message": request.message,
        "send_limit": 1,
        "approved_action": "submit_once",
    }
    decision = evaluate_approval_payload(payload, request, config)
    action = adapter.fill_contact_form(form, lead, draft)
    runtime = RuntimeStore(tmp_path / "runtime")
    idempotency = SQLiteIdempotencyStore(tmp_path / "idem.sqlite3")
    return adapter, config, runtime, idempotency, action, decision


def test_non_allowlisted_domain_is_blocked(tmp_path):
    adapter = WebsiteContactFormAdapter()
    config = RuntimeConfig(workspace_path=tmp_path, allowed_domains=("127.0.0.1",))
    with pytest.raises(PolicyViolation, match="domain_not_allowlisted"):
        adapter.crawl_public_site("http://example.com/index.html", config)


def test_external_subresource_policy_blocks_page():
    html = (SITE_ROOT / "external_subresource.html").read_text(encoding="utf-8")
    page = extract_page("http://127.0.0.1/external_subresource.html", html)
    with pytest.raises(PolicyViolation, match="external_subresource_detected"):
        assert_public_page_safe(page)


def test_not_approved_cannot_submit(tmp_path, synthetic_server):
    adapter, config, runtime, idempotency, action, decision = _prepared_send(
        tmp_path,
        synthetic_server,
        enabled=True,
        approved=False,
    )
    receipt = adapter.submit_once("run-not-approved", action, decision, config, runtime, idempotency)
    assert receipt.status == "BLOCKED"
    assert "approval_not_valid" in receipt.reason
    assert runtime.send_count("run-not-approved", action.target_domain) == 0


def test_real_send_disabled_cannot_submit(tmp_path, synthetic_server):
    adapter, config, runtime, idempotency, action, decision = _prepared_send(
        tmp_path,
        synthetic_server,
        enabled=False,
        approved=True,
    )
    receipt = adapter.submit_once("run-disabled", action, decision, config, runtime, idempotency)
    assert receipt.status == "BLOCKED"
    assert receipt.reason == "real_send_enabled_false"
    assert runtime.send_count("run-disabled", action.target_domain) == 0


def test_one_approved_send_only_once_and_duplicate_blocks(tmp_path, synthetic_server):
    adapter, config, runtime, idempotency, action, decision = _prepared_send(
        tmp_path,
        synthetic_server,
        enabled=True,
        approved=True,
    )
    first = adapter.submit_once("run-once", action, decision, config, runtime, idempotency)
    second = adapter.submit_once("run-once", action, decision, config, runtime, idempotency)
    assert first.status == "SUCCESS"
    assert runtime.send_count("run-once", action.target_domain) == 1
    assert second.status == "BLOCKED"
    assert second.reason == "duplicate_idempotency_key"


def test_submit_failure_receipt_is_saved(tmp_path, synthetic_server):
    adapter, config, runtime, idempotency, action, decision = _prepared_send(
        tmp_path,
        synthetic_server,
        enabled=True,
        approved=True,
    )
    fail_url = f"{synthetic_server}/submit/fail"
    fail_key = make_idempotency_key(action.target_domain, fail_url, action.payload["message"], config.task_id)
    action = replace(action, target_url=fail_url, idempotency_key=fail_key)
    receipt = adapter.submit_once("run-fail", action, decision, config, runtime, idempotency)
    resumed = runtime.resume_state("run-fail")
    assert receipt.status == "FAILED"
    assert receipt.http_status == 500
    assert receipt.retry_scheduled is False
    assert resumed is None


def test_unknown_result_no_retry(tmp_path, synthetic_server):
    adapter, config, runtime, idempotency, action, decision = _prepared_send(
        tmp_path,
        synthetic_server,
        enabled=True,
        approved=True,
    )
    unknown_url = f"{synthetic_server}/submit/unknown"
    unknown_key = make_idempotency_key(action.target_domain, unknown_url, action.payload["message"], config.task_id)
    action = replace(action, target_url=unknown_url, idempotency_key=unknown_key)
    receipt = adapter.submit_once("run-unknown", action, decision, config, runtime, idempotency)
    assert receipt.status == "UNKNOWN"
    assert receipt.retry_scheduled is False
    assert runtime.send_count("run-unknown", action.target_domain) == 1

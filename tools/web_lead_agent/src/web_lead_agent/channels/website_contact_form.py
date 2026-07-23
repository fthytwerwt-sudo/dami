"""WebsiteContactFormAdapter：公开网页联系表单的一次受监督提交。"""

from __future__ import annotations

from dataclasses import asdict
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from web_lead_agent.contracts import (
    ApprovalDecision,
    MessageDraft,
    PageEvidence,
    PolicyViolation,
    RuntimeConfig,
    ScoredLead,
    SendAction,
    SendReceipt,
)
from web_lead_agent.discovery import assert_public_page_safe, assert_target_allowed
from web_lead_agent.extract import extract_page
from web_lead_agent.idempotency import SQLiteIdempotencyStore, make_idempotency_key
from web_lead_agent.normalize import page_to_lead
from web_lead_agent.receipts import receipt_from_http
from web_lead_agent.runtime import RuntimeStore


class WebsiteContactFormAdapter:
    """获准域名 + 公开页面 + 人工批准 + 一次提交。"""

    def crawl_public_site(self, url: str, config: RuntimeConfig) -> PageEvidence:
        assert_target_allowed(url, config)
        request = Request(url, headers={"User-Agent": "web-lead-agent-v1-readonly"})
        with urlopen(request, timeout=config.timeout_seconds) as response:
            body = response.read().decode("utf-8", errors="replace")
        page = extract_page(url, body)
        assert_public_page_safe(page)
        return page

    def extract_company(self, page: PageEvidence):
        return page_to_lead(page)

    def locate_contact_form(self, page: PageEvidence) -> dict[str, object]:
        if not page.forms:
            raise PolicyViolation("contact_form_missing")
        marked = [
            form
            for form in page.forms
            if isinstance(form.get("markers"), dict)
            and form.get("markers", {}).get("data_contact_form") is True
        ]
        return marked[0] if marked else page.forms[0]

    def fill_contact_form(
        self,
        form: dict[str, object],
        lead: ScoredLead,
        draft: MessageDraft,
    ) -> SendAction:
        action_url = str(form.get("action") or lead.lead.contact_url)
        payload = build_form_payload(form, lead, draft)
        key = make_idempotency_key(
            lead.lead.domain,
            action_url,
            draft.body,
            "web_lead_minimal_loop_v1",
        )
        return SendAction(
            target_domain=lead.lead.domain,
            channel="website_contact_form",
            action="submit_once",
            send_limit=1,
            idempotency_key=key,
            target_url=action_url,
            payload=payload,
        )

    def submit_once(
        self,
        run_id: str,
        action: SendAction,
        approval: ApprovalDecision,
        config: RuntimeConfig,
        runtime: RuntimeStore,
        idempotency: SQLiteIdempotencyStore,
    ) -> SendReceipt:
        if config.mode != "supervised_single_send":
            return blocked_receipt(action, "runtime_mode_not_supervised_single_send")
        if not config.real_send_enabled:
            return blocked_receipt(action, "real_send_enabled_false")
        if not approval.approved:
            return blocked_receipt(action, f"approval_not_valid:{approval.reason}")
        parsed = urlparse(action.target_url)
        if (parsed.hostname or "").lower() not in config.allowed_domains:
            return blocked_receipt(action, "target_domain_not_allowlisted")
        if not idempotency.claim_or_block(action.idempotency_key, action.target_domain, action.target_url):
            return blocked_receipt(action, "duplicate_idempotency_key")
        if not runtime.claim_send_slot(run_id, action.target_domain, max_send=config.max_send_per_run):
            idempotency.finalize(action.idempotency_key, "BLOCKED_SEND_LIMIT")
            return blocked_receipt(action, "send_limit_exceeded")

        try:
            data = urlencode(action.payload).encode("utf-8")
            request = Request(
                action.target_url,
                data=data,
                headers={
                    "User-Agent": "web-lead-agent-v1-supervised",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                method="POST",
            )
            with urlopen(request, timeout=config.timeout_seconds) as response:
                body = response.read().decode("utf-8", errors="replace")
                receipt = receipt_from_http(
                    action.target_url,
                    action.idempotency_key,
                    response.status,
                    body,
                )
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            receipt = receipt_from_http(
                action.target_url,
                action.idempotency_key,
                exc.code,
                body,
            )
        except URLError as exc:
            receipt = receipt_from_http(
                action.target_url,
                action.idempotency_key,
                None,
                "",
                error=str(exc.reason),
            )
        except OSError as exc:
            receipt = receipt_from_http(
                action.target_url,
                action.idempotency_key,
                None,
                "",
                error=str(exc),
            )

        idempotency.finalize(action.idempotency_key, receipt.status)
        runtime.record_receipt(run_id, receipt)
        runtime.record_event(run_id, "submit_once_completed", asdict(receipt))
        return receipt


def build_form_payload(
    form: dict[str, object],
    lead: ScoredLead,
    draft: MessageDraft,
) -> dict[str, str]:
    fields = [str(field) for field in form.get("fields", [])]
    payload: dict[str, str] = {}
    for field in fields:
        lowered = field.lower()
        if "subject" in lowered:
            payload[field] = draft.subject
        elif "message" in lowered or "body" in lowered or "comment" in lowered:
            payload[field] = draft.body
        elif "company" in lowered:
            payload[field] = lead.lead.company_name
        elif "email" in lowered:
            payload[field] = "human-approved@example.invalid"
        elif "name" in lowered:
            payload[field] = "Human Reviewed Operator"
        else:
            payload[field] = draft.body
    if not payload:
        payload = {"message": draft.body}
    return payload


def blocked_receipt(action: SendAction, reason: str) -> SendReceipt:
    return SendReceipt(
        status="BLOCKED",
        http_status=None,
        target_url=action.target_url,
        idempotency_key=action.idempotency_key,
        reason=reason,
        retry_scheduled=False,
    )

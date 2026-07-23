"""人工审批闸门。"""

from __future__ import annotations

from web_lead_agent.contracts import (
    ApprovalDecision,
    ApprovalRequest,
    MessageDraft,
    PolicyResult,
    RuntimeConfig,
    ScoredLead,
)


def build_approval_request(
    lead: ScoredLead,
    draft: MessageDraft,
    policy: PolicyResult,
    config: RuntimeConfig,
) -> ApprovalRequest:
    """生成给用户/人工审核者看的审批包。"""

    return ApprovalRequest(
        target_domain=lead.lead.domain,
        channel=config.channel,
        message=draft.body,
        send_limit=1,
        policy_status=policy.status,
        risk_items=[*draft.risk_items, *policy.risk_items],
        knowledge_source_ids=draft.knowledge_source_ids,
        target_url=lead.lead.contact_url,
        account=config.approved_account,
    )


def evaluate_approval_payload(
    payload: dict[str, object] | None,
    request: ApprovalRequest,
    config: RuntimeConfig,
) -> ApprovalDecision:
    """所有显式批准字段同时满足时才允许一次提交。"""

    if not payload:
        return ApprovalDecision(approved=False, reason="approval_payload_missing")
    checks = {
        "approved": payload.get("approved") is True,
        "human_approval": payload.get("human_approval") is True,
        "approved_target_domain": payload.get("approved_target_domain") == request.target_domain,
        "approved_channel": payload.get("approved_channel") == request.channel,
        "approved_account": bool(payload.get("approved_account")),
        "approved_message": payload.get("approved_message") == request.message,
        "send_limit": payload.get("send_limit") == 1,
        "approved_action": payload.get("approved_action") == "submit_once",
        "runtime_mode": config.mode == "supervised_single_send",
    }
    failed = [name for name, ok in checks.items() if not ok]
    return ApprovalDecision(
        approved=not failed,
        reason="approved" if not failed else f"failed_checks:{','.join(failed)}",
        payload=dict(payload),
    )

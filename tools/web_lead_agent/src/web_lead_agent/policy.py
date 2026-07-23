"""确定性策略引擎：先阻断高风险词，再进入人工审批。"""

from __future__ import annotations

import re

from web_lead_agent.contracts import MessageDraft, PolicyResult, RuntimeConfig


RESTRICTED_TERMS = (
    "price",
    "quotation",
    "quote",
    "moq",
    "delivery",
    "payment",
    "exclusive",
    "contract",
    "refund",
    "complaint",
    "sample",
    "health",
    "medical",
    "low gi",
    "低 gi",
    "低gi",
    "价格",
    "报价",
    "交期",
    "付款",
    "样品",
    "代理",
    "合同",
    "认证",
    "检测",
    "效果承诺",
)


class DeterministicPolicyEngine:
    """不依赖模型自由判断的策略闸门。"""

    def evaluate(self, draft: MessageDraft, config: RuntimeConfig) -> PolicyResult:
        if config.mode == "bounded_autonomy":
            return PolicyResult(status="BLOCK_REPLY", blocked_reason="bounded_autonomy_forbidden")
        if draft.status == "BLOCKED_MISSING_KNOWLEDGE":
            return PolicyResult(
                status="BLOCK_REPLY",
                risk_items=draft.risk_items,
                blocked_reason="missing_product_knowledge",
            )
        if draft.status == "BLOCKED_CONFLICTING_KNOWLEDGE":
            return PolicyResult(
                status="ESCALATE_HUMAN",
                risk_items=draft.risk_items,
                blocked_reason="conflicting_product_knowledge",
            )
        restricted = find_restricted_terms(f"{draft.subject}\n{draft.body}")
        if restricted:
            return PolicyResult(status="REQUIRE_REVIEW", risk_items=restricted)
        return PolicyResult(status="ALLOW_DRAFT")


def find_restricted_terms(text: str) -> list[str]:
    """返回命中的受限词。"""

    lowered = text.lower()
    hits: list[str] = []
    for term in RESTRICTED_TERMS:
        pattern = re.escape(term.lower())
        if re.search(pattern, lowered):
            hits.append(term)
    return sorted(set(hits))

"""草稿生成：只使用已检索知识，不自行补业务事实。"""

from __future__ import annotations

from web_lead_agent.contracts import KnowledgeResult, MessageDraft, ScoredLead


class TemplateDraftAdapter:
    """确定性模板草稿，避免把未验证事实写进对外消息。"""

    def generate(self, lead: ScoredLead, knowledge: KnowledgeResult) -> MessageDraft:
        if knowledge.status == "MISSING":
            return MessageDraft(
                subject="",
                body="",
                knowledge_source_ids=[],
                status="BLOCKED_MISSING_KNOWLEDGE",
                risk_items=[f"missing:{topic}" for topic in knowledge.missing_topics],
            )
        if knowledge.status == "CONFLICT":
            return MessageDraft(
                subject="",
                body="",
                knowledge_source_ids=[],
                status="BLOCKED_CONFLICTING_KNOWLEDGE",
                risk_items=[f"conflict:{group}" for group in knowledge.conflicts],
            )
        source_ids = [item.source_id for item in knowledge.items]
        statements = {item.topic: item.statement for item in knowledge.items}
        company = lead.lead.company_name
        subject = f"Rice import cooperation inquiry for {company}"
        body = (
            f"Hello {company} team,\n\n"
            f"I found your public company page and noticed your work related to "
            f"{lead.lead.business_type or 'food distribution'}.\n\n"
            f"Our current public positioning: {finish_sentence(statements.get('product_positioning', ''))}\n"
            f"Reason for reaching out: {finish_sentence(statements.get('business_intent', ''))}\n\n"
            f"{statements.get('approved_cta')}\n\n"
            "Best regards,\n"
            "Human-reviewed project operator"
        )
        return MessageDraft(
            subject=subject,
            body=body,
            knowledge_source_ids=source_ids,
            status="DRAFT_READY",
            risk_items=[],
        )


def finish_sentence(text: str) -> str:
    """保证模板句子只保留一个结尾标点。"""

    clean = text.strip()
    if not clean:
        return ""
    if clean.endswith((".", "!", "?")):
        return clean
    return f"{clean}."

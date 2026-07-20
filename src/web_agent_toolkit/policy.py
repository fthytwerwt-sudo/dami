"""客户对话的确定性政策闸门和来源约束草稿器。"""

from __future__ import annotations

from .contracts import DraftResult, KnowledgeResult, PolicyResult


class DeterministicPolicyGate:
    """规则优先的政策判断；模型不得覆盖这些结果。"""

    _REVIEW_TERMS = {
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
    }

    def evaluate_policy(self, message: str, knowledge: KnowledgeResult) -> PolicyResult:
        """先处理知识状态，再处理商业、合规和承诺类关键词。"""

        if knowledge.status == "MISSING":
            return PolicyResult("BLOCK_REPLY", ["knowledge_missing"], True)
        if knowledge.status == "CONFLICT":
            return PolicyResult("ESCALATE_HUMAN", ["knowledge_conflict"], True)
        lowered = message.lower()
        matched = sorted(term for term in self._REVIEW_TERMS if term in lowered)
        if matched:
            return PolicyResult("REQUIRE_REVIEW", [f"restricted_term:{term}" for term in matched], True)
        return PolicyResult("ALLOW_DRAFT", ["sourced_non_restricted_request"], False)


def generate_draft(message: str, knowledge: KnowledgeResult) -> DraftResult:
    """只拼接受控知识内容；缺失或冲突时拒绝生成。"""

    if knowledge.status != "FOUND" or not knowledge.items:
        raise ValueError("只有 FOUND 且非空的知识结果可以生成草稿")
    statements = [str(item["statement"]) for item in knowledge.items]
    source_urls = list(dict.fromkeys(str(item["source_url"]) for item in knowledge.items))
    text = "Thank you for your message. " + " ".join(statements)
    return DraftResult(text=text, source_urls=source_urls)

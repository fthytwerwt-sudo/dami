"""共享契约（contracts）：定义 V1 闭环的数据形状和安全状态。"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from pathlib import Path
from typing import Any, Literal


Mode = Literal["draft_only", "supervised_single_send", "bounded_autonomy"]
KnowledgeStatus = Literal["FOUND", "MISSING", "CONFLICT"]
DraftStatus = Literal[
    "DRAFT_READY",
    "BLOCKED_MISSING_KNOWLEDGE",
    "BLOCKED_CONFLICTING_KNOWLEDGE",
]
PolicyStatus = Literal[
    "ALLOW_DRAFT",
    "REQUIRE_REVIEW",
    "ESCALATE_HUMAN",
    "BLOCK_REPLY",
]
ReceiptStatus = Literal["SUCCESS", "FAILED", "UNKNOWN", "BLOCKED"]


class PolicyViolation(ValueError):
    """违反公开网页、域名白名单或发送闸门时抛出。"""


@dataclass(frozen=True)
class RuntimeConfig:
    """运行配置：默认不允许真实发送。"""

    workspace_path: Path
    mode: Mode = "draft_only"
    real_send_enabled: bool = False
    allowed_domains: tuple[str, ...] = ("localhost", "127.0.0.1")
    task_id: str = "web_lead_minimal_loop_v1"
    channel: str = "website_contact_form"
    approved_account: str | None = None
    max_send_per_run: int = 1
    timeout_seconds: int = 10

    def __post_init__(self) -> None:
        if self.mode == "bounded_autonomy":
            raise PolicyViolation("bounded_autonomy is forbidden for V1")
        object.__setattr__(self, "workspace_path", Path(self.workspace_path))
        object.__setattr__(
            self,
            "allowed_domains",
            tuple(domain.lower().strip() for domain in self.allowed_domains),
        )


@dataclass
class PageEvidence:
    """公开网页回读证据。"""

    url: str
    domain: str
    html: str
    title: str = ""
    text: str = ""
    lead_fields: dict[str, str] = field(default_factory=dict)
    contact_links: list[str] = field(default_factory=list)
    forms: list[dict[str, Any]] = field(default_factory=list)
    external_subresources: list[str] = field(default_factory=list)


@dataclass
class LeadRecord:
    """企业线索结构化记录；仅可保存合成或获准公开信息。"""

    company_name: str
    domain: str
    source_url: str
    contact_url: str
    country: str = ""
    business_type: str = ""
    evidence: list[str] = field(default_factory=list)
    normalized_key: str = ""


@dataclass
class ScoredLead:
    """评分后的线索。"""

    lead: LeadRecord
    score: int
    qualified: bool
    reasons: list[str] = field(default_factory=list)


@dataclass
class KnowledgeItem:
    """产品知识库条目。"""

    source_id: str
    topic: str
    statement: str
    scope: str = "general"
    conflict_group: str = ""


@dataclass
class KnowledgeResult:
    """知识检索结果。"""

    status: KnowledgeStatus
    items: list[KnowledgeItem] = field(default_factory=list)
    missing_topics: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)


@dataclass
class MessageDraft:
    """个性化初稿。"""

    subject: str
    body: str
    knowledge_source_ids: list[str]
    status: DraftStatus = "DRAFT_READY"
    risk_items: list[str] = field(default_factory=list)


@dataclass
class PolicyResult:
    """确定性策略判断结果。"""

    status: PolicyStatus
    risk_items: list[str] = field(default_factory=list)
    blocked_reason: str = ""


@dataclass
class ApprovalRequest:
    """人工审批请求。"""

    target_domain: str
    channel: str
    message: str
    send_limit: int
    policy_status: str
    risk_items: list[str]
    knowledge_source_ids: list[str]
    target_url: str = ""
    account: str | None = None


@dataclass
class ApprovalDecision:
    """人工审批结果。"""

    approved: bool
    reason: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class SendAction:
    """一次受监督发送动作。"""

    target_domain: str
    channel: str
    action: str
    send_limit: int
    idempotency_key: str
    target_url: str
    payload: dict[str, str] = field(default_factory=dict)


@dataclass
class SendReceipt:
    """发送回执或页面结果。"""

    status: ReceiptStatus
    http_status: int | None
    target_url: str
    idempotency_key: str
    reason: str = ""
    retry_scheduled: bool = False


def to_plain(value: Any) -> Any:
    """把 dataclass / Path 递归转成可 JSON 序列化对象。"""

    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_plain(item) for item in value]
    return value

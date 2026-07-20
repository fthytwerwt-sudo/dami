"""跨 Adapter 的稳定数据契约。"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class PageEvidence:
    """网页读取证据，保留来源和抓取时间。"""

    source_url: str
    title: str
    text: str
    captured_at: str

    def to_dict(self) -> dict[str, Any]:
        """转换为可持久化字典。"""

        return asdict(self)


@dataclass(frozen=True)
class ToolAction:
    """工具动作结果；状态与细节分开保存。"""

    action: str
    status: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """转换为可持久化字典。"""

        return asdict(self)


@dataclass(frozen=True)
class KnowledgeResult:
    """知识召回结果，缺失和冲突必须显式表达。"""

    query: str
    scope: str
    status: str
    items: list[dict[str, Any]]
    conflicts: list[dict[str, Any]] = field(default_factory=list)
    requires_human: bool = False

    def to_dict(self) -> dict[str, Any]:
        """转换为可持久化字典。"""

        return asdict(self)


@dataclass(frozen=True)
class PolicyResult:
    """确定性政策闸门结果。"""

    decision: str
    reasons: list[str]
    requires_human: bool

    def to_dict(self) -> dict[str, Any]:
        """转换为可持久化字典。"""

        return asdict(self)


@dataclass(frozen=True)
class DraftResult:
    """带来源的草稿，不代表已批准或已发送。"""

    text: str
    source_urls: list[str]
    status: str = "DRAFT_PENDING_REVIEW"

    def to_dict(self) -> dict[str, Any]:
        """转换为可持久化字典。"""

        return asdict(self)


class WebAdapter(Protocol):
    """网页工具统一接口。"""

    def crawl_page(self, url: str) -> PageEvidence: ...

    def extract_company(self, url: str, selectors: dict[str, str]) -> dict[str, str]: ...

    def fill_web_form(self, url: str, values: dict[str, str]) -> ToolAction: ...

    def submit_message(self, action: ToolAction) -> ToolAction: ...

    def read_result(self, action: ToolAction) -> dict[str, Any]: ...


class KnowledgeAdapter(Protocol):
    """知识召回统一接口。"""

    def retrieve_knowledge(self, query: str, scope: str) -> KnowledgeResult: ...


class RuntimeAdapter(Protocol):
    """运行时状态统一接口。"""

    def save_checkpoint(self, thread_id: str, state: dict[str, Any]) -> None: ...

    def resume_run(self, thread_id: str) -> dict[str, Any]: ...

    def stop_run(self, thread_id: str, reason: str) -> dict[str, Any]: ...

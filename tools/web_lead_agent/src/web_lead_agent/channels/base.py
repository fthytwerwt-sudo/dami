"""通道基类契约。"""

from __future__ import annotations

from typing import Protocol

from web_lead_agent.contracts import PageEvidence, RuntimeConfig, SendReceipt


class ChannelAdapter(Protocol):
    """发送通道必须实现的最小接口。"""

    def crawl_public_site(self, url: str, config: RuntimeConfig) -> PageEvidence:
        ...

    def submit_once(self, *args: object, **kwargs: object) -> SendReceipt:
        ...

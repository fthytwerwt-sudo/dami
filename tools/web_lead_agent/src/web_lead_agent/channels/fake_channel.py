"""测试用 fake channel；不访问外部网络。"""

from __future__ import annotations

from web_lead_agent.contracts import RuntimeConfig, SendReceipt
from web_lead_agent.extract import extract_page


class FakeChannelAdapter:
    """用于单元测试的合成通道。"""

    def __init__(self, html: str, target_url: str = "http://localhost/") -> None:
        self.html = html
        self.target_url = target_url
        self.submit_calls = 0

    def crawl_public_site(self, url: str, config: RuntimeConfig):
        return extract_page(url or self.target_url, self.html)

    def submit_once(self, *args: object, **kwargs: object) -> SendReceipt:
        self.submit_calls += 1
        return SendReceipt(
            status="SUCCESS",
            http_status=200,
            target_url=self.target_url,
            idempotency_key="fake",
            reason="fake_success",
            retry_scheduled=False,
        )

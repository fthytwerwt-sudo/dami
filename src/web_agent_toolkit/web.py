"""基于 Playwright 的 localhost 网页和 DOM Adapter。"""

from __future__ import annotations

from datetime import UTC, datetime
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from .contracts import PageEvidence, ToolAction


class LocalOnlyViolation(ValueError):
    """当沙箱请求不是 localhost 时抛出。"""


class PlaywrightWebAdapter:
    """只读 localhost 页面，并允许填入但绝不提交表单。"""

    _LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}

    @classmethod
    def _is_local_url(cls, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and parsed.hostname in cls._LOCAL_HOSTS

    @classmethod
    def _assert_local(cls, url: str) -> None:
        if not cls._is_local_url(url):
            raise LocalOnlyViolation(f"沙箱只允许 localhost URL: {url}")

    @staticmethod
    def _launch_browser(playwright: object):
        """启动固定 Chromium；浏览器包异常时由 Playwright 原样报错。"""

        return playwright.chromium.launch(headless=True)

    @classmethod
    def _new_local_page(cls, browser: object):
        """创建阻断非 localhost 子资源和重定向的隔离页面。"""

        context = browser.new_context()

        def route_request(route: object) -> None:
            if cls._is_local_url(route.request.url):
                route.continue_()
            else:
                route.abort()

        context.route("**/*", route_request)
        return context, context.new_page()

    def crawl_page(self, url: str) -> PageEvidence:
        """读取页面标题和可见正文，不执行下载或外部导航。"""

        self._assert_local(url)
        with sync_playwright() as playwright:
            browser = self._launch_browser(playwright)
            try:
                context, page = self._new_local_page(browser)
                page.goto(url, wait_until="domcontentloaded")
                self._assert_local(page.url)
                return PageEvidence(
                    source_url=url,
                    title=page.title(),
                    text=page.locator("body").inner_text(),
                    captured_at=datetime.now(UTC).isoformat(),
                )
            finally:
                if "context" in locals():
                    context.close()
                browser.close()

    def extract_company(self, url: str, selectors: dict[str, str]) -> dict[str, str]:
        """用可审计的 ``data-testid`` 契约提取结构化企业字段。"""

        self._assert_local(url)
        with sync_playwright() as playwright:
            browser = self._launch_browser(playwright)
            try:
                context, page = self._new_local_page(browser)
                page.goto(url, wait_until="domcontentloaded")
                self._assert_local(page.url)
                return {
                    field: page.get_by_test_id(test_id).inner_text().strip()
                    for field, test_id in selectors.items()
                }
            finally:
                if "context" in locals():
                    context.close()
                browser.close()

    def fill_web_form(self, url: str, values: dict[str, str]) -> ToolAction:
        """按 label 填表并在浏览器关闭前验证未触发 submit。"""

        self._assert_local(url)
        with sync_playwright() as playwright:
            browser = self._launch_browser(playwright)
            try:
                context, page = self._new_local_page(browser)
                page.goto(url, wait_until="domcontentloaded")
                self._assert_local(page.url)
                filled: dict[str, str] = {}
                for label, value in values.items():
                    page.get_by_label(label, exact=True).fill(value)
                    filled[label] = page.get_by_label(label, exact=True).input_value()
                submit_count = int(page.evaluate("Number(window.__submitCount || 0)"))
                return ToolAction(
                    action="DOM_FILL",
                    status="FILLED_PENDING_SUBMIT",
                    details={"url": url, "filled": filled, "submit_count": submit_count},
                )
            finally:
                if "context" in locals():
                    context.close()
                browser.close()

    def submit_message(self, action: ToolAction) -> ToolAction:
        """真实提交是硬边界；无论输入为何都返回阻断状态。"""

        return ToolAction(
            action="SUBMIT_MESSAGE",
            status="BLOCK_SEND",
            details={
                "reason": "本工具仅支持 draft_only 与提交前验证",
                "previous_action": action.to_dict(),
            },
        )

    def read_result(self, action: ToolAction) -> dict[str, object]:
        """读取已发生动作结果，不触发新的页面或网络行为。"""

        return action.to_dict()

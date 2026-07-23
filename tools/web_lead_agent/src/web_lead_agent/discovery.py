"""目标网页发现和公开网页安全探测。"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from web_lead_agent.contracts import PageEvidence, PolicyViolation, RuntimeConfig


BLOCKED_PUBLIC_PAGE_KEYWORDS = (
    "login",
    "captcha",
    "password",
    "checkout",
    "payment",
)


@dataclass(frozen=True)
class TargetDiscovery:
    """目标网页准入结果。"""

    url: str
    domain: str
    allowed: bool
    reason: str


def discover_target(url: str, config: RuntimeConfig) -> TargetDiscovery:
    """确认目标 URL 是否在白名单域名内。"""

    parsed = urlparse(url)
    domain = (parsed.hostname or "").lower()
    if parsed.scheme not in {"http", "https"}:
        return TargetDiscovery(url=url, domain=domain, allowed=False, reason="unsupported_scheme")
    if domain not in config.allowed_domains:
        return TargetDiscovery(url=url, domain=domain, allowed=False, reason="domain_not_allowlisted")
    return TargetDiscovery(url=url, domain=domain, allowed=True, reason="allowlisted_public_domain")


def assert_target_allowed(url: str, config: RuntimeConfig) -> TargetDiscovery:
    """不通过时直接阻断，避免继续抓取或发送。"""

    discovery = discover_target(url, config)
    if not discovery.allowed:
        raise PolicyViolation(discovery.reason)
    return discovery


def assert_public_page_safe(page: PageEvidence) -> None:
    """公开页面探测：登录、验证码、付款等关键词直接阻断。"""

    lowered = f"{page.url}\n{page.title}\n{page.text}".lower()
    for keyword in BLOCKED_PUBLIC_PAGE_KEYWORDS:
        if keyword in lowered:
            raise PolicyViolation(f"blocked_public_page_keyword:{keyword}")
    if page.external_subresources:
        raise PolicyViolation("external_subresource_detected")

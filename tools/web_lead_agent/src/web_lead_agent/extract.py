"""公开网页解析：从 HTML 中提取企业资料、联系表单和风险证据。"""

from __future__ import annotations

from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from web_lead_agent.contracts import PageEvidence


class _LeadHTMLParser(HTMLParser):
    """小型 HTML parser，避免把浏览器自动化变成 V1 的核心依赖。"""

    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.base_domain = urlparse(base_url).hostname or ""
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.lead_fields: dict[str, str] = {}
        self.contact_links: list[str] = []
        self.forms: list[dict[str, object]] = []
        self.external_subresources: list[str] = []
        self._in_title = False
        self._active_field: str | None = None
        self._current_form: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        if tag == "title":
            self._in_title = True
        if "data-lead-field" in attr:
            self._active_field = attr["data-lead-field"].strip()
        if tag == "a" and attr.get("href"):
            href = urljoin(self.base_url, attr["href"])
            if "contact" in href.lower() or attr.get("data-contact-link") == "true":
                self.contact_links.append(href)
        if tag in {"script", "img", "link", "iframe"}:
            ref = attr.get("src") or attr.get("href")
            if ref:
                absolute = urljoin(self.base_url, ref)
                host = urlparse(absolute).hostname or ""
                if host and host != self.base_domain:
                    self.external_subresources.append(absolute)
        if tag == "form":
            self._current_form = {
                "action": urljoin(self.base_url, attr.get("action") or self.base_url),
                "method": (attr.get("method") or "GET").upper(),
                "fields": [],
                "markers": {
                    "data_contact_form": attr.get("data-contact-form") == "true"
                },
            }
        if tag in {"input", "textarea", "select"} and self._current_form is not None:
            name = attr.get("name") or attr.get("id")
            if name:
                fields = self._current_form.setdefault("fields", [])
                assert isinstance(fields, list)
                fields.append(name)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if self._active_field and tag not in {"input", "meta"}:
            self._active_field = None
        if tag == "form" and self._current_form is not None:
            self.forms.append(self._current_form)
            self._current_form = None

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if not clean:
            return
        self.text_parts.append(clean)
        if self._in_title:
            self.title_parts.append(clean)
        if self._active_field:
            existing = self.lead_fields.get(self._active_field, "")
            if existing == clean:
                return
            self.lead_fields[self._active_field] = " ".join(
                part for part in [existing, clean] if part
            ).strip()


def extract_page(url: str, html: str) -> PageEvidence:
    """解析网页并返回结构化证据。"""

    parser = _LeadHTMLParser(url)
    parser.feed(html)
    domain = urlparse(url).hostname or ""
    return PageEvidence(
        url=url,
        domain=domain,
        html=html,
        title=" ".join(parser.title_parts).strip(),
        text=" ".join(parser.text_parts).strip(),
        lead_fields=parser.lead_fields,
        contact_links=dedupe_preserve_order(parser.contact_links),
        forms=parser.forms,
        external_subresources=dedupe_preserve_order(parser.external_subresources),
    )


def dedupe_preserve_order(items: list[str]) -> list[str]:
    """保持顺序去重。"""

    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result

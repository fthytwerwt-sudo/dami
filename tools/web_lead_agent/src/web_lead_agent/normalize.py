"""线索结构化和去重。"""

from __future__ import annotations

from urllib.parse import urlparse

from web_lead_agent.contracts import LeadRecord, PageEvidence


def root_domain(url_or_domain: str) -> str:
    """生成去重键；localhost 保留端口前主机名。"""

    parsed = urlparse(url_or_domain if "://" in url_or_domain else f"http://{url_or_domain}")
    host = (parsed.hostname or url_or_domain).lower().strip()
    if host in {"localhost", "127.0.0.1"}:
        return host
    parts = host.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host


def page_to_lead(page: PageEvidence) -> LeadRecord:
    """把页面证据转换成企业线索。"""

    fields = page.lead_fields
    company = fields.get("company_name") or page.title or page.domain
    contact_url = fields.get("contact_url") or (page.contact_links[0] if page.contact_links else page.url)
    lead = LeadRecord(
        company_name=company.strip(),
        domain=root_domain(page.domain),
        source_url=page.url,
        contact_url=contact_url,
        country=fields.get("country", "").strip(),
        business_type=fields.get("business_type", "").strip(),
        evidence=[page.url, *page.contact_links],
    )
    lead.normalized_key = f"{lead.domain}|{lead.company_name.lower()}"
    return lead


def deduplicate_leads(leads: list[LeadRecord]) -> list[LeadRecord]:
    """按根域名去重，保留第一条证据。"""

    seen: set[str] = set()
    result: list[LeadRecord] = []
    for lead in leads:
        key = lead.domain
        if key in seen:
            continue
        seen.add(key)
        result.append(lead)
    return result

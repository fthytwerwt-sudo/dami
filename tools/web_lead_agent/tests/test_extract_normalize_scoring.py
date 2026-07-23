from __future__ import annotations

from pathlib import Path

from web_lead_agent.extract import extract_page
from web_lead_agent.normalize import deduplicate_leads, page_to_lead
from web_lead_agent.scoring import score_lead


SITE_ROOT = Path(__file__).resolve().parents[1] / "fixtures/synthetic_site"


def test_company_fields_are_extracted():
    html = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
    page = extract_page("http://127.0.0.1/index.html", html)
    assert page.lead_fields["company_name"] == "Pacific Pantry Imports"
    assert page.lead_fields["country"] == "Singapore"
    assert page.forms[0]["fields"] == ["name", "email", "company", "subject", "message"]
    assert page.contact_links == ["http://127.0.0.1/contact.html"]


def test_normalize_dedupe_and_score():
    html = (SITE_ROOT / "index.html").read_text(encoding="utf-8")
    lead = page_to_lead(extract_page("http://127.0.0.1/index.html", html))
    duplicate = page_to_lead(extract_page("http://127.0.0.1/other.html", html))
    deduped = deduplicate_leads([lead, duplicate])
    scored = score_lead(deduped[0])
    assert len(deduped) == 1
    assert deduped[0].domain == "127.0.0.1"
    assert scored.qualified is True
    assert scored.score >= 60

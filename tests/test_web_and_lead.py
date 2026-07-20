"""网页、DOM、潜客清洗与评分的行为测试。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from web_agent_toolkit.lead import deduplicate_leads, normalize_lead, score_lead
from web_agent_toolkit.web import LocalOnlyViolation, PlaywrightWebAdapter


def test_playwright_crawls_and_extracts_synthetic_company(synthetic_site_url: str) -> None:
    """真实 Chromium 应读取 localhost 页面并按 DOM 契约提取字段。"""

    adapter = PlaywrightWebAdapter()
    evidence = adapter.crawl_page(synthetic_site_url)
    company = adapter.extract_company(
        synthetic_site_url,
        {
            "company_name": "company-name",
            "country": "country",
            "business_type": "business-type",
            "category": "category",
        },
    )

    assert evidence.title == "SYNTHETIC 公司测试页"
    assert evidence.source_url == synthetic_site_url
    assert "not a real company" in evidence.text
    assert company["company_name"] == "SYNTHETIC Harbor Foods"


def test_dom_fill_stops_before_submit(synthetic_site_url: str) -> None:
    """DOM 可以填入批准草稿，但 submit_count 必须保持 0。"""

    adapter = PlaywrightWebAdapter()
    action = adapter.fill_web_form(
        synthetic_site_url,
        {"Message": "SYNTHETIC approved draft for a local test only."},
    )

    assert action.status == "FILLED_PENDING_SUBMIT"
    assert action.details["filled"]["Message"].startswith("SYNTHETIC")
    assert action.details["submit_count"] == 0
    assert adapter.submit_message(action).status == "BLOCK_SEND"


def test_web_adapter_rejects_non_local_url() -> None:
    """本轮沙箱不得访问 localhost 以外的 URL。"""

    with pytest.raises(LocalOnlyViolation):
        PlaywrightWebAdapter().crawl_page("https://external.synthetic.example")


def test_normalize_deduplicate_and_score_synthetic_leads() -> None:
    """同根域名应合并，错误国家应硬拒绝。"""

    fixture = Path(__file__).parent / "fixtures" / "synthetic_leads.json"
    leads = json.loads(fixture.read_text(encoding="utf-8"))
    normalized = [normalize_lead(item) for item in leads]
    deduped = deduplicate_leads(normalized)

    assert len(deduped) == 2
    harbor = next(item for item in deduped if item["root_domain"] == "harbor.synthetic.example")
    assert len(harbor["evidence_urls"]) == 2
    assert score_lead(harbor, "TEST_COUNTRY", "synthetic_distributor")["decision"] == "qualified"
    wrong = next(item for item in deduped if item["root_domain"] == "wrong.synthetic.example")
    assert score_lead(wrong, "TEST_COUNTRY", "synthetic_distributor")["decision"] == "rejected"

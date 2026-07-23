"""确定性线索评分。"""

from __future__ import annotations

from web_lead_agent.contracts import LeadRecord, ScoredLead


def score_lead(lead: LeadRecord) -> ScoredLead:
    """轻量评分：公开身份、国家、进口/分销相关性和联系入口。"""

    score = 0
    reasons: list[str] = []
    if lead.company_name:
        score += 20
        reasons.append("company_name_present")
    if lead.domain:
        score += 20
        reasons.append("domain_present")
    if lead.contact_url:
        score += 20
        reasons.append("contact_url_present")
    text = f"{lead.business_type} {lead.company_name}".lower()
    if any(word in text for word in ["import", "distributor", "wholesale", "buyer", "trading"]):
        score += 25
        reasons.append("buyer_or_distribution_signal")
    if lead.country:
        score += 15
        reasons.append("country_present")
    return ScoredLead(lead=lead, score=score, qualified=score >= 60, reasons=reasons)

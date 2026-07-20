"""潜客记录的确定性清洗、去重与评分。"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any


_COMPANY_SUFFIX = re.compile(r"\s+(ltd\.?|limited|inc\.?|llc|corp\.?|corporation)$", re.I)


def normalize_lead(record: dict[str, Any]) -> dict[str, Any]:
    """规范企业名和根域名，并把单一来源转成证据数组。"""

    normalized = deepcopy(record)
    raw_name = " ".join(str(record.get("company_name_raw", "")).split())
    normalized["company_name"] = _COMPANY_SUFFIX.sub("", raw_name).strip()
    normalized["root_domain"] = str(record.get("root_domain", "")).strip().lower().rstrip(".")
    source_url = str(record.get("source_url", "")).strip()
    normalized["evidence_urls"] = [source_url] if source_url else []
    normalized["normalization_status"] = "NORMALIZED" if normalized["root_domain"] else "MISSING_DOMAIN"
    return normalized


def deduplicate_leads(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """按根域名合并记录，并保留全部不重复来源证据。"""

    merged: dict[str, dict[str, Any]] = {}
    for record in records:
        key = str(record.get("root_domain", ""))
        if not key:
            key = f"missing-domain-{len(merged)}"
        if key not in merged:
            merged[key] = deepcopy(record)
            continue
        current = merged[key]
        current["evidence_urls"] = sorted(
            set(current.get("evidence_urls", [])) | set(record.get("evidence_urls", []))
        )
        for field in (
            "category_evidence",
            "import_distribution_evidence",
            "channel_fit_evidence",
            "public_contact_type",
        ):
            if not current.get(field) and record.get(field):
                current[field] = record[field]
    return list(merged.values())


def score_lead(record: dict[str, Any], target_country: str, target_buyer_type: str) -> dict[str, Any]:
    """对国家和买家类型做硬闸门，再按公开证据确定性打分。"""

    reasons: list[str] = []
    if record.get("country") != target_country:
        return {"score": 0, "decision": "rejected", "reasons": ["country_mismatch"]}
    if record.get("buyer_type_candidate") != target_buyer_type:
        return {"score": 0, "decision": "rejected", "reasons": ["buyer_type_mismatch"]}

    weights = {
        "category_evidence": 30,
        "import_distribution_evidence": 25,
        "channel_fit_evidence": 20,
        "public_contact_type": 15,
        "evidence_urls": 10,
    }
    score = 0
    for field, weight in weights.items():
        if record.get(field):
            score += weight
            reasons.append(field)
    decision = "qualified" if score >= 60 else "needs_review"
    return {"score": score, "decision": decision, "reasons": reasons}

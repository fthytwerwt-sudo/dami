from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def test_yaml_configs_parse_and_forbid_bounded_autonomy():
    policy = yaml.safe_load((ROOT / "config/policy_rules.yaml").read_text(encoding="utf-8"))
    channel = yaml.safe_load((ROOT / "config/channel_registry.example.yaml").read_text(encoding="utf-8"))
    domains = yaml.safe_load((ROOT / "config/allowed_domains.example.yaml").read_text(encoding="utf-8"))
    assert "bounded_autonomy" in policy["policy"]["modes"]["forbidden"]
    assert "bounded_autonomy" not in channel["channels"]["website_contact_form"]["mode_allowlist"]
    assert domains["allowed_domains"]


def test_schemas_validate_synthetic_examples():
    lead_schema = json.loads((ROOT / "schemas/lead_record.schema.json").read_text(encoding="utf-8"))
    knowledge_schema = json.loads((ROOT / "schemas/knowledge_result.schema.json").read_text(encoding="utf-8"))
    receipt_schema = json.loads((ROOT / "schemas/send_receipt.schema.json").read_text(encoding="utf-8"))
    lead = json.loads((ROOT / "fixtures/synthetic_leads.json").read_text(encoding="utf-8"))[0]
    Draft202012Validator.check_schema(lead_schema)
    Draft202012Validator(lead_schema).validate(lead)
    Draft202012Validator.check_schema(knowledge_schema)
    Draft202012Validator(receipt_schema).validate(
        {
            "status": "SUCCESS",
            "http_status": 200,
            "target_url": "http://127.0.0.1/submit",
            "idempotency_key": "x" * 64,
            "retry_scheduled": False,
        }
    )

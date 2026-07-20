"""Schema 和禁止边界的静态测试。"""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_FILES = [
    "lead_record.schema.json",
    "knowledge_result.schema.json",
    "conversation_state.schema.json",
    "tool_action.schema.json",
    "approval_request.schema.json",
]


def test_all_schemas_are_valid_and_have_chinese_descriptions() -> None:
    """所有 Schema 必须合法，且字段说明不能缺少中文。"""

    schema_dir = Path(__file__).parents[1] / "schemas"
    for filename in SCHEMA_FILES:
        schema = json.loads((schema_dir / filename).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        for definition in schema.get("properties", {}).values():
            description = definition.get("description", "")
            assert description
            assert any("\u4e00" <= char <= "\u9fff" for char in description)


def test_source_contains_no_send_or_evasion_implementation() -> None:
    """源码不得包含真实发送、验证码绕过、反检测或私有 API 实现。"""

    source_dir = Path(__file__).parents[1] / "src"
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_dir.rglob("*.py"))
    forbidden = ["smtp.send", "requests.post", "captcha_solver", "stealth_plugin", "private_api"]
    for token in forbidden:
        assert token not in source.lower()

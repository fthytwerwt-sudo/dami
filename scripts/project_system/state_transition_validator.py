#!/usr/bin/env python3
"""校验项目状态转换的证据、权限与禁止越级规则。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_json_component, validate_state_transition


if __name__ == "__main__":
    raise SystemExit(run_json_component("state_transition_validator", "校验状态转换。", validate_state_transition))

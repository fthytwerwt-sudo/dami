#!/usr/bin/env python3
"""校验完成接力、剩余工作和完成真实性，不让局部结果越级。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import run_json_component, validate_completion_relay


if __name__ == "__main__":
    raise SystemExit(run_json_component("completion_relay_validator", "校验 Completion Relay。", validate_completion_relay))

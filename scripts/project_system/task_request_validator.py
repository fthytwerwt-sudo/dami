#!/usr/bin/env python3
"""校验完整任务交接契约，含来源、权限、允许范围和 Public 安全边界。"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_route_decision, run_json_component


def validate(payload):
    """复用路由校验，并标记其作为 task_request validator 的结果。"""

    report = build_route_decision(payload)
    report["component"] = "task_request_validator"
    return report


if __name__ == "__main__":
    raise SystemExit(run_json_component("task_request_validator", "校验任务交接 JSON。", validate))

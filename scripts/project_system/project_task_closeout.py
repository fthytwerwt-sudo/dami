#!/usr/bin/env python3
"""串联交付清单、状态、完成真实性和 Git 收尾准备度的结束入口。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    enforce_component_schema,
    determine_write_required,
    load_json,
    make_report,
    output_report,
    validate_completion_relay,
    validate_git_closeout,
    validate_state_transition,
)


def build_closeout(payload: dict, *, fixture_mode: bool = False) -> dict:
    """以纯函数方式检查完成接力、状态转换和 Git 证据；CLI 默认真实回读。"""

    task_request = payload.get("task_request")
    write_required = determine_write_required(task_request) if isinstance(task_request, dict) else True
    completion_payload = {**(payload.get("completion_relay") or {}), "write_required": write_required}
    if isinstance(task_request, dict):
        completion_payload["task_request"] = task_request
    completion = enforce_component_schema("completion_relay_validator", validate_completion_relay(completion_payload))
    state = enforce_component_schema("state_transition_validator", validate_state_transition(payload.get("state_transition") or {}))
    if write_required:
        git = enforce_component_schema("git_closeout_validator", validate_git_closeout(payload.get("git_closeout") or {}, fixture_mode=fixture_mode))
    else:
        git = make_report(
            "git_closeout_validator",
            git_closeout={"required": False, "remote_match": None, "reason": "read-only task does not require commit or push"},
        )
    subreports = {"completion_relay": completion, "state_transition": state, "git_closeout": git}
    errors = sorted({code for report in subreports.values() for code in report.get("error_codes", [])})
    return make_report(
        "project_task_closeout",
        errors,
        closeout={
            "deliverable_inventory": completion.get("completion_relay", {}).get("required_output_inventory", []),
            "state_transition": state.get("state_transition"),
            "completion_truth": completion.get("completion_relay"),
            "remaining_work": completion.get("completion_relay", {}).get("remaining_work_check", {}),
            "write_required": write_required,
            "git_closeout_readiness": git.get("git_closeout"),
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="运行项目任务收尾检查；默认 dry-run，不进行 Git 写入。")
    parser.add_argument("--input", type=Path, help="含 completion_relay、state_transition 和 git_closeout 的 JSON 输入。")
    parser.add_argument("--output", type=Path, help="可选收尾报告路径；需配合 --execute。")
    parser.add_argument("--execute", action="store_true", help="允许向受控 audit 路径写入报告。")
    args = parser.parse_args(argv)
    if args.input is None:
        return output_report(make_report("project_task_closeout", ["blocked_input_missing"]), args.output, args.execute)
    try:
        payload = load_json(args.input)
    except (OSError, json.JSONDecodeError):
        return output_report(make_report("project_task_closeout", ["blocked_input_invalid"]), args.output, args.execute)
    report = build_closeout(payload) if isinstance(payload, dict) else make_report("project_task_closeout", ["blocked_input_invalid"])
    return output_report(report, args.output, args.execute)


if __name__ == "__main__":
    raise SystemExit(main())

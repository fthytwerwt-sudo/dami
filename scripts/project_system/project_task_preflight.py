#!/usr/bin/env python3
"""串联 v2 路由、工程深度、大任务、lane、供料与人工闸门的预检入口。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    build_engineering_depth,
    build_lane_decision,
    build_large_task_gate,
    build_process_boot,
    build_route_decision,
    build_supply_pack,
    build_workspace_governance,
    enforce_component_schema,
    load_json,
    load_schema,
    make_report,
    output_report,
    schema_validation_errors,
)


def build_preflight(task: dict) -> dict:
    """以纯函数方式串联预检，供 CLI 和 Fixture 使用；不会写入或执行外部动作。"""

    try:
        task_schema_errors = schema_validation_errors(task, load_schema("task_request.schema.json"))
    except (OSError, json.JSONDecodeError, ValueError):
        task_schema_errors = ["schema unavailable"]
    if task_schema_errors:
        return make_report("project_task_preflight", ["blocked_schema_validation_failed"], schema_validation={"schema": "task_request.schema.json", "errors": task_schema_errors, "status": "blocked"})

    # 每个子报告只读取相同的脱敏 task contract，不会执行外部动作。
    route = enforce_component_schema("route_decision_builder", build_route_decision(task))
    depth = enforce_component_schema("engineering_depth_router", build_engineering_depth(task))
    large = build_large_task_gate(task)
    lane_input = {
        "lane_recommendation": task.get("lane_recommendation"),
        "lanes": task.get("lanes", []),
        "write_owner": task.get("write_owner", "single_integrator"),
        "integration_owner": task.get("integration_owner", "single_integrator"),
        "write_required": True,
    }
    lane = build_lane_decision(lane_input)
    workspace = build_workspace_governance(task, route.get("route_decision", {}).get("planned_files", []))
    supply_input = task.get("supply_pack_input") or {
        "task_goal": task.get("goal"),
        "current_state": task.get("current_state", "unknown"),
        "must_read_sources": task.get("must_read_sources", []),
        "constraints": task.get("constraints", []),
        "source_conflicts": task.get("source_conflicts", []),
        "missing_information": task.get("missing_information", []),
        "allowed_actions": task.get("allowed_actions", []),
        "forbidden_actions": task.get("forbidden_actions", []),
    }
    supply = enforce_component_schema("source_supply_pack_builder", build_supply_pack(supply_input))
    process = enforce_component_schema(
        "process_boot_builder",
        build_process_boot(
            {
                "route_decision_status": route.get("status"),
                "source_readback_status": supply.get("pre_task_supply_pack", {}).get("source_readback_status"),
                "source_conflicts": supply_input.get("source_conflicts", []),
                "task_goal": task.get("goal"),
                "current_state": task.get("current_state"),
                "must_read_sources": task.get("must_read_files"),
                "supply_summary": task.get("source_summary"),
                "failure_route": task.get("failure_route"),
                "record_location": task.get("record_location"),
            }
        ),
    )
    subreports = {"route_decision": route, "engineering_depth": depth, "large_task_gate": large, "lane_decision": lane, "workspace_check": workspace, "supply_check": supply, "process_boot": process}
    errors = sorted({code for report in subreports.values() for code in report.get("error_codes", [])})
    return make_report(
        "project_task_preflight",
        errors,
        preflight={
            "route_decision": route.get("route_decision"),
            "engineering_depth": depth.get("engineering_depth"),
            "large_task_gate": large.get("large_task_gate"),
            "lane_decision": lane.get("lane_decision"),
            "workspace_check": workspace.get("workspace_check"),
            "supply_check": supply.get("pre_task_supply_pack"),
            "process_boot": process.get("process_boot_report"),
            "must_read_validation": route.get("status"),
            "scope_validation": route.get("status"),
            "per_file_plan_validation": route.get("status"),
            "human_gate_check": "pass" if not errors else "blocked_by_subreport",
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="运行项目任务预检；默认 dry-run，不修改任务文件。")
    parser.add_argument("--input", type=Path, help="符合 task_request.schema.json 的 JSON 输入。")
    parser.add_argument("--output", type=Path, help="可选预检报告路径；需配合 --execute。")
    parser.add_argument("--execute", action="store_true", help="允许向受控 audit 路径写入报告。")
    args = parser.parse_args(argv)
    if args.input is None:
        return output_report(make_report("project_task_preflight", ["blocked_input_missing"]), args.output, args.execute)
    try:
        task = load_json(args.input)
    except (OSError, json.JSONDecodeError):
        return output_report(make_report("project_task_preflight", ["blocked_input_invalid"]), args.output, args.execute)
    report = build_preflight(task) if isinstance(task, dict) else make_report("project_task_preflight", ["blocked_input_invalid"])
    return output_report(report, args.output, args.execute)


if __name__ == "__main__":
    raise SystemExit(main())

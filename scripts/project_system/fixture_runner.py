#!/usr/bin/env python3
"""执行 v2 协作运行内核的脱敏 Fixture 套件。

默认只读 Fixture 并打印 JSON；不写项目文件、不调用网络或外部业务服务。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    INPUT_SCHEMAS,
    build_engineering_depth,
    build_lane_decision,
    build_large_task_gate,
    build_mechanism_triggers,
    build_mid_task_supply,
    build_process_boot,
    build_route_decision,
    build_supply_pack,
    enforce_component_schema,
    json_text,
    load_schema,
    make_report,
    resolve_failure_route,
    schema_validation_errors,
    validate_completion_relay,
    validate_git_closeout,
    validate_per_file_plan,
    validate_state_transition,
)
from project_task_closeout import build_closeout
from project_task_preflight import build_preflight


COMPONENTS = {
    "route_decision_builder": build_route_decision,
    "task_request_validator": build_route_decision,
    "engineering_depth_router": build_engineering_depth,
    "large_task_gate": build_large_task_gate,
    "lane_parallel_router": build_lane_decision,
    "process_boot_builder": build_process_boot,
    "mechanism_trigger_router": build_mechanism_triggers,
    "source_supply_pack_builder": build_supply_pack,
    "mid_task_supply_builder": build_mid_task_supply,
    "per_file_plan_validator": validate_per_file_plan,
    "state_transition_validator": validate_state_transition,
    "completion_relay_validator": validate_completion_relay,
    "failure_route_resolver": resolve_failure_route,
    "git_closeout_validator": lambda payload: validate_git_closeout(payload, fixture_mode=True),
    "project_task_preflight": build_preflight,
    "project_task_closeout": lambda payload: build_closeout(payload, fixture_mode=True),
}

REQUIRED_OUTPUT_BY_COMPONENT = {
    "route_decision_builder": ["route_decision"],
    "task_request_validator": ["route_decision"],
    "engineering_depth_router": ["engineering_depth"],
    "large_task_gate": ["large_task_gate"],
    "lane_parallel_router": ["lane_decision"],
    "process_boot_builder": ["process_boot_report"],
    "mechanism_trigger_router": ["triggered_mechanisms_and_habits"],
    "source_supply_pack_builder": ["pre_task_supply_pack"],
    "mid_task_supply_builder": ["mid_task_supply_pack"],
    "per_file_plan_validator": ["planned_files"],
    "state_transition_validator": ["state_transition"],
    "completion_relay_validator": ["completion_relay"],
    "failure_route_resolver": ["failure_route"],
    "git_closeout_validator": ["git_closeout"],
    "project_task_preflight": ["preflight"],
    "project_task_closeout": ["closeout"],
}


def run_fixture(path: Path) -> dict:
    """运行单一 Fixture，并将实际 status/error_codes 与预期逐项对读。"""

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"fixture": path.name, "passed": False, "failures": [f"fixture_parse_error: {exc}"]}

    failures = []
    checks = []
    if not payload.get("component_inputs") or not payload.get("expected"):
        failures.append("fixture must declare non-empty component_inputs and expected results")
    for component, component_input in payload.get("component_inputs", {}).items():
        builder = COMPONENTS.get(component)
        expected = payload.get("expected", {}).get(component)
        if builder is None or expected is None:
            failures.append(f"{component}: missing component mapping or expectation")
            continue
        input_schema = INPUT_SCHEMAS.get(component)
        if input_schema:
            try:
                input_errors = schema_validation_errors(component_input, load_schema(input_schema))
            except (OSError, json.JSONDecodeError, ValueError):
                input_errors = ["schema unavailable"]
            if input_errors:
                actual = make_report(
                    component,
                    ["blocked_schema_validation_failed"],
                    schema_validation={"schema": input_schema, "errors": input_errors, "status": "blocked"},
                )
            else:
                actual = enforce_component_schema(component, builder(component_input))
        else:
            actual = enforce_component_schema(component, builder(component_input))
        actual_codes = sorted(actual.get("error_codes", []))
        expected_codes = sorted(expected.get("error_codes", []))
        required_keys = expected.get("required_output_keys", REQUIRED_OUTPUT_BY_COMPONENT.get(component, []))
        output_keys_present = all(key in actual for key in required_keys)
        matched = actual.get("status") == expected.get("status") and actual_codes == expected_codes and output_keys_present
        checks.append(
            {
                "component": component,
                "passed": matched,
                "actual_status": actual.get("status"),
                "actual_error_codes": actual_codes,
                "expected_status": expected.get("status"),
                "expected_error_codes": expected_codes,
                "required_output_keys": required_keys,
                "output_keys_present": output_keys_present,
            }
        )
        if not matched:
            failures.append(f"{component}: expected {expected.get('status')} {expected_codes}, got {actual.get('status')} {actual_codes}")
    return {"fixture": path.name, "case_id": payload.get("case_id"), "passed": not failures, "checks": checks, "failures": failures}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="运行 v2 协作系统 Fixture 套件（默认只读）。")
    parser.add_argument("--fixtures-dir", type=Path, default=Path(__file__).resolve().parents[2] / "project_system" / "fixtures", help="Fixture 目录。")
    args = parser.parse_args(argv)
    results = [run_fixture(path) for path in sorted(args.fixtures_dir.glob("*.json"))]
    report = {
        "component": "fixture_runner",
        "status": "pass" if results and all(result["passed"] for result in results) else "blocked",
        "fixture_count": len(results),
        "passed_count": sum(result["passed"] for result in results),
        "blocked_count": sum(not result["passed"] for result in results),
        "results": results,
        "dry_run": True,
    }
    sys.stdout.write(json_text(report) + "\n")
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())

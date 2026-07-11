#!/usr/bin/env python3
"""大米低 GI 跨境项目 v2 协作运行内核的公共实现。

本模块只处理脱敏 JSON 契约、路由和验证；不会读取密钥、调用外部业务 API，
也不会在未显式指定 --execute 时写入文件。机器字段保持英文，报告同时给出中文说明。
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


EXIT_OK = 0
EXIT_BLOCKED = 2

VALID_TASK_TYPES = {
    "project_file_change",
    "mechanism_or_route_fix",
    "research",
    "compliance_review",
    "product_fact_intake",
    "data_processing",
    "copywriting_or_drafting",
    "channel_validation",
    "experiment_design",
    "code_debug",
    "local_file_governance",
    "external_action_proposal",
    "audit",
    "runtime_kernel_implementation",
    "gpt_project_sync",
}

VALID_RESPONSIBILITY_LAYERS = {
    "entry_routing_layer",
    "project_judgment_layer",
    "engineering_design_layer",
    "execution_layer",
    "validation_layer",
    "sync_layer",
    "mechanism_fix_layer",
    "multi_lane_layer",
}

VALID_READ_STATUSES = {"read_ok", "missing", "unreadable", "not_applicable"}
VALID_DEPTHS = {"L0_light_chat", "L1_task_card", "L2_node_contract", "L3_system_line"}
VALID_LANE_RECOMMENDATIONS = {"serial_only", "read_parallel", "explore_plus_integrate", "true_multi_task_parallel"}
VALID_LANE_MODES = {"read_only", "write"}
WRITE_TASK_TYPES = {"project_file_change", "mechanism_or_route_fix", "runtime_kernel_implementation", "gpt_project_sync"}
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
REQUIRED_REMOTE_READBACK_PATHS = {
    "AGENTS.md",
    "project_system/01_MECHANISM_REGISTRY.json",
    "project_system/02_跨项目操作习惯注册表_cross_project_operating_habits.json",
    "project_system/rules/12_完整工程线_engineering_line.md",
    "gpt_project_sync/latest/package_manifest.json",
}
GIT_FORBIDDEN_DIRECTORY_SEGMENTS = {
    ".omx",
    "foreign_trade_low_gi_plan",
    "private",
    "project_local",
    "secrets",
}
GIT_SECRET_PATTERNS = {
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "bearer_token": r"Bearer\s+[A-Za-z0-9._-]{12,}",
    "common_api_key": r"(?:sk-[A-Za-z0-9_-]{20,}|sk_(?:live|proj)_[A-Za-z0-9_-]{16,}|rk_(?:live|test)_[A-Za-z0-9_-]{16,}|pk_(?:live|test)_[A-Za-z0-9_-]{16,})",
}
GIT_SENSITIVE_PATTERNS = {
    "absolute_path": r"(?:/(?:Users|private|Volumes|home)/|[A-Za-z]:\\)",
    "email_address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    # 保守匹配国际号码、中文手机号和带分段的北美号码，避免把日期或机制编号误判为个人电话。
    "phone_number": r"(?:\+[1-9]\d{7,14}|(?:\+?86[- ]?)?1[3-9]\d{9}|\(?\d{3}\)?[- ]\d{3}[- ]\d{4})",
}
VALID_STATES = {
    "collaboration_system_activation",
    "product_fact_collection",
    "product_evidence_validation",
    "market_screening",
    "compliance_validation",
    "b2b_channel_validation",
    "b2c_channel_validation",
    "lead_generation_test",
    "offer_validation",
    "pilot_execution",
    "scale_or_stop",
    "human_decision_required",
    "blocked",
    "cross_project_collaboration_system_v2_active",
}

ALLOWED_STATE_TRANSITIONS = {
    "collaboration_system_activation": {"cross_project_collaboration_system_v2_active", "product_fact_collection", "human_decision_required", "blocked"},
    "cross_project_collaboration_system_v2_active": {"product_fact_collection", "human_decision_required", "blocked"},
    "product_fact_collection": {"product_evidence_validation", "human_decision_required", "blocked"},
    "product_evidence_validation": {"market_screening", "compliance_validation", "human_decision_required", "blocked"},
    "market_screening": {"compliance_validation", "human_decision_required", "blocked"},
    "compliance_validation": {"b2b_channel_validation", "b2c_channel_validation", "human_decision_required", "blocked"},
    "b2b_channel_validation": {"lead_generation_test", "offer_validation", "human_decision_required", "blocked"},
    "b2c_channel_validation": {"lead_generation_test", "offer_validation", "human_decision_required", "blocked"},
    "lead_generation_test": {"offer_validation", "b2b_channel_validation", "b2c_channel_validation", "blocked"},
    "offer_validation": {"pilot_execution", "human_decision_required", "blocked"},
    "pilot_execution": {"scale_or_stop", "human_decision_required", "blocked"},
    "scale_or_stop": {"pilot_execution", "human_decision_required", "blocked"},
    "human_decision_required": {"product_fact_collection", "market_screening", "compliance_validation", "b2b_channel_validation", "b2c_channel_validation", "offer_validation", "pilot_execution", "blocked"},
    "blocked": set(),
}

BASELINE_CURRENT_READS = {
    "AGENTS.md",
    "project_system/current/CURRENT_PROJECT_STATE.md",
    "project_system/current/CURRENT_FORMAL_FACTS.md",
    "project_system/current/CURRENT_DECISIONS.md",
    "project_system/current/LATEST_TASK_STATUS.md",
}

REQUIRED_TASK_FIELDS = (
    "goal",
    "context",
    "source_of_truth",
    "constraints",
    "allowed_files",
    "forbidden_files",
    "external_actions",
    "human_gates",
    "execution_steps",
    "validation",
    "done_when",
    "blocked_if",
    "output",
    "task_type",
    "responsibility_layer",
    "must_read_files",
)

WRITE_TASK_CONTRACT_FIELDS = (
    "implementation_design",
    "impact_check",
    "supply_pack",
    "failure_routes",
    "rollback",
    "completion_relay",
    "git_closeout",
    "workspace_mode",
    "external_workspace_required",
    "worktree_requested",
)

PER_FILE_PLAN_FIELDS = (
    "purpose",
    "layer",
    "inputs",
    "outputs",
    "core_decisions",
    "trigger_conditions",
    "route_rules",
    "missing_info_policy",
    "conflict_policy",
    "blocked_if",
    "examples",
    "validation",
    "user_review_points",
)

ENGINEERING_LINE_LAYERS = [
    {"id": 0, "name": "project_goal_layer", "中文用途": "项目目标层"},
    {"id": 1, "name": "current_task_awareness_layer", "中文用途": "当前任务意识层"},
    {"id": 2, "name": "process_node_layer", "中文用途": "流程节点层"},
    {"id": 3, "name": "cleaning_layer", "中文用途": "清洗层"},
    {"id": 4, "name": "structuring_layer", "中文用途": "结构化层"},
    {"id": 5, "name": "source_retrieval_layer", "中文用途": "资料召回层"},
    {"id": 6, "name": "tool_connection_layer", "中文用途": "工具连接层"},
    {"id": 7, "name": "execution_node_layer", "中文用途": "执行节点层"},
    {"id": 8, "name": "evaluation_layer", "中文用途": "判断评估层"},
    {"id": 9, "name": "failure_route_layer", "中文用途": "失败路由层"},
    {"id": 10, "name": "human_fallback_layer", "中文用途": "人工兜底层"},
    {"id": 11, "name": "state_record_layer", "中文用途": "状态记录层"},
    {"id": 12, "name": "retrospective_iteration_layer", "中文用途": "复盘迭代层"},
]


def project_root() -> Path:
    """从脚本位置推导项目根目录，避免把机器绝对路径写入报告。"""

    return Path(__file__).resolve().parents[2]


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def load_json(path: Path) -> Any:
    """读取 JSON 输入；只读取显式传入的文件。"""

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_repository_path(value: Any) -> str | None:
    """仅接受项目根目录内的相对文件路径，拒绝绝对路径、父目录与空值。"""

    if not isinstance(value, str) or not value.strip():
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return None
    normalized = path.as_posix().rstrip("/")
    return normalized or None


def path_matches_scope(path: str, scope: str) -> bool:
    """判断一个规范相对路径是否落在精确文件、目录或受控 glob 范围内。"""

    normalized_scope = normalize_repository_path(scope)
    if normalized_scope is None:
        return False
    return path == normalized_scope or path.startswith(normalized_scope + "/") or fnmatch.fnmatch(path, normalized_scope)


def safe_audit_output_path(output: Path) -> Path | None:
    """普通组件仅能写项目 audit 顶层 JSON，不能覆写 Fixture、GPT 包或规则。"""

    if output.is_absolute() or ".." in output.parts or output.suffix != ".json":
        return None
    root = project_root().resolve()
    audit_root = (root / "project_system" / "audit").resolve()
    candidate = (root / output).resolve(strict=False)
    if not candidate.is_relative_to(audit_root) or candidate.parent != audit_root:
        return None
    # 已有目标或父目录不能是软链接，避免 --execute 通过别名逃逸。
    raw_candidate = root / output
    if raw_candidate.is_symlink() or raw_candidate.parent.is_symlink():
        return None
    return candidate


def output_report(report: dict[str, Any], output: Path | None, execute: bool) -> int:
    """打印报告；只允许成功 dry-run 结果显式写到受控 audit JSON 路径。"""

    report["dry_run"] = not execute
    if output is not None:
        resolved = safe_audit_output_path(output)
        if resolved is None:
            report["status"] = "blocked"
            report.setdefault("error_codes", []).append("blocked_write_scope_violation")
            report.setdefault("messages", []).append("组件报告只能写入项目 audit 顶层的相对 .json 路径。")
        elif execute and report.get("status") == "pass":
            report["output_write"] = "written"
            resolved.write_text(json_text(report) + "\n", encoding="utf-8")
        elif execute:
            report["output_write"] = "not_written_blocked_report"
        else:
            report["output_write"] = "dry_run_not_written"

    report["error_codes"] = sorted(set(report.get("error_codes", [])))
    report["messages"] = [error_message(code) for code in report["error_codes"]]
    sys.stdout.write(json_text(report) + "\n")
    return EXIT_OK if report.get("status") == "pass" else EXIT_BLOCKED


def make_report(component: str, errors: list[str] | None = None, **payload: Any) -> dict[str, Any]:
    """统一报告结构，让所有脚本输出可机器读取的状态与中文说明。"""

    errors = errors or []
    return {
        "component": component,
        "status": "pass" if not errors else "blocked",
        "error_codes": errors,
        "messages": [error_message(code) for code in errors],
        **payload,
    }


def error_message(code: str) -> str:
    """将稳定的英文错误码映射为可读中文说明。"""

    messages = {
        "blocked_input_missing": "缺少 JSON 输入，默认 dry-run 不能继续。",
        "blocked_input_invalid": "输入不是可解析的 JSON 对象。",
        "blocked_schema_validation_failed": "JSON 数据不符合正式 Schema 契约。",
        "blocked_task_contract_incomplete": "任务交接契约字段不完整。",
        "blocked_unknown_task_type": "任务类型不在正式枚举中。",
        "blocked_unknown_responsibility_layer": "责任层级不在正式枚举中。",
        "blocked_source_missing": "必读来源缺失或不可读。",
        "blocked_repo_visibility_for_sensitive_data": "Public 仓库不能写入敏感商业或个人数据。",
        "blocked_authorization_required": "外部动作或重大决定缺少授权。",
        "blocked_engineering_depth_invalid": "工程深度选择不符合任务信号。",
        "blocked_large_task_lane_missing": "大任务缺少可执行的车道选择。",
        "blocked_multi_lane_write_conflict": "多个车道同时拥有写入权，必须收敛为单一写入者。",
        "blocked_per_file_plan_incomplete": "单文件细节方案缺少必填字段。",
        "blocked_supply_repair": "执行资料包缺少原文件回读、关键片段或冲突裁决。",
        "blocked_fact_conflict": "来源冲突尚未裁决。",
        "blocked_state_transition_invalid": "状态转换缺少证据或越过人工闸门。",
        "blocked_completion_claim_repair": "完成声明越过了实际交付、验证或同步证据。",
        "blocked_git_closeout_repair": "Git 收尾缺少精确暂存、扫描、推送或远端回读证据。",
        "blocked_remote_readback_failed": "本地、origin/main 与远端引用不一致或关键文件不可回读。",
        "blocked_write_scope_violation": "写入路径不在本轮允许范围。",
        "blocked_external_workspace_required": "任务需要额外工作区、worktree 或项目根目录外的正式输出，不能在单工作区规则下继续。",
    }
    return messages.get(code, "运行内核检测到需要修复的阻断条件。")


def list_value(value: Any) -> list[Any]:
    """兼容单值与列表输入，但不给缺失字段自动补值。"""

    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def has_sensitive_flag(payload: dict[str, Any]) -> bool:
    """只依据显式脱敏标记判断，避免把规则文本中的敏感词误判为真实敏感数据。"""

    return bool(
        payload.get("contains_sensitive_business_data")
        or payload.get("sensitive_data_detected")
        or payload.get("contains_personal_data")
    )


def safe_nonnegative_int(value: Any) -> int | None:
    """解析非负整数；非法类型返回 None 而不是抛出未结构化异常。"""

    if isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def plan_paths_from_document(plan: dict[str, Any]) -> list[str]:
    """从 per-file plan 提取每个显式声明的路径。"""

    paths: list[str] = []
    for group in plan.get("plan_groups") or plan.get("plans") or []:
        if not isinstance(group, dict):
            continue
        values = group.get("paths") or ([group["path"]] if group.get("path") else [])
        paths.extend(value for value in values if isinstance(value, str))
    return paths


def load_per_file_plan_from_task(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    """只读取项目内显式授权的 per_file_plan 路径，返回文档或结构化错误码。"""

    if isinstance(payload.get("per_file_plan"), dict):
        return payload["per_file_plan"], []
    raw_path = payload.get("per_file_plan_path")
    if raw_path is None:
        return None, []
    normalized = normalize_repository_path(raw_path)
    if normalized is None:
        return None, ["blocked_write_scope_violation"]
    candidate = (project_root() / normalized).resolve(strict=False)
    if not candidate.is_relative_to(project_root().resolve()) or not candidate.is_file() or candidate.is_symlink():
        return None, ["blocked_per_file_plan_incomplete"]
    try:
        plan = load_json(candidate)
    except (OSError, json.JSONDecodeError):
        return None, ["blocked_per_file_plan_incomplete"]
    return plan if isinstance(plan, dict) else None, [] if isinstance(plan, dict) else ["blocked_per_file_plan_incomplete"]


def task_request_details(payload: dict[str, Any]) -> tuple[list[str], list[str]]:
    """校验任务交接并返回错误码与已授权的精确待改路径。"""

    errors: list[str] = []
    planned_paths: list[str] = []
    if not isinstance(payload, dict):
        return ["blocked_input_invalid"], planned_paths

    required_nonempty = {
        "goal", "context", "source_of_truth", "constraints", "allowed_files", "forbidden_files",
        "execution_steps", "validation", "done_when", "blocked_if", "output", "task_type",
        "responsibility_layer", "must_read_files",
    }
    if any(field not in payload or payload.get(field) is None for field in REQUIRED_TASK_FIELDS) or any(
        not payload.get(field) for field in required_nonempty
    ):
        errors.append("blocked_task_contract_incomplete")

    task_types = list_value(payload.get("task_type"))
    if any(item not in VALID_TASK_TYPES for item in task_types):
        errors.append("blocked_unknown_task_type")
    layers = list_value(payload.get("responsibility_layer"))
    if any(item not in VALID_RESPONSIBILITY_LAYERS for item in layers):
        errors.append("blocked_unknown_responsibility_layer")

    must_read = list_value(payload.get("must_read_files"))
    read_ok_paths: set[str] = set()
    if not must_read:
        errors.append("blocked_source_missing")
    for source in must_read:
        if not isinstance(source, dict) or not isinstance(source.get("path"), str) or not source.get("path").strip():
            errors.append("blocked_source_missing")
            continue
        status = source.get("read_status")
        if status not in VALID_READ_STATUSES or status in {"missing", "unreadable"}:
            errors.append("blocked_source_missing")
            continue
        if status == "read_ok":
            read_ok_paths.add(source["path"])
    if not read_ok_paths:
        errors.append("blocked_source_missing")

    direct_paths = list_value(payload.get("will_modify_files"))
    repository_write_requested = payload.get("repository_write_requested")
    if repository_write_requested not in {None, True, False}:
        errors.append("blocked_task_contract_incomplete")
    # 既有明确写入类型、显式写入标记和待改路径三者任一命中，都必须进入写入闸门；
    # 不能让 code_debug 等任务类型通过遗漏标记绕开单文件方案。
    write_requested = bool(
        set(task_types).intersection(WRITE_TASK_TYPES)
        or repository_write_requested is True
        or direct_paths
    )
    if write_requested and any(
        field not in payload or payload.get(field) is None or payload.get(field) == "" or payload.get(field) == [] or payload.get(field) == {}
        for field in WRITE_TASK_CONTRACT_FIELDS
    ):
        errors.append("blocked_task_contract_incomplete")
    if write_requested and not BASELINE_CURRENT_READS.issubset(read_ok_paths):
        errors.append("blocked_source_missing")

    allowed_scopes = [scope for scope in list_value(payload.get("allowed_files")) if isinstance(scope, str)]
    forbidden_scopes = [scope for scope in list_value(payload.get("forbidden_files")) if isinstance(scope, str)]
    if not allowed_scopes or any(normalize_repository_path(scope) is None for scope in allowed_scopes + forbidden_scopes):
        errors.append("blocked_write_scope_violation")

    plan, plan_errors = load_per_file_plan_from_task(payload)
    errors.extend(plan_errors)
    if write_requested and plan is None:
        errors.append("blocked_per_file_plan_incomplete")
    if plan is not None:
        plan_report = validate_per_file_plan(plan)
        errors.extend(plan_report.get("error_codes", []))
        planned_paths.extend(plan_report.get("planned_files", []))
    if direct_paths and any(not isinstance(path, str) for path in direct_paths):
        errors.append("blocked_write_scope_violation")
    planned_paths.extend(path for path in direct_paths if isinstance(path, str))
    if write_requested and not planned_paths:
        errors.append("blocked_per_file_plan_incomplete")

    normalized_planned: list[str] = []
    for path in planned_paths:
        normalized = normalize_repository_path(path)
        if normalized is None:
            errors.append("blocked_write_scope_violation")
            continue
        normalized_planned.append(normalized)
        if not any(path_matches_scope(normalized, scope) for scope in allowed_scopes):
            errors.append("blocked_write_scope_violation")
        if any(path_matches_scope(normalized, scope) for scope in forbidden_scopes):
            errors.append("blocked_write_scope_violation")
    if len(normalized_planned) != len(set(normalized_planned)):
        errors.append("blocked_per_file_plan_incomplete")

    external_actions = payload.get("external_actions")
    external_requested = external_actions not in (None, "none", [], {"allowed": "none"})
    if external_requested and payload.get("external_action_authorized") is not True:
        errors.append("blocked_authorization_required")
    # 本项目已确认 Public；写入契约必须显式承认可见性和脱敏结论，
    # 缺省不作为放宽安全边界的理由。
    if write_requested and (
        payload.get("repository_visibility") != "Public"
        or payload.get("contains_sensitive_business_data") is not False
        or payload.get("contains_personal_data") is not False
    ):
        errors.append("blocked_repo_visibility_for_sensitive_data")
    if has_sensitive_flag(payload):
        errors.append("blocked_repo_visibility_for_sensitive_data")
    return sorted(set(errors)), normalized_planned


def validate_task_request(payload: dict[str, Any]) -> list[str]:
    """校验 H01-H04 所需的最小任务交接信息。"""

    return task_request_details(payload)[0]


def build_route_decision(payload: dict[str, Any]) -> dict[str, Any]:
    """生成写入前路由判断（route_decision）；缺必读或权限时 fail-closed。"""

    errors, planned_files = task_request_details(payload)
    must_read = list_value(payload.get("must_read_files"))
    engineering_worth = payload.get("engineering_worth_question") or {}
    formal_count = safe_nonnegative_int(payload.get("formal_file_count", 0))
    if formal_count is None:
        errors.append("blocked_input_invalid")
        formal_count = 0
    worth_engineering = bool(engineering_worth.get("worth_engineering", formal_count >= 3))
    decision = {
        "task_type": list_value(payload.get("task_type")),
        "responsibility_layer": list_value(payload.get("responsibility_layer")),
        "must_read_files": must_read,
        "allowed_changes": list_value(payload.get("allowed_files")),
        "forbidden_changes": list_value(payload.get("forbidden_files")),
        "planned_files": planned_files,
        "external_actions": payload.get("external_actions"),
        "human_gates": list_value(payload.get("human_gates")),
        "engineering_worth_question": {
            "worth_engineering": worth_engineering,
            "reason": engineering_worth.get("reason", "由文件数量、状态、工具和验证复杂度决定。"),
            "engineering_depth": engineering_worth.get("engineering_depth", payload.get("engineering_depth", "L1_task_card")),
            "chosen_gate": engineering_worth.get("chosen_gate", "route_decision"),
            "not_chosen_gate": engineering_worth.get("not_chosen_gate", "unscoped_write"),
        },
        "execution_permission": "blocked" if errors else "authorized_within_allowed_files",
    }
    return make_report("route_decision_builder", errors, route_decision=decision)


def build_engineering_depth(payload: dict[str, Any]) -> dict[str, Any]:
    """根据价值、风险和重复度选择 L0-L3，防止简单任务被强制 L3。"""

    errors: list[str] = []
    requested = payload.get("engineering_depth") or payload.get("requested_depth")
    signals = payload.get("engineering_signals") or {}
    formal_files = safe_nonnegative_int(payload.get("formal_file_count", 0))
    if formal_files is None:
        errors.append("blocked_input_invalid")
        formal_files = 0
    if requested not in VALID_DEPTHS:
        errors.append("blocked_engineering_depth_invalid")
        requested = "L1_task_card"

    l3_signals = ("has_state", "multi_node", "requires_tools", "requires_evaluation", "has_failure_route", "long_running")
    if requested == "L3_system_line":
        missing = [signal for signal in l3_signals if not signals.get(signal)]
        required_context = ("goal", "current_state", "source_summary", "failure_route", "record_location")
        if missing or any(not payload.get(field) for field in required_context):
            errors.append("blocked_engineering_depth_invalid")
    if requested == "L2_node_contract":
        node_contract = payload.get("node_contract")
        if not isinstance(node_contract, dict) or any(not node_contract.get(field) for field in ("inputs", "outputs", "validation", "failure_route")):
            errors.append("blocked_engineering_depth_invalid")
    if requested == "L0_light_chat" and formal_files:
        errors.append("blocked_engineering_depth_invalid")

    report = {
        "selected_depth": requested,
        "中文含义": {
            "L0_light_chat": "L0 轻量聊天",
            "L1_task_card": "L1 任务卡",
            "L2_node_contract": "L2 节点契约",
            "L3_system_line": "L3 系统工程线",
        }[requested],
        "reason": payload.get("reason") or payload.get("engineering_worth_question", {}).get("reason", "工程深度由任务价值、风险、重复度和可验证性共同决定。"),
        "engineering_line_layers": ENGINEERING_LINE_LAYERS if requested == "L3_system_line" else [],
        "five_questions": {
            "要什么": payload.get("goal", ""),
            "到哪了": payload.get("current_state", ""),
            "吃什么资料": payload.get("source_summary", ""),
            "错了去哪": payload.get("failure_route", "failure_route_resolver"),
            "留没留记录": payload.get("record_location", "project_system/audit/"),
        },
    }
    return make_report("engineering_depth_router", sorted(set(errors)), engineering_depth=report)


def build_large_task_gate(payload: dict[str, Any]) -> dict[str, Any]:
    """判断是否进入大任务闸门，但不把大任务自动变成多代理写入。"""

    errors: list[str] = []
    formal_files = safe_nonnegative_int(payload.get("formal_file_count", 0))
    if formal_files is None:
        errors.append("blocked_input_invalid")
        formal_files = 0
    categories = set(list_value(payload.get("affected_categories")))
    reasons = []
    if formal_files >= 3:
        reasons.append("涉及 3 个以上正式文件")
    if len(categories.intersection({"rules", "scripts", "state", "logs"})) >= 3:
        reasons.append("同时涉及规则、脚本、状态或日志中的 3 类以上")
    if payload.get("large_readonly_audit"):
        reasons.append("需要大量只读审计后统一写入")
    if payload.get("multi_stage_or_role"):
        reasons.append("涉及多阶段、多角色或多状态")
    if payload.get("user_requests_complete_or_parallel"):
        reasons.append("用户要求完整执行或并发")
    if payload.get("single_executor_may_miss_items"):
        reasons.append("单执行器容易漏项")
    triggered = bool(reasons)
    lane = payload.get("lane_recommendation") or ("explore_plus_integrate" if triggered else "serial_only")
    if triggered and lane not in VALID_LANE_RECOMMENDATIONS:
        errors.append("blocked_large_task_lane_missing")
    return make_report(
        "large_task_gate",
        errors,
        large_task_gate={"triggered": triggered, "reasons": reasons, "lane_recommendation": lane},
    )


def build_lane_decision(payload: dict[str, Any]) -> dict[str, Any]:
    """检查并发车道；只读探索可以并发，写入必须由单一 integrator 拥有。"""

    errors: list[str] = []
    lanes = list_value(payload.get("lanes"))
    recommendation = payload.get("lane_recommendation", "serial_only")
    if recommendation not in VALID_LANE_RECOMMENDATIONS or not lanes:
        errors.append("blocked_large_task_lane_missing")
    for lane in lanes:
        if not isinstance(lane, dict) or not lane.get("name") or lane.get("mode") not in VALID_LANE_MODES or not lane.get("owner"):
            errors.append("blocked_large_task_lane_missing")
    write_lanes = [lane for lane in lanes if isinstance(lane, dict) and lane.get("mode") == "write"]
    owners = {lane.get("owner") for lane in write_lanes if lane.get("owner")}
    if len(write_lanes) > 1 or len(owners) > 1:
        errors.append("blocked_multi_lane_write_conflict")
    write_owner = payload.get("write_owner")
    if write_lanes and (not write_owner or write_owner not in owners or len(write_lanes) != 1):
        errors.append("blocked_multi_lane_write_conflict")
    if write_lanes and write_owner != payload.get("integration_owner"):
        errors.append("blocked_multi_lane_write_conflict")
    if payload.get("write_required") and not write_lanes:
        errors.append("blocked_large_task_lane_missing")
    return make_report(
        "lane_parallel_router",
        sorted(set(errors)),
        lane_decision={
            "lane_recommendation": recommendation,
            "lanes": lanes,
            "write_owner": write_owner,
            "integration_owner": payload.get("integration_owner"),
            "read_parallel_allowed": all(lane.get("mode") != "write" for lane in lanes[:-1] if isinstance(lane, dict)),
        },
    )


def build_workspace_governance(payload: dict[str, Any], planned_files: list[str] | None = None) -> dict[str, Any]:
    """检查 H19 单工作区：不接受 worktree、外部正式路径或多根工作区。"""

    errors: list[str] = []
    if payload.get("workspace_mode") != "single_formal_workspace":
        errors.append("blocked_external_workspace_required")
    if payload.get("external_workspace_required") is not False or payload.get("worktree_requested") is not False:
        errors.append("blocked_external_workspace_required")
    normalized_outputs: list[str] = []
    for path in planned_files or []:
        normalized = normalize_repository_path(path)
        if normalized is None:
            errors.append("blocked_external_workspace_required")
            continue
        normalized_outputs.append(normalized)

    worktree_count = 0
    project_root_matches = False
    try:
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=project_root(),
            capture_output=True,
            text=True,
            check=False,
        )
        worktree_roots = [line.removeprefix("worktree ") for line in result.stdout.splitlines() if line.startswith("worktree ")]
        worktree_count = len(worktree_roots)
        project_root_matches = worktree_count == 1 and Path(worktree_roots[0]).resolve() == project_root().resolve()
        if result.returncode != 0 or not project_root_matches:
            errors.append("blocked_external_workspace_required")
    except OSError:
        errors.append("blocked_external_workspace_required")
    return make_report(
        "workspace_governance_check",
        sorted(set(errors)),
        workspace_check={
            "workspace_mode": payload.get("workspace_mode"),
            "single_formal_workspace": not errors,
            "worktree_count": worktree_count,
            "project_root_matches": project_root_matches,
            "formal_output_paths": normalized_outputs,
        },
    )


def build_process_boot(payload: dict[str, Any]) -> dict[str, Any]:
    """建立流程启动报告，确保 prompt 只是本轮增量而不是完整流程来源。"""

    errors: list[str] = []
    if payload.get("route_decision_status") not in {"pass", "authorized_within_allowed_files"}:
        errors.append("blocked_task_contract_incomplete")
    if payload.get("source_readback_status") not in {"read_ok", "not_applicable"}:
        errors.append("blocked_source_missing")
    sources = list_value(payload.get("must_read_sources"))
    if not sources or any(not isinstance(source, (str, dict)) for source in sources):
        errors.append("blocked_source_missing")
    if any(not payload.get(field) for field in ("task_goal", "current_state", "supply_summary", "failure_route", "record_location")):
        errors.append("blocked_task_contract_incomplete")
    if payload.get("source_conflicts"):
        errors.append("blocked_fact_conflict")
    report = {
        "task_goal": payload.get("task_goal", "未提供"),
        "current_state": payload.get("current_state", "未提供"),
        "must_read_sources": sources,
        "five_questions": {
            "要什么": payload.get("task_goal", ""),
            "到哪了": payload.get("current_state", ""),
            "吃什么资料": payload.get("supply_summary", ""),
            "错了去哪": payload.get("failure_route", "failure_route_resolver"),
            "留没留记录": payload.get("record_location", "project_system/audit/"),
        },
        "prompt_role": "prompt_delta_only",
    }
    return make_report("process_boot_builder", errors, process_boot_report=report)


def build_mechanism_triggers(payload: dict[str, Any]) -> dict[str, Any]:
    """将任务类型映射到相关机制和习惯；它是选择器，不会强制所有机制运行。"""

    mapping = {
        "project_file_change": ["M02", "M07", "M10", "M11", "M14", "M17", "M27", "H01", "H04", "H09", "H17"],
        "mechanism_or_route_fix": ["M04", "M10", "M19", "M21", "H01", "H05", "H06", "H10", "H11"],
        "runtime_kernel_implementation": ["M07", "M08", "M17", "M19", "M20", "H05", "H06", "H07", "H09", "H14"],
        "gpt_project_sync": ["M02", "M11", "M12", "M15", "M27", "M28", "H15", "H17", "H18"],
        "research": ["M03", "M16", "M22", "H12", "H13"],
        "compliance_review": ["M03", "M16", "M18", "H12", "H14"],
        "external_action_proposal": ["M04", "M18", "H14", "H18"],
        "audit": ["M10", "M12", "M16", "M27", "H03", "H18"],
        "product_fact_intake": ["M03", "M04", "M16", "H03", "H12"],
        "data_processing": ["M07", "M17", "H09", "H14"],
        "copywriting_or_drafting": ["M04", "M07", "M18", "H01", "H18"],
        "channel_validation": ["M04", "M18", "M22", "M23", "H12", "H14"],
        "experiment_design": ["M04", "M22", "M23", "H12", "H18"],
        "code_debug": ["M07", "M08", "M17", "M19", "H06", "H16"],
        "local_file_governance": ["M02", "M10", "M17", "H04", "H19"],
    }
    task_types = list_value(payload.get("task_type"))
    triggered = sorted({item for task_type in task_types for item in mapping.get(task_type, [])})
    errors = ["blocked_unknown_task_type"] if any(item not in VALID_TASK_TYPES for item in task_types) or not triggered else []
    return make_report("mechanism_trigger_router", errors, triggered_mechanisms_and_habits=triggered)


def build_supply_pack(payload: dict[str, Any]) -> dict[str, Any]:
    """创建执行前供料包；来源没有原文件回读时不允许继续写入。"""

    errors: list[str] = []
    sources = list_value(payload.get("must_read_sources"))
    if not payload.get("task_goal") or not payload.get("current_state") or not sources:
        errors.append("blocked_supply_repair")
    normalized_sources = []
    for source in sources:
        if not isinstance(source, dict):
            errors.append("blocked_supply_repair")
            continue
        required = ("source_path", "readback_status", "exact_relevant_snippets")
        if any(not source.get(field) for field in required) or source.get("readback_status") != "read_ok" or not isinstance(source.get("exact_relevant_snippets"), list):
            errors.append("blocked_supply_repair")
        normalized_sources.append(source)
    conflicts = list_value(payload.get("source_conflicts"))
    if conflicts:
        errors.append("blocked_fact_conflict")
    second_opinion = bool(
        payload.get("second_opinion_trigger")
        or conflicts
        or payload.get("low_confidence")
        or payload.get("high_risk")
        or payload.get("user_requested_second_opinion")
    )
    pack = {
        "task_goal": payload.get("task_goal"),
        "current_state": payload.get("current_state"),
        "must_read_sources": normalized_sources,
        "retrieval_manifest": [{"source_path": source.get("source_path"), "readback_status": source.get("readback_status")} for source in normalized_sources],
        "source_readback_status": "read_ok" if not errors else "blocked",
        "constraints": list_value(payload.get("constraints")),
        "conflicts": conflicts,
        "missing_information": list_value(payload.get("missing_information")),
        "decision_authority": payload.get("decision_authority", "execution_authority"),
        "allowed_actions": list_value(payload.get("allowed_actions")),
        "forbidden_actions": list_value(payload.get("forbidden_actions")),
        "next_input_for_codex": payload.get("next_input_for_codex", "原文件回读通过后再执行。"),
        "external_research_needed": bool(payload.get("external_research_needed")),
        "second_opinion_trigger": second_opinion,
    }
    return make_report("source_supply_pack_builder", sorted(set(errors)), pre_task_supply_pack=pack)


def build_mid_task_supply(payload: dict[str, Any]) -> dict[str, Any]:
    """在缺上下文、验证失败或冲突时补料；无法补齐时 fail-closed。"""

    errors: list[str] = []
    base_pack = payload.get("base_supply_pack") or {}
    needs_supply = bool(payload.get("validation_failed") or payload.get("missing_information") or payload.get("source_conflicts"))
    if needs_supply and not base_pack.get("task_goal"):
        errors.append("blocked_supply_repair")
    if payload.get("validation_failed") and (not payload.get("validation_failures") or not payload.get("exact_relevant_snippets")):
        errors.append("blocked_supply_repair")
    if payload.get("source_conflicts"):
        errors.append("blocked_fact_conflict")
    if payload.get("validation_failed"):
        errors.append("blocked_supply_repair")
    continue_allowed = not errors
    pack = {
        "base_task_goal": base_pack.get("task_goal"),
        "trigger": payload.get("trigger", "mid_task_context_gap"),
        "missing_information": list_value(payload.get("missing_information")),
        "validation_failures": list_value(payload.get("validation_failures")),
        "source_conflicts": list_value(payload.get("source_conflicts")),
        "exact_relevant_snippets": list_value(payload.get("exact_relevant_snippets")),
        "continue_allowed": continue_allowed,
        "next_safe_step": payload.get("next_safe_step", "补齐来源或进入对应失败路由。"),
    }
    return make_report("mid_task_supply_builder", sorted(set(errors)), mid_task_supply_pack=pack)


def validate_per_file_plan(payload: dict[str, Any]) -> dict[str, Any]:
    """验证每个拟改文件都具备用途、路由、边界与验收说明。"""

    errors: list[str] = []
    shared = payload.get("shared_policy") or {}
    groups = payload.get("plan_groups") or payload.get("plans") or []
    planned_paths: list[str] = []
    if not isinstance(groups, list) or not groups:
        errors.append("blocked_per_file_plan_incomplete")
    for group in groups:
        if not isinstance(group, dict):
            errors.append("blocked_per_file_plan_incomplete")
            continue
        paths = group.get("paths") or ([group["path"]] if group.get("path") else [])
        if not paths or any(normalize_repository_path(path) is None for path in paths):
            errors.append("blocked_per_file_plan_incomplete")
        planned_paths.extend(normalize_repository_path(path) for path in paths if normalize_repository_path(path) is not None)
        effective = {**shared, **group}
        if any(not effective.get(field) for field in PER_FILE_PLAN_FIELDS):
            errors.append("blocked_per_file_plan_incomplete")
    if len(planned_paths) != len(set(planned_paths)):
        errors.append("blocked_per_file_plan_incomplete")
    return make_report(
        "per_file_plan_validator",
        sorted(set(errors)),
        planned_file_count=len(planned_paths),
        planned_files=planned_paths,
    )


def validate_state_transition(payload: dict[str, Any]) -> dict[str, Any]:
    """校验动态状态更新不会跳过证据或需要人工决定的边界。"""

    errors: list[str] = []
    current = payload.get("current_state")
    target = payload.get("target_state")
    evidence = list_value(payload.get("required_evidence"))
    if current not in VALID_STATES or target not in VALID_STATES or not evidence or target not in ALLOWED_STATE_TRANSITIONS.get(current, set()):
        errors.append("blocked_state_transition_invalid")
    if not isinstance(payload.get("human_gate_required"), bool) or not isinstance(payload.get("human_gate_satisfied"), bool):
        errors.append("blocked_state_transition_invalid")
    for item in evidence:
        if not isinstance(item, dict) or not item.get("evidence_type") or not item.get("source_path") or item.get("readback_status") != "read_ok":
            errors.append("blocked_state_transition_invalid")
    business_targets = {"market_screening", "b2b_channel_validation", "b2c_channel_validation", "lead_generation_test", "offer_validation", "pilot_execution", "scale_or_stop"}
    if (payload.get("human_gate_required") or target in business_targets) and payload.get("human_gate_satisfied") is not True:
        errors.append("blocked_authorization_required")
    if payload.get("business_execution_started") and target == "cross_project_collaboration_system_v2_active":
        errors.append("blocked_state_transition_invalid")
    return make_report(
        "state_transition_validator",
        sorted(set(errors)),
        state_transition={
            "current_state": current,
            "target_state": target,
            "required_evidence": evidence,
            "human_gate_required": bool(payload.get("human_gate_required")),
            "human_gate_satisfied": bool(payload.get("human_gate_satisfied")),
        },
    )


def validate_completion_relay(payload: dict[str, Any]) -> dict[str, Any]:
    """验证 Completion Relay：必交付、剩余工作和 Git 真相必须同时闭合。"""

    errors: list[str] = []
    inventory = list_value(payload.get("required_output_inventory"))
    if not inventory or not isinstance(payload.get("remaining_work_check"), dict) or not list_value(payload.get("child_task_graph")):
        errors.append("blocked_completion_claim_repair")
    incomplete = []
    for item in inventory:
        if not isinstance(item, dict):
            incomplete.append("invalid_inventory_item")
        elif item.get("required", True) and item.get("status") not in {"completed", "not_applicable"}:
            incomplete.append(item.get("name", "unnamed_output"))
    remaining = payload.get("remaining_work_check") or {}
    claimed = payload.get("completion_status")
    final_claim = claimed not in {None, "blocked", "partial_completed", "continue"}
    if incomplete or remaining.get("remaining_required") is not False or final_claim and payload.get("git_closeout", {}).get("remote_match") is not True:
        errors.append("blocked_completion_claim_repair")
    return make_report(
        "completion_relay_validator",
        sorted(set(errors)),
        completion_relay={
            "required_output_inventory": inventory,
            "child_task_graph": list_value(payload.get("child_task_graph")),
            "remaining_work_check": remaining,
            "incomplete_outputs": incomplete,
            "completion_status": claimed,
            "git_closeout": payload.get("git_closeout", {}),
        },
    )


def resolve_failure_route(payload: dict[str, Any]) -> dict[str, Any]:
    """将失败映射到明确修复层，而不是泛化为 retry。"""

    mapping = {
        "missing_fact": "product_fact_collection",
        "fact_conflict": "fact_conflict_resolution",
        "missing_compliance_evidence": "compliance_validation",
        "capability_unverified": "capability_probe",
        "write_scope_violation": "scope_repair",
        "supply_insufficient": "supply_repair",
        "state_not_allowed": "state_transition_repair",
        "completion_overclaim": "completion_claim_repair",
        "git_inconsistent": "git_closeout_repair",
        "human_decision_needed": "human_decision_required",
    }
    condition = payload.get("failure_condition")
    route = mapping.get(condition)
    errors = [] if route else ["blocked_input_invalid"]
    return make_report(
        "failure_route_resolver",
        errors,
        failure_route={
            "failure_condition": condition,
            "repair_route": route,
            "owner": "single_integrator" if route != "human_decision_required" else "user_or_authorized_reviewer",
            "next_safe_step": "执行对应修复并重新验证，不得只重试。" if route else "提供正式失败条件。",
        },
    )


def is_forbidden_git_path(value: Any) -> bool:
    """拒绝任何层级的环境文件、私有目录和受保护迁移证据路径。"""

    normalized = normalize_repository_path(value)
    if normalized is None:
        return True
    path = Path(normalized)
    if path.name == ".DS_Store" or path.name == ".env" or path.name.startswith(".env."):
        return True
    if any(part in GIT_FORBIDDEN_DIRECTORY_SEGMENTS for part in path.parts):
        return True
    protected = "project_bootstrap/collaboration_mechanism_migration"
    return normalized == protected or normalized.startswith(protected + "/")


def run_git_readonly(arguments: list[str]) -> tuple[int, str]:
    """以只读方式调用 Git；调用方只保存状态摘要，不输出敏感 diff 内容。"""

    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=project_root(),
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout
    except OSError:
        return 1, ""


def scan_git_diff_text(text: str) -> tuple[list[str], list[str]]:
    """扫描已提交 diff 的秘密与个人信息迹象；报告只给类别和计数。"""

    secret_findings = [label for label, pattern in GIT_SECRET_PATTERNS.items() if re.search(pattern, text)]
    sensitive_findings = [label for label, pattern in GIT_SENSITIVE_PATTERNS.items() if re.search(pattern, text)]
    return secret_findings, sensitive_findings


def live_git_evidence_errors(payload: dict[str, Any], staged_paths: list[str]) -> tuple[list[str], dict[str, Any]]:
    """回读真实 commit、refs、远端关键文件和 diff；不执行 Git 写入。"""

    errors: list[str] = []
    evidence: dict[str, Any] = {
        "mode": "live_commit_readback",
        "commit_paths_match": False,
        "diff_check_passed": False,
        "secret_finding_count": 0,
        "sensitive_finding_count": 0,
        "refs_match_payload": False,
        "remote_files_readable": False,
        "working_tree_clean": False,
    }
    commit_sha = payload.get("commit_sha")
    if not isinstance(commit_sha, str) or not SHA_PATTERN.fullmatch(commit_sha):
        return ["blocked_remote_readback_failed"], evidence

    paths_code, raw_paths = run_git_readonly(["diff-tree", "--no-commit-id", "--name-only", "-r", "-z", commit_sha])
    actual_paths = [normalize_repository_path(item) for item in raw_paths.split("\0") if item]
    actual_paths = [path for path in actual_paths if path is not None]
    if paths_code != 0 or set(actual_paths) != set(staged_paths):
        errors.append("blocked_git_closeout_repair")
    else:
        evidence["commit_paths_match"] = True

    check_code, _ = run_git_readonly(["show", "--check", "--format=", commit_sha])
    if check_code != 0:
        errors.append("blocked_git_closeout_repair")
    else:
        evidence["diff_check_passed"] = True

    diff_code, diff_text = run_git_readonly(["show", "--format=", "--no-ext-diff", commit_sha])
    if diff_code != 0:
        errors.append("blocked_git_closeout_repair")
    else:
        secret_findings, sensitive_findings = scan_git_diff_text(diff_text)
        evidence["secret_finding_count"] = len(secret_findings)
        evidence["sensitive_finding_count"] = len(sensitive_findings)
        if secret_findings:
            errors.append("blocked_git_closeout_repair")
        if sensitive_findings:
            errors.append("blocked_repo_visibility_for_sensitive_data")

    head_code, local_head = run_git_readonly(["rev-parse", "HEAD"])
    origin_code, origin_main = run_git_readonly(["rev-parse", "origin/main"])
    remote_code, remote_lines = run_git_readonly(["ls-remote", "origin", "refs/heads/main"])
    remote_parts = remote_lines.strip().split()
    ls_remote_main = remote_parts[0] if remote_parts else ""
    branch_code, branch = run_git_readonly(["branch", "--show-current"])
    payload_refs = [payload.get("commit_sha"), payload.get("local_head"), payload.get("origin_main"), payload.get("ls_remote_main")]
    actual_refs = [local_head.strip(), origin_main.strip(), ls_remote_main]
    if (
        head_code != 0
        or origin_code != 0
        or remote_code != 0
        or branch_code != 0
        or branch.strip() != "main"
        or any(value != actual_refs[0] for value in actual_refs)
        or payload_refs != [actual_refs[0], actual_refs[0], actual_refs[0], actual_refs[0]]
    ):
        errors.append("blocked_remote_readback_failed")
    else:
        evidence["refs_match_payload"] = True

    remote_readback = payload.get("remote_readback") or []
    declared_remote_paths = {
        normalize_repository_path(item.get("path"))
        for item in remote_readback
        if isinstance(item, dict) and item.get("read_status") == "read_ok"
    }
    required_present = REQUIRED_REMOTE_READBACK_PATHS.issubset(declared_remote_paths)
    files_readable = required_present
    if required_present:
        for path in REQUIRED_REMOTE_READBACK_PATHS:
            file_code, _ = run_git_readonly(["show", f"origin/main:{path}"])
            if file_code != 0:
                files_readable = False
                break
    if not files_readable:
        errors.append("blocked_remote_readback_failed")
    else:
        evidence["remote_files_readable"] = True

    status_code, status_text = run_git_readonly(["status", "--porcelain"])
    if status_code != 0 or status_text.strip():
        errors.append("blocked_git_closeout_repair")
    else:
        evidence["working_tree_clean"] = True
    return errors, evidence


def validate_git_closeout(payload: dict[str, Any], *, fixture_mode: bool = False) -> dict[str, Any]:
    """验证 Git 收尾；正式调用回读真实 commit/远端，Fixture 才可使用脱敏模拟证据。"""

    errors: list[str] = []
    raw_staged_paths = list_value(payload.get("staged_paths"))
    staged_paths = [normalize_repository_path(path) for path in raw_staged_paths if isinstance(path, str)]
    staged_paths = [path for path in staged_paths if path is not None]
    authorized_paths = [normalize_repository_path(path) for path in list_value(payload.get("authorized_staged_paths")) if isinstance(path, str)]
    authorized_paths = [path for path in authorized_paths if path is not None]
    if (
        not raw_staged_paths
        or len(staged_paths) != len(raw_staged_paths)
        or not authorized_paths
        or not set(staged_paths).issubset(set(authorized_paths))
        or payload.get("broad_stage_used") is not False
        or any(is_forbidden_git_path(path) for path in staged_paths)
    ):
        errors.append("blocked_git_closeout_repair")
    bool_fields = ("diff_check_passed", "secret_scan_passed", "sensitive_scan_passed", "push_succeeded")
    if any(payload.get(field) is not True for field in bool_fields):
        errors.append("blocked_git_closeout_repair")
    sha_values = [payload.get("commit_sha"), payload.get("local_head"), payload.get("origin_main"), payload.get("ls_remote_main")]
    if not all(isinstance(sha, str) and SHA_PATTERN.fullmatch(sha) for sha in sha_values) or len(set(sha_values)) != 1:
        errors.append("blocked_remote_readback_failed")
    remote_readback = payload.get("remote_readback")
    declared_remote_paths = {
        normalize_repository_path(item.get("path"))
        for item in remote_readback or []
        if isinstance(item, dict) and item.get("read_status") == "read_ok"
    }
    if (
        payload.get("branch") != "main"
        or not isinstance(remote_readback, list)
        or not REQUIRED_REMOTE_READBACK_PATHS.issubset(declared_remote_paths)
    ):
        errors.append("blocked_remote_readback_failed")
    if (
        payload.get("repository_visibility") != "Public"
        or payload.get("contains_sensitive_business_data") is not False
        or payload.get("contains_personal_data") is not False
        or has_sensitive_flag(payload)
    ):
        errors.append("blocked_repo_visibility_for_sensitive_data")

    live_evidence: dict[str, Any] = {"mode": "fixture" if fixture_mode else "live_commit_readback"}
    if not fixture_mode:
        plan, plan_errors = load_per_file_plan_from_task({"per_file_plan_path": payload.get("per_file_plan_path")})
        if plan_errors or plan is None:
            errors.append("blocked_git_closeout_repair")
        else:
            plan_report = validate_per_file_plan(plan)
            if plan_report.get("status") != "pass" or not set(staged_paths).issubset(set(plan_report.get("planned_files", []))):
                errors.append("blocked_git_closeout_repair")
        live_errors, live_evidence = live_git_evidence_errors(payload, staged_paths)
        errors.extend(live_errors)
    return make_report(
        "git_closeout_validator",
        sorted(set(errors)),
        git_closeout={
            "staged_paths": staged_paths,
            "authorized_staged_paths": authorized_paths,
            "diff_check_passed": bool(payload.get("diff_check_passed")),
            "secret_scan_passed": bool(payload.get("secret_scan_passed")),
            "sensitive_scan_passed": bool(payload.get("sensitive_scan_passed")),
            "commit_sha": payload.get("commit_sha"),
            "push_succeeded": bool(payload.get("push_succeeded")),
            "local_head": payload.get("local_head"),
            "origin_main": payload.get("origin_main"),
            "ls_remote_main": payload.get("ls_remote_main"),
            "branch": payload.get("branch"),
            "remote_readback": remote_readback,
            "repository_visibility": payload.get("repository_visibility"),
            "contains_sensitive_business_data": payload.get("contains_sensitive_business_data"),
            "contains_personal_data": payload.get("contains_personal_data"),
            "live_evidence": live_evidence,
            "remote_match": not errors,
        },
    )


INPUT_SCHEMAS = {
    "route_decision_builder": "task_request.schema.json",
    "task_request_validator": "task_request.schema.json",
    "per_file_plan_validator": "per_file_plan.schema.json",
    "state_transition_validator": "state_transition.schema.json",
    "completion_relay_validator": "completion_relay.schema.json",
    "git_closeout_validator": "git_closeout.schema.json",
}

OUTPUT_SCHEMAS = {
    "route_decision_builder": ("route_decision", "route_decision.schema.json"),
    "task_request_validator": ("route_decision", "route_decision.schema.json"),
    "engineering_depth_router": ("engineering_depth", "engineering_depth.schema.json"),
    "process_boot_builder": ("process_boot_report", "process_boot_report.schema.json"),
    "source_supply_pack_builder": ("pre_task_supply_pack", "pre_task_supply_pack.schema.json"),
    "mid_task_supply_builder": ("mid_task_supply_pack", "mid_task_supply_pack.schema.json"),
    "state_transition_validator": ("state_transition", "state_transition.schema.json"),
    "completion_relay_validator": ("completion_relay", "completion_relay.schema.json"),
    "failure_route_resolver": ("failure_route", "failure_route.schema.json"),
    "git_closeout_validator": ("git_closeout", "git_closeout.schema.json"),
}


def schema_validation_errors(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """执行本项目 Schema 使用到的安全子集：type、required、enum、const、minItems、properties/items。"""

    errors: list[str] = []
    expected_type = schema.get("type")
    type_ok = {
        "object": isinstance(instance, dict),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
        "boolean": isinstance(instance, bool),
        "integer": isinstance(instance, int) and not isinstance(instance, bool),
    }
    if expected_type and not type_ok.get(expected_type, True):
        return [f"{path}: expected {expected_type}"]
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value not in enum")
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: value does not equal const")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path}: minItems not met")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(instance):
                errors.extend(schema_validation_errors(item, schema["items"], f"{path}[{index}]"))
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing {key}")
        for key, child_schema in schema.get("properties", {}).items():
            if key in instance and isinstance(child_schema, dict):
                errors.extend(schema_validation_errors(instance[key], child_schema, f"{path}.{key}"))
    return errors


def load_schema(filename: str) -> dict[str, Any]:
    """读取随仓库提交的 Schema；失败由调用方作为阻断处理。"""

    schema = load_json(project_root() / "project_system" / "schemas" / filename)
    if not isinstance(schema, dict):
        raise ValueError("schema root is not an object")
    return schema


def enforce_component_schema(component: str, report: dict[str, Any]) -> dict[str, Any]:
    """把通过的运行器输出绑定到对应 Schema，防止只解析不校验。"""

    mapping = OUTPUT_SCHEMAS.get(component)
    if report.get("status") != "pass" or mapping is None:
        return report
    key, filename = mapping
    try:
        errors = schema_validation_errors(report.get(key), load_schema(filename))
    except (OSError, json.JSONDecodeError, ValueError):
        errors = ["schema unavailable"]
    report["schema_validation"] = {"schema": filename, "errors": errors, "status": "pass" if not errors else "blocked"}
    if errors:
        report["status"] = "blocked"
        report.setdefault("error_codes", []).append("blocked_schema_validation_failed")
    return report


def sha256_file(path: Path) -> str:
    """为 GPT 包清单计算文件摘要。"""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_json_component(
    component: str,
    description: str,
    builder: Callable[[dict[str, Any]], dict[str, Any]],
    argv: list[str] | None = None,
) -> int:
    """为大多数 JSON 组件提供统一 CLI：默认 dry-run、--help、输出与阻断退出码。"""

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--input", type=Path, help="JSON 输入文件；未提供时只返回阻断 dry-run 报告。")
    parser.add_argument("--output", type=Path, help="可选 JSON 报告路径；只有加 --execute 才会写入。")
    parser.add_argument("--execute", action="store_true", help="允许把报告写到受控项目路径；默认不写入。")
    args = parser.parse_args(argv)
    if args.input is None:
        return output_report(make_report(component, ["blocked_input_missing"]), args.output, args.execute)
    try:
        payload = load_json(args.input)
    except (OSError, json.JSONDecodeError):
        return output_report(make_report(component, ["blocked_input_invalid"]), args.output, args.execute)
    if not isinstance(payload, dict):
        report = make_report(component, ["blocked_input_invalid"])
    else:
        input_schema = INPUT_SCHEMAS.get(component)
        if input_schema:
            try:
                input_errors = schema_validation_errors(payload, load_schema(input_schema))
            except (OSError, json.JSONDecodeError, ValueError):
                input_errors = ["schema unavailable"]
            if input_errors:
                report = make_report(component, ["blocked_schema_validation_failed"], schema_validation={"schema": input_schema, "errors": input_errors, "status": "blocked"})
            else:
                report = builder(payload)
        else:
            report = builder(payload)
    report = enforce_component_schema(component, report)
    return output_report(report, args.output, args.execute)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="v2 协作运行内核公共模块；供各 JSON 组件导入，不单独执行任务。")
    parser.parse_args()

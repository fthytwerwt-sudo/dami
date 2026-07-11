#!/usr/bin/env python3
"""生成完整 GPT Project v2 分发包，默认只预览、不写入。

该构建器只读取本仓库正式规则和 current 快照，不访问网络、密钥或外部业务系统。
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import json_text, project_root, sha256_file


PACKAGE_FILES = (
    "00_上传说明_UPLOAD_MANIFEST.md",
    "01_GPT项目完整指令_GPT_PROJECT_INSTRUCTIONS.md",
    "02_跨项目操作习惯_cross_project_operating_habits.md",
    "03_工程线与任务路由_engineering_line_and_task_routing.md",
    "04_事实源与人工闸门_source_of_truth_and_human_gates.md",
    "05_当前项目状态快照_current_project_state_snapshot.md",
    "06_Codex交接契约_codex_handoff_contract.md",
    "07_Codex回报复审契约_codex_report_review_contract.md",
)

VERSION_PATTERN = re.compile(r"v[0-9]+_[0-9]{8}(?:_[A-Za-z0-9._-]+)?$")


def read_required(root: Path, relative: str) -> str:
    """读取正式文本；缺文件由调用方转为 blocked，而不伪造包内容。"""

    return (root / relative).read_text(encoding="utf-8")


def git_head(root: Path) -> str:
    """只读获取生成快照所基于的提交 SHA。"""

    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False)
    source_commit = result.stdout.strip()
    if result.returncode != 0 or not re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", source_commit):
        raise RuntimeError("unable to resolve a valid source commit")
    return source_commit


def package_content(root: Path, version: str, source_commit: str) -> dict[str, str]:
    """从正式规则组装用户可上传的 v2 文件，不把静态包当作动态事实源。"""

    habits = read_required(root, "project_system/02_跨项目操作习惯注册表_cross_project_operating_habits.md")
    engineering = "\n\n".join(
        read_required(root, relative)
        for relative in (
            "project_system/rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md",
            "project_system/rules/11_路由判断与流程启动_route_decision_and_process_boot.md",
            "project_system/rules/12_完整工程线_engineering_line.md",
            "project_system/rules/13_大任务与执行车道_large_task_and_execution_lanes.md",
            "project_system/rules/15_单文件细节方案_per_file_detail_plan.md",
            "project_system/rules/16_完成接力与失败路由_completion_relay_and_failure_routes.md",
        )
    )
    source_and_gates = "\n\n".join(
        read_required(root, relative)
        for relative in (
            "project_system/rules/01_ROLES_AND_AUTHORITY.md",
            "project_system/rules/02_SOURCE_OF_TRUTH_AND_CONFLICT.md",
            "project_system/rules/05_EXECUTION_SAFETY_AND_HUMAN_GATES.md",
            "project_system/rules/14_供料与执行中补料_supply_and_mid_task_supply.md",
        )
    )
    current_snapshot = "\n\n".join(
        read_required(root, relative)
        for relative in (
            "project_system/current/CURRENT_PROJECT_STATE.md",
            "project_system/current/CURRENT_FORMAL_FACTS.md",
            "project_system/current/CURRENT_DECISIONS.md",
            "project_system/current/LATEST_TASK_STATUS.md",
        )
    )
    instructions = """# GPT Project 完整指令（GPT Project Instructions）v2

## 角色与总原则

你是大米低 GI 跨境项目的 ChatGPT 总控与复审层（project judgment and review layer）。先判断真实问题、来源、权限、状态和工程深度，再向 Codex 下发执行单。Codex 是受控写入与验证层；用户保留市场、渠道、模式、价格、MOQ、交期、代理、合同、样品、预算、外部动作和最终业务判断权限。客观事实必须由当前原始证据决定。

默认中文解释在前、英文原词在后。先判断真实问题而非只复述表面请求；每项判断区分事实、推论、计划和建议，并标注证据标签、来源、适用范围与 `confidence（置信度）`。状态标签使用 `已确认`、`部分成立`、`待验证`、`推测` 或 `通用建议`。用户说“不对、空、怪怪的”时，先触发内部 self-repair audit（自修审计），回查目标、来源、范围、路由、验证和状态，不要求用户排查工程原因。

## 事实源与静态包边界

当前仓库 `main` 的 `AGENTS.md`、`project_system/current/` 和直接相关正式规则高于本静态包、聊天记忆、检索摘要与外部 AI 意见。静态包只用于协作一致性；动态事实发生变化时，先回读仓库 current。不得把包生成写成 UI 上传，也不得把技术、Git 或文档完成写成市场、合规、商业或外部执行完成。

## 每轮路由

先输出 `route_decision（路由判断）`：任务类型、责任层、必读文件和读取状态、允许/禁止修改、来源与冲突、工程价值、外部动作、人工闸门和执行权限。目标有歧义、用户反馈矛盾或新要求可能冲突时，先做需求对齐（requirement alignment）：目标层、机制层、实现设计层、流程层、判断标准层和反馈层。未完成路由或需求对齐，不得向 Codex 下发复杂或写入任务。

再回答“值不值得工程化”，选择 L0-L3：L0 轻量解释、L1 任务卡、L2 节点契约、L3 系统工程线。简单问题不强行工程化；存在状态、多节点、工具、评估、失败路由和长期运行价值时才进入 L3。L3 覆盖 13 层工程线与五问法：要什么、到哪了、吃什么资料、错了去哪、留没留记录。

大任务先跑 `large_task_gate`，再选 `serial_only`、`read_parallel`、`explore_plus_integrate` 或 `true_multi_task_parallel`。只读可以并发；写入只能有一个 integrator。每个新改机制、脚本、Schema、Validator 或节点都要有 `per_file_plan`。

## 供料、研究与外部 AI

资料顺序为当前正式原文件 → 经授权私有来源 → 外部权威原始来源 → 搜索/AI 摘要导航 → 条件第二意见。外部研究（包括 Perplexity 或任何其他工具）只能提供导航或只读第二意见，必须回读原始来源；不绑定供应商，不读取密钥，不替代事实或用户决定。执行前建 pre-task supply pack，执行中有缺上下文、验证失败或冲突时建 mid-task supply pack；缺原文、readback 或冲突裁决时 block。

## Codex 执行单

每次交接必须包含：Goal｜目标、Context｜上下文、Source of truth｜事实源、Constraints｜边界、Route decision｜路由判断、Engineering depth｜工程深度、Implementation design｜实现设计、Impact check｜影响面、Supply pack｜供料包、Allowed files｜允许文件、Forbidden files｜禁止文件、External actions｜外部动作、Human gates｜人工闸门、Per-file plans｜单文件方案、Execution steps｜执行步骤、Validation｜验证、Failure routes｜失败路由、Rollback｜回滚、Done when｜完成标准、Blocked if｜阻断条件、Completion Relay｜完成接力、Git closeout｜Git 收尾、Output｜回报格式。

## 人工闸门与完成真实性

不得自行决定市场、渠道、B2B/B2C、价格、健康/医疗承诺、客户联系、发布、广告、账号、支付、合同或样品。若需要，输出证据、选项、风险与最小人工决定，而不是执行。

完整任务需要 Completion Relay：required output inventory、child task graph、remaining work check、sync back check。Codex 回报必须区分 Tested/Not-tested、status promotions/status not promoted、blocked items、remaining work，最后写“下一个目标”。只有正式文件精确暂存、扫描、commit、push、三方 SHA 一致和远端关键文件回读后，才可以说 Git 同步完成。
"""
    handoff = """# Codex 交接契约（Codex handoff contract）

任何需要 Codex 执行的复杂或写入任务，必须按以下字段完整下发：

```text
Goal｜目标
Context｜上下文
Source of truth｜事实源
Constraints｜边界
Route decision｜路由判断
Engineering depth｜工程深度
Implementation design｜实现设计
Impact check｜影响面
Supply pack｜供料包
Allowed files｜允许文件
Forbidden files｜禁止文件
External actions｜外部动作
Human gates｜人工闸门
Per-file plans｜单文件方案
Execution steps｜执行步骤
Validation｜验证
Failure routes｜失败路由
Rollback｜回滚
Done when｜完成标准
Blocked if｜阻断条件
Completion Relay｜完成接力
Git closeout｜Git 收尾
Output｜回报格式
```

不得只给一句目标要求 Codex 猜实现。缺来源、权限、范围或完成标准时先补供料或阻断。Codex 只可修改 `Allowed files`，不得自动执行 `External actions` 或越过 `Human gates`。
"""
    review = """# Codex 回报复审契约（Codex report review contract）

ChatGPT 审核 Codex 回报时逐项检查：

1. 是否有 route decision、必读文件回读、工程深度与大任务/lane 判断。
2. 是否读取原文件而非只依赖摘要、静态包或聊天记忆。
3. 是否修改了未授权文件、触及敏感数据，或越过人工/外部动作权限。
4. 是否有 per-file plan、供料、验证、失败路由、完成接力和剩余工作检查。
5. 是否把技术、文档、Git、人工、合规、业务和 UI 上传状态混写或越级。
6. 是否完成精确暂存、扫描、commit、push、HEAD/origin/ls-remote 对读和远端关键文件回读。
7. 是否把本地未推送、fallback、partial 或 blocked 写成 completed。
8. 是否报告 Tested、Not-tested、status promotions、status not promoted、blocked items、remaining work 和“下一个目标”。

任一关键项缺失时，要求 Codex 继续修复或报告具体 `blocked_*`，不接受“看起来完成”的口头结论。
"""
    manifest = """# 上传说明（UPLOAD MANIFEST）

package_version: `{version}`
ui_uploaded: `false`

1. 将 `01_GPT项目完整指令_GPT_PROJECT_INSTRUCTIONS.md` 的内容粘贴到 ChatGPT Project Instructions。
2. 将 `02` 至 `07` 作为 Project files 上传；`00` 与 `package_manifest.json` 用于上传和版本核对。
3. 上传后仍以仓库 current 为动态事实源；本包生成不代表 UI 已上传或已生效。
4. 如仓库规则或 current 变化，使用 builder 重新生成包并由用户确认 UI 上传。
""".format(version=version)
    snapshot_header = f"""# 当前项目状态快照（current project state snapshot）

package_version: `{version}`
source_commit: `{source_commit}`
generated_on: `{date.today().isoformat()}`
snapshot_status: `repository_snapshot; dynamic truth remains project_system/current/`
ui_uploaded: `false`

以下是生成时的 current 正式文件快照。后续动态事实以仓库 `main` 的 current 文件为准。

"""
    return {
        "00_上传说明_UPLOAD_MANIFEST.md": manifest,
        "01_GPT项目完整指令_GPT_PROJECT_INSTRUCTIONS.md": instructions,
        "02_跨项目操作习惯_cross_project_operating_habits.md": habits,
        "03_工程线与任务路由_engineering_line_and_task_routing.md": engineering,
        "04_事实源与人工闸门_source_of_truth_and_human_gates.md": source_and_gates,
        "05_当前项目状态快照_current_project_state_snapshot.md": snapshot_header + current_snapshot,
        "06_Codex交接契约_codex_handoff_contract.md": handoff,
        "07_Codex回报复审契约_codex_report_review_contract.md": review,
    }


def package_scan(files: dict[str, str]) -> list[str]:
    """阻止明显密钥、本机绝对路径和旧领域污染进入 Public 分发包。"""

    findings: list[str] = []
    forbidden_patterns = {
        "absolute_path": r"(?:/(?:Users|private|Volumes|home)/|[A-Za-z]:\\)",
        "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        "bearer_token": r"Bearer\s+[A-Za-z0-9._-]{12,}",
        # 仅识别具备常见服务商密钥形态的前缀，避免把
        # ``task_request_validator`` 这类正常脚本名误判为密钥。
        "common_api_key": r"(?:sk-[A-Za-z0-9_-]{20,}|sk_(?:live|proj)_[A-Za-z0-9_-]{16,}|rk_(?:live|test)_[A-Za-z0-9_-]{16,}|pk_(?:live|test)_[A-Za-z0-9_-]{16,})",
    }
    forbidden_terms = ("DashVector", "Chroma", "DeepSeek", "视频工厂", "TTS", "剪辑")
    for name, text in files.items():
        for label, pattern in forbidden_patterns.items():
            if re.search(pattern, text):
                findings.append(f"{name}:{label}")
        for term in forbidden_terms:
            if term in text:
                findings.append(f"{name}:forbidden_term:{term}")
    return findings


def validate_version(version: str) -> bool:
    """只接受 v2 日期式版本，阻止绝对路径、父目录和 latest 别名。"""

    return bool(VERSION_PATTERN.fullmatch(version)) and ".." not in version and "/" not in version and "\\" not in version


def safe_package_directory(path: Path, parent: Path) -> Path:
    """确认目录位于 builder 拥有的父目录内，且没有软链接或目录替换风险。"""

    if path.is_symlink() or parent.is_symlink():
        raise RuntimeError("package directory or parent must not be a symlink")
    parent_resolved = parent.resolve()
    path_resolved = path.resolve(strict=False)
    if not path_resolved.is_relative_to(parent_resolved) or path_resolved == parent_resolved:
        raise RuntimeError("package directory escapes its approved parent")
    if path.exists() and not path.is_dir():
        raise RuntimeError("package destination must be a directory")
    return path_resolved


def clean_package_dir(path: Path, parent: Path) -> None:
    """仅删除 builder 自己认识的平面文件；遇到目录、软链接或陌生文件即拒绝。"""

    safe_path = safe_package_directory(path, parent)
    safe_path.mkdir(parents=True, exist_ok=True)
    expected = set(PACKAGE_FILES) | {"package_manifest.json"}
    for child in safe_path.iterdir():
        if child.is_symlink() or child.is_dir() or child.name not in expected:
            raise RuntimeError("package directory contains an unsafe or unexpected entry")
        child.unlink()


def write_package(directory: Path, parent: Path, files: dict[str, str], version: str, source_commit: str) -> dict:
    """先在批准父目录内临时构建，再写入受控目标目录，避免不完整包进入 latest。"""

    if parent.is_symlink():
        raise RuntimeError("package parent must not be a symlink")
    parent.mkdir(parents=True, exist_ok=True)
    safe_directory = safe_package_directory(directory, parent)
    stage = Path(tempfile.mkdtemp(prefix=".package-build-", dir=parent))
    try:
        for name, content in files.items():
            (stage / name).write_text(content.rstrip() + "\n", encoding="utf-8")
        records = [{"path": name, "sha256": sha256_file(stage / name)} for name in PACKAGE_FILES]
        package_manifest = {
            "package_version": version,
            "project_id": "low_gi_rice_crossborder",
            "source_commit": source_commit,
            "generated_on": date.today().isoformat(),
            "dynamic_source": "project_system/current/",
            "ui_uploaded": False,
            "files": records,
        }
        (stage / "package_manifest.json").write_text(json_text(package_manifest) + "\n", encoding="utf-8")
        # 清理前先确认目标永远仍在 approved parent 内，防止 TOCTOU 目录替换。
        clean_package_dir(safe_directory, parent)
        for child in stage.iterdir():
            shutil.move(str(child), str(safe_directory / child.name))
        return package_manifest
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="构建 GPT Project v2 分发包；默认只预览。")
    parser.add_argument("--version", default="v2_20260712", help="包版本名。")
    parser.add_argument("--execute", action="store_true", help="允许重建 latest 和同版本 archive；默认不写入。")
    args = parser.parse_args(argv)
    root = project_root()
    if not validate_version(args.version):
        report = {"component": "gpt_sync_package_builder", "status": "blocked", "error_codes": ["blocked_write_scope_violation"], "messages": ["版本只能是 v数字_YYYYMMDD 的安全名称，不能包含路径或父目录。"], "dry_run": not args.execute}
        sys.stdout.write(json_text(report) + "\n")
        return 2
    try:
        source_commit = git_head(root)
        files = package_content(root, args.version, source_commit)
    except (OSError, RuntimeError) as exc:
        report = {"component": "gpt_sync_package_builder", "status": "blocked", "error_codes": ["blocked_source_missing"], "messages": [str(exc)], "dry_run": not args.execute}
        sys.stdout.write(json_text(report) + "\n")
        return 2
    findings = package_scan(files)
    if findings:
        report = {"component": "gpt_sync_package_builder", "status": "blocked", "error_codes": ["blocked_sensitive_content_detected"], "findings": findings, "dry_run": not args.execute}
        sys.stdout.write(json_text(report) + "\n")
        return 2
    distribution_root = root / "gpt_project_sync"
    archive_root = distribution_root / "archive"
    latest = distribution_root / "latest"
    archive = archive_root / args.version
    report = {"component": "gpt_sync_package_builder", "status": "pass", "version": args.version, "planned_files": list(PACKAGE_FILES) + ["package_manifest.json"], "latest_path": "gpt_project_sync/latest/", "archive_path": f"gpt_project_sync/archive/{args.version}/", "ui_uploaded": False, "dry_run": not args.execute}
    if args.execute:
        try:
            latest_manifest = write_package(latest, distribution_root, files, args.version, source_commit)
            archive_manifest = write_package(archive, archive_root, files, args.version, source_commit)
            report["latest_manifest"] = latest_manifest
            report["archive_manifest"] = archive_manifest
            report["archive_matches_latest"] = all((latest / name).read_bytes() == (archive / name).read_bytes() for name in list(PACKAGE_FILES) + ["package_manifest.json"])
            if not report["archive_matches_latest"]:
                report["status"] = "blocked"
                report["error_codes"] = ["blocked_static_dynamic_pollution"]
        except (OSError, RuntimeError) as exc:
            report["status"] = "blocked"
            report["error_codes"] = ["blocked_write_scope_violation"]
            report["messages"] = [str(exc)]
    sys.stdout.write(json_text(report) + "\n")
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())

# Project Collaboration System v2

status: `cross_project_collaboration_system_v2_active`
project_id: `low_gi_rice_crossborder`
formal_system_version: `v2`

## 唯一正式入口

根 `AGENTS.md` 是唯一 Codex 正式入口。本文是导航索引（index），不重述动态业务事实，不形成第二套入口。动态 current 只在 `current/`；历史证据只在 `history/` 与受保护的 `project_bootstrap/`。

## 五层结构

1. **静态规则层（static rules）**：`AGENTS.md`、本索引、M01-M28 注册表、H01-H20 注册表、`rules/`。
2. **动态事实层（dynamic current truth）**：`current/` 中的状态、事实、决定、任务交接与仓库安全状态。
3. **执行契约层（task contracts）**：`templates/`、`schemas/`、任务输入与单文件方案。
4. **运行内核层（runtime kernel）**：`scripts/project_system/` 的 route、depth、lane、supply、validation、closeout 和 package builder。
5. **证据与历史层（evidence and history）**：`audit/`、`history/`、原始证据和只读迁移包。

## Canonical read chain｜规范读取链

`AGENTS.md` → `current/CURRENT_PROJECT_STATE.md` → `CURRENT_FORMAL_FACTS.md` → `CURRENT_DECISIONS.md` → `LATEST_TASK_STATUS.md` → 任务规则、Schema、原文件 → 受保护历史证据。

复杂或写入任务必须先完成 `route_decision`，再按 H05-H18 选择工程深度、供料、验证和 Git 收尾。`project_task_preflight.py` 与 `project_task_closeout.py` 是运行内核入口；默认 dry-run，不拥有业务或外部动作权限。

## 注册表与规则导航

- M01-M28：`01_MECHANISM_REGISTRY.md` 与 `.json`。
- H01-H20：`02_跨项目操作习惯注册表_cross_project_operating_habits.md` 与 `.json`。
- 角色与权限：`rules/01_ROLES_AND_AUTHORITY.md`。
- 来源与冲突：`rules/02_SOURCE_OF_TRUTH_AND_CONFLICT.md`。
- 对齐与设计：`rules/03_REQUIREMENT_ALIGNMENT_AND_IMPLEMENTATION_DESIGN.md`。
- 状态与转换：`rules/04_TASK_ROUTING_AND_STATE_MACHINE.md`。
- 安全与人工闸门：`rules/05_EXECUTION_SAFETY_AND_HUMAN_GATES.md`。
- 完成真实性：`rules/06_COMPLETION_TRUTH_AND_RELAY.md`。
- 研究与实验：`rules/07_RESEARCH_TO_ACTION_AND_EXPERIMENTS.md`。
- Git 与同步：`rules/08_GIT_AND_SYNC_TRUTH.md`。
- 工程深度、预算和协作：`rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md`。
- H01-H20 专项规则：`rules/10` 至 `rules/18`。

## v2 激活裁决

- `total_registered: 28`
- `ACTIVE_DIRECT: 16`
- `ACTIVE_ADAPTED: 9`（M19 已按用户本轮决定激活）
- `DEFERRED: 0`
- `REJECTED_NOT_MIGRATED: 3`（M24-M26）
- `operating_habits: H01-H20 active`

只触发本轮相关机制；注册表不是要求每轮跑完全部机制的命令。

## Toolchain exceptions｜工具链例外

```text
toolchain_exception: true
中文用途: Python 运行文件使用英文名以满足可执行模块入口；其中文用途由模块 docstring、规则和 H20 注册表说明。
toolchain_exception: true
中文用途: JSON Schema 使用固定英文文件名以满足机器引用；其中文用途由 title 和 description 说明。
```

它们不是用户可读业务目录命名的反例。

## GPT Project 分发边界

`gpt_project_sync/latest/` 是完整 GPT Project 分发快照，`archive/` 是版本归档；两者都不替代 `current/`。包生成不代表 UI 上传或业务状态推进。

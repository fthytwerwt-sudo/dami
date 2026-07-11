# v2 激活影响面检查（v2 activation impact check）

检查日期：`2026-07-12`

## 检查结论

本轮可以在受控范围内执行。目标仓库为 `Public`，但拟写入内容仅为协作机制、运行内核、测试样例、规则与 GPT Project 分发包；不包含客户、供应商、报价、成本、合同、认证原件、个人信息、密钥或其他商业敏感资料。

## 仓库与来源检查

- repository：`fthytwerwt-sudo/dami`
- branch：`main`
- target_starting_sha：`c254cb5b0fe28b6ec9d50ce550de83a369f6361d`
- origin_main_starting_sha：`c254cb5b0fe28b6ec9d50ce550de83a369f6361d`
- ls_remote_main_starting_sha：`c254cb5b0fe28b6ec9d50ce550de83a369f6361d`
- repository_visibility：`Public`（GitHub API 已回读）
- learning_repository：`fthytwerwt-sudo/-`
- learning_repo_sha：`ebc420f7bf42bd8c6c1d9ed435fd889177aa452c`
- learning_baseline_sha：`ebc420f7bf42bd8c6c1d9ed435fd889177aa452c`
- learning_main_changed_after_baseline：`false`
- worktree_at_start：`clean`
- parallel_formal_entry：`not_found`
- external_workspace_required：`false`
- current_package_version：`v1_20260711`
- protected_history_package：`project_bootstrap/collaboration_mechanism_migration/`，只读且未修改。

本检查有意不把本机绝对路径写入仓库；唯一正式工作区规则见 `rules/18_单工作区与路径治理_single_workspace_and_path_governance.md`。

## Source readback｜来源回读

| 来源 | 读取状态 | 本轮用途 |
| --- | --- | --- |
| `AGENTS.md` | `read_ok` | v1 唯一入口、启动链、权限和 Git 边界 |
| `project_system/current/CURRENT_PROJECT_STATE.md` | `read_ok` | 当前状态与不推进业务边界 |
| `project_system/current/CURRENT_FORMAL_FACTS.md` | `read_ok` | 正式事实与 GPT UI 未上传状态 |
| `project_system/current/CURRENT_DECISIONS.md` | `read_ok` | v1 决定与 M19 延后历史 |
| `project_system/current/LATEST_TASK_STATUS.md` | `read_ok` | v1 Git 交接事实 |
| `project_system/01_MECHANISM_REGISTRY.*` | `read_ok` | M01—M28 当前裁决和数量 |
| `project_system/rules/01`—`09` | `read_ok` | v1 可复用规则和 M19 冲突点 |
| `gpt_project_sync/latest/` | `read_ok` | v1 分发包与归档边界 |
| `project_bootstrap/collaboration_mechanism_migration/` | `read_ok` | 历史机制证据，仅作可追溯性 |
| `fthytwerwt-sudo/-` 的 `AGENTS.md`、项目状态路由、工程线、执行车道和 Codex 入口 | `read_ok` | 跨项目通用习惯证据 |

## route_decision｜路由判断

```yaml
task_type:
  - mechanism_or_route_fix
  - project_file_change
  - runtime_kernel_implementation
  - gpt_project_sync
responsibility_layer:
  - engineering_design_layer
  - execution_layer
  - validation_layer
  - sync_layer
must_read_files:
  - path: AGENTS.md
    read_status: read_ok
  - path: project_system/current/CURRENT_PROJECT_STATE.md
    read_status: read_ok
  - path: project_system/current/CURRENT_FORMAL_FACTS.md
    read_status: read_ok
  - path: project_system/current/CURRENT_DECISIONS.md
    read_status: read_ok
  - path: project_system/current/LATEST_TASK_STATUS.md
    read_status: read_ok
  - path: project_system/01_MECHANISM_REGISTRY.json
    read_status: read_ok
  - path: project_system/rules/01_ROLES_AND_AUTHORITY.md
    read_status: read_ok
  - path: project_system/rules/08_GIT_AND_SYNC_TRUTH.md
    read_status: read_ok
  - path: project_system/rules/09_ENGINEERING_DEPTH_AND_COLLABORATION_EFFECTIVENESS.md
    read_status: read_ok
  - path: project_bootstrap/collaboration_mechanism_migration/02_mechanism_inventory.json
    read_status: read_ok
allowed_changes:
  - AGENTS.md
  - project_system/ except protected project_bootstrap history
  - scripts/project_system/
  - gpt_project_sync/
forbidden_changes:
  - project_bootstrap/collaboration_mechanism_migration/
  - .DS_Store
  - .omx/
  - .env and .env.*
  - project_local/
  - foreign_trade_low_gi_plan/
  - secrets/
  - private/
  - customer, supplier, quotation, cost, contract, certification-original, or personal data
external_actions: none
human_gates:
  - no business, market, channel, pricing, compliance, or external action is authorized or promoted
execution_permission: authorized_for_repository_system_only
```

## 工程价值与大任务闸门

```yaml
engineering_worth_question:
  worth_engineering: true
  reason: 需要可重复运行的路由、验证、失败处理、状态与 Git 收尾，而非一次性说明文档。
  engineering_depth: L3_system_line
  chosen_gate: executable_runtime_kernel_with_schemas_and_fixtures
  not_chosen_gate: L0_light_chat_or_L1_task_card
engineering_depth: L3_system_line
engineering_line_13_layers_required: true
large_task_gate:
  triggered: true
  reasons:
    - 影响三个以上正式文件
    - 同时涉及规则、脚本、状态、日志和 GPT 分发包
    - 存在多阶段、多角色、多状态和统一验证
lane_recommendation: explore_plus_integrate
write_owner: single_integrator
integration_owner: single_integrator
```

## 影响面与安全检查

1. 根入口仍为 `AGENTS.md`；`project_system/00_PROJECT_SYSTEM_INDEX.md` 仅作为导航，不形成平行正式入口。
2. v1 机制计数为 `16 / 8 / 1 / 3`；v2 只调整 M19 为 `ACTIVE_ADAPTED`，目标为 `16 / 9 / 0 / 3`。
3. 新增运行内核、Schema 与 Fixture 路径当前不存在，因此不存在脚本覆盖冲突。
4. 当前 `latest/` 与 `archive/v1_20260711/` 同为轻量 v1 包；v1 归档保留不动，v2 仅替换 `latest/` 并新增独立 v2 archive。
5. 仓库 Public 安全开关保持 `business_sensitive_git_write_blocked_while_repo_public: true`。本轮采用规则文本、模拟 Fixture 与非敏感元数据，不读取私有源、不需要密钥。
6. 初始敏感信息和绝对路径检查未发现可提交风险；最终仍须重新扫描实际 diff 和暂存区。
7. 无需 clone、worktree 或外部正式目录；所有写入留在当前项目内。

## Completion Relay｜完成接力

```yaml
required_output_inventory:
  - M01-M28 v2 registry and M19 activation
  - H01-H20 operating-habits registry
  - AGENTS.md v2 sole-entry upgrade
  - formal rules and upgraded templates
  - runtime kernel scripts, schemas, fixtures, and simulator results
  - current-state and decision updates
  - complete GPT Project v2 package and archive
  - validation evidence
  - two scoped commits, push, SHA comparison, and remote readback
child_task_graph:
  - read_only_source_audit
  - v2_formal_system_and_file_plans
  - runtime_kernel_and_test_contracts
  - gpt_sync_and_current_state
  - validation_and_git_closeout
remaining_work_check: required_before_completion_claim
failure_routes:
  - source evidence missing -> blocked_source_habit_evidence_missing
  - scope or dirty-worktree conflict -> blocked_unrelated_dirty_changes_cannot_be_isolated
  - sensitive data -> blocked_sensitive_content_detected
  - validation failure -> corresponding failure_route repair
  - remote mismatch -> blocked_remote_readback_failed
```

## Bootstrap exception

v1 没有可执行 `route_decision` 入口。本文件是经用户明确授权、基于 v1 强制影响面检查创建的首次 v2 路由记录；后续写入将由 v2 运行内核的 `project_task_preflight.py` 复现并验证同一类输出。

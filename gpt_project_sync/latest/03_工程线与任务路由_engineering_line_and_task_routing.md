# 工程深度、执行预算与协作有效性

状态：`active`
适用机制：M19、M20、M21

## M19 v2 裁决

`M19 activation_status: ACTIVE_ADAPTED`。

工程深度路由已正式激活，但不是“每个任务都跑 L3”的命令。每轮先回答 `engineering_worth_question（值不值得工程化）`，以任务价值、风险、可逆性、重复度、节点数量、状态/工具/评估/失败路由复杂度及维护成本选择最轻充分方案。具体 L0-L3 和 13 层规则由 `rules/12_完整工程线_engineering_line.md` 承担。

## 执行预算

每个任务说明：

- 预计读取、写入、工具调用和外部成本。
- 最小验证集与停止条件。
- 何时从文档/模板升级到脚本、L2 或 L3。
- 新增机制的收益证据、维护者、回滚和退出方式。

已有规则、模板或轻量检查足以满足时，不新增脚本、依赖、状态机或多代理。L3 只有在真实的长期系统需求存在时才使用；L0/L1 不能被文件数量或“完整感”错误升级。

## 协作有效性复盘

在可比真实任务积累后复盘：是否减少重复解释、事实误升级、遗漏和未授权动作；是否增加维护成本；哪些字段无价值、哪些阻断过频、哪些机制应简化或自动化。复盘建议必须以实际证据和权限为准，不由文件数量或模拟 Fixture 自动得出业务效果。


# 路由判断与流程启动（route decision and process boot）

状态：`active`
适用习惯：H01-H04

## route_decision 硬闸门

任何仓库写入、commit 或 push 前必须有通过的 `route_decision`。它至少输出：

```text
task_type
responsibility_layer
must_read_files
read_status
allowed_changes
forbidden_changes
engineering_worth_question
external_actions
human_gates
execution_permission
```

`read_status` 只能为 `read_ok`、`missing`、`unreadable`、`not_applicable`。必读来源 `missing` 或 `unreadable`、允许范围不清、外部动作未授权、Public 仓库敏感资料、或责任层不明时，禁止写入并进入相应失败路由。

## process_boot_report

复杂任务在路由后建立 `process_boot_report`，回答：要什么、到哪了、吃什么资料、错了去哪、留没留记录。prompt 是 `prompt_delta_only`，不得替代仓库正式流程和原文件。

`project_task_preflight.py` 串联 route decision → engineering depth → large task gate → lane decision → must-read validation → scope validation → supply check → human gate check。默认 dry-run；报告通过不等于业务、合规或外部批准。


# 完整工程线（engineering line）

状态：`active`
适用机制：M19
适用习惯：H05-H08

## 深度路由

`L0_light_chat` 用于解释且不写正式文件；`L1_task_card` 用于小范围可逆任务；`L2_node_contract` 用于有稳定输入输出和验证的单节点；`L3_system_line` 仅在同时有状态、多节点、工具、评估、失败路由和长期运行价值时使用。用户说“直接做”不等于跳过判断。

## L3 的 13 层

```text
0 project_goal_layer（项目目标层）
1 current_task_awareness_layer（当前任务意识层）
2 process_node_layer（流程节点层）
3 cleaning_layer（清洗层）
4 structuring_layer（结构化层）
5 source_retrieval_layer（资料召回层）
6 tool_connection_layer（工具连接层）
7 execution_node_layer（执行节点层）
8 evaluation_layer（判断评估层）
9 failure_route_layer（失败路由层）
10 human_fallback_layer（人工兜底层）
11 state_record_layer（状态记录层）
12 retrospective_iteration_layer（复盘迭代层）
```

L3 必须有数据契约（Schema）、Evaluator（评估器）、Fixture、fail-closed 失败路由和记录；不得只画图、只列文件名或只生成说明。复杂任务至少完成工程线五问法，并用 `engineering_depth_router.py` 输出选择理由。


# 大任务与执行车道（large task and execution lanes）

状态：`active`
适用习惯：H10-H11

## large_task_gate

以下任一触发大任务：影响 3 个以上正式文件；规则/脚本/状态/日志中至少 3 类同时变化；需要大量只读审计；多阶段、多角色或多状态；用户明确要求完整执行/多 Agent/并发；单执行器容易漏项。

触发后必须输出 `large_task_gate.triggered`、理由、`lane_recommendation`、`write_owner` 和 `integration_owner`。大任务不自动要求多 Agent。

## lane 规则

可选：`serial_only`、`read_parallel`、`explore_plus_integrate`、`true_multi_task_parallel`。只有对象、目标、验收、范围、依赖和 blocker 已锁定，且写入不重叠时才可并行。读取冲突、判断风险或写入重叠时降级串行。

`explore_plus_integrate` 的 explorer 只读，唯一 integrator 拥有写权。`lane_parallel_router.py` 检出多个写入 owner 时返回 `blocked_multi_lane_write_conflict`。


# 单文件细节方案（per-file detail plan）

状态：`active`
适用习惯：H09

新增或修改机制文件、脚本、Schema、Validator 或节点前，为每个文件建立 `per_file_plan`。允许共享政策继承，但每个具体路径必须出现在一个计划组中，未列入路径不得修改。

必填字段：

```text
purpose
layer
inputs
outputs
core_decisions
trigger_conditions
route_rules
missing_info_policy
conflict_policy
blocked_if
examples
validation
user_review_points
```

`per_file_plan_validator.py` 必须在实现前验证这些字段。计划不是替代实现；实现后仍需脚本、Schema、Fixture、实际验证和 Git 收尾。


# 完成接力与失败路由（completion relay and failure routes）

状态：`active`
适用机制：M11-M13
适用习惯：H15-H18

## Completion Relay

完整任务先建立 `required_output_inventory`、`child_task_graph`、`remaining_work_check`。关闭前校验交付、验证、状态回写、人工复审和 Git 收尾；缺任一必交付项时继续或 blocked，不把局部文件、fallback、本地产物或技术探测写成完成。

完成状态只可为 `completed_verified`、`completed_pending_human_review`、`partial_completed`、`blocked`。状态报告必须分开列 `status_promotions` 与 `status_not_promoted`，并诚实写 `Tested`、`Not-tested`、`blocked_items`、`remaining_work`、`下一个目标`。

## 失败路由

```text
missing_fact -> product_fact_collection
fact_conflict -> fact_conflict_resolution
missing_compliance_evidence -> compliance_validation
capability_unverified -> capability_probe
write_scope_violation -> scope_repair
supply_insufficient -> supply_repair
state_not_allowed -> state_transition_repair
completion_overclaim -> completion_claim_repair
git_inconsistent -> git_closeout_repair
human_decision_needed -> human_decision_required
```

`failure_route_resolver.py` 输出 repair route、owner 和 `next_safe_step`。禁止只写 retry；用户反馈“不对、空、怪怪的”时先做内部自修审计，必要时补料、修复或阻断，而非要求用户诊断工程原因。

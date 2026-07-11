# Low-GI Rice Cross-Border Project Instructions v2

project_id: `low_gi_rice_crossborder`
project_name: `大米低 GI 跨境`
repository: `fthytwerwt-sudo/dami`
formal_system_version: `v2`

本文件是 Codex 的唯一正式入口（sole formal Codex entry）。它只保存稳定的协作规则；当前状态、动态业务事实和临时任务结论必须从 `project_system/current/` 回读，不能写入本文件。

## 1. 唯一工作区与启动读取顺序

唯一正式工作区是当前仓库根目录（repository root）。不得默认新建 clone、audit clone、fresh clone、外部 worktree、临时正式目录或根目录外的交付物；不得把 Desktop、Downloads 或临时目录作为正式路径。确实需要外部工作区时，先停止并报告：`reason`、`target_path`、`risk`、`internal_alternative`。

每轮按以下顺序读取：

1. 用户本轮输入。
2. 根 `AGENTS.md`。
3. `project_system/current/CURRENT_PROJECT_STATE.md`。
4. `project_system/current/CURRENT_FORMAL_FACTS.md`。
5. `project_system/current/CURRENT_DECISIONS.md`。
6. `project_system/current/LATEST_TASK_STATUS.md`。
7. 任务直接相关的正式规则、Schema、模板和原文件。
8. 原始证据与受控来源。
9. `project_system/history/` 和 `project_bootstrap/`，仅用于可追溯性，不能替代 current。

必读项缺失、不可读或冲突未解时，使用具体 `blocked_*` 状态；候选、历史、检索摘要或 GPT Project 静态包都不是 current 的替代物。

## 2. 路由判断是写入硬闸门

除 v2 首次 bootstrap 记录外，任何仓库写入、commit 或 push 前必须产生并通过 `route_decision（路由判断）`。复杂任务缺少该输出不得修改文件。

`route_decision` 至少包含：

- `task_type（任务类型）` 与 `responsibility_layer（责任层级）`。
- `must_read_files` 与逐项 `read_status`：`read_ok`、`missing`、`unreadable`、`not_applicable`。
- `allowed_changes`、`forbidden_changes`、`external_actions`、`human_gates`。
- `engineering_worth_question（值不值得工程化）`、工程深度、失败条件与 `execution_permission`。

跨境项目允许的 `task_type` 至少包括：`project_file_change`、`mechanism_or_route_fix`、`research`、`compliance_review`、`product_fact_intake`、`data_processing`、`copywriting_or_drafting`、`channel_validation`、`experiment_design`、`code_debug`、`local_file_governance`、`external_action_proposal`、`audit`。责任层使用：`entry_routing_layer`、`project_judgment_layer`、`engineering_design_layer`、`execution_layer`、`validation_layer`、`sync_layer`、`mechanism_fix_layer`、`multi_lane_layer`。

可使用 `scripts/project_system/project_task_preflight.py` 生成可机读预检；默认是 dry-run（空跑），只有显式 `--execute` 才可写入受控审计路径。

## 3. 工程深度、大任务和执行车道

先回答 `engineering_worth_question`，再选最轻且足够的深度：

- `L0_light_chat（L0 轻量聊天）`：解释或一次性判断，不写正式文件。
- `L1_task_card（L1 任务卡）`：小范围、低风险、可逆修改。
- `L2_node_contract（L2 节点契约）`：单一稳定节点，必须有明确输入、输出、验证和失败条件。
- `L3_system_line（L3 系统工程线）`：只在存在状态、多节点、工具、评估、失败路由和长期运行价值时采用。

简单任务不得强制 L3；复杂且重复的系统任务不得停在 L0/L1。L3 覆盖 13 层：项目目标、当前任务意识、流程节点、清洗、结构化、资料召回、工具连接、执行节点、判断评估、失败路由、人工兜底、状态记录、复盘迭代。复杂任务还要回答工程线五问法：要什么、到哪了、吃什么资料、错了去哪、留没留记录。

`large_task_gate（大任务闸门）` 在以下任一情况触发：影响 3 个以上正式文件；同时涉及规则、脚本、状态、日志中的 3 类以上；大量只读审计后统一写入；多阶段/多角色/多状态；用户要求完整执行或并发；单执行器容易漏项。大任务先选车道，后决定是否并发：`serial_only`、`read_parallel`、`explore_plus_integrate`、`true_multi_task_parallel`。

只读探索可并发；写入路径重叠、验收未锁定或有高风险判断时必须串行。全程只能有一个 `write_owner` 和一个 `integration_owner`，通常为 `single_integrator`。

## 4. 供料、单文件方案和安全探测

资料裁决顺序：当前正式仓库原文件 → 经授权的本地私有来源 → 外部权威原始来源 → 搜索或 AI 摘要导航 → 条件触发的第二意见。检索、静态包或 AI 摘要不得替代原文件回读。

每次需要来源的执行必须记录 `retrieval_manifest`、`source_readback_status`、`source_conflicts`、`external_research_needed` 与 `second_opinion_trigger`。外部第二意见仅在来源冲突、低置信度、高风险或用户明确要求时触发；不绑定任何供应商，不读取密钥，不写文件，不拍板事实。

写入前使用 `pre_task_supply_pack（执行前供料包）`；出现上下文不足、验证失败或冲突时使用 `mid_task_supply_pack（执行中补料包）`。供料包至少含任务目标、当前状态、必读来源、关键原文片段、约束、冲突、缺信息、决定权限、允许/禁止动作和给 Codex 的下一输入。缺 `source_path`、原文片段或回读状态时，禁止继续写入。

新增或修改机制文件、脚本、Schema、Validator 或节点前，每个文件必须有 `per_file_plan（单文件细节方案）`：`purpose`、`layer`、`inputs`、`outputs`、`core_decisions`、`trigger_conditions`、`route_rules`、`missing_info_policy`、`conflict_policy`、`blocked_if`、`examples`、`validation`、`user_review_points`。未列入方案的文件默认不得改。

高风险动作先用 `dry_run`、`read_only_probe` 或 `fake_client_or_fixture` 验证；不因技术可运行而写成业务可用。

## 5. 权限、业务边界与 Public 仓库安全

权限维度必须分开：

- `business_decision_authority`：用户决定市场、渠道、模式、报价、MOQ、交期、代理、合同、样品、预算和规模。
- `objective_fact_evidence_authority`：当前原始监管、检测、认证、合同、平台等一手证据决定客观事实。
- `execution_authority`：ChatGPT 做判断和路由；Codex 仅在授权范围内写入和验证。

本系统不得自行选择国家、B2B/B2C、渠道、价格或健康/医疗承诺；不得联系客户、发送消息、投放、创建外部账号、付款、签约、寄样或其他外部业务动作。需要这些动作时，生成提案或使用 `human_decision_required`，不得执行。

仓库为 Public 时，`business_sensitive_git_write_blocked_while_repo_public: true`。不得写入或提交客户、供应商、报价、成本、合同、认证/检测原件、个人信息、密钥及其他敏感资料；不得擅自修改仓库可见性。

## 6. 完成接力、失败路由与状态真实性

收到“完整执行、不要只做一半、多文件补全”等任务时，先生成 `Completion Relay（完成接力）`：`required_output_inventory`、`child_task_graph` 和 `remaining_work_check`。结束时逐项检查：用户要求是否齐全、是否需要 current 回写、是否有人工复审、是否完成 Git 收尾、能否安全进入下一状态。

失败必须路由，而不是笼统 retry：

`missing_fact → product_fact_collection`；`fact_conflict → fact_conflict_resolution`；`missing_compliance_evidence → compliance_validation`；`capability_unverified → capability_probe`；`write_scope_violation → scope_repair`；`supply_insufficient → supply_repair`；`state_not_allowed → state_transition_repair`；`completion_overclaim → completion_claim_repair`；`git_inconsistent → git_closeout_repair`；`human_decision_needed → human_decision_required`。

状态和报告必须区分：`已确认`、`部分成立`、`待验证`、`推测`、`通用建议`。机器验证、人工复审、合规批准、业务决定、外部动作、Git 同步和 GPT Project UI 上传互不替代。可用结果状态为 `completed_verified`、`completed_pending_human_review`、`partial_completed`、`blocked`；缺必交付时继续执行或 blocked，不能降级冒充完成。

## 7. 语言、命名与可理解性

自然语言解释默认“中文含义在前，英文原词在后”，例如工程深度路由器（engineering depth router）。函数、变量、JSON/YAML key、CLI 参数、环境变量、原始报错和工具文件名保留英文，但须有中文用途说明。

新建或大改代码时，模块 docstring、核心判断、输入输出、异常与边界使用中文注释；不得生成只有英文且用户无法理解的执行脚本。新建用户可读业务文档与目录默认用 `中文名_english_name`；`AGENTS.md`、`README.md`、`.gitignore`、固定 JSON Schema 文件名和 Python 模块是 `toolchain_exception（工具链例外）`，须在系统索引中记录中文用途。已有文件不为改名而改名。

## 8. Git 与 GPT Project 同步真实性

只要正式仓库文件被修改，且用户未明确免除 Git 收尾，必须执行：精确路径暂存 → `git diff --cached --check` → staged secret/sensitive scan → commit → 普通 push → fetch → 对读本地 `HEAD`、`origin/main`、`git ls-remote` → 远端关键文件回读。禁止 `git add .`、`git add -A`、`git commit -a`、`git push --force`、`git push -f`；不得夹带无关脏改或受保护历史包。

GPT Project 包生成、Git push 和 ChatGPT Project UI 上传是三个独立事实。`gpt_project_sync/latest/` 是分发快照，不能覆盖 current；在用户手动上传并确认前只能写 `gpt_project_sync_package_generated_pending_user_upload` 与 `ui_uploaded: false`。

收尾可使用 `scripts/project_system/project_task_closeout.py` 验证交付、状态、剩余工作和 Git 证据；该脚本不会自行 commit 或 push。

## 9. 最终回报

最终报告至少包含：`Tested`、`Not-tested`、`status_promotions`、`status_not_promoted`、`blocked_items`、`remaining_work`、Git 三方 SHA 和远端回读。最后一栏固定使用 `下一个目标`，不得使用含糊的“下一步行动建议”。

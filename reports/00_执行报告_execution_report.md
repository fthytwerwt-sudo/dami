# 大米低 GI 网页获客工具底座：执行记录

- 状态：`partial_completed`
- 日期：2026-07-21
- 模式：`draft_only`
- 业务事实来源：`fthytwerwt-sudo/dami/project_system/current/`
- 本仓库定位：技术工具与合成沙箱，不是市场、产品、价格、合规或客户事实源

## 1. Route decision｜路由判断

- `task_type`：`system_tooling_and_architecture`
- `responsibility_layer`：`project_judgment_layer`、`engineering_design_layer`、`execution_layer`、`validation_layer`、`multi_lane_layer`、`sync_layer`
- `engineering_depth`：`L3_system_line`
- `lane`：`explore_plus_integrate`
- `write_owner` / `integration_owner`：单一主执行器
- `execution_permission`：`private_tool_repo_build_and_sandbox_only`
- `allowed_changes`：本 Private 工具仓库中的非敏感代码、Schema、合成 Fixture、测试、配置、许可证和文档
- `forbidden_changes`：`dami` current、真实客户/联系人/账号/消息、密钥、隐藏 API、反检测、验证码绕过、真实提交和发送
- `external_actions`：公开 GitHub 只读调研、固定版本依赖安装、创建并普通推送 Private 工具仓库
- `human_gates`：许可证正式接受、真实平台/账号/客户、真实提交、`supervised`、`bounded_autonomy`、市场/产品/低 GI 宣称

## 2. Process boot 与供料包

1. 要什么：开源组合优先、可替换的网页抓取/DOM/知识召回/政策/状态/追踪底座。
2. 到哪了：候选研究和人工边界已完成；正式市场、产品、合规和客户执行未开始。
3. 吃什么资料：`dami` current/rules、上一轮 6 份私有规划、GitHub 官方 README/LICENSE/Release/Commit/Issue/Docs。
4. 错了去哪：按 `open_source_gap`、`capability_unverified`、`license_unclear`、`integration_conflict`、`platform_terms_block`、`checkpoint_failure`、`git_inconsistent` 等路由修复。
5. 留没留记录：本报告、选型文档、版本/工具注册表、测试和 Git 证据共同记录。

供料允许合成技术验证，不允许真实产品事实、客户或外发。上一轮“无依赖原型”由本轮更具体的“真实开源组合沙箱”覆盖，但业务状态与发送禁令不变。

## 3. Completion Relay｜完成接力

### required_output_inventory

- 开源候选矩阵、两套架构、唯一推荐和自建证明。
- 工具/版本/许可证清单与统一 Adapter。
- 网页抓取、DOM 填入、结构化、知识召回、政策闸门、LangGraph、Checkpoint/Resume、Trace。
- 七份未来规划、测试报告、Private GitHub 三方 SHA 和远端回读。

### child_task_graph

```text
Explorer A-F 只读官方证据
        ↓
单一整合者选型与逐文件计划
        ↓
测试 RED → 最小实现 GREEN → 重构
        ↓
集成沙箱与边界验证
        ↓
精确 Git closeout 与远端回读
```

## 4. Per-file plans｜逐文件方案

以下计划组逐项继承全部必填字段；每个具体路径都已显式列出。未列出的文件不得创建。

### P1 根文件与依赖

- `paths`：`.gitignore`、`README.md`、`pyproject.toml`、`requirements.lock`、`LICENSE`
- `purpose`：定义安全边界、安装/运行方式、固定依赖和本仓库代码许可。
- `layer`：项目目标层、工具连接层、状态记录层。
- `inputs`：推荐组合、Python 3.12、官方许可证与可安装版本。
- `outputs`：可复现环境、中文入口、被忽略的运行数据。
- `core_decisions`：只锁最小依赖；不复制第三方源码；不提交浏览器缓存、数据库、日志或 secret。
- `trigger_conditions`：选型完成且许可证可识别。
- `route_rules`：不清晰许可证转 `legal_review_required`；不可安装转 `capability_probe`。
- `missing_info_policy`：不猜版本或许可，保留 `recheck_later`。
- `conflict_policy`：官方 LICENSE 优先于 README 宣称。
- `blocked_if`：依赖要求付费 API、反检测、隐藏接口或真实账号。
- `examples`：README 中给出本地合成沙箱命令。
- `validation`：干净 venv 安装、版本输出、secret/sensitive scan。
- `user_review_points`：项目组合、许可证正式采用、生产部署。

### P2 架构与规划文档

- `paths`：`docs/01_开源项目选型_open_source_selection.md`、`docs/02_组合架构_composed_architecture.md`、`docs/03_知识库契约_knowledge_contract.md`、`docs/04_客户对话边界_conversation_policy.md`、`docs/05_LangGraph流程蓝图_langgraph_blueprint.md`、`docs/06_Runtime运行时契约_runtime_contract.md`、`docs/07_未来定制规划_customization_blueprint.md`
- `purpose`：记录候选矩阵、两套架构、知识/政策/流程/运行时和升级路线。
- `layer`：L3 全 13 层。
- `inputs`：官方 GitHub 证据、current 状态和沙箱实测。
- `outputs`：可审计、可替换、中文优先的工程契约。
- `core_decisions`：技术能力与业务授权分层；Adapter 隔离底层项目。
- `trigger_conditions`：官方证据回读完成。
- `route_rules`：候选只在证据充分时进入采用层；否则 reference/recheck/reject。
- `missing_info_policy`：标记 `待验证`，不得提升。
- `conflict_policy`：许可证与能力冲突分别记录，安全/官方原文优先。
- `blocked_if`：把规划写成生产完成或业务决定。
- `examples`：每份文档提供合成输入输出/状态例子。
- `validation`：链接、术语、状态边界和实测结果交叉检查。
- `user_review_points`：唯一组合、真实平台、市场/产品和自动化升级。

### P3 工具与版本配置

- `paths`：`config/tool_registry.yaml`、`config/version_lock.yaml`
- `purpose`：机器可读记录工具职责、Adapter、采用方式、版本、许可和替换方案。
- `layer`：工具连接层、状态记录层。
- `inputs`：最终选型和实际安装版本。
- `outputs`：工具注册表与版本锁。
- `core_decisions`：版本精确固定；容器未来锁 digest；Git 依赖未来锁 commit。
- `trigger_conditions`：项目纳入 adopt/reference/recheck/reject 矩阵。
- `route_rules`：许可不清不得标为 adopted。
- `missing_info_policy`：使用 `unverified` 和复核日期。
- `conflict_policy`：实际安装版本与配置不一致即测试失败。
- `blocked_if`：出现 secret、账号或真实业务配置。
- `examples`：每项提供中文名称、Adapter 和 replacement。
- `validation`：YAML 解析、版本命令对读。
- `user_review_points`：正式接受的依赖范围。

### P4 JSON Schema

- `paths`：`schemas/lead_record.schema.json`、`schemas/knowledge_result.schema.json`、`schemas/conversation_state.schema.json`、`schemas/tool_action.schema.json`、`schemas/approval_request.schema.json`
- `purpose`：约束潜客、知识、会话、工具动作和审批请求。
- `layer`：清洗层、结构化层、判断评估层、状态记录层。
- `inputs`：统一接口和政策状态枚举。
- `outputs`：Draft 2020-12 JSON Schema。
- `core_decisions`：每个字段中文 `description`；缺来源/状态 fail-closed。
- `trigger_conditions`：接口字段确定。
- `route_rules`：Schema 失败转输入修复，不进入后续节点。
- `missing_info_policy`：必填缺失即拒绝；可选字段显式 null/空数组。
- `conflict_policy`：冲突必须有 `conflicts`，不能覆盖旧证据。
- `blocked_if`：允许真实个人信息或自动发送默认值。
- `examples`：由合成 Fixture 覆盖。
- `validation`：`jsonschema` 元 Schema 和 Fixture validation。
- `user_review_points`：未来正式数据字段与保留策略。

### P5 统一接口与网页/潜客实现

- `paths`：`src/web_agent_toolkit/__init__.py`、`src/web_agent_toolkit/contracts.py`、`src/web_agent_toolkit/web.py`、`src/web_agent_toolkit/lead.py`
- `purpose`：定义统一 Adapter，运行本地网页抓取、DOM 填入、结构化、清洗和评分。
- `layer`：清洗、结构化、工具连接、执行、评估层。
- `inputs`：localhost 合成网页、selector 合约、合成 lead。
- `outputs`：网页证据、企业记录、评分、表单填入结果。
- `core_decisions`：Playwright 使用 role/label/test-id；只填不提交；来源与时间保留。
- `trigger_conditions`：只允许 localhost/显式 allowlist。
- `route_rules`：robots/ToS/登录/验证码/反检测需求均阻断；submit 永远走 Fake。
- `missing_info_policy`：缺字段保留理由并阻断评分/草稿。
- `conflict_policy`：保留全部来源，实体歧义转人工。
- `blocked_if`：真实域名、账号、私有 API 或提交动作。
- `examples`：合成公司页与联系表单。
- `validation`：测试先 RED；抓取、结构化、去重、评分、DOM 值和 submit_count=0。
- `user_review_points`：未来真实来源 allowlist 与平台 Adapter。

### P6 知识、政策、运行时和流程实现

- `paths`：`src/web_agent_toolkit/knowledge.py`、`src/web_agent_toolkit/policy.py`、`src/web_agent_toolkit/runtime.py`、`src/web_agent_toolkit/workflow.py`、`src/web_agent_toolkit/sandbox.py`
- `purpose`：SQLite FTS5 合成召回、确定性政策、SQLite/JSONL 状态与 Trace、LangGraph 中断/恢复和端到端沙箱。
- `layer`：资料召回、判断评估、失败路由、人工兜底、状态记录、复盘层。
- `inputs`：合成知识、消息、客户状态、Fake approval。
- `outputs`：带来源知识结果、政策状态、草稿、Checkpoint、Trace 和提交前阻断。
- `core_decisions`：缺/冲突知识 fail-closed；敏感条件确定性升级；仅 `draft_only`；本地模拟 supervised。
- `trigger_conditions`：Schema 通过且 thread_id 存在。
- `route_rules`：知识缺失、政策不确定、审批拒绝、checkpoint 失败均走显式分支。
- `missing_info_policy`：不生成事实，返回 `BLOCK_REPLY`/`ESCALATE_HUMAN`。
- `conflict_policy`：冲突知识禁止自动草稿。
- `blocked_if`：模型自由决定政策、自动 submit、真实消息或无 checkpoint。
- `examples`：安全问题、价格问题、冲突事实和恢复流程。
- `validation`：测试先 RED；检索来源、政策枚举、interrupt/resume、SQLite 重开、Trace 回读。
- `user_review_points`：知识版本、审批人、supervised/bounded_autonomy 条件。

### P7 测试与 Fixture

- `paths`：`tests/conftest.py`、`tests/test_web_and_lead.py`、`tests/test_knowledge_and_policy.py`、`tests/test_runtime_and_workflow.py`、`tests/test_schemas_and_boundaries.py`、`tests/fixtures/synthetic_company.html`、`tests/fixtures/synthetic_knowledge.json`、`tests/fixtures/synthetic_leads.json`
- `purpose`：TDD 锁定所有可运行能力和禁止边界。
- `layer`：验证层。
- `inputs`：纯合成 `.example`/localhost 数据。
- `outputs`：可重复测试与端到端证据。
- `core_decisions`：先看预期 RED，再最小 GREEN；不 mock Playwright DOM 或 SQLite。
- `trigger_conditions`：每个生产能力实现前。
- `route_rules`：非预期错误先修测试；行为失败才实现。
- `missing_info_policy`：测试数据不足先补合成 Fixture。
- `conflict_policy`：实测优先，文档随实测修正。
- `blocked_if`：真实企业、邮箱、账号、网络外发或随机不稳定测试。
- `examples`：重复 lead、知识冲突、价格升级、人工恢复、submit 阻断。
- `validation`：全套 pytest 重跑、无 flaky、无外部网络。
- `user_review_points`：未来真实平台测试需单独授权。

### P8 许可证与最终报告

- `paths`：`LICENSES/THIRD_PARTY_LICENSES.md`、`reports/00_执行报告_execution_report.md`
- `purpose`：记录第三方许可、来源、采用边界、测试、状态与 Git 证据。
- `layer`：项目判断、验证、同步、复盘层。
- `inputs`：官方 LICENSE、实际 diff/test/Git 输出。
- `outputs`：非法律意见的许可清单和完成真实性报告。
- `core_decisions`：技术、人工、业务、Git 分层；不复制第三方许可证文本全文。
- `trigger_conditions`：选型和每次 closeout。
- `route_rules`：许可不清转法律复核；Git 不一致转修复。
- `missing_info_policy`：明确 Not-tested/blocked/remaining。
- `conflict_policy`：官方 LICENSE 和远端 Git 证据优先。
- `blocked_if`：完成过度声称或遗漏未知项。
- `examples`：采用/拒绝表、三方 SHA、远端回读。
- `validation`：官方链接、扫描、Git closeout 对读。
- `user_review_points`：最终项目组合、许可证和下一阶段。

## 5. 实施与验证日志

### 已确认

- TDD 红灯：首次 `pytest -q` 在收集阶段出现 3 个 `ModuleNotFoundError`，原因是生产模块尚未实现，符合预期。
- TDD 绿灯：实现最小 Adapter、Schema、政策、Runtime 和 LangGraph 图后，`11 passed`。
- 真实 Playwright：已安装 Chromium revision `1228`；localhost 页面标题、正文、test-id 字段和 label 表单均由浏览器真实读取/填入。
- 闭环 CLI：`python -m web_agent_toolkit.sandbox` 依次完成 crawl、extract、normalize、dedupe、score、knowledge、draft、policy、interrupt/resume 和 DOM fill。
- 最终动作：`submit_count=0`、`stage=FILLED_PENDING_SUBMIT`、`send_status=BLOCKED`。
- 持久化：SQLite 业务 checkpoint 重开可读；LangGraph checkpointer 关闭重开后可用同一 `thread_id` resume。
- 边界扫描：`src/` 未发现真实 send、私有 API、验证码绕过、stealth 或坐标点击实现；合成 Fixture 无真实企业/客户/账号。
- 配置验证：5 个 JSON Schema 合法且顶层字段含中文说明；2 个 YAML 可解析；`pip check` 无破损依赖；`compileall` 通过。

### 部分成立

- 开源项目调研覆盖全部要求能力并形成候选矩阵；已实际采用项目的版本/许可证有官方回读，未采用长尾候选的最新 tag/HEAD 仍有 `待验证` 标记。
- `supervised` 只在 localhost 以 `Command(resume={approved: true})` 模拟；不是正式运行模式，也没有真实审批身份。

### Not-tested / 未验证

- 真实网站 robots/ToS、页面变更、登录、验证码、真实账号和真实 DOM 平台均未测试且不在本轮授权范围。
- 真实知识库、产品事实、检测/认证、合规、低 GI、市场、渠道、价格、MOQ、客户和多语言均未测试。
- LLM、embedding、向量数据库、CRM、消息通道、OpenTelemetry backend 和并发/负载未测试。
- 许可证清单不是法律意见；mixed/modified/source-available 候选需正式法律复核。

## 6. 状态推进与未推进

### status_promotions

- `toolkit_local_implementation`：`planned` → `completed_verified_local_synthetic`
- `playwright_dom_probe`：`unverified` → `verified_localhost_only`
- `langgraph_checkpoint_resume`：`unverified` → `verified_local_synthetic`
- `source_constrained_policy_skeleton`：`planned` → `verified_deterministic_fixture`

### status_not_promoted

- 市场、渠道、B2B/B2C、产品、合规、价格、客户、平台权限、真实外发：保持未决定/未验证。
- `supervised` 和 `bounded_autonomy`：未启用。
- 工具可运行没有提升为平台允许、业务可用或客户沟通完成。

## 7. Git closeout

- 本地新仓库：`main` 已完成 Lore commit；实现提交为 `6dde4f65a7a6b98fd07f926a6caee90beaff49ea`，提交后工作区对读为 clean。
- 目标远端：`fthytwerwt-sudo/dami-web-agent-toolkit` Private。
- 阻断：`gh` keyring token 无效；GitHub Connector 无创建仓库能力；可用 in-app Browser 未登录。
- 已配置预期 `origin` 并尝试普通 push；GitHub 返回 `Repository not found`，与“远端尚未创建/当前凭证不可访问”一致。
- `origin/main`、`git ls-remote`、远端关键文件回读：均因目标远端尚未创建而未验证。
- 本地关键文件回读：commit 中 README 与工作区 SHA-256 均为 `73108a4c9b656f9b4d34c2035d90cb4a13b774d9a4f53cf460503bba8212997e`。
- 原 `dami` 仓库 current 未修改；独立工具仓库不成为业务事实源。

## 8. blocked_items 与 remaining_work

- `blocked_git_remote_auth`：用户需在已保留的 GitHub 登录页登录，或运行 `gh auth login` 恢复凭证，之后才能创建 Private repo、push 和三方 SHA/远端回读。
- `remaining_work`：远端创建/推送/回读；人工复核项目组合与许可证；选择正式产品/市场前不得进入真实数据和平台阶段。

## 9. 下一个目标

恢复 GitHub 认证并完成 Private 远端三方 SHA 与关键文件回读；在此之前不推进真实客户或发送能力。

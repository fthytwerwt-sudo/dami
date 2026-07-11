# 任务路由与跨境状态机

状态：`active`
适用机制：M04、M13

## 通用规则

每次状态判断必须记录：`entry_condition`、`allowed_actions`、`forbidden_actions`、`required_inputs`、`required_evidence`、`human_gate`、`done_when`、`failure_condition`、`next_possible_states`。文档生成、代码完成或单项机器验证均不会自动推进业务状态。

## 1. `collaboration_system_activation`

- `entry_condition`：正式协作入口尚未建立或正在受控激活。
- `allowed_actions`：规则、事实入口、模板、验证和同步包建设。
- `forbidden_actions`：任何外部业务执行或业务结论定案。
- `required_inputs`：激活授权、迁移裁决、仓库现状。
- `required_evidence`：入口可达、机制登记完整、验证通过。
- `human_gate`：正式激活授权。
- `done_when`：正式入口和当前状态已落库并经验证。
- `failure_condition`：存在平行正式入口、范围污染或关键规则冲突。
- `next_possible_states`：`product_fact_collection`、`human_decision_required`、`blocked`。

## 2. `product_fact_collection`

- `entry_condition`：协作系统已激活，产品事实字段和证据需求明确。
- `allowed_actions`：收集、索引、去重和标记产品资料。
- `forbidden_actions`：无证据声明、正式报价、外发或市场定案。
- `required_inputs`：事实字段清单、资料读取授权。
- `required_evidence`：原始资料、签发者、日期、适用范围、有效期。
- `human_gate`：敏感资料读取及事实批准。
- `done_when`：关键事实有可回读证据，缺口和冲突均已登记。
- `failure_condition`：核心资料缺失、不可读或相互冲突。
- `next_possible_states`：`product_evidence_validation`、`human_decision_required`、`blocked`。

## 3. `product_evidence_validation`

- `entry_condition`：已有待核验的产品事实与直接证据。
- `allowed_actions`：原文件回读、范围核对、有效期和冲突检查。
- `forbidden_actions`：把摘要、推论或机器抽取直接升为正式事实。
- `required_inputs`：候选事实、原始证据、验证标准。
- `required_evidence`：逐条证据映射与验证结果。
- `human_gate`：正式事实批准；专业结论由合格人员确认。
- `done_when`：可确认事实、待验证项和阻断项清晰分离。
- `failure_condition`：证据不能直接证明声明或专业复核缺失。
- `next_possible_states`：`market_screening`、`compliance_validation`、`human_decision_required`、`blocked`。

## 4. `market_screening`

- `entry_condition`：最小产品事实足以定义筛选条件。
- `allowed_actions`：公开研究、候选比较、反证和验证计划。
- `forbidden_actions`：将评分、建议或研究摘要写成正式市场决定。
- `required_inputs`：筛选问题、产品边界、研究口径。
- `required_evidence`：可回读来源、方法、限制、时效和反证。
- `human_gate`：候选短名单及正式方向选择。
- `done_when`：候选、证据、限制和下一步验证计划齐全。
- `failure_condition`：来源不可比、过期或适用性不明。
- `next_possible_states`：`compliance_validation`、`human_decision_required`、`blocked`。

## 5. `compliance_validation`

- `entry_condition`：产品边界与候选适用范围明确。
- `allowed_actions`：适用规则、标签、认证、声明和准入要求核验。
- `forbidden_actions`：AI 自行批准合规、健康或医疗结论。
- `required_inputs`：产品事实、适用范围、拟议动作或声明。
- `required_evidence`：当前官方原文、直接产品证据、专业意见记录。
- `human_gate`：合规负责人或合格专业人员确认。
- `done_when`：适用要求、证据缺口、禁止项和批准记录齐全。
- `failure_condition`：关键规则或产品证明缺失、冲突或已过期。
- `next_possible_states`：`b2b_channel_validation`、`b2c_channel_validation`、`human_decision_required`、`blocked`。

## 6. `b2b_channel_validation`

- `entry_condition`：相关范围与最小合规边界已获确认。
- `allowed_actions`：渠道研究、公开信息整理、名单和话术草稿、沙箱测试。
- `forbidden_actions`：未授权触达、承诺、签约、寄送或扩量。
- `required_inputs`：渠道假设、对象标准、风险边界。
- `required_evidence`：来源、样本、指标、停止线和验证记录。
- `human_gate`：对象、模板、频率和任何外发动作批准。
- `done_when`：渠道可行性结论、限制和下一实验清晰可追溯。
- `failure_condition`：证据不足、风险超限或渠道不可达。
- `next_possible_states`：`lead_generation_test`、`offer_validation`、`human_decision_required`、`blocked`。

## 7. `b2c_channel_validation`

- `entry_condition`：相关范围与最小合规边界已获确认。
- `allowed_actions`：渠道研究、内容与页面草稿、沙箱测试。
- `forbidden_actions`：未授权发布、上架、投放、收款或公开承诺。
- `required_inputs`：渠道假设、受众边界、内容与风险标准。
- `required_evidence`：来源、样本、指标、停止线和验证记录。
- `human_gate`：账号操作、发布、预算和外部可见动作批准。
- `done_when`：渠道可行性结论、限制和下一实验清晰可追溯。
- `failure_condition`：证据不足、风险超限或渠道不可用。
- `next_possible_states`：`lead_generation_test`、`offer_validation`、`human_decision_required`、`blocked`。

## 8. `lead_generation_test`

- `entry_condition`：小样本对象、模板、频率、数据边界和授权明确。
- `allowed_actions`：仅执行获批样本动作并记录结果。
- `forbidden_actions`：扩大对象、自动群发、改变承诺或绕过退出机制。
- `required_inputs`：批准的实验卡、对象清单、模板和停止规则。
- `required_evidence`：发送记录、响应、异常、数据来源和授权记录。
- `human_gate`：正式触达及样本范围批准。
- `done_when`：样本结果、异常和可复核结论齐全。
- `failure_condition`：投诉、权限、隐私、交付或声誉停止线触发。
- `next_possible_states`：`offer_validation`、`b2b_channel_validation`、`b2c_channel_validation`、`blocked`。

## 9. `offer_validation`

- `entry_condition`：产品、需求和交易输入有足够证据。
- `allowed_actions`：在获批范围内测试价值主张与条件草案。
- `forbidden_actions`：未经批准的价格、数量、交付、功效或合同承诺。
- `required_inputs`：候选方案、成本与履约输入、需求证据、实验卡。
- `required_evidence`：批准记录、反馈、风险与履约核验。
- `human_gate`：任何正式交易条件、报价、样品或承诺批准。
- `done_when`：测试证据、可行边界与人工决定齐全。
- `failure_condition`：履约、合规、成本或需求假设不成立。
- `next_possible_states`：`pilot_execution`、`human_decision_required`、`blocked`。

## 10. `pilot_execution`

- `entry_condition`：试点范围、预算、责任、合规、停止线和回滚已获批准。
- `allowed_actions`：严格按批准的执行单实施和监测。
- `forbidden_actions`：自动扩量、跨范围复制或改变关键条件。
- `required_inputs`：批准的试点计划、资源、责任人与回滚方案。
- `required_evidence`：过程记录、指标、成本、风险事件和复盘。
- `human_gate`：启动、重大偏差、额外支出和外部承诺批准。
- `done_when`：结果、成本、风险、偏差和人工复盘完整。
- `failure_condition`：安全、合规、财务、客户或回滚停止线触发。
- `next_possible_states`：`scale_or_stop`、`human_decision_required`、`blocked`。

## 11. `scale_or_stop`

- `entry_condition`：试点证据和复盘完整。
- `allowed_actions`：形成扩量、继续验证、暂停或停止选项。
- `forbidden_actions`：AI 自动决定或执行规模化。
- `required_inputs`：试点结果、风险、资源和替代方案。
- `required_evidence`：完整指标、异常、成本与证据限制。
- `human_gate`：用户正式决定。
- `done_when`：决定、依据、范围、条件和复核点已记录。
- `failure_condition`：证据不足或风险不可接受。
- `next_possible_states`：`pilot_execution`、`human_decision_required`、`blocked`，或由正式决定指定的已定义状态。

## 12. `human_decision_required`

- `entry_condition`：存在业务、合规、资金、外发、删除、不可逆或重大分支决定。
- `allowed_actions`：呈现选项、证据、风险、替代损失和默认安全动作。
- `forbidden_actions`：AI 代替用户或专业责任人拍板。
- `required_inputs`：待决定事项、证据、影响面和授权需求。
- `required_evidence`：选项依据、风险和可追溯授权记录。
- `human_gate`：对应授权人明确决定。
- `done_when`：决定的时间、范围、条件、有效期和撤销方式已记录。
- `failure_condition`：授权模糊、过期或无法验证。
- `next_possible_states`：按有效决定进入本文件已定义的目标状态，或 `blocked`。

## 13. `blocked`

- `entry_condition`：关键事实、权限、能力、证据、安全或写入条件缺失。
- `allowed_actions`：诊断、补证据、提出替代路线及损失、保持现状。
- `forbidden_actions`：绕过阻断或用降级结果冒充完成。
- `required_inputs`：具体阻断码、触发证据和受影响目标。
- `required_evidence`：解除条件及其验证记录。
- `human_gate`：仅在阻断涉及授权或业务取舍时需要。
- `done_when`：阻断解除且证据满足原状态进入条件。
- `failure_condition`：解除证据仍缺失或产生新阻断。
- `next_possible_states`：返回原状态或 `human_decision_required`。

## 四态完成

- `completed_verified`
- `completed_pending_human_review`
- `partial_completed`
- `blocked`

每次必须同时写明未推进的状态；低层完成不得自动提升为人工、合规、商业或外部同步完成。

## v2 路由与状态转换衔接

状态机不替代 `route_decision`：前者判断项目状态允许什么，后者确定本轮任务类型、必读来源、允许范围、工程深度和执行权限。任何状态回写前需通过 `state_transition_validator.py`；业务状态、市场、渠道、价格、合规、外部执行等仍需要相应人工闸门。`cross_project_collaboration_system_v2_active` 只表示协作系统技术落成，不推进任何业务状态。

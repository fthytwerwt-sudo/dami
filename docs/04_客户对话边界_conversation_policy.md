# 客户对话、状态和政策边界

## 1. 状态分层

客户状态未来最少包含：画像、历史沟通、客户阶段、已确认需求、未解决问题、语言偏好、联系渠道、跟进节奏、禁止事项。当前没有真实客户数据，只有 `thread-graph-1` 等合成编号。

必须分开：候选潜客、已人工确认客户、草稿、已批准草稿、DOM 已填、提交待执行、平台回执、业务接受。任何一层都不能推断下一层已完成。

## 2. 政策输出

| 决定 | 含义 | 后续 |
|---|---|---|
| `ALLOW_DRAFT` | 允许生成带来源候选草稿 | 仍进入人工 interrupt |
| `REQUIRE_REVIEW` | 触及敏感条件 | 必须人工，不得自动执行 |
| `BLOCK_REPLY` | 知识缺失或不允许回答 | 停止并补料 |
| `BLOCK_SEND` | 不允许提交/发送 | 当前所有路径最终状态 |
| `ESCALATE_HUMAN` | 冲突、合规或客户要求真人 | 转人工队列 |

必须人工：价格、MOQ、交期、付款、独家/区域授权、样品、合同、退款、投诉、低 GI、营养/健康宣称、无证据、法律/合规、正式条件修改、低置信度、真人请求。

## 3. 权限矩阵

| 动作 | 机器 | 人工 | 本轮 |
|---|---|---|---|
| 读取合成知识/网页 | 可 | 可复核 | 允许 |
| 生成来源约束草稿 | 可 | 必须复核 | 允许 |
| 决定市场/价格/产品/承诺 | 不可 | 用户 | 禁止 |
| 政策放行敏感事项 | 不可 | 授权审批人 | 禁止 |
| DOM 填入测试页 | Fake approval 后 | 可复核 | 允许 |
| DOM 提交/真实发送 | 不可 | 仍需单独授权和平台 Adapter | 禁止 |
| 真实账号/客户历史 | 不可擅自读取 | 用户单独授权 | 禁止 |

## 4. 三种 Runtime 模式

- `draft_only`：生成草稿、保存状态；当前唯一启用。
- `supervised`：每次执行前由明确审批人批准；本轮只在 localhost 模拟，不代表已启用。
- `bounded_autonomy`：仅在平台条款、合规、幂等、停止开关、审计和业务权限全部通过后评估；当前不可用。

升级不能只改一个配置键。必须增加独立 Adapter、真实平台测试、审批身份、幂等键、速率限制、回执读取、停止条件、数据保留和事故回滚。

## 5. Prompt 与规则优先级

优先级：系统安全边界 → 项目政策版本 → 当前正式事实 → 人工审批 → 客户/市场/产品 Prompt → 模型草稿。低层 Prompt 不得覆盖高层规则。

未来 Prompt 必须记录 `system_prompt_version/market_prompt_version/product_prompt_version/customer_prompt_version/template_version/policy_version`。模型输出必须带召回来源和政策结果，禁止自由补价格、认证或健康结论。

## 6. 失败路由

`knowledge_missing → supply_repair`；`knowledge_conflict → human_fact_resolution`；`restricted_term → human_review`；`approval_rejected → stop_run`；`checkpoint_failure → runtime_repair`；`platform_terms_unknown → platform_terms_block`；`duplicate_action → idempotency_block`；`submit_attempt → BLOCK_SEND`。

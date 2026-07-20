# 未来定制化规划

这是一份完成度较高的工程蓝图，不是生产系统完成声明。所有条目默认 `planned_pending_user_decision`。

## 1. 产品和市场定制

| 维度 | 配置/数据 | Adapter/规则 | 人工闸门 |
|---|---|---|---|
| 产品 | `product_id/knowledge_scope/fact_version` | KnowledgeAdapter + 产品 Schema | 产品事实、检测、低 GI/健康表述 |
| 国家 | `market_id/language/compliance_version` | MarketPolicyAdapter | 正式市场、监管证据 |
| 买家类型 | `buyer_type/qualification_rules` | LeadScoringAdapter | B2B/B2C 和 ICP |
| 平台 | `channel_id/url_allowlist/dom_contract` | Web/Channel Adapter | 条款、账号、提交权限 |
| Offer | `offer_id/version/effective_at` | OfferRepository | 价格、MOQ、交期、付款 |
| 审批 | `risk_class/approver_role/SLA` | ApprovalAdapter | 审批人和授权范围 |

当前这些正式业务选择全部未推进。

## 2. 客户定制

客户实体分层保存：稳定画像、历史沟通索引、当前阶段、已确认需求、未解决问题、语言偏好、联系渠道、跟进节奏、禁止事项/opt-out。原始沟通和结构化摘要分开；摘要必须带来源消息 ID 和版本。

客户范围变化触发重新召回和政策评估，不能复用旧批准草稿。任何个人数据接入前需数据治理、访问权限和保留期确认。

## 3. Prompt 和政策定制

```text
system safety prompt
  → market prompt
  → product prompt
  → customer context prompt
  → approved reply template
  → deterministic policy gate
  → human approval
```

每层记录版本、hash、effective_at、owner、approval_status 和 rollback_version。风险/审批/阻断规则使用结构化配置和单测，不只写自然语言 Prompt。模型评估至少覆盖事实引用、禁止承诺、语言、拒答、冲突和 Prompt injection。

## 4. 工具定制

| Adapter | 当前 | 未来候选 | 接入前验证 |
|---|---|---|---|
| Web crawler | Playwright localhost | Trafilatura/Scrapy/Crawlee/Crawl4AI | robots/ToS、SSRF、allowlist、速率 |
| Platform DOM | Playwright local | 每平台独立 locator contract | 账号权限、UI 变更、回执、无验证码绕过 |
| CRM | 无 | Chatwoot/Twenty/Baserow API Adapter | 许可、数据导出、字段映射、删除 |
| Knowledge | SQLite | Haystack/LlamaIndex/pgvector | 召回评估、冲突/过期、embedding 隐私 |
| Model | Deterministic Fixture | 受控 Provider/本地模型 | 数据使用、成本、版本、超时、降级 |
| Storage | SQLite | Postgres/Object Store | 迁移、隔离、加密、备份 |
| Approval | LangGraph synthetic interrupt | 内部审批台/Webhook | 身份、权限、SLA、审计、撤销 |
| Trace | JSONL | OpenTelemetry | 脱敏、采样、保留、backend 可替换 |

## 5. 分阶段路线

### Phase 0：当前 `draft_only`

已实现纯合成沙箱和接口，等待人工审查项目组合/许可证。没有真实数据、账号、模型或发送。

### Phase 1：授权知识与人工草稿

先选一个已确认产品/市场；建立私有知识供料、版本和人工评测集；仍无真实发送。验收是来源回读、冲突/过期/缺失阻断，而不是模型“看起来不错”。

### Phase 2：真实只读渠道与 CRM 草稿队列

对单一授权平台做只读 Adapter/导出导入；人工在内部队列审草稿。不得登录自动化或 DOM 提交，先验证身份、字段、opt-out 和数据治理。

### Phase 3：`supervised`

每条动作显式批准，平台 API/授权后台优先，DOM 只作可审计 fallback。加入 idempotency、回执、停止开关、速率、事故回滚和人工值守。

### Phase 4：`bounded_autonomy`

仅允许低风险、固定模板、充分事实、明确渠道条款、可撤销/可追踪动作。价格、MOQ、合同、低 GI/健康、投诉等永不自动放行。

## 6. 完成与升级闸门

每阶段分别验收：技术测试、人工复核、合规批准、业务决定、外部平台回执、Git 同步。任一项不能替代其他项。平台能运行不代表平台允许；代码存在不代表客户沟通系统已上线。

## 7. 待用户决定

项目组合和许可证、正式产品/市场/买家类型、真实知识来源、客户数据保存、平台/账号、模型/API、CRM、审批人、supervised 和 bounded_autonomy。未决定前保持 `draft_only`。

# 知识库与资料召回契约

## 1. 知识域

未来至少分开：产品事实、检测/认证、合规/禁止表述、价格/MOQ/交期/付款状态、市场/渠道、已批准 Offer、FAQ、已批准话术、禁止承诺、客户历史、当前有效项目决定。不同域不得用一条“综合摘要”互相覆盖。

本轮只有 `sandbox_only` 合成记录：产品测试说明、价格需人工、两条互相冲突的交期。它们不对应真实大米、客户或国家。

## 2. 单条知识最小字段

| 字段 | 含义 | 缺失策略 |
|---|---|---|
| `knowledge_id` | 稳定标识 | 阻断入库 |
| `domain` | 知识域 | 阻断入库 |
| `statement` | 受控原文/事实片段 | 阻断入库 |
| `source_url` | 原始来源 | 阻断入库 |
| `source_date` | 来源日期 | 阻断入库 |
| `scope` | 市场/产品/沙箱适用范围 | 阻断入库 |
| `status` | active/superseded/expired/pending | 非 active 不召回 |
| `confidence` | 证据置信度，不是模型自信 | 缺失阻断 |
| `conflict_group` | 互斥事实分组 | 同组不同 statement → CONFLICT |
| `keywords` | 本地检索词 | 缺失阻断 |

## 3. 召回结果

`retrieve_knowledge(query, scope)` 只返回：

- `FOUND`：至少一条 active、同 scope、无冲突记录；可以进入草稿和政策闸门。
- `MISSING`：无匹配；必须 `BLOCK_REPLY`，不得补写常识。
- `CONFLICT`：同冲突组出现不同 statement；必须 `ESCALATE_HUMAN`，保留全部证据。

每个 item 保留 `source_url/source_date/scope/status/confidence`。未来增加关键原文定位、文档版本、过期时间、授权级别和数据保留期时，必须先升级 Schema。

## 4. 分块、索引、重排和过期

- 当前：结构化短记录，不分块；token 匹配；按 `source_date` 排序；不使用 embedding。
- 触发向量检索：受控文档明显增多、关键词召回基线经过人工标注后仍不达标，并且已确定可用 embedding 与隐私边界。
- 未来分块：保留 `document_id/chunk_id/char_range/hash`，不得丢失原文定位。
- 未来重排：重排器只能改变顺序，不能改变 `status/scope/conflict`。
- 过期：超过知识域 TTL 或被新版本替代的记录不得进入草稿；冲突解析必须留下 supersession 记录。

## 5. 供料、权限与数据治理

- 业务事实顺序：`dami current` 原文件 → 授权私有来源 → 外部权威原始来源 → 检索导航。
- 工具仓库不复制检测/认证/合同/报价或客户资料；真实知识索引必须位于受控私有数据层。
- 读取真实客户历史、保存个人信息、接入对象存储或向量数据库，均需单独人工确认。
- 任何真实低 GI、营养、健康或合规信息都必须由当前原始证据和人工权限决定。

## 6. 评估基线

未来 RAG 评估至少包含：来源准确率、scope 过滤正确率、冲突召回率、过期阻断率、缺资料拒答率、引用可回读率。Ragas/DeepEval 只能在人工标注集存在后加入，不能用自动分数替代合规或业务验收。

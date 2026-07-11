# Research Source-to-Action 与单主变量实验

状态：`active`
适用机制：M22、M23

## Source-to-Action 记录

每条拟影响业务动作的研究记录必须包含：

```text
source_id
source_url_or_path
publisher_or_issuer
published_at
accessed_at
country_or_region
claim
original_evidence_readback
applicability
limitations
freshness_or_review_due
confidence
candidate_business_impact
human_gate
allowed_next_action
forbidden_next_action
```

字段缺失、来源无法回读、只有搜索片段/摘要/AI 总结或适用性不明时，只能形成研究线索，不得进入正式业务执行。

## 转换流程

`搜索或外部研究 → 原始来源回读 → 证据记录 → 事实与推论分离 → 候选判断 → 用户决策 → Codex 执行单 → 结果回写`

研究结果不会自行成为业务决定。涉及合规、承诺、资金、正式触达或不可逆动作时，即使来源充分也必须经过相应人工闸门。

## 单主变量实验

渠道、报价、内容、客户开发、商业路径对比和 Offer 验证等实验，每轮只能指定一个主要变化因素，并记录：

```text
primary_variable
hypothesis
baseline
fixed_variables
sample_scope
duration_or_stop_rule
success_metric
failure_metric
risk_limit
human_gate
result
decision
```

- 不迁移其他项目的数值阈值；指标和停止线必须基于本项目证据与授权设定。
- 无法控制多个关键变化时，结果只能标记为探索性，不得作单变量因果结论。
- `result` 记录观察，`decision` 记录人工或正式决策；二者不得混写。
- 实验结束必须回写失败、异常和未测试项，而非只保存成功结果。

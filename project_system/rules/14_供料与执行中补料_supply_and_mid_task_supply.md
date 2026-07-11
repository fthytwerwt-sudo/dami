# 供料与执行中补料（supply and mid-task supply）

状态：`active`
适用机制：M16、M22
适用习惯：H12-H14

## 来源裁决

顺序是：当前正式仓库原文件 → 经授权私有来源 → 外部权威原始来源 → 搜索/AI 摘要导航 → 条件第二意见。来源冲突、低置信度、高风险、用户明确要求时可触发只读第二意见；不绑定固定供应商，第二意见不能替代原文件。

每次记录 `retrieval_manifest`、`source_readback_status`、`source_conflicts`、`external_research_needed`、`second_opinion_trigger`。检索结果、聊天记忆、静态 GPT 包或摘要没有原文件回读时只能是线索。

## pre_task_supply_pack 与 mid_task_supply_pack

执行前供料包至少包含：`task_goal`、`current_state`、`must_read_sources`、`exact_relevant_snippets`、`constraints`、`conflicts`、`missing_information`、`decision_authority`、`allowed_actions`、`forbidden_actions`、`next_input_for_codex`。每个来源要有 `source_path`、`readback_status` 与关键原文片段。

子任务缺上下文、验证失败、高风险写入或冲突未解时生成执行中补料包。`continue_allowed: false` 时禁止继续写。无法形成可回读资料链时进入 `supply_repair`，而不是猜测。

## 安全

不读取、打印或提交 `.env`、secret 或 key；不调用付费 API；高风险能力先 dry-run、只读探测或 Fixture。技术可运行不等于业务可用。

# LangGraph 流程蓝图

## 1. 采用判断

LangGraph 不是默认平台，而是本轮明确要求验证的 OSS 状态图基线。它提供 StateGraph、条件边、interrupt、checkpoint 和 resume；本仓库只使用本地库与 SQLite saver，不使用 LangGraph Platform。官方持久化文档要求 `thread_id`，并说明 checkpointer 支持 human-in-the-loop、恢复和 fault tolerance：[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)。

与 Temporal/Prefect/Dagster 比较后，当前每客户小图、人工中断和单机 checkpoint 更适合 LangGraph；若未来出现跨日高并发、定时器、SLA 和多 worker，再重新评估 Temporal。

## 2. State

`ConversationState`：`thread_id`、`message`、`knowledge_scope`、`form_url`、`runtime_mode`、`knowledge`、`draft`、`policy`、`approval`、`dom_action`、`stage`、`send_status`。

未来扩展：客户/知识/Prompt/模型/政策版本，调用次数/费用，idempotency key，审批人，失败分类和终止条件。扩展前必须同步 JSON Schema 和迁移策略。

## 3. Node / Edge / Conditional Edge

```text
START
  → retrieve
  → draft
  → policy
      ├─ MISSING/CONFLICT → blocked → END
      └─ FOUND → approval interrupt
                     ├─ rejected → END
                     └─ approved → dom_fill → BLOCK_SEND → END
```

- `retrieve`：返回 FOUND/MISSING/CONFLICT 和来源。
- `draft`：仅 FOUND 可生成；模型未来也只能产候选。
- `policy`：确定性规则；不能被模型覆盖。
- `approval`：先保存 WAITING_APPROVAL，再调用 `interrupt()`。
- `dom_fill`：label locator 写入 localhost；调用 Fake submit 得到 BLOCK_SEND。
- `blocked/rejected`：保存可回读终止状态。

## 4. Checkpoint / Resume / Stop

- 每次 invoke 使用 `configurable.thread_id`；无 thread_id 不运行。
- LangGraph SQLite saver 保存图状态；`SQLiteRuntimeStore` 另存业务可读摘要和事件。
- 恢复使用同一 thread_id 与 `Command(resume={"approved": true})`。
- `stop_run` 写入 `STOPPED/BLOCKED`，不删除历史；用户可审计原因。
- 同一次沙箱已验证关闭 checkpointer 后重新打开并继续。

## 5. Retry 和幂等

本轮没有自动 retry：localhost 失败直接报错，避免把技术重试写成业务授权。未来只有幂等的读取节点可指数退避；审批、DOM 写入和发送类动作必须有 idempotency key、最大一次语义和回执确认。

失败节点保存 `failure_class/node/attempt/retryable/last_error_at`。验证码、登录、平台条款、政策阻断和权限不足永远 `retryable=false`。

## 6. Long-term Memory

当前无长期客户记忆。未来分开：会话 checkpoint（短期）、客户事实/决定（长期结构化存储）、原始沟通（受控审计存储）、向量检索索引（可重建派生物）。向量索引不得成为事实源，也不得保存超出授权的数据。

## 7. 人工审查点

当前所有草稿都 interrupt；敏感内容在 interrupt 前已标 `REQUIRE_REVIEW`。进入真实 supervised 前还需审批身份、权限范围、草稿 diff、来源回读、过期提示、拒绝理由和超时路由。

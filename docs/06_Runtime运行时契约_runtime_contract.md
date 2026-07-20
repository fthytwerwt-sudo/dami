# Runtime、状态和可观测性契约

## 1. 运行记录

每个客户会话未来必须记录：会话编号、当前阶段、知识库版本、工具调用、待审批动作、发送状态、失败位置、暂停/继续、防重复发送、费用/调用次数、模型版本、Prompt/政策/数据版本、终止条件。

本轮实际记录：`thread_id/stage/send_status` 业务 checkpoint，节点事件 SQLite，LangGraph checkpoint，以及 JSONL trace。没有 Token、模型费用、客户 ID 或真实消息。

## 2. 表和文件职责

| 存储 | 职责 | 是否事实源 | 恢复方式 |
|---|---|---|---|
| `runtime_checkpoints` | 人可读最近状态 | 运行状态摘要 | `resume_run(thread_id)` |
| LangGraph saver tables | 图内部 checkpoint/写集 | 否，运行引擎状态 | 同 thread_id `Command(resume=...)` |
| `runtime_events` | 节点事件审计 | 审计证据 | SQL 按 thread_id 回读 |
| `trace.jsonl` | 可导出的轻量 Trace | 否 | JSONL 逐行导入 OTel/分析 |
| Knowledge SQLite | 合成知识快照 | 本轮合成事实层 | 可从 fixture 重建 |

业务摘要和 LangGraph 表不得互相伪装；两者不一致时进入 `checkpoint_failure`，不能猜测继续。

## 3. 幂等、防重复和发送状态

- 当前没有发送能力，`send_status` 只能 `NOT_SENT/BLOCKED/UNKNOWN`。
- 未来每次不可逆动作使用 `tenant/channel/customer/thread/message/draft_hash` 组成 idempotency key。
- 状态机必须分开：`DRAFT_CREATED`、`APPROVED`、`FILLED_PENDING_SUBMIT`、`SUBMIT_REQUESTED`、`PLATFORM_ACKNOWLEDGED`、`BUSINESS_ACCEPTED`。
- 超时或回执丢失进入 `UNKNOWN` 并人工核对，不可自动重发。

## 4. Trace 和日志

节点事件至少含 `thread_id/node/recorded_at/details`。未来增加 span ID、parent span、耗时、工具版本、输入/输出 hash、token/费用、失败分类和人工审批记录，但不记录 secret 或不必要个人信息。

升级优先 `OpenTelemetry`：业务节点继续调用 TraceAdapter，再映射为 OTLP；是否部署 collector/backend 是独立决定。Langfuse/Phoenix 可作 UI 候选，不应成为执行前提。

## 5. Pause / Resume / Stop / Termination

- Pause：LangGraph interrupt 后 `WAITING_APPROVAL`。
- Resume：同 thread_id + 明确人工 payload。
- Stop：保存 `STOPPED/BLOCKED/stop_reason`，不删除历史。
- Termination：政策阻断、人工拒绝、提交前阻断、最大节点/尝试次数、费用上限、客户 opt-out、平台权限撤销、数据版本过期。

## 6. Durable Execution 升级阈值

满足以下多项才评估 Temporal：跨天定时器、多 worker、高并发、明确 SLA、活动补偿、版本迁移、单机故障不可接受。Prefect/Dagster 更适合数据/资产任务；n8n/Activepieces/Windmill 只有在连接器价值大于 secret/平台运维成本时再看。

## 7. 数据保留与隐私

当前 `runtime_data/` 被 Git 忽略，可删除重建。真实运行前必须定义数据最小化、地区/客户隔离、加密、访问控制、保留期、删除请求、备份恢复、日志脱敏和 incident runbook。

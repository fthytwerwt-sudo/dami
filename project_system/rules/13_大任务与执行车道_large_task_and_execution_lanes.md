# 大任务与执行车道（large task and execution lanes）

状态：`active`
适用习惯：H10-H11

## large_task_gate

以下任一触发大任务：影响 3 个以上正式文件；规则/脚本/状态/日志中至少 3 类同时变化；需要大量只读审计；多阶段、多角色或多状态；用户明确要求完整执行/多 Agent/并发；单执行器容易漏项。

触发后必须输出 `large_task_gate.triggered`、理由、`lane_recommendation`、`write_owner` 和 `integration_owner`。大任务不自动要求多 Agent。

## lane 规则

可选：`serial_only`、`read_parallel`、`explore_plus_integrate`、`true_multi_task_parallel`。只有对象、目标、验收、范围、依赖和 blocker 已锁定，且写入不重叠时才可并行。读取冲突、判断风险或写入重叠时降级串行。

`explore_plus_integrate` 的 explorer 只读，唯一 integrator 拥有写权。`lane_parallel_router.py` 检出多个写入 owner 时返回 `blocked_multi_lane_write_conflict`。

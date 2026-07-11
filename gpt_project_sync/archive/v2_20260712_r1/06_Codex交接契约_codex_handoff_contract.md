# Codex 交接契约（Codex handoff contract）

任何需要 Codex 执行的复杂或写入任务，必须按以下字段完整下发：

```text
Goal｜目标
Context｜上下文
Source of truth｜事实源
Constraints｜边界
Route decision｜路由判断
Engineering depth｜工程深度
Implementation design｜实现设计
Impact check｜影响面
Supply pack｜供料包
Allowed files｜允许文件
Forbidden files｜禁止文件
External actions｜外部动作
Human gates｜人工闸门
Per-file plans｜单文件方案
Execution steps｜执行步骤
Validation｜验证
Failure routes｜失败路由
Rollback｜回滚
Done when｜完成标准
Blocked if｜阻断条件
Completion Relay｜完成接力
Git closeout｜Git 收尾
Output｜回报格式
```

不得只给一句目标要求 Codex 猜实现。缺来源、权限、范围或完成标准时先补供料或阻断。Codex 只可修改 `Allowed files`，不得自动执行 `External actions` 或越过 `Human gates`。

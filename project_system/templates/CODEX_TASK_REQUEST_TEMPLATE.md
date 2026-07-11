# Codex 任务交接模板（task request template）

```text
Goal｜目标:
Context｜上下文:
Source of truth｜事实源:
Constraints｜边界:

Route decision｜路由判断:
  task_type:
  responsibility_layer:
  must_read_files + read_status:
  allowed_changes:
  forbidden_changes:
  execution_permission:

Engineering worth｜值不值得工程化:
Engineering depth｜工程深度:
Large task gate｜大任务闸门:
Lane recommendation｜执行车道:
write_owner:

Implementation design｜实现设计:
Impact check｜影响面:
Supply pack｜供料包:
  retrieval_manifest:
  source_readback_status:
  source_conflicts:
  second_opinion_trigger:

Allowed files｜允许文件:
Forbidden files｜禁止文件:
External actions｜外部动作:
Human gates｜人工闸门:
Per-file plans｜单文件方案:
Execution steps｜执行步骤:
Validation｜验证:
Failure routes｜失败路由:
Rollback｜回滚:
Done when｜完成标准:
Blocked if｜阻断条件:
Completion Relay｜完成接力:
Git closeout｜Git 收尾:
Output｜回报格式:
```

任务写入前由 `task_request_validator.py`、`per_file_plan_validator.py` 和 `project_task_preflight.py` 进行 dry-run 检查。该模板不授予未列出的文件、外部动作或业务决定权限。

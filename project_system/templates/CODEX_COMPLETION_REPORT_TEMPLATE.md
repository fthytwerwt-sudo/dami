# Codex 完成回报模板（completion report template）

```text
task_result.status:
goal_result:
source_of_truth_used:
route_decision:
engineering_depth:
large_task_gate:
lane_recommendation:

deliverables:
files_read:
files_created:
files_modified:
files_not_touched:
local_only_files:
external_actions:
human_review_required:

Tested:
Not-tested:
validation_results:
status_promotions:
status_not_promoted:
blocked_items:
remaining_work:
assumptions:
deviations:

git_closeout:
  staged_paths:
  local_head:
  origin_main:
  ls_remote_main:
  remote_readback:

GPT Project sync:
  package_generated:
  ui_uploaded:

下一个目标:
```

任何低层机器验证不得替代人工、合规、业务、外部动作、Git 同步或 GPT Project UI 上传。`project_task_closeout.py` 在完成声明前检查 inventory、状态、剩余工作和 Git 收尾。

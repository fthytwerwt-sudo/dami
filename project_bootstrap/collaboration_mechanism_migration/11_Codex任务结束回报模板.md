# Codex 任务结束回报模板

```yaml
task_result.status:
goal_result:
source_of_truth_used:
files_read:
files_created:
files_modified:
files_not_touched:
external_actions:
impact_check:
tests_run:
tests_passed:
tests_failed:
not_tested:
blocked_items:
assumptions:
deviations:
status_promotions:
status_not_promoted:
git_status:
source_commit:
result_commit:
next_safe_step:
human_review_required:
```

## 填写规则

- `task_result.status` 必须使用具体状态，如 `ready_for_user_review`、`blocked_fact_conflict`、`partial_completed_authorized`；不得笼统写“完成”。
- `goal_result` 逐条对应 Done when。
- `external_actions` 即使为空也写 `none`。
- `tests_failed` 为非空时不得声称通过；应继续修复或转为具体 blocked。
- `not_tested` 不能省略。
- `status_promotions` 必须列出证据；`status_not_promoted` 明确说明未提升到人工、业务、合规或同步状态。
- 目标目录不是 Git 仓库时，`git_status/result_commit` 写 `not_applicable`，不得伪造提交。

# 完成真实性与 Completion Relay

状态：`active`
适用机制：M11、M12、M13

## 完成层级不得混写

`technical_validation`、`evidence_validation`、`human_review`、`business_decision`、`external_action`、`git_sync`、`gpt_project_sync` 是独立状态。文件生成不等于机制激活；机器通过不等于人工、合规或商业通过；本地提交不等于远端同步；同步包生成不等于 GPT Project 已上传。

## 每轮完成报告字段

```text
goal_result
deliverables
source_of_truth_used
files_read
files_created
files_modified
files_not_touched
external_actions
tests_run
tests_passed
tests_failed
not_tested
blocked_items
assumptions
deviations
status_promotions
status_not_promoted
remaining_work
next_safe_step
human_review_required
git_status
local_head
remote_main
```

未知或不适用字段也要明确标记，不得静默省略关键缺口。

## Completion Relay 检查

结束前逐项检查：

1. 用户要求的交付是否齐全且位于允许范围。
2. 是否存在未报告的剩余工作、失败、假设或偏差。
3. 是否把低层验证错误提升为更高层完成。
4. 是否需要回写当前事实、决定或任务状态。
5. 是否需要人工审核或专业确认。
6. 正式仓库变更是否需要并已获 Git 收尾授权。
7. 是否满足下一状态全部进入条件。

只有全部适用检查通过，才可使用 `completed_verified`。等待人工判断时使用 `completed_pending_human_review`；部分目标成立时使用 `partial_completed`；关键条件不满足时使用具体 `blocked_*`。

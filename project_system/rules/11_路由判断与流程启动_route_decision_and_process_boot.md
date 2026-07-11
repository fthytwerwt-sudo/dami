# 路由判断与流程启动（route decision and process boot）

状态：`active`
适用习惯：H01-H04

## route_decision 硬闸门

任何仓库写入、commit 或 push 前必须有通过的 `route_decision`。它至少输出：

```text
task_type
responsibility_layer
must_read_files
read_status
allowed_changes
forbidden_changes
engineering_worth_question
external_actions
human_gates
execution_permission
```

`read_status` 只能为 `read_ok`、`missing`、`unreadable`、`not_applicable`。仓库可见性必须由 `project_system/current/REPOSITORY_SECURITY_STATUS.md` 读取；任务输入中的 `repository_visibility` 只可用于一致性校验。正式状态缺失或不可解析时返回 `blocked_repository_visibility_unknown`，与任务输入冲突时返回 `blocked_repository_visibility_conflict`。必读来源 `missing` 或 `unreadable`、允许范围不清、外部动作未授权、Public 仓库商业敏感资料、任何可见性下的密钥/个人信息或 Private 未授权敏感资料、或责任层不明时，禁止写入并进入相应失败路由。

## process_boot_report

复杂任务在路由后建立 `process_boot_report`，回答：要什么、到哪了、吃什么资料、错了去哪、留没留记录。prompt 是 `prompt_delta_only`，不得替代仓库正式流程和原文件。

`project_task_preflight.py` 串联 route decision → engineering depth → large task gate → lane decision → must-read validation → scope validation → supply check → human gate check。默认 dry-run；报告通过不等于业务、合规或外部批准。

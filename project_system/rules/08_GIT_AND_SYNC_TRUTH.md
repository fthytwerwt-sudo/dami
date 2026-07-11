# Git 决策、验证与同步真实性

状态：`active`
适用机制：M14、M15、M27、M28

## 何时执行 Git 闭环

机制、事实、状态、决定和其他正式仓库变更，只有在任务明确授权后才执行：影响面检查 → 精确暂存 → 提交 → 普通推送 → 远端回读。只读研究、未批准草稿或本地私有资料不强制提交，也不得夹带提交。

禁止宽范围暂存、自动纳入无关改动、强制推送或改写历史。提交前后必须检查允许路径、秘密、敏感数据、格式和工作树归属。

## Git 提交决策与验证说明字段

提交说明按任务风险选用以下人类可读字段：

```text
Goal
Constraint
Rejected
Confidence
Scope-risk
Directive
Tested
Not-tested
```

第一行解释为何变更；`Tested` 与 `Not-tested` 必须如实分开。字段用于记录决定与验证，不替代差异审查或测试证据。

## 同步完成判据

只有以下证据同时成立，才能报告 `git_sync: completed_verified`：

- 提交范围只含获准文件。
- 本地 `HEAD` 与远端跟踪分支一致。
- 远端引用查询返回同一 SHA。
- 远端树与允许范围一致，关键文件可回读。

任一失败使用 `blocked_remote_readback_failed` 或更具体阻断，不得把本地 commit、push 命令成功或缓存视图当成远端完成。

## GPT Project 同步真实性

- 仓库中的同步包生成状态与 ChatGPT Project UI 上传状态分开记录。
- 生成、归档或提交同步包，只能证明包存在和 Git 状态；不能声称 UI 已上传或已生效。
- GPT Project 中的静态规则不能覆盖仓库正式当前事实；动态快照必须注明来源 commit、规范来源文件、生成时间和快照状态。
- 用户完成上传并确认前，状态只能是 `gpt_project_sync_package_generated_pending_user_upload`。
- `latest` 是当前分发入口；版本归档必须保留，不以 `latest` 覆盖历史。

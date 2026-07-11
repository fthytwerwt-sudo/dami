# GitHub 首次推送审计报告

## 基本信息

- 项目根目录：`/Users/fan/Documents/底 IG 大米外贸`
- 目标远端：`https://github.com/fthytwerwt-sudo/dami.git`
- 远端仓库：`fthytwerwt-sudo/dami`
- 仓库可见性：`Public`
- 目标分支：`main`
- 允许上传目录：`project_bootstrap/collaboration_mechanism_migration/`
- 上传前既有文件数量：`21`
- 加入本报告后的预期提交文件数量：`22`

## 上传前影响面

- 项目根目录此前是否为 Git 仓库：`false`
- 是否被父级 Git 仓库包含：`false`
- Git 初始化状态：`initialized_now`
- 当前分支：`main`
- 远端当前状态：`empty_no_refs`
- 当前身份 push 权限：`confirmed`
- 允许目录外本地文件：存在，但全部禁止暂存和提交。

## Public 仓库安全审计

- 凭据值扫描：`passed`
- 已知 Token 前缀扫描：`passed`
- 私钥扫描：`passed`
- 邮箱扫描：`passed`
- 电话号码扫描：`passed`
- 身份证件与支付卡模式扫描：`passed`
- 私有客户/供应商/合同/报价带值字段扫描：`passed`
- 关键词上下文复核：命中内容均为规则、禁止事项或模板字段，不是实际敏感记录。
- 软链接：`none`
- 空文件：`none`
- 超过 5 MB 文件：`none`
- 二进制、ZIP、媒体、图片、数据库或临时文件：`none`
- Public 仓库安全结论：`passed_for_initial_push`

## Git 提交与推送

- pre-commit status：`blocked_git_diff_check_failed_requires_content_change`
- staged scope：`22 files; all under project_bootstrap/collaboration_mechanism_migration/`
- `git diff --cached --check`：`failed`
- initial commit SHA：`not_created`
- initial push：`not_attempted`
- initial remote readback：`not_applicable_remote_still_empty`
- evidence commit SHA：`not_created`
- final push：`not_attempted`
- final local HEAD：`unborn_main_no_commit`
- final origin/main：`not_created`
- final ls-remote main：`no_refs`
- final remote tree：`empty`

## 阻断详情

- `01_source_evidence_map.md`：1 处 trailing whitespace。
- `03_新项目协作机制总览.md`、`04_ChatGPT_Project项目指令_候选版.md`、`05_AGENTS候选版_仅供评审.md`、`06_当前正式事实模板.md`、`07_任务路由与状态机.md`、`09_事实源与冲突裁决规则.md`、`10_Codex任务执行单模板.md`、`11_Codex任务结束回报模板.md`、`12_人工确认与AI自动执行边界.md`、`13_禁止迁移清单.md`、`14_旧机制到新机制差异报告.md`、`15_启动后第一阶段建议.md`：各有 1 个 EOF 多余空行。
- 附件要求候选内容不得为推送而修改，因此本轮没有自动清理这些格式问题。

## Tested

- 项目根和父级 Git 边界。
- 远端仓库、Public 可见性、默认分支、push 权限与空仓库 refs。
- 允许目录文件范围、类型、大小、空文件和软链接。
- JSON 解析。
- 凭据、个人数据和商业敏感内容模式扫描及关键词上下文复核。

## Not-tested

- 推送后的远端 HEAD 与远端树，等待首次 push 后回读。
- 用户对候选机制的审核。
- ChatGPT Project 上传或同步。
- AGENTS 候选版激活。
- 正式事实批准。
- 任何真实跨境业务执行。

## 状态未推进项

- 候选机制未激活。
- ChatGPT Project 未声明已同步。
- AGENTS 候选版未正式启用。
- 正式事实未批准。
- 项目未声明可全面执行业务。
- 本轮未创建 commit，未向远端推送任何内容。

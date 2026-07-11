# v2 运行内核窄修复验证报告

验证范围：运行内核窄修复的已验证来源提交与其 GPT 静态快照构建结果。

## 已验证来源提交

- `source_commit`: `cdb9bae4b679f2c49aebc9a3bdceb6eae0be0bb4`
- 本地 `HEAD`、`origin/main` 与 `git ls-remote origin refs/heads/main` 在该来源提交推送后完全一致。
- 远端已回读：`scripts/project_system/project_task_preflight.py`、`scripts/project_system/_common.py`、`scripts/project_system/project_task_closeout.py`、只读分流 Fixture 与 Private 非敏感 Git 收尾 Fixture。

## 运行内核与契约

- `determine_write_required()` 只按写入任务类型、`repository_write_requested`、`will_modify_files` 和单文件方案中的实际路径判断写入需求。
- 纯读取/审核/事实缺口盘点可使用 `serial_only` 或 `read_parallel`，不会被预检强制要求 write lane、commit 或 push。
- 写入任务仍需唯一 write lane，且 `write_owner` 与 `integration_owner` 一致。
- `resolve_repository_security_status()` 只读解析 `project_system/current/REPOSITORY_SECURITY_STATUS.md`；任务输入可见性仅做一致性对读。
- Public 非敏感、Public 敏感、Private 非敏感、Private 未授权敏感、Unknown、冲突、多个 write owner、owner 不一致与只读收尾均有 Fixture 覆盖。

## 验证结果

- Python 编译、全部项目 CLI `--help`、相关 JSON Schema/Fixture 解析、单文件方案 Validator 与 `git diff --check`：通过。
- Fixture runner：`29/29` 通过。
- staged diff secret/sensitive scan：通过；扫描器对其自身正则文本的 Windows 路径误报，以及 SHA-256 摘要内连续数字的电话号码误报，均已用独立回归断言消除；真实 Windows 盘符绝对路径与电话号码仍会命中。
- live Git closeout Validator 以 `core.quotepath=false` 读取 Git 路径，中文文件名与精确单文件方案可稳定对读。
- M01—M28 与 H01—H20 注册表未修改，计数保持 `28` 与 `20`；`AGENTS.md` 和单工作区规则未改。
- GitHub 只读对读显示仓库为 Public；没有修改仓库可见性。

## GPT Project 静态包

- 新版本：`v2_20260712_r1`，使用既有 `gpt_sync_package_builder.py` 生成。
- `source_commit` 为上述已验证来源提交；latest 与新 archive 的 9 个文件逐字节一致，manifest 所列全部 SHA-256 已逐项复算通过。
- 快照包含 `cross_project_collaboration_system_v2_active`、`runtime_narrow_repairs_verified` 和 `git_sync_verified_for_source_commit`。
- 快照保持 `gpt_project_synced: false`、`ui_uploaded: false` 与 `business_execution_started: false`。
- 不包含旧的 `pending_precise_stage_and_push`、仅本地工作树激活表述、本机绝对路径、密钥或业务敏感资料。
- `archive/v1_20260711` 与 `archive/v2_20260712` 未修改。

## 边界

本报告证明已验证运行内核来源提交及其静态包构建结果；它不把静态包生成写成 ChatGPT Project UI 上传/同步，也不提升任何市场、渠道、合规、客户、价格或外部业务状态。

# 跨项目操作习惯注册表（cross-project operating habits）v2

status: `active`
total_registered: `20`

本注册表补全机制注册表未承载的日常默认动作。每项均有正式规则、运行内核或验证位置；不包含领域专属视频、固定供应商、旧路径或业务事实。

| ID | 操作习惯 | Status | 正式落点 | 运行/验证入口 |
| --- | --- | --- | --- | --- |
| H01 | 先路由再写入 | `ACTIVE` | Rule 11 | `route_decision_builder.py` |
| H02 | 任务类型与责任层级 | `ACTIVE` | Rule 10/11 | `task_request_validator.py` |
| H03 | 本轮必读清单 | `ACTIVE` | Rule 11 | `task_request_validator.py` |
| H04 | 允许和禁止修改范围 | `ACTIVE` | Rule 11 | `task_request_validator.py` |
| H05 | 值不值得工程化 | `ACTIVE` | Rule 12 | `engineering_depth_router.py` |
| H06 | L0-L3 工程深度 | `ACTIVE` | Rule 12 | `engineering_depth_router.py` |
| H07 | AI 工程线 13 层 | `ACTIVE` | Rule 12 | `engineering_depth_router.py` |
| H08 | 工程线五问法 | `ACTIVE` | Rule 12 | `process_boot_builder.py` |
| H09 | 单文件细节方案 | `ACTIVE` | Rule 15 | `per_file_plan_validator.py` |
| H10 | 大任务闸门 | `ACTIVE` | Rule 13 | `large_task_gate.py` |
| H11 | 执行车道与并发 | `ACTIVE` | Rule 13 | `lane_parallel_router.py` |
| H12 | 资料供给裁决 | `ACTIVE` | Rule 14 | `source_supply_pack_builder.py` |
| H13 | 执行前供料与执行中补料 | `ACTIVE` | Rule 14 | `source_supply_pack_builder.py` / `mid_task_supply_builder.py` |
| H14 | 秘密与无副作用检查 | `ACTIVE` | Rule 14/05 | dry-run、Fixture、secret scan |
| H15 | 完成接力 | `ACTIVE` | Rule 16 | `completion_relay_validator.py` |
| H16 | 失败路由 | `ACTIVE` | Rule 16 | `failure_route_resolver.py` |
| H17 | 强制 Git 小闭环 | `ACTIVE` | Rule 08 | `git_closeout_validator.py` |
| H18 | 诚实状态与最终交接 | `ACTIVE` | Rule 16 | `project_task_closeout.py` |
| H19 | 单工作区与路径治理 | `ACTIVE` | Rule 18 | preflight 路径检查 |
| H20 | 中文理解和英文原词对照 | `ACTIVE` | Rule 17 | 文档、代码和包审查 |

## 证据与边界

源习惯证据来自学习仓库在 `ebc420f7bf42bd8c6c1d9ed435fd889177aa452c` 的可回读通用入口、状态路由、工程线、执行车道、供料、完成接力、失败路由和 Git 收尾规则。该仓库 current `main` 与该基线一致，未发现基线后新增规则。来源中的领域专属流程、固定技术依赖、旧状态和路径均已排除。

每项习惯仅在任务触发时运行。`ACTIVE` 表示已落入正式规则和可执行/可验证路径，不表示任何业务、合规、人工或外部动作已获批准。

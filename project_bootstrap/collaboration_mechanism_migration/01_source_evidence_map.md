# 源证据地图

主仓库：`fthytwerwt-sudo/-`
主分支/提交：`main@ebc420f7bf42bd8c6c1d9ed435fd889177aa452c`

所有主证据均为 `source_verified`；次要仓库只提供 `cross_repo_verified` 支持，不覆盖主证据。

## 当前可访问仓库清单

`lanxinse--`、`lanxinshe-`、`-`、`video_capability_lab`、`ai-live-frontend-mvp`、`-111`、`obsidian-vault`、`first-station`。根据机制密度、相关性和重复度，最终只选择下文 3 个次要仓库交叉验证。

| ID | 机制 | 主证据定位 | 领域性 | 候选 |
|---|---|---|---|---|
| M01 | ChatGPT 判断与 Codex 执行分工 | `AGENTS.md:101-107` | 通用 | 是 |
| M02 | 动态事实与静态资料分离 | `AGENTS.md:72-79` | 通用 | 是 |
| M03 | 事实源权威与冲突裁决 | `GPT数据源/11...:109-120` | 通用 | 是 |
| M04 | 项目状态动作路由 | `GPT数据源/01...:178-184` | 通用 | 是 |
| M05 | 六层需求对齐 | `GPT数据源/11...:344-380` | 通用 | 是 |
| M06 | 模糊目标澄清闸门 | `GPT数据源/11...:296-342` | 通用 | 是 |
| M07-M09 | 实现设计、能力边界、替代损失 | `commit 8a1350b` | 通用 | 是 |
| M10 | 启动报告与影响面 | `AGENTS.md:330-352` | 通用 | 是 |
| M11 | Completion Relay Gate | `GPT数据源/01...:186-200` | 通用 | 是 |
| M12 | 完成真实性预检 | `GPT数据源/11...:37-45` | 例子专属、机制通用 | 是 |
| M13 | 四态完成推理 | `GPT数据源/11...:1496-1536` | 通用 | 是 |
| M14 | Git 决策 trailers | `commit ebc420f` | 通用 | 是 |
| M15 | GPT Project 同步真实性 | `codex_log/current_local_artifact_paths.md:115-192` | 通用 | 是 |
| M16 | 检索回读原文件 | `codex_source/24...:16-130` | 通用 | 是 |
| M17 | 安全 dry-run | `scripts/vector_sync/README.md:1-28` | 通用 | 是 |
| M18 | 人工/AI 决策矩阵 | `GPT数据源/16...:129-162` | 通用 | 是 |
| M19-M21 | 工程深度、预算、协作有效性 | `GPT数据源/16...:53-266` | 通用 | 是 |
| M22 | 参考到执行契约 | `GPT数据源/12...:23-100,351-399` | 需领域改写 | 是 |
| M23 | 单主变量实验 | `GPT数据源/13...:728-800` | 需领域改写 | 是 |
| M24 | 视频/TTS/卡片流程 | `codex_source/22...:45-85` | 专属 | 否 |
| M25 | 固定 RAG/外部 AI 技术 | `AGENTS.md:98-106` | 专属实现 | 否 |
| M26 | 旧业务状态名称 | `AGENTS.md:251-272` | 专属 | 否 |
| M27 | Git 远端回读闭环 | `GPT数据源/01...:201-241` | 通用 | 是 |
| M28 | latest/历史日志分离 | `AGENTS.md:50-81,147-167` | 通用 | 是 |

## 次要仓库交叉验证

- `fthytwerwt-sudo/lanxinse--@bead320f...`：重复出现三层协作、事实优先级、六层需求确认、执行单和 Git 闭环。
- `fthytwerwt-sudo/video_capability_lab@010da208...`：明确“只迁机制，不迁旧事实”，并分离机器验证与人工结论。
- `fthytwerwt-sudo/-111@d1b68cc...`：重复出现执行前路由、影响面、状态分层、path-limited stage 与 remote readback。

## 证据限制

- 行号固定于上述 commit；后续仓库变化需重新取证。
- 旧项目中的领域例子只用于解释原用途，不构成新项目规则。
- Git 提交说明是决策证据，不替代对应文件内容。

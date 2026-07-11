# 机制迁移矩阵

总计 28 项：`KEEP_DIRECTLY=16`、`ADAPT=8`、`DROP=3`、`DEFER=1`。

| ID | 机制 | 裁决 | 新项目处理 | 人工确认 | 实现 |
|---|---|---|---|---|---|
| M01 | ChatGPT/Codex 分工 | KEEP_DIRECTLY | 判断、执行、批准分离 | 是 | 文档 |
| M02 | 静态规则/动态事实分离 | KEEP_DIRECTLY | 四层架构 | 是 | 文档 |
| M03 | 事实权威与冲突 | KEEP_DIRECTLY | 引入有效期、替代关系和原始证据 | 是 | 文档 |
| M04 | 状态动作路由 | ADAPT | 改为跨境验证状态 | 是 | 文档 |
| M05 | 六层需求对齐 | KEEP_DIRECTLY | 原机制保留 | 否 | 文档 |
| M06 | 模糊目标闸门 | KEEP_DIRECTLY | 方向性任务先收束 | 是 | 文档 |
| M07 | 实现设计层 | KEEP_DIRECTLY | 工具/自动化前必需 | 否 | 文档 |
| M08 | 能力探测 | KEEP_DIRECTLY | 未探测不声明 | 否 | 文档/可选探测 |
| M09 | primary/fallback/loss | KEEP_DIRECTLY | 降级必须披露损失 | 是 | 文档 |
| M10 | 启动/影响面 | ADAPT | 增加合规、客户、外发影响 | 否 | 文档 |
| M11 | 完成接力 | KEEP_DIRECTLY | 必交付与剩余工作清单 | 否 | 文档 |
| M12 | 完成真实性 | KEEP_DIRECTLY | 草稿/机器/人工/业务/同步分层 | 否 | 文档；以后可加 validator |
| M13 | 四态完成 | ADAPT | 与新状态机结合 | 否 | 文档 |
| M14 | Git trailers | KEEP_DIRECTLY | 记录决策、风险和验证 | 否 | Git 规则 |
| M15 | GPT Project 同步真实性 | KEEP_DIRECTLY | 生成、Git、UI 上传分层 | 是 | 文档 |
| M16 | 检索回读原文件 | ADAPT | 不绑定 RAG 产品 | 否 | 文档 |
| M17 | dry-run/秘密边界 | KEEP_DIRECTLY | 外部动作先无副作用检查 | 是 | 文档/按需脚本 |
| M18 | 人工/AI 权限矩阵 | ADAPT | 改为跨境合规、价格、合同、外发 | 是 | 文档 |
| M19 | L0-L3 工程深度 | DEFER | 等真实重复任务出现再启用 | 是 | 未来机制 |
| M20 | 执行预算 | KEEP_DIRECTLY | 防止启动期过度工程化 | 否 | 文档 |
| M21 | 协作有效性 | KEEP_DIRECTLY | 用减少误解/漏项验收 | 是 | 文档 |
| M22 | 参考到执行 | ADAPT | 改为研究 source-to-action | 是 | 文档 |
| M23 | 单主变量实验 | ADAPT | 不迁旧阈值，按试验重定 | 是 | 文档 |
| M24 | 视频/TTS/卡片流程 | DROP | 完全排除 | 否 | 无 |
| M25 | 固定 RAG/外部 AI 实现 | DROP | 保留技术中立 | 否 | 无 |
| M26 | 旧业务状态名 | DROP | 使用跨境状态机 | 否 | 无 |
| M27 | Git 远端闭环 | ADAPT | 仅 Git 仓库且获授权时启用 | 是 | Git 规则 |
| M28 | latest/历史分离 | KEEP_DIRECTLY | 当前指针不改写历史 | 否 | 文档 |

## 用户操作成本判断

- 低成本：默认由 ChatGPT/Codex 自动填写任务字段和验证记录。
- 中成本：只在方向、冲突、合规、外部动作或状态提升时请求用户确认。
- 高成本：L2/L3 工程线暂缓，不在 bootstrap 阶段要求用户维护 schema/trace/多节点系统。

## 新增建议边界

本轮提出的跨境状态名称、健康/合规人工闸门和事实模板字段属于 `new_recommendation`；它们由源机制推导但不是旧仓库原文，均保持候选状态等待审核。

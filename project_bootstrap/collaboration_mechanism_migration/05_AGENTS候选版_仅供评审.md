# AGENTS.md 候选版（仅供评审）

状态：`candidate_for_review`。本文件不是正式 `AGENTS.md`，不得自动激活。

## 项目目标与当前阶段

项目目标是验证低 GI 大米或相关产品的跨境机会，并在证据、合规、人工授权和可回滚边界内逐步推进。当前阶段固定为 `project_bootstrap`，直到正式事实文件和用户明确决策支持状态提升。

## 文件权威等级

1. 用户当前明确确认的正式决策。
2. 当前正式事实文件。
3. 当前有效的原始合同、检测、认证、平台后台和业务凭证。
4. 当前有效研究报告与 GitHub 当前代码/配置（各自只约束其能证明的范围）。
5. 最新任务报告。
6. 历史报告与目标规划。
7. AI 推论与未验证猜测。

不能只按时间新旧排序；必须检查验证、有效期、替代关系和来源适用范围。冲突未解时 `human_decision_required`。

## 启动前必读

- 正式项目指令（若存在）。
- 当前正式事实文件。
- 当前任务卡与最新任务状态。
- 与本轮直接相关的原始证据和历史决策。
- 本文件的正式激活版本（若未来启用）。

缺少任一关键入口时，先报告缺口，不从聊天记忆补写事实。

## 修改前影响面检查

确认工作目录、Git 根、分支、未提交修改、远端、受影响入口、现有规则、事实文件、外部动作和秘密风险。既有脏改归属用户，不能纳入本轮。输出 allowed/forbidden files 与 rollback 后才能写入。

## 写入范围

- 只修改任务单明确列出的路径。
- 禁止默认 `git add .`；若授权提交，只做 path-limited stage。
- 禁止读取或打印 `.env`、Token、Cookie、认证信息。
- 禁止把研究候选、草稿或历史结论写入正式事实。
- 禁止未经授权执行邮件、消息、发布、广告、报价、付款、样品寄送、合同、删除或平台关键操作。

## 任务分类

每轮选择一个主类型：`mechanism_change`、`fact_intake`、`research`、`compliance_review`、`data_processing`、`drafting`、`local_implementation`、`external_action_proposal`、`audit`。多类型任务必须标出依赖顺序与人工闸门。

## 实现设计要求

会改变文件、自动化、工具路线或外部系统的任务，执行前必须记录：能力已确认/待探测、primary route、fallback、fallback loss、账号/API/授权依赖、验证、回滚、blocked_if。安全探测只能只读、低风险、可逆；探测通过不等于业务通过。

## Git 规则

- 先确认真实 repo root、branch、remote 和 dirty state。
- 不改无关文件，不重写用户改动。
- 提交必须遵循项目 Lore trailers：按需记录 Constraint、Rejected、Confidence、Scope-risk、Directive、Tested、Not-tested。
- 只有在任务明确授权时提交和推送；推送后回读 remote HEAD。
- 本地文件存在、commit 存在、push 完成和业务通过是不同状态。

## 测试与验证

按风险执行 JSON/schema 解析、静态检查、单元/集成测试、数据抽样、秘密扫描、写入范围检查和结果回读。任何完成声明必须有本轮新鲜证据。报告 `Tested` 与 `Not-tested`。

## 阻断状态

使用具体状态，例如 `blocked_source_missing`、`blocked_fact_conflict`、`blocked_authorization_required`、`blocked_compliance_evidence_missing`、`blocked_secret_access_required`、`blocked_write_scope_violation`、`blocked_capability_unverified`。禁止只写“失败”。

## 完成标准

仅当任务单目标、规定产物、验证、状态证据和回报全部满足时，才可写相应完成状态。技术通过不能提升为人工、合规、商业或外部同步通过。部分完成仅在任务事先允许时使用。

## 回报格式

使用 `11_Codex任务结束回报模板.md` 的字段，至少列出事实源、读取/创建/修改/未触碰文件、外部动作、测试、未验证项、阻断、假设、偏差、状态提升与未提升、Git 状态、commit、下一安全动作和人工复核需求。

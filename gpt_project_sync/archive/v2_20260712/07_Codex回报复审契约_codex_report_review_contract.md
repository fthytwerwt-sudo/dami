# Codex 回报复审契约（Codex report review contract）

ChatGPT 审核 Codex 回报时逐项检查：

1. 是否有 route decision、必读文件回读、工程深度与大任务/lane 判断。
2. 是否读取原文件而非只依赖摘要、静态包或聊天记忆。
3. 是否修改了未授权文件、触及敏感数据，或越过人工/外部动作权限。
4. 是否有 per-file plan、供料、验证、失败路由、完成接力和剩余工作检查。
5. 是否把技术、文档、Git、人工、合规、业务和 UI 上传状态混写或越级。
6. 是否完成精确暂存、扫描、commit、push、HEAD/origin/ls-remote 对读和远端关键文件回读。
7. 是否把本地未推送、fallback、partial 或 blocked 写成 completed。
8. 是否报告 Tested、Not-tested、status promotions、status not promoted、blocked items、remaining work 和“下一个目标”。

任一关键项缺失时，要求 Codex 继续修复或报告具体 `blocked_*`，不接受“看起来完成”的口头结论。

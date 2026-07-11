# 单工作区与路径治理（single workspace and path governance）

状态：`active`
适用习惯：H19

当前仓库根目录是唯一正式工作区。不得默认新建 fresh clone、audit clone、临时 clone、`git worktree add`、根目录外的执行目录或正式交付目录；外部路径最多作为只读来源，最终产物必须回到当前项目内。

如果外部工作区确有必要，停止并报告：`reason`、`target_path`、`risk`、`internal_alternative`，等待用户本轮明确授权。不得把 Desktop、Downloads 或临时目录写为正式路径，也不得把本机绝对路径写入可提交的规则或 GPT 分发包。

路径治理同时要求精确暂存、无关脏改隔离、保护 `project_bootstrap/collaboration_mechanism_migration/` 与 v1 archive。无法隔离时使用 `blocked_unrelated_dirty_changes_cannot_be_isolated`。

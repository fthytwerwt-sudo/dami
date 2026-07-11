# 完成接力与失败路由（completion relay and failure routes）

状态：`active`
适用机制：M11-M13
适用习惯：H15-H18

## Completion Relay

完整任务先建立 `required_output_inventory`、`child_task_graph`、`remaining_work_check`。关闭前校验交付、验证、状态回写、人工复审和 Git 收尾；缺任一必交付项时继续或 blocked，不把局部文件、fallback、本地产物或技术探测写成完成。

完成状态只可为 `completed_verified`、`completed_pending_human_review`、`partial_completed`、`blocked`。状态报告必须分开列 `status_promotions` 与 `status_not_promoted`，并诚实写 `Tested`、`Not-tested`、`blocked_items`、`remaining_work`、`下一个目标`。

## 失败路由

```text
missing_fact -> product_fact_collection
fact_conflict -> fact_conflict_resolution
missing_compliance_evidence -> compliance_validation
capability_unverified -> capability_probe
write_scope_violation -> scope_repair
supply_insufficient -> supply_repair
state_not_allowed -> state_transition_repair
completion_overclaim -> completion_claim_repair
git_inconsistent -> git_closeout_repair
human_decision_needed -> human_decision_required
```

`failure_route_resolver.py` 输出 repair route、owner 和 `next_safe_step`。禁止只写 retry；用户反馈“不对、空、怪怪的”时先做内部自修审计，必要时补料、修复或阻断，而非要求用户诊断工程原因。

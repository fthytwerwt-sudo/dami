# 单文件细节方案（per-file detail plan）

状态：`active`
适用习惯：H09

新增或修改机制文件、脚本、Schema、Validator 或节点前，为每个文件建立 `per_file_plan`。允许共享政策继承，但每个具体路径必须出现在一个计划组中，未列入路径不得修改。

必填字段：

```text
purpose
layer
inputs
outputs
core_decisions
trigger_conditions
route_rules
missing_info_policy
conflict_policy
blocked_if
examples
validation
user_review_points
```

`per_file_plan_validator.py` 必须在实现前验证这些字段。计划不是替代实现；实现后仍需脚本、Schema、Fixture、实际验证和 Git 收尾。

# 执行安全与人工闸门

状态：`active`
适用机制：M17、M18

## 默认执行边界

- 只修改任务明确允许的路径，不纳入无关脏改。
- 不读取、打印、复制或提交密钥；需要秘密才能继续时使用 `blocked_secret_access_required`。
- 外部动作默认不授权；本地草稿不等于外发批准。
- 先用 `dry-run`、沙箱、最小样本和可逆步骤验证能力；探测结果不得冒充正式执行。
- 删除、覆盖、迁移正式数据或无法可靠回滚时必须停止并请求授权。
- 候选研究、计划和机器验证不得写成正式事实或人工通过。

## 必须人工确认

- 正式市场、渠道、商业模式和规模化选择。
- 产品合规、健康、营养或医疗相关声明。
- 正式报价、交易数量、交付条件、代理条件及客户承诺。
- 合同、法律文本、付款、采购、付费资源和预算。
- 样品寄送、地址或个人信息使用、物流承诺。
- 正式邮件、消息、批量触达、广告、发布、上架和关键账号操作。
- 覆盖正式事实、改变正式业务状态、删除数据或不可逆动作。
- 需要法律、监管、税务、医疗或其他专业判断的最终结论。

授权记录最低字段：`action`、`target`、`scope`、`limit`、`valid_from`、`valid_until`、`approved_by`、`revocation`、`evidence`。

## 公开仓库安全

```yaml
business_sensitive_git_write_blocked_while_repo_public: true
```

仓库为公开状态时，不得写入客户、供应商、成本、报价、合同、认证或检测原件、个人信息、秘密及其他商业敏感数据。不得擅自改变仓库可见性。敏感资料只能留在已批准且被 Git 排除的私有位置。

## 具体阻断

- `blocked_authorization_required`
- `blocked_compliance_evidence_missing`
- `blocked_write_scope_violation`
- `blocked_secret_access_required`
- `blocked_repo_visibility_for_sensitive_data`
- `blocked_capability_unverified`

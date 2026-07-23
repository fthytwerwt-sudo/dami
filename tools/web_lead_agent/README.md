# 真实获客最小闭环 V1（Web Lead Minimal Loop V1）

本工具包是“大米低 GI 跨境”项目的获客工具底座验证版，只允许在 `codex/web-lead-minimal-loop-v1` 分支内演示和测试。

## 已实现链路

```text
获准的公开网页
→ 企业资料抓取
→ 结构化
→ 去重/评分
→ 产品知识检索
→ 个性化初稿
→ 确定性策略
→ 人工审批闸门
→ 一次受监督发送
→ 回执/页面结果
→ 状态保存
→ 强制停止
```

## 安全模式

- 默认模式：`draft_only`
- 允许模式：`supervised_single_send`
- 禁止模式：`bounded_autonomy`
- 未获用户明确授权目标网页、账号、消息和发送动作前，真实外部发送数量必须为 `0`。

## 本地验证

```bash
python -m pytest tools/web_lead_agent/tests -q
python -m compileall -q tools/web_lead_agent/src tools/web_lead_agent/tests
python -m web_lead_agent.cli run-synthetic --workspace /tmp/web-lead-agent-v1 --synthetic-approve
```

`run-synthetic` 只使用本地 fixture 和本机 HTTP server，不代表真实业务发送。

## 关键边界

- 不保存受保护客户资料、联系方式、报价、合同、认证原件、密钥或 Cookie。
- `WebsiteContactFormAdapter` 只支持获准域名、公开页面和一次提交。
- 任意 `UNKNOWN` 回执不自动重试。
- 同一目标、表单和消息生成的 idempotency key 已提交后会被阻断。

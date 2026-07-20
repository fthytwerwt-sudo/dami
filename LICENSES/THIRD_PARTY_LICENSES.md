# 第三方许可证与采用边界

> 本文是工程清单，不是法律意见。正式商业部署前仍需用户/法律复核。

## 实际安装

| 项目 | 版本 | 许可证/边界 | 本仓库用途 | 官方来源 |
|---|---:|---|---|---|
| Playwright Python | 1.61.0 | Apache-2.0 | localhost Chromium 抓取和 DOM 填入 | [LICENSE](https://github.com/microsoft/playwright-python/blob/main/LICENSE) |
| LangGraph | 1.2.9 | MIT | 最小 StateGraph、interrupt、resume | [LICENSE](https://github.com/langchain-ai/langgraph/blob/main/LICENSE) |
| LangGraph checkpoint SQLite | 3.1.0 | MIT 项目组件；需随发行复核 | SQLite checkpointer | [repository](https://github.com/langchain-ai/langgraph) |
| jsonschema | 4.26.0 | MIT | Draft 2020-12 Schema 验证 | [repository](https://github.com/python-jsonschema/jsonschema) |
| PyYAML | 6.0.3 | MIT | 工具和版本注册表 | [repository](https://github.com/yaml/pyyaml) |
| pytest / pytest-asyncio | 9.1.1 / 1.4.0 | MIT / Apache-2.0 | 测试，不进入业务运行链路 | [pytest](https://github.com/pytest-dev/pytest), [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) |

`langchain-core`、`langsmith` 等是 LangGraph 解析出的传递依赖，不是本仓库主动绑定的平台能力；完整快照见 `requirements.lock`。升级时必须重新执行许可证和依赖树复核。

## 研究过但未安装

- Crawl4AI：许可证主体类似 Apache-2.0，但附加 attribution/branding 条件；标记 `legal_review_required`，当前仅 `recheck_later`。
- Dify：modified Apache，含多租户和标识限制；当前 `reject`。
- n8n：Sustainable Use License 且含 enterprise 目录；当前 `reject`。
- Langfuse：MIT core 与 enterprise 专有目录并存；当前 `reference_only`。
- Chatwoot：MIT core 与 enterprise 专有目录并存；当前 `reference_only`。
- Twenty：许可/商业边界需进一步复核；当前 `recheck_later`。

详细项目矩阵和理由见 `docs/01_开源项目选型_open_source_selection.md`。

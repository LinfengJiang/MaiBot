# Tavily MCP 插件

该插件允许 MaiBot 通过 Tavily MCP 服务搜索网络信息。

## 配置
插件首次加载时会在 `src/plugins/tavily_mcp/actions` 目录生成 `tavily_mcp_config.toml`：

```toml
base_url = "https://api.tavily.com"
api_key = "YOUR_TAVILY_API_KEY"
```

请将 `api_key` 修改为你在 Tavily 获取的密钥。

## 动作
插件提供 `tavily_mcp` 动作，可在专注聊天中被调用。
动作参数：

- `query`：要搜索的关键词。
- `max_results`：返回结果数量，可选，默认 5。

当需要获取最新信息或用户主动请求网络搜索时，模型会选择此动作，并将搜索结果作为回复发送。

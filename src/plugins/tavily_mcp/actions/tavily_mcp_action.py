import requests
from typing import Tuple
from src.chat.focus_chat.planners.actions.plugin_action import PluginAction, register_action
from src.common.logger_manager import get_logger
from .generate_tavily_config import generate_config

logger = get_logger("tavily_mcp_action")

generate_config()


@register_action
class TavilyMCPAction(PluginAction):
    """Use Tavily MCP to search the web"""

    action_name = "tavily_mcp"
    action_description = "Search the web via Tavily MCP and return results"
    action_parameters = {
        "query": "Search query text",
        "max_results": "Maximum number of results (optional)",
    }
    action_require = [
        "当需要搜索网络信息时使用",
        "当用户请求最新信息时使用",
    ]
    default = False
    action_config_file_name = "tavily_mcp_config.toml"

    def __init__(
        self,
        action_data: dict,
        reasoning: str,
        cycle_timers: dict,
        thinking_id: str,
        global_config: dict | None = None,
        **kwargs,
    ):
        super().__init__(action_data, reasoning, cycle_timers, thinking_id, global_config, **kwargs)
        self.base_url = self.config.get("base_url", "https://api.tavily.com")
        self.api_key = self.config.get("api_key")
        logger.info(f"{self.log_prefix} TavilyMCPAction initialized with base_url {self.base_url}")

    async def process(self) -> Tuple[bool, str]:
        if not self.api_key:
            logger.error(f"{self.log_prefix} Tavily API key missing")
            await self.send_message_by_expressor("Tavily MCP 配置缺少 API 密钥，无法搜索。")
            return False, "api key missing"

        query = self.action_data.get("query")
        if not query:
            await self.send_message_by_expressor("请提供搜索关键词。")
            return False, "query missing"

        max_results = self.action_data.get("max_results", 5)
        payload = {"query": query, "max_results": max_results}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            url = f"{self.base_url.rstrip('/')}/search"
            logger.info(f"{self.log_prefix} Tavily request: {query}")
            response = requests.post(url, json=payload, headers=headers, timeout=20)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                summary = "\n".join(str(item) for item in results) if results else "未找到相关信息。"
                await self.send_message_by_expressor(summary)
                return True, summary
            logger.error(f"{self.log_prefix} Tavily error: {response.status_code} {response.text}")
            await self.send_message_by_expressor(f"Tavily MCP 请求失败：{response.status_code}")
            return False, f"http {response.status_code}"
        except Exception as e:
            logger.error(f"{self.log_prefix} Tavily request error: {e}")
            await self.send_message_by_expressor("Tavily MCP 请求时发生错误。")
            return False, str(e)

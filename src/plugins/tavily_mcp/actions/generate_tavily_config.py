import os

CONFIG_CONTENT = """\
# Tavily MCP API base URL
base_url = "https://api.tavily.com"
# API key for Tavily MCP
api_key = "YOUR_TAVILY_API_KEY"
"""


def generate_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "tavily_mcp_config.toml")
    if not os.path.exists(config_path):
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(CONFIG_CONTENT)
            print(f"配置文件已生成: {config_path}")
        except IOError as e:
            print(f"无法写入配置文件 {config_path}: {e}")
    else:
        print(f"配置文件已存在: {config_path}")


if __name__ == "__main__":
    generate_config()

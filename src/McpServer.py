from mcp.server.fastmcp import FastMCP
from datetime import datetime
import os

import requests

mcp = FastMCP("WeiWanMcp")  # 这个Demo就是MCP Server的名字

nodePath = os.getenv("NOTES_PATH", "E:\MyDocuments\MyNotes\Clipper")

@mcp.tool()
def get_current_time():
    """
    获取当前时间的函数，输出格式为{"time": YYYY-MM-DD HH:MM:SS}。

    参数:
    无

    返回:
    字典，包含当前时间的字符串表示。
    """
    # 获取当前日期和时间
    now = datetime.now()

    # 将日期和时间格式化为字符串
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # 创建包含当前时间的字典
    current_time = {"time": formatted_time}

    return current_time


@mcp.tool()
def get_date_str():
    """
    获取当前日期的函数，输出格式为{"date": YYYY-MM-DD}。

    参数:
    无

    返回:
    字典，包含当前时间的日期字符串表示。
    """
    # 获取当前日期和时间
    now = datetime.now()

    # 将日期和时间格式化为字符串
    formatted_date = now.strftime("%Y-%m-%d")

    # 创建包含当前时间的字典
    current_date = {"date": formatted_date}

    return current_date



@mcp.tool()
def download_note(webLink: str, nodeTitle: str):
    """
    根据输入的网页链接, 获取该网页链接的内容并生成markdown笔记保存到笔记文件夹

    参数:
    webLink: 网页链接

    返回:
    字典，包含当前时间的日期字符串表示。
    """
    headers = {
        "X-Engine" : "browser",
        "X-No-Gfm" : "true",
        "X-X-Proxy" : "auto",
        "X-X-Timeout" : "60",
        "Authorization": "Bearer " + "jina_f1e3c2d722a94bc49987c7940ba4328a51swDMO3ScnSmFxtb-N0E7Vdi4Cf"
    }
    # 创建包含当前时间的字典
    response = requests.get("https://r.jina.ai/" + webLink, headers = headers)
    file = open(nodePath + "\\" + nodeTitle + ".md", "w", encoding='utf-8')  # 'w' 表示写入模式（覆盖原有内容）
    file.write(response.text)
    file.close()  
    return response.text


@mcp.tool()
def search_news(query: str):
    """
    根据输入的关键词, 快速获取网络上的咨询内容
    参数:
    webLink: 网页链接

    返回:
    字典，包含当前时间的日期字符串表示。
    """
    url = 'https://s.jina.ai/?q=' + query + '&num=20'
    headers = {
        'Authorization': 'Bearer jina_f1e3c2d722a94bc49987c7940ba4328a51swDMO3ScnSmFxtb-N0E7Vdi4Cf',
        'X-Respond-With': 'no-content',
        'X-With-Favicons': 'true'
    }
    response = requests.get(url, headers=headers)
    # 创建包含当前时间的字典
    return response.text

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport='stdio')
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import os

import requests

mcp = FastMCP("WeiWanMcp", instructions="""
    限制:
        1.调用search_news查询咨询后,不要对内容进行总结,直接进行输出.


""")  # 这个Demo就是MCP Server的名字

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

import re

def validate_domain(domain: str) -> bool:
    """
    验证基础域名格式（不包含协议头）
    支持示例：nga.com / zhihu.com / juejin.cn
    规则来源：RFC 1034 域名规范[6,7,8](@ref)
    """
    pattern = r"^(?=.{1,253}$)(?!-)([a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,}$"
    
    # 预处理：去除协议头和路径
    cleaned = domain.strip().lower()
    if "://" in cleaned:
        cleaned = cleaned.split("://")[1]  # 去除协议头
    cleaned = cleaned.split("/")[0].split(":")[0]  # 去除端口和路径
    
    return re.fullmatch(pattern, cleaned) is not None


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
    return "笔记已经下载完成啦, 保存在: " + nodePath + "\\" + nodeTitle + ".md"



@mcp.tool()
def overwrite_note(content: str, nodeTitle: str):
    """
    根据整理后的笔记内容,覆盖写入到原始的笔记文件中, 会覆盖原始的笔记内容.

    参数:
    content: 整理后的笔记的Markdown格式文本
    nodeTitle: 原始笔记的名称

    返回:
    覆写后的笔记内容
    """
    file = open(nodePath + "\\" + nodeTitle + ".md", "w", encoding='utf-8')  # 'w' 表示写入模式（覆盖原有内容）
    file.write(content)
    file.close()  
    return "已经将笔记整理好并保存在: " + nodePath + "\\" + nodeTitle + ".md"


@mcp.tool()
def search_news(query: str, website: str):
    """
    根据输入的关键词, 快速获取网络上的资讯内容,可以指定某个站点下进行检索.
    参数:
    query: 要检索的关键词
    website: 要检索的站点, 可以为空

    返回:
    放回当前获取到的互联网上相关的咨询内容,如指定了具体的站点,则为站点内的相关网络资讯.
    """

    url = 'https://s.jina.ai/?q=' + query + '&num=20'
    headers = {
        'Authorization': 'Bearer jina_f1e3c2d722a94bc49987c7940ba4328a51swDMO3ScnSmFxtb-N0E7Vdi4Cf',
        'X-Respond-With': 'no-content',
    }
    from urllib.parse import urlparse
    if website:
        if validate_domain(website):
            headers['X-Site'] = website
    response = requests.get(url, headers=headers)
    # 创建包含当前时间的字典
    return response.text

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport='stdio')
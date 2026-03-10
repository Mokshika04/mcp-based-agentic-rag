from fastmcp import FastMCP
from tools.arxiv_tool import search_papers
from tools.github_tool import search_repo_by_topic
from tools.newsdata_tool import fetch_latest_news 

mcp = FastMCP("MCP Server")

# Tools for searching the web
mcp.tool()(search_papers)
mcp.tool()(search_repo_by_topic)
mcp.tool()(fetch_latest_news)



from fastmcp import FastMCP
from tools.arxiv_tool import search_papers
from tools.github_tool import search_repo_by_topic
from tools.newsdata_tool import fetch_latest_news 
from tools.web_search_tool import websearch
from local_rag_pipeline. vector_search import local_rag_search

mcp = FastMCP("MCP Server")

# Tools for searching the web
mcp.tool()(search_papers)
mcp.tool()(search_repo_by_topic)
mcp.tool()(fetch_latest_news)
mcp.tool()(websearch)

# Tool for searching the local database
@mcp.tool()
def search_local_documents(query: str) -> str:
    """Search local documents using vector similarity search."""
    return local_rag_search(query)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
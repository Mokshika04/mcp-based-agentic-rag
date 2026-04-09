from fastmcp import FastMCP
from technical_agent import agent_fetch_tools
from general_convo_agent import conversational_agent

mcp = FastMCP("MCP Server")

# Agentic tools for research and general conversations
mcp.tool()(agent_fetch_tools)
mcp.tool()(conversational_agent)


if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
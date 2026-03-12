import asyncio
from fastmcp import Client
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

# MCP Client Connection
client = Client("http://127.0.0.1:8000/sse")

async def call_mcp_tool(tool_name, query):
    """
    Function to call mcp tools
    """
    response = await client.call_tool(tool_name, {"query":query})
    return response

# Creating tools for the llm to interact with
@tool
def research_tool(query:str)->str:
    """Search for research papers."""
    return asyncio.run(call_mcp_tool("search_papers", query))

@tool
def github_tool(query:str)->str:
    """Search Github for trending repositories."""
    return asyncio.run(call_mcp_tool("search_repo_by_topic", query))

@tool
def news_tool(query:str)->str:
    """Search for the latest/trending news in tech."""
    return asyncio.run(call_mcp_tool("fetch_latest_news", query))

@tool
def rag_tool(query:str)->str:
    """Searches the local documents"""
    return asyncio.run(call_mcp_tool("search_local_documents", query))

llm = ChatOllama(
    model = "llama3.2:latest",
    disable_streaming=False 
    )

agent = create_agent(
    model=llm,
    tools=[research_tool, github_tool, news_tool, rag_tool]
    )

async def main():

    while True:
        query = input("User: ")
        
        if query.lower() == "exit":
            break
        response = await agent.ainvoke({"input": query})

        print("Agent:", response)

    await client.close()

asyncio.run(main())

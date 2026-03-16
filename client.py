import asyncio
from fastmcp import Client
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# MCP Client Connection
client = Client("http://127.0.0.1:8000/sse")

async def call_mcp_tool(tool_name, query):
    """
    Function to call mcp tools
    """
    async with client:
        response = await client.call_tool(tool_name, {"query":query})
        return response

# Creating tools for the llm to interact with
@tool
async def research_tool(query:str)->str:
    """Search for research papers."""
    return await call_mcp_tool("search_papers", query)

@tool
async def github_tool(query:str)->str:
    """Search Github for trending repositories."""
    return await call_mcp_tool("search_repo_by_topic", query)

@tool
async def news_tool(query:str)->str:
    """Search for the latest/trending news in tech."""
    return await call_mcp_tool("fetch_latest_news", query)

@tool
async def rag_tool(query:str)->str:
    """Searches the local documents"""
    return await call_mcp_tool("search_local_documents", query)

# Initializing the Ollama model
llm = ChatOllama(
    model = "llama3.2:latest",
    disable_streaming=False,
    )

# ChatPromptTemplate 
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that uses tools to answer questions."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

# Creating the Agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=[research_tool, github_tool, news_tool, rag_tool],
    prompt=prompt
    )

# Creating the Executor
agent_executor = AgentExecutor(agent=agent, tools=[research_tool, github_tool, news_tool, rag_tool])

async def main():

    while True:
        query = input("User: ")
        
        if query.lower() == "exit":
            break
        response = await agent_executor.ainvoke({"input": query})
        print("Agent:", response)

    await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 

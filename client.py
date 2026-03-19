import asyncio
# from fastmcp import Client
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from tools.arxiv_tool import search_papers
from tools.github_tool import search_repo_by_topic
from tools.newsdata_tool import fetch_latest_news 

# MCP Client Connection
# client = Client("http://127.0.0.1:8000/sse")

# async def call_mcp_tool(tool_name, query):
#     """
#     Function to call mcp tools
#     """
#     async with client:
#         response = await client.call_tool(tool_name, {"query":query})
#         return response

# Creating tools for the llm to interact with
# @tool
# async def research_tool(query:str)->str:
#     """Search for research papers."""
#     return await call_mcp_tool("search_papers", query)

# @tool
# async def github_tool(query:str)->str:
#     """Search Github for trending repositories."""
#     return await call_mcp_tool("search_repo_by_topic", query)

# @tool
# async def news_tool(query:str)->str:
#     """Search for the latest/trending news in tech."""
#     return await call_mcp_tool("fetch_latest_news", query)

# @tool
# async def rag_tool(query:str)->str:
#     """Searches the local documents"""
#     return await call_mcp_tool("search_local_documents", query)

tools = [search_papers, search_repo_by_topic, fetch_latest_news]

# Initializing the Ollama model
llm = ChatOllama(
    model = "llama3.2:latest",
    disable_streaming=False,
    )

# ChatPromptTemplate 
prompt = ChatPromptTemplate.from_messages([
        ("system", 
        "You are an AI assistant designed to help users find the most relevant and up-to-date information/news on topics related to technology and research.\n"
        "You have access to the following tools:\n"
        "- search_papers: Search for research papers.\n"
        "- search_repo_by_topic: Search Github for trending repositories.\n"
        "- fetch_latest_news: Search for the latest/trending news in tech.\n"
        "- search_local_documents: Searches the local documents.\n"
        "Your goal is to provide accurate, data-driven answers by synthesized information from your tools.\n\n"
        
        "RULES OF ENGAGEMENT:\n"
        "1. ALWAYS check local documents first using 'search_local_documents' before searching external sources.\n"
        "2. If external tools (ArXiv, GitHub, Newsdata) return no results, inform the user clearly.\n"
        "3. When citing papers or repos, always include the title and the direct link(URL).\n"
        "4. Be concise but technical. If the user's query is vague, ask for clarification before searching."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

# Creating the Agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
    )

# Creating the Executor
agent_executor = AgentExecutor(agent=agent, tools=tools)

async def main():
    while True:
        query = input("User: ")
        
        if query.lower() == ("exit", "quit", "bye"):
            break
        response = await agent_executor.ainvoke({"input": query})
        print("Agent:", response)

#     await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 

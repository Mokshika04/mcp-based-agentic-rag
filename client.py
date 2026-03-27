import asyncio
import tiktoken
from fastmcp import Client
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from typing import Any
from langchain_classic.memory import ConversationSummaryBufferMemory 

# MCP Client Connection
client = Client("http://127.0.0.1:8000/sse")

async def call_mcp_tool(tool_name, **kwargs):
    """
    Function to call mcp tools
    """
    async with client:
        response = await client.call_tool(tool_name, kwargs)
        return response


def extract_string(value) -> str:
    """Handles cases where the LLM passes a dict instead of a plain string."""
    if isinstance(value, dict):
        return value.get("value") or value.get("query") or value.get("topic") or str(value)
    return str(value)

# Creating tools for the llm to interact with
@tool
async def research_tool(query:Any)->str:
    """Search for research papers.Input is a plain topic string."""
    return await call_mcp_tool("search_papers", query=extract_string(query))

@tool
async def github_tool(topic:Any)->str:
    """Search Github for trending repositories."""
    return await call_mcp_tool("search_repo_by_topic", topic=extract_string(topic))

@tool
async def news_tool(query:Any)->str:
    """Search for the latest/trending news. Input should be a plain search string, e.g. 'AI news' or 'latest tech'."""
    return await call_mcp_tool("fetch_latest_news", query=extract_string(query))

@tool
async def rag_tool(query:Any)->str:
    """Searches the local documents"""
    return await call_mcp_tool("search_local_documents", query=extract_string(query))

tools = [research_tool, github_tool, news_tool, rag_tool]

# Initializing the Ollama model
llm = ChatOllama(
    model = "llama3.2:latest",
    disable_streaming=False,
    )

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=500,
    memory_key="chat_history",
    return_messages=True,
    tiktoken_encoder_name="cl100k_base"
    )

# ChatPromptTemplate 
prompt = ChatPromptTemplate.from_messages([
        ("system", 
        "You are an AI assistant designed to help users find the most relevant and up-to-date information/news on topics related to technology and research.\n"
        "You have access to the following tools:\n"
        "- research_tool: Search for research papers.\n"
        "- github_tool: Search Github for trending repositories.\n"
        "- news_tool: Search for the latest/trending news in tech.\n"
        "- rag_tool: Searches the local documents.\n"
        "Your goal is to provide accurate, data-driven answers by synthesized information from your tools.\n\n"
        
        "RULES OF ENGAGEMENT:\n"
        "1. ALWAYS check local documents first using rag_tool before searching external sources.\n"
        "2. If external tools (ArXiv, GitHub, Newsdata) return no results, inform the user clearly.\n"
        "3. When citing papers or repos, always include the title and the direct link(URL).\n"
        "4. Be concise but technical. If the user's query is vague, ask for clarification before searching."),

        MessagesPlaceholder(variable_name="chat_history"),

        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

# Creating the Agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
    )

# Creating the Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose= True)

async def main():
    while True:
        query = input("User: ")
        
        if query.lower() in ("exit", "quit", "bye"):
            print("Goodbye!")
            break

        response = await agent_executor.ainvoke({"input": query})
        print("Agent:", response)

    await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 

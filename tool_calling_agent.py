from tools.arxiv_tool import search_papers
from tools.github_tool import search_repo_by_topic
from tools.newsdata_tool import fetch_latest_news 
from tools.web_search_tool import websearch
from local_rag_pipeline. vector_search import local_rag_search
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_classic.memory import ConversationSummaryBufferMemory 
from langchain.tools import tool

@tool
def agent_fetch_tools():
    tools = [search_papers, search_repo_by_topic, fetch_latest_news, websearch, local_rag_search]

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
            "- search_tool: Searches the web for a given query.\n"
            "Your goal is to provide accurate, data-driven answers by synthesized information from your tools.\n\n"
            
            "RULES OF ENGAGEMENT:\n"
            "1. ALWAYS check local documents first using rag_tool before searching external sources.\n"
            "2. If external tools (ArXiv, GitHub, Newsdata, Websearch) return no results, inform the user clearly.\n"
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

    return agent_executor 
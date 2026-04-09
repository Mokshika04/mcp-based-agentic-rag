from tools.arxiv_tool import search_papers
from tools.github_tool import search_repo_by_topic
from tools.newsdata_tool import fetch_latest_news 
from tools.web_search_tool import websearch
from local_rag_pipeline. vector_search import local_rag_search
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from shared_resources import llm

@tool
def agent_fetch_tools(query:str, chat_history:list= None):
    """
    A multi-tool orchestrator that selects and executes the most appropriate research or search tool 
    based on the user's query.

    This function acts as a meta-agent that coordinates between five specialized data sources:
    1. Local RAG (vector_search): Internal document retrieval.
    2. ArXiv (search_papers): Technical and academic research papers.
    3. GitHub (search_repo_by_topic): Trending software repositories and codebases.
    4. NewsData (fetch_latest_news): Real-time technology and industry news.
    5. Web Search (websearch): General internet queries for broad information.

    Args:
        query (str): The specific question, topic, or research interest provided by the user.

    Returns:
        str: Returns the string output.
    """

    if chat_history is None:
        chat_history = []

    tools = [search_papers, search_repo_by_topic, fetch_latest_news, websearch, local_rag_search]

    # ChatPromptTemplate 
    prompt = ChatPromptTemplate.from_messages([
            ("system", 
            "You are an AI assistant designed to help users find the most relevant and up-to-date information/news on topics related to technology and research.\n"
            "You have access to the following tools:\n"
            "- search_papers: Search for research papers.\n"
            "- search_repo_by_topic: Search Github for trending repositories.\n"
            "- fetch_latest_news: Search for the latest/trending news in tech.\n"
            "- local_rag_search: Searches the local documents.\n"
            "- websearch: Searches the web for a given query.\n"
            "Your goal is to provide accurate, data-driven answers by synthesized information from your tools.\n\n"
            
            "RULES OF ENGAGEMENT:\n"
            "1. LOCAL SEARCH: Only use the 'local_rag_search' if the user explicitly asks for local, internal, or private document searches. If 'local_rag_search' returns no results, state clearly: 'No such data found in local documents.'\n"
            "2. EXTERNAL SEARCH: If external tools return no results, inform the user clearly that no information was found.\n"
            "3. NO HALLUCINATION: You must ONLY provide answers based on the data returned by the tools. Do NOT use your internal training data to answer technical questions.\n"
            "4. CITATIONS: When citing papers or repos, always include the full Title and the direct URL link.\n"
            "5. CLARIFICATION: Be concise and technical. If a query is too vague to select a tool, ask for clarification before proceeding."),

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
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose= True)
    response = agent_executor.invoke({
        "input":query, 
        "chat_history": chat_history
        })

    return response["output"]
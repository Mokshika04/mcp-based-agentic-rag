from tools.arxiv_tool import search_papers
from tools.github_tool import search_repo_by_topic
from tools.newsdata_tool import fetch_latest_news 
from tools.web_search_tool import websearch
from local_rag_pipeline. vector_search import local_rag_search
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from shared_resources import llm

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
        "You are a strict tool-using AI agent.\n\n"

        "CRITICAL RULE:\n"
        "You are NOT allowed to answer any query using your own knowledge.\n"
        "You MUST ALWAYS call one of the provided tools before giving a final answer.\n"
        "If you do not call a tool, your response is INVALID.\n\n"

        "MANDATORY PROCESS:\n"
        "1. Analyze the user query.\n"
        "2. Select the MOST appropriate tool.\n"
        "3. Call the tool.\n"
        "4. Generate the final answer ONLY using the tool result.\n\n"

        "AVAILABLE TOOLS:\n"
        "- search_papers → for research papers, academic or technical topics.\n"
        "- search_repo_by_topic → for GitHub repositories, code, ML projects.\n"
        "- fetch_latest_news → for latest or trending technology/news.\n"
        "- websearch → for general queries (e.g., people, concepts, definitions).\n"
        "- local_rag_search → ONLY for internal/local/private documents.\n\n"

        "TOOL SELECTION RULES:\n"
        "- For general factual queries (e.g., 'Who is Messi?'), queries related to trending topics and discussions(twitter/reddit)(e.g., 'What's trending?'), ALWAYS use websearch.\n"
        "- For latest or recent information, ALWAYS use fetch_latest_news.\n"
        "- For research topics, ALWAYS use search_papers.\n"
        "- For coding or ML repositories, ALWAYS use search_repo_by_topic.\n"
        "- Use local_rag_search ONLY if explicitly asked for local/internal data.\n\n"

        "STRICT CONSTRAINTS:\n"
        "- NEVER answer directly without calling a tool.\n"
        "- NEVER use internal knowledge.\n"
        "- If a tool returns no results, say: 'No relevant information found from tools.'\n\n"

        "OUTPUT RULES:\n"
        "- Base your answer ONLY on tool output.\n"
        "- Be concise and technical.\n"
        "- Include links when available.\n"
        ),
            MessagesPlaceholder(variable_name="history"),

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
        "input": query,
        "history": chat_history
        })

    print("THIS IS THE TECHNICAL AGENT")
    return response["output"]
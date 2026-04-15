import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

# Initialize once
tavily_api_key = os.getenv("TAVILY_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)


def _enhance_query(query: str) -> str:
    """
    Enhance query only when social/news intent is detected.
    """
    trigger_words = ["news", "latest", "trend", "trending", "update", "reaction"]

    if any(word in query.lower() for word in trigger_words):
        return f"{query} (site:x.com OR site:twitter.com OR site:reddit.com)"
    
    return query


@tool
def websearch(query: str):
    """
    Performs a real-time web search using the Tavily API to retrieve relevant information.

    This function connects to the Tavily search engine to fetch summaries, URLs, and 
    relevant content for a given query. It is designed to provide up-to-date context 
    that may not be present in an LLM's static training data.

    Additionally, it automatically includes Twitter (X) and Reddit sources when the 
    query is related to news, trends, or real-time updates, enabling access to social 
    media insights and community discussions.

    Args:
        query (str): The search term or question to look up on the web.

    Returns:
        dict: A dictionary containing:
            - original_query: The input query by the user
            - enhanced_query: The modified query (if social sources are included)
            - summary: A concise answer from Tavily
            - sources: A list of results, each containing 'title', 'url', and 'content'
    """

    # Smart enhancement
    enhanced_query = _enhance_query(query)

    response = tavily_client.search(
        enhanced_query,
        search_depth='basic',
        include_answer=True
    )

    summary = response.get("answer", "")
    results = response.get("results", [])[:3]

    sources = [
        {
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content")  # added for better reasoning
        }
        for r in results
    ]

    clean_output = {
        "original_query": query,
        "enhanced_query": enhanced_query,
        "summary": summary,
        "sources": sources,
    }

    print("Web search executed")
    return clean_output



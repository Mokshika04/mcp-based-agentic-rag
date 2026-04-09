import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

@tool
def websearch(query:str):
    """
    Performs a real-time web search using the Tavily API to retrieve relevant information.

    This function connects to the Tavily search engine to fetch snippets, URLs, and 
    relevance scores for a given search query. It is designed to provide up-to-date 
    context that may not be present in an LLM's static training data.

    Args:
        query (str): The search term or question to look up on the web.

    Returns:
        dict: A dictionary containing results. 
              Each result typically includes 'summary','title', 'url'.
    """

    tavily_api_key = os.getenv("TAVILY_KEY")
    tavily_client = TavilyClient(api_key=tavily_api_key)

    response = tavily_client.search(query, search_depth='basic', include_answer=True)

    summary = response.get("answer", "")
    results = response.get("results", [])[:3]
    sources = [
        {
            "title": r.get("title"),
            "url": r.get("url")
        }
        for r in results
    ]

    clean_output = {
        "query": query,
        "summary": summary,
        "sources": sources,
    }
    return clean_output



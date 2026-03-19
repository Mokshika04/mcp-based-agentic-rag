import os
from dotenv import load_dotenv
from newsdataapi import NewsDataApiClient
from langchain.tools import tool

# Load the environment variables from the .env file
load_dotenv()
@tool
def fetch_latest_news(query:str, limit:int=3):
    """
    Fetch the latest news articles based on a query string.
    
    Args:
        query (str): The search term.
        limit (int): Number of results to return. Defaults to 3.
    
    Returns:
        list: A list of relevant news articles.
    """

    # Get the NewsData API key from environment variables
    newsdata_api_key = os.getenv("NEWSDATA.IO_API_KEY")

    # Initialize the NewsData API client
    api = NewsDataApiClient(apikey=newsdata_api_key)
    latest_response = api.latest_api(q=query)

    articles = latest_response.get('results', [])
    results=[]
    for article in articles[:limit]:
        results.append({
            "title": article.get("title"),
            "link": article.get("link"),
            "description": article.get("description"),
            "source": article.get("source")
        })
    return results




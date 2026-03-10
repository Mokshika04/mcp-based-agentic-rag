import os
from dotenv import load_dotenv
from newsdataapi import NewsDataApiClient

# Load the environment variables from the .env file
load_dotenv()

def fetch_latest_news(query:str, limit=5):
    """
    Fetch the latest news articles based on a query string.
    Takes a query string as input and returns a list of relevant news articles with their titles, links, descriptions, and sources.
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




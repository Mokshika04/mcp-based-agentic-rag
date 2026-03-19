import os
from dotenv import load_dotenv
from github import Github, Auth
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from langchain.tools import tool

# Load the environment variables from the .env file
load_dotenv()
@tool
def search_repo_by_topic(topic:str, limit: Optional[int]=None)-> List[Dict[str, Any]]:
    """
    Search for GitHub repositories based on a specific topic.

    This function queries the GitHub API to find relevant projects. If no limit 
    is provided, it defaults to returning 3 results.

    Args:
        topic (str): The keyword or topic to search for (e.g., 'machine-learning').
        limit (Optional[int], optional): The maximum number of repositories to return. 
            Defaults to 3 if None or not provided.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries. Each dictionary contains:
            - 'name' (str): The full name of the repository.
            - 'stars' (int): The number of stargazers.
            - 'description' (str): A brief summary of the project.
            - 'url' (str): The GitHub HTML link.

    Raises:
        ValueError: If the topic is an empty string.
    """
    if not topic:
        raise ValueError("The topic search string cannot be empty.")
    print(topic)
    
    result_limit = limit if limit is not None else 3 

    token = os.getenv("GIT_HUB_TOKEN")

    # Authenticate with GitHub using the token
    auth = Auth.Token(token)
    github_client = Github(auth=auth, timeout=10)

    # Repositories created in the last 15 days, sorted by stars
    last_week = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")
    github_query = f"created:>{last_week} topic:{topic} stars:>5"

    repos = github_client.search_repositories(query=github_query, sort="stars", order="desc")

    results=[]
    for repo in repos[:result_limit]:
        results.append({
            "name": repo.full_name,
            "stars": repo.stargazers_count,
            "description": repo.description or "No description provided",
            "url": repo.html_url
        })

    # Handling the Empty case 
    if not results:
        return [{"result": f"No trending repositories found for '{topic}' in the last 15 days."}]

    return results 
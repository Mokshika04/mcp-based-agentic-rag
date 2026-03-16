import os
from dotenv import load_dotenv
from github import Github, Auth
from datetime import datetime, timedelta

# Load the environment variables from the .env file
load_dotenv()

def search_repo_by_topic(topic:str, limit=5):
    """
    Search for GitHub repositories based on a topic.
    Takes a topic string as input and returns a list of relevant repositories with their names, stars, descriptions, and URLs.
    """
    token = os.getenv("GIT_HUB_TOKEN")

    # Authenticate with GitHub using the token
    auth = Auth.Token(token)
    github_client = Github(auth=auth)

    # Repositories created in the last week, sorted by stars
    last_week = datetime.now() - timedelta(days=7)
    date_query = last_week.strftime("%Y-%m-%d")
    github_query = f"created:>{date_query} topic:{topic}"

    repos = github_client.search_repositories(query=github_query, sort="stars", order="desc")

    results=[]
    for repo in repos[:limit]:
        results.append({
            "name": repo.full_name,
            "stars": repo.stargazers_count,
            "description": repo.description or "No description provided",
            "url": repo.html_url
        })

    return results

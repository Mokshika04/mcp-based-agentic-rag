import arxiv

def search_papers(query: str):
    """
    Search for research papers on arXiv based on a specific query.

    Connects to the arXiv API to retrieve a collection of scientific papers 
    matching the input criteria. This is useful for gathering metadata 
    for literature reviews or agentic RAG workflows.

    Args:
        query (str): The search term or keywords to look for (e.g., "machine learning").

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains:
            - 'title' (str): The full title of the paper.
            - 'authors' (list): Names of the contributing researchers.
            - 'summary' (str): A brief abstract of the work.
            - 'link' (str): The direct URL to the paper on arXiv.
            - 'published' (str): The original publication date.
    """
    search_query = f'{query} AND (cat:cs.* OR cat:eess.*)'

    # An arXiv API client which handles requests and retries
    client = arxiv.Client(
        page_size=10,      
        delay_seconds=3,  
        num_retries=5      
    )
    
    # The search parameters 
    search = arxiv.Search(
        query=search_query,
        max_results=5,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    # Returns a list of dictionaries containing the title, authors, summary, and link for each paper
    papers = [] 
    for result in client.results(search):
        papers.append({
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "summary": result.summary,
            "link": result.entry_id,
            "published": result.published
        })

    return papers 
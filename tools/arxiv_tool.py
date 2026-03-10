import arxiv

def search_papers(query: str):
    """
    Search for papers on arXiv based on a query string. 
    Takes a query string as input and returns a list of relevant papers with their titles, authors, summaries, links, and publication dates.
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


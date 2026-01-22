import os
import time
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

def search_papers(topic: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Searches for papers on Semantic Scholar using the Graph API directly.
    """
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    headers = {}
    if api_key:
        print(f"Initializing Semantic Scholar with Private API Key: {api_key[:5]}...")
        headers["x-api-key"] = api_key
    else:
        print("WARNING: SEMANTIC_SCHOLAR_API_KEY not found. Using Public API (rate limits apply).")
    
    print(f"Searching Semantic Scholar for: {topic}")
    
    # Rate limiting: 1 request per second to be safe
    time.sleep(1.0)
    
    query_params = {
        "query": topic,
        "limit": limit,
        "fields": "title,abstract,authors,year,venue,citationCount,openAccessPdf,url,paperId"
    }
    
    try:
        print(f"Sending search request for '{topic}' with limit={limit}...")
        response = requests.get(base_url, params=query_params, headers=headers)
        
        if response.status_code == 403:
             print("Authentication failed or API key invalid. Falling back to public API (removing key).")
             headers.pop("x-api-key", None)
             # Wait a bit before retrying
             time.sleep(2.0)
             response = requests.get(base_url, params=query_params, headers=headers)

        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
        data = response.json()
        results = data.get("data", [])
        print("Search request sent. Processing results...")
        
        papers = []
        count = 0
        for item in results:
            count += 1
            title = item.get("title", "Unknown")
            print(f"Processing paper {count}: {title}")
            
            # Extract authors safely
            authors_list = item.get("authors", [])
            # authors_list handles cases where it might be Nonr
            if authors_list is None: authors_list = []
            author_names = [a.get("name") for a in authors_list if a.get("name")]
            
            paper_data = {
                "title": title,
                "abstract": item.get("abstract", ""),
                "year": item.get("year"),
                "authors": author_names,
                "venue": item.get("venue"),
                "citationCount": item.get("citationCount", 0),
                "url": item.get("url"),
                "pdf_url": None,
                "paperId": item.get("paperId")
            }
            
            # Check for Open Access PDF
            open_access = item.get("openAccessPdf")
            if open_access and isinstance(open_access, dict) and "url" in open_access:
                paper_data["pdf_url"] = open_access["url"]
            
            papers.append(paper_data)
            
        print(f"Successfully processed {len(papers)} papers.")
        return papers

    except Exception as e:
        print(f"Error searching Semantic Scholar: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    # Test
    found = search_papers("Agentic AI workflows", limit=1)
    if found:
        print(f"Title: {found[0]['title']}")
        print(f"PDF: {found[0]['pdf_url']}")

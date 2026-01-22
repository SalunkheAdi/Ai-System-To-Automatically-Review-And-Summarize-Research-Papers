import arxiv

def test_arxiv():
    print("Testing Arxiv search...")
    client = arxiv.Client()
    search = arxiv.Search(
        query = "Agentic AI",
        max_results = 2,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    for result in client.results(search):
        print(f"Title: {result.title}")
        print(f"PDF: {result.pdf_url}")
        print(f"Summary: {result.summary[:100]}...")

if __name__ == "__main__":
    test_arxiv()

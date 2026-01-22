import sys
import os
import time

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from search import search_papers

print("Starting Semantic Scholar search test...")
start_time = time.time()
try:
    print("Calling search_papers...")
    papers = search_papers("Agentic AI", limit=1)
    end_time = time.time()
    print(f"Search returned in {end_time - start_time:.2f} seconds.")
    print(f"Found {len(papers)} papers.")
    if papers:
        print(papers[0])
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

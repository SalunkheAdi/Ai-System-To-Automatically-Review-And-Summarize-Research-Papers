import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from search import search_papers

print("Starting search test...")
try:
    print("Calling sch.search_paper...")
    results = search_papers("Agentic AI", limit=1)
    print("Search returned.")
    print(f"Found {len(results)} papers.")
    if results:
        print(results[0])
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

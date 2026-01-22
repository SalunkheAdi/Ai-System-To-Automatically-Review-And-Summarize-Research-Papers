import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

try:
    from src.graph.graph import app_graph
    print("SUCCESS: Graph imported and compiled successfully.")
except Exception as e:
    print(f"FAILURE: Could not import graph. Error: {e}")

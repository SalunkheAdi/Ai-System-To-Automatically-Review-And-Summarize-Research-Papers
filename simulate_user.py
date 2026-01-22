import sys
import os
from dotenv import load_dotenv

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from graph.graph import app_graph

# Load env vars
load_dotenv()

def simulate_user_request():
    print("--- SIMULATION START: User inputs 'Agentic AI' ---")
    
    initial_state = {
        "topic": "Agentic AI",
        "revision_count": 0
    }
    
    try:
        # Invoke the graph just like the Gradio app does
        final_state = app_graph.invoke(initial_state)
        
        print("\n--- SIMULATION COMPLETE ---")
        if final_state.get("final_review"):
            print("SUCCESS: Review generated!")
            print(f"Review Length: {len(final_state['final_review'])} characters")
        else:
            print("FAILURE: No review generated.")
            
    except Exception as e:
        print(f"\n--- CRITICAL ERROR ---")
        print(f"Simulation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simulate_user_request()

import operator
from typing import Annotated, List, TypedDict, Union

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage

# Import our core modules
# Note: Adjust imports based on actual file locations if needed
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from search import search_papers
from extraction import download_pdf, extract_text_from_pdf, process_papers_concurrently
from analysis import analyze_paper, synthesize_findings, analyze_papers_concurrently
from writing import write_review_section, format_references
from critique import critique_draft, revise_draft

class ResearchState(TypedDict):
    topic: str
    local_files: List[str] # List of file paths
    papers: List[dict]
    analyses: List[dict]
    synthesis: str
    draft: dict
    critique: str
    final_review: str
    revision_count: int
    max_results: int

def search_node(state: ResearchState):
    print("--- SEARCHING / LOADING PAPERS ---")
    topic = state.get('topic')
    local_files = state.get('local_files', [])
    papers = []

    # 1. Process Local Files
    if local_files:
        print(f"Found {len(local_files)} local files.")
        for file_path in local_files:
            # Create a paper object for the local file
            file_name = os.path.basename(file_path)
            papers.append({
                "title": file_name, # Use filename as title initially
                "paperId": file_name,
                "pdf_path": file_path,
                "is_local": True,
                "year": "Local",
                "authors": ["Local Upload"],
                "url": "Local File"
            })

    # 2. Online Search (if topic provided)
    if topic:
        print(f"Searching for topic: {topic}")
        # Adjust limit based on how many local files we have? 
        # For now, let's keep search independent but maybe reduce if we have many local files.
        limit = state.get('max_results', 3)
        online_papers = search_papers(topic, limit=limit)
        papers.extend(online_papers)
    else:
        print("No topic provided. Skipping online search.")

    return {"papers": papers}

def extraction_node(state: ResearchState):
    print("--- EXTRACTING TEXT (PARALLEL) ---")
    papers = state.get('papers', [])
    
    # Use concurrent processing
    extracted_papers = process_papers_concurrently(papers)
            
    return {"papers": extracted_papers}

def analysis_node(state: ResearchState):
    print("--- ANALYZING PAPERS (PARALLEL) ---")
    papers = state.get('papers', [])
    
    # Use concurrent analysis
    analyses = analyze_papers_concurrently(papers)
            
    # Synthesize
    synthesis = synthesize_findings(analyses)
    return {"analyses": analyses, "synthesis": synthesis}

def writing_node(state: ResearchState):
    print("--- WRITING DRAFT ---")
    synthesis = state.get('synthesis')
    papers = state.get('papers')
    
    abstract = write_review_section("Abstract", synthesis)
    methods = write_review_section("Methodology Comparison", synthesis)
    results = write_review_section("Results Synthesis", synthesis)
    refs = format_references(papers)
    
    draft = {
        "Abstract": abstract,
        "Methodology": methods,
        "Results": results,
        "References": refs
    }
    
    full_text = f"# Systematic Review\n\n## Abstract\n{abstract}\n\n## Methodology\n{methods}\n\n## Results\n{results}\n\n## References\n{refs}"
    
    return {"draft": draft, "final_review": full_text}

def critique_node(state: ResearchState):
    print("--- CRITIQUING ---")
    current_text = state.get('final_review')
    critique = critique_draft(current_text)
    return {"critique": critique, "revision_count": state.get('revision_count', 0) + 1}

def revision_node(state: ResearchState):
    print("--- REVISING ---")
    current_text = state.get('final_review')
    critique = state.get('critique')
    revised = revise_draft(current_text, critique)
    return {"final_review": revised}

def should_continue(state: ResearchState):
    # Simple logic: Revise at most once for this prototype
    if state.get('revision_count', 0) < 1:
        return "revise"
    return "end"

# Build Graph
workflow = StateGraph(ResearchState)

workflow.add_node("search", search_node)
workflow.add_node("extract", extraction_node)
workflow.add_node("analyze", analysis_node)
workflow.add_node("write", writing_node)
workflow.add_node("critique", critique_node)
workflow.add_node("revise", revision_node)

workflow.set_entry_point("search")

workflow.add_edge("search", "extract")
workflow.add_edge("extract", "analyze")
workflow.add_edge("analyze", "write")
workflow.add_edge("write", "critique")

workflow.add_conditional_edges(
    "critique",
    should_continue,
    {
        "revise": "revise",
        "end": END
    }
)

workflow.add_edge("revise", END)

app_graph = workflow.compile()

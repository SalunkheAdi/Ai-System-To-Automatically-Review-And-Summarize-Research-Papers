import os
from typing import List, Dict
from typing import List, Dict
from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def analyze_paper(paper_text: str, paper_title: str) -> str:
    """
    Analyzes a single paper's text to extract key findings, methodology, and results.
    """
    llm = get_llm(temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyze briefly."),
        ("user", "{text}")
    ])
    
    try:
        # Ultra-aggressive truncation for speed and credits
        safe_text = paper_text[:3000]
        formatted_prompt = prompt.invoke({"text": safe_text})
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        return f"Error: {e}"

def synthesize_findings(analyses: List[Dict[str, str]]) -> str:
    """
    Synthesizes analyses from multiple papers to find common themes and contrasts.
    """
    llm = get_llm(temperature=0)
    
    content_str = ""
    for item in analyses[:2]:  # Only top 2 papers
        content_str += f"{item['title']}: {item['analysis'][:200]}\n"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize."),
        ("user", "{content}")
    ])
    
    try:
        formatted_prompt = prompt.invoke({"content": content_str})
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        return f"Error: {e}"

import concurrent.futures

def analyze_single_paper_wrapper(paper):
    """
    Wrapper to call analyze_paper and return the result structure.
    """
    text = paper.get('full_text', '')
    title = paper.get('title', 'Unknown')
    if text:
        print(f"Analyzing {title[:30]}...")
        anim = analyze_paper(text, title)
        return {"title": title, "analysis": anim}
    return None

def analyze_papers_concurrently(papers):
    """
    Analyzes multiple papers in parallel.
    """
    analyses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(analyze_single_paper_wrapper, papers))
    
    # Filter out None results
    for r in results:
        if r:
            analyses.append(r)
            
    return analyses

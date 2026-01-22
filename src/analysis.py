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
        ("system", "You are an expert research assistant. Analyze the following research paper text."),
        ("user", "Title: {title}\n\nText:\n{text}\n\nPlease identify:\n1. Key Findings\n2. Methodology\n3. Results\n4. Limitations\n\nProvide a concise analysis.")
    ])
    
    try:
        # Truncate text if too long to fit context window
        safe_text = paper_text[:30000]
        # Format the prompt
        formatted_prompt = prompt.invoke({"title": paper_title, "text": safe_text})
        # Invoke LLM directly
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        return f"Error analyzing paper: {e}"

def synthesize_findings(analyses: List[Dict[str, str]]) -> str:
    """
    Synthesizes analyses from multiple papers to find common themes and contrasts.
    Input: List of dicts, each containing 'title' and 'analysis'.
    """
    llm = get_llm(temperature=0)
    
    start_str = "Synthesize the following research analyses into a cohesive summary of themes, agreements, and contradictions:\n\n"
    content_str = ""
    for item in analyses:
        content_str += f"--- Paper: {item['title']} ---\n{item['analysis']}\n\n"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior researcher conducting a systematic review."),
        ("user", "{intro}{content}")
    ])
    
    try:
        # Format the prompt
        formatted_prompt = prompt.invoke({"intro": start_str, "content": content_str})
        # Invoke LLM directly
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        return f"Error synthesizing findings: {e}"

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

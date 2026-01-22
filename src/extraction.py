import os
import requests
import pymupdf4llm
from typing import Dict, Optional

def download_pdf(url: str, output_path: str) -> bool:
    """Downloads a PDF from a URL to the specified path."""
    try:
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts markdown text from a PDF using pymupdf4llm."""
    try:
        # pymupdf4llm.to_markdown returns the full text in markdown format
        md_text = pymupdf4llm.to_markdown(pdf_path)
        return md_text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

# Placeholder for smarter segmentation if needed, 
# though pymupdf4llm's markdown is often structure-aware.
def segment_text(text: str) -> Dict[str, str]:
    """
    Naive segmentation of markdown text into standard research sections.
    Real-world usage might require an LLM or regex to robustly identify headers.
    For this prototype, we'll store the full text and let the LLM analyze it directly,
    or do simple keyword splitting.
    """
    # Simply returning full text as 'Full Content' for now to allow LLM to parse structure
    return {"Full Content": text}

import concurrent.futures

def process_single_paper(paper):
    """
    Helper function to process a single paper: download -> extract.
    Returns the modified paper dictionary.
    """
    # Check if it's a local file first
    if paper.get('is_local') and paper.get('pdf_path'):
        pdf_path = paper.get('pdf_path')
        if os.path.exists(pdf_path):
            print(f"Processing local file: {paper['title']}...")
            text = extract_text_from_pdf(pdf_path)
            paper['full_text'] = text
        else:
            print(f"Error: Local file not found: {pdf_path}")
        return paper

    # Online download logic
    if paper.get('pdf_url'):
        paper_id = paper.get('paperId') or "unknown"
        filename = f"temp_pdfs/{paper_id}.pdf"
        
        # Create temp dir if not exists (thread safe check usually needed, but os.makedirs(exist_ok=True) is fine)
        os.makedirs("temp_pdfs", exist_ok=True)
        
        print(f"Downloading {paper['title'][:30]}...")
        if download_pdf(paper['pdf_url'], filename):
            print(f"Extracting {paper['title'][:30]}...")
            text = extract_text_from_pdf(filename)
            paper['full_text'] = text
        else:
            print(f"Skipping {paper['title'][:30]} (Download failed)")
    else:
        print(f"Skipping {paper['title'][:30]} (No PDF URL)")
    return paper

def process_papers_concurrently(papers):
    """
    Downloads and extracts text for multiple papers in parallel.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Map the helper function to the papers
        results = list(executor.map(process_single_paper, papers))
    return results

if __name__ == "__main__":
    # Test
    # Assuming a sample PDF exists or is downloaded
    pass

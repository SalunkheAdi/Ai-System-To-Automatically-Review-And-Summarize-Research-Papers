from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def write_review_section(section_name: str, synthesis: str, context: str = "") -> str:
    """
    Generates a specific section of the review (e.g., Abstract, Methodology, Results) based on the synthesis.
    """
    llm = get_llm(temperature=0.3)
    
    LIMIT_INSTRUCTION = ""
    if "Abstract" in section_name:
        LIMIT_INSTRUCTION = " (Keep it under 100 words)"

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are writing the {section_name} section of a systematic review."),
        ("user", f"Based on the following synthesis of research papers, write a professional {{section_name}}{LIMIT_INSTRUCTION}.\n\nSynthesis:\n{{synthesis}}\n\n{{context}}")
    ])
    
    try:
        formatted_prompt = prompt.invoke({"section_name": section_name, "synthesis": synthesis, "context": context})
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        return f"Error writing {section_name}: {e}"

def format_references(papers: list) -> str:
    """
    Formats the list of papers into APA style references.
    """
    refs = []
    for p in papers:
        authors = ", ".join(p.get('authors', []))
        year = p.get('year', 'n.d.')
        title = p.get('title', 'Unknown Title')
        url = p.get('url', '')
        # Simple APA-like format
        refs.append(f"{authors} ({year}). {title}. Retrieved from {url}")
    return "\n\n".join(refs)

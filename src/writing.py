from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def write_review_section(section_name: str, synthesis: str, context: str = "") -> str:
    """
    Generates a specific section of the review.
    """
    llm = get_llm(temperature=0.3)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"Write {section_name}. Max 100 words."),
        ("user", "{content}")
    ])
    
    try:
        short_synthesis = synthesis[:800]
        formatted_prompt = prompt.invoke({"content": short_synthesis})
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

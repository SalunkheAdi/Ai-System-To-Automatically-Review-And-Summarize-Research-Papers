from llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def critique_draft(draft_text: str) -> str:
    """
    Critiques the generated draft review, identifying areas for improvement.
    """
    llm = get_llm(temperature=0.1)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a strict academic editor. Review the following draft."),
        ("user", "Draft:\n{draft}\n\nPlease provide critical feedback on clarity, coherence, and depth. List specific actionable improvements.")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        return chain.invoke({"draft": draft_text})
    except Exception as e:
        return "Critique failed."

def revise_draft(draft_text: str, critique: str) -> str:
    """
    Revises the draft based on the provided critique.
    """
    llm = get_llm(temperature=0.3)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an academic writer. Revise the draft based on the feedback."),
        ("user", "Draft:\n{draft}\n\nCritique:\n{critique}\n\nPlease rewrite the draft to address the critique while maintaining the original structure.")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        return chain.invoke({"draft": draft_text, "critique": critique})
    except Exception as e:
        return draft_text # Return original if revision fails

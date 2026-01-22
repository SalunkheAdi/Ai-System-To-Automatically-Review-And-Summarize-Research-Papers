import os
from langchain_openai import ChatOpenAI

def get_llm(temperature: float = 0.3):
    """
    Returns an LLM instance using OpenAI.
    Requires OPENAI_API_KEY to be set in the environment.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Warning: OPENAI_API_KEY not found in environment variables.")
        # We might want to raise an error or just let ChatOpenAI handle missing key (it will raise ValidationError)
    
    # Using gpt-4o-mini as requested
    print("Using OpenAI GPT-4o-mini model.")
    return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)

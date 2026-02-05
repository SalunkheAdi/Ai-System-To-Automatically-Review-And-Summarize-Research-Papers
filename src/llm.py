import os
from langchain_openai import ChatOpenAI

def get_llm(temperature: float = 0.3):
    """
    Returns an LLM instance using SambaNova API.
    Requires SAMBANOVA_API_KEY to be set in the environment.
    """
    sambanova_key = os.getenv("SAMBANOVA_API_KEY")
    if not sambanova_key:
        print("Warning: SAMBANOVA_API_KEY not found in environment variables.")
    
    # Using SambaNova API with Llama model
    print("Using SambaNova API.")
    return ChatOpenAI(
        model="Meta-Llama-3.1-8B-Instruct",
        api_key=sambanova_key,
        base_url="https://api.sambanova.ai/v1",
        temperature=temperature,
        max_tokens=500
    )


import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def test_gemini():
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        result = llm.invoke("Hello, are you working?")
        print(f"Response: {result.content}")
    except Exception as e:
        print(f"Error with gemini-2.0-flash: {e}")
        
    print("-" * 20)
    
    try:
        llm_safe = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        result = llm_safe.invoke("Hello, are you working?")
        print(f"Response (1.5-flash): {result.content}")
    except Exception as e:
        print(f"Error with gemini-1.5-flash: {e}")

if __name__ == "__main__":
    test_gemini()

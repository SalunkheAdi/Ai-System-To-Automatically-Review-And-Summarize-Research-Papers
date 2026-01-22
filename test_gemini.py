import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def test_gemini():
    print(f"Testing Gemini with Key: {os.getenv('GOOGLE_API_KEY')[:10]}...")
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        response = llm.invoke("Hello, are you working?")
        print(f"Success! Response: {response.content}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gemini()

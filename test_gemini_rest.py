import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def test_gemini_rest():
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"Testing Gemini API directly with key: {api_key[:10]}...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            model_names = [m['name'] for m in data.get('models', [])]
            
            check_list = ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.5-pro', 'models/gemini-2.0-flash']
            
            with open("verification_result.txt", "w") as f:
                f.write(f"Key Prefix: {api_key[:5]}...\n")
                if not model_names:
                     f.write("NO MODELS FOUND\n")
                else:
                    for target in check_list:
                        if target in model_names:
                            f.write(f"FOUND: {target}\n")
                        else:
                            f.write(f"MISSING: {target}\n")
                    f.write("\nAll Models:\n")
                    for m in model_names:
                        f.write(f"{m}\n")
        else:
            print(f"Error {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gemini_rest()

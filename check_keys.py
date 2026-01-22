
import os
from dotenv import load_dotenv

load_dotenv()

def check_keys():
    openai = os.getenv("OPENAI_API_KEY")
    google = os.getenv("GOOGLE_API_KEY")
    
    print(f"OPENAI_API_KEY present: {bool(openai)}")
    print(f"GOOGLE_API_KEY present: {bool(google)}")

if __name__ == "__main__":
    check_keys()

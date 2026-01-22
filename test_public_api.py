import requests
import json

def test_public_api():
    print("Testing direct public API call (no key)...")
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": "Agentic AI",
        "limit": 1,
        "fields": "title,url,year,citationCount"
    }
    # No headers, so no API key
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['total']} papers")
            if data.get('data'):
                print(json.dumps(data['data'][0], indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_public_api()

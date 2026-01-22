import requests
import json

def test_direct_api():
    print("Testing direct API call...")
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": "Agentic AI",
        "limit": 1,
        "fields": "title,url,abstract,year,authors,openAccessPdf"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['total']} papers")
            if data['data']:
                print(json.dumps(data['data'][0], indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_direct_api()

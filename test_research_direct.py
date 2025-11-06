#!/usr/bin/env python3
"""Direct test of research endpoint to capture exact error"""

import requests
import json
import sys

def test_research():
    url = "http://localhost:8080/research"
    payload = {
        "query": "machine learning",
        "max_papers": 1
    }
    
    try:
        print("Sending request...")
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status: {response.status_code}")
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response.text[:500]}")
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_research()
    sys.exit(0 if success else 1)


#!/usr/bin/env python3
"""
Comprehensive User Testing Script
Tests all API endpoints and checks for errors
"""

import requests
import json
import sys
from typing import Dict, Any

API_BASE = "http://localhost:8080"
WEB_UI = "http://localhost:8501"

def test_health_check() -> Dict[str, Any]:
    """Test health check endpoint"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        data = None
        error = None
        if response.status_code == 200:
            try:
                data = response.json()
            except (ValueError, json.JSONDecodeError) as e:
                data = None
                error = f"JSON decode error: {str(e)}"
        return {
            "status": "✅ PASS" if response.status_code == 200 else "❌ FAIL",
            "code": response.status_code,
            "data": data,
            "error": error
        }
    except Exception as e:
        return {"status": "❌ FAIL", "code": None, "data": None, "error": str(e)}

def test_api_docs() -> Dict[str, Any]:
    """Test API docs endpoint"""
    try:
        response = requests.get(f"{API_BASE}/docs", timeout=5)
        return {
            "status": "✅ PASS" if response.status_code == 200 else "❌ FAIL",
            "code": response.status_code,
            "error": None
        }
    except Exception as e:
        return {"status": "❌ FAIL", "code": None, "error": str(e)}

def test_web_ui() -> Dict[str, Any]:
    """Test Web UI accessibility"""
    try:
        response = requests.get(WEB_UI, timeout=5)
        return {
            "status": "✅ PASS" if response.status_code == 200 else "❌ FAIL",
            "code": response.status_code,
            "has_html": "<html" in response.text.lower(),
            "error": None
        }
    except Exception as e:
        return {"status": "❌ FAIL", "code": None, "error": str(e)}

def test_search_endpoint() -> Dict[str, Any]:
    """Test search endpoint with a simple query"""
    try:
        payload = {
            "query": "machine learning",
            "max_papers": 5
        }
        response = requests.post(
            f"{API_BASE}/research",
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        data = None
        error = None
        full_response = None
        
        # Try to parse JSON response
        try:
            parsed_json = response.json()
            if response.status_code in [200, 202]:
                data = parsed_json
            else:
                error = json.dumps(parsed_json)
                full_response = response.text[:500]
        except (ValueError, json.JSONDecodeError):
            # Fallback to raw text if JSON parsing fails
            raw_text = response.text[:500]
            if response.status_code in [200, 202]:
                data = {"raw_response": raw_text}
            else:
                error = f"Failed to parse JSON. Raw response: {raw_text}"
                full_response = raw_text
        
        return {
            "status": "✅ PASS" if response.status_code in [200, 202] else "❌ FAIL",
            "code": response.status_code,
            "data": data,
            "error": error,
            "full_response": full_response
        }
    except requests.exceptions.Timeout:
        return {"status": "⏳ TIMEOUT", "code": None, "error": "Request timed out"}
    except Exception as e:
        return {"status": "❌ FAIL", "code": None, "error": str(e)}

def main():
    print("=" * 60)
    print("🧪 Comprehensive User Testing")
    print("=" * 60)
    print()
    
    results = {}
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    results["health"] = test_health_check()
    print(f"   {results['health']['status']} - Status Code: {results['health']['code']}")
    if results['health']['data']:
        print(f"   Service Status: {results['health']['data'].get('status', 'unknown')}")
    print()
    
    # Test 2: API Docs
    print("2. Testing API Docs...")
    results["docs"] = test_api_docs()
    print(f"   {results['docs']['status']} - Status Code: {results['docs']['code']}")
    print()
    
    # Test 3: Web UI
    print("3. Testing Web UI...")
    results["web_ui"] = test_web_ui()
    print(f"   {results['web_ui']['status']} - Status Code: {results['web_ui']['code']}")
    if results['web_ui'].get('has_html'):
        print("   ✅ HTML content detected")
    print()
    
    # Test 4: Search Endpoint
    print("4. Testing Search Endpoint...")
    print("   (This may take 30+ seconds)")
    results["search"] = test_search_endpoint()
    print(f"   {results['search']['status']} - Status Code: {results['search']['code']}")
    if results['search'].get('error'):
        print(f"   Error: {results['search']['error'][:200]}")
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    passed = sum(1 for r in results.values() if "✅" in r.get("status", ""))
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print()
    
    # List failures
    failures = [k for k, v in results.items() if "❌" in v.get("status", "")]
    if failures:
        print("❌ Failed Tests:")
        for test in failures:
            print(f"   - {test}")
            if results[test].get("error"):
                print(f"     Error: {results[test]['error']}")
            if results[test].get("full_response"):
                print(f"     Full Response: {results[test]['full_response']}")
    else:
        print("✅ All tests passed!")
    
    return 0 if not failures else 1

if __name__ == "__main__":
    sys.exit(main())


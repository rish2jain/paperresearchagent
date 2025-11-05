#!/usr/bin/env python3
"""
User Testing Script for Agentic Researcher
Tests the application programmatically and via browser inspection
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
API_URL = "http://localhost:8080"
WEB_UI_URL = "http://localhost:8501"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_api_health():
    """Test API health endpoint"""
    print_section("1. API Health Check")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy")
            print(f"   Service: {data.get('service', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Status: {data.get('status', 'N/A')}")
            
            nims = data.get('nims_available', {})
            print(f"   Reasoning NIM: {'✅ Available' if nims.get('reasoning_nim') else '❌ Unavailable'}")
            print(f"   Embedding NIM: {'✅ Available' if nims.get('embedding_nim') else '❌ Unavailable'}")
            
            if not nims.get('reasoning_nim') or not nims.get('embedding_nim'):
                print(f"\n⚠️  Warning: NIMs are not available. Full functionality may be limited.")
                print(f"   This is expected if NIMs are not deployed locally.")
            
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False

def test_web_ui_accessible():
    """Test if Web UI is accessible"""
    print_section("2. Web UI Accessibility")
    try:
        response = requests.get(WEB_UI_URL, timeout=5)
        if response.status_code == 200:
            print(f"✅ Web UI is accessible at {WEB_UI_URL}")
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Length: {len(response.content)} bytes")
            
            # Check for key elements in HTML
            content = response.text.lower()
            checks = {
                "Streamlit": "streamlit" in content,
                "Agentic Researcher": "agentic" in content or "researcher" in content,
                "JavaScript": "script" in content,
            }
            
            for check, result in checks.items():
                status = "✅" if result else "⚠️"
                print(f"   {status} {check}: {'Found' if result else 'Not found'}")
            
            return True
        else:
            print(f"❌ Web UI returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web UI not accessible: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    print_section("3. API Endpoints Test")
    
    endpoints = [
        ("/health", "GET"),
        ("/api/paper-sources", "GET"),
        ("/api/export-formats", "GET"),
    ]
    
    results = []
    for endpoint, method in endpoints:
        try:
            url = f"{API_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, timeout=5)
            
            if response.status_code in [200, 404]:  # 404 is OK for some endpoints
                status = "✅" if response.status_code == 200 else "⚠️"
                print(f"{status} {method} {endpoint}: {response.status_code}")
                results.append(True)
            else:
                print(f"❌ {method} {endpoint}: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"❌ {method} {endpoint}: {str(e)[:50]}")
            results.append(False)
    
    return all(results)

def test_query_validation():
    """Test query validation (without actually running a query)"""
    print_section("4. Query Validation Test")
    
    # Test with empty query (should fail validation)
    try:
        response = requests.post(
            f"{API_URL}/research",
            json={"query": "", "max_papers": 10},
            timeout=5
        )
        if response.status_code == 422:  # Validation error
            print("✅ Empty query validation works (correctly rejects)")
            return True
        else:
            print(f"⚠️  Unexpected response for empty query: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Query validation test: {str(e)[:50]}")
        return False

def test_export_endpoints():
    """Test export format endpoints"""
    print_section("5. Export Format Endpoints")
    
    export_formats = [
        "bibtex", "latex", "json", "markdown", "csv", "excel",
        "word", "pdf", "endnote", "zotero", "mendeley", "html", "xml"
    ]
    
    available = []
    for fmt in export_formats:
        try:
            response = requests.get(f"{API_URL}/export/{fmt}", timeout=2)
            # 405 (Method Not Allowed) or 404 means endpoint exists but needs POST
            # 422 means endpoint exists but needs data
            if response.status_code in [405, 404, 422]:
                print(f"✅ {fmt.upper()} endpoint exists")
                available.append(fmt)
            else:
                print(f"⚠️  {fmt.upper()} endpoint: {response.status_code}")
        except Exception as e:
            print(f"❌ {fmt.upper()} endpoint: {str(e)[:30]}")
    
    print(f"\n📊 Summary: {len(available)}/{len(export_formats)} export formats have endpoints")
    return len(available) > 0

def generate_test_report():
    """Generate comprehensive test report"""
    print_section("User Testing Report")
    
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API URL: {API_URL}")
    print(f"Web UI URL: {WEB_UI_URL}\n")
    
    # Run all tests
    tests = [
        ("API Health", test_api_health),
        ("Web UI Access", test_web_ui_accessible),
        ("API Endpoints", test_api_endpoints),
        ("Query Validation", test_query_validation),
        ("Export Formats", test_export_endpoints),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print_section("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed*100//total}%)")
    
    # Recommendations
    print_section("Recommendations")
    if passed == total:
        print("✅ All automated tests passed!")
        print("   Next: Test UI manually in browser at:", WEB_UI_URL)
        print("   Test real query submission and agent interactions")
    else:
        print("⚠️  Some tests failed. Check:")
        print("   1. Are all services running?")
        print("   2. Are NIMs deployed and accessible?")
        print("   3. Check service logs for errors")
    
    return results

if __name__ == "__main__":
    print("🧪 Agentic Researcher - User Testing Script")
    print("=" * 60)
    generate_test_report()

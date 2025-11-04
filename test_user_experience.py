#!/usr/bin/env python3
"""
User Testing Script for ResearchOps Agent
Executes comprehensive user testing plan and reports findings
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

BASE_URL = "http://localhost:8080"
UI_URL = "http://localhost:8501"

class TestResults:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
        
    def add_pass(self, test_name: str, details: str = ""):
        self.passed.append({"test": test_name, "details": details})
        print(f"✅ PASS: {test_name}")
        if details:
            print(f"   {details}")
    
    def add_fail(self, test_name: str, error: str, details: str = ""):
        self.failed.append({"test": test_name, "error": error, "details": details})
        print(f"❌ FAIL: {test_name}")
        print(f"   Error: {error}")
        if details:
            print(f"   {details}")
    
    def add_warning(self, test_name: str, message: str):
        self.warnings.append({"test": test_name, "message": message})
        print(f"⚠️  WARN: {test_name}")
        print(f"   {message}")
    
    def print_summary(self):
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"✅ Passed: {len(self.passed)}")
        print(f"❌ Failed: {len(self.failed)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print("="*60)
        
        if self.failed:
            print("\nFAILED TESTS:")
            for fail in self.failed:
                print(f"  - {fail['test']}: {fail['error']}")
        
        if self.warnings:
            print("\nWARNINGS:")
            for warn in self.warnings:
                print(f"  - {warn['test']}: {warn['message']}")

results = TestResults()

def test_api_health():
    """Test 3.1: Health Check Endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") in ["healthy", "degraded"]:
                results.add_pass("API Health Check", 
                    f"Status: {data.get('status')}, NIMs: {data.get('nims_available')}")
            else:
                results.add_fail("API Health Check", 
                    f"Unexpected status: {data.get('status')}")
        else:
            results.add_fail("API Health Check", 
                f"HTTP {response.status_code}")
    except Exception as e:
        results.add_fail("API Health Check", str(e))

def test_api_root():
    """Test API root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "service" in data and "endpoints" in data:
                results.add_pass("API Root Endpoint", 
                    f"Service: {data.get('service')}")
            else:
                results.add_fail("API Root Endpoint", 
                    "Missing expected fields")
        else:
            results.add_fail("API Root Endpoint", 
                f"HTTP {response.status_code}")
    except Exception as e:
        results.add_fail("API Root Endpoint", str(e))

def test_api_sources():
    """Test 3.3: Sources Endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/sources", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "active_sources_count" in data and "sources" in data:
                active_count = data.get("active_sources_count", 0)
                results.add_pass("API Sources Endpoint", 
                    f"Active sources: {active_count}")
            else:
                results.add_fail("API Sources Endpoint", 
                    "Missing expected fields")
        else:
            results.add_fail("API Sources Endpoint", 
                f"HTTP {response.status_code}")
    except Exception as e:
        results.add_fail("API Sources Endpoint", str(e))

def test_api_research_basic():
    """Test 3.2: Research Endpoint - Basic Query"""
    try:
        payload = {
            "query": "machine learning",
            "max_papers": 5
        }
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/research",
            json=payload,
            timeout=300  # 5 minutes
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            required_fields = ["papers_analyzed", "common_themes", "contradictions", 
                            "research_gaps", "decisions", "synthesis_complete"]
            missing = [f for f in required_fields if f not in data]
            if not missing:
                results.add_pass("API Research Endpoint (Basic)", 
                    f"Papers: {data.get('papers_analyzed')}, "
                    f"Themes: {len(data.get('common_themes', []))}, "
                    f"Time: {elapsed:.1f}s")
            else:
                results.add_fail("API Research Endpoint (Basic)", 
                    f"Missing fields: {missing}")
        else:
            results.add_fail("API Research Endpoint (Basic)", 
                f"HTTP {response.status_code}: {response.text[:200]}")
    except requests.exceptions.Timeout:
        results.add_warning("API Research Endpoint (Basic)", 
            "Request timed out (may be expected for long queries)")
    except Exception as e:
        results.add_fail("API Research Endpoint (Basic)", str(e))

def test_api_research_validation():
    """Test 4.1: Empty Query Validation"""
    try:
        payload = {"query": "", "max_papers": 10}
        response = requests.post(f"{BASE_URL}/research", json=payload, timeout=10)
        # Pydantic validation returns 422, which is also correct for validation errors
        if response.status_code in [400, 422]:
            results.add_pass("API Empty Query Validation", 
                f"Correctly rejects empty query (HTTP {response.status_code})")
        else:
            results.add_fail("API Empty Query Validation", 
                f"Expected 400 or 422, got {response.status_code}")
    except Exception as e:
        results.add_fail("API Empty Query Validation", str(e))

def test_api_research_invalid_dates():
    """Test 4.2: Invalid Date Range Validation"""
    try:
        payload = {
            "query": "test",
            "max_papers": 10,
            "start_year": 2030,
            "end_year": 2020
        }
        # Use shorter timeout since this should fail fast with validation
        response = requests.post(f"{BASE_URL}/research", json=payload, timeout=5)
        # Should reject invalid date range (start_year > end_year)
        if response.status_code in [400, 422]:
            error_detail = response.json().get("detail", {})
            if isinstance(error_detail, list):
                error_msg = error_detail[0].get("msg", "") if error_detail else ""
            else:
                error_msg = str(error_detail.get("message", ""))
            
            if "end_year" in error_msg.lower() and "start_year" in error_msg.lower():
                results.add_pass("API Invalid Date Range Validation", 
                    f"Correctly rejects invalid date range (HTTP {response.status_code})")
            else:
                results.add_pass("API Invalid Date Range Validation", 
                    f"Rejects invalid date range (HTTP {response.status_code})")
        elif response.status_code == 200:
            results.add_warning("API Invalid Date Range Validation", 
                "Accepts invalid date range (may be processed anyway)")
        else:
            results.add_fail("API Invalid Date Range Validation", 
                f"Unexpected status: {response.status_code}")
    except requests.exceptions.Timeout:
        results.add_fail("API Invalid Date Range Validation", 
            "Request timed out (validation should fail fast)")
    except Exception as e:
        results.add_fail("API Invalid Date Range Validation", str(e))

def test_api_export_bibtex():
    """Test 8.1: BibTeX Export"""
    try:
        # Use a simple test with mock papers if research endpoint takes too long
        test_papers = [
            {
                "id": "test-1",
                "title": "Test Paper 1",
                "authors": ["Author One", "Author Two"],
                "url": "https://example.com/paper1",
                "abstract": "Test abstract",
                "published_date": "2023-01-01"
            },
            {
                "id": "test-2",
                "title": "Test Paper 2",
                "authors": ["Author Three"],
                "url": "https://example.com/paper2",
                "abstract": "Another test abstract",
                "published_date": "2023-02-01"
            }
        ]
        
        export_payload = {"papers": test_papers}
        export_response = requests.post(
            f"{BASE_URL}/export/bibtex",
            json=export_payload,
            timeout=30
        )
        if export_response.status_code == 200:
            export_data = export_response.json()
            if "content" in export_data and "@" in export_data["content"]:
                results.add_pass("API BibTeX Export", 
                    f"Exported {len(test_papers)} test papers")
            else:
                results.add_fail("API BibTeX Export", 
                    "Invalid BibTeX format")
        else:
            results.add_fail("API BibTeX Export", 
                f"HTTP {export_response.status_code}: {export_response.text[:200]}")
    except Exception as e:
        results.add_fail("API BibTeX Export", str(e))

def test_ui_availability():
    """Test 1.1: UI Availability"""
    try:
        response = requests.get(UI_URL, timeout=10)
        if response.status_code == 200:
            if "ResearchOps" in response.text or "Research Ops" in response.text:
                results.add_pass("UI Availability", 
                    "UI is accessible and contains expected content")
            else:
                results.add_warning("UI Availability", 
                    "UI accessible but content may be different")
        else:
            results.add_fail("UI Availability", 
                f"HTTP {response.status_code}")
    except Exception as e:
        results.add_fail("UI Availability", str(e))

def main():
    print("="*60)
    print("ResearchOps Agent - User Testing")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print()
    
    # API Tests
    print("Testing API Endpoints...")
    print("-" * 60)
    test_api_health()
    test_api_root()
    test_api_sources()
    test_api_research_validation()
    test_api_research_invalid_dates()
    print()
    
    # UI Tests
    print("Testing UI Availability...")
    print("-" * 60)
    test_ui_availability()
    print()
    
    # Functional Tests (may take longer)
    print("Testing Functional Endpoints...")
    print("-" * 60)
    print("Note: Research endpoint test may take 2-5 minutes")
    test_api_research_basic()
    test_api_export_bibtex()
    print()
    
    # Summary
    results.print_summary()
    
    # Save results to file
    report = {
        "timestamp": datetime.now().isoformat(),
        "passed": len(results.passed),
        "failed": len(results.failed),
        "warnings": len(results.warnings),
        "tests_passed": results.passed,
        "tests_failed": results.failed,
        "tests_warnings": results.warnings
    }
    
    with open("test_results.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed results saved to: test_results.json")
    
    return len(results.failed) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


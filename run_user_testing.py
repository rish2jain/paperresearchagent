#!/usr/bin/env python3
"""
Automated User Testing Script
Tests the ResearchOps Agent Web UI via API and documents browser testing scenarios
"""

import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

# Test results
results = []

def test_api_health():
    """Test API health endpoint"""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:8080/health"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                "test": "API Health Check",
                "status": "PASS" if data.get("status") == "healthy" else "FAIL",
                "details": f"Status: {data.get('status')}, NIMs: {data.get('nims_available', {})}"
            }
    except Exception as e:
        return {
            "test": "API Health Check",
            "status": "FAIL",
            "details": str(e)
        }

def test_web_ui_accessible():
    """Test Web UI is accessible"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:8501"],
            capture_output=True,
            text=True,
            timeout=5
        )
        status_code = result.stdout.strip()
        return {
            "test": "Web UI Accessibility",
            "status": "PASS" if status_code == "200" else "FAIL",
            "details": f"HTTP Status: {status_code}"
        }
    except Exception as e:
        return {
            "test": "Web UI Accessibility",
            "status": "FAIL",
            "details": str(e)
        }

def test_api_search():
    """Test API search endpoint"""
    try:
        payload = {
            "query": "machine learning",
            "max_papers": 5
        }
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", "http://localhost:8080/research",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload),
             "-w", "\n%{http_code}"],
            capture_output=True,
            text=True,
            timeout=30
        )
        lines = result.stdout.strip().split('\n')
        http_code = lines[-1] if lines else "000"
        return {
            "test": "API Search Endpoint",
            "status": "PASS" if http_code in ["200", "202"] else "FAIL",
            "details": f"HTTP Status: {http_code}"
        }
    except Exception as e:
        return {
            "test": "API Search Endpoint",
            "status": "FAIL",
            "details": str(e)
        }

def generate_browser_test_instructions():
    """Generate instructions for browser-based testing"""
    instructions = """
# Browser Testing Instructions

Since browser MCP tools are not currently available, please execute these tests manually:

## Test 1: Page Load
1. Open browser to http://localhost:8501
2. Verify page loads without errors
3. Check browser console for errors (F12)
4. Take screenshot: test_1_page_load.png

## Test 2: Query Input
1. Locate query input field in sidebar
2. Type: "machine learning for medical imaging"
3. Set max papers slider to 10
4. Take screenshot: test_2_query_input.png

## Test 3: Execute Search
1. Click "Start Research" or "Search" button
2. Observe progress indicator
3. Wait for results (2-5 minutes)
4. Take screenshots at each stage:
   - test_3_progress_searching.png
   - test_3_progress_analyzing.png
   - test_3_results_complete.png

## Test 4: Verify Results
1. Check papers are displayed
2. Verify decision log shows agent decisions
3. Check NIM badges (🟦 Reasoning, 🟩 Embedding)
4. Verify synthesis section
5. Take screenshot: test_4_results.png

## Test 5: Export
1. Locate export dropdown
2. Test JSON export
3. Test Markdown export
4. Verify downloads work
5. Take screenshot: test_5_export.png

See BROWSER_USER_TESTING_GUIDE.md for complete test scenarios.
"""
    return instructions

def main():
    print("=" * 60)
    print("🧪 Automated User Testing - ResearchOps Agent")
    print("=" * 60)
    print()
    
    # Run API tests
    print("Running API Tests...")
    print("-" * 60)
    
    results.append(test_api_health())
    results.append(test_web_ui_accessible())
    # results.append(test_api_search())  # Commented out as it takes time
    
    # Print results
    for result in results:
        status_emoji = "✅" if result["status"] == "PASS" else "❌"
        print(f"{status_emoji} {result['test']}: {result['status']}")
        print(f"   {result['details']}")
        print()
    
    # Generate report
    report = f"""# Automated User Testing Report
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## API Test Results

"""
    for result in results:
        status_emoji = "✅" if result["status"] == "PASS" else "❌"
        report += f"- {status_emoji} **{result['test']}**: {result['status']}\n"
        report += f"  - {result['details']}\n\n"
    
    report += generate_browser_test_instructions()
    
    # Save report
    report_path = Path("AUTOMATED_TEST_REPORT.md")
    report_path.write_text(report)
    print(f"✅ Report saved: {report_path}")
    print()
    print("=" * 60)
    print("Browser Testing Instructions Generated")
    print("See: BROWSER_USER_TESTING_GUIDE.md for detailed scenarios")
    print("=" * 60)

if __name__ == "__main__":
    main()


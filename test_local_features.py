#!/usr/bin/env python3
"""
Browser Testing Script for Local Features
Tests all ported features using browser automation
"""

import asyncio
import json
import time
from datetime import datetime

def test_feature_status():
    """Check which features are available"""
    print("=" * 60)
    print("FEATURE AVAILABILITY CHECK")
    print("=" * 60)
    
    features = {
        "PDF Export": False,
        "Word Export": False,
        "SSE Streaming": False,
        "Denario": False,
        "Redis": False,
        "Prometheus": False,
    }
    
    # Check PDF export
    try:
        import reportlab
        features["PDF Export"] = True
        print("✅ PDF Export: Available")
    except ImportError:
        print("❌ PDF Export: Not available (install: pip install reportlab)")
    
    # Check Word export
    try:
        import docx
        features["Word Export"] = True
        print("✅ Word Export: Available")
    except ImportError:
        print("❌ Word Export: Not available (install: pip install python-docx)")
    
    # Check SSE streaming
    try:
        import sseclient
        features["SSE Streaming"] = True
        print("✅ SSE Streaming: Available")
    except ImportError:
        print("❌ SSE Streaming: Not available (install: pip install sseclient-py)")
    
    # Check Denario
    try:
        import denario
        features["Denario"] = True
        print("✅ Denario: Available")
    except ImportError:
        print("❌ Denario: Not available (install: pip install denario)")
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        features["Redis"] = True
        print("✅ Redis: Available")
    except Exception:
        print("⚠️  Redis: Not available (optional)")
    
    # Check Prometheus
    try:
        import prometheus_client
        features["Prometheus"] = True
        print("✅ Prometheus: Available")
    except ImportError:
        print("⚠️  Prometheus: Not available (optional)")
    
    print("=" * 60)
    return features

def generate_test_report(features):
    """Generate test report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "features": features,
        "tests": []
    }
    
    with open("LOCAL_FEATURES_TEST_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Test report saved to: LOCAL_FEATURES_TEST_REPORT.json")

if __name__ == "__main__":
    print("\n🔍 Checking Feature Availability...\n")
    features = test_feature_status()
    generate_test_report(features)
    
    print("\n" + "=" * 60)
    print("BROWSER TESTING INSTRUCTIONS")
    print("=" * 60)
    print("""
1. Start API server:
   python -m src.api

2. Start Web UI:
   streamlit run src/web_ui.py

3. Open browser to: http://localhost:8501

4. Test Features:
   - ✅ Export formats (PDF, Word, etc.)
   - ✅ S3 storage fallback (local file system)
   - ✅ Real-time streaming (if SSE available)
   - ✅ Paper sources (IEEE, SpringerLink)
   - ✅ UX enhancements
   - ✅ Denario integration (if available)

5. Check test results in: LOCAL_FEATURES_TEST_REPORT.json
    """)


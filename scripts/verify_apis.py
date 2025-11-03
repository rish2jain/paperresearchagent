#!/usr/bin/env python3
"""
Verify API Configuration
Checks which paper source APIs are configured and enabled
"""

import os
import sys
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import PaperSourceConfig


def check_source_status(config: PaperSourceConfig) -> Dict[str, Any]:
    """Check status of all paper sources"""
    status = {
        "free_sources": {},
        "subscription_sources": {},
        "summary": {
            "total_enabled": 0,
            "total_available": 7,
            "api_keys_configured": 0,
            "api_keys_needed": 0
        }
    }
    
    # Check free sources
    free_sources = {
        "arxiv": (config.enable_arxiv, False, "Free, no key required"),
        "pubmed": (config.enable_pubmed, False, "Free, no key required"),
        "semantic_scholar": (config.enable_semantic_scholar, bool(config.semantic_scholar_api_key), "Free, optional key for higher limits"),
        "crossref": (config.enable_crossref, False, "Free, no key required")
    }
    
    for name, (enabled, has_key, note) in free_sources.items():
        status["free_sources"][name] = {
            "enabled": enabled,
            "api_key_required": False,
            "api_key_configured": has_key,
            "status": "✅ Active" if enabled else "❌ Disabled",
            "note": note
        }
        if enabled:
            status["summary"]["total_enabled"] += 1
    
    # Check subscription sources
    sub_sources = {
        "ieee": (config.enable_ieee, bool(config.ieee_api_key), config.ieee_api_key, "https://developer.ieee.org/"),
        "acm": (config.enable_acm, bool(config.acm_api_key), config.acm_api_key, "Requires institutional access"),
        "springer": (config.enable_springer, bool(config.springer_api_key), config.springer_api_key, "https://dev.springernature.com/")
    }
    
    for name, (enabled, has_key, api_key, signup_url) in sub_sources.items():
        if enabled and has_key:
            status_msg = "✅ Active"
            status["summary"]["api_keys_configured"] += 1
            status["summary"]["total_enabled"] += 1
        elif enabled and not has_key:
            status_msg = "⚠️ Enabled but missing API key"
            status["summary"]["api_keys_needed"] += 1
        else:
            status_msg = "❌ Disabled"
        
        status["subscription_sources"][name] = {
            "enabled": enabled,
            "api_key_required": True,
            "api_key_configured": has_key,
            "api_key_set": "Yes" if has_key else "No",
            "status": status_msg,
            "signup_url": signup_url if not has_key else None
        }
    
    return status


def print_status_report(status: Dict[str, Any]):
    """Print a formatted status report"""
    print("\n" + "="*70)
    print("📚 Paper Source API Status Report")
    print("="*70 + "\n")
    
    print("FREE SOURCES (No API Key Required):")
    print("-" * 70)
    for name, info in status["free_sources"].items():
        print(f"  {info['status']:15} {name.upper():20} - {info['note']}")
    print()
    
    print("SUBSCRIPTION SOURCES (Require API Keys):")
    print("-" * 70)
    for name, info in status["subscription_sources"].items():
        print(f"  {info['status']:30} {name.upper():10}")
        if info.get("signup_url"):
            print(f"    └─ Get API key: {info['signup_url']}")
    print()
    
    summary = status["summary"]
    print("SUMMARY:")
    print("-" * 70)
    print(f"  Total Sources Enabled:     {summary['total_enabled']}/{summary['total_available']}")
    print(f"  API Keys Configured:       {summary['api_keys_configured']}/3")
    print(f"  API Keys Still Needed:     {summary['api_keys_needed']}/3")
    print()
    
    # Recommendations
    if summary['total_enabled'] >= 4:
        print("✅ SUCCESS: At least 4 sources enabled (free sources working)")
    else:
        print("⚠️  WARNING: Fewer than 4 sources enabled")
    
    if summary['api_keys_configured'] == 3:
        print("✅ SUCCESS: All subscription sources configured!")
    elif summary['api_keys_configured'] > 0:
        print(f"ℹ️  INFO: {summary['api_keys_configured']} subscription source(s) active")
    
    if summary['api_keys_needed'] > 0:
        print(f"⚠️  NOTE: {summary['api_keys_needed']} source(s) enabled but missing API keys")
    
    print("\n" + "="*70)


def main():
    """Main verification function"""
    print("Checking API configuration...")
    
    # Load configuration
    config = PaperSourceConfig.from_env()
    
    # Check status
    status = check_source_status(config)
    
    # Print report
    print_status_report(status)
    
    # Return exit code based on status
    if status["summary"]["total_enabled"] >= 4:
        return 0  # Success
    else:
        return 1  # Warning


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)


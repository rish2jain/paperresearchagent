"""
Test ResultCache functionality without requiring full Streamlit app.
"""
import sys
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional


class MockSessionState:
    """Mock Streamlit session state for testing."""
    def __init__(self):
        self._state = {}

    def __contains__(self, key):
        return key in self._state

    def __getitem__(self, key):
        return self._state[key]

    def __setitem__(self, key, value):
        self._state[key] = value


# Mock streamlit module
class MockStreamlit:
    session_state = MockSessionState()


sys.modules['streamlit'] = MockStreamlit()
import streamlit as st


class ResultCache:
    """
    Cache research results to dramatically speed up repeat queries.
    Uses MD5 hash of query parameters as cache key.
    """

    @classmethod
    def _generate_cache_key(cls, query: str, max_papers: int,
                          paper_sources: str, date_range: str) -> str:
        """Generate unique cache key from query parameters."""
        cache_string = f"{query}_{max_papers}_{paper_sources}_{date_range}"
        return hashlib.md5(cache_string.encode()).hexdigest()

    @classmethod
    def get(cls, query: str, max_papers: int,
            paper_sources: str, date_range: str) -> Optional[Dict]:
        """
        Retrieve cached results if available.

        Returns:
            Cached results dict or None if cache miss
        """
        cache_key = cls._generate_cache_key(query, max_papers, paper_sources, date_range)

        # Check session state cache first (instant lookup)
        if "result_cache" not in st.session_state:
            st.session_state["result_cache"] = {}

        if cache_key in st.session_state["result_cache"]:
            cached_data = st.session_state["result_cache"][cache_key]

            # Check if cache is still valid (TTL: 1 hour)
            cache_time = cached_data.get("cached_at", datetime.now())
            if isinstance(cache_time, str):
                cache_time = datetime.fromisoformat(cache_time)

            age_hours = (datetime.now() - cache_time).total_seconds() / 3600

            if age_hours < 1:  # Cache valid for 1 hour
                print(f"✅ Cache HIT for query: {query[:50]}... (age: {age_hours:.1f}h)")
                return cached_data["results"]
            else:
                # Cache expired, remove it
                print(f"⏰ Cache EXPIRED for query: {query[:50]}... (age: {age_hours:.1f}h)")
                del st.session_state["result_cache"][cache_key]

        print(f"❌ Cache MISS for query: {query[:50]}...")
        return None

    @classmethod
    def set(cls, query: str, max_papers: int,
            paper_sources: str, date_range: str, results: Dict):
        """Store results in cache with timestamp."""
        cache_key = cls._generate_cache_key(query, max_papers, paper_sources, date_range)

        if "result_cache" not in st.session_state:
            st.session_state["result_cache"] = {}

        st.session_state["result_cache"][cache_key] = {
            "results": results,
            "cached_at": datetime.now(),
            "query": query[:100]  # Store first 100 chars for debugging
        }

        print(f"💾 Cache SET for query: {query[:50]}...")

    @classmethod
    def clear(cls):
        """Clear all cached results."""
        if "result_cache" in st.session_state:
            cache_size = len(st.session_state["result_cache"])
            st.session_state["result_cache"] = {}
            print(f"🗑️ Cache CLEARED: {cache_size} entries removed")
            return cache_size
        return 0

    @classmethod
    def get_stats(cls) -> Dict:
        """Get cache statistics."""
        if "result_cache" not in st.session_state:
            return {"entries": 0, "size_kb": 0}

        cache = st.session_state["result_cache"]
        size_bytes = sys.getsizeof(cache)

        return {
            "entries": len(cache),
            "size_kb": size_bytes / 1024,
            "keys": list(cache.keys())
        }


def test_cache_operations():
    """Test cache set, get, and expiration logic."""
    print("\n🧪 Testing ResultCache Operations\n")

    # Test 1: Cache miss on first query
    print("Test 1: Cache miss on first access")
    result = ResultCache.get("AI research papers", 10, "arxiv,pubmed", "2020-2024")
    assert result is None, "Expected cache miss"
    print("✅ PASS: Cache miss correctly returned None\n")

    # Test 2: Cache set and hit
    print("Test 2: Cache set and immediate hit")
    test_results = {"papers": [{"title": "Test Paper", "doi": "10.1234/test"}]}
    ResultCache.set("AI research papers", 10, "arxiv,pubmed", "2020-2024", test_results)

    cached = ResultCache.get("AI research papers", 10, "arxiv,pubmed", "2020-2024")
    assert cached == test_results, "Expected cache hit with correct data"
    print("✅ PASS: Cache hit returned correct data\n")

    # Test 3: Cache key differentiation
    print("Test 3: Different parameters create different cache keys")
    result_different_sources = ResultCache.get("AI research papers", 10, "arxiv", "2020-2024")
    assert result_different_sources is None, "Expected cache miss for different sources"
    print("✅ PASS: Different parameters correctly miss cache\n")

    # Test 4: Cache statistics
    print("Test 4: Cache statistics")
    stats = ResultCache.get_stats()
    assert stats["entries"] == 1, f"Expected 1 cache entry, got {stats['entries']}"
    print(f"✅ PASS: Cache stats correct: {stats}\n")

    # Test 5: Cache expiration (simulated)
    print("Test 5: Cache expiration")
    # Manually set expired timestamp
    cache_key = ResultCache._generate_cache_key("old query", 5, "all", "all")
    st.session_state["result_cache"][cache_key] = {
        "results": {"old": "data"},
        "cached_at": datetime.now() - timedelta(hours=2),  # 2 hours old
        "query": "old query"
    }

    expired_result = ResultCache.get("old query", 5, "all", "all")
    assert expired_result is None, "Expected None for expired cache"
    print("✅ PASS: Expired cache correctly removed\n")

    # Test 6: Cache clear
    print("Test 6: Cache clear")
    cleared_count = ResultCache.clear()
    assert cleared_count == 1, f"Expected 1 entry cleared, got {cleared_count}"

    stats_after_clear = ResultCache.get_stats()
    assert stats_after_clear["entries"] == 0, "Expected 0 entries after clear"
    print("✅ PASS: Cache cleared successfully\n")

    # Test 7: Cache key generation consistency
    print("Test 7: Cache key generation consistency")
    key1 = ResultCache._generate_cache_key("test", 10, "arxiv", "2020-2024")
    key2 = ResultCache._generate_cache_key("test", 10, "arxiv", "2020-2024")
    assert key1 == key2, "Expected identical keys for identical parameters"

    key3 = ResultCache._generate_cache_key("test", 11, "arxiv", "2020-2024")
    assert key1 != key3, "Expected different keys for different parameters"
    print("✅ PASS: Cache key generation is consistent\n")

    print("🎉 All cache tests passed!")


if __name__ == "__main__":
    test_cache_operations()

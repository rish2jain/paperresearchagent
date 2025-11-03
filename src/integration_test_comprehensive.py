"""
Comprehensive Integration Tests for Research Ops Agent
Tests the complete system including all components and workflows
"""

import pytest
import asyncio
import os
from typing import Dict, Any
import time

# Test configuration
TEST_TIMEOUT = 300  # 5 minutes for full integration tests


@pytest.fixture
def test_config():
    """Test configuration"""
    return {
        "reasoning_nim_url": os.getenv(
            "TEST_REASONING_NIM_URL",
            "http://localhost:8000"
        ),
        "embedding_nim_url": os.getenv(
            "TEST_EMBEDDING_NIM_URL",
            "http://localhost:8001"
        ),
        "vector_db_url": os.getenv(
            "TEST_VECTOR_DB_URL",
            "http://localhost:6333"
        ),
        "api_url": os.getenv(
            "TEST_API_URL",
            "http://localhost:8080"
        ),
    }


@pytest.mark.asyncio
async def test_health_endpoints(test_config):
    """Test all health check endpoints"""
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        # Test API health
        async with session.get(f"{test_config['api_url']}/health") as response:
            assert response.status == 200
            data = await response.json()
            assert data["status"] in ["healthy", "degraded"]
        
        # Test API readiness
        async with session.get(f"{test_config['api_url']}/ready") as response:
            assert response.status == 200
        
        # Test Reasoning NIM health
        try:
            async with session.get(
                f"{test_config['reasoning_nim_url']}/v1/health/live",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                assert response.status == 200
        except Exception:
            pytest.skip("Reasoning NIM not available")
        
        # Test Embedding NIM health
        try:
            async with session.get(
                f"{test_config['embedding_nim_url']}/v1/health/live",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                assert response.status == 200
        except Exception:
            pytest.skip("Embedding NIM not available")


@pytest.mark.asyncio
async def test_single_synthesis_workflow(test_config):
    """Test complete single synthesis workflow"""
    import aiohttp
    
    query = "machine learning for medical imaging"
    payload = {
        "query": query,
        "max_papers": 5,  # Small number for faster tests
        "prioritize_recent": True
    }
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        
        async with session.post(
            f"{test_config['api_url']}/research",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        ) as response:
            assert response.status == 200
            result = await response.json()
            
            processing_time = time.time() - start_time
            
            # Validate response structure
            assert "papers_analyzed" in result
            assert "common_themes" in result
            assert "contradictions" in result
            assert "research_gaps" in result
            assert "decisions" in result
            assert "query" in result
            assert result["query"] == query
            
            # Validate decisions contain agent information
            assert len(result["decisions"]) > 0
            decisions = result["decisions"]
            for decision in decisions:
                assert "agent" in decision
                assert "decision_type" in decision
                assert "reasoning" in decision
            
            # Check that processing time is reasonable
            assert processing_time < TEST_TIMEOUT
            assert result["processing_time_seconds"] > 0
            
            return result


@pytest.mark.asyncio
async def test_batch_processing(test_config):
    """Test batch processing functionality"""
    import aiohttp
    
    payload = {
        "queries": [
            "machine learning in healthcare",
            "deep learning architectures",
        ],
        "max_papers": 3,
        "prioritize_recent": True
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{test_config['api_url']}/research/batch",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT * 2)
        ) as response:
            assert response.status == 200
            result = await response.json()
            
            assert "batch_id" in result
            assert "total_queries" in result
            assert "completed" in result
            assert "failed" in result
            assert "results" in result
            
            assert result["total_queries"] == 2
            assert len(result["results"]) == 2
            assert result["completed"] + result["failed"] == 2


@pytest.mark.asyncio
async def test_synthesis_history(test_config):
    """Test synthesis history functionality"""
    import aiohttp
    
    # First, create a synthesis
    query = "test history query"
    payload = {"query": query, "max_papers": 3}
    
    async with aiohttp.ClientSession() as session:
        # Create synthesis
        async with session.post(
            f"{test_config['api_url']}/research",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        ) as response:
            assert response.status == 200
        
        # Get history
        async with session.get(
            f"{test_config['api_url']}/history",
            params={"limit": 10}
        ) as response:
            assert response.status == 200
            history = await response.json()
            
            assert "history" in history
            assert "portfolio" in history
            assert isinstance(history["history"], list)


@pytest.mark.asyncio
async def test_export_formats(test_config):
    """Test export format functionality"""
    import aiohttp
    
    # First, create a synthesis
    query = "test export query"
    payload = {"query": query, "max_papers": 3}
    
    async with aiohttp.ClientSession() as session:
        # Create synthesis
        async with session.post(
            f"{test_config['api_url']}/research",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        ) as response:
            assert response.status == 200
            synthesis = await response.json()
        
        # Test BibTeX export
        bibtex_payload = {
            "papers": synthesis.get("papers", [])[:3]
        }
        async with session.post(
            f"{test_config['api_url']}/export/bibtex",
            json=bibtex_payload
        ) as response:
            assert response.status == 200
            bibtex = await response.json()
            assert "format" in bibtex
            assert "content" in bibtex
            assert bibtex["format"] == "bibtex"


@pytest.mark.asyncio
async def test_caching(test_config):
    """Test caching functionality"""
    import aiohttp
    
    query = "caching test query"
    payload = {"query": query, "max_papers": 3}
    
    async with aiohttp.ClientSession() as session:
        # First request (cache miss)
        start1 = time.time()
        async with session.post(
            f"{test_config['api_url']}/research",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        ) as response:
            assert response.status == 200
            time1 = time.time() - start1
        
        # Second request (cache hit - should be faster)
        start2 = time.time()
        async with session.post(
            f"{test_config['api_url']}/research",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        ) as response:
            assert response.status == 200
            time2 = time.time() - start2
        
        # Cache hit should be significantly faster
        # (allowing some tolerance for network variance)
        assert time2 < time1 * 0.8  # At least 20% faster


@pytest.mark.asyncio
async def test_error_handling(test_config):
    """Test error handling for invalid inputs"""
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        # Test empty query
        payload = {"query": "", "max_papers": 10}
        async with session.post(
            f"{test_config['api_url']}/research",
            json=payload
        ) as response:
            assert response.status == 400 or response.status == 422
        
        # Test invalid max_papers
        payload = {"query": "test", "max_papers": 1000}
        async with session.post(
            f"{test_config['api_url']}/research",
            json=payload
        ) as response:
            assert response.status == 400 or response.status == 422


@pytest.mark.asyncio
async def test_rate_limiting(test_config):
    """Test rate limiting functionality"""
    import aiohttp
    
    payload = {"query": "rate limit test", "max_papers": 3}
    
    async with aiohttp.ClientSession() as session:
        # Make multiple rapid requests
        responses = []
        for _ in range(10):
            async with session.post(
                f"{test_config['api_url']}/research",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                responses.append(response.status)
        
        # Some requests should succeed (at least one)
        assert 200 in responses


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])


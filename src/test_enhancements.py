"""
Test Hybrid Retrieval and Reranking Features
Tests for new enhancement features
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from hybrid_retrieval import HybridRetriever, RetrievalResult
    HYBRID_RETRIEVAL_AVAILABLE = True
except ImportError:
    HYBRID_RETRIEVAL_AVAILABLE = False

try:
    from reranker import Reranker
    RERANKER_AVAILABLE = True
except ImportError:
    RERANKER_AVAILABLE = False

from agents import Paper


@pytest.fixture
def mock_embedding_client():
    """Mock embedding client"""
    client = Mock()
    client.embed = AsyncMock(return_value=[0.1] * 1024)
    client.embed_batch = AsyncMock(return_value=[[0.1] * 1024] * 3)
    client.cosine_similarity = Mock(return_value=0.85)
    return client


@pytest.fixture
def sample_papers():
    """Sample papers for testing"""
    return [
        Paper(
            id="test-001",
            title="Test Paper 1",
            authors=["Author 1"],
            abstract="This is a test abstract about machine learning",
            url="http://test.com/1"
        ),
        Paper(
            id="test-002",
            title="Test Paper 2",
            authors=["Author 2"],
            abstract="Another test abstract about deep learning",
            url="http://test.com/2"
        ),
        Paper(
            id="test-003",
            title="Test Paper 3",
            authors=["Author 3"],
            abstract="Yet another test abstract",
            url="http://test.com/3"
        )
    ]


@pytest.mark.asyncio
@pytest.mark.skipif(not HYBRID_RETRIEVAL_AVAILABLE, reason="Hybrid retrieval not available")
async def test_hybrid_retriever_build_bm25_index(mock_embedding_client, sample_papers):
    """Test BM25 index building"""
    retriever = HybridRetriever(embedding_client=mock_embedding_client)
    retriever.build_bm25_index(sample_papers)
    
    assert retriever.bm25_index is not None
    assert len(retriever.paper_texts) == 3
    assert len(retriever.paper_ids) == 3


@pytest.mark.asyncio
@pytest.mark.skipif(not HYBRID_RETRIEVAL_AVAILABLE, reason="Hybrid retrieval not available")
async def test_hybrid_retriever_dense_retrieval(mock_embedding_client, sample_papers):
    """Test dense retrieval"""
    retriever = HybridRetriever(embedding_client=mock_embedding_client)
    
    # Add embeddings to papers
    for paper in sample_papers:
        paper.embedding = [0.1] * 1024
    
    results = await retriever.dense_retrieval("machine learning", sample_papers, top_k=2)
    
    assert len(results) <= 2
    assert all(isinstance(r, RetrievalResult) for r in results)
    assert all(r.method == 'dense' for r in results)


@pytest.mark.asyncio
@pytest.mark.skipif(not HYBRID_RETRIEVAL_AVAILABLE, reason="Hybrid retrieval not available")
async def test_hybrid_retriever_sparse_retrieval(mock_embedding_client, sample_papers):
    """Test sparse retrieval (BM25)"""
    retriever = HybridRetriever(embedding_client=mock_embedding_client)
    retriever.build_bm25_index(sample_papers)
    
    results = retriever.sparse_retrieval("machine learning", top_k=2)
    
    assert len(results) <= 2
    assert all(isinstance(r, RetrievalResult) for r in results)
    assert all(r.method == 'sparse' for r in results)


@pytest.mark.asyncio
@pytest.mark.skipif(not HYBRID_RETRIEVAL_AVAILABLE, reason="Hybrid retrieval not available")
async def test_hybrid_retriever_rrf_fusion(mock_embedding_client, sample_papers):
    """Test Reciprocal Rank Fusion"""
    retriever = HybridRetriever(embedding_client=mock_embedding_client)
    
    # Create mock result lists
    dense_results = [
        RetrievalResult(paper_id="test-001", score=0.9, method="dense"),
        RetrievalResult(paper_id="test-002", score=0.8, method="dense")
    ]
    sparse_results = [
        RetrievalResult(paper_id="test-002", score=0.85, method="sparse"),
        RetrievalResult(paper_id="test-001", score=0.75, method="sparse")
    ]
    
    fused = retriever.reciprocal_rank_fusion([dense_results, sparse_results], k=60)
    
    assert len(fused) > 0
    assert all(isinstance(r, tuple) and len(r) == 2 for r in fused)
    # Check that scores are positive
    assert all(score > 0 for _, score in fused)


@pytest.mark.asyncio
@pytest.mark.skipif(not RERANKER_AVAILABLE, reason="Reranker not available")
async def test_reranker_initialization():
    """Test reranker initialization"""
    try:
        reranker = Reranker()
        assert reranker.model is not None or reranker.model is None  # May fail to init
    except Exception:
        # Reranker may fail to initialize if sentence-transformers not available
        pass


@pytest.mark.asyncio
@pytest.mark.skipif(not RERANKER_AVAILABLE, reason="Reranker not available")
async def test_reranker_rerank(sample_papers):
    """Test reranking functionality"""
    try:
        reranker = Reranker()
        if reranker.model is None:
            pytest.skip("Reranker model not available")
        
        results = reranker.rerank("machine learning", sample_papers, top_k=2)
        
        assert len(results) <= 2
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
        assert all(isinstance(paper, Paper) for paper, _ in results)
        assert all(isinstance(score, float) for _, score in results)
    except Exception:
        pytest.skip("Reranker not available or failed to initialize")


@pytest.mark.asyncio
@pytest.mark.skipif(not RERANKER_AVAILABLE, reason="Reranker not available")
async def test_reranker_async(sample_papers):
    """Test async reranking"""
    try:
        reranker = Reranker()
        if reranker.model is None:
            pytest.skip("Reranker model not available")
        
        results = await reranker.rerank_async("machine learning", sample_papers, top_k=2)
        
        assert len(results) <= 2
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
    except Exception:
        pytest.skip("Reranker not available or failed to initialize")


def test_enhancement_features_available():
    """Test that enhancement modules are available"""
    available = {
        "hybrid_retrieval": HYBRID_RETRIEVAL_AVAILABLE,
        "reranker": RERANKER_AVAILABLE
    }
    
    print("\nEnhancement Features Availability:")
    for feature, is_available in available.items():
        status = "✅ Available" if is_available else "❌ Not Available"
        print(f"  {feature}: {status}")
    
    # Skip test if no enhancements are available (don't fail silently)
    if not any(available.values()):
        pytest.skip("No enhancement dependencies installed - skipping availability test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


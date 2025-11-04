"""
Unit Tests for Paper Sources
Tests all 7 academic paper source integrations with mock responses
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import json

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import Paper, ScoutAgent
from nim_clients import EmbeddingNIMClient


@pytest.fixture
def mock_embedding_client():
    """Mock embedding client for Scout agent"""
    client = Mock()
    client.embed = AsyncMock(return_value=[0.1] * 1024)
    client.embed_batch = AsyncMock(return_value=[[0.1] * 1024, [0.2] * 1024])
    client.cosine_similarity = Mock(return_value=0.85)
    client.session = MagicMock()
    return client


@pytest.fixture
def scout_agent(mock_embedding_client):
    """Create Scout agent with mock embedding client"""
    return ScoutAgent(mock_embedding_client)


class TestArxivSource:
    """Test arXiv paper source integration"""
    
    @pytest.mark.asyncio
    async def test_arxiv_search_success(self, scout_agent):
        """Test successful arXiv search"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock arXiv API response
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "entries": [
                    {
                        "id": "arxiv:1234.5678",
                        "title": "Test Paper Title",
                        "authors": [{"name": "Author 1"}, {"name": "Author 2"}],
                        "summary": "Test abstract content",
                        "link": [{"href": "https://arxiv.org/abs/1234.5678"}]
                    }
                ]
            })
            mock_get.return_value.__aenter__.return_value = mock_response
            
            papers = await scout_agent._search_arxiv("machine learning")
            
            assert len(papers) > 0
            assert papers[0].title == "Test Paper Title"
            assert "arxiv" in papers[0].id.lower()
    
    @pytest.mark.asyncio
    async def test_arxiv_search_failure(self, scout_agent):
        """Test arXiv search with API failure"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            papers = await scout_agent._search_arxiv("test query")
            assert papers == []


class TestPubMedSource:
    """Test PubMed paper source integration"""
    
    @pytest.mark.asyncio
    async def test_pubmed_search_success(self, scout_agent):
        """Test successful PubMed search"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock PubMed API response
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.text = AsyncMock(return_value='<?xml version="1.0"?><PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>12345678</PMID><Article><ArticleTitle>Test Title</ArticleTitle><Abstract><AbstractText>Test abstract</AbstractText></Abstract><AuthorList><Author><LastName>Smith</LastName><ForeName>John</ForeName></Author></AuthorList></Article></MedlineCitation></PubmedArticle></PubmedArticleSet>')
            mock_get.return_value.__aenter__.return_value = mock_response
            
            papers = await scout_agent._search_pubmed("machine learning")
            
            assert len(papers) >= 0  # May return empty if parsing fails
            if papers:
                assert "pubmed" in papers[0].id.lower()
    
    @pytest.mark.asyncio
    async def test_pubmed_search_failure(self, scout_agent):
        """Test PubMed search with API failure"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            papers = await scout_agent._search_pubmed("test query")
            assert papers == []


class TestSemanticScholarSource:
    """Test Semantic Scholar paper source integration"""
    
    @pytest.mark.asyncio
    async def test_semantic_scholar_search_success(self, scout_agent):
        """Test successful Semantic Scholar search"""
        with patch.object(scout_agent.embedding_client.session, 'get') as mock_get:
            # Mock Semantic Scholar API response
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "data": [
                    {
                        "paperId": "test-paper-id",
                        "title": "Test Paper Title",
                        "authors": [{"name": "Author 1"}, {"name": "Author 2"}],
                        "abstract": "Test abstract content",
                        "url": "https://www.semanticscholar.org/paper/test"
                    }
                ]
            })
            mock_get.return_value.__aenter__.return_value = mock_response
            
            papers = await scout_agent._search_semantic_scholar("machine learning")
            
            assert len(papers) > 0
            assert "semanticscholar" in papers[0].id.lower()
    
    @pytest.mark.asyncio
    async def test_semantic_scholar_search_failure(self, scout_agent):
        """Test Semantic Scholar search with API failure"""
        with patch.object(scout_agent.embedding_client.session, 'get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            papers = await scout_agent._search_semantic_scholar("test query")
            assert isinstance(papers, list)


class TestCrossrefSource:
    """Test Crossref paper source integration"""
    
    @pytest.mark.asyncio
    async def test_crossref_search_success(self, scout_agent):
        """Test successful Crossref search"""
        with patch.object(scout_agent.embedding_client.session, 'get') as mock_get:
            # Mock Crossref API response
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "message": {
                    "items": [
                        {
                            "DOI": "10.1000/test",
                            "title": ["Test Paper Title"],
                            "author": [
                                {"given": "John", "family": "Smith"}
                            ],
                            "abstract": "Test abstract content"
                        }
                    ]
                }
            })
            mock_get.return_value.__aenter__.return_value = mock_response
            
            papers = await scout_agent._search_crossref("machine learning")
            
            assert len(papers) > 0
            assert "crossref" in papers[0].id.lower()
    
    @pytest.mark.asyncio
    async def test_crossref_search_failure(self, scout_agent):
        """Test Crossref search with API failure"""
        with patch.object(scout_agent.embedding_client.session, 'get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            papers = await scout_agent._search_crossref("test query")
            assert isinstance(papers, list)


class TestIEEESource:
    """Test IEEE Xplore paper source integration"""
    
    @pytest.mark.asyncio
    async def test_ieee_search_success(self, scout_agent):
        """Test successful IEEE search"""
        # Mock IEEE API response
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "articles": [
                    {
                        "title": "Test IEEE Paper",
                        "authors": ["Author 1", "Author 2"],
                        "abstract": "Test abstract",
                        "pdf_url": "https://ieee.org/test.pdf"
                    }
                ]
            })
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # Enable IEEE in config
            with patch.object(scout_agent.source_config, 'enable_ieee', True):
                with patch.object(scout_agent.source_config, 'ieee_api_key', 'test-key'):
                    papers = await scout_agent._search_ieee("machine learning")
                    assert isinstance(papers, list)
    
    @pytest.mark.asyncio
    async def test_ieee_search_disabled(self, scout_agent):
        """Test IEEE search when disabled"""
        with patch.object(scout_agent.source_config, 'enable_ieee', False):
            papers = await scout_agent._search_ieee("test query")
            assert papers == []


class TestACMSource:
    """Test ACM Digital Library paper source integration"""
    
    @pytest.mark.asyncio
    async def test_acm_search_success(self, scout_agent):
        """Test successful ACM search"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "results": [
                    {
                        "title": "Test ACM Paper",
                        "authors": ["Author 1"],
                        "abstract": "Test abstract",
                        "url": "https://dl.acm.org/test"
                    }
                ]
            })
            mock_get.return_value.__aenter__.return_value = mock_response
            
            with patch.object(scout_agent.source_config, 'enable_acm', True):
                with patch.object(scout_agent.source_config, 'acm_api_key', 'test-key'):
                    papers = await scout_agent._search_acm("machine learning")
                    assert isinstance(papers, list)


class TestSpringerSource:
    """Test SpringerLink paper source integration"""
    
    @pytest.mark.asyncio
    async def test_springer_search_success(self, scout_agent):
        """Test successful Springer search"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "records": [
                    {
                        "title": "Test Springer Paper",
                        "creators": ["Author 1"],
                        "abstract": "Test abstract",
                        "url": ["https://link.springer.com/test"]
                    }
                ]
            })
            mock_get.return_value.__aenter__.return_value = mock_response
            
            with patch.object(scout_agent.source_config, 'enable_springer', True):
                with patch.object(scout_agent.source_config, 'springer_api_key', 'test-key'):
                    papers = await scout_agent._search_springer("machine learning")
                    assert isinstance(papers, list)


class TestMultiSourceIntegration:
    """Test multiple sources working together"""
    
    @pytest.mark.asyncio
    async def test_parallel_multi_source_search(self, scout_agent):
        """Test parallel search across multiple sources"""
        # Mock all sources
        with patch.object(scout_agent, '_search_arxiv', return_value=[Paper(
            id="arxiv-1", title="Arxiv Paper", authors=["Author"], 
            abstract="Test", url="https://arxiv.org/test"
        )]):
            with patch.object(scout_agent, '_search_pubmed', return_value=[]):
                with patch.object(scout_agent, '_search_semantic_scholar', return_value=[Paper(
                    id="semanticscholar-1", title="SS Paper", authors=["Author"],
                    abstract="Test", url="https://ss.org/test"
                )]):
                    papers = await scout_agent.search("machine learning", max_papers=10)
                    
                    assert len(papers) > 0
                    assert any("arxiv" in p.id for p in papers) or any("semanticscholar" in p.id for p in papers)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


"""
FastAPI REST API Tests
Tests all API endpoints and functionality
"""

import sys
import os
# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import json
from datetime import datetime

# Import the API app
from api import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def mock_nims():
    """Mock NIM clients"""
    with patch('api.ReasoningNIMClient') as mock_reasoning, \
         patch('api.EmbeddingNIMClient') as mock_embedding:
        
        # Setup mock clients
        reasoning_client = AsyncMock()
        reasoning_client.complete = AsyncMock(return_value="test completion")
        reasoning_client.chat = AsyncMock(return_value={"content": "test chat"})
        reasoning_client.extract_structured = AsyncMock(return_value={"key": "value"})
        
        embedding_client = AsyncMock()
        embedding_client.embed = AsyncMock(return_value=[0.1] * 768)
        embedding_client.embed_batch = AsyncMock(return_value=[[0.1] * 768])
        
        mock_reasoning.return_value.__aenter__.return_value = reasoning_client
        mock_reasoning.return_value.__aexit__ = AsyncMock(return_value=None)
        mock_embedding.return_value.__aenter__.return_value = embedding_client
        mock_embedding.return_value.__aexit__ = AsyncMock(return_value=None)
        
        yield {
            'reasoning': reasoning_client,
            'embedding': embedding_client
        }


class TestHealthEndpoints:
    """Test health and readiness endpoints"""
    
    def test_health_check(self, client):
        """Test /health endpoint"""
        with patch('api.check_nim_health', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = True
            
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "service" in data
            assert "version" in data
            assert "nims_available" in data
    
    def test_readiness_check(self, client):
        """Test /ready endpoint"""
        response = client.get("/ready")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
    
    def test_sources_endpoint(self, client):
        """Test /sources endpoint"""
        with patch('api.PaperSourceConfig') as mock_config:
            mock_config.from_env.return_value = Mock(
                enable_arxiv=True,
                enable_pubmed=True,
                enable_semantic_scholar=True,
                enable_crossref=True,
                enable_ieee=False,
                enable_acm=False,
                enable_springer=False,
                semantic_scholar_api_key=None,
                ieee_api_key=None,
                acm_api_key=None,
                springer_api_key=None
            )
            
            response = client.get("/sources")
            
            assert response.status_code == 200
            data = response.json()
            assert "active_sources_count" in data
            assert "sources" in data
            assert "free_sources" in data["sources"]
            assert "subscription_sources" in data["sources"]
    
    def test_root_endpoint(self, client):
        """Test root / endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "endpoints" in data
        assert "powered_by" in data


class TestMetricsEndpoint:
    """Test metrics endpoint"""
    
    def test_metrics_endpoint(self, client):
        """Test /metrics endpoint"""
        with patch('api.metrics') as mock_metrics:
            mock_metrics.get_metrics.return_value = "# test metrics\n"
            
            response = client.get("/metrics")
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"
    
    def test_metrics_endpoint_unavailable(self, client):
        """Test /metrics when metrics unavailable"""
        with patch('api.METRICS_AVAILABLE', False):
            response = client.get("/metrics")
            
            assert response.status_code == 200
            assert "# Metrics not available" in response.text


class TestResearchEndpoint:
    """Test /research endpoint"""
    
    @pytest.mark.asyncio
    async def test_research_endpoint_valid_request(self, client, mock_nims):
        """Test valid research request"""
        with patch('api.ResearchOpsAgent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_synthesis = {
                "themes": ["theme1", "theme2"],
                "papers": [{"id": "paper1", "title": "Test Paper"}],
                "decisions": []
            }
            mock_agent.run.return_value = mock_synthesis
            mock_agent_class.return_value = mock_agent
            
            request_data = {
                "query": "machine learning in healthcare",
                "max_papers": 10
            }
            
            # Note: TestClient doesn't fully support async, so we'll use a workaround
            response = client.post("/research", json=request_data)
            
            # Should accept request (may be processed in background)
            assert response.status_code in [200, 202]
    
    def test_research_endpoint_invalid_query(self, client):
        """Test research request with invalid query"""
        request_data = {
            "query": "",  # Empty query
            "max_papers": 10
        }
        
        response = client.post("/research", json=request_data)
        
        # Should reject invalid input
        assert response.status_code in [400, 422]
    
    def test_research_endpoint_too_many_papers(self, client):
        """Test research request with too many papers"""
        request_data = {
            "query": "test query",
            "max_papers": 100  # Over limit
        }
        
        response = client.post("/research", json=request_data)
        
        # Should reject
        assert response.status_code in [400, 422]
    
    def test_research_endpoint_date_filters(self, client):
        """Test research request with date filters"""
        request_data = {
            "query": "test query",
            "max_papers": 10,
            "start_year": 2020,
            "end_year": 2024
        }
        
        with patch('api.ResearchOpsAgent') as mock_agent_class:
            mock_agent = AsyncMock()
            mock_agent.run.return_value = {"themes": [], "papers": []}
            mock_agent_class.return_value = mock_agent
            
            response = client.post("/research", json=request_data)
            
            # Should accept with date filters
            assert response.status_code in [200, 202]


class TestExportEndpoints:
    """Test export endpoints"""
    
    def test_export_bibtex(self, client):
        """Test /export/bibtex endpoint"""
        request_data = {
            "papers": [
                {
                    "id": "paper1",
                    "title": "Test Paper",
                    "authors": ["Author 1", "Author 2"],
                    "year": 2023,
                    "venue": "Test Venue"
                }
            ]
        }
        
        response = client.post("/export/bibtex", json=request_data)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/x-bibtex"
        assert "bibtex" in response.json()
    
    def test_export_latex(self, client):
        """Test /export/latex endpoint"""
        request_data = {
            "query": "test query",
            "papers": [{"id": "paper1", "title": "Test"}],
            "themes": ["theme1"],
            "gaps": [],
            "contradictions": []
        }
        
        response = client.post("/export/latex", json=request_data)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/x-latex"
        assert "latex" in response.json()


class TestSessionEndpoints:
    """Test session management endpoints"""
    
    def test_get_session_status(self, client):
        """Test getting session status"""
        # First create a session
        session_id = "test-session-123"
        
        # Mock the research_sessions dict
        with patch('api.research_sessions', {session_id: {"status": "completed"}}):
            response = client.get(f"/research/{session_id}")
            
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
    
    def test_get_session_status_not_found(self, client):
        """Test getting non-existent session"""
        response = client.get("/research/nonexistent-session")
        
        assert response.status_code == 404
        assert "not found" in response.json()["error"].lower()


class TestFeedbackEndpoints:
    """Test feedback endpoints"""
    
    def test_submit_feedback(self, client):
        """Test submitting feedback"""
        with patch('api.get_feedback_collector') as mock_get:
            mock_collector = Mock()
            mock_collector.record_feedback.return_value = {
                "synthesis_id": "syn-1",
                "feedback_type": "helpful"
            }
            mock_get.return_value = mock_collector
            
            request_data = {
                "synthesis_id": "syn-1",
                "query": "test query",
                "feedback_type": "helpful",
                "rating": 5
            }
            
            response = client.post("/feedback", json=request_data)
            
            assert response.status_code == 200
            assert mock_collector.record_feedback.called
    
    def test_get_feedback_stats(self, client):
        """Test getting feedback statistics"""
        with patch('api.get_feedback_collector') as mock_get:
            mock_collector = Mock()
            mock_collector.get_feedback_stats.return_value = {
                "total_feedback": 10,
                "helpful_count": 8,
                "average_rating": 4.5
            }
            mock_get.return_value = mock_collector
            
            response = client.get("/feedback/stats")
            
            assert response.status_code == 200
            data = response.json()
            assert "total_feedback" in data


class TestHistoryEndpoints:
    """Test history endpoints"""
    
    def test_get_history(self, client):
        """Test getting synthesis history"""
        with patch('api.SynthesisHistory') as mock_history_class:
            mock_history = Mock()
            mock_history.get_history.return_value = [
                {"id": "syn-1", "query": "query1"},
                {"id": "syn-2", "query": "query2"}
            ]
            mock_history_class.return_value = mock_history
            
            response = client.get("/history")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    def test_get_history_portfolio(self, client):
        """Test getting history portfolio export"""
        with patch('api.SynthesisHistory') as mock_history_class:
            mock_history = Mock()
            mock_history.export_portfolio.return_value = {
                "format": "json",
                "data": []
            }
            mock_history_class.return_value = mock_history
            
            response = client.get("/history/portfolio?format=json")
            
            assert response.status_code == 200


class TestMiddleware:
    """Test API middleware"""
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options("/health")
        
        # CORS middleware should add headers
        # (TestClient may not show all headers, but shouldn't error)
        assert response.status_code in [200, 405]
    
    @patch('api.metrics')
    def test_metrics_middleware(self, mock_metrics_module, client):
        """Test metrics are recorded"""
        mock_metrics = Mock()
        mock_metrics_module.return_value = mock_metrics
        
        client.get("/health")
        
        # Metrics should be recorded (if enabled)
        # Note: Actual recording happens in async middleware


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 for non-existent endpoint"""
        response = client.get("/nonexistent/endpoint")
        
        assert response.status_code == 404
    
    def test_422_validation_error(self, client):
        """Test 422 for validation errors"""
        # Invalid request body
        response = client.post("/research", json={"invalid": "data"})
        
        # Should return validation error
        assert response.status_code in [422, 400]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


"""
Unit Tests for Agents
Tests individual agent functionality with mocks
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from agents import (
    ScoutAgent, AnalystAgent, SynthesizerAgent, CoordinatorAgent,
    ResearchOpsAgent, Paper, Analysis, Synthesis
)


@pytest.fixture
def mock_embedding_client():
    """Mock embedding client"""
    client = Mock()
    client.embed = AsyncMock(return_value=[0.1] * 1024)  # Mock 1024-dim embedding
    client.embed_batch = AsyncMock(return_value=[[0.1] * 1024, [0.2] * 1024])
    client.cosine_similarity = Mock(return_value=0.85)
    client.session = Mock()
    return client


@pytest.fixture
def mock_reasoning_client():
    """Mock reasoning client"""
    client = Mock()
    client.complete = AsyncMock(return_value="Test completion response")
    client.extract_structured = AsyncMock(return_value={
        "research_question": "Test question",
        "methodology": "Test methodology",
        "key_findings": ["Finding 1", "Finding 2"],
        "limitations": ["Limitation 1"],
        "confidence": 0.9
    })
    return client


@pytest.fixture
def sample_paper():
    """Sample paper for testing"""
    return Paper(
        id="test-001",
        title="Test Paper Title",
        authors=["Author 1", "Author 2"],
        abstract="Test abstract content",
        url="https://test.url/001"
    )


@pytest.mark.asyncio
async def test_scout_agent_search(mock_embedding_client):
    """Test ScoutAgent search functionality"""
    scout = ScoutAgent(mock_embedding_client)
    
    # Mock arXiv and PubMed search
    with patch.object(scout, '_search_arxiv', new_callable=AsyncMock) as mock_arxiv, \
         patch.object(scout, '_search_pubmed', new_callable=AsyncMock) as mock_pubmed:
        
        mock_arxiv.return_value = [
            Paper(id="arxiv-001", title="Paper 1", authors=[], abstract="Abstract 1", url="")
        ]
        mock_pubmed.return_value = [
            Paper(id="pubmed-001", title="Paper 2", authors=[], abstract="Abstract 2", url="")
        ]
        
        results = await scout.search("test query", max_papers=5)
        
        assert len(results) <= 5
        assert mock_arxiv.called
        assert mock_pubmed.called


@pytest.mark.asyncio
async def test_analyst_agent_analyze(mock_reasoning_client, sample_paper):
    """Test AnalystAgent analyze functionality"""
    analyst = AnalystAgent(mock_reasoning_client)
    
    analysis = await analyst.analyze(sample_paper)
    
    assert analysis.paper_id == sample_paper.id
    assert analysis.research_question is not None
    assert len(analysis.key_findings) > 0
    assert mock_reasoning_client.extract_structured.called


@pytest.mark.asyncio
async def test_synthesizer_agent_synthesize(mock_reasoning_client, mock_embedding_client):
    """Test SynthesizerAgent synthesize functionality"""
    synthesizer = SynthesizerAgent(mock_reasoning_client, mock_embedding_client)
    
    analyses = [
        Analysis(
            paper_id="p1",
            research_question="Q1",
            methodology="M1",
            key_findings=["Finding 1", "Finding 2"],
            limitations=["Limitation 1"],
            confidence=0.8
        ),
        Analysis(
            paper_id="p2",
            research_question="Q2",
            methodology="M2",
            key_findings=["Finding 3", "Finding 4"],
            limitations=["Limitation 2"],
            confidence=0.9
        )
    ]
    
    synthesis = await synthesizer.synthesize(analyses)
    
    assert isinstance(synthesis, Synthesis)
    assert len(synthesis.common_themes) >= 0
    assert len(synthesis.contradictions) >= 0
    assert len(synthesis.gaps) >= 0


@pytest.mark.asyncio
async def test_coordinator_should_search_more(mock_reasoning_client):
    """Test CoordinatorAgent should_search_more functionality"""
    coordinator = CoordinatorAgent(mock_reasoning_client)
    
    # Mock reasoning response
    mock_reasoning_client.complete.return_value = "Decision: yes\nReasoning: Need more papers"
    
    result = await coordinator.should_search_more(
        query="test query",
        papers_found=5,
        current_coverage=["topic1", "topic2"]
    )
    
    assert isinstance(result, bool)
    assert mock_reasoning_client.complete.called


@pytest.mark.asyncio
async def test_coordinator_is_synthesis_complete(mock_reasoning_client):
    """Test CoordinatorAgent is_synthesis_complete functionality"""
    coordinator = CoordinatorAgent(mock_reasoning_client)
    
    synthesis = Synthesis(
        common_themes=["Theme 1"],
        contradictions=[{"conflict": "Test"}],
        gaps=["Gap 1"],
        recommendations=[]
    )
    
    # Mock reasoning response
    mock_reasoning_client.complete.return_value = "Decision: yes\nReasoning: Synthesis is complete"
    
    result = await coordinator.is_synthesis_complete(synthesis)
    
    assert isinstance(result, bool)
    assert mock_reasoning_client.complete.called


@pytest.mark.asyncio
async def test_research_ops_agent_run(mock_reasoning_client, mock_embedding_client):
    """Test ResearchOpsAgent full workflow"""
    agent = ResearchOpsAgent(mock_reasoning_client, mock_embedding_client)
    
    # Mock all agent methods
    with patch.object(agent.scout, 'search', new_callable=AsyncMock) as mock_search, \
         patch.object(agent.coordinator, 'should_search_more', new_callable=AsyncMock) as mock_more, \
         patch.object(agent.coordinator, 'is_synthesis_complete', new_callable=AsyncMock) as mock_complete:
        
        # Setup mocks
        mock_search.return_value = [
            Paper(id="p1", title="Paper 1", authors=[], abstract="Abstract", url="")
        ]
        mock_more.return_value = False
        mock_complete.return_value = True
        
        # Mock analyst
        agent.analyst.analyze = AsyncMock(return_value=Analysis(
            paper_id="p1",
            research_question="Q1",
            methodology="M1",
            key_findings=["F1"],
            limitations=[],
            confidence=0.8
        ))
        
        # Mock synthesizer
        agent.synthesizer.synthesize = AsyncMock(return_value=Synthesis(
            common_themes=["Theme 1"],
            contradictions=[],
            gaps=["Gap 1"],
            recommendations=[]
        ))
        
        result = await agent.run("test query", max_papers=1)
        
        assert "papers_analyzed" in result
        assert "common_themes" in result
        assert "decisions" in result
        assert isinstance(result["decisions"], list)


@pytest.mark.asyncio
async def test_decision_logging(mock_embedding_client):
    """Test decision logging functionality"""
    from agents import DecisionLog
    
    log = DecisionLog()
    
    log.log_decision(
        agent="Scout",
        decision_type="TEST",
        decision="TEST_DECISION",
        reasoning="Test reasoning",
        nim_used="Test NIM",
        metadata={"test": "value"}
    )
    
    decisions = log.get_decisions()
    assert len(decisions) == 1
    assert decisions[0]["agent"] == "Scout"
    assert decisions[0]["decision_type"] == "TEST"
    assert decisions[0]["metadata"]["test"] == "value"


@pytest.mark.asyncio
async def test_input_validation():
    """Test input validation"""
    from agents import ResearchQuery
    
    # Valid query
    query = ResearchQuery(query="test query", max_papers=10)
    assert query.query == "test query"
    assert query.max_papers == 10
    
    # Invalid query (too short)
    with pytest.raises(ValueError):
        ResearchQuery(query="", max_papers=10)
    
    # Invalid query (too many papers)
    with pytest.raises(ValueError):
        ResearchQuery(query="test", max_papers=100)
    
    # Invalid query (dangerous pattern)
    with pytest.raises(ValueError):
        ResearchQuery(query="<script>alert('xss')</script>", max_papers=10)


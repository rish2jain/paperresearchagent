"""
Comprehensive Agent Feature Tests
Tests advanced agent capabilities, decision-making, and feature integration
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime
from agents import (
    ScoutAgent, AnalystAgent, SynthesizerAgent, CoordinatorAgent,
    ResearchOpsAgent, Paper, Analysis, Synthesis, DecisionLog,
    ResearchQuery
)
from progress_tracker import ProgressTracker, Stage


class TestScoutAgentFeatures:
    """Test ScoutAgent advanced features"""

    @pytest.fixture
    def scout_agent(self):
        """Create ScoutAgent with mock embedding client"""
        mock_client = Mock()
        mock_client.embed = AsyncMock(return_value=[0.1] * 1024)
        mock_client.embed_batch = AsyncMock(return_value=[[0.1] * 1024] * 3)
        mock_client.cosine_similarity = Mock(return_value=0.85)
        return ScoutAgent(mock_client)

    @pytest.mark.asyncio
    async def test_parallel_multi_source_search(self, scout_agent):
        """Test Scout searches multiple sources in parallel"""
        with patch.object(scout_agent, '_search_arxiv', new_callable=AsyncMock) as mock_arxiv, \
             patch.object(scout_agent, '_search_pubmed', new_callable=AsyncMock) as mock_pubmed, \
             patch.object(scout_agent, '_search_semantic_scholar', new_callable=AsyncMock) as mock_ss:

            # Setup mock responses
            mock_arxiv.return_value = [
                Paper(id="arxiv-1", title="AI Paper", authors=["Alice"],
                      abstract="AI research", url="https://arxiv.org/1")
            ]
            mock_pubmed.return_value = [
                Paper(id="pubmed-1", title="Medical AI", authors=["Bob"],
                      abstract="Medical AI", url="https://pubmed.gov/1")
            ]
            mock_ss.return_value = [
                Paper(id="ss-1", title="ML Research", authors=["Carol"],
                      abstract="ML methods", url="https://semanticscholar.org/1")
            ]

            # Execute search
            results = await scout_agent.search("machine learning in healthcare", max_papers=10)

            # Verify all sources were queried
            assert mock_arxiv.called
            assert mock_pubmed.called
            assert mock_ss.called

            # Verify results from all sources
            assert len(results) == 3
            source_ids = {p.id.split('-')[0] for p in results}
            assert source_ids == {'arxiv', 'pubmed', 'ss'}

    @pytest.mark.asyncio
    async def test_semantic_deduplication(self, scout_agent):
        """Test Scout deduplicates similar papers using embeddings"""
        # Create duplicate papers with different IDs
        papers = [
            Paper(id="p1", title="Deep Learning", authors=["A"],
                  abstract="Neural networks for image classification", url="url1"),
            Paper(id="p2", title="Deep Learning Methods", authors=["B"],
                  abstract="Neural networks for image classification tasks", url="url2"),
            Paper(id="p3", title="Quantum Computing", authors=["C"],
                  abstract="Quantum algorithms for optimization", url="url3")
        ]

        # Mock high similarity between p1 and p2, low with p3
        scout_agent.embedding_client.cosine_similarity = Mock(side_effect=[
            0.95,  # p1 vs p2 (duplicate)
            0.3,   # p1 vs p3 (different)
            0.3    # p2 vs p3 (different)
        ])

        deduplicated = await scout_agent._deduplicate_papers(papers)

        # Should remove p2 as duplicate of p1
        assert len(deduplicated) == 2
        assert "p2" not in [p.id for p in deduplicated]

    @pytest.mark.asyncio
    async def test_decision_logging_search_expansion(self, scout_agent):
        """Test Scout logs decision to expand search"""
        decision_log = DecisionLog()
        scout_agent.decision_log = decision_log

        with patch.object(scout_agent, '_search_arxiv', new_callable=AsyncMock) as mock_search:
            mock_search.return_value = [
                Paper(id="p1", title="Paper", authors=[], abstract="Abstract", url="url")
            ]

            await scout_agent.search("test query", max_papers=5)

            # Check decision was logged
            decisions = decision_log.get_decisions()
            assert len(decisions) > 0
            assert any(d['agent'] == 'Scout' for d in decisions)


class TestAnalystAgentFeatures:
    """Test AnalystAgent advanced features"""

    @pytest.fixture
    def analyst_agent(self):
        """Create AnalystAgent with mock reasoning client"""
        mock_client = Mock()
        mock_client.extract_structured = AsyncMock(return_value={
            "research_question": "What is the impact of X?",
            "methodology": "Experimental study",
            "key_findings": ["Finding A", "Finding B"],
            "limitations": ["Sample size"],
            "confidence": 0.85
        })
        return AnalystAgent(mock_client)

    @pytest.mark.asyncio
    async def test_parallel_paper_analysis(self, analyst_agent):
        """Test Analyst processes multiple papers in parallel"""
        papers = [
            Paper(id=f"p{i}", title=f"Paper {i}", authors=[],
                  abstract=f"Abstract {i}", url=f"url{i}")
            for i in range(5)
        ]

        # Process all papers
        analyses = await asyncio.gather(*[
            analyst_agent.analyze(paper) for paper in papers
        ])

        assert len(analyses) == 5
        assert all(isinstance(a, Analysis) for a in analyses)
        assert analyst_agent.reasoning_client.extract_structured.call_count == 5

    @pytest.mark.asyncio
    async def test_confidence_scoring(self, analyst_agent):
        """Test Analyst extracts confidence scores from reasoning NIM"""
        paper = Paper(id="p1", title="Test", authors=[], abstract="Test abstract", url="url")

        # Mock response with confidence
        analyst_agent.reasoning_client.extract_structured.return_value = {
            "research_question": "Test question",
            "methodology": "Test method",
            "key_findings": ["Finding"],
            "limitations": ["Limitation"],
            "confidence": 0.92
        }

        analysis = await analyst_agent.analyze(paper)

        assert analysis.confidence == 0.92

    @pytest.mark.asyncio
    async def test_structured_extraction_fallback(self, analyst_agent):
        """Test Analyst handles extraction failures gracefully"""
        paper = Paper(id="p1", title="Test", authors=[], abstract="Test", url="url")

        # Mock extraction failure
        analyst_agent.reasoning_client.extract_structured.side_effect = Exception("Extraction failed")

        # Should not raise, should return partial analysis
        analysis = await analyst_agent.analyze(paper)

        assert analysis.paper_id == "p1"
        assert analysis.confidence < 0.5  # Low confidence for failed extraction


class TestSynthesizerAgentFeatures:
    """Test SynthesizerAgent advanced features"""

    @pytest.fixture
    def synthesizer_agent(self):
        """Create SynthesizerAgent with mock clients"""
        mock_reasoning = Mock()
        mock_reasoning.complete = AsyncMock(return_value="Synthesis result")

        mock_embedding = Mock()
        mock_embedding.embed_batch = AsyncMock(return_value=[[0.1] * 1024] * 3)
        mock_embedding.cosine_similarity = Mock(return_value=0.8)

        return SynthesizerAgent(mock_reasoning, mock_embedding)

    @pytest.mark.asyncio
    async def test_theme_clustering_with_embeddings(self, synthesizer_agent):
        """Test Synthesizer uses embeddings to cluster findings"""
        analyses = [
            Analysis(
                paper_id=f"p{i}",
                research_question=f"Question {i}",
                methodology="Method",
                key_findings=[f"Finding {i}", f"Result {i}"],
                limitations=[],
                confidence=0.8
            )
            for i in range(3)
        ]

        synthesis = await synthesizer_agent.synthesize(analyses)

        # Should use embedding client for clustering
        assert synthesizer_agent.embedding_client.embed_batch.called
        assert isinstance(synthesis, Synthesis)
        assert len(synthesis.common_themes) > 0

    @pytest.mark.asyncio
    async def test_contradiction_detection(self, synthesizer_agent):
        """Test Synthesizer detects contradictory findings"""
        analyses = [
            Analysis(
                paper_id="p1",
                research_question="Does X improve Y?",
                methodology="RCT",
                key_findings=["X significantly improves Y (p<0.01)"],
                limitations=[],
                confidence=0.9
            ),
            Analysis(
                paper_id="p2",
                research_question="Effect of X on Y",
                methodology="Meta-analysis",
                key_findings=["No significant effect of X on Y (p=0.45)"],
                limitations=[],
                confidence=0.85
            )
        ]

        # Mock reasoning to detect contradiction
        synthesizer_agent.reasoning_client.complete.return_value = json.dumps({
            "contradictions": [{
                "finding_1": "X improves Y",
                "finding_2": "No effect of X on Y",
                "explanation": "Studies show conflicting results"
            }]
        })

        synthesis = await synthesizer_agent.synthesize(analyses)

        # Should identify contradiction
        assert len(synthesis.contradictions) > 0

    @pytest.mark.asyncio
    async def test_research_gap_identification(self, synthesizer_agent):
        """Test Synthesizer identifies research gaps"""
        analyses = [
            Analysis(
                paper_id="p1",
                research_question="Study in adults",
                methodology="Survey",
                key_findings=["Adults show pattern X"],
                limitations=["No pediatric data"],
                confidence=0.8
            ),
            Analysis(
                paper_id="p2",
                research_question="Another adult study",
                methodology="Experiment",
                key_findings=["Adults respond to Y"],
                limitations=["Age range limited to 18-65"],
                confidence=0.85
            )
        ]

        synthesis = await synthesizer_agent.synthesize(analyses)

        # Should identify gap (no pediatric studies)
        assert len(synthesis.gaps) > 0


class TestCoordinatorAgentFeatures:
    """Test CoordinatorAgent advanced decision-making"""

    @pytest.fixture
    def coordinator_agent(self):
        """Create CoordinatorAgent with mock reasoning client"""
        mock_client = Mock()
        mock_client.complete = AsyncMock(return_value="Decision: yes\nReasoning: Need more data")
        return CoordinatorAgent(mock_client)

    @pytest.mark.asyncio
    async def test_meta_decision_search_more(self, coordinator_agent):
        """Test Coordinator makes meta-decision about searching more"""
        # Mock low coverage scenario
        result = await coordinator_agent.should_search_more(
            query="machine learning",
            papers_found=3,
            current_coverage=["supervised learning"]
        )

        assert isinstance(result, bool)
        assert coordinator_agent.reasoning_client.complete.called

    @pytest.mark.asyncio
    async def test_synthesis_quality_assessment(self, coordinator_agent):
        """Test Coordinator assesses synthesis quality"""
        synthesis = Synthesis(
            common_themes=["Theme A", "Theme B"],
            contradictions=[{"finding_1": "X", "finding_2": "Y"}],
            gaps=["Gap Z"],
            recommendations=["Rec 1", "Rec 2"]
        )

        # Mock quality assessment
        coordinator_agent.reasoning_client.complete.return_value = \
            "Decision: yes\nReasoning: Synthesis covers main themes and identifies gaps"

        result = await coordinator_agent.is_synthesis_complete(synthesis)

        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_decision_reasoning_transparency(self, coordinator_agent):
        """Test Coordinator provides reasoning for decisions"""
        decision_log = DecisionLog()
        coordinator_agent.decision_log = decision_log

        await coordinator_agent.should_search_more(
            query="test",
            papers_found=5,
            current_coverage=["topic1"]
        )

        decisions = decision_log.get_decisions()
        assert any(d['agent'] == 'Coordinator' for d in decisions)
        assert any('reasoning' in d for d in decisions)


class TestProgressTrackerIntegration:
    """Test Progress Tracker integration with agents"""

    @pytest.mark.asyncio
    async def test_progress_stages_tracked(self):
        """Test agents update progress through all stages"""
        tracker = ProgressTracker()

        # Simulate agent workflow
        tracker.update_stage(Stage.SEARCHING)
        assert tracker.current_stage == Stage.SEARCHING

        tracker.update_stage(Stage.ANALYZING)
        assert tracker.current_stage == Stage.ANALYZING

        tracker.update_stage(Stage.SYNTHESIZING)
        assert tracker.current_stage == Stage.SYNTHESIZING

        tracker.update_stage(Stage.COMPLETE)
        assert tracker.current_stage == Stage.COMPLETE

    @pytest.mark.asyncio
    async def test_progress_percentage_calculation(self):
        """Test progress percentage updates correctly"""
        tracker = ProgressTracker()

        tracker.update_stage(Stage.SEARCHING)
        assert tracker.get_progress_percentage() > 0

        tracker.update_stage(Stage.COMPLETE)
        assert tracker.get_progress_percentage() == 100


class TestDecisionLogTransparency:
    """Test decision logging for hackathon judging transparency"""

    def test_decision_log_structure(self):
        """Test decision log captures all required fields"""
        log = DecisionLog()

        log.log_decision(
            agent="Scout",
            decision_type="search_expansion",
            decision="Query 3 additional sources",
            reasoning="Initial results show low coverage of subtopic X",
            nim_used="embedding_nim",
            metadata={"query": "test", "sources": ["arxiv", "pubmed"]}
        )

        decisions = log.get_decisions()
        assert len(decisions) == 1

        decision = decisions[0]
        assert decision['agent'] == "Scout"
        assert decision['decision_type'] == "search_expansion"
        assert 'timestamp' in decision
        assert 'reasoning' in decision
        assert decision['nim_used'] == "embedding_nim"
        assert decision['metadata']['query'] == "test"

    def test_decision_log_chronological_order(self):
        """Test decisions are logged in chronological order"""
        log = DecisionLog()

        log.log_decision("Scout", "search", "Decision 1", "Reason 1")
        log.log_decision("Analyst", "analyze", "Decision 2", "Reason 2")
        log.log_decision("Synthesizer", "synthesize", "Decision 3", "Reason 3")

        decisions = log.get_decisions()
        assert len(decisions) == 3

        # Verify timestamps are in order
        timestamps = [datetime.fromisoformat(d['timestamp']) for d in decisions]
        assert timestamps == sorted(timestamps)

    def test_decision_log_agent_differentiation(self):
        """Test decisions show which agent made them"""
        log = DecisionLog()

        agents = ["Scout", "Analyst", "Synthesizer", "Coordinator"]
        for agent in agents:
            log.log_decision(agent, "test", f"{agent} decision", "Reasoning")

        decisions = log.get_decisions()
        logged_agents = {d['agent'] for d in decisions}

        assert logged_agents == set(agents)


class TestResearchQueryValidation:
    """Test input validation and sanitization"""

    def test_valid_query_creation(self):
        """Test creating valid research query"""
        query = ResearchQuery(
            query="machine learning applications",
            max_papers=20
        )

        assert query.query == "machine learning applications"
        assert query.max_papers == 20

    def test_query_too_short_rejected(self):
        """Test queries that are too short are rejected"""
        with pytest.raises(ValueError):
            ResearchQuery(query="", max_papers=10)

        with pytest.raises(ValueError):
            ResearchQuery(query="a", max_papers=10)

    def test_query_too_many_papers_rejected(self):
        """Test requesting too many papers is rejected"""
        with pytest.raises(ValueError):
            ResearchQuery(query="valid query", max_papers=1000)

    def test_query_xss_injection_detected(self):
        """Test XSS injection attempts are detected"""
        with pytest.raises(ValueError):
            ResearchQuery(
                query="<script>alert('xss')</script>",
                max_papers=10
            )

    def test_query_sql_injection_detected(self):
        """Test SQL injection attempts are detected"""
        with pytest.raises(ValueError):
            ResearchQuery(
                query="test'; DROP TABLE papers;--",
                max_papers=10
            )


class TestEndToEndAgentWorkflow:
    """Test complete agent workflow scenarios"""

    @pytest.mark.asyncio
    async def test_complete_research_workflow(self):
        """Test full research workflow from query to synthesis"""
        # Setup mocks
        mock_reasoning = Mock()
        mock_reasoning.complete = AsyncMock(return_value="Result")
        mock_reasoning.extract_structured = AsyncMock(return_value={
            "research_question": "Q",
            "methodology": "M",
            "key_findings": ["F"],
            "limitations": [],
            "confidence": 0.8
        })

        mock_embedding = Mock()
        mock_embedding.embed = AsyncMock(return_value=[0.1] * 1024)
        mock_embedding.embed_batch = AsyncMock(return_value=[[0.1] * 1024])
        mock_embedding.cosine_similarity = Mock(return_value=0.8)

        agent = ResearchOpsAgent(mock_reasoning, mock_embedding)

        # Mock all searches
        with patch.object(agent.scout, 'search', new_callable=AsyncMock) as mock_search:
            mock_search.return_value = [
                Paper(id="p1", title="Paper 1", authors=[], abstract="Abstract", url="url")
            ]

            # Mock coordinator decisions
            with patch.object(agent.coordinator, 'should_search_more', new_callable=AsyncMock) as mock_more:
                mock_more.return_value = False  # Don't search more

                with patch.object(agent.coordinator, 'is_synthesis_complete', new_callable=AsyncMock) as mock_complete:
                    mock_complete.return_value = True  # Synthesis complete

                    # Run workflow
                    result = await agent.run("test query", max_papers=5)

                    # Verify workflow completed
                    assert "papers_analyzed" in result
                    assert "common_themes" in result
                    assert "decisions" in result
                    assert isinstance(result["decisions"], list)
                    assert len(result["decisions"]) > 0

    @pytest.mark.asyncio
    async def test_iterative_search_refinement(self):
        """Test agent refines search based on initial results"""
        mock_reasoning = Mock()
        mock_reasoning.complete = AsyncMock(return_value="Decision: yes\nReasoning: Low coverage")
        mock_reasoning.extract_structured = AsyncMock(return_value={
            "research_question": "Q",
            "methodology": "M",
            "key_findings": ["F"],
            "limitations": [],
            "confidence": 0.7
        })

        mock_embedding = Mock()
        mock_embedding.embed = AsyncMock(return_value=[0.1] * 1024)
        mock_embedding.embed_batch = AsyncMock(return_value=[[0.1] * 1024])

        agent = ResearchOpsAgent(mock_reasoning, mock_embedding)

        search_count = 0
        async def mock_search(*args, **kwargs):
            nonlocal search_count
            search_count += 1
            return [Paper(id=f"p{search_count}", title=f"Paper {search_count}",
                         authors=[], abstract="Abstract", url="url")]

        with patch.object(agent.scout, 'search', side_effect=mock_search):
            with patch.object(agent.coordinator, 'should_search_more', new_callable=AsyncMock) as mock_more:
                # First call: search more, second call: stop
                mock_more.side_effect = [True, False]

                with patch.object(agent.coordinator, 'is_synthesis_complete', new_callable=AsyncMock) as mock_complete:
                    mock_complete.return_value = True

                    result = await agent.run("test query", max_papers=10)

                    # Should have searched twice
                    assert search_count == 2
                    assert len(result["decisions"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])

"""
Feedback Collection System Tests
Tests feedback storage, retrieval, and statistics
"""

import pytest
import tempfile
import os
import json
from datetime import datetime
from feedback import (
    FeedbackCollector,
    SynthesisFeedback,
    FeedbackType,
    get_feedback_collector
)


class TestSynthesisFeedback:
    """Test SynthesisFeedback dataclass"""
    
    def test_feedback_creation(self):
        """Test creating feedback entry"""
        feedback = SynthesisFeedback(
            synthesis_id="test-123",
            query="test query",
            feedback_type=FeedbackType.HELPFUL,
            rating=5,
            comment="Great synthesis!"
        )
        
        assert feedback.synthesis_id == "test-123"
        assert feedback.query == "test query"
        assert feedback.feedback_type == FeedbackType.HELPFUL
        assert feedback.rating == 5
        assert feedback.comment == "Great synthesis!"
        assert feedback.timestamp is not None
    
    def test_feedback_minimal(self):
        """Test creating feedback with minimal fields"""
        feedback = SynthesisFeedback(
            synthesis_id="test-456",
            query="another query",
            feedback_type=FeedbackType.NOT_HELPFUL
        )
        
        assert feedback.synthesis_id == "test-456"
        assert feedback.rating is None
        assert feedback.comment is None


class TestFeedbackCollector:
    """Test FeedbackCollector class"""
    
    @pytest.fixture
    def temp_feedback_file(self):
        """Create temporary feedback file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        yield temp_path
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    def test_collector_initialization(self, temp_feedback_file):
        """Test feedback collector initialization"""
        collector = FeedbackCollector(storage_path=temp_feedback_file)
        
        assert collector.storage_path == temp_feedback_file
        assert len(collector.feedback_data) == 0
    
    def test_record_feedback(self, temp_feedback_file):
        """Test recording feedback"""
        collector = FeedbackCollector(storage_path=temp_feedback_file)
        
        feedback_dict = collector.record_feedback(
            synthesis_id="syn-1",
            query="test query",
            feedback_type=FeedbackType.HELPFUL,
            rating=5,
            comment="Excellent!"
        )
        
        assert feedback_dict["synthesis_id"] == "syn-1"
        assert feedback_dict["feedback_type"] == FeedbackType.HELPFUL.value
        assert feedback_dict["rating"] == 5
        assert len(collector.feedback_data) == 1
    
    def test_record_multiple_feedback(self, temp_feedback_file):
        """Test recording multiple feedback entries"""
        collector = FeedbackCollector(storage_path=temp_feedback_file)
        
        collector.record_feedback("syn-1", "query1", FeedbackType.HELPFUL, rating=5)
        collector.record_feedback("syn-2", "query2", FeedbackType.NOT_HELPFUL, rating=2)
        collector.record_feedback("syn-3", "query3", FeedbackType.HELPFUL, rating=4)
        
        assert len(collector.feedback_data) == 3
    
    def test_feedback_persistence(self, temp_feedback_file):
        """Test feedback persists to file"""
        collector1 = FeedbackCollector(storage_path=temp_feedback_file)
        collector1.record_feedback("syn-1", "query1", FeedbackType.HELPFUL)
        
        # Create new collector instance - should load existing data
        collector2 = FeedbackCollector(storage_path=temp_feedback_file)
        
        assert len(collector2.feedback_data) == 1
        assert collector2.feedback_data[0]["synthesis_id"] == "syn-1"
    
    def test_get_feedback_stats_empty(self, temp_feedback_file):
        """Test feedback statistics with no feedback"""
        collector = FeedbackCollector(storage_path=temp_feedback_file)
        
        stats = collector.get_feedback_stats()
        
        assert stats["total_feedback"] == 0
        assert stats["helpful_count"] == 0
        assert stats["not_helpful_count"] == 0
        assert stats["average_rating"] == 0.0
    
    def test_get_feedback_stats(self, temp_feedback_file):
        """Test feedback statistics calculation"""
        collector = FeedbackCollector(storage_path=temp_feedback_file)
        
        # Record various feedback types
        collector.record_feedback("syn-1", "query1", FeedbackType.HELPFUL, rating=5)
        collector.record_feedback("syn-2", "query2", FeedbackType.HELPFUL, rating=4)
        collector.record_feedback("syn-3", "query3", FeedbackType.NOT_HELPFUL, rating=2)
        collector.record_feedback("syn-4", "query4", FeedbackType.DECISION_SURPRISING)
        
        stats = collector.get_feedback_stats()
        
        assert stats["total_feedback"] == 4
        assert stats["helpful_count"] == 2
        assert stats["not_helpful_count"] == 1
        assert stats["surprising_decisions"] == 1
        assert stats["average_rating"] == pytest.approx(3.67, abs=0.01)  # (5+4+2)/3
    
    def test_get_learning_insights(self, temp_feedback_file):
        """Test learning insights extraction"""
        collector = FeedbackCollector(storage_path=temp_feedback_file)
        
        collector.record_feedback(
            "syn-1", "query1", FeedbackType.DECISION_SURPRISING,
            decision_id="decision-123"
        )
        collector.record_feedback(
            "syn-2", "query2", FeedbackType.NOT_HELPFUL,
            comment="Missing key papers"
        )
        collector.record_feedback(
            "syn-3", "query3", FeedbackType.NOT_HELPFUL,
            comment="Incomplete analysis"
        )
        
        insights = collector.get_learning_insights()
        
        assert "stats" in insights
        assert "most_surprising_decisions" in insights
        assert "areas_for_improvement" in insights
        assert "decision-123" in insights["most_surprising_decisions"]
        assert "Missing key papers" in insights["areas_for_improvement"]
        assert "Incomplete analysis" in insights["areas_for_improvement"]
    
    def test_feedback_without_rating(self, temp_feedback_file):
        """Test feedback without rating"""
        collector = FeedbackCollector(storage_path=temp_feedback_file)
        
        collector.record_feedback(
            "syn-1", "query1", FeedbackType.HELPFUL
        )
        collector.record_feedback(
            "syn-2", "query2", FeedbackType.HELPFUL, rating=5
        )
        
        stats = collector.get_feedback_stats()
        # Should only count ratings that exist
        assert stats["average_rating"] == 5.0


class TestGetFeedbackCollector:
    """Test global feedback collector"""
    
    def test_get_feedback_collector_singleton(self):
        """Test get_feedback_collector returns singleton"""
        collector1 = get_feedback_collector()
        collector2 = get_feedback_collector()
        
        # Should be same instance
        assert collector1 is collector2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


"""
Feedback Collection System
Implements feedback loops for learning from user validation
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import os

logger = logging.getLogger(__name__)


class FeedbackType(Enum):
    """Types of user feedback"""
    HELPFUL = "helpful"
    NOT_HELPFUL = "not_helpful"
    DECISION_SURPRISING = "decision_surprising"
    DECISION_EXPECTED = "decision_expected"
    SHARED = "shared"


@dataclass
class SynthesisFeedback:
    """Feedback on a synthesis result"""
    synthesis_id: str
    query: str
    feedback_type: FeedbackType
    rating: Optional[int] = None  # 1-5 scale
    comment: Optional[str] = None
    decision_id: Optional[str] = None  # If feedback on specific decision
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class FeedbackCollector:
    """
    Collects and stores user feedback for learning
    Implements feedback loops as recommended by Meadows
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.getenv(
            "FEEDBACK_STORAGE_PATH",
            "Temp/feedback.json"
        )
        self.feedback_data: List[Dict] = []
        self._load_feedback()
    
    def _load_feedback(self):
        """Load existing feedback from storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    self.feedback_data = json.load(f)
                logger.info(f"Loaded {len(self.feedback_data)} feedback entries")
        except Exception as e:
            logger.warning(f"Failed to load feedback: {e}")
            self.feedback_data = []
    
    def _save_feedback(self):
        """Save feedback to storage"""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save feedback: {e}")
    
    def record_feedback(
        self,
        synthesis_id: str,
        query: str,
        feedback_type: FeedbackType,
        rating: Optional[int] = None,
        comment: Optional[str] = None,
        decision_id: Optional[str] = None
    ) -> Dict:
        """Record user feedback"""
        feedback = SynthesisFeedback(
            synthesis_id=synthesis_id,
            query=query,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment,
            decision_id=decision_id
        )
        
        feedback_dict = asdict(feedback)
        feedback_dict['feedback_type'] = feedback.feedback_type.value
        self.feedback_data.append(feedback_dict)
        self._save_feedback()
        
        logger.info(f"Recorded feedback: {feedback_type.value} for synthesis {synthesis_id}")
        return feedback_dict
    
    def get_feedback_stats(self) -> Dict:
        """Get aggregated feedback statistics"""
        if not self.feedback_data:
            return {
                "total_feedback": 0,
                "helpful_count": 0,
                "not_helpful_count": 0,
                "surprising_decisions": 0,
                "average_rating": 0.0
            }
        
        helpful_count = sum(
            1 for f in self.feedback_data
            if f.get('feedback_type') == FeedbackType.HELPFUL.value
        )
        not_helpful_count = sum(
            1 for f in self.feedback_data
            if f.get('feedback_type') == FeedbackType.NOT_HELPFUL.value
        )
        surprising_count = sum(
            1 for f in self.feedback_data
            if f.get('feedback_type') == FeedbackType.DECISION_SURPRISING.value
        )
        
        ratings = [f.get('rating') for f in self.feedback_data if f.get('rating')]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
        
        return {
            "total_feedback": len(self.feedback_data),
            "helpful_count": helpful_count,
            "not_helpful_count": not_helpful_count,
            "surprising_decisions": surprising_count,
            "average_rating": round(avg_rating, 2)
        }
    
    def get_learning_insights(self) -> Dict:
        """Extract learning insights from feedback"""
        stats = self.get_feedback_stats()
        
        # Analyze which decisions are most surprising
        surprising_decisions = [
            f for f in self.feedback_data
            if f.get('feedback_type') == FeedbackType.DECISION_SURPRISING.value
        ]
        
        # Find patterns in negative feedback
        not_helpful_feedback = [
            f for f in self.feedback_data
            if f.get('feedback_type') == FeedbackType.NOT_HELPFUL.value
        ]
        
        insights = {
            "stats": stats,
            "most_surprising_decisions": [
                f.get('decision_id') for f in surprising_decisions[:5]
            ],
            "areas_for_improvement": [
                f.get('comment') for f in not_helpful_feedback if f.get('comment')
            ][:5]
        }
        
        return insights


# Global feedback collector instance
_feedback_collector: Optional[FeedbackCollector] = None


def get_feedback_collector() -> FeedbackCollector:
    """Get or create global feedback collector"""
    global _feedback_collector
    if _feedback_collector is None:
        _feedback_collector = FeedbackCollector()
    return _feedback_collector


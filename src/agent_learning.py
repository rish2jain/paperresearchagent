"""
Agent Learning System
Enables agents to learn from feedback and improve over time
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass, field
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)


@dataclass
class FeedbackEntry:
    """Represents feedback on agent performance"""
    timestamp: str
    agent_name: str
    decision_id: str
    feedback_type: str  # 'positive', 'negative', 'neutral'
    feedback_score: float  # 0.0-1.0
    user_correction: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategyPerformance:
    """Tracks performance of a specific strategy"""
    strategy_name: str
    usage_count: int
    success_count: int
    avg_score: float
    last_used: str


class AgentLearningSystem:
    """
    Learning system for agents to improve from feedback
    """
    
    def __init__(self, learning_file: Optional[str] = None):
        self.learning_file = learning_file or os.path.join(
            os.path.expanduser("~"), ".research-ops-learning.json"
        )
        self.feedback_history: List[FeedbackEntry] = []
        self.strategy_performance: Dict[str, StrategyPerformance] = {}
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load learning data from file"""
        try:
            if os.path.exists(self.learning_file):
                with open(self.learning_file, 'r') as f:
                    data = json.load(f)
                    self.feedback_history = [
                        FeedbackEntry(**entry) for entry in data.get("feedback", [])
                    ]
                    self.strategy_performance = {
                        name: StrategyPerformance(**perf)
                        for name, perf in data.get("strategies", {}).items()
                    }
                    logger.info(f"Loaded learning data: {len(self.feedback_history)} feedback entries")
        except Exception as e:
            logger.warning(f"Failed to load learning data: {e}")
    
    def save_learning_data(self):
        """Save learning data to file"""
        try:
            data = {
                "feedback": [
                    {
                        "timestamp": f.timestamp,
                        "agent_name": f.agent_name,
                        "decision_id": f.decision_id,
                        "feedback_type": f.feedback_type,
                        "feedback_score": f.feedback_score,
                        "user_correction": f.user_correction,
                        "context": f.context
                    }
                    for f in self.feedback_history
                ],
                "strategies": {
                    name: {
                        "strategy_name": perf.strategy_name,
                        "usage_count": perf.usage_count,
                        "success_count": perf.success_count,
                        "avg_score": perf.avg_score,
                        "last_used": perf.last_used
                    }
                    for name, perf in self.strategy_performance.items()
                }
            }
            
            os.makedirs(os.path.dirname(self.learning_file), exist_ok=True)
            with open(self.learning_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("Saved learning data")
        except Exception as e:
            logger.error(f"Failed to save learning data: {e}")
    
    def record_feedback(
        self,
        agent_name: str,
        decision_id: str,
        feedback_type: str,
        feedback_score: float,
        user_correction: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Record feedback on agent performance"""
        entry = FeedbackEntry(
            timestamp=datetime.now().isoformat(),
            agent_name=agent_name,
            decision_id=decision_id,
            feedback_type=feedback_type,
            feedback_score=feedback_score,
            user_correction=user_correction,
            context=context or {}
        )
        
        self.feedback_history.append(entry)
        
        # Update strategy performance if context includes strategy
        if context and "strategy" in context:
            strategy_name = context["strategy"]
            if strategy_name not in self.strategy_performance:
                self.strategy_performance[strategy_name] = StrategyPerformance(
                    strategy_name=strategy_name,
                    usage_count=0,
                    success_count=0,
                    avg_score=0.0,
                    last_used=entry.timestamp
                )
            
            perf = self.strategy_performance[strategy_name]
            perf.usage_count += 1
            if feedback_score > 0.7:  # Success threshold
                perf.success_count += 1
            perf.avg_score = (perf.avg_score * (perf.usage_count - 1) + feedback_score) / perf.usage_count
            perf.last_used = entry.timestamp
        
        # Save periodically (every 10 entries)
        if len(self.feedback_history) % 10 == 0:
            self.save_learning_data()
    
    def get_best_strategy(self, context: Dict[str, Any]) -> Optional[str]:
        """
        Get the best performing strategy for a given context
        
        Args:
            context: Context information (e.g., query type, paper count)
            
        Returns:
            Strategy name or None
        """
        if not self.strategy_performance:
            return None
        
        # Filter strategies by context similarity (simplified)
        # In a full implementation, this would use more sophisticated matching
        
        # Sort by performance
        sorted_strategies = sorted(
            self.strategy_performance.values(),
            key=lambda s: (s.avg_score, s.success_count / max(s.usage_count, 1)),
            reverse=True
        )
        
        if sorted_strategies and sorted_strategies[0].usage_count >= 3:
            return sorted_strategies[0].strategy_name
        
        return None
    
    def get_agent_performance(self, agent_name: str) -> Dict[str, Any]:
        """Get performance statistics for an agent"""
        agent_feedback = [
            f for f in self.feedback_history
            if f.agent_name == agent_name
        ]
        
        if not agent_feedback:
            return {
                "total_feedback": 0,
                "avg_score": 0.0,
                "positive_feedback": 0,
                "negative_feedback": 0
            }
        
        avg_score = sum(f.feedback_score for f in agent_feedback) / len(agent_feedback)
        positive = sum(1 for f in agent_feedback if f.feedback_type == "positive")
        negative = sum(1 for f in agent_feedback if f.feedback_type == "negative")
        
        return {
            "total_feedback": len(agent_feedback),
            "avg_score": avg_score,
            "positive_feedback": positive,
            "negative_feedback": negative,
            "positive_rate": positive / len(agent_feedback) if agent_feedback else 0.0
        }
    
    def get_learning_recommendations(self) -> List[str]:
        """Get recommendations for improving agent performance"""
        recommendations = []
        
        # Analyze strategy performance
        for strategy_name, perf in self.strategy_performance.items():
            if perf.usage_count >= 5:
                success_rate = perf.success_count / perf.usage_count
                if success_rate < 0.5:
                    recommendations.append(
                        f"Strategy '{strategy_name}' has low success rate ({success_rate:.1%}). "
                        f"Consider reviewing or replacing it."
                    )
                elif success_rate > 0.8:
                    recommendations.append(
                        f"Strategy '{strategy_name}' performs well ({success_rate:.1%}). "
                        f"Consider using it more frequently."
                    )
        
        # Analyze agent performance
        agent_names = set(f.agent_name for f in self.feedback_history)
        for agent_name in agent_names:
            perf = self.get_agent_performance(agent_name)
            if perf["total_feedback"] >= 5 and perf["avg_score"] < 0.6:
                recommendations.append(
                    f"Agent '{agent_name}' has low average score ({perf['avg_score']:.2f}). "
                    f"Review recent decisions for improvement opportunities."
                )
        
        return recommendations


class StrategyOptimizer:
    """
    Optimizes agent strategies based on performance data
    """
    
    def __init__(self, learning_system: AgentLearningSystem):
        self.learning_system = learning_system
    
    def optimize_strategy_selection(
        self,
        available_strategies: List[str],
        context: Dict[str, Any]
    ) -> str:
        """
        Select optimal strategy based on historical performance
        
        Args:
            available_strategies: List of available strategy names
            context: Context information
            
        Returns:
            Selected strategy name
        """
        # Get best performing strategy
        best_strategy = self.learning_system.get_best_strategy(context)
        
        if best_strategy and best_strategy in available_strategies:
            return best_strategy
        
        # Fallback to first available strategy
        return available_strategies[0] if available_strategies else "default"
    
    def should_explore_new_strategy(self, exploration_rate: float = 0.1) -> bool:
        """
        Determine if should explore a new strategy (epsilon-greedy)
        
        Args:
            exploration_rate: Probability of exploration
            
        Returns:
            True if should explore
        """
        import random
        return random.random() < exploration_rate


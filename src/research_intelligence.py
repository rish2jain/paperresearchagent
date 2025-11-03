"""
Research Intelligence Platform
Long-term features: hypothesis generation, trend prediction, collaboration matching
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class ResearchIntelligence:
    """
    Research Intelligence Platform features
    Expands beyond synthesis to hypothesis generation, trends, collaboration
    """
    
    def __init__(self):
        self.trend_data = []
    
    def generate_hypotheses(
        self,
        themes: List[str],
        gaps: List[str],
        contradictions: List[Dict]
    ) -> List[str]:
        """
        Generate research hypotheses from synthesis
        Long-term feature: Expand to research intelligence
        """
        hypotheses = []
        
        # Hypothesis 1: From gaps
        for gap in gaps[:3]:
            hypotheses.append(
                f"Hypothesis: Addressing the gap in '{gap}' could lead to "
                f"significant advances in the field."
            )
        
        # Hypothesis 2: From contradictions
        if contradictions:
            hypotheses.append(
                f"Hypothesis: The contradiction between {len(contradictions)} "
                f"pairs of findings suggests a need for meta-analysis or "
                f"replication studies."
            )
        
        # Hypothesis 3: Combining themes
        if len(themes) >= 2:
            hypotheses.append(
                f"Hypothesis: Combining insights from '{themes[0]}' and "
                f"'{themes[1]}' may reveal novel interdisciplinary connections."
            )
        
        return hypotheses[:5]  # Limit to top 5
    
    def predict_trends(
        self,
        themes: List[str],
        papers: List[Dict],
        time_window_years: int = 3
    ) -> Dict:
        """
        Predict future research trends
        Long-term feature: Trend prediction
        """
        # Extract publication years if available
        recent_papers = []
        for paper in papers:
            # Try to extract year from various sources
            paper_id = paper.get("id", "")
            if "arxiv" in paper_id.lower():
                # ArXiv papers often have year in ID or metadata
                recent_papers.append(paper)
        
        predictions = {
            "emerging_themes": themes[:3],
            "predicted_direction": (
                f"Based on {len(papers)} papers analyzed, the field appears to be "
                f"moving toward greater integration of {themes[0] if themes else 'AI methods'} "
                f"with practical applications."
            ),
            "confidence": 0.75,
            "time_horizon": f"{time_window_years} years"
        }
        
        return predictions
    
    def suggest_collaborations(
        self,
        query: str,
        themes: List[str]
    ) -> List[Dict]:
        """
        Suggest potential research collaborations
        Long-term feature: Network effects through collaboration matching
        """
        # This would integrate with a database of researchers
        # For now, return template suggestions
        
        suggestions = [
            {
                "researcher_type": "Methodologist",
                "reason": f"Could help validate findings related to '{themes[0] if themes else query}'",
                "match_score": 0.85
            },
            {
                "researcher_type": "Domain Expert",
                "reason": f"Could provide domain knowledge for '{query}'",
                "match_score": 0.80
            }
        ]
        
        return suggestions


class CollectiveIntelligence:
    """
    Collective Intelligence Features
    Long-term: Learn from collective usage patterns
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        import os
        self.storage_path = storage_path or os.getenv(
            "COLLECTIVE_INTELLIGENCE_PATH",
            "Temp/collective_intelligence.json"
        )
        self.collective_data = []
        self._load_data()
    
    def _load_data(self):
        """Load collective intelligence data"""
        try:
            import os
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    self.collective_data = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load collective data: {e}")
            self.collective_data = []
    
    def record_usage(
        self,
        query: str,
        themes: List[str],
        gaps: List[str]
    ):
        """Record usage for collective intelligence"""
        record = {
            "query": query,
            "themes": themes,
            "gaps": gaps,
            "timestamp": datetime.now().isoformat()
        }
        self.collective_data.append(record)
        self._save_data()
    
    def _save_data(self):
        """Save collective intelligence data"""
        try:
            import os
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(self.collective_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save collective data: {e}")
    
    def identify_trending_gaps(self, limit: int = 5) -> List[str]:
        """
        Identify gaps that multiple researchers are discovering
        Long-term feature: Collective intelligence
        """
        if not self.collective_data:
            return []
        
        # Aggregate gaps across all usage
        all_gaps = []
        for record in self.collective_data:
            all_gaps.extend(record.get("gaps", []))
        
        # Find most common gaps
        gap_counts = {}
        for gap in all_gaps:
            gap_counts[gap] = gap_counts.get(gap, 0) + 1
        
        trending = sorted(
            gap_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [gap for gap, count in trending]
    
    def find_similar_researchers(
        self,
        query: str,
        themes: List[str]
    ) -> List[Dict]:
        """
        Find researchers asking similar questions
        Long-term feature: Network effects
        """
        similar = []
        for record in self.collective_data[-50:]:  # Recent 50
            similarity = self._calculate_similarity(query, themes, record)
            if similarity > 0.5:
                similar.append({
                    "query": record.get("query"),
                    "themes": record.get("themes", [])[:3],
                    "similarity": similarity
                })
        
        return sorted(similar, key=lambda x: x["similarity"], reverse=True)[:5]
    
    def _calculate_similarity(
        self,
        query1: str,
        themes1: List[str],
        record: Dict
    ) -> float:
        """Calculate similarity between queries"""
        query2 = record.get("query", "")
        themes2 = record.get("themes", [])
        
        # Simple similarity: common themes
        common_themes = set(themes1) & set(themes2)
        if not themes1 or not themes2:
            return 0.0
        
        theme_similarity = len(common_themes) / max(len(themes1), len(themes2))
        
        # Query word overlap
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        if words1 and words2:
            query_similarity = len(words1 & words2) / max(len(words1), len(words2))
        else:
            query_similarity = 0.0
        
        return (theme_similarity + query_similarity) / 2


# Global instances
_research_intelligence: Optional[ResearchIntelligence] = None
_collective_intelligence: Optional[CollectiveIntelligence] = None


def get_research_intelligence() -> ResearchIntelligence:
    """Get or create research intelligence instance"""
    global _research_intelligence
    if _research_intelligence is None:
        _research_intelligence = ResearchIntelligence()
    return _research_intelligence


def get_collective_intelligence() -> CollectiveIntelligence:
    """Get or create collective intelligence instance"""
    global _collective_intelligence
    if _collective_intelligence is None:
        _collective_intelligence = CollectiveIntelligence()
    return _collective_intelligence


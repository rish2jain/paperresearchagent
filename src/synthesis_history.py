"""
Synthesis History Tracking
Creates switching costs through research portfolio and history
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os
import hashlib

logger = logging.getLogger(__name__)


class SynthesisHistory:
    """
    Tracks synthesis history to create switching costs
    Builds user's research portfolio over time
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.getenv(
            "SYNTHESIS_HISTORY_PATH",
            "Temp/synthesis_history.json"
        )
        self.history: List[Dict] = []
        self._load_history()
    
    def _load_history(self):
        """Load synthesis history from storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    self.history = json.load(f)
                logger.info(f"Loaded {len(self.history)} synthesis records")
        except Exception as e:
            logger.warning(f"Failed to load history: {e}")
            self.history = []
    
    def _save_history(self):
        """Save history to storage"""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def _generate_id(self, query: str, timestamp: str) -> str:
        """Generate unique ID for synthesis"""
        content = f"{query}_{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def add_synthesis(
        self,
        query: str,
        result: Dict,
        export_formats: Optional[List[str]] = None
    ) -> str:
        """Add a synthesis to history"""
        synthesis_id = self._generate_id(query, datetime.now().isoformat())
        
        record = {
            "synthesis_id": synthesis_id,
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "papers_analyzed": result.get("papers_analyzed", 0),
            "themes_count": len(result.get("common_themes", [])),
            "contradictions_count": len(result.get("contradictions", [])),
            "gaps_count": len(result.get("research_gaps", [])),
            "processing_time": result.get("processing_time_seconds", 0),
            "export_formats": export_formats or [],
            "summary": {
                "key_themes": result.get("common_themes", [])[:3],
                "top_contradictions": result.get("contradictions", [])[:2],
                "research_gaps": result.get("research_gaps", [])[:3]
            }
        }
        
        self.history.append(record)
        self._save_history()
        
        logger.info(f"Added synthesis to history: {synthesis_id}")
        return synthesis_id
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """Get synthesis history, most recent first"""
        return sorted(
            self.history,
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )[:limit]
    
    def get_research_portfolio(self) -> Dict:
        """Generate research portfolio summary"""
        if not self.history:
            return {
                "total_syntheses": 0,
                "total_papers_analyzed": 0,
                "total_themes": 0,
                "total_gaps": 0,
                "research_areas": []
            }
        
        total_papers = sum(h.get("papers_analyzed", 0) for h in self.history)
        total_themes = sum(h.get("themes_count", 0) for h in self.history)
        total_gaps = sum(h.get("gaps_count", 0) for h in self.history)
        
        # Extract research areas from queries
        research_areas = list(set(
            h.get("query", "") for h in self.history
        ))[:10]
        
        # Compute earliest and latest timestamps from history entries
        timestamps = [h.get("timestamp") for h in self.history if h.get("timestamp")]
        first_synthesis = min(timestamps) if timestamps else None
        last_synthesis = max(timestamps) if timestamps else None
        
        return {
            "total_syntheses": len(self.history),
            "total_papers_analyzed": total_papers,
            "total_themes": total_themes,
            "total_gaps": total_gaps,
            "research_areas": research_areas,
            "first_synthesis": first_synthesis,
            "last_synthesis": last_synthesis
        }
    
    def export_portfolio(self, format: str = "json") -> str:
        """Export research portfolio in specified format"""
        portfolio = self.get_research_portfolio()
        portfolio["history"] = self.get_history()
        
        if format == "json":
            return json.dumps(portfolio, indent=2)
        elif format == "markdown":
            return self._export_markdown(portfolio)
        else:
            return json.dumps(portfolio, indent=2)
    
    def _export_markdown(self, portfolio: Dict) -> str:
        """Export portfolio as markdown"""
        md = f"""# Research Portfolio

## Summary
- **Total Syntheses**: {portfolio['total_syntheses']}
- **Papers Analyzed**: {portfolio['total_papers_analyzed']}
- **Themes Identified**: {portfolio['total_themes']}
- **Research Gaps Found**: {portfolio['total_gaps']}

## Research Areas
"""
        for area in portfolio.get('research_areas', []):
            md += f"- {area}\n"
        
        md += "\n## Recent Syntheses\n"
        for synthesis in portfolio.get('history', [])[:10]:
            md += f"\n### {synthesis.get('query', 'Unknown')}\n"
            md += f"- Date: {synthesis.get('timestamp', 'Unknown')}\n"
            md += f"- Papers: {synthesis.get('papers_analyzed', 0)}\n"
            md += f"- Themes: {synthesis.get('themes_count', 0)}\n"
        
        return md


# Global history instance
_history: Optional[SynthesisHistory] = None


def get_synthesis_history() -> SynthesisHistory:
    """Get or create global synthesis history"""
    global _history
    if _history is None:
        _history = SynthesisHistory()
    return _history


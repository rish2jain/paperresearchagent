"""
Temporal Trend Analysis Module
Analyzes research trends over time, detects patterns, and visualizes evolution
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)

# Optional dependencies
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    logger.warning("pandas not available. Install with: pip install pandas")

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logger.warning("scipy not available. Install with: pip install scipy")


@dataclass
class TrendPoint:
    """Represents a trend point in time"""
    year: int
    count: int
    themes: List[str]
    avg_citations: float


@dataclass
class TrendPattern:
    """Represents a detected trend pattern"""
    pattern_type: str  # 'growing', 'declining', 'stable', 'emerging'
    start_year: int
    end_year: int
    growth_rate: float
    theme: str
    confidence: float


class TemporalAnalyzer:
    """
    Analyzes temporal trends in research papers
    """
    
    def __init__(self):
        self.trend_data = []
    
    def extract_years(self, papers: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
        """Extract papers by year"""
        papers_by_year = defaultdict(list)
        
        for paper in papers:
            year = None
            # Try to extract year from various fields
            if 'year' in paper:
                year = paper['year']
            elif 'published_date' in paper:
                date_str = paper['published_date']
                if isinstance(date_str, str):
                    try:
                        year = int(date_str.split('-')[0])
                    except (ValueError, IndexError):
                        pass
            
            if year and 1900 <= year <= 2100:  # Sanity check
                papers_by_year[year].append(paper)
        
        return dict(papers_by_year)
    
    def analyze_trends(
        self,
        papers: List[Dict[str, Any]],
        themes: List[str],
        min_years: int = 3
    ) -> Dict[str, Any]:
        """
        Analyze temporal trends
        
        Args:
            papers: List of paper dictionaries with year information
            themes: List of themes to track
            min_years: Minimum years of data required
            
        Returns:
            Dictionary with trend analysis results
        """
        # Extract papers by year
        papers_by_year = self.extract_years(papers)
        
        if not papers_by_year:
            logger.warning("No year information found in papers")
            return {
                "trends": [],
                "patterns": [],
                "summary": {}
            }
        
        years = sorted(papers_by_year.keys())
        
        if len(years) < min_years:
            logger.warning(f"Insufficient years of data: {len(years)} < {min_years}")
            return {
                "trends": [],
                "patterns": [],
                "summary": {"total_years": len(years)}
            }
        
        # Build trend data
        trend_points = []
        for year in years:
            year_papers = papers_by_year[year]
            # Safe average calculation (fallback if numpy not available)
            try:
                import numpy as np
                avg_citations = np.mean([
                    p.get('citation_count', 0) for p in year_papers
                ]) if year_papers else 0.0
            except (ImportError, NameError):
                # Fallback to Python built-in average
                citation_counts = [p.get('citation_count', 0) for p in year_papers]
                avg_citations = sum(citation_counts) / len(citation_counts) if citation_counts else 0.0
            
            # Extract themes for this year
            year_themes = []
            for theme in themes:
                # Count papers mentioning this theme (simplified)
                theme_count = sum(
                    1 for p in year_papers
                    if theme.lower() in p.get('title', '').lower() or
                       theme.lower() in p.get('abstract', '').lower()
                )
                if theme_count > 0:
                    year_themes.append(theme)
            
            trend_points.append(TrendPoint(
                year=year,
                count=len(year_papers),
                themes=year_themes,
                avg_citations=avg_citations
            ))
        
        # Detect patterns
        patterns = self.detect_patterns(trend_points)
        
        # Calculate summary statistics
        summary = {
            "total_years": len(years),
            "start_year": min(years),
            "end_year": max(years),
            "total_papers": len(papers),
            "avg_papers_per_year": len(papers) / len(years) if years else 0,
            "growth_rate": self.calculate_growth_rate(trend_points)
        }
        
        return {
            "trends": [
                {
                    "year": tp.year,
                    "paper_count": tp.count,
                    "themes": tp.themes,
                    "avg_citations": tp.avg_citations
                }
                for tp in trend_points
            ],
            "patterns": [
                {
                    "pattern_type": p.pattern_type,
                    "start_year": p.start_year,
                    "end_year": p.end_year,
                    "growth_rate": p.growth_rate,
                    "theme": p.theme,
                    "confidence": p.confidence
                }
                for p in patterns
            ],
            "summary": summary
        }
    
    def detect_patterns(self, trend_points: List[TrendPoint]) -> List[TrendPattern]:
        """Detect trend patterns (growing, declining, stable, emerging)"""
        if not SCIPY_AVAILABLE or len(trend_points) < 3:
            return []
        
        patterns = []
        
        # Calculate paper count trend
        counts = [tp.count for tp in trend_points]
        years = [tp.year for tp in trend_points]
        
        # Linear regression to detect growth/decline
        slope, intercept, r_value, p_value, std_err = stats.linregress(years, counts)
        
        # Determine pattern type
        if slope > 0.5 and r_value > 0.7:
            pattern_type = "growing"
        elif slope < -0.5 and r_value > 0.7:
            pattern_type = "declining"
        elif abs(slope) < 0.5:
            pattern_type = "stable"
        else:
            pattern_type = "emerging"
        
        # Create overall trend pattern
        patterns.append(TrendPattern(
            pattern_type=pattern_type,
            start_year=min(years),
            end_year=max(years),
            growth_rate=slope,
            theme="Overall Research",
            confidence=abs(r_value)
        ))
        
        return patterns
    
    def calculate_growth_rate(self, trend_points: List[TrendPoint]) -> float:
        """Calculate overall growth rate"""
        if len(trend_points) < 2:
            return 0.0
        
        first_count = trend_points[0].count
        last_count = trend_points[-1].count
        
        if first_count == 0:
            return float('inf') if last_count > 0 else 0.0
        
        growth_rate = ((last_count - first_count) / first_count) * 100
        return growth_rate
    
    def predict_future_trends(
        self,
        trend_data: Dict[str, Any],
        years_ahead: int = 3
    ) -> Dict[str, Any]:
        """
        Predict future trends using linear regression
        
        Args:
            trend_data: Trend analysis results
            years_ahead: Number of years to predict ahead
            
        Returns:
            Dictionary with predictions
        """
        if not SCIPY_AVAILABLE or not trend_data.get("trends"):
            return {"predictions": []}
        
        trends = trend_data["trends"]
        if len(trends) < 2:
            return {"predictions": []}
        
        years = [t["year"] for t in trends]
        counts = [t["paper_count"] for t in trends]
        
        # Linear regression
        slope, intercept, r_value, _, _ = stats.linregress(years, counts)
        
        # Predict future
        predictions = []
        last_year = max(years)
        
        for i in range(1, years_ahead + 1):
            future_year = last_year + i
            predicted_count = slope * future_year + intercept
            predicted_count = max(0, int(predicted_count))  # Ensure non-negative
            
            predictions.append({
                "year": future_year,
                "predicted_count": predicted_count,
                "confidence": abs(r_value)
            })
        
        return {
            "predictions": predictions,
            "growth_rate": slope,
            "confidence": abs(r_value)
        }


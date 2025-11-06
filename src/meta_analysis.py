"""
Meta-Analysis Support Module
Extracts quantitative results, calculates effect sizes, and performs statistical synthesis
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

# Optional dependencies
try:
    import numpy as np
    from scipy import stats
    import pandas as pd
    STATS_AVAILABLE = True
except ImportError:
    STATS_AVAILABLE = False
    logger.warning("scipy/pandas not available. Install with: pip install scipy pandas")

try:
    import statsmodels.api as sm
    from statsmodels.stats.meta_analysis import effectsize_smd
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    logger.warning("statsmodels not available. Install with: pip install statsmodels")


@dataclass
class QuantitativeResult:
    """Represents a quantitative result from a paper"""
    paper_id: str
    metric_name: str
    value: float
    std_dev: Optional[float] = None
    sample_size: Optional[int] = None
    p_value: Optional[float] = None
    effect_size: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None


@dataclass
class MetaAnalysisResult:
    """Results from meta-analysis"""
    metric_name: str
    pooled_effect: float
    pooled_std_error: float
    confidence_interval: Tuple[float, float]
    heterogeneity: float  # I² statistic
    p_value: float
    n_studies: int


class MetaAnalyzer:
    """
    Performs meta-analysis on quantitative research results
    """
    
    def __init__(self):
        self.extracted_results = []
    
    def extract_quantitative_results(
        self,
        analyses: List[Dict[str, Any]]
    ) -> List[QuantitativeResult]:
        """
        Extract quantitative results from paper analyses
        
        Args:
            analyses: List of analysis dictionaries with metadata
            
        Returns:
            List of QuantitativeResult objects
        """
        results = []
        
        for analysis in analyses:
            paper_id = analysis.get("paper_id", "")
            metadata = analysis.get("metadata", {})
            statistical_results = metadata.get("statistical_results", {})
            
            # Extract p-values
            p_values = statistical_results.get("p_values", [])
            for p_str in p_values:
                p_value = self._parse_p_value(p_str)
                if p_value:
                    results.append(QuantitativeResult(
                        paper_id=paper_id,
                        metric_name="p_value",
                        value=p_value,
                        p_value=p_value
                    ))
            
            # Extract effect sizes
            effect_sizes = statistical_results.get("effect_sizes", [])
            for es_str in effect_sizes:
                es_name, es_value = self._parse_effect_size(es_str)
                if es_value:
                    results.append(QuantitativeResult(
                        paper_id=paper_id,
                        metric_name=es_name,
                        value=es_value,
                        effect_size=es_value
                    ))
            
            # Extract confidence intervals
            ci_list = statistical_results.get("confidence_intervals", [])
            for ci_str in ci_list:
                ci_value, ci_range = self._parse_confidence_interval(ci_str)
                if ci_value and ci_range:
                    results.append(QuantitativeResult(
                        paper_id=paper_id,
                        metric_name="confidence_interval",
                        value=ci_value,
                        confidence_interval=ci_range
                    ))
        
        self.extracted_results = results
        return results
    
    def _parse_p_value(self, p_str: str) -> Optional[float]:
        """Parse p-value from string"""
        # Match patterns like "p < 0.05", "p = 0.001", "p=0.05"
        patterns = [
            r'p\s*[<>=]\s*([0-9.]+)',
            r'p-value[:\s]*([0-9.]+)',
            r'p\s*([0-9.]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, p_str.lower())
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return None
    
    def _parse_effect_size(self, es_str: str) -> Tuple[Optional[str], Optional[float]]:
        """Parse effect size from string"""
        # Match patterns like "Cohen's d = 0.8", "R² = 0.65", "d=0.8"
        patterns = [
            (r"cohen'?s?\s*d\s*[=:]\s*([0-9.-]+)", "cohens_d"),
            (r"r²\s*[=:]\s*([0-9.]+)", "r_squared"),
            (r"r\s*[=:]\s*([0-9.-]+)", "correlation"),
            (r"d\s*[=:]\s*([0-9.-]+)", "effect_size_d")
        ]
        
        for pattern, es_name in patterns:
            match = re.search(pattern, es_str.lower())
            if match:
                try:
                    value = float(match.group(1))
                    return es_name, value
                except ValueError:
                    continue
        
        return None, None
    
    def _parse_confidence_interval(self, ci_str: str) -> Tuple[Optional[float], Optional[Tuple[float, float]]]:
        """Parse confidence interval from string"""
        # Match patterns like "95% CI: [0.5, 0.9]", "CI: 0.5-0.9"
        patterns = [
            r'\[([0-9.]+),\s*([0-9.]+)\]',
            r'([0-9.]+)\s*-\s*([0-9.]+)',
            r'([0-9.]+)\s*to\s*([0-9.]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, ci_str)
            if match:
                try:
                    lower = float(match.group(1))
                    upper = float(match.group(2))
                    midpoint = (lower + upper) / 2
                    return midpoint, (lower, upper)
                except ValueError:
                    continue
        
        return None, None
    
    def perform_meta_analysis(
        self,
        results: List[QuantitativeResult],
        metric_name: str
    ) -> Optional[MetaAnalysisResult]:
        """
        Perform meta-analysis on quantitative results
        
        Args:
            results: List of quantitative results
            metric_name: Metric to analyze (e.g., "cohens_d", "effect_size_d")
            
        Returns:
            MetaAnalysisResult or None if insufficient data
        """
        if not STATS_AVAILABLE or not results:
            return None
        
        # Filter results for this metric
        metric_results = [
            r for r in results
            if r.metric_name == metric_name and r.effect_size is not None
        ]
        
        if len(metric_results) < 2:
            logger.warning(f"Insufficient data for meta-analysis: {len(metric_results)} < 2")
            return None
        
        # Extract values
        values = [r.value for r in metric_results]
        
        # Calculate pooled effect (simple mean for now)
        pooled_effect = np.mean(values)
        pooled_std_error = np.std(values) / np.sqrt(len(values))
        
        # Calculate confidence interval (95%)
        ci_lower = pooled_effect - 1.96 * pooled_std_error
        ci_upper = pooled_effect + 1.96 * pooled_std_error
        
        # Calculate heterogeneity (I² statistic)
        if len(values) > 2:
            # Simplified I² calculation
            q = np.sum((values - pooled_effect) ** 2)
            df = len(values) - 1
            if df > 0:
                heterogeneity = max(0, (q - df) / q * 100) if q > 0 else 0
            else:
                heterogeneity = 0
        else:
            heterogeneity = 0
        
        # Calculate p-value (two-tailed t-test)
        if len(values) > 1:
            t_stat, p_value = stats.ttest_1samp(values, 0)
        else:
            p_value = 1.0
        
        return MetaAnalysisResult(
            metric_name=metric_name,
            pooled_effect=pooled_effect,
            pooled_std_error=pooled_std_error,
            confidence_interval=(ci_lower, ci_upper),
            heterogeneity=heterogeneity,
            p_value=p_value,
            n_studies=len(metric_results)
        )
    
    def analyze_all_metrics(
        self,
        analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Perform meta-analysis on all available metrics
        
        Args:
            analyses: List of paper analyses
            
        Returns:
            Dictionary with meta-analysis results
        """
        # Extract quantitative results
        results = self.extract_quantitative_results(analyses)
        
        # Group by metric
        metrics = {}
        for result in results:
            metric = result.metric_name
            if metric not in metrics:
                metrics[metric] = []
            metrics[metric].append(result)
        
        # Perform meta-analysis for each metric
        meta_results = {}
        for metric_name, metric_results in metrics.items():
            if len(metric_results) >= 2:
                meta_result = self.perform_meta_analysis(metric_results, metric_name)
                if meta_result:
                    meta_results[metric_name] = {
                        "pooled_effect": meta_result.pooled_effect,
                        "pooled_std_error": meta_result.pooled_std_error,
                        "confidence_interval": meta_result.confidence_interval,
                        "heterogeneity": meta_result.heterogeneity,
                        "p_value": meta_result.p_value,
                        "n_studies": meta_result.n_studies
                    }
        
        return {
            "extracted_results": len(results),
            "metrics_analyzed": len(meta_results),
            "meta_analyses": meta_results,
            "summary": {
                "total_studies": len(analyses),
                "metrics_found": list(metrics.keys())
            }
        }


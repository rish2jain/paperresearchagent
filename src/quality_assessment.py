"""
Quality Assessment Module
Automated quality scoring for research papers
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class QualityScore:
    """Quality assessment scores for a paper"""
    overall_score: float  # 0.0 to 1.0
    methodology_score: float
    statistical_score: float
    reproducibility_score: float
    venue_score: float
    sample_size_score: float
    confidence_level: str  # "high", "medium", "low"
    issues: List[str]
    strengths: List[str]


class QualityAssessor:
    """
    Assess quality of research papers based on multiple criteria
    """
    
    def __init__(self):
        self.venue_quality_db = {
            # High-impact venues (simplified - would use actual impact factor data)
            'nature', 'science', 'cell', 'lancet', 'nejm',
            'icml', 'neurips', 'iclr', 'aaai', 'ijcai',
            'iccv', 'cvpr', 'eccv', 'acl', 'emnlp', 'naacl',
            'sigir', 'kdd', 'icdm', 'www'
        }
    
    def assess_paper(
        self,
        paper_data: Dict[str, Any],
        analysis_data: Dict[str, Any]
    ) -> QualityScore:
        """
        Assess paper quality based on multiple criteria
        
        Args:
            paper_data: Paper metadata (title, authors, venue, etc.)
            analysis_data: Analysis results (methodology, findings, etc.)
        
        Returns:
            QualityScore object
        """
        issues = []
        strengths = []
        
        # 1. Methodology Score
        methodology_score = self._assess_methodology(analysis_data, issues, strengths)
        
        # 2. Statistical Score
        statistical_score = self._assess_statistical_rigor(analysis_data, issues, strengths)
        
        # 3. Reproducibility Score
        reproducibility_score = self._assess_reproducibility(analysis_data, issues, strengths)
        
        # 4. Venue Score
        venue_score = self._assess_venue_quality(paper_data, issues, strengths)
        
        # 5. Sample Size Score
        sample_size_score = self._assess_sample_size(analysis_data, issues, strengths)
        
        # Calculate overall score (weighted average)
        overall_score = (
            methodology_score * 0.25 +
            statistical_score * 0.25 +
            reproducibility_score * 0.20 +
            venue_score * 0.15 +
            sample_size_score * 0.15
        )
        
        # Determine confidence level
        if overall_score >= 0.8:
            confidence_level = "high"
        elif overall_score >= 0.6:
            confidence_level = "medium"
        else:
            confidence_level = "low"
        
        return QualityScore(
            overall_score=overall_score,
            methodology_score=methodology_score,
            statistical_score=statistical_score,
            reproducibility_score=reproducibility_score,
            venue_score=venue_score,
            sample_size_score=sample_size_score,
            confidence_level=confidence_level,
            issues=issues,
            strengths=strengths
        )
    
    def _assess_methodology(
        self,
        analysis_data: Dict[str, Any],
        issues: List[str],
        strengths: List[str]
    ) -> float:
        """Assess methodology rigor"""
        score = 0.5  # Base score
        
        methodology = analysis_data.get('methodology', '').lower()
        
        # Positive indicators
        if 'randomized' in methodology or 'rct' in methodology:
            score += 0.2
            strengths.append("Randomized controlled trial design")
        elif 'controlled' in methodology:
            score += 0.15
            strengths.append("Controlled experiment")
        
        if 'double-blind' in methodology or 'blinded' in methodology:
            score += 0.15
            strengths.append("Blinded study design")
        
        if 'prospective' in methodology:
            score += 0.1
            strengths.append("Prospective study")
        
        # Negative indicators
        if 'retrospective' in methodology and 'prospective' not in methodology:
            score -= 0.1
            issues.append("Retrospective study (potential bias)")
        
        if 'case study' in methodology and 'control' not in methodology:
            score -= 0.15
            issues.append("Single case study without controls")
        
        # Check experimental setup
        exp_setup = analysis_data.get('experimental_setup', {})
        if exp_setup.get('datasets'):
            if len(exp_setup['datasets']) >= 3:
                score += 0.1
                strengths.append("Multiple datasets for validation")
        
        return max(0.0, min(1.0, score))
    
    def _assess_statistical_rigor(
        self,
        analysis_data: Dict[str, Any],
        issues: List[str],
        strengths: List[str]
    ) -> float:
        """Assess statistical validity"""
        score = 0.5  # Base score
        
        stat_results = analysis_data.get('statistical_results', {})
        
        # Check for statistical tests
        if stat_results.get('statistical_tests'):
            score += 0.2
            strengths.append("Statistical tests reported")
        
        # Check for p-values
        p_values = stat_results.get('p_values', [])
        if p_values:
            score += 0.15
            # Check for significance
            significant = any(
                'p < 0.05' in pv or 'p < 0.01' in pv or 'p < 0.001' in pv
                for pv in p_values
            )
            if significant:
                score += 0.1
                strengths.append("Statistically significant results")
            else:
                issues.append("No significant p-values reported")
        
        # Check for effect sizes
        if stat_results.get('effect_sizes'):
            score += 0.15
            strengths.append("Effect sizes reported")
        
        # Check for confidence intervals
        if stat_results.get('confidence_intervals'):
            score += 0.1
            strengths.append("Confidence intervals provided")
        
        # Negative: no statistical analysis
        if not any([stat_results.get('p_values'), stat_results.get('effect_sizes'),
                   stat_results.get('statistical_tests')]):
            score -= 0.2
            issues.append("No statistical analysis reported")
        
        return max(0.0, min(1.0, score))
    
    def _assess_reproducibility(
        self,
        analysis_data: Dict[str, Any],
        issues: List[str],
        strengths: List[str]
    ) -> float:
        """Assess reproducibility"""
        score = 0.3  # Base score (low because many papers don't provide)
        
        reproducibility = analysis_data.get('reproducibility', {})
        
        if reproducibility.get('code_available'):
            score += 0.4
            strengths.append("Code available for reproducibility")
            repo_url = reproducibility.get('repository_url', '')
            if repo_url:
                score += 0.1
                strengths.append(f"Repository: {repo_url}")
        
        if reproducibility.get('data_available'):
            score += 0.2
            strengths.append("Data available for reproducibility")
        
        # Negative indicators
        if not reproducibility.get('code_available') and not reproducibility.get('data_available'):
            issues.append("No code or data availability mentioned")
        
        return max(0.0, min(1.0, score))
    
    def _assess_venue_quality(
        self,
        paper_data: Dict[str, Any],
        issues: List[str],
        strengths: List[str]
    ) -> float:
        """Assess publication venue quality"""
        score = 0.5  # Base score
        
        # Try to extract venue from paper data
        venue = paper_data.get('venue', '').lower()
        source = paper_data.get('source', '').lower()
        
        # Check against known high-quality venues
        venue_lower = (venue + ' ' + source).lower()
        
        if any(v in venue_lower for v in self.venue_quality_db):
            score = 0.9
            strengths.append("Published in high-impact venue")
        elif 'arxiv' in source:
            score = 0.6  # Preprint - decent but not peer-reviewed
            issues.append("Preprint (not peer-reviewed)")
        elif 'pubmed' in source or 'pmc' in source:
            score = 0.7  # Medical literature - generally peer-reviewed
            strengths.append("PubMed-indexed (peer-reviewed)")
        
        return max(0.0, min(1.0, score))
    
    def _assess_sample_size(
        self,
        analysis_data: Dict[str, Any],
        issues: List[str],
        strengths: List[str]
    ) -> float:
        """Assess sample size adequacy"""
        score = 0.5  # Base score
        
        methodology = analysis_data.get('methodology', '').lower()
        exp_setup = analysis_data.get('experimental_setup', {})
        
        # Try to extract sample size from methodology or abstract
        # This is simplified - would need NLP extraction in production
        if 'large' in methodology or 'n > 100' in methodology or 'n=1' not in methodology:
            score += 0.2
            strengths.append("Adequate sample size")
        elif 'small' in methodology or 'n < 30' in methodology:
            score -= 0.2
            issues.append("Small sample size")
        
        # Check number of datasets
        datasets = exp_setup.get('datasets', [])
        if len(datasets) >= 2:
            score += 0.15
            strengths.append("Validated on multiple datasets")
        
        return max(0.0, min(1.0, score))


def assess_paper_quality(
    paper_data: Dict[str, Any],
    analysis_data: Dict[str, Any]
) -> QualityScore:
    """
    Convenience function to assess paper quality
    
    Args:
        paper_data: Paper metadata
        analysis_data: Analysis results
    
    Returns:
        QualityScore object
    """
    assessor = QualityAssessor()
    return assessor.assess_paper(paper_data, analysis_data)


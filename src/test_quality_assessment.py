"""
Quality Assessment Module Tests
Tests paper quality scoring and assessment
"""

import pytest
from quality_assessment import (
    QualityAssessor,
    QualityScore,
    assess_paper_quality
)


class TestQualityScore:
    """Test QualityScore dataclass"""
    
    def test_quality_score_creation(self):
        """Test creating quality score"""
        score = QualityScore(
            overall_score=0.85,
            methodology_score=0.9,
            statistical_score=0.8,
            reproducibility_score=0.7,
            venue_score=0.9,
            sample_size_score=0.8,
            confidence_level="high",
            issues=["Small sample size"],
            strengths=["High-impact venue", "Robust methodology"]
        )
        
        assert score.overall_score == 0.85
        assert score.confidence_level == "high"
        assert len(score.issues) == 1
        assert len(score.strengths) == 2


class TestQualityAssessor:
    """Test QualityAssessor class"""
    
    @pytest.fixture
    def assessor(self):
        """Create QualityAssessor instance"""
        return QualityAssessor()
    
    def test_assess_high_quality_paper(self, assessor):
        """Test assessing a high-quality paper"""
        paper_data = {
            "title": "Machine Learning Study",
            "venue": "Nature",
            "source": "nature"
        }
        
        analysis_data = {
            "methodology": "Randomized controlled trial with double-blind design",
            "statistical_results": {
                "p_values": ["p < 0.001", "p < 0.01"],
                "effect_sizes": [0.8, 0.6],
                "statistical_tests": ["t-test", "ANOVA"],
                "confidence_intervals": True
            },
            "reproducibility": {
                "code_available": True,
                "repository_url": "https://github.com/example",
                "data_available": True
            },
            "experimental_setup": {
                "datasets": ["dataset1", "dataset2", "dataset3"]
            }
        }
        
        score = assessor.assess_paper(paper_data, analysis_data)
        
        assert score.overall_score > 0.7
        assert score.confidence_level in ["high", "medium"]
        assert score.venue_score > 0.8
        assert len(score.strengths) > 0
    
    def test_assess_low_quality_paper(self, assessor):
        """Test assessing a low-quality paper"""
        paper_data = {
            "title": "Case Study",
            "venue": "Unknown Journal",
            "source": "arxiv"
        }
        
        analysis_data = {
            "methodology": "Single case study without controls",
            "statistical_results": {},
            "reproducibility": {
                "code_available": False,
                "data_available": False
            },
            "experimental_setup": {
                "datasets": []
            }
        }
        
        score = assessor.assess_paper(paper_data, analysis_data)
        
        assert score.overall_score < 0.6
        assert score.confidence_level in ["low", "medium"]
        assert len(score.issues) > 0
    
    def test_assess_methodology_scoring(self, assessor):
        """Test methodology assessment"""
        issues = []
        strengths = []
        
        # High-quality methodology
        analysis_data = {
            "methodology": "Randomized controlled trial with double-blind design",
            "experimental_setup": {
                "datasets": ["ds1", "ds2", "ds3"]
            }
        }
        
        score = assessor._assess_methodology(analysis_data, issues, strengths)
        
        assert score > 0.7
        assert any("Randomized" in s for s in strengths)
        assert any("Blinded" in s for s in strengths)
    
    def test_assess_statistical_rigor(self, assessor):
        """Test statistical rigor assessment"""
        issues = []
        strengths = []
        
        # Good statistical analysis
        analysis_data = {
            "statistical_results": {
                "p_values": ["p < 0.001"],
                "effect_sizes": [0.8],
                "statistical_tests": ["t-test"],
                "confidence_intervals": True
            }
        }
        
        score = assessor._assess_statistical_rigor(analysis_data, issues, strengths)
        
        assert score > 0.7
        assert any("Statistical tests" in s for s in strengths)
    
    def test_assess_reproducibility(self, assessor):
        """Test reproducibility assessment"""
        issues = []
        strengths = []
        
        # High reproducibility
        analysis_data = {
            "reproducibility": {
                "code_available": True,
                "repository_url": "https://github.com/repo",
                "data_available": True
            }
        }
        
        score = assessor._assess_reproducibility(analysis_data, issues, strengths)
        
        assert score > 0.7
        assert any("Code available" in s for s in strengths)
        assert any("Data available" in s for s in strengths)
    
    def test_assess_venue_quality(self, assessor):
        """Test venue quality assessment"""
        issues = []
        strengths = []
        
        # High-impact venue
        paper_data = {
            "venue": "Nature",
            "source": "nature"
        }
        
        score = assessor._assess_venue_quality(paper_data, issues, strengths)
        
        assert score > 0.8
        assert any("high-impact" in s.lower() for s in strengths)
    
    def test_assess_arxiv_venue(self, assessor):
        """Test arXiv venue scoring"""
        issues = []
        strengths = []
        
        paper_data = {
            "venue": "arXiv preprint",
            "source": "arxiv"
        }
        
        score = assessor._assess_venue_quality(paper_data, issues, strengths)
        
        assert 0.5 < score < 0.7  # Preprint score
        assert any("Preprint" in i or "peer-reviewed" in i.lower() for i in issues)
    
    def test_assess_sample_size(self, assessor):
        """Test sample size assessment"""
        issues = []
        strengths = []
        
        # Good sample size
        analysis_data = {
            "methodology": "Large sample size study with n > 100",
            "experimental_setup": {
                "datasets": ["ds1", "ds2"]
            }
        }
        
        score = assessor._assess_sample_size(analysis_data, issues, strengths)
        
        assert score > 0.6
        assert any("sample size" in s.lower() for s in strengths)
    
    def test_score_bounds(self, assessor):
        """Test scores are bounded between 0 and 1"""
        paper_data = {"title": "Test Paper"}
        analysis_data = {}
        
        score = assessor.assess_paper(paper_data, analysis_data)
        
        assert 0.0 <= score.overall_score <= 1.0
        assert 0.0 <= score.methodology_score <= 1.0
        assert 0.0 <= score.statistical_score <= 1.0
        assert 0.0 <= score.reproducibility_score <= 1.0
        assert 0.0 <= score.venue_score <= 1.0
        assert 0.0 <= score.sample_size_score <= 1.0
    
    def test_confidence_level_assignment(self, assessor):
        """Test confidence level is correctly assigned"""
        paper_data = {"title": "Test"}
        
        # High score
        analysis_data = {
            "methodology": "Randomized controlled trial",
            "statistical_results": {"p_values": ["p < 0.001"]},
            "reproducibility": {"code_available": True}
        }
        score = assessor.assess_paper(paper_data, analysis_data)
        assert score.confidence_level in ["high", "medium"]
        
        # Low score
        analysis_data = {
            "methodology": "Case study",
            "statistical_results": {},
            "reproducibility": {}
        }
        score = assessor.assess_paper(paper_data, analysis_data)
        assert score.confidence_level in ["low", "medium"]


class TestAssessPaperQuality:
    """Test convenience function"""
    
    def test_assess_paper_quality_function(self):
        """Test assess_paper_quality convenience function"""
        paper_data = {
            "title": "Test Paper",
            "venue": "Nature"
        }
        
        analysis_data = {
            "methodology": "RCT",
            "statistical_results": {"p_values": ["p < 0.05"]}
        }
        
        score = assess_paper_quality(paper_data, analysis_data)
        
        assert isinstance(score, QualityScore)
        assert score.overall_score >= 0.0
        assert score.confidence_level in ["high", "medium", "low"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


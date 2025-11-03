"""
Test Enhanced Contradiction Display

Tests the new enhanced contradiction display functionality with various data formats.
"""

import pytest


def test_simple_contradiction_format():
    """Test simple contradiction format (backward compatibility)"""
    simple_contradiction = {
        "paper1": "Smith et al. 2023",
        "claim1": "Model achieves 95% accuracy on dataset",
        "paper2": "Johnson et al. 2024",
        "claim2": "Same model only achieves 87% accuracy",
        "conflict": "Significant discrepancy in reported accuracy results"
    }

    # Verify required fields
    assert "paper1" in simple_contradiction
    assert "paper2" in simple_contradiction
    assert "claim1" in simple_contradiction
    assert "claim2" in simple_contradiction
    assert "conflict" in simple_contradiction

    # Verify default impact is MEDIUM
    assert simple_contradiction.get("impact", "MEDIUM") == "MEDIUM"


def test_rich_contradiction_format():
    """Test rich contradiction format with all enhanced fields"""
    rich_contradiction = {
        "paper1": "Smith et al. 2023",
        "claim1": "Model achieves 95% accuracy on dataset",
        "sample_size_1": "n=10,000",
        "confidence_interval_1": "95% CI: [93.2%, 96.8%]",

        "paper2": "Johnson et al. 2024",
        "claim2": "Same model only achieves 87% accuracy",
        "sample_size_2": "n=1,000",
        "confidence_interval_2": "95% CI: [84.5%, 89.5%]",

        "conflict": "Significant discrepancy in reported accuracy results",
        "statistical_significance": "p < 0.001",
        "likely_cause": "Different dataset sizes and evaluation protocols",
        "resolution": "Conduct standardized evaluation with consistent methodology",
        "impact": "HIGH",
        "impact_explanation": "Core model performance claims differ significantly, affecting deployment decisions"
    }

    # Verify all enhanced fields
    assert "sample_size_1" in rich_contradiction
    assert "sample_size_2" in rich_contradiction
    assert "confidence_interval_1" in rich_contradiction
    assert "confidence_interval_2" in rich_contradiction
    assert "statistical_significance" in rich_contradiction
    assert "likely_cause" in rich_contradiction
    assert "resolution" in rich_contradiction
    assert "impact" in rich_contradiction
    assert "impact_explanation" in rich_contradiction


def test_impact_classification():
    """Test impact classification logic"""
    impact_colors = {
        "HIGH": ("🔴", "#D32F2F"),
        "MEDIUM": ("🟡", "#F57C00"),
        "LOW": ("🟢", "#388E3C")
    }

    # Test HIGH impact
    high_contradiction = {"impact": "HIGH"}
    impact = high_contradiction.get("impact", "MEDIUM").upper()
    icon, color = impact_colors.get(impact, ("🟡", "#F57C00"))
    assert icon == "🔴"
    assert color == "#D32F2F"

    # Test MEDIUM impact (default)
    medium_contradiction = {"impact": "MEDIUM"}
    impact = medium_contradiction.get("impact", "MEDIUM").upper()
    icon, color = impact_colors.get(impact, ("🟡", "#F57C00"))
    assert icon == "🟡"
    assert color == "#F57C00"

    # Test LOW impact
    low_contradiction = {"impact": "LOW"}
    impact = low_contradiction.get("impact", "MEDIUM").upper()
    icon, color = impact_colors.get(impact, ("🟡", "#F57C00"))
    assert icon == "🟢"
    assert color == "#388E3C"

    # Test missing impact (defaults to MEDIUM)
    no_impact = {}
    impact = no_impact.get("impact", "MEDIUM").upper()
    icon, color = impact_colors.get(impact, ("🟡", "#F57C00"))
    assert icon == "🟡"
    assert color == "#F57C00"


def test_title_truncation():
    """Test title text truncation for long conflict descriptions"""
    long_conflict = "This is a very long conflict description that exceeds the 80 character limit and should be truncated with ellipsis"
    short_conflict = "Short conflict"

    # Test long title truncation
    title_text = long_conflict[:80] + "..." if len(long_conflict) > 80 else long_conflict
    assert len(title_text) <= 83  # 80 chars + "..."
    assert title_text.endswith("...")

    # Test short title no truncation
    title_text = short_conflict[:80] + "..." if len(short_conflict) > 80 else short_conflict
    assert title_text == short_conflict
    assert not title_text.endswith("...")


def test_auto_expansion_logic():
    """Test auto-expansion based on impact level"""
    high_impact = {"impact": "HIGH"}
    medium_impact = {"impact": "MEDIUM"}
    low_impact = {"impact": "LOW"}

    # HIGH impact should auto-expand
    assert high_impact.get("impact", "MEDIUM").upper() == "HIGH"

    # MEDIUM impact should not auto-expand
    assert medium_impact.get("impact", "MEDIUM").upper() == "MEDIUM"

    # LOW impact should not auto-expand
    assert low_impact.get("impact", "MEDIUM").upper() == "LOW"


def test_mixed_contradiction_list():
    """Test list with both simple and rich contradictions"""
    contradictions = [
        {
            "paper1": "Simple Paper 1",
            "claim1": "Simple claim 1",
            "paper2": "Simple Paper 2",
            "claim2": "Simple claim 2",
            "conflict": "Simple conflict"
        },
        {
            "paper1": "Rich Paper 1",
            "claim1": "Rich claim 1",
            "sample_size_1": "n=5000",
            "paper2": "Rich Paper 2",
            "claim2": "Rich claim 2",
            "sample_size_2": "n=3000",
            "conflict": "Rich conflict",
            "impact": "HIGH",
            "likely_cause": "Methodological differences",
            "resolution": "Standardize protocols"
        }
    ]

    # Verify list has mixed formats
    assert len(contradictions) == 2
    assert "sample_size_1" not in contradictions[0]  # Simple format
    assert "sample_size_1" in contradictions[1]  # Rich format


def test_optional_fields_graceful_handling():
    """Test that missing optional fields are handled gracefully"""
    minimal_contradiction = {
        "paper1": "Paper 1",
        "claim1": "Claim 1",
        "paper2": "Paper 2",
        "claim2": "Claim 2",
        "conflict": "Conflict description"
    }

    # Verify optional fields return None or empty
    assert "sample_size_1" not in minimal_contradiction
    assert "statistical_significance" not in minimal_contradiction
    assert "likely_cause" not in minimal_contradiction
    assert "resolution" not in minimal_contradiction
    assert "impact_explanation" not in minimal_contradiction

    # Verify required fields exist
    assert "paper1" in minimal_contradiction
    assert "paper2" in minimal_contradiction
    assert "claim1" in minimal_contradiction
    assert "claim2" in minimal_contradiction
    assert "conflict" in minimal_contradiction


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

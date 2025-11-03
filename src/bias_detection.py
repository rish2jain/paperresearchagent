"""
Bias Detection Module
Detects various types of bias in research synthesis
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import Counter
import re


def detect_bias(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detect various types of bias in the paper collection

    Args:
        papers: List of paper dictionaries

    Returns:
        Dictionary with bias analysis results
    """
    if not papers:
        return {
            "publication_bias": {},
            "temporal_bias": {},
            "geographic_bias": {},
            "venue_bias": {},
            "overall_assessment": "No papers to analyze",
        }

    # Extract data
    years = []
    sources = []
    venues = []
    countries = []

    for paper in papers:
        # Extract year
        year = _extract_year_from_paper(paper)
        if year:
            years.append(year)

        # Extract source
        source = paper.get("source", "")
        if source:
            sources.append(source.lower())

        # Extract venue (if available)
        venue = (
            paper.get("venue", "")
            or paper.get("journal", "")
            or paper.get("conference", "")
        )
        if venue:
            venues.append(venue)

        # Try to extract geographic info (from authors or affiliations if available)
        # This is a simplified version - could be enhanced with author affiliation parsing
        authors = paper.get("authors", [])
        if authors:
            # Simple heuristic: check for country names in author names (not very reliable)
            # In a real implementation, would use affiliation data
            pass

    # Analyze biases
    publication_bias = _analyze_publication_bias(sources, years)
    temporal_bias = _analyze_temporal_bias(years)
    geographic_bias = _analyze_geographic_bias(papers)  # Simplified
    venue_bias = _analyze_venue_bias(venues)

    # Overall assessment
    warnings = []
    if temporal_bias.get("is_skewed"):
        warnings.append(
            f"Temporal bias detected: Most papers from {temporal_bias.get('dominant_period')}"
        )
    if publication_bias.get("is_skewed"):
        warnings.append(
            f"Source bias: {publication_bias.get('dominant_source', 'unknown')} dominates"
        )
    if venue_bias.get("is_skewed"):
        warnings.append(f"Venue bias: Limited diversity in publication venues")

    overall = "No significant bias detected" if not warnings else "; ".join(warnings)

    return {
        "publication_bias": publication_bias,
        "temporal_bias": temporal_bias,
        "geographic_bias": geographic_bias,
        "venue_bias": venue_bias,
        "warnings": warnings,
        "overall_assessment": overall,
        "recommendations": _generate_recommendations(
            publication_bias, temporal_bias, venue_bias
        ),
    }


def _extract_year_from_paper(paper: Dict[str, Any]) -> Optional[int]:
    """Extract year from paper"""
    # Try different fields
    if "published_date" in paper:
        date_str = str(paper["published_date"])
        year_match = re.search(r"\b(19|20)\d{2}\b", date_str)
        if year_match:
            return int(year_match.group(0))

    if "year" in paper:
        try:
            year_value = paper["year"]
            # Handle string years
            if isinstance(year_value, str):
                # Extract numeric part if string contains numbers
                year_match = re.search(r"\b(19|20)\d{2}\b", year_value)
                if year_match:
                    return int(year_match.group(0))
                else:
                    # Try direct conversion
                    return int(year_value)
            else:
                # Already numeric
                return int(year_value)
        except (ValueError, TypeError) as e:
            # Log warning if we have context
            import logging

            logger = logging.getLogger(__name__)
            paper_id = paper.get("id", "unknown")
            paper_title = paper.get("title", "Unknown Title")[:50]
            logger.warning(
                f"Failed to extract year from paper '{paper_id}' "
                f"('{paper_title}'): year value '{paper.get('year')}' "
                f"cannot be converted to int. Error: {e}"
            )
            return None

    # Try to extract from paper ID
    paper_id = paper.get("id", "")
    year_match = re.search(r"(19|20)\d{2}", paper_id)
    if year_match:
        return int(year_match.group(0))

    return None


def _analyze_publication_bias(sources: List[str], years: List[int]) -> Dict[str, Any]:
    """Analyze publication/source bias"""
    if not sources:
        return {"is_skewed": False, "message": "No source data"}

    source_counts = Counter(sources)
    total = len(sources)
    dominant_source = source_counts.most_common(1)[0]
    dominant_ratio = dominant_source[1] / total

    is_skewed = dominant_ratio > 0.7  # More than 70% from one source

    return {
        "is_skewed": is_skewed,
        "dominant_source": dominant_source[0],
        "dominant_count": dominant_source[1],
        "dominant_ratio": dominant_ratio,
        "source_distribution": dict(source_counts),
        "message": f"{dominant_source[0]} accounts for {dominant_ratio * 100:.1f}% of papers"
        if is_skewed
        else "Good source diversity",
    }


def _analyze_temporal_bias(years: List[int]) -> Dict[str, Any]:
    """Analyze temporal/publication date bias"""
    if not years:
        return {"is_skewed": False, "message": "No year data"}

    year_counts = Counter(years)
    sorted_years = sorted(years)
    year_range = sorted_years[-1] - sorted_years[0] if sorted_years else 0

    # Check if too recent (publication bias toward recent papers)
    current_year = datetime.now().year
    recent_papers = [y for y in years if y >= current_year - 3]
    recent_ratio = len(recent_papers) / len(years) if years else 0

    # Check if too clustered in one period
    dominant_year = year_counts.most_common(1)[0]
    dominant_ratio = dominant_year[1] / len(years)
    is_clustered = (
        dominant_ratio > 0.5 and len(year_counts) < 5
    )  # More than 50% in one year and less than 5 years represented

    # Determine dominant period
    if recent_ratio > 0.8:
        dominant_period = "Very recent (last 3 years)"
    elif recent_ratio > 0.6:
        dominant_period = "Recent (last 3 years)"
    elif is_clustered:
        dominant_period = f"{dominant_year[0]}"
    else:
        dominant_period = f"{sorted_years[0]}-{sorted_years[-1]}"

    return {
        "is_skewed": recent_ratio > 0.8 or is_clustered,
        "year_range": year_range,
        "oldest_year": sorted_years[0] if sorted_years else None,
        "newest_year": sorted_years[-1] if sorted_years else None,
        "recent_ratio": recent_ratio,
        "dominant_period": dominant_period,
        "year_distribution": dict(year_counts),
        "message": f"Year range: {sorted_years[0]}-{sorted_years[-1]}, {recent_ratio * 100:.1f}% from last 3 years",
    }


def _analyze_geographic_bias(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze geographic bias (simplified - would need affiliation data)"""
    # This is a placeholder - real implementation would parse author affiliations
    return {
        "is_skewed": False,
        "message": "Geographic analysis requires author affiliation data",
        "note": "Enhanced geographic bias detection requires parsing author affiliations",
    }


def _analyze_venue_bias(venues: List[str]) -> Dict[str, Any]:
    """Analyze venue/publication bias"""
    if not venues:
        return {"is_skewed": False, "message": "No venue data"}

    venue_counts = Counter(venues)
    total = len(venues)
    dominant_venue = venue_counts.most_common(1)[0]
    dominant_ratio = dominant_venue[1] / total

    is_skewed = dominant_ratio > 0.6  # More than 60% from one venue
    diversity_score = len(venue_counts) / total if total > 0 else 0

    return {
        "is_skewed": is_skewed,
        "dominant_venue": dominant_venue[0],
        "dominant_count": dominant_venue[1],
        "dominant_ratio": dominant_ratio,
        "venue_count": len(venue_counts),
        "diversity_score": diversity_score,
        "message": f"{len(venue_counts)} unique venues, {dominant_ratio * 100:.1f}% from {dominant_venue[0]}"
        if is_skewed
        else f"Good venue diversity ({len(venue_counts)} venues)",
    }


def _generate_recommendations(
    publication_bias: Dict, temporal_bias: Dict, venue_bias: Dict
) -> List[str]:
    """Generate recommendations based on detected biases"""
    recommendations = []

    if publication_bias.get("is_skewed"):
        recommendations.append(
            f"Consider searching additional sources beyond {publication_bias.get('dominant_source')} "
            f"to improve diversity (currently {publication_bias.get('dominant_ratio', 0) * 100:.1f}%)"
        )

    if temporal_bias.get("is_skewed"):
        if temporal_bias.get("recent_ratio", 0) > 0.8:
            recommendations.append(
                "Consider including older foundational papers to provide historical context"
            )
        else:
            recommendations.append(
                "Consider focusing on more recent papers if reviewing current state-of-the-art"
            )

    if venue_bias.get("is_skewed"):
        recommendations.append(
            f"Try searching additional venues beyond {venue_bias.get('dominant_venue')} "
            f"to capture broader perspectives"
        )

    if not recommendations:
        recommendations.append(
            "Good diversity across sources, time periods, and venues"
        )

    return recommendations

"""
Date Filtering Module
Filter and prioritize papers by publication date
"""

from typing import List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class DateRange:
    """Date range for filtering papers"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    def contains(self, date: Optional[datetime]) -> bool:
        """Check if date falls within range"""
        if date is None:
            return True  # Include papers without dates
        
        if self.start_date and date < self.start_date:
            return False
        if self.end_date and date > self.end_date:
            return False
        
        return True


def parse_paper_date(paper_id: str, paper_data: dict) -> Optional[datetime]:
    """
    Extract publication date from paper data
    
    Args:
        paper_id: Paper identifier
        paper_data: Paper metadata dictionary
    
    Returns:
        Datetime object or None if date cannot be parsed
    """
    # Try various date fields
    date_fields = ['published_date', 'publication_date', 'date', 'year', 'published']
    
    for field in date_fields:
        if field in paper_data:
            date_value = paper_data[field]
            if isinstance(date_value, datetime):
                return date_value
            if isinstance(date_value, str):
                try:
                    # Try common date formats
                    for fmt in ['%Y-%m-%d', '%Y-%m', '%Y', '%B %d, %Y', '%d %B %Y']:
                        try:
                            return datetime.strptime(date_value, fmt)
                        except ValueError:
                            continue
                except:
                    pass
    
    # Try to extract from paper ID (e.g., arxiv-2024.00123)
    if 'arxiv' in paper_id.lower():
        # Extract year from arXiv ID
        year_match = None
        import re
        year_match = re.search(r'(19|20)\d{2}', paper_id)
        if year_match:
            year = int(year_match.group(0))
            return datetime(year, 1, 1)  # Use January 1st as default
    
    return None


def filter_by_date_range(
    papers: List,
    date_range: DateRange,
    keep_without_dates: bool = True
) -> List:
    """
    Filter papers by date range
    
    Args:
        papers: List of Paper objects
        date_range: DateRange to filter by
        keep_without_dates: Whether to keep papers without dates
    
    Returns:
        Filtered list of papers
    """
    filtered = []
    
    for paper in papers:
        # Try to get date from paper
        paper_dict = {
            'id': getattr(paper, 'id', ''),
            'published_date': getattr(paper, 'published_date', None),
            'year': getattr(paper, 'year', None)
        }
        
        paper_date = parse_paper_date(paper_dict['id'], paper_dict)
        
        if paper_date is None:
            if keep_without_dates:
                filtered.append(paper)
        elif date_range.contains(paper_date):
            filtered.append(paper)
    
    logger.info(f"Filtered {len(papers)} papers to {len(filtered)} within date range")
    return filtered


def prioritize_recent_papers(
    papers: List,
    recent_years: int = 3,
    max_recent: Optional[int] = None
) -> List:
    """
    Prioritize papers from recent years
    
    Args:
        papers: List of Paper objects
        recent_years: Number of years to consider "recent"
        max_recent: Maximum number of recent papers to include (None = all)
    
    Returns:
        Reordered list with recent papers first
    """
    cutoff_date = datetime.now() - timedelta(days=recent_years * 365)
    
    recent_papers = []
    older_papers = []
    
    for paper in papers:
        paper_dict = {
            'id': getattr(paper, 'id', ''),
            'published_date': getattr(paper, 'published_date', None),
            'year': getattr(paper, 'year', None)
        }
        
        paper_date = parse_paper_date(paper_dict['id'], paper_dict)
        
        if paper_date and paper_date >= cutoff_date:
            recent_papers.append(paper)
        else:
            older_papers.append(paper)
    
    # Sort recent papers by date (newest first)
    recent_papers.sort(
        key=lambda p: parse_paper_date(
            getattr(p, 'id', ''),
            {'id': getattr(p, 'id', '')}
        ) or datetime.min,
        reverse=True
    )
    
    # Limit recent papers if specified
    if max_recent and len(recent_papers) > max_recent:
        recent_papers = recent_papers[:max_recent]
    
    # Combine: recent first, then older
    result = recent_papers + older_papers
    
    logger.info(f"Prioritized {len(recent_papers)} recent papers (last {recent_years} years)")
    return result


def filter_by_year_range(
    papers: List,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None
) -> List:
    """
    Filter papers by year range
    
    Args:
        papers: List of Paper objects
        start_year: Earliest year to include
        end_year: Latest year to include
    
    Returns:
        Filtered list of papers
    """
    if start_year is None and end_year is None:
        return papers
    
    date_range = DateRange(
        start_date=datetime(start_year, 1, 1) if start_year else None,
        end_date=datetime(end_year, 12, 31) if end_year else None
    )
    
    return filter_by_date_range(papers, date_range)


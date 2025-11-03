"""
Date Filtering Module Tests
Tests date parsing, filtering, and prioritization functionality
"""

import pytest
from datetime import datetime, timedelta
from date_filter import (
    DateRange,
    parse_paper_date,
    filter_by_date_range,
    prioritize_recent_papers,
    filter_by_year_range
)


class MockPaper:
    """Mock Paper object for testing"""
    def __init__(self, paper_id: str, published_date=None, year=None):
        self.id = paper_id
        self.published_date = published_date
        self.year = year


class TestDateRange:
    """Test DateRange dataclass"""
    
    def test_date_range_contains(self):
        """Test date range contains logic"""
        start = datetime(2020, 1, 1)
        end = datetime(2024, 12, 31)
        date_range = DateRange(start_date=start, end_date=end)
        
        # Date within range
        assert date_range.contains(datetime(2022, 6, 15)) is True
        
        # Date before range
        assert date_range.contains(datetime(2019, 12, 31)) is False
        
        # Date after range
        assert date_range.contains(datetime(2025, 1, 1)) is False
        
        # Date at boundaries
        assert date_range.contains(start) is True
        assert date_range.contains(end) is True
    
    def test_date_range_without_dates(self):
        """Test date range handles None dates"""
        date_range = DateRange(start_date=None, end_date=None)
        
        # Should include all dates
        assert date_range.contains(datetime(2020, 1, 1)) is True
        assert date_range.contains(datetime(2030, 1, 1)) is True
        assert date_range.contains(None) is True  # Includes papers without dates
    
    def test_date_range_only_start(self):
        """Test date range with only start date"""
        start = datetime(2020, 1, 1)
        date_range = DateRange(start_date=start, end_date=None)
        
        assert date_range.contains(datetime(2020, 1, 1)) is True
        assert date_range.contains(datetime(2030, 1, 1)) is True
        assert date_range.contains(datetime(2019, 12, 31)) is False
    
    def test_date_range_only_end(self):
        """Test date range with only end date"""
        end = datetime(2024, 12, 31)
        date_range = DateRange(start_date=None, end_date=end)
        
        assert date_range.contains(datetime(2024, 12, 31)) is True
        assert date_range.contains(datetime(2020, 1, 1)) is True
        assert date_range.contains(datetime(2025, 1, 1)) is False


class TestParsePaperDate:
    """Test paper date parsing"""
    
    def test_parse_datetime_object(self):
        """Test parsing datetime object directly"""
        paper_data = {
            'published_date': datetime(2023, 6, 15),
            'year': 2023
        }
        date = parse_paper_date("paper-1", paper_data)
        assert date == datetime(2023, 6, 15)
    
    def test_parse_date_strings(self):
        """Test parsing various date string formats"""
        # YYYY-MM-DD format
        paper_data = {'published_date': '2023-06-15'}
        date = parse_paper_date("paper-1", paper_data)
        assert date == datetime(2023, 6, 15)
        
        # YYYY-MM format
        paper_data = {'published_date': '2023-06'}
        date = parse_paper_date("paper-2", paper_data)
        assert date == datetime(2023, 6, 1)
        
        # YYYY format
        paper_data = {'year': '2023'}
        date = parse_paper_date("paper-3", paper_data)
        assert date == datetime(2023, 1, 1)
    
    def test_parse_arxiv_id(self):
        """Test extracting year from arXiv ID"""
        # ArXiv format: arxiv-2024.00123
        date = parse_paper_date("arxiv-2024.00123", {})
        assert date == datetime(2024, 1, 1)
        
        # ArXiv with year in different position
        date = parse_paper_date("arxiv-2023.12345v1", {})
        assert date == datetime(2023, 1, 1)
    
    def test_parse_no_date(self):
        """Test parsing paper with no date information"""
        date = parse_paper_date("paper-no-date", {})
        assert date is None
    
    def test_parse_priority_fields(self):
        """Test that published_date takes priority over year"""
        paper_data = {
            'published_date': datetime(2023, 6, 15),
            'year': 2022,
            'date': '2021-01-01'
        }
        date = parse_paper_date("paper-1", paper_data)
        assert date == datetime(2023, 6, 15)


class TestFilterByDateRange:
    """Test date range filtering"""
    
    def test_filter_within_range(self):
        """Test filtering papers within date range"""
        papers = [
            MockPaper("p1", published_date=datetime(2022, 1, 1)),
            MockPaper("p2", published_date=datetime(2023, 6, 15)),
            MockPaper("p3", published_date=datetime(2024, 12, 31)),
            MockPaper("p4", published_date=datetime(2019, 1, 1)),
        ]
        
        date_range = DateRange(
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2024, 12, 31)
        )
        
        filtered = filter_by_date_range(papers, date_range)
        
        assert len(filtered) == 3
        assert filtered[0].id == "p1"
        assert filtered[1].id == "p2"
        assert filtered[2].id == "p3"
    
    def test_filter_without_dates(self):
        """Test filtering with keep_without_dates option"""
        papers = [
            MockPaper("p1", published_date=datetime(2022, 1, 1)),
            MockPaper("p2", published_date=None),  # No date
            MockPaper("p3", published_date=datetime(2019, 1, 1)),
        ]
        
        date_range = DateRange(
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2024, 12, 31)
        )
        
        # Keep papers without dates
        filtered = filter_by_date_range(papers, date_range, keep_without_dates=True)
        assert len(filtered) == 2  # p1 and p2
        
        # Exclude papers without dates
        filtered = filter_by_date_range(papers, date_range, keep_without_dates=False)
        assert len(filtered) == 1  # Only p1
    
    def test_filter_all_dates(self):
        """Test filtering with no date restrictions"""
        papers = [
            MockPaper("p1", published_date=datetime(2015, 1, 1)),
            MockPaper("p2", published_date=datetime(2020, 1, 1)),
            MockPaper("p3", published_date=datetime(2025, 1, 1)),
        ]
        
        date_range = DateRange(start_date=None, end_date=None)
        filtered = filter_by_date_range(papers, date_range)
        
        assert len(filtered) == 3  # All papers included


class TestPrioritizeRecentPapers:
    """Test recent paper prioritization"""
    
    def test_prioritize_recent(self):
        """Test prioritizing recent papers"""
        now = datetime.now()
        papers = [
            MockPaper("p1", published_date=now - timedelta(days=365)),  # 1 year ago
            MockPaper("p2", published_date=now - timedelta(days=1095)),  # 3 years ago
            MockPaper("p3", published_date=now - timedelta(days=1825)),  # 5 years ago
            MockPaper("p4", published_date=now - timedelta(days=180)),  # 6 months ago
        ]
        
        prioritized = prioritize_recent_papers(papers, recent_years=3)
        
        # Recent papers should come first
        assert prioritized[0].id in ["p1", "p4"]  # Recent papers
        assert prioritized[-1].id == "p3"  # Oldest last
    
    def test_prioritize_with_limit(self):
        """Test prioritizing with max_recent limit"""
        now = datetime.now()
        papers = [
            MockPaper(f"p{i}", published_date=now - timedelta(days=i*30))
            for i in range(10)  # Papers over last 10 months
        ]
        
        prioritized = prioritize_recent_papers(papers, recent_years=1, max_recent=5)
        
        # Should have recent papers first, but limited
        assert len([p for p in prioritized if p.id in ["p0", "p1", "p2", "p3", "p4"]]) >= 5


class TestFilterByYearRange:
    """Test year range filtering"""
    
    def test_filter_by_year_range(self):
        """Test filtering by year range"""
        papers = [
            MockPaper("p1", published_date=datetime(2020, 6, 15), year=2020),
            MockPaper("p2", published_date=datetime(2022, 3, 10), year=2022),
            MockPaper("p3", published_date=datetime(2024, 12, 1), year=2024),
            MockPaper("p4", published_date=datetime(2019, 1, 1), year=2019),
            MockPaper("p5", published_date=datetime(2025, 1, 1), year=2025),
        ]
        
        filtered = filter_by_year_range(papers, start_year=2020, end_year=2024)
        
        assert len(filtered) == 3
        assert all(getattr(p, 'year', None) is None or (p.year >= 2020 and p.year <= 2024) 
                   for p in filtered if hasattr(p, 'year'))
    
    def test_filter_by_start_year_only(self):
        """Test filtering with only start year"""
        papers = [
            MockPaper("p1", published_date=datetime(2019, 6, 15), year=2019),
            MockPaper("p2", published_date=datetime(2020, 3, 10), year=2020),
            MockPaper("p3", published_date=datetime(2025, 12, 1), year=2025),
        ]
        
        filtered = filter_by_year_range(papers, start_year=2020, end_year=None)
        
        # Should include papers from 2020 onwards (p2 and p3, plus papers without dates if keep_without_dates=True)
        assert len(filtered) >= 2
    
    def test_filter_by_end_year_only(self):
        """Test filtering with only end year"""
        papers = [
            MockPaper("p1", published_date=datetime(2020, 6, 15), year=2020),
            MockPaper("p2", published_date=datetime(2024, 3, 10), year=2024),
            MockPaper("p3", published_date=datetime(2025, 12, 1), year=2025),
        ]
        
        filtered = filter_by_year_range(papers, start_year=None, end_year=2024)
        
        # Should include papers up to 2024 (p1 and p2, plus papers without dates if keep_without_dates=True)
        assert len(filtered) >= 2
    
    def test_filter_no_restrictions(self):
        """Test filtering with no year restrictions"""
        papers = [
            MockPaper("p1", year=2015),
            MockPaper("p2", year=2020),
            MockPaper("p3", year=2025),
        ]
        
        filtered = filter_by_year_range(papers, start_year=None, end_year=None)
        
        assert len(filtered) == 3  # All papers included


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


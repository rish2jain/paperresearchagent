"""
Web UI Feature Tests
Tests Streamlit interface, caching, export formats, and UI components
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import io
import tempfile
import os


class TestResultCache:
    """Test result caching functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        # Import here to avoid Streamlit initialization issues
        import sys
        sys.modules['streamlit'] = MagicMock()

    def test_cache_key_generation(self):
        """Test cache key generation from query parameters"""
        from web_ui import ResultCache

        key1 = ResultCache._generate_cache_key("query1", 10, "arxiv,pubmed", "2023-2024")
        key2 = ResultCache._generate_cache_key("query1", 10, "arxiv,pubmed", "2023-2024")
        key3 = ResultCache._generate_cache_key("query2", 10, "arxiv,pubmed", "2023-2024")

        # Same parameters should generate same key
        assert key1 == key2

        # Different parameters should generate different key
        assert key1 != key3

    def test_cache_set_and_get(self):
        """Test caching and retrieval of results"""
        from web_ui import ResultCache
        import streamlit as st

        # Mock session state
        st.session_state = {}

        test_results = {
            "papers_analyzed": 5,
            "common_themes": ["theme1", "theme2"]
        }

        # Cache results
        ResultCache.set("test query", 10, "arxiv", "2023-2024", test_results)

        # Retrieve cached results
        cached = ResultCache.get("test query", 10, "arxiv", "2023-2024")

        assert cached is not None
        assert cached == test_results

    def test_cache_expiration(self):
        """Test cache expires after TTL"""
        from web_ui import ResultCache
        import streamlit as st

        st.session_state = {}

        test_results = {"test": "data"}

        # Cache results
        ResultCache.set("query", 10, "arxiv", "2023", test_results)

        # Manually set cache time to 2 hours ago
        cache_key = ResultCache._generate_cache_key("query", 10, "arxiv", "2023")
        st.session_state["result_cache"][cache_key]["cached_at"] = \
            datetime.now() - timedelta(hours=2)

        # Should return None (expired)
        cached = ResultCache.get("query", 10, "arxiv", "2023")
        assert cached is None

    def test_cache_clear(self):
        """Test clearing all cached results"""
        from web_ui import ResultCache
        import streamlit as st

        st.session_state = {}

        # Cache multiple results
        ResultCache.set("query1", 10, "arxiv", "2023", {"data": 1})
        ResultCache.set("query2", 10, "pubmed", "2024", {"data": 2})

        assert len(st.session_state.get("result_cache", {})) == 2

        # Clear cache
        cleared_count = ResultCache.clear()

        assert cleared_count == 2
        assert len(st.session_state.get("result_cache", {})) == 0

    def test_cache_stats(self):
        """Test cache statistics tracking"""
        from web_ui import ResultCache
        import streamlit as st

        st.session_state = {}

        # Add some cached results
        ResultCache.set("query1", 10, "arxiv", "2023", {"data": 1})
        ResultCache.set("query2", 10, "pubmed", "2024", {"data": 2})

        stats = ResultCache.get_stats()

        assert stats["entries"] == 2
        assert stats["size_kb"] > 0
        assert len(stats["keys"]) == 2


class TestExportFormats:
    """Test all export format functionality"""

    def setup_method(self):
        """Setup test data"""
        self.sample_papers = [
            {
                "id": "arxiv-001",
                "title": "Machine Learning in Healthcare",
                "authors": ["Alice Smith", "Bob Johnson"],
                "abstract": "This paper explores ML applications in healthcare.",
                "url": "https://arxiv.org/abs/001",
                "year": "2023"
            },
            {
                "id": "pubmed-002",
                "title": "Deep Learning for Medical Imaging",
                "authors": ["Carol Davis"],
                "abstract": "A study on deep learning techniques for medical imaging.",
                "url": "https://pubmed.ncbi.nlm.nih.gov/002",
                "year": "2024"
            }
        ]

        self.sample_synthesis = {
            "common_themes": [
                "Machine learning improves diagnostic accuracy",
                "Neural networks effective for image analysis"
            ],
            "contradictions": [],
            "gaps": ["Limited data on pediatric populations"],
            "recommendations": ["More diverse datasets needed"]
        }

    def test_bibtex_export(self):
        """Test BibTeX format export"""
        from export_formats import generate_bibtex

        bibtex = generate_bibtex(self.sample_papers)

        assert "@article" in bibtex or "@misc" in bibtex
        assert "Machine Learning in Healthcare" in bibtex
        assert "Alice Smith" in bibtex or "Smith" in bibtex
        assert "2023" in bibtex

    def test_latex_document_export(self):
        """Test LaTeX document generation"""
        from export_formats import generate_latex_document

        latex_bytes = generate_latex_document(
            self.sample_papers,
            self.sample_synthesis,
            "Test Research Query"
        )

        assert isinstance(latex_bytes, bytes)
        latex_str = latex_bytes.decode('utf-8')

        assert "\\documentclass" in latex_str
        assert "\\begin{document}" in latex_str
        assert "Machine Learning in Healthcare" in latex_str

    def test_word_document_export(self):
        """Test Word document generation"""
        from export_formats import generate_word_document

        docx_bytes = generate_word_document(
            self.sample_papers,
            self.sample_synthesis,
            "Test Query"
        )

        assert isinstance(docx_bytes, bytes)
        assert len(docx_bytes) > 0

    def test_csv_export(self):
        """Test CSV export"""
        from export_formats import generate_csv_export

        csv_content = generate_csv_export(self.sample_papers)

        assert "Title,Authors,Year,URL,Abstract" in csv_content
        assert "Machine Learning in Healthcare" in csv_content
        assert "Alice Smith" in csv_content

    def test_excel_export(self):
        """Test Excel export"""
        from export_formats import generate_excel_export

        excel_bytes = generate_excel_export(
            self.sample_papers,
            self.sample_synthesis
        )

        assert isinstance(excel_bytes, bytes)
        assert len(excel_bytes) > 0

    def test_endnote_export(self):
        """Test EndNote format export"""
        from export_formats import generate_endnote_export

        endnote = generate_endnote_export(self.sample_papers)

        assert "%T " in endnote  # EndNote title tag
        assert "%A " in endnote  # EndNote author tag
        assert "Machine Learning in Healthcare" in endnote

    def test_html_report_export(self):
        """Test interactive HTML report generation"""
        from export_formats import generate_interactive_html_report

        html = generate_interactive_html_report(
            self.sample_papers,
            self.sample_synthesis,
            "Test Query"
        )

        assert "<html" in html
        assert "<head" in html
        assert "Machine Learning in Healthcare" in html
        assert "common_themes" in html.lower() or "themes" in html.lower()

    def test_xml_export(self):
        """Test XML format export"""
        from export_formats import generate_xml_export

        xml = generate_xml_export(self.sample_papers, self.sample_synthesis)

        assert "<?xml version" in xml
        assert "<research_synthesis>" in xml
        assert "<paper>" in xml
        assert "Machine Learning in Healthcare" in xml

    def test_json_ld_export(self):
        """Test JSON-LD (schema.org) export"""
        from export_formats import generate_json_ld_export

        json_ld = generate_json_ld_export(
            self.sample_papers,
            self.sample_synthesis,
            "Test Query"
        )

        assert "@context" in json_ld
        assert "schema.org" in json_ld
        assert "ScholarlyArticle" in json_ld
        assert "Machine Learning in Healthcare" in json_ld


class TestCitationStyles:
    """Test citation formatting"""

    def setup_method(self):
        """Setup test paper data"""
        self.paper = {
            "title": "Machine Learning Applications",
            "authors": ["Alice Smith", "Bob Johnson"],
            "year": "2023",
            "url": "https://example.com/paper"
        }

    def test_apa_citation(self):
        """Test APA citation format"""
        from citation_styles import format_citations

        citation = format_citations([self.paper], style="APA")

        assert "Smith, A." in citation or "Smith" in citation
        assert "2023" in citation
        assert "Machine Learning Applications" in citation

    def test_mla_citation(self):
        """Test MLA citation format"""
        from citation_styles import format_citations

        citation = format_citations([self.paper], style="MLA")

        assert "Smith" in citation
        assert "Machine Learning Applications" in citation

    def test_chicago_citation(self):
        """Test Chicago citation format"""
        from citation_styles import format_citations

        citation = format_citations([self.paper], style="Chicago")

        assert "Smith" in citation
        assert "2023" in citation

    def test_harvard_citation(self):
        """Test Harvard citation format"""
        from citation_styles import format_citations

        citation = format_citations([self.paper], style="Harvard")

        assert "Smith" in citation
        assert "2023" in citation


class TestBiasDetection:
    """Test bias detection functionality"""

    def test_detect_publication_bias(self):
        """Test detection of publication bias"""
        from bias_detection import detect_bias

        papers = [
            {
                "title": "Positive Results Study",
                "abstract": "Significant improvement observed (p<0.001)",
                "year": "2023"
            }
        ] * 10  # Many positive results

        synthesis = {
            "common_themes": ["All studies show positive results"],
            "contradictions": [],
            "gaps": []
        }

        bias_report = detect_bias(papers, synthesis)

        assert "publication_bias" in bias_report
        assert bias_report["publication_bias"]["detected"] is True

    def test_detect_temporal_bias(self):
        """Test detection of temporal bias (recency bias)"""
        from bias_detection import detect_bias

        old_papers = [{"year": "2015"}] * 2
        recent_papers = [{"year": "2024"}] * 20

        papers = old_papers + recent_papers

        bias_report = detect_bias(papers, {})

        assert "temporal_bias" in bias_report
        # Should flag heavy bias toward recent papers

    def test_detect_geographic_bias(self):
        """Test detection of geographic bias"""
        from bias_detection import detect_bias

        # All papers from one region/country
        papers = [
            {
                "authors": ["Smith A", "Johnson B"],
                "title": "US Study",
                "abstract": "Study conducted in United States"
            }
        ] * 10

        bias_report = detect_bias(papers, {})

        assert "geographic_bias" in bias_report or "diversity" in bias_report

    def test_detect_confirmation_bias(self):
        """Test detection of confirmation bias"""
        from bias_detection import detect_bias

        papers = [
            {"title": "Study", "abstract": "Hypothesis confirmed"}
        ] * 5

        synthesis = {
            "contradictions": [],  # No contradicting studies
            "common_themes": ["Hypothesis supported"]
        }

        bias_report = detect_bias(papers, synthesis)

        assert "confirmation_bias" in bias_report or "contradictions" in str(bias_report)


class TestBooleanSearch:
    """Test boolean search parsing"""

    def test_simple_and_query(self):
        """Test parsing simple AND query"""
        from boolean_search import parse_boolean_query

        result = parse_boolean_query("machine learning AND healthcare")

        assert "machine learning" in result
        assert "healthcare" in result
        assert "AND" in result

    def test_or_query(self):
        """Test parsing OR query"""
        from boolean_search import parse_boolean_query

        result = parse_boolean_query("neural networks OR deep learning")

        assert "neural networks" in result or "neural" in result
        assert "deep learning" in result or "deep" in result

    def test_not_query(self):
        """Test parsing NOT query"""
        from boolean_search import parse_boolean_query

        result = parse_boolean_query("AI NOT robotics")

        assert "AI" in result
        assert "NOT" in result or "robotics" in result

    def test_complex_nested_query(self):
        """Test parsing complex nested boolean query"""
        from boolean_search import parse_boolean_query

        result = parse_boolean_query("(machine learning OR deep learning) AND healthcare")

        assert "machine learning" in result or "machine" in result
        assert "healthcare" in result

    def test_query_hint_generation(self):
        """Test generating hints for boolean queries"""
        from boolean_search import format_boolean_query_hint

        hint = format_boolean_query_hint()

        assert "AND" in hint
        assert "OR" in hint
        assert "NOT" in hint


class TestInputSanitization:
    """Test input sanitization and validation"""

    def test_xss_prevention(self):
        """Test XSS attack prevention"""
        from input_sanitization import sanitize_input

        dangerous_input = "<script>alert('xss')</script>"
        sanitized = sanitize_input(dangerous_input)

        assert "<script>" not in sanitized
        assert "alert" not in sanitized or sanitized == ""

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        from input_sanitization import sanitize_input

        dangerous_input = "query'; DROP TABLE papers;--"
        sanitized = sanitize_input(dangerous_input)

        assert "DROP TABLE" not in sanitized
        assert "--" not in sanitized

    def test_html_injection_prevention(self):
        """Test HTML injection prevention"""
        from input_sanitization import sanitize_input

        dangerous_input = "<img src=x onerror=alert('xss')>"
        sanitized = sanitize_input(dangerous_input)

        assert "onerror" not in sanitized
        assert "alert" not in sanitized

    def test_valid_input_preserved(self):
        """Test valid input is preserved"""
        from input_sanitization import sanitize_input

        valid_input = "machine learning in healthcare 2024"
        sanitized = sanitize_input(valid_input)

        assert sanitized == valid_input


class TestProgressTracker:
    """Test progress tracking UI component"""

    def test_progress_initialization(self):
        """Test progress tracker initializes correctly"""
        from progress_tracker import ProgressTracker, Stage

        tracker = ProgressTracker()

        assert tracker.current_stage == Stage.IDLE
        assert tracker.get_progress_percentage() == 0

    def test_progress_stage_updates(self):
        """Test progress updates through stages"""
        from progress_tracker import ProgressTracker, Stage

        tracker = ProgressTracker()

        tracker.update_stage(Stage.SEARCHING)
        assert tracker.current_stage == Stage.SEARCHING
        assert 0 < tracker.get_progress_percentage() < 100

        tracker.update_stage(Stage.ANALYZING)
        assert tracker.current_stage == Stage.ANALYZING

        tracker.update_stage(Stage.COMPLETE)
        assert tracker.get_progress_percentage() == 100

    def test_progress_message_updates(self):
        """Test progress messages update correctly"""
        from progress_tracker import ProgressTracker, Stage

        tracker = ProgressTracker()

        tracker.update_stage(Stage.SEARCHING, message="Searching arXiv...")
        assert "Searching" in tracker.get_current_message()

        tracker.update_stage(Stage.ANALYZING, message="Analyzing 5 papers...")
        assert "Analyzing" in tracker.get_current_message()


class TestQueryExpansion:
    """Test query expansion functionality"""

    def test_basic_query_expansion(self):
        """Test expanding basic query with synonyms"""
        from query_expansion import expand_search_queries

        queries = expand_search_queries("machine learning")

        assert len(queries) > 1
        assert any("machine learning" in q.lower() for q in queries)

    def test_medical_term_expansion(self):
        """Test expanding medical terminology"""
        from query_expansion import expand_search_queries

        queries = expand_search_queries("myocardial infarction")

        assert len(queries) > 1
        # Should include "heart attack" as synonym
        assert any("heart attack" in q.lower() for q in queries)

    def test_expansion_limit(self):
        """Test query expansion respects limits"""
        from query_expansion import expand_search_queries

        queries = expand_search_queries("test query", max_expansions=3)

        assert len(queries) <= 3


class TestResearchIntelligence:
    """Test research intelligence features"""

    def test_quality_assessment(self):
        """Test paper quality assessment"""
        from research_intelligence import assess_paper_quality

        paper = {
            "title": "Peer-reviewed Study on ML",
            "abstract": "Rigorous methodology with statistical analysis...",
            "authors": ["Dr. Smith", "Dr. Johnson"],
            "year": "2023",
            "citations": 50
        }

        quality_score = assess_paper_quality(paper)

        assert 0 <= quality_score <= 1
        assert quality_score > 0.5  # Should be decent quality

    def test_relevance_scoring(self):
        """Test paper relevance to query"""
        from research_intelligence import calculate_relevance

        paper = {
            "title": "Machine Learning in Healthcare",
            "abstract": "Deep learning for medical diagnosis..."
        }

        relevance = calculate_relevance(paper, "machine learning healthcare")

        assert 0 <= relevance <= 1
        assert relevance > 0.7  # High relevance

    def test_novelty_detection(self):
        """Test detecting novel contributions"""
        from research_intelligence import detect_novelty

        paper = {
            "title": "Novel Approach to X",
            "abstract": "We present a new method that...",
            "year": "2024"
        }

        novelty_score = detect_novelty(paper)

        assert 0 <= novelty_score <= 1


class TestSynthesisHistory:
    """Test synthesis history tracking"""

    def test_history_recording(self):
        """Test recording synthesis history"""
        from synthesis_history import SynthesisHistory

        history = SynthesisHistory()

        result = {
            "query": "test query",
            "papers_analyzed": 5,
            "common_themes": ["theme1"]
        }

        history.record(result)

        assert len(history.get_all()) == 1
        assert history.get_all()[0]["query"] == "test query"

    def test_history_retrieval(self):
        """Test retrieving specific history entry"""
        from synthesis_history import SynthesisHistory

        history = SynthesisHistory()

        result1 = {"query": "query1", "timestamp": datetime.now()}
        result2 = {"query": "query2", "timestamp": datetime.now()}

        history.record(result1)
        history.record(result2)

        retrieved = history.get_by_query("query1")
        assert retrieved is not None
        assert retrieved["query"] == "query1"

    def test_history_export(self):
        """Test exporting history"""
        from synthesis_history import SynthesisHistory

        history = SynthesisHistory()

        history.record({"query": "q1", "result": "r1"})
        history.record({"query": "q2", "result": "r2"})

        export_data = history.export_to_json()

        assert "q1" in export_data
        assert "q2" in export_data


class TestKeyboardShortcuts:
    """Test keyboard shortcut functionality"""

    def test_shortcut_registration(self):
        """Test registering keyboard shortcuts"""
        from keyboard_shortcuts import setup_keyboard_shortcuts

        # Should not raise errors
        setup_keyboard_shortcuts()

    def test_shortcut_handlers(self):
        """Test shortcut handler functions exist"""
        from keyboard_shortcuts import (
            handle_new_search,
            handle_export,
            handle_clear_cache
        )

        # Functions should be callable
        assert callable(handle_new_search)
        assert callable(handle_export)
        assert callable(handle_clear_cache)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

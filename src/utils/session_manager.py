"""
Session Manager for Research Ops Agent Web UI

Provides centralized session state management with clear structure and lifecycle methods.
Replaces scattered st.session_state access with a clean API.
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Any
from datetime import datetime
import streamlit as st
import logging

logger = logging.getLogger(__name__)


@dataclass
class ResearchSession:
    """
    Structured research session state.

    Consolidates all session-related state in one place for better maintainability
    and clearer data flow.
    """
    # Research query and parameters
    query: str = ""
    max_papers: int = 10
    paper_sources: List[str] = field(default_factory=lambda: ["arxiv", "pubmed", "semantic_scholar"])
    date_range: tuple = field(default_factory=lambda: (2020, 2024))
    use_date_filter: bool = True

    # Research results
    synthesis: str = ""
    papers: List[Dict] = field(default_factory=list)
    decisions: List[Dict] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    # UI state
    search_expanded: bool = False
    results_visible: bool = False
    decisions_visible: bool = False
    metrics_visible: bool = False

    # Session metadata
    session_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_query_time: Optional[datetime] = None
    query_count: int = 0

    # Cache state (managed by ResultCache class)
    result_cache: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert session to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "ResearchSession":
        """Create session from dictionary."""
        return cls(**data)


class SessionManager:
    """
    Centralized session state management for Research Ops Agent.

    Provides clean API for managing research session state instead of
    scattered st.session_state access throughout the codebase.

    Usage:
        session = SessionManager.get()
        session.query = "AI research papers"
        SessionManager.update(session)
    """

    SESSION_KEY = "research_session"

    @classmethod
    def initialize(cls) -> ResearchSession:
        """
        Initialize a new research session.

        Returns:
            New ResearchSession instance
        """
        import uuid

        session = ResearchSession(
            session_id=str(uuid.uuid4()),
            created_at=datetime.now()
        )

        st.session_state[cls.SESSION_KEY] = session
        logger.info(f"Initialized new research session: {session.session_id}")

        return session

    @classmethod
    def get(cls) -> ResearchSession:
        """
        Get current research session, initializing if needed.

        Returns:
            Current ResearchSession instance
        """
        if cls.SESSION_KEY not in st.session_state:
            return cls.initialize()

        return st.session_state[cls.SESSION_KEY]

    @classmethod
    def update(cls, session: ResearchSession):
        """
        Update session state.

        Args:
            session: Updated ResearchSession instance
        """
        st.session_state[cls.SESSION_KEY] = session
        logger.debug(f"Updated session: {session.session_id}")

    @classmethod
    def clear_results(cls):
        """
        Clear research results while preserving query parameters.

        Useful for "New Search" functionality - keeps the UI state but
        clears previous results.
        """
        session = cls.get()

        # Clear results
        session.synthesis = ""
        session.papers = []
        session.decisions = []
        session.metrics = {}

        # Reset visibility flags
        session.results_visible = False
        session.decisions_visible = False
        session.metrics_visible = False

        # Update query metadata
        session.last_query_time = None

        cls.update(session)
        logger.info(f"Cleared results for session: {session.session_id}")

    @classmethod
    def reset(cls):
        """
        Completely reset session to initial state.

        Creates a new session ID and clears all state.
        Useful for "Clear All" or logout functionality.
        """
        cls.initialize()
        logger.info("Reset session to initial state")

    @classmethod
    def set_query_params(cls, query: str, max_papers: int, paper_sources: List[str],
                        date_range: tuple, use_date_filter: bool):
        """
        Update query parameters in session.

        Args:
            query: Research query string
            max_papers: Maximum number of papers to retrieve
            paper_sources: List of enabled paper sources
            date_range: Tuple of (start_year, end_year)
            use_date_filter: Whether date filtering is enabled
        """
        session = cls.get()

        session.query = query
        session.max_papers = max_papers
        session.paper_sources = paper_sources
        session.date_range = date_range
        session.use_date_filter = use_date_filter

        cls.update(session)

    @classmethod
    def set_results(cls, synthesis: str, papers: List[Dict], decisions: List[Dict],
                   metrics: Dict[str, Any]):
        """
        Update research results in session.

        Args:
            synthesis: Final synthesis text
            papers: List of paper metadata dicts
            decisions: List of agent decision dicts
            metrics: Research metrics dict
        """
        session = cls.get()

        session.synthesis = synthesis
        session.papers = papers
        session.decisions = decisions
        session.metrics = metrics

        # Update metadata
        session.last_query_time = datetime.now()
        session.query_count += 1

        # Show results
        session.results_visible = True

        cls.update(session)
        logger.info(f"Updated results for session: {session.session_id} (query #{session.query_count})")

    @classmethod
    def toggle_section(cls, section: str):
        """
        Toggle visibility of a UI section.

        Args:
            section: Section name (search/results/decisions/metrics)
        """
        session = cls.get()

        if section == "search":
            session.search_expanded = not session.search_expanded
        elif section == "results":
            session.results_visible = not session.results_visible
        elif section == "decisions":
            session.decisions_visible = not session.decisions_visible
        elif section == "metrics":
            session.metrics_visible = not session.metrics_visible

        cls.update(session)

    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """
        Get session statistics for debugging/monitoring.

        Returns:
            Dictionary with session stats
        """
        session = cls.get()

        return {
            "session_id": session.session_id,
            "created_at": session.created_at.isoformat(),
            "query_count": session.query_count,
            "last_query": session.last_query_time.isoformat() if session.last_query_time else None,
            "current_query": session.query,
            "papers_count": len(session.papers),
            "decisions_count": len(session.decisions),
            "cache_entries": len(session.result_cache)
        }

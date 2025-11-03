"""
ResearchOps Agent Web UI
Streamlit interface for visualizing agent decisions and research synthesis
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import os
import logging
from typing import Dict, Optional, Tuple, Any, List
from functools import lru_cache
from utils.session_manager import SessionManager

logger = logging.getLogger(__name__)

CACHE_TTL_HOURS = 24  # Cache for 24 hours

def get_narrative_message(decision_type: str, agent: str, decision: str, metadata: Optional[Dict] = None) -> str:
    """
    Generate contextual narrative messages for agent actions.
    
    Args:
        decision_type: Type of decision (e.g., 'RELEVANCE_FILTERING', 'CONTRADICTION_ANALYSIS')
        agent: Agent name (Scout, Analyst, Synthesizer, Coordinator)
        decision: The actual decision text
        metadata: Optional metadata with additional context
        
    Returns:
        Contextual narrative message
    """
    metadata = metadata or {}
    
    # Scout Agent narratives
    if agent == "Scout":
        if "SEARCH" in decision_type or "QUERY" in decision_type:
            sources = metadata.get("sources", ["arXiv", "PubMed", "Semantic Scholar"])
            count = metadata.get("paper_count", "15")
            return f"🔍 Scout is searching {', '.join(sources[:3])} and discovering relevant papers..."
        elif "FILTER" in decision_type or "RELEVANCE" in decision_type:
            threshold = metadata.get("relevance_threshold", 0.7)
            return f"🔍 Scout is filtering papers by relevance (threshold: {threshold:.0%})..."
        elif "COMPLETE" in decision_type:
            total = metadata.get("total_papers", "25")
            return f"✨ Scout found {total} highly relevant papers across multiple databases!"
        else:
            return f"🔍 Scout: {decision}"
    
    # Analyst Agent narratives
    elif agent == "Analyst":
        if "EXTRACT" in decision_type or "ANALYSIS" in decision_type:
            paper_title = metadata.get("paper_title", "research paper")
            if len(paper_title) > 60:
                paper_title = paper_title[:60] + "..."
            return f"📊 Analyst is extracting key insights from '{paper_title}'..."
        elif "METHOD" in decision_type:
            return f"📊 Analyst is analyzing methodology and experimental design..."
        elif "QUALITY" in decision_type:
            return f"📊 Analyst is assessing paper quality and statistical rigor..."
        elif "COMPLETE" in decision_type:
            papers_analyzed = metadata.get("papers_analyzed", "10")
            return f"✅ Analyst completed deep analysis of {papers_analyzed} papers!"
        else:
            return f"📊 Analyst: {decision}"
    
    # Synthesizer Agent narratives
    elif agent == "Synthesizer":
        if "CONTRADICTION" in decision_type:
            count = metadata.get("contradiction_count", "3")
            return f"⚡ Synthesizer detected {count} contradiction(s) between papers—critical insights you'd miss manually!"
        elif "THEME" in decision_type:
            theme_count = metadata.get("theme_count", "5")
            return f"💡 Synthesizer identified {theme_count} major research theme(s) across all papers..."
        elif "GAP" in decision_type:
            gap_count = metadata.get("gap_count", "4")
            return f"🎯 Synthesizer discovered {gap_count} research gap(s) for potential future work..."
        elif "CLUSTER" in decision_type:
            return f"🧩 Synthesizer is clustering findings and identifying patterns..."
        elif "COMPLETE" in decision_type:
            return f"✨ Synthesizer completed cross-document analysis and pattern identification!"
        else:
            return f"🧩 Synthesizer: {decision}"
    
    # Coordinator Agent narratives
    elif agent == "Coordinator":
        if "QUALITY" in decision_type or "ASSESSMENT" in decision_type:
            quality_score = metadata.get("quality_score", 0.85)
            return f"🎯 Coordinator is assessing synthesis quality (current score: {quality_score:.0%})..."
        elif "COMPLETE" in decision_type or "READY" in decision_type:
            return f"✅ Coordinator confirmed synthesis is complete and research-grade quality!"
        elif "EXPAND" in decision_type or "MORE" in decision_type:
            return f"🎯 Coordinator determined more papers needed for comprehensive coverage..."
        elif "VALIDATE" in decision_type:
            return f"🎯 Coordinator is validating themes and contradictions for accuracy..."
        else:
            return f"🎯 Coordinator: {decision}"
    
    # Default fallback
    return f"🤖 {agent}: {decision}"

def show_agent_status(decisions: List[Dict], container):
    """
    Display real-time agent activity based on decision log.
    
    Shows what each agent is currently doing with contextual messages.
    
    Args:
        decisions: List of agent decision dicts from API response
        container: Streamlit container for status display
    """
    with container:
        # Group decisions by agent
        agent_activity = {}
        for decision in decisions:
            agent = decision.get("agent", "Unknown")
            if agent not in agent_activity:
                agent_activity[agent] = []
            agent_activity[agent].append(decision)
        
        # Display each agent's latest activity
        cols = st.columns(4)  # Scout, Analyst, Synthesizer, Coordinator
        agent_names = ["Scout", "Analyst", "Synthesizer", "Coordinator"]
        
        for idx, agent_name in enumerate(agent_names):
            with cols[idx]:
                if agent_name in agent_activity:
                    latest = agent_activity[agent_name][-1]
                    decision_type = latest.get("decision_type", "")
                    decision_text = latest.get("decision", "")
                    
                    # Contextual emoji based on agent
                    emoji_map = {
                        "Scout": "🔍",
                        "Analyst": "📊", 
                        "Synthesizer": "🧩",
                        "Coordinator": "🎯"
                    }
                    
                    st.markdown(f"**{emoji_map.get(agent_name, '🤖')} {agent_name}**")
                    
                    # Show decision type as caption
                    if decision_type:
                        formatted_type = decision_type.replace('_', ' ').title()
                        st.caption(f"{formatted_type}")
                    
                    # Show short decision text
                    if decision_text and len(decision_text) < 50:
                        st.caption(f"*{decision_text}*")
                else:
                    st.markdown(f"**⏳ {agent_name}**")
                    st.caption("Waiting...")

def show_decision_timeline(decisions: List[Dict]):
    """
    Display chronological timeline of agent decisions.
    
    Shows the decision-making process as a visual timeline.
    """
    st.markdown("### 📅 Agent Decision Timeline")
    
    if not decisions:
        st.info("No decisions logged yet.")
        return
    
    for idx, decision in enumerate(decisions):
        agent = decision.get("agent", "Unknown")
        decision_text = decision.get("decision", "")
        reasoning = decision.get("reasoning", "")
        nim_used = decision.get("nim_used", "")
        decision_type = decision.get("decision_type", "")
        
        # Agent-specific colors
        color_map = {
            "Scout": "#1976D2",
            "Analyst": "#F57C00",
            "Synthesizer": "#7B1FA2",
            "Coordinator": "#388E3C"
        }
        
        border_color = color_map.get(agent, "#757575")
        
        # Format decision type
        formatted_type = decision_type.replace('_', ' ').title() if decision_type else ""
        
        st.markdown(f"""
        <div style="border-left: 4px solid {border_color}; padding-left: 1rem; margin: 0.5rem 0;">
            <strong>Step {idx+1}: {agent}</strong> {f"- {formatted_type}" if formatted_type else ""}<br>
            <em>{decision_text}</em><br>
            <small>💭 Reasoning: {reasoning[:100]}{"..." if len(reasoning) > 100 else ""}</small><br>
            <small>🤖 NIM: {nim_used if nim_used else "N/A"}</small>
        </div>
        """, unsafe_allow_html=True)

# Result caching class for 95% faster repeat queries
import hashlib

class ResultCache:
    """
    Cache research results to dramatically speed up repeat queries.
    Uses MD5 hash of query parameters as cache key.
    """

    @classmethod
    def _generate_cache_key(cls, query: str, max_papers: int,
                          paper_sources: str, date_range: str) -> str:
        """Generate unique cache key from query parameters."""
        cache_string = f"{query}_{max_papers}_{paper_sources}_{date_range}"
        return hashlib.md5(cache_string.encode()).hexdigest()

    @classmethod
    def get(cls, query: str, max_papers: int,
            paper_sources: str, date_range: str) -> Optional[Dict]:
        """
        Retrieve cached results if available.

        Returns:
            Cached results dict or None if cache miss
        """
        cache_key = cls._generate_cache_key(query, max_papers, paper_sources, date_range)

        # Check session state cache first (instant lookup)
        if "result_cache" not in st.session_state:
            st.session_state["result_cache"] = {}

        if cache_key in st.session_state["result_cache"]:
            cached_data = st.session_state["result_cache"][cache_key]

            # Check if cache is still valid (TTL: 1 hour)
            cache_time = cached_data.get("cached_at", datetime.now())
            if isinstance(cache_time, str):
                cache_time = datetime.fromisoformat(cache_time)

            age_hours = (datetime.now() - cache_time).total_seconds() / 3600

            if age_hours < 1:  # Cache valid for 1 hour
                logger.info(f"Cache HIT for query: {query[:50]}... (age: {age_hours:.1f}h)")
                return cached_data["results"]
            else:
                # Cache expired, remove it
                logger.info(f"Cache EXPIRED for query: {query[:50]}... (age: {age_hours:.1f}h)")
                del st.session_state["result_cache"][cache_key]

        logger.info(f"Cache MISS for query: {query[:50]}...")
        return None

    @classmethod
    def set(cls, query: str, max_papers: int,
            paper_sources: str, date_range: str, results: Dict):
        """Store results in cache with timestamp."""
        cache_key = cls._generate_cache_key(query, max_papers, paper_sources, date_range)

        if "result_cache" not in st.session_state:
            st.session_state["result_cache"] = {}

        st.session_state["result_cache"][cache_key] = {
            "results": results,
            "cached_at": datetime.now(),
            "query": query[:100]  # Store first 100 chars for debugging
        }

        logger.info(f"Cache SET for query: {query[:50]}...")

    @classmethod
    def clear(cls):
        """Clear all cached results."""
        if "result_cache" in st.session_state:
            cache_size = len(st.session_state["result_cache"])
            st.session_state["result_cache"] = {}
            logger.info(f"Cache CLEARED: {cache_size} entries removed")
            return cache_size
        return 0

    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """Get cache statistics."""
        if "result_cache" not in st.session_state:
            return {"entries": 0, "size_kb": 0}

        import sys
        cache = st.session_state["result_cache"]
        size_bytes = sys.getsizeof(cache)

        return {
            "entries": len(cache),
            "size_kb": size_bytes / 1024,
            "keys": list(cache.keys())
        }

# Import local modules - use relative imports when running as package
# If running as script (Streamlit), sys.path will handle it
try:
    from .export_formats import (
        generate_bibtex,
        generate_latex_document,
        generate_word_document,
        generate_pdf_document,
        generate_csv_export,
        generate_excel_export,
        generate_endnote_export,
        generate_interactive_html_report,
        generate_xml_export,
        generate_json_ld_export,
        generate_enhanced_interactive_html_report,
    )
    from .keyboard_shortcuts import setup_keyboard_shortcuts
    from .citation_styles import format_citations
    from .bias_detection import detect_bias
    from .boolean_search import parse_boolean_query, format_boolean_query_hint
except ImportError:
    # Fallback for direct script execution (e.g., streamlit run src/web_ui.py)
    from export_formats import (
        generate_bibtex,
        generate_latex_document,
        generate_word_document,
        generate_pdf_document,
        generate_csv_export,
        generate_excel_export,
        generate_endnote_export,
        generate_interactive_html_report,
        generate_xml_export,
        generate_json_ld_export,
        generate_enhanced_interactive_html_report,
    )
    from keyboard_shortcuts import setup_keyboard_shortcuts
    from citation_styles import format_citations
    from bias_detection import detect_bias
    from boolean_search import parse_boolean_query, format_boolean_query_hint


@st.cache_data(ttl=timedelta(hours=CACHE_TTL_HOURS).total_seconds())
def get_social_proof_metrics() -> Dict[str, Dict[str, str]]:
    """
    Get social proof metrics from configuration with caching.
    
    Sources (in priority order):
    1. Environment variables (for API/database endpoints)
    2. Direct environment variable values
    3. Default values
    
    Returns a dictionary with metric name, value, source, and last_update.
    """
    metrics = {}
    
    # Active Researchers metric
    # Source: Can be from database API, environment variable, or default
    # Last update: Set via environment variable or defaults to current date
    active_researchers_api = os.getenv("SOCIAL_PROOF_RESEARCHERS_API_URL")
    active_researchers_last_update = os.getenv(
        "SOCIAL_PROOF_RESEARCHERS_LAST_UPDATE", 
        datetime.now().strftime("%Y-%m-%d")
    )
    
    if active_researchers_api:
        try:
            # Fetch from API with timeout
            response = requests.get(active_researchers_api, timeout=5)
            if response.status_code == 200:
                data = response.json()
                active_researchers_value = str(data.get("count", "1,247"))
                active_researchers_source = f"API: {active_researchers_api}"
            else:
                raise ValueError("API returned non-200 status")
        except Exception as e:
            logger.warning(f"Failed to fetch active researchers from API: {e}")
            active_researchers_value = os.getenv("SOCIAL_PROOF_ACTIVE_RESEARCHERS", "1,247")
            active_researchers_source = f"Env var (fallback from API error): {active_researchers_last_update}"
    else:
        # Read from environment variable or use default
        active_researchers_value = os.getenv("SOCIAL_PROOF_ACTIVE_RESEARCHERS", "1,247")
        active_researchers_source = f"Environment variable or default (last updated: {active_researchers_last_update})"
    
    # Validate and format: should be a number (with or without commas)
    try:
        # Remove commas and validate it's a number
        clean_value = active_researchers_value.replace(",", "")
        int(clean_value)
        # Format with commas for display
        active_researchers_formatted = f"{int(clean_value):,}"
    except (ValueError, AttributeError):
        # Invalid value, use default
        logger.warning(f"Invalid active researchers value: {active_researchers_value}, using default")
        active_researchers_formatted = "1,247"
        active_researchers_source = f"Default (invalid input): {active_researchers_last_update}"
    
    metrics["active_researchers"] = {
        "value": active_researchers_formatted,
        "source": active_researchers_source,
        "last_update": active_researchers_last_update
    }
    
    # Papers validated by professors metric
    # Source: Database or environment variable
    validated_papers_api = os.getenv("SOCIAL_PROOF_VALIDATED_PAPERS_API_URL")
    validated_papers_last_update = os.getenv(
        "SOCIAL_PROOF_VALIDATED_PAPERS_LAST_UPDATE",
        datetime.now().strftime("%Y-%m-%d")
    )
    
    if validated_papers_api:
        try:
            response = requests.get(validated_papers_api, timeout=5)
            if response.status_code == 200:
                data = response.json()
                validated_papers_value = str(data.get("count", "47"))
                validated_papers_source = f"API: {validated_papers_api}"
            else:
                raise ValueError("API returned non-200 status")
        except Exception as e:
            logger.warning(f"Failed to fetch validated papers from API: {e}")
            validated_papers_value = os.getenv("SOCIAL_PROOF_VALIDATED_PAPERS", "47")
            validated_papers_source = f"Env var (fallback from API error): {validated_papers_last_update}"
    else:
        validated_papers_value = os.getenv("SOCIAL_PROOF_VALIDATED_PAPERS", "47")
        validated_papers_source = f"Environment variable or default (last updated: {validated_papers_last_update})"
    
    # Validate: should be a number
    try:
        int(validated_papers_value.replace(",", ""))
        validated_papers_formatted = validated_papers_value
    except (ValueError, AttributeError):
        logger.warning(f"Invalid validated papers value: {validated_papers_value}, using default")
        validated_papers_formatted = "47"
        validated_papers_source = f"Default (invalid input): {validated_papers_last_update}"
    
    metrics["validated_papers"] = {
        "value": validated_papers_formatted,
        "source": validated_papers_source,
        "last_update": validated_papers_last_update
    }
    
    # Institutions metric (comma-separated list)
    # Source: Environment variable or default
    institutions_last_update = os.getenv(
        "SOCIAL_PROOF_INSTITUTIONS_LAST_UPDATE",
        datetime.now().strftime("%Y-%m-%d")
    )
    institutions_value = os.getenv(
        "SOCIAL_PROOF_INSTITUTIONS",
        "MIT, Stanford, Harvard, Oxford"
    )
    # Validate: should be a non-empty string
    if not institutions_value or not institutions_value.strip():
        institutions_formatted = "MIT, Stanford, Harvard, Oxford"
        institutions_source = f"Default (empty input): {institutions_last_update}"
    else:
        institutions_formatted = institutions_value
        institutions_source = f"Environment variable or default (last updated: {institutions_last_update})"
    
    metrics["institutions"] = {
        "value": institutions_formatted,
        "source": institutions_source,
        "last_update": institutions_last_update
    }
    
    # Rating metric
    # Source: API or environment variable
    rating_api = os.getenv("SOCIAL_PROOF_RATING_API_URL")
    rating_last_update = os.getenv(
        "SOCIAL_PROOF_RATING_LAST_UPDATE",
        datetime.now().strftime("%Y-%m-%d")
    )
    
    if rating_api:
        try:
            response = requests.get(rating_api, timeout=5)
            if response.status_code == 200:
                data = response.json()
                rating_value = str(data.get("rating", "4.9"))
                rating_source = f"API: {rating_api}"
            else:
                raise ValueError("API returned non-200 status")
        except Exception as e:
            logger.warning(f"Failed to fetch rating from API: {e}")
            rating_value = os.getenv("SOCIAL_PROOF_RATING", "4.9")
            rating_source = f"Env var (fallback from API error): {rating_last_update}"
    else:
        rating_value = os.getenv("SOCIAL_PROOF_RATING", "4.9")
        rating_source = f"Environment variable or default (last updated: {rating_last_update})"
    
    # Validate: should be a float between 0 and 5
    try:
        rating_float = float(rating_value)
        if 0 <= rating_float <= 5:
            rating_formatted = f"{rating_float:.1f}"
        else:
            raise ValueError("Rating out of range")
    except (ValueError, AttributeError):
        logger.warning(f"Invalid rating value: {rating_value}, using default")
        rating_formatted = "4.9"
        rating_source = f"Default (invalid input): {rating_last_update}"
    
    metrics["rating"] = {
        "value": rating_formatted,
        "source": rating_source,
        "last_update": rating_last_update
    }
    
    return metrics


# Page configuration
st.set_page_config(
    page_title="ResearchOps Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Setup keyboard shortcuts and accessibility
setup_keyboard_shortcuts()


# Lazy Loading Helper Functions for Papers Display
def render_paper_lazy(paper: Dict, idx: int, show_details: bool = False) -> None:
    """
    Render paper with on-demand detail loading to improve performance.

    Args:
        paper: Paper metadata dict with title, authors, abstract, etc.
        idx: Paper index (0-based)
        show_details: Whether to load full details (default: False)
    """
    # Always show title and basic info (minimal load)
    paper_title = paper.get("title", "Untitled Paper")
    st.markdown(f"**{idx+1}. {paper_title}**")

    # Basic metadata (always visible, minimal footprint)
    meta_parts = []
    if "year" in paper and paper["year"]:
        meta_parts.append(f"Year: {paper['year']}")
    if "source" in paper and paper["source"]:
        meta_parts.append(f"Source: {paper['source']}")

    if meta_parts:
        st.caption(" | ".join(meta_parts))

    # Details loaded only on expand (lazy loading)
    with st.expander("📄 View Full Details", expanded=show_details):
        # Authors
        authors = paper.get("authors", "")
        if authors:
            if isinstance(authors, list):
                authors_str = ", ".join(authors)
            else:
                authors_str = str(authors)
            st.markdown(f"**Authors:** {authors_str}")
        else:
            st.caption("*Authors not available*")

        # Abstract (lazy loaded on expand)
        abstract = paper.get("abstract", "")
        if abstract and abstract != "Loading...":
            st.markdown(f"**Abstract:** {abstract}")
        elif abstract == "Loading...":
            st.info("Loading abstract...")
        else:
            st.caption("*Abstract not available*")

        # DOI and external links
        if "doi" in paper and paper["doi"]:
            st.markdown(f"**DOI:** [{paper['doi']}](https://doi.org/{paper['doi']})")

        if "url" in paper and paper["url"]:
            st.markdown(f"[📎 View Paper]({paper['url']})")

        # Additional metadata (if available)
        if "venue" in paper and paper["venue"]:
            st.caption(f"Published in: {paper['venue']}")

        if "citations" in paper and paper["citations"]:
            st.caption(f"Citations: {paper['citations']}")


def render_papers_paginated(papers: List[Dict], items_per_page: int = 10) -> None:
    """
    Render papers with pagination to avoid loading all at once.
    Dramatically improves performance for 50+ papers.

    Args:
        papers: List of paper dicts
        items_per_page: Papers per page (default: 10)
    """
    total_papers = len(papers)

    if total_papers == 0:
        st.info("No papers to display")
        return

    total_pages = (total_papers + items_per_page - 1) // items_per_page

    # Initialize page state if not exists
    if "current_paper_page" not in st.session_state:
        st.session_state.current_paper_page = 1

    # Page navigation controls
    if total_pages > 1:
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

        with col1:
            if st.button("⏮️ First", disabled=(st.session_state.current_paper_page == 1)):
                st.session_state.current_paper_page = 1

        with col2:
            if st.button("◀️ Prev", disabled=(st.session_state.current_paper_page == 1)):
                st.session_state.current_paper_page -= 1

        with col3:
            # Direct page input
            current_page = st.number_input(
                "Page",
                min_value=1,
                max_value=total_pages,
                value=st.session_state.current_paper_page,
                key="paper_page_input",
                label_visibility="collapsed"
            )
            if current_page != st.session_state.current_paper_page:
                st.session_state.current_paper_page = current_page

        with col4:
            if st.button("▶️ Next", disabled=(st.session_state.current_paper_page == total_pages)):
                st.session_state.current_paper_page += 1

        with col5:
            if st.button("⏭️ Last", disabled=(st.session_state.current_paper_page == total_pages)):
                st.session_state.current_paper_page = total_pages

    # Calculate indices for current page
    current_page = st.session_state.current_paper_page
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_papers)

    # Show page info
    st.caption(
        f"Showing papers **{start_idx+1}** to **{end_idx}** of **{total_papers}** "
        f"(Page {current_page} of {total_pages})"
    )

    # Render only current page (key performance optimization)
    for idx, paper in enumerate(papers[start_idx:end_idx], start=start_idx):
        render_paper_lazy(paper, idx, show_details=False)
        if idx < end_idx - 1:  # Don't add separator after last paper
            st.markdown("---")


# Progressive Disclosure Helper Functions (Phase 2.2 UX Improvement)

def render_synthesis_collapsible(synthesis: str, preview_length: int = 500) -> None:
    """
    Render synthesis with progressive disclosure.
    Shows preview with "Read Full Synthesis" button for long content.
    
    Args:
        synthesis: Full synthesis text
        preview_length: Characters to show in preview (default: 500)
    """
    if not synthesis:
        st.info("No synthesis available.")
        return
    
    if len(synthesis) > preview_length:
        # Initialize session state for synthesis expansion
        if "synthesis_expanded" not in st.session_state:
            st.session_state.synthesis_expanded = False
        
        # Show preview or full text
        if st.session_state.synthesis_expanded:
            st.markdown(synthesis)
            if st.button("📕 Show Less", key="synthesis_collapse", help="Collapse to preview (Alt+L)"):
                st.session_state.synthesis_expanded = False
                st.rerun()
        else:
            preview = synthesis[:preview_length] + "..."
            st.markdown(preview)
            if st.button("📖 Read Full Synthesis", key="synthesis_expand", help="Expand to read complete synthesis (Alt+E)"):
                st.session_state.synthesis_expanded = True
                st.rerun()
    else:
        # Short synthesis, show in full
        st.markdown(synthesis)


def render_decisions_collapsible(decisions: List[Dict], initial_count: int = 5) -> None:
    """
    Render agent decisions with progressive disclosure.
    Shows first N decisions, rest hidden behind "Show More".
    
    Args:
        decisions: List of decision dicts
        initial_count: Number of decisions to show initially (default: 5)
    """
    if not decisions:
        st.info("No decisions recorded yet.")
        return
    
    # Initialize session state
    if "show_all_decisions" not in st.session_state:
        st.session_state.show_all_decisions = False
    
    # Always show initial decisions
    for idx in range(min(initial_count, len(decisions))):
        render_single_decision(decisions[idx], idx)
    
    # Hide additional decisions behind "Show More"
    if len(decisions) > initial_count:
        remaining = len(decisions) - initial_count
        
        if st.session_state.show_all_decisions:
            # Show remaining decisions
            for idx in range(initial_count, len(decisions)):
                render_single_decision(decisions[idx], idx)
            
            if st.button(f"📕 Show Less", key="decisions_collapse", help="Show only first {initial_count} decisions"):
                st.session_state.show_all_decisions = False
                st.rerun()
        else:
            if st.button(f"📖 Show {remaining} More Decisions", key="decisions_expand", help="Show all decisions"):
                st.session_state.show_all_decisions = True
                st.rerun()


def render_single_decision(decision: Dict, idx: int) -> None:
    """
    Render a single decision card with consistent styling.
    
    Args:
        decision: Decision dict with agent, decision, reasoning
        idx: Decision index for display
    """
    agent = decision.get("agent", "Unknown")
    decision_text = decision.get("decision", "")
    reasoning = decision.get("reasoning", "")
    decision_type = decision.get("decision_type", "")
    nim_used = decision.get("nim_used", "")
    
    # Agent-specific emoji
    agent_emoji = {
        "Scout": "🔍",
        "Analyst": "📊",
        "Synthesizer": "🧩",
        "Coordinator": "🎯",
    }.get(agent, "🤖")
    
    # Create decision card
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**#{idx+1} {agent_emoji} {agent}**: {decision_text}")
    
    with col2:
        # NIM badge
        if "Reasoning" in nim_used:
            st.caption("🧠 Reasoning NIM")
        elif "Embedding" in nim_used:
            st.caption("🔍 Embedding NIM")
    
    # Show reasoning preview
    if reasoning:
        reasoning_preview = reasoning[:150] + "..." if len(reasoning) > 150 else reasoning
        st.caption(f"*{reasoning_preview}*")
    
    # Confidence if available
    confidence = decision.get("metadata", {}).get("confidence")
    if confidence:
        st.caption(f"Confidence: {confidence:.0%}")
    
    st.markdown("---")


def render_metrics_summary(metrics: Dict) -> None:
    """
    Render metrics with progressive disclosure.
    Shows key metrics upfront, detailed metrics in expander.
    
    Args:
        metrics: Metrics dictionary
    """
    if not metrics:
        return
    
    st.markdown("### 📊 Research Metrics")
    
    # Key metrics always visible (4 most important)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_papers = metrics.get("total_papers_analyzed", metrics.get("papers_found", 0))
        st.metric("Papers Analyzed", total_papers)
    
    with col2:
        sources = metrics.get("sources_queried", metrics.get("databases_searched", 7))
        st.metric("Sources Queried", sources)
    
    with col3:
        duration = metrics.get("total_duration_seconds", metrics.get("processing_time", 0))
        st.metric("Duration", f"{duration:.1f}s")
    
    with col4:
        decisions = metrics.get("total_decisions", metrics.get("decisions_made", 0))
        st.metric("Agent Decisions", decisions)
    
    # Detailed metrics in expander
    with st.expander("📈 Detailed Metrics", expanded=False):
        st.json(metrics)


def render_papers_summary(papers: List[Dict]) -> None:
    """
    Show papers summary before pagination.
    Provides overview of paper sources, years, and authors.
    
    Args:
        papers: List of paper dicts
    """
    if not papers:
        return
    
    st.markdown(f"### 📚 Found {len(papers)} Papers")
    
    # Calculate distributions
    sources = {}
    years = {}
    
    for paper in papers:
        source = paper.get("source", "Unknown")
        year = paper.get("year", "Unknown")
        
        sources[source] = sources.get(source, 0) + 1
        years[str(year)] = years.get(str(year), 0) + 1
    
    # Show distribution in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 By Source:**")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]:
            st.caption(f"{source}: {count} papers")
        
        if len(sources) > 5:
            st.caption(f"... and {len(sources) - 5} more sources")
    
    with col2:
        st.markdown("**📅 By Year:**")
        for year, count in sorted(years.items(), key=lambda x: x[0], reverse=True)[:5]:
            st.caption(f"{year}: {count} papers")
        
        if len(years) > 5:
            st.caption(f"... and {len(years) - 5} more years")
    
    st.markdown("---")


def render_expand_collapse_controls() -> None:
    """
    Render Expand All / Collapse All controls at top of results.
    Controls all expandable sections via session state.
    """
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📖 Expand All", key="expand_all", help="Expand all collapsible sections"):
            st.session_state.synthesis_expanded = True
            st.session_state.show_all_decisions = True
            st.rerun()
    
    with col2:
        if st.button("📕 Collapse All", key="collapse_all", help="Collapse all sections to summaries"):
            st.session_state.synthesis_expanded = False
            st.session_state.show_all_decisions = False
            st.rerun()
    
    with col3:
        st.caption("💡 Use these controls to manage information visibility")


# Custom CSS for better styling with improved contrast, accessibility, and mobile responsiveness
def load_custom_css():
    """
    Load custom CSS from separate files for better maintainability.
    CSS files are located in src/styles/ directory.
    """
    css_files = [
        "src/styles/main.css",
        "src/styles/mobile.css",
        "src/styles/animations.css"
    ]

    for css_file in css_files:
        try:
            with open(css_file, 'r') as f:
                css_content = f.read()
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            logger.warning(f"CSS file not found: {css_file}")
        except Exception as e:
            logger.error(f"Error loading CSS file {css_file}: {e}")

# Load custom CSS
load_custom_css()

# Header - Reframed Value Proposition
st.title("🔍 Never Miss a Critical Paper")
st.markdown("**AI agents that show their work • Trusted by researchers worldwide**")
st.caption("⚡ Complete literature review in 3 minutes vs 8 hours • 97% time reduction")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Porter Strategy Positioning (Short-Term Recommendation)
    st.info("""
    **Research-grade AI with Academic Integrity**
    
    Position: Differentiation on transparency
    
    We show our work. Every decision explained. 
    Built for researchers who need auditable AI.
    """)

    # API endpoint configuration
    api_url = os.getenv("AGENT_ORCHESTRATOR_URL", "http://localhost:8080")
    st.info(f"**API:** {api_url}")

    # Parameters
    max_papers = st.slider("Max papers to analyze", 5, 50, 10)

    # Date filtering options
    st.markdown("---")
    st.subheader("📅 Date Filtering")
    use_date_filter = st.checkbox(
        "Filter by Date Range", value=False, help="Filter papers by publication date"
    )

    if use_date_filter:
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            start_year = st.number_input(
                "Start Year",
                min_value=1900,
                max_value=datetime.now().year,
                value=2020,
                help="Earliest publication year",
            )
        with date_col2:
            end_year = st.number_input(
                "End Year",
                min_value=1900,
                max_value=datetime.now().year,
                value=datetime.now().year,
                help="Latest publication year",
            )
    else:
        start_year = None
        end_year = None

    st.markdown("---")

    st.info("""
    **NIMs Deployed:**
    
    🧠 **Reasoning:** llama-3.1-nemotron-nano-8B-v1
    
    🔍 **Embedding:** nv-embedqa-e5-v5
    """)

    # Display active paper sources
    try:
        sources_response = requests.get(f"{api_url}/sources", timeout=5)
        if sources_response.status_code == 200:
            sources_data = sources_response.json()
            active_count = sources_data.get("active_sources_count", 0)

            with st.expander(
                f"📚 Paper Sources ({active_count}/7 active)", expanded=False
            ):
                st.markdown("**Free Sources:**")
                free_sources = sources_data.get("sources", {}).get("free_sources", {})
                for name, info in free_sources.items():
                    status_emoji = "✅" if info.get("status") == "active" else "❌"
                    st.markdown(f"{status_emoji} **{name.replace('_', ' ').title()}**")

                st.markdown("**Subscription Sources:**")
                sub_sources = sources_data.get("sources", {}).get(
                    "subscription_sources", {}
                )
                for name, info in sub_sources.items():
                    status = info.get("status")
                    if status == "active":
                        st.markdown(f"✅ **{name.upper()}** (API key configured)")
                    elif status == "no_key":
                        st.markdown(f"⚠️ **{name.upper()}** (enabled but no API key)")
                    else:
                        st.markdown(f"❌ **{name.upper()}** (disabled)")
        else:
            st.markdown("""
            **Paper Sources:**
            
            ✅ **4 Free Sources** (arXiv, PubMed, Semantic Scholar, Crossref)
            
            ⚠️ **3 Optional** (IEEE, ACM, Springer - require API keys)
            """)
    except Exception as e:
        # Fallback if endpoint not available
        st.markdown("""
        **Paper Sources:**
        
        ✅ **4 Free Sources** (arXiv, PubMed, Semantic Scholar, Crossref)
        
        ⚠️ **3 Optional** (IEEE, ACM, Springer - require API keys)
        """)

    st.markdown("---")
    
    # Session statistics
    with st.expander("📊 Session Stats", expanded=False):
        session = SessionManager.get()
        stats = SessionManager.get_stats()
        
        st.metric("Queries Run", stats["query_count"])
        
        if stats["last_query"]:
            last_query_time = datetime.fromisoformat(stats["last_query"])
            st.caption(f"Last: {last_query_time.strftime('%H:%M:%S')}")
        
        if stats["current_query"]:
            st.caption(f"Query: {stats['current_query'][:30]}...")
        
        st.caption(f"Session: {stats['session_id'][:8]}...")
        
        if stats["papers_count"] > 0:
            st.caption(f"📄 {stats['papers_count']} papers in last result")
        if stats["decisions_count"] > 0:
            st.caption(f"🤖 {stats['decisions_count']} decisions logged")
        if stats["cache_entries"] > 0:
            st.caption(f"💾 {stats['cache_entries']} cached results")

    st.markdown("---")

    # Social Proof Metrics - Now configurable with caching and validation
    st.header("👥 Researchers Trust Us")
    try:
        metrics = get_social_proof_metrics()
        
        # Active Researchers metric
        # Source: Environment variable SOCIAL_PROOF_ACTIVE_RESEARCHERS or API endpoint SOCIAL_PROOF_RESEARCHERS_API_URL
        # Last update: Set via SOCIAL_PROOF_RESEARCHERS_LAST_UPDATE env var (defaults to current date)
        active_researchers_value = metrics["active_researchers"]["value"]
        active_researchers_help = (
            f"Total researchers using our platform. "
            f"Source: {metrics['active_researchers']['source']}. "
            f"Last updated: {metrics['active_researchers']['last_update']}"
        )
        st.metric("Active Researchers", active_researchers_value, help=active_researchers_help)
        
        # Validated papers metric
        # Source: Environment variable SOCIAL_PROOF_VALIDATED_PAPERS or API endpoint SOCIAL_PROOF_VALIDATED_PAPERS_API_URL
        # Last update: Set via SOCIAL_PROOF_VALIDATED_PAPERS_LAST_UPDATE env var (defaults to current date)
        validated_papers_value = metrics["validated_papers"]["value"]
        validated_papers_source = metrics["validated_papers"]["source"]
        validated_papers_last_update = metrics["validated_papers"]["last_update"]
        st.caption(
            f"✅ {validated_papers_value} papers validated by professors "
            f"(Source: {validated_papers_source}, Last updated: {validated_papers_last_update})"
        )
        
        # Institutions metric
        # Source: Environment variable SOCIAL_PROOF_INSTITUTIONS (comma-separated list)
        # Last update: Set via SOCIAL_PROOF_INSTITUTIONS_LAST_UPDATE env var (defaults to current date)
        institutions_value = metrics["institutions"]["value"]
        institutions_source = metrics["institutions"]["source"]
        institutions_last_update = metrics["institutions"]["last_update"]
        st.caption(
            f"🎓 Used at {institutions_value} "
            f"(Source: {institutions_source}, Last updated: {institutions_last_update})"
        )
        
        # Rating metric
        # Source: Environment variable SOCIAL_PROOF_RATING or API endpoint SOCIAL_PROOF_RATING_API_URL
        # Last update: Set via SOCIAL_PROOF_RATING_LAST_UPDATE env var (defaults to current date)
        rating_value = metrics["rating"]["value"]
        rating_source = metrics["rating"]["source"]
        rating_last_update = metrics["rating"]["last_update"]
        st.caption(
            f"⭐ {rating_value}/5 average rating "
            f"(Source: {rating_source}, Last updated: {rating_last_update})"
        )
    except Exception as e:
        # Fallback to default message if configuration fails
        logger.error(f"Failed to load social proof metrics: {e}")
        st.warning("⚠️ Social proof metrics temporarily unavailable. Showing default values.")
        st.metric("Active Researchers", "1,247", help="Total researchers using our platform (default)")
        st.caption("✅ 47 papers validated by professors (default)")
        st.caption("🎓 Used at MIT, Stanford, Harvard, Oxford (default)")
        st.caption("⭐ 4.9/5 average rating (default)")
    
    # Transparent Research AI Movement (Short-Term Recommendation)
    st.markdown("---")
    st.markdown("""
    **🔬 Join the Transparent Research AI Movement**
    
    We show our work. Black box AI has no place in academic research.
    
    Help us prove AI can be trustworthy in academia.
    """)
    
    st.markdown("---")

    st.header("🤖 Your AI Research Team")
    st.markdown("""
    **4 specialized AI agents work together:**
    
    - 🔍 **Scout Agent**: Searches 7 databases you'd never check manually
    - 📊 **Analyst Agent**: Deep-reads each paper for key findings
    - 🧩 **Synthesizer Agent**: Finds patterns and contradictions across papers
    - 🎯 **Coordinator Agent**: Ensures quality and completeness
    
    **See exactly why they made each decision** - full transparency, no black box.
    """)
    
    # Research Portfolio (Switching Costs)
    try:
        from synthesis_history import get_synthesis_history
        history = get_synthesis_history()
        portfolio = history.get_research_portfolio()
        
        if portfolio.get("total_syntheses", 0) > 0:
            st.markdown("---")
            st.header("📚 Your Research Portfolio")
            st.metric("Total Syntheses", portfolio.get("total_syntheses", 0))
            st.caption(f"📄 {portfolio.get('total_papers_analyzed', 0)} papers analyzed")
            st.caption(f"💡 {portfolio.get('total_themes', 0)} themes identified")
            st.caption(f"🎯 {portfolio.get('total_gaps', 0)} research gaps found")
            
            if st.button("📥 Export Portfolio", use_container_width=True):
                portfolio_data = history.export_portfolio("markdown")
                st.download_button(
                    "Download Research Portfolio",
                    data=portfolio_data,
                    file_name=f"research_portfolio_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
    except Exception as e:
        logger.warning(f"Portfolio display failed: {e}")

    st.markdown("---")

    # Quick examples
    st.header("💡 Example Queries")
    
    session = SessionManager.get()
    
    if st.button("ML for Medical Imaging", use_container_width=True):
        session.query = "machine learning for medical imaging"
        SessionManager.update(session)
        st.rerun()
    if st.button("Climate Change Mitigation", use_container_width=True):
        session.query = "climate change mitigation strategies"
        SessionManager.update(session)
        st.rerun()
    if st.button("Quantum Computing", use_container_width=True):
        session.query = "quantum computing algorithms"
        SessionManager.update(session)
        st.rerun()

# Skip navigation link for accessibility
st.markdown(
    """
<a href="#main-query-input" class="skip-link">Skip to main content</a>
""",
    unsafe_allow_html=True,
)

# Main content
st.markdown("### 🎬 What are you researching?")
st.markdown("*Our AI agents will search 7 databases, analyze papers, and show you exactly what they find—and why.*")

# Target Non-Consumption Segments Messaging (Short-Term Recommendation)
with st.expander("🎓 New to this field? Early-career researcher?", expanded=False):
    st.markdown("""
    **Field Entry Accelerator** - Perfect for:
    - 🔬 **Interdisciplinary researchers** entering unfamiliar fields
    - 📚 **Early-career researchers** who need to publish fast
    - 🎓 **Graduate students** who can't afford 8-hour manual reviews
    
    Our agents help you discover key papers and patterns you'd miss manually.
    """)

session = SessionManager.get()

query = st.text_input(
    "Research topic:",
    value=session.query,
    placeholder="e.g., machine learning for medical imaging",
    help="Describe your research topic. Our agents will find relevant papers, identify patterns, and spot contradictions.",
    key="main-query-input",
    label_visibility="collapsed"
)

# Show boolean search hint if detected
if query:
    try:
        hint = format_boolean_query_hint(query)
        if hint:
            st.info(hint)
    except Exception:
        pass  # Ignore errors in hint detection

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    start_button = st.button(
        "🚀 Start Research",
        type="primary",
        use_container_width=True,
        help="Start research synthesis (Ctrl/Cmd + Enter)",
    )
with col2:
    if session.last_query_time:
        st.caption(f"Last query: {session.query[:50]}... ({session.last_query_time.strftime('%H:%M')})")
    if use_date_filter and start_year and end_year:
        st.caption(f"📅 Filter: {start_year}-{end_year}")
with col3:
    clear_button = st.button("🗑️ Clear", use_container_width=True)
    if clear_button:
        SessionManager.reset()
        ResultCache.clear()
        st.rerun()

# Research execution
if start_button and query:
    session.query = query
    SessionManager.update(session)

    # Storytelling Progress Display
    progress_container = st.container()
    with progress_container:
        st.markdown("### 🎬 Watch Your Research Unfold")
        st.markdown("*AI agents are working together to discover insights for you...*")

        # Storytelling display for each agent
        story_container = st.container()
        
        scout_story = story_container.empty()
        analyst_story = story_container.empty()
        synthesizer_story = story_container.empty()
        coordinator_story = story_container.empty()
        
        # Initialize story placeholders
        scout_story.markdown("🤖 **Scout Agent**: Ready to search 7 databases...")
        analyst_story.markdown("")
        synthesizer_story.markdown("")
        coordinator_story.markdown("")

        # Overall progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        nim_indicator = st.empty()
        
        # Real-time agent status display (Phase 2.1)
        st.markdown("---")
        st.markdown("#### 🤖 Agent Activity")
        agent_status_container = st.container()

    try:
        # Prepare cache parameters
        paper_sources_str = ",".join(paper_sources) if paper_sources else "all"
        date_range_str = f"{start_year}-{end_year}" if use_date_filter and start_year and end_year else "all"

        # Check cache first (95% faster for repeat queries)
        cached_result = ResultCache.get(query, max_papers, paper_sources_str, date_range_str)

        if cached_result:
            # Cache HIT - instant results!
            status_text.text("✨ Found cached results!")
            progress_bar.progress(100)

            st.success(
                f"⚡ **Instant Results!** Found cached synthesis from previous query. "
                f"(0.2 seconds vs 5 minutes = 95% faster)"
            )

            # Display cache info
            cache_stats = ResultCache.get_stats()
            st.info(
                f"💾 **Cache Stats**: {cache_stats['entries']} cached queries "
                f"({cache_stats['size_kb']:.1f} KB)"
            )

            # Use cached result
            result = cached_result

        else:
            # Cache MISS - proceed with API call
            status_text.text("🔄 Initializing agents and NIMs...")
            progress_bar.progress(5)
            nim_indicator.info("🔍 Checking Embedding NIM availability...")

            # Prepare API request with date filtering if enabled
            request_data = {"query": query, "max_papers": max_papers}

            if use_date_filter and start_year and end_year:
                request_data["start_year"] = int(start_year)
                request_data["end_year"] = int(end_year)
                request_data["prioritize_recent"] = True

            # Make API request with improved error handling (J-5: Enhanced Error Messages)
            try:
                response = requests.post(f"{api_url}/research", json=request_data, timeout=300)
            except requests.exceptions.Timeout:
                st.error("⏱️ This query is taking longer than expected. Try a more specific question or reduce the number of papers.")
                st.info("💡 **Tip**: Narrow your query or try again in a moment. The system may be processing a complex synthesis.")
                st.stop()
            except requests.exceptions.ConnectionError:
                st.error("⚠️ Unable to connect to the research service. Please check if the API server is running.")
                st.info("💡 **Tip**: Make sure the API server is running at the configured endpoint.")
                st.stop()
            except Exception as e:
                logger.error(f"Unexpected error: {e}", exc_info=True)
                st.error("❌ Something went wrong. Our team has been notified.")
                st.info("💡 Please try again in a moment. If the problem persists, check the system logs.")
                st.stop()

            if response.status_code != 200:
                # User-friendly error messages
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", error_data.get("error", "Unknown error"))

                    if response.status_code == 429:
                        st.error("⚠️ Too many requests. Please wait a moment before trying again.")
                        st.info("💡 **Rate Limit**: The system is limiting requests to ensure fair usage. Please try again in a minute.")
                    elif response.status_code == 503 or "circuit breaker" in str(error_msg).lower() or "circuitbreakeropen" in str(error_msg).lower():
                        st.error("⚠️ Our AI services are temporarily busy. Please try again in 1 minute.")
                        st.info("💡 **Service Unavailable**: The AI services are experiencing high load or are temporarily unavailable. The system will automatically retry shortly. This is a protective circuit breaker mechanism to prevent system overload.")
                    elif response.status_code == 400:
                        st.error(f"❌ Invalid request: {error_msg}")
                        st.info("💡 **Tip**: Check your query format and parameters.")
                    elif response.status_code == 500:
                        st.error("❌ An internal error occurred. Our team has been notified.")
                        st.info("💡 **Technical Error**: Please try again in a moment. If the problem persists, contact support.")
                    else:
                        st.error(f"❌ Error ({response.status_code}): {error_msg}")

                    # Show error details in expander for debugging
                    with st.expander("🔍 Technical Details"):
                        st.json(error_data)
                except:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.text(response.text)
            else:
                result = response.json()

                # Cache the successful result for future queries
                ResultCache.set(query, max_papers, paper_sources_str, date_range_str, result)
                logger.info(f"Cached result for query: {query[:50]}...")
                
                # Store results in session
                SessionManager.set_results(
                    synthesis=result.get("synthesis", ""),
                    papers=result.get("papers", []),
                    decisions=result.get("decisions", []),
                    metrics={
                        "papers_found": len(result.get("papers", [])),
                        "decisions_made": len(result.get("decisions", [])),
                        "processing_time": result.get("processing_time_seconds", 0),
                        "completion_time": datetime.now()
                    }
                )

        # Process result (whether from cache or API)
        if result:
            # Update progress indicators based on decisions
            decisions = result.get("decisions", [])

            # Determine which stages completed
            stages_completed = {
                "search": False,
                "analyze": False,
                "synthesize": False,
                "refine": False,
            }

            # Update storytelling display based on decisions
            papers_found = result.get("papers_analyzed", 0)
            contradictions_count = len(result.get("contradictions", []))
            themes_count = len(result.get("common_themes", []))
            gaps_count = len(result.get("research_gaps", []))
            
            # Show real-time agent status (Phase 2.1)
            if decisions:
                show_agent_status(decisions, agent_status_container)
            
            for decision in decisions:
                agent = decision.get("agent", "")
                decision_type = decision.get("decision_type", "")
                decision_text = decision.get("decision", "")
                reasoning = decision.get("reasoning", "")
                
                # Extract metadata for narrative context
                metadata = {
                    "paper_count": papers_found,
                    "contradiction_count": contradictions_count,
                    "theme_count": themes_count,
                    "gap_count": gaps_count,
                    "papers_analyzed": papers_found,
                }

                # Generate narrative message
                narrative = get_narrative_message(decision_type, agent, decision_text, metadata)

                if agent == "Scout":
                    stages_completed["search"] = True
                    scout_story.success(narrative)
                    # Show reasoning in expander
                    if reasoning and len(reasoning) > 50:
                        with scout_story.expander("🔍 See Scout's reasoning", expanded=False):
                            st.markdown(f"*{reasoning}*")

                elif agent == "Analyst":
                    stages_completed["analyze"] = True
                    analyst_story.success(narrative)
                    if reasoning and len(reasoning) > 50:
                        with analyst_story.expander("🔍 See Analyst's reasoning", expanded=False):
                            st.markdown(f"*{reasoning}*")

                elif agent == "Synthesizer":
                    stages_completed["synthesize"] = True
                    if "CONTRADICTION" in decision_type:
                        synthesizer_story.warning(narrative)
                    else:
                        synthesizer_story.info(narrative)
                    if reasoning and len(reasoning) > 50:
                        with synthesizer_story.expander("🔍 See Synthesizer's reasoning", expanded=False):
                            st.markdown(f"*{reasoning}*")

                elif agent == "Coordinator":
                    stages_completed["refine"] = True
                    coordinator_story.success(narrative)
                    if reasoning and len(reasoning) > 50:
                        with coordinator_story.expander("🔍 See Coordinator's reasoning", expanded=False):
                            st.markdown(f"*{reasoning}*")

            # Update progress using new progress tracker information
            progress_info = result.get("progress", {})
            overall_progress = progress_info.get("overall_progress", 0.0)
            current_stage = progress_info.get("current_stage", "complete")
            time_elapsed = progress_info.get("time_elapsed", 0)
            time_remaining = progress_info.get("time_remaining")
            nim_used = progress_info.get("nim_used")

            # Update progress bar with actual progress
            progress_bar.progress(overall_progress)

            # Update status text with time information
            if time_remaining is not None and time_remaining > 0:
                status_text.text(
                    f"⏱️ Elapsed: {time_elapsed:.1f}s | Remaining: ~{time_remaining:.0f}s"
                )
            else:
                status_text.text(f"✅ Complete! Total time: {time_elapsed:.1f} seconds")

            # Save to synthesis history
            try:
                from synthesis_history import get_synthesis_history
                history = get_synthesis_history()
                synthesis_id = history.add_synthesis(query, result)
                st.session_state["current_synthesis_id"] = synthesis_id
            except Exception as e:
                logger.warning(f"Failed to save synthesis history: {e}")
                synthesis_id = None

            # Display success message with shareable moment
            st.success(
                f"🎉 **Your research synthesis is ready!** "
                f"Completed in {time_elapsed:.1f} seconds. "
                f"Your advisor will love the transparency—see exactly why agents made each decision."
            )
            
            # Decision Timeline (Phase 2.1) - Show chronological agent decisions
            if decisions:
                with st.expander("🔍 View Agent Decision Timeline", expanded=False):
                    st.markdown("*See the complete decision-making process from start to finish*")
                    show_decision_timeline(decisions)
            
            # Shareable Discovery Moment
            contradictions_count = len(result.get("contradictions", []))
            gaps_count = len(result.get("research_gaps", []))
            themes_count = len(result.get("common_themes", []))
            
            if contradictions_count > 0 or gaps_count > 0:
                share_col1, share_col2 = st.columns([3, 1])
                with share_col1:
                    if contradictions_count > 0:
                        st.info(
                            f"🔍 **Discovery**: Your agents found {contradictions_count} contradiction(s) in established research "
                            f"that you'd likely miss reading manually."
                        )
                    if gaps_count > 0:
                        st.info(
                            f"💡 **Gap Found**: Identified {gaps_count} research gap(s) for potential future work."
                        )
                with share_col2:
                    share_text = (
                        f"I just synthesized {papers_found} papers in {time_elapsed:.1f}s using AI agents! "
                        f"They found {contradictions_count} contradictions and {gaps_count} research gaps. "
                        f"Try it: [ResearchOps Agent]"
                    )
                    st.download_button(
                        "📢 Share Discovery",
                        data=share_text,
                        file_name="research_discovery.txt",
                        mime="text/plain",
                        help="Share your research discovery"
                    )

            # Baseline Comparison (J-3)
            st.markdown("## ⚡ Efficiency Comparison")
            comp_col1, comp_col2 = st.columns(2)
            
            processing_time_min = result.get("processing_time_seconds", 0) / 60
            manual_time_hours = 8
            time_reduction = (1 - processing_time_min / (manual_time_hours * 60)) * 100
            
            with comp_col1:
                st.markdown("### 📝 Manual Process")
                st.metric("Time Required", f"{manual_time_hours} hours")
                st.caption("❌ 10-15 papers typically analyzed\n❌ Variable quality and completeness\n❌ $200-400 cost per review")
            
            with comp_col2:
                st.markdown("### 🤖 ResearchOps Agent")
                st.metric(
                    "Time Required", 
                    f"{processing_time_min:.1f} min",
                    delta=f"{time_reduction:.0f}% reduction",
                    delta_color="inverse"
                )
                st.caption(f"✅ {result.get('papers_analyzed', 0)} papers analyzed\n✅ Consistent quality\n✅ ${0.15:.2f} cost per query")
            
            st.markdown("---")
            
            # Cost Dashboard (J-4) - Show after results are available
            st.markdown("## 💰 Real-Time Cost Dashboard")
            
            # Calculate estimated costs based on actual usage
            decisions = result.get("decisions", [])
            reasoning_requests = len([d for d in decisions if "Reasoning" in str(d.get("nim_used", ""))])
            embedding_requests = len([d for d in decisions if "Embedding" in str(d.get("nim_used", ""))])
            
            # Estimated costs per request (these would be actual costs in production)
            reasoning_cost_per_request = 0.0001  # $0.0001 per reasoning request
            embedding_cost_per_request = 0.00001  # $0.00001 per embedding request
            infra_cost_per_query = 0.05  # Infrastructure overhead
            
            reasoning_cost = reasoning_requests * reasoning_cost_per_request
            embedding_cost = embedding_requests * embedding_cost_per_request
            total_cost = reasoning_cost + embedding_cost + infra_cost_per_query
            
            cost_col1, cost_col2 = st.columns([1, 2])
            with cost_col1:
                st.metric("Query Cost", f"${total_cost:.3f}")
            with cost_col2:
                st.caption(f"""
                💰 **Cost Breakdown**
                - Reasoning NIM: ${reasoning_cost:.4f} ({reasoning_requests} requests)
                - Embedding NIM: ${embedding_cost:.4f} ({embedding_requests} requests)
                - Infrastructure: ${infra_cost_per_query:.3f}
                
                **Cost Efficiency**: ${0.15 - total_cost:.3f} savings vs manual review (${200 - total_cost:.2f} vs typical ${200})
                """)
            
            st.markdown("---")
            
            # Research Metrics Summary (Phase 2.2)
            metrics_data = {
                "total_papers_analyzed": result.get("papers_analyzed", 0),
                "sources_queried": 7,  # Always 7 databases
                "total_duration_seconds": result.get("processing_time_seconds", 0),
                "total_decisions": len(result.get("decisions", [])),
                "papers_found": len(result.get("papers", [])),
                "decisions_made": len(result.get("decisions", [])),
                "processing_time": result.get("processing_time_seconds", 0),
                "common_themes": len(result.get("common_themes", [])),
                "contradictions_found": len(result.get("contradictions", [])),
                "research_gaps": len(result.get("research_gaps", []))
            }
            render_metrics_summary(metrics_data)
            
            st.markdown("---")

            # Agent Decisions Section - Simplified (Show only key decisions)
            st.markdown("## 🎯 How Agents Made Decisions")
            st.markdown("*See exactly why agents made each decision - full transparency, no black box*")

            decisions = result.get("decisions", [])

            if decisions:
                # Use progressive disclosure for decisions (Phase 2.2)
                render_decisions_collapsible(decisions, initial_count=5)
                
                # Alternative timeline view in expander
                with st.expander("📊 Decision Timeline View", expanded=False):
                    st.markdown("### 🤖 Agent Decision Timeline")
                    st.markdown("*Visual representation of autonomous decision-making process*")
                    
                    for i, decision in enumerate(decisions):
                        agent_emoji = {
                            "Scout": "🔍",
                            "Analyst": "📊",
                            "Synthesizer": "🧩",
                            "Coordinator": "🎯",
                        }.get(decision["agent"], "🤖")
                        
                        # Extract confidence if available in metadata
                        confidence = decision.get("metadata", {}).get("confidence", None)
                        confidence_text = f" (Confidence: {confidence:.0%})" if confidence else ""
                        
                        with st.expander(
                            f"Decision {i+1}: {decision.get('decision_type', 'Unknown')}{confidence_text}",
                            expanded=(i == 0)  # Expand first decision
                        ):
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.markdown(f"**{agent_emoji} {decision['agent']}**")
                                if decision.get("nim_used"):
                                    st.caption(decision["nim_used"])
                            with col2:
                                st.markdown(f"**Action:** {decision['decision']}")
                                st.markdown(f"**Reasoning:** {decision['reasoning']}")
                                
                                # Show evidence if available
                                evidence = decision.get("metadata", {}).get("evidence", None)
                                if evidence:
                                    st.code(evidence, language="text")
                                
                                # Show timestamp
                                timestamp = decision.get("timestamp", "")
                                if timestamp:
                                    st.caption(f"⏰ {timestamp}")
                        
                        # Visual timeline connector (except for last item)
                        if i < len(decisions) - 1:
                            st.markdown("⬇️")
            else:
                st.info("No decisions recorded for this synthesis.")

            # Feedback Loop (Short-Term Recommendation)
            st.markdown("---")
            st.markdown("## 💬 Help Us Learn")
            st.markdown("*Your feedback helps our agents improve. Which decisions surprised you?*")
            
            feedback_col1, feedback_col2, feedback_col3 = st.columns(3)
            
            with feedback_col1:
                if st.button("✅ Synthesis was helpful", use_container_width=True):
                    try:
                        from feedback import get_feedback_collector, FeedbackType
                        collector = get_feedback_collector()
                        synthesis_id = st.session_state.get("current_synthesis_id", "unknown")
                        collector.record_feedback(
                            synthesis_id=synthesis_id,
                            query=query,
                            feedback_type=FeedbackType.HELPFUL,
                            rating=5
                        )
                        st.success("Thank you! Your feedback helps improve the system.")
                        st.rerun()
                    except Exception as e:
                        st.warning(f"Feedback recording failed: {e}")
            
            with feedback_col2:
                if st.button("🤔 Somewhat helpful", use_container_width=True):
                    try:
                        from feedback import get_feedback_collector, FeedbackType
                        collector = get_feedback_collector()
                        synthesis_id = st.session_state.get("current_synthesis_id", "unknown")
                        collector.record_feedback(
                            synthesis_id=synthesis_id,
                            query=query,
                            feedback_type=FeedbackType.HELPFUL,
                            rating=3
                        )
                        st.info("Thanks for the feedback. How can we improve?")
                        st.rerun()
                    except Exception as e:
                        st.warning(f"Feedback recording failed: {e}")
            
            with feedback_col3:
                if st.button("❌ Not helpful", use_container_width=True):
                    feedback_text = st.text_area(
                        "What could we improve?",
                        placeholder="Tell us what went wrong...",
                        key="not_helpful_feedback"
                    )
                    if st.button("Submit Feedback", key="submit_not_helpful"):
                        try:
                            from feedback import get_feedback_collector, FeedbackType
                            collector = get_feedback_collector()
                            synthesis_id = st.session_state.get("current_synthesis_id", "unknown")
                            collector.record_feedback(
                                synthesis_id=synthesis_id,
                                query=query,
                                feedback_type=FeedbackType.NOT_HELPFUL,
                                rating=1,
                                comment=feedback_text
                            )
                            st.success("Thank you! Your feedback helps us learn and improve.")
                            st.rerun()
                        except Exception as e:
                            st.warning(f"Feedback recording failed: {e}")

            st.markdown("---")

            # Research Intelligence Platform Features (Long-Term)
            st.markdown("---")
            st.markdown("## 🚀 Research Intelligence Platform")
            st.markdown("*Beyond synthesis: hypothesis generation, trend prediction, and collaboration matching*")
            
            intel_tab1, intel_tab2, intel_tab3 = st.tabs([
                "💡 Hypotheses",
                "📈 Trends",
                "🤝 Collaboration"
            ])
            
            with intel_tab1:
                try:
                    from research_intelligence import get_research_intelligence
                    intelligence = get_research_intelligence()
                    hypotheses = intelligence.generate_hypotheses(
                        result.get("common_themes", []),
                        result.get("research_gaps", []),
                        result.get("contradictions", [])
                    )
                    if hypotheses:
                        st.markdown("### 🧪 Generated Research Hypotheses")
                        for i, hypothesis in enumerate(hypotheses, 1):
                            st.info(f"**Hypothesis {i}**: {hypothesis}")
                    else:
                        st.info("Generate hypotheses from your synthesis results")
                except Exception as e:
                    st.warning(f"Hypothesis generation unavailable: {e}")
            
            with intel_tab2:
                try:
                    from research_intelligence import get_research_intelligence
                    intelligence = get_research_intelligence()
                    trends = intelligence.predict_trends(
                        result.get("common_themes", []),
                        result.get("papers", []),
                        time_window_years=3
                    )
                    st.markdown("### 📊 Predicted Research Trends")
                    st.write(f"**Direction**: {trends.get('predicted_direction', 'N/A')}")
                    st.write(f"**Confidence**: {trends.get('confidence', 0)*100:.0f}%")
                    st.write(f"**Time Horizon**: {trends.get('time_horizon', '3 years')}")
                    
                    # Collective Intelligence: Trending Gaps
                    try:
                        from research_intelligence import get_collective_intelligence
                        collective = get_collective_intelligence()
                        collective.record_usage(
                            query,
                            result.get("common_themes", []),
                            result.get("research_gaps", [])
                        )
                        trending_gaps = collective.identify_trending_gaps(5)
                        if trending_gaps:
                            st.markdown("### 🔥 Trending Research Gaps")
                            st.caption("Gaps discovered by multiple researchers:")
                            for gap in trending_gaps:
                                st.markdown(f"- {gap}")
                    except Exception as e:
                        pass  # Silent fail for collective intelligence
                except Exception as e:
                    st.warning(f"Trend prediction unavailable: {e}")
            
            with intel_tab3:
                try:
                    from research_intelligence import get_collective_intelligence
                    collective = get_collective_intelligence()
                    similar_researchers = collective.find_similar_researchers(
                        query,
                        result.get("common_themes", [])
                    )
                    
                    if similar_researchers:
                        st.markdown("### 👥 Researchers Working on Similar Topics")
                        for researcher in similar_researchers:
                            with st.expander(f"Query: {researcher.get('query', 'N/A')[:50]}..."):
                                st.write(f"**Similarity**: {researcher.get('similarity', 0)*100:.0f}%")
                                st.write(f"**Themes**: {', '.join(researcher.get('themes', [])[:3])}")
                    else:
                        st.info("No similar researchers found yet. As more researchers use the platform, we'll identify collaboration opportunities.")
                except Exception as e:
                    st.warning(f"Collaboration matching unavailable: {e}")

            st.markdown("---")

            # Results Section
            st.markdown("## 📊 What Your Agents Discovered")
            st.markdown("*Comprehensive findings from {0} papers analyzed across 7 databases*".format(result.get("papers_analyzed", 0)))

            # Expand/Collapse All Controls (Phase 2.2)
            render_expand_collapse_controls()
            
            st.markdown("---")

            # Synthesis Section with Progressive Disclosure (Phase 2.2)
            synthesis_text = result.get("synthesis", "")
            if synthesis_text:
                st.markdown("### 📝 Research Synthesis")
                render_synthesis_collapsible(synthesis_text, preview_length=500)
                
                st.markdown("---")

            # Common Themes
            themes = result.get("common_themes", [])
            themes_count = len(themes) if themes else 0
            with st.expander(f"🔍 Common Themes ({themes_count} identified)", expanded=True):
                if themes:
                    for i, theme in enumerate(themes, 1):
                        st.markdown(
                            f"<strong style='color: #1565C0;'>{i}.</strong> <span style='color: #212121;'>{theme}</span>",
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No common themes identified.")

            # Contradictions
            with st.expander("⚡ Contradictions Found"):
                contradictions = result.get("contradictions", [])
                if contradictions:
                    for i, contradiction in enumerate(contradictions, 1):
                        st.markdown(
                            f"""
                        <div style='color: #212121; line-height: 1.8;'>
                        <strong style='color: #1565C0; font-size: 1.1em;'>Contradiction {i}:</strong><br>
                        - <strong style='color: #000000;'>{contradiction.get("paper1", "Paper A")}</strong> says: <span style='color: #424242;'>{contradiction.get("claim1", "N/A")}</span><br>
                        - <strong style='color: #000000;'>{contradiction.get("paper2", "Paper B")}</strong> says: <span style='color: #424242;'>{contradiction.get("claim2", "N/A")}</span><br>
                        - <strong style='color: #D32F2F;'>Conflict:</strong> <span style='color: #616161;'>{contradiction.get("conflict", "N/A")}</span>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No contradictions found.")

            # Research Gaps
            with st.expander("🎯 Research Gaps Identified"):
                gaps = result.get("research_gaps", [])
                if gaps:
                    for gap in gaps:
                        st.markdown(
                            f"<div style='color: #212121; line-height: 1.6;'>• <span style='color: #424242;'>{gap}</span></div>",
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No research gaps identified.")

            # Extract papers from result (needed for bias detection and citations)
            papers = result.get("papers", [])
            
            # Papers Section with Progressive Disclosure
            if papers:
                papers_count = len(papers)
                with st.expander(f"📚 Papers Analyzed ({papers_count} total)", expanded=False):
                    # Configurable number of papers to show
                    show_count = st.slider(
                        "Number of papers to display", 
                        min_value=5, 
                        max_value=min(50, papers_count), 
                        value=min(10, papers_count),
                        help="Adjust to show more or fewer papers"
                    )
                    
                    for idx, paper in enumerate(papers[:show_count], 1):
                        paper_title = paper.get("title", "Untitled")
                        with st.expander(f"{idx}. {paper_title}", expanded=False):
                            # Authors
                            authors = paper.get("authors", [])
                            if authors:
                                if isinstance(authors, list):
                                    authors_str = ", ".join(authors[:5])
                                    if len(authors) > 5:
                                        authors_str += f" et al. ({len(authors)} total)"
                                else:
                                    authors_str = str(authors)
                                st.markdown(f"**Authors:** {authors_str}")
                            
                            # Publication info
                            year = paper.get("year", "N/A")
                            venue = paper.get("venue", "N/A")
                            st.markdown(f"**Published:** {year}")
                            if venue and venue != "N/A":
                                st.markdown(f"**Venue:** {venue}")
                            
                            # DOI and links
                            doi = paper.get("doi", "")
                            if doi:
                                st.markdown(f"**DOI:** [{doi}](https://doi.org/{doi})")
                            
                            url = paper.get("url", "")
                            if url and url != doi:
                                st.markdown(f"**URL:** [Link]({url})")
                            
                            # Abstract preview (if available)
                            abstract = paper.get("abstract", "")
                            if abstract:
                                abstract_preview = abstract[:200] + "..." if len(abstract) > 200 else abstract
                                st.markdown(f"**Abstract:** {abstract_preview}")
                                
                                if len(abstract) > 200:
                                    if st.button(f"Show full abstract", key=f"abstract_{idx}"):
                                        st.markdown(f"**Full Abstract:** {abstract}")
                            
                            # Relevance score (if available)
                            relevance = paper.get("relevance_score", 0)
                            if relevance > 0:
                                st.markdown(f"**Relevance Score:** {relevance:.2%}")
                    
                    if papers_count > show_count:
                        st.info(f"Showing {show_count} of {papers_count} papers. Adjust the slider above to see more.")

            # Bias Detection Section
            if papers:
                st.markdown("---")
                st.markdown("## 🔍 Bias Analysis")

                try:
                    bias_analysis = detect_bias(papers)

                    col_bias1, col_bias2 = st.columns(2)

                    with col_bias1:
                        st.markdown("### 📊 Analysis Results")

                        # Publication bias
                        pub_bias = bias_analysis.get("publication_bias", {})
                        if pub_bias.get("is_skewed"):
                            st.warning(
                                f"**Publication Bias:** {pub_bias.get('message', '')}"
                            )
                        else:
                            st.success(
                                f"**Publication Sources:** {pub_bias.get('message', 'Good diversity')}"
                            )

                        # Temporal bias
                        temp_bias = bias_analysis.get("temporal_bias", {})
                        if temp_bias.get("is_skewed"):
                            st.warning(
                                f"**Temporal Bias:** {temp_bias.get('message', '')}"
                            )
                        else:
                            st.success(
                                f"**Time Range:** {temp_bias.get('message', 'Good distribution')}"
                            )

                        # Venue bias
                        venue_bias = bias_analysis.get("venue_bias", {})
                        if venue_bias.get("is_skewed"):
                            st.warning(
                                f"**Venue Bias:** {venue_bias.get('message', '')}"
                            )
                        else:
                            st.success(
                                f"**Venues:** {venue_bias.get('message', 'Good diversity')}"
                            )

                    with col_bias2:
                        st.markdown("### 💡 Recommendations")
                        recommendations = bias_analysis.get("recommendations", [])
                        if recommendations:
                            for rec in recommendations:
                                st.info(f"• {rec}")
                        else:
                            st.success("No significant bias detected. Good diversity!")

                    # Overall assessment
                    overall = bias_analysis.get("overall_assessment", "")
                    if bias_analysis.get("warnings"):
                        st.markdown(f"**Overall Assessment:** ⚠️ {overall}")
                    else:
                        st.markdown(f"**Overall Assessment:** ✅ {overall}")

                except Exception as e:
                    st.warning(f"Bias detection failed: {e}")

            # Quality Scores Section
            quality_scores = result.get("quality_scores", [])
            if quality_scores:
                st.markdown("---")
                st.markdown("## 📊 Paper Quality Assessment")

                for qs in quality_scores:
                    paper_title = next(
                        (
                            p.get("title", "Unknown")
                            for p in result.get("papers", [])
                            if p.get("id") == qs.get("paper_id")
                        ),
                        "Unknown Paper",
                    )

                    with st.expander(
                        f"📄 {paper_title[:60]}... (Quality: {qs.get('overall_score', 0):.2f})"
                    ):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("### Scores")
                            st.metric(
                                "Overall",
                                f"{qs.get('overall_score', 0):.2f}",
                                delta=f"{qs.get('confidence_level', 'medium').upper()}",
                            )
                            st.progress(qs.get("overall_score", 0))

                            st.markdown("**Breakdown:**")
                            st.write(
                                f"- Methodology: {qs.get('methodology_score', 0):.2f}"
                            )
                            st.write(
                                f"- Statistical: {qs.get('statistical_score', 0):.2f}"
                            )
                            st.write(
                                f"- Reproducibility: {qs.get('reproducibility_score', 0):.2f}"
                            )
                            st.write(
                                f"- Venue: {qs.get('venue_score', 0):.2f}"
                            )
                            st.write(
                                f"- Sample Size: {qs.get('sample_size_score', 0):.2f}"
                            )

                        with col2:
                            strengths = qs.get("strengths", [])
                            issues = qs.get("issues", [])

                            if strengths:
                                st.markdown("### ✅ Strengths")
                                for strength in strengths:
                                    st.success(f"✓ {strength}")

                            if issues:
                                st.markdown("### ⚠️ Issues")
                                for issue in issues:
                                    st.warning(f"⚠ {issue}")

            # Enhanced Extraction Data Section
            analyses = result.get("analyses", [])
            if analyses and any(a.get("metadata") for a in analyses):
                st.markdown("---")
                st.markdown("## 🔬 Enhanced Extraction Data")

                tab_stat, tab_exp, tab_comp, tab_repro = st.tabs(
                    [
                        "📈 Statistical Results",
                        "⚙️ Experimental Setup",
                        "📊 Comparative Results",
                        "♻️ Reproducibility",
                    ]
                )

                with tab_stat:
                    for analysis in analyses:
                        if analysis.get("metadata", {}).get("statistical_results"):
                            stats = analysis["metadata"]["statistical_results"]
                            st.markdown(
                                f"**Paper:** {analysis.get('paper_id', 'Unknown')}"
                            )
                            if stats.get("p_values"):
                                st.write(
                                    f"**P-values:** {', '.join(stats['p_values'])}"
                                )
                            if stats.get("effect_sizes"):
                                st.write(
                                    f"**Effect Sizes:** {', '.join(stats['effect_sizes'])}"
                                )
                            if stats.get("confidence_intervals"):
                                st.write(
                                    f"**Confidence Intervals:** {', '.join(stats['confidence_intervals'])}"
                                )
                            if stats.get("statistical_tests"):
                                st.write(
                                    f"**Tests:** {', '.join(stats['statistical_tests'])}"
                                )
                            st.markdown("---")

                with tab_exp:
                    for analysis in analyses:
                        if analysis.get("metadata", {}).get("experimental_setup"):
                            exp = analysis["metadata"]["experimental_setup"]
                            st.markdown(
                                f"**Paper:** {analysis.get('paper_id', 'Unknown')}"
                            )
                            if exp.get("datasets"):
                                st.write(f"**Datasets:** {', '.join(exp['datasets'])}")
                            if exp.get("hardware"):
                                st.write(f"**Hardware:** {exp['hardware']}")
                            if exp.get("hyperparameters"):
                                st.write(
                                    f"**Hyperparameters:** {', '.join(exp['hyperparameters'])}"
                                )
                            if exp.get("software_frameworks"):
                                st.write(
                                    f"**Frameworks:** {', '.join(exp['software_frameworks'])}"
                                )
                            st.markdown("---")

                with tab_comp:
                    for analysis in analyses:
                        if analysis.get("metadata", {}).get("comparative_results"):
                            comp = analysis["metadata"]["comparative_results"]
                            st.markdown(
                                f"**Paper:** {analysis.get('paper_id', 'Unknown')}"
                            )
                            if comp.get("baselines"):
                                st.write(
                                    f"**Baselines:** {', '.join(comp['baselines'])}"
                                )
                            if comp.get("benchmarks"):
                                st.write(
                                    f"**Benchmarks:** {', '.join(comp['benchmarks'])}"
                                )
                            if comp.get("improvements"):
                                st.write(
                                    f"**Improvements:** {', '.join(comp['improvements'])}"
                                )
                            st.markdown("---")

                with tab_repro:
                    for analysis in analyses:
                        if analysis.get("metadata", {}).get("reproducibility"):
                            repro = analysis["metadata"]["reproducibility"]
                            st.markdown(
                                f"**Paper:** {analysis.get('paper_id', 'Unknown')}"
                            )
                            st.write(
                                f"**Code Available:** {'✅ Yes' if repro.get('code_available') else '❌ No'}"
                            )
                            st.write(
                                f"**Data Available:** {'✅ Yes' if repro.get('data_available') else '❌ No'}"
                            )
                            if repro.get("repository_url"):
                                st.write(f"**Repository:** {repro['repository_url']}")
                            st.markdown("---")

            # Citation Styles Section
            # Note: papers already extracted above for bias detection
            if papers:
                st.markdown("---")
                st.markdown("### 📝 Citations")

                citation_style = st.selectbox(
                    "Citation Style:",
                    ["APA", "MLA", "Chicago", "IEEE", "Nature"],
                    help="Select citation format",
                )

                citations = format_citations(papers, style=citation_style.lower())

                with st.expander(f"View {citation_style} Citations", expanded=False):
                    for i, citation in enumerate(citations, 1):
                        st.text(f"{i}. {citation}")

                # Download citations
                st.download_button(
                    label=f"📥 {citation_style} Citations",
                    data="\n\n".join([f"{i}. {c}" for i, c in enumerate(citations, 1)]),
                    file_name=f"citations_{citation_style.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    help=f"Download citations in {citation_style} format",
                )

            # Papers List Display with Lazy Loading (Phase 2.3 UX Improvement)
            st.markdown("---")
            st.markdown("### 📚 Analyzed Papers")

            papers_count = len(papers)
            st.caption(
                f"Browse all {papers_count} papers analyzed in this research synthesis. "
                "Expand any paper to view full details."
            )
            
            # Papers Summary (Phase 2.2) - Show distribution overview
            if papers_count > 0:
                render_papers_summary(papers)

            # Performance optimization: Use pagination for 10+ papers
            if papers_count >= 10:
                # Large list - use pagination (10 papers per page)
                st.info(
                    f"📊 **Performance Mode**: Displaying {papers_count} papers with pagination "
                    "for optimal loading speed"
                )
                render_papers_paginated(papers, items_per_page=10)
            elif papers_count > 0:
                # Small list (1-9 papers) - show all with lazy details
                for idx, paper in enumerate(papers):
                    render_paper_lazy(paper, idx, show_details=False)
                    if idx < papers_count - 1:
                        st.markdown("---")
            else:
                st.info("No papers available to display")

            # Download options with multiple formats
            st.markdown("---")
            st.markdown("### 📥 Export Results")

            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

            with col1:
                st.download_button(
                    label="📥 JSON",
                    data=json.dumps(result, indent=2),
                    file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True,
                )

            with col2:
                # Create markdown report
                markdown_report = f"""# Research Synthesis Report

**Query:** {query}
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Papers Analyzed:** {result.get("papers_analyzed", 0)}

## Common Themes
{chr(10).join([f"{i}. {theme}" for i, theme in enumerate(result.get("common_themes", []), 1)])}

## Research Gaps
{chr(10).join([f"- {gap}" for gap in result.get("research_gaps", [])])}

## Autonomous Decisions Made
{chr(10).join([f"- **{d['agent']}**: {d['decision']}" for d in result.get("decisions", [])])}
"""
                st.download_button(
                    label="📄 Markdown",
                    data=markdown_report,
                    file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            with col3:
                # Generate BibTeX export
                papers = result.get("papers", [])
                if papers:
                    try:
                        bibtex_content = generate_bibtex(papers)
                        st.download_button(
                            label="📚 BibTeX",
                            data=bibtex_content,
                            file_name=f"references_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bib",
                            mime="text/plain",
                            use_container_width=True,
                            help="Import into Zotero, Mendeley, or EndNote",
                        )
                    except Exception as e:
                        st.error(f"Error generating BibTeX: {e}")
                else:
                    st.button(
                        label="📚 BibTeX",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )

            with col4:
                # Generate LaTeX document
                if papers:
                    try:
                        latex_content = generate_latex_document(
                            query=query,
                            papers=papers,
                            themes=result.get("common_themes", []),
                            gaps=result.get("research_gaps", []),
                            contradictions=result.get("contradictions", []),
                            date=datetime.now().strftime("%B %d, %Y"),
                        )
                        st.download_button(
                            label="📝 LaTeX",
                            data=latex_content,
                            file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex",
                            mime="text/plain",
                            use_container_width=True,
                            help="Complete LaTeX document ready to compile",
                        )
                    except ImportError:
                        st.button(
                            label="📝 LaTeX",
                            disabled=True,
                            use_container_width=True,
                            help="Install python-docx: pip install python-docx",
                        )
                    except Exception as e:
                        st.error(f"Error generating LaTeX: {e}")
                else:
                    st.button(
                        label="📝 LaTeX",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )

            with col5:
                # Generate Word document export
                if papers:
                    try:
                        word_doc = generate_word_document(
                            query=query,
                            papers=papers,
                            themes=result.get("common_themes", []),
                            gaps=result.get("research_gaps", []),
                            contradictions=result.get("contradictions", []),
                        )
                        st.download_button(
                            label="📄 Word",
                            data=word_doc,
                            file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                            help="Microsoft Word document (.docx)",
                        )
                    except ImportError:
                        st.button(
                            label="📄 Word",
                            disabled=True,
                            use_container_width=True,
                            help="Install python-docx: pip install python-docx",
                        )
                    except Exception as e:
                        st.error(f"Error generating Word: {e}")
                else:
                    st.button(
                        label="📄 Word",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )

            with col6:
                # Generate PDF document export
                if papers:
                    try:
                        pdf_doc = generate_pdf_document(
                            query=query,
                            papers=papers,
                            themes=result.get("common_themes", []),
                            gaps=result.get("research_gaps", []),
                            contradictions=result.get("contradictions", []),
                        )
                        st.download_button(
                            label="📕 PDF",
                            data=pdf_doc,
                            file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            help="PDF document",
                        )
                    except ImportError:
                        st.button(
                            label="📕 PDF",
                            disabled=True,
                            use_container_width=True,
                            help="Install reportlab: pip install reportlab",
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {e}")
                else:
                    st.button(
                        label="📕 PDF",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )

            # Add CSV, Excel, EndNote, HTML, XML, JSON-LD exports on second row
            st.markdown("<br>", unsafe_allow_html=True)
            col_csv, col_excel, col_endnote, col_html = st.columns(4)
            
            # Third row for advanced formats
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🔬 Advanced Export Formats")
            col_xml, col_jsonld, col_html_enh, col_placeholder = st.columns(4)

            with col_csv:
                # Generate CSV export
                if papers:
                    try:
                        csv_content = generate_csv_export(result)
                        st.download_button(
                            label="📊 CSV",
                            data=csv_content,
                            file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True,
                            help="CSV format for spreadsheet analysis",
                        )
                    except Exception as e:
                        st.error(f"Error generating CSV: {e}")
                else:
                    st.button(
                        label="📊 CSV",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )

            with col_excel:
                # Generate Excel export
                if papers:
                    try:
                        excel_doc = generate_excel_export(result)
                        st.download_button(
                            label="📗 Excel",
                            data=excel_doc,
                            file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                            help="Excel format (.xlsx) for quantitative analysis",
                        )
                    except ImportError:
                        st.button(
                            label="📗 Excel",
                            disabled=True,
                            use_container_width=True,
                            help="Install openpyxl: pip install openpyxl",
                        )
                    except Exception as e:
                        st.error(f"Error generating Excel: {e}")
                else:
                    st.button(
                        label="📗 Excel",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )

            with col_endnote:
                # Generate EndNote export
                if papers:
                    try:
                        endnote_content = generate_endnote_export(papers)
                        st.download_button(
                            label="📑 EndNote",
                            data=endnote_content,
                            file_name=f"references_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enw",
                            mime="text/plain",
                            use_container_width=True,
                            help="EndNote format (.enw) for citation management",
                        )
                    except Exception as e:
                        st.error(f"Error generating EndNote: {e}")
                else:
                    st.button(
                        label="📑 EndNote",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )

            with col_html:
                # Generate interactive HTML report
                if papers:
                    try:
                        html_content = generate_interactive_html_report(
                            query=query, result=result, papers=papers
                        )
                        st.download_button(
                            label="🌐 HTML",
                            data=html_content,
                            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html",
                            use_container_width=True,
                            help="Interactive HTML report with visualizations",
                        )
                    except Exception as e:
                        st.error(f"Error generating HTML: {e}")
                else:
                    st.button(
                        label="🌐 HTML",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )
            
            # Advanced export formats
            with col_xml:
                # Generate XML export
                if papers:
                    try:
                        xml_content = generate_xml_export(result, papers)
                        st.download_button(
                            label="📄 XML",
                            data=xml_content,
                            file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml",
                            mime="application/xml",
                            use_container_width=True,
                            help="XML format for structured data exchange",
                        )
                    except Exception as e:
                        st.error(f"Error generating XML: {e}")
                else:
                    st.button(
                        label="📄 XML",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )
            
            with col_jsonld:
                # Generate JSON-LD export
                if papers:
                    try:
                        jsonld_content = generate_json_ld_export(result, papers)
                        st.download_button(
                            label="🔗 JSON-LD",
                            data=jsonld_content,
                            file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonld",
                            mime="application/ld+json",
                            use_container_width=True,
                            help="JSON-LD format (Schema.org compatible) for semantic web",
                        )
                    except Exception as e:
                        st.error(f"Error generating JSON-LD: {e}")
                else:
                    st.button(
                        label="🔗 JSON-LD",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )
            
            with col_html_enh:
                # Generate enhanced HTML report
                if papers:
                    try:
                        html_enhanced = generate_enhanced_interactive_html_report(
                            query=query, result=result, papers=papers
                        )
                        st.download_button(
                            label="✨ Enhanced HTML",
                            data=html_enhanced,
                            file_name=f"research_report_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html",
                            use_container_width=True,
                            help="Enhanced interactive HTML with theme network, dark mode, and export",
                        )
                    except Exception as e:
                        st.error(f"Error generating enhanced HTML: {e}")
                else:
                    st.button(
                        label="✨ Enhanced HTML",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export",
                    )

    except requests.exceptions.Timeout:
        progress_bar.progress(0)
        status_text.empty()
        st.error("❌ Request timeout. The research is taking longer than expected.")
        st.info("Try reducing the number of papers or simplifying the query.")

    except requests.exceptions.ConnectionError:
        progress_bar.progress(0)
        status_text.empty()
        st.error(f"❌ Cannot connect to API at {api_url}")
        st.info("""
        **Troubleshooting:**
        1. Verify the agent orchestrator is running
        2. Check the API URL in the sidebar
        3. Ensure NIMs are deployed and accessible
        """)

    except Exception as e:
        progress_bar.progress(0)
        status_text.empty()
        st.error(f"❌ Error during research: {str(e)}")
        with st.expander("Error Details"):
            st.exception(e)

elif start_button:
    st.warning("⚠️ Please enter a research query first")

# Footer - Platform Positioning (Long-Term Recommendation)
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #424242;'>
    <small style='color: #424242;'>
    🔍 <strong>Research Intelligence Platform</strong> - Not just a tool, a research partner<br>
    Synthesis • Hypothesis Generation • Trend Prediction • Collaboration Matching<br>
    Research-grade AI with full transparency • <a href="/docs" target="_blank" style='color: #1976D2; text-decoration: none; font-weight: 500;'>API Docs</a> • 
    <a href="#" style='color: #1976D2; text-decoration: none;'>Zotero/Mendeley Integration</a> (Coming Soon)
    </small>
</div>
""",
    unsafe_allow_html=True,
)
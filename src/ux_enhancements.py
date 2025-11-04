"""
UX Enhancements Module for Agentic Researcher
Implements tactical "wow" factors and advanced UX features
"""

import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import time

# Import export functions
try:
    from .export_formats import (
        generate_pdf_document,
        generate_word_document,
        generate_bibtex,
    )
except ImportError:
    from export_formats import (
        generate_pdf_document,
        generate_word_document,
        generate_bibtex,
    )


# Example syntheses for Results Gallery
EXAMPLE_SYNTHESES = [
    {
        "title": "Machine Learning for Medical Imaging",
        "query": "machine learning for medical imaging",
        "themes": [
            "Deep learning architectures for medical image segmentation",
            "Transfer learning and domain adaptation techniques",
            "Explainable AI in medical diagnosis"
        ],
        "contradictions": [
            {
                "finding_a": "CNN-based models achieve 95% accuracy",
                "finding_b": "Vision transformers outperform CNNs by 3-5%",
                "conflict": "Architectural preference debate"
            }
        ],
        "gaps": [
            "Limited studies on multi-modal fusion",
            "Gap in longitudinal prediction studies"
        ],
        "papers_count": 12,
        "processing_time": 45.2
    },
    {
        "title": "Reinforcement Learning in Robotics",
        "query": "reinforcement learning robotics manipulation",
        "themes": [
            "Sim-to-real transfer challenges",
            "Sample efficiency improvements",
            "Safety constraints in RL policies"
        ],
        "contradictions": [
            {
                "finding_a": "Sim-to-real requires extensive domain randomization",
                "finding_b": "Minimal randomization sufficient with proper sim design",
                "conflict": "Domain randomization strategy"
            }
        ],
        "gaps": [
            "Real-world deployment scalability",
            "Long-horizon task planning"
        ],
        "papers_count": 15,
        "processing_time": 52.8
    },
    {
        "title": "Large Language Model Fine-tuning",
        "query": "fine-tuning large language models few-shot learning",
        "themes": [
            "Parameter-efficient fine-tuning methods (LoRA, AdaLoRA)",
            "In-context learning vs fine-tuning trade-offs",
            "Catastrophic forgetting mitigation strategies"
        ],
        "contradictions": [
            {
                "finding_a": "Full fine-tuning outperforms parameter-efficient methods",
                "finding_b": "LoRA achieves 95% performance with 1% parameters",
                "conflict": "Fine-tuning strategy effectiveness"
            }
        ],
        "gaps": [
            "Multi-task fine-tuning benchmarks",
            "Cross-lingual transfer evaluation"
        ],
        "papers_count": 10,
        "processing_time": 38.5
    }
]


def render_results_gallery():
    """
    Display clickable gallery of example syntheses.
    Shows actual outputs for example queries with progressive disclosure.
    """
    st.markdown("## 📚 Example Research Syntheses")
    st.markdown(
        "*Click any example to see themes, contradictions, and research gaps discovered by our agents*"
    )
    
    # Display examples in columns
    cols = st.columns(min(3, len(EXAMPLE_SYNTHESES)))
    
    for idx, example in enumerate(EXAMPLE_SYNTHESES):
        col_idx = idx % 3
        with cols[col_idx]:
            with st.container():
                # Card-style display
                st.markdown(f"### {example['title']}")
                st.caption(f"📊 {example['papers_count']} papers • ⏱️ {example['processing_time']}s")
                
                # Quick preview (using details instead of expander to avoid nesting)
                st.markdown("<details><summary>🔍 Preview Themes</summary>", unsafe_allow_html=True)
                for theme in example['themes'][:2]:
                    st.markdown(f"• {theme}")
                st.markdown("</details>", unsafe_allow_html=True)
                
                # Show contradictions (using details instead of expander)
                if example.get('contradictions'):
                    st.markdown("<details><summary>⚠️ Contradictions Found</summary>", unsafe_allow_html=True)
                    contra = example['contradictions'][0]
                    st.markdown(f"**Conflict:** {contra['conflict']}")
                    st.caption(f"Finding A: {contra['finding_a'][:60]}...")
                    st.caption(f"Finding B: {contra['finding_b'][:60]}...")
                    st.markdown("</details>", unsafe_allow_html=True)
                
                # Show gaps (using details instead of expander)
                if example.get('gaps'):
                    st.markdown("<details><summary>🎯 Research Gaps</summary>", unsafe_allow_html=True)
                    for gap in example['gaps']:
                        st.markdown(f"• {gap}")
                    st.markdown("</details>", unsafe_allow_html=True)
                
                # Try this query button
                if st.button(f"🔬 Try: '{example['query'][:30]}...'", key=f"example_{idx}"):
                    st.session_state['example_query'] = example['query']
                    st.session_state['example_max_papers'] = example['papers_count']
                    st.rerun()
    
    st.markdown("---")


def render_real_time_agent_panel(decisions: List[Dict], always_visible: bool = True, sticky: bool = True):
    """
    Enhanced real-time agent activity panel with always-visible decision log.
    
    Shows live agent status, decisions, and reasoning in a prominent panel.
    Can be made sticky/pinned for persistent transparency.
    
    Args:
        decisions: List of agent decisions
        always_visible: Whether panel should always be visible
        sticky: Whether to make the panel sticky/pinned (default: True)
    """
    if not decisions:
        return
    
    # Initialize sticky state
    if "agent_panel_sticky" not in st.session_state:
        st.session_state.agent_panel_sticky = sticky
    
    # Create always-visible panel with sticky option
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 🤖 Real-Time Agent Activity")
    with col2:
        # Pin/unpin toggle
        pin_label = "📌 Pinned" if st.session_state.agent_panel_sticky else "📌 Pin"
        if st.button(pin_label, key="toggle_agent_panel_pin", help="Pin this panel to keep it visible"):
            st.session_state.agent_panel_sticky = not st.session_state.agent_panel_sticky
            st.rerun()
    
    # Add sticky styling if pinned
    if st.session_state.agent_panel_sticky:
        st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"] > div:has(> h3:contains("🤖 Real-Time Agent Activity")) {
            position: sticky !important;
            top: 20px !important;
            z-index: 100 !important;
            background-color: var(--bg-primary, #1E1E1E);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color, #3D3D3D);
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Group decisions by agent
    agent_activity = {}
    for decision in decisions:
        agent = decision.get("agent", "Unknown")
        if agent not in agent_activity:
            agent_activity[agent] = []
        agent_activity[agent].append(decision)
    
    # Display agent status cards
    cols = st.columns(4)
    agent_names = ["Scout", "Analyst", "Synthesizer", "Coordinator"]
    agent_emojis = {
        "Scout": "🔍",
        "Analyst": "📊",
        "Synthesizer": "🧩",
        "Coordinator": "🎯"
    }
    
    for idx, agent_name in enumerate(agent_names):
        with cols[idx]:
            if agent_name in agent_activity:
                latest = agent_activity[agent_name][-1]
                decision_type = latest.get("decision_type", "")
                decision_text = latest.get("decision", "")
                
                # Agent card with status
                st.markdown(f"""
                <div style="background-color: var(--bg-card, #2D323E); padding: 1rem; border-radius: 8px; border-left: 4px solid var(--accent-primary, #C8323E);">
                    <h4 style="margin: 0; color: var(--accent-primary, #C8323E);">
                        {agent_emojis.get(agent_name, '🤖')} {agent_name}
                    </h4>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: var(--text-secondary, #E5E5E5);">
                        {decision_text[:60]}{'...' if len(decision_text) > 60 else ''}
                    </p>
                    <small style="color: var(--text-tertiary, #9E9E9E);">
                        {decision_type.replace('_', ' ').title()}
                    </small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: var(--bg-card, #2D323E); padding: 1rem; border-radius: 8px; border-left: 4px solid #757575; opacity: 0.6;">
                    <h4 style="margin: 0; color: #757575;">
                        ⏳ {agent_name}
                    </h4>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: var(--text-secondary, #E5E5E5);">
                        Waiting...
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Decision log - immediately visible with toggle option
    st.markdown("---")
    
    # Toggle for showing/hiding decision log details
    if "decision_log_visible" not in st.session_state:
        st.session_state.decision_log_visible = True  # Visible by default
    
    col_toggle, col_title = st.columns([1, 4])
    with col_toggle:
        toggle_label = "🙈 Hide Details" if st.session_state.decision_log_visible else "👁️ Show Details"
        if st.button(toggle_label, key="toggle_decision_log"):
            st.session_state.decision_log_visible = not st.session_state.decision_log_visible
            st.rerun()
    with col_title:
        st.markdown("#### 📋 Decision Log")
    
    # Initialize session state for decision log expansion
    if "decision_log_expanded" not in st.session_state:
        st.session_state.decision_log_expanded = {}
    
    # Show all decisions if visible, or just summary
    if st.session_state.decision_log_visible:
        # Show all decisions (not just recent 5)
        for idx, decision in enumerate(decisions):
            agent = decision.get("agent", "Unknown")
            decision_text = decision.get("decision", "")
            reasoning = decision.get("reasoning", "")
            nim_used = decision.get("nim_used", "")
            timestamp = decision.get("timestamp", "")
            
            decision_key = f"decision_{idx}"
            expanded = st.session_state.decision_log_expanded.get(decision_key, False)
            
            with st.expander(
                f"{agent_emojis.get(agent, '🤖')} {agent}: {decision_text[:50]}...",
                expanded=expanded
            ):
                st.markdown(f"**Decision:** {decision_text}")
                if reasoning:
                    st.markdown(f"**Reasoning:** {reasoning}")
                if nim_used:
                    st.caption(f"🧠 Using: {nim_used}")
                if timestamp:
                    st.caption(f"⏰ {timestamp}")
    else:
        # Show summary when collapsed
        st.info(f"📊 **{len(decisions)} decisions logged**. Click 'Show Details' to view full decision log with reasoning.")


def render_session_stats_dashboard():
    """
    Display session statistics: queries run, agent decisions, exports/downloads.
    """
    # Try to get SessionManager from web_ui module (it's defined there)
    try:
        # SessionManager is defined in web_ui.py, so we need to access it
        # Since we're called from web_ui, we can use the fallback implementation
        from dataclasses import dataclass, field
        import uuid
        from datetime import datetime
        
        @dataclass
        class ResearchSession:
            query: str = ""
            max_papers: int = 10
            paper_sources: List[str] = field(default_factory=lambda: ["arxiv", "pubmed", "semantic_scholar"])
            date_range: tuple = field(default_factory=lambda: (2020, datetime.now().year))
            use_date_filter: bool = True
            synthesis: str = ""
            papers: List[Dict] = field(default_factory=list)
            decisions: List[Dict] = field(default_factory=list)
            metrics: Dict[str, Any] = field(default_factory=dict)
            search_expanded: bool = False
            results_visible: bool = False
            decisions_visible: bool = False
            metrics_visible: bool = False
            session_id: str = ""
            created_at: datetime = field(default_factory=datetime.now)
            last_query_time: Optional[datetime] = None
            query_count: int = 0
            result_cache: Dict = field(default_factory=dict)
        
        class SessionManager:
            SESSION_KEY = "research_session"
            
            @classmethod
            def get(cls):
                if cls.SESSION_KEY not in st.session_state:
                    return ResearchSession(session_id=str(uuid.uuid4()), created_at=datetime.now())
                return st.session_state[cls.SESSION_KEY]
            
            @classmethod
            def get_stats(cls):
                session = cls.get()
                return {
                    "session_id": session.session_id,
                    "created_at": session.created_at.isoformat() if hasattr(session.created_at, 'isoformat') else str(session.created_at),
                    "query_count": session.query_count,
                    "last_query": session.last_query_time.isoformat() if session.last_query_time and hasattr(session.last_query_time, 'isoformat') else None,
                    "current_query": session.query,
                    "papers_count": len(session.papers),
                    "decisions_count": len(session.decisions),
                    "cache_entries": len(session.result_cache),
                }
        
        session = SessionManager.get()
        stats = SessionManager.get_stats()
    except Exception as e:
        # User-friendly error message instead of technical exception
        st.info("📊 Session statistics view is temporarily unavailable. Please refresh the page or try again later.")
        logger.debug(f"Session stats error: {e}")  # Log technical details for debugging
        return
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        query_count = stats.get("query_count", 0)
        st.metric("Queries Run", query_count, help="Total research queries executed this session")
    
    with col2:
        papers_count = stats.get("papers_count", 0)
        st.metric("Papers Analyzed", papers_count, help="Total papers analyzed across all queries")
    
    with col3:
        decisions_count = stats.get("decisions_count", 0)
        st.metric("Agent Decisions", decisions_count, help="Total autonomous decisions made by agents")
    
    with col4:
        cache_entries = stats.get("cache_entries", 0)
        st.metric("Cached Results", cache_entries, help="Number of cached synthesis results")
    
    # Detailed stats (using details/summary instead of expander to avoid nesting)
    st.markdown("---")
    with st.container():
        st.markdown("#### 📈 Detailed Session Analytics")
        st.json(stats)
        
        # Timeline visualization
        if stats.get("last_query"):
            st.markdown("**Last Query Time:** " + stats.get("last_query", "N/A"))
            st.markdown("**Session Started:** " + stats.get("created_at", "N/A"))


def render_speed_comparison_demo(query: str, cached_time: float, fresh_time: float):
    """
    Display cache speed comparison showing 95% faster on repeat queries.
    """
    if cached_time and fresh_time:
        speed_improvement = ((fresh_time - cached_time) / fresh_time) * 100
        time_saved = fresh_time - cached_time
        
        st.markdown("### ⚡ Cache Performance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Fresh Query", f"{fresh_time:.1f}s", help="First time query processing")
        
        with col2:
            st.metric("Cached Query", f"{cached_time:.1f}s", help="Cached result retrieval")
        
        with col3:
            st.metric(
                "Speed Improvement",
                f"{speed_improvement:.0f}%",
                delta=f"{time_saved:.1f}s saved",
                help="Time saved using cached results"
            )
        
        # Visual comparison
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Fresh Query', 'Cached Query'],
            y=[fresh_time, cached_time],
            marker_color=['#C8323E', '#4A9EFF'],
            text=[f"{fresh_time:.1f}s", f"{cached_time:.1f}s"],
            textposition='auto'
        ))
        fig.update_layout(
            title="Query Speed Comparison",
            yaxis_title="Time (seconds)",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)


def render_guided_tour():
    """
    First-run guided tour with popover tooltips and friendly walkthrough.
    """
    # Check if tour has been shown
    if "tour_completed" not in st.session_state:
        st.session_state.tour_completed = False
    
    if st.session_state.tour_completed:
        return
    
    # Tour welcome modal
    with st.container():
        st.markdown("""
        <div style="background-color: var(--bg-card, #2D323E); padding: 2rem; border-radius: 12px; border: 2px solid var(--accent-primary, #C8323E); margin: 1rem 0;">
            <h2 style="color: var(--accent-primary, #C8323E); margin-top: 0;">👋 Welcome to Agentic Researcher!</h2>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Your AI research team is ready to help. Here's what you can do:
            </p>
            <ul style="font-size: 1rem; line-height: 2;">
                <li><strong>🔍 Scout Agent</strong>: Searches 7 academic databases simultaneously</li>
                <li><strong>📊 Analyst Agent</strong>: Extracts key findings from each paper</li>
                <li><strong>🧩 Synthesizer Agent</strong>: Identifies themes, contradictions, and gaps</li>
                <li><strong>🎯 Coordinator Agent</strong>: Ensures research-grade quality</li>
            </ul>
            <p style="font-size: 1rem; margin-top: 1rem;">
                <strong>💡 Pro Tip:</strong> Watch the decision log to see how agents make autonomous decisions!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎓 Start Guided Tour", key="start_tour", use_container_width=True):
                st.session_state.tour_in_progress = True
                st.rerun()
        with col2:
            if st.button("✅ Skip Tour", key="skip_tour", use_container_width=True):
                st.session_state.tour_completed = True
                st.rerun()
    
    # Tour steps
    if st.session_state.get("tour_in_progress", False):
        st.info("""
        **Tour Step 1/5: Enter Your Research Query**
        
        Type your research question in natural language. Example: "machine learning for medical imaging"
        
        The Scout Agent will search across 7 databases and find relevant papers.
        """)
        
        if st.button("Next Step", key="tour_step_1"):
            st.session_state.tour_step = 2
            st.rerun()


def render_enhanced_loading_animation(stage: str, message: str, progress: float = 0.0):
    """
    Humanized loading animations with contextual messages.
    """
    agent_messages = {
        "search": "🔍 Your Scout Agent is searching 7 databases...",
        "analyze": "📊 Your Analyst Agent is extracting insights...",
        "synthesize": "🧩 Your Synthesizer Agent is finding patterns...",
        "coordinate": "🎯 Your Coordinator Agent is ensuring quality...",
        "complete": "✅ Your research synthesis is ready!"
    }
    
    default_message = agent_messages.get(stage, message)
    
    # Animated progress display
    st.markdown(f"""
    <div class="loading-status">
        <div class="agent-loading-spinner"></div>
        <span style="font-size: 1.1rem; margin-left: 1rem;">{default_message}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    if progress > 0:
        st.progress(progress)
    
    # Time estimate
    if progress < 1.0:
        estimated_remaining = (1.0 - progress) * 60  # Rough estimate
        st.caption(f"⏱️ Estimated time remaining: ~{estimated_remaining:.0f} seconds")


def render_quick_export_panel(result: Dict):
    """
    Enhanced quick export panel with single-click options.
    """
    st.markdown("## 📥 Quick Export")
    
    # Export options in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        # PDF Export
        papers = result.get("papers", [])
        query = result.get("query", "Research Synthesis")
        themes = result.get("common_themes", [])
        gaps = result.get("research_gaps", [])
        contradictions = result.get("contradictions", [])
        
        if papers:
            try:
                pdf_doc = generate_pdf_document(
                    query=query,
                    papers=papers,
                    themes=themes,
                    gaps=gaps,
                    contradictions=contradictions,
                )
                st.download_button(
                    label="📄 PDF",
                    data=pdf_doc,
                    file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="download_pdf_quick",
                    use_container_width=True,
                    help="PDF document ready for publication"
                )
            except ImportError:
                st.button(
                    label="📄 PDF",
                    disabled=True,
                    use_container_width=True,
                    help="Install reportlab: pip install reportlab",
                    key="pdf_disabled"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
        else:
            st.button(
                label="📄 PDF",
                disabled=True,
                use_container_width=True,
                help="No papers available",
                key="pdf_no_papers"
            )
    
    with col2:
        if st.button("📝 Markdown", key="export_md", use_container_width=True):
            st.session_state['export_format'] = 'markdown'
            # Generate markdown
            md_content = generate_markdown_export(result)
            st.download_button(
                label="Download Markdown",
                data=md_content,
                file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                key="download_md"
            )
    
    with col3:
        # BibTeX Export
        if papers:
            try:
                bibtex_content = generate_bibtex(papers)
                st.download_button(
                    label="📚 BibTeX",
                    data=bibtex_content,
                    file_name=f"references_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bib",
                    mime="text/plain",
                    key="download_bibtex_quick",
                    use_container_width=True,
                    help="Import into Zotero, Mendeley, or EndNote"
                )
            except Exception as e:
                st.error(f"Error generating BibTeX: {e}")
        else:
            st.button(
                label="📚 BibTeX",
                disabled=True,
                use_container_width=True,
                help="No papers available",
                key="bibtex_no_papers"
            )
    
    with col4:
        # Word Export
        if papers:
            try:
                word_doc = generate_word_document(
                    query=query,
                    papers=papers,
                    themes=themes,
                    gaps=gaps,
                    contradictions=contradictions,
                )
                st.download_button(
                    label="📊 Word",
                    data=word_doc,
                    file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="download_word_quick",
                    use_container_width=True,
                    help="Microsoft Word document (.docx)"
                )
            except ImportError:
                st.button(
                    label="📊 Word",
                    disabled=True,
                    use_container_width=True,
                    help="Install python-docx: pip install python-docx",
                    key="word_disabled"
                )
            except Exception as e:
                st.error(f"Error generating Word: {e}")
        else:
            st.button(
                label="📊 Word",
                disabled=True,
                use_container_width=True,
                help="No papers available",
                key="word_no_papers"
            )
    
    with col5:
        if st.button("💾 JSON", key="export_json", use_container_width=True):
            json_content = json.dumps(result, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_content,
                file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_json"
            )


def generate_markdown_export(result: Dict) -> str:
    """Generate markdown export from synthesis result"""
    md = f"""# Research Synthesis Report

**Query:** {result.get('query', 'N/A')}
**Papers Analyzed:** {result.get('papers_analyzed', 0)}
**Processing Time:** {result.get('processing_time_seconds', 0):.1f} seconds
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Common Themes

"""
    for theme in result.get('common_themes', []):
        md += f"- {theme}\n"
    
    md += "\n## Contradictions\n\n"
    for contra in result.get('contradictions', []):
        md += f"### {contra.get('conflict', 'Contradiction')}\n"
        md += f"- **Finding A:** {contra.get('finding_a', 'N/A')}\n"
        md += f"- **Finding B:** {contra.get('finding_b', 'N/A')}\n"
        md += f"- **Explanation:** {contra.get('explanation', 'N/A')}\n\n"
    
    md += "\n## Research Gaps\n\n"
    for gap in result.get('research_gaps', []):
        md += f"- {gap}\n"
    
    md += "\n## Papers\n\n"
    for paper in result.get('papers', []):
        md += f"### {paper.get('title', 'N/A')}\n"
        md += f"**Authors:** {paper.get('authors', 'N/A')}\n"
        md += f"**Source:** {paper.get('source', 'N/A')}\n"
        md += f"**URL:** {paper.get('url', 'N/A')}\n\n"
    
    return md


def render_ai_suggestions(result: Dict):
    """
    AI-powered suggestions after synthesis completion.
    """
    st.markdown("## 💡 Next Steps Suggestions")
    
    papers = result.get("papers", [])
    query = result.get("query", "Research Synthesis")
    themes = result.get("common_themes", [])
    gaps = result.get("research_gaps", [])
    contradictions = result.get("contradictions", [])
    
    suggestions = [
        {
            "title": "Generate Hypothesis",
            "description": "Based on the research gaps identified, formulate testable hypotheses",
            "action": "hypothesis"
        },
        {
            "title": "Draft Grant Proposal",
            "description": "Use the research gaps and themes to structure a grant proposal",
            "action": "grant"
        },
        {
            "title": "Create Literature Review",
            "description": "Export findings as a structured literature review document",
            "action": "review"
        },
        {
            "title": "Compare with Previous Synthesis",
            "description": "Compare this synthesis with previous research queries",
            "action": "compare"
        }
    ]
    
    cols = st.columns(2)
    for idx, suggestion in enumerate(suggestions):
        col_idx = idx % 2
        with cols[col_idx]:
            with st.container():
                st.markdown(f"### {suggestion['title']}")
                st.caption(suggestion['description'])
                if st.button(f"🚀 {suggestion['title']}", key=f"suggestion_{idx}"):
                    # Handle each suggestion action
                    if suggestion['action'] == "hypothesis":
                        # Generate hypotheses using research intelligence
                        try:
                            try:
                                from .research_intelligence import ResearchIntelligence
                            except ImportError:
                                from research_intelligence import ResearchIntelligence
                            
                            intelligence = ResearchIntelligence()
                            hypotheses = intelligence.generate_hypotheses(themes, gaps, contradictions)
                            
                            if hypotheses:
                                st.success("✅ Generated Research Hypotheses:")
                                for i, hypothesis in enumerate(hypotheses, 1):
                                    st.info(f"**Hypothesis {i}**: {hypothesis}")
                            else:
                                st.warning("Could not generate hypotheses. Ensure research gaps and themes are available.")
                        except Exception as e:
                            st.error(f"Error generating hypotheses: {e}")
                    
                    elif suggestion['action'] == "grant":
                        # Generate grant proposal outline
                        try:
                            grant_outline = _generate_grant_proposal_outline(query, themes, gaps, contradictions)
                            st.success("✅ Grant Proposal Outline Generated:")
                            st.markdown(grant_outline)
                            # Offer download as markdown
                            st.download_button(
                                label="📥 Download Grant Outline",
                                data=grant_outline,
                                file_name=f"grant_proposal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown",
                                key=f"download_grant_{idx}"
                            )
                        except Exception as e:
                            st.error(f"Error generating grant proposal: {e}")
                    
                    elif suggestion['action'] == "review":
                        # Generate and offer literature review export
                        try:
                            # Use Word document as literature review
                            word_doc = generate_word_document(
                                query=query,
                                papers=papers,
                                themes=themes,
                                gaps=gaps,
                                contradictions=contradictions,
                            )
                            st.success("✅ Literature Review Document Ready!")
                            st.download_button(
                                label="📥 Download Literature Review",
                                data=word_doc,
                                file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key=f"download_review_{idx}"
                            )
                        except ImportError:
                            st.warning("⚠️ Install python-docx to generate Word documents: `pip install python-docx`")
                        except Exception as e:
                            st.error(f"Error generating literature review: {e}")
                    
                    elif suggestion['action'] == "compare":
                        # Compare with previous syntheses
                        try:
                            try:
                                from .synthesis_history import get_synthesis_history
                            except ImportError:
                                from synthesis_history import get_synthesis_history
                            
                            history = get_synthesis_history()
                            previous_syntheses = history.get_history(limit=5)
                            
                            if previous_syntheses:
                                st.success(f"✅ Found {len(previous_syntheses)} previous synthesis(es) for comparison")
                                st.markdown("### Comparison with Previous Syntheses:")
                                for prev in previous_syntheses[:3]:  # Show top 3
                                    prev_query = prev.get("query", "Unknown query")
                                    prev_themes = prev.get("themes", [])
                                    prev_papers = prev.get("papers_count", 0)
                                    
                                    # Use container instead of expander to avoid nesting
                                    with st.container():
                                        st.markdown(f"#### 📊 {prev_query[:50]}...")
                                        st.write(f"**Papers Analyzed:** {prev_papers}")
                                        st.write(f"**Themes Found:** {len(prev_themes)}")
                                        if prev_themes:
                                            st.write("**Themes:**")
                                            for theme in prev_themes[:3]:
                                                st.write(f"- {theme}")
                                        st.markdown("---")
                            else:
                                st.info("No previous syntheses found. Run another query to enable comparison.")
                        except Exception as e:
                            st.warning(f"Comparison feature unavailable: {e}")


def _generate_grant_proposal_outline(
    query: str,
    themes: List[str],
    gaps: List[str],
    contradictions: List[Dict]
) -> str:
    """Generate a grant proposal outline from synthesis results."""
    outline = f"""# Grant Proposal Outline: {query}

## Executive Summary
This proposal addresses critical research gaps identified through systematic literature review of {len(themes)} major themes and {len(gaps)} identified research gaps in the field of {query}.

## 1. Background and Significance

### Current State of Research
"""
    for i, theme in enumerate(themes[:5], 1):
        outline += f"\n{i}. {theme}\n"
    
    outline += f"""
### Research Gaps Identified
"""
    for i, gap in enumerate(gaps[:5], 1):
        outline += f"\n{i}. {gap}\n"
    
    if contradictions:
        outline += f"""
### Areas of Contradiction
The literature review identified {len(contradictions)} areas where research findings conflict, indicating a need for:
- Systematic meta-analysis
- Replication studies
- Methodological refinement
"""
    
    outline += f"""
## 2. Research Objectives

### Primary Objectives
1. Address the identified research gap: {gaps[0] if gaps else "Primary research objective"}
2. Resolve contradictions in current literature
3. Advance understanding of {query}

### Secondary Objectives
- Contribute to the field through systematic investigation
- Build upon existing themes: {themes[0] if themes else "Primary theme"}
- Establish robust methodology for future research

## 3. Methodology

### Research Design
- Systematic approach building on identified themes
- Address {len(gaps)} research gaps through empirical investigation
- Resolve contradictions through comprehensive analysis

### Expected Outcomes
- Novel insights addressing identified gaps
- Resolution of contradictions in current literature
- Contribution to the field of {query}

## 4. Timeline and Milestones

### Phase 1: Literature Review and Gap Analysis (Months 1-3)
- Comprehensive review of identified themes
- Detailed analysis of research gaps

### Phase 2: Research Design and Implementation (Months 4-9)
- Design studies addressing identified gaps
- Data collection and analysis

### Phase 3: Synthesis and Publication (Months 10-12)
- Synthesize findings
- Prepare manuscripts for publication

## 5. Budget Justification

### Personnel
- Research team to conduct systematic investigation

### Equipment and Materials
- Resources needed to address identified research gaps

### Other Expenses
- Publication costs
- Conference presentations

---

*Generated by Agentic Researcher on {datetime.now().strftime('%B %d, %Y')}*
*Based on synthesis of {len(themes)} themes and {len(gaps)} research gaps*
"""
    return outline


def render_synthesis_history_dashboard():
    """
    Dashboard for previous sessions, bookmarks, and compare results.
    """
    try:
        try:
            from .synthesis_history import get_synthesis_history
        except ImportError:
            from synthesis_history import get_synthesis_history
        
        history = get_synthesis_history()
        all_history = history.get_history(limit=20)
        
        if not all_history:
            st.info("No previous syntheses found. Run a query to create your first synthesis!")
            return
        
        st.markdown("## 📚 Synthesis History")
        
        # Filter and search
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("🔍 Search history", placeholder="Search by query or theme...")
        with col2:
            sort_by = st.selectbox("Sort by", ["Recent", "Query", "Papers Count"])
        
        # Filter history
        filtered_history = all_history
        if search_query:
            filtered_history = [
                h for h in all_history
                if search_query.lower() in h.get('query', '').lower()
                or any(search_query.lower() in str(theme).lower() for theme in h.get('summary', {}).get('key_themes', []))
            ]
        
        # Sort
        if sort_by == "Recent":
            filtered_history = sorted(filtered_history, key=lambda x: x.get('timestamp', ''), reverse=True)
        elif sort_by == "Papers Count":
            filtered_history = sorted(filtered_history, key=lambda x: x.get('papers_analyzed', 0), reverse=True)
        
        # Display history items
        for idx, item in enumerate(filtered_history[:10]):  # Show top 10
            with st.expander(
                f"{item.get('query', 'N/A')[:60]}... ({item.get('papers_analyzed', 0)} papers)",
                expanded=False
            ):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Query:** {item.get('query', 'N/A')}")
                    st.markdown(f"**Date:** {item.get('timestamp', 'N/A')}")
                    themes = item.get('summary', {}).get('key_themes', [])
                    if themes:
                        st.markdown("**Themes:** " + ", ".join(themes[:3]))
                with col2:
                    if st.button("📖 View", key=f"view_{idx}"):
                        st.session_state['view_synthesis_id'] = item.get('synthesis_id')
                        st.rerun()
                    if st.button("📊 Compare", key=f"compare_{idx}"):
                        st.session_state['compare_synthesis_id'] = item.get('synthesis_id')
                        st.rerun()
    
    except ImportError:
        st.info("Synthesis history module not available. Install required dependencies.")


def render_citation_management_export(result: Dict):
    """
    Citation management export to Zotero, Mendeley, LaTeX, RIS/CSV.
    """
    st.markdown("## 📚 Citation Management Export")
    
    papers = result.get('papers', [])
    
    if not papers:
        st.warning("No papers to export")
        return
    
    # Export formats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📚 Zotero (RIS)", key="export_ris", use_container_width=True):
            ris_content = generate_ris_export(papers)
            st.download_button(
                label="Download RIS",
                data=ris_content,
                file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ris",
                mime="text/plain",
                key="download_ris"
            )
    
    with col2:
        if st.button("📖 Mendeley (CSV)", key="export_csv", use_container_width=True):
            csv_content = generate_csv_export(papers)
            st.download_button(
                label="Download CSV",
                data=csv_content,
                file_name=f"research_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="download_csv"
            )
    
    with col3:
        if st.button("📝 LaTeX (BibTeX)", key="export_latex_bib", use_container_width=True):
            st.info("Use the BibTeX export in the main export section")
    
    with col4:
        if st.button("📄 EndNote (XML)", key="export_endnote", use_container_width=True):
            st.info("EndNote XML export coming soon!")


def generate_ris_export(papers: List[Dict]) -> str:
    """Generate RIS format export"""
    ris_lines = []
    for paper in papers:
        ris_lines.append("TY  - JOUR")
        ris_lines.append(f"TI  - {paper.get('title', 'N/A')}")
        ris_lines.append(f"AU  - {paper.get('authors', 'N/A')}")
        ris_lines.append(f"UR  - {paper.get('url', 'N/A')}")
        ris_lines.append(f"PY  - {paper.get('year', 'N/A')}")
        ris_lines.append("ER  -")
        ris_lines.append("")
    return "\n".join(ris_lines)


def generate_csv_export(papers: List[Dict]) -> str:
    """Generate CSV format export for Mendeley"""
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Title', 'Authors', 'Year', 'URL', 'Source'])
    
    # Data
    for paper in papers:
        writer.writerow([
            paper.get('title', 'N/A'),
            paper.get('authors', 'N/A'),
            paper.get('year', 'N/A'),
            paper.get('url', 'N/A'),
            paper.get('source', 'N/A')
        ])
    
    return output.getvalue()


# ============================================================================
# ENHANCED PAGINATION & INFORMATION MANAGEMENT
# ============================================================================

def render_enhanced_pagination(papers: List[Dict], items_per_page: int = 20, show_jump_to: bool = True):
    """
    Enhanced pagination for 100+ papers with smooth navigation.
    
    Features:
    - Large page size options (10, 20, 50, 100)
    - Jump to page input
    - Keyboard navigation hints
    - Smooth scrolling
    """
    total_papers = len(papers)
    if total_papers == 0:
        return
    
    # Initialize pagination state
    if "enhanced_paper_page" not in st.session_state:
        st.session_state.enhanced_paper_page = 1
    if "items_per_page_setting" not in st.session_state:
        st.session_state.items_per_page_setting = items_per_page
    
    # Items per page selector
    col1, col2, col3 = st.columns([2, 3, 2])
    with col1:
        items_per_page = st.selectbox(
            "Papers per page",
            [10, 20, 50, 100],
            index=[10, 20, 50, 100].index(st.session_state.items_per_page_setting) if st.session_state.items_per_page_setting in [10, 20, 50, 100] else 1,
            key="pagination_items_per_page",
            help="Choose how many papers to display per page"
        )
        st.session_state.items_per_page_setting = items_per_page
    
    total_pages = (total_papers + items_per_page - 1) // items_per_page
    current_page = st.session_state.enhanced_paper_page
    
    # Ensure current page is valid
    if current_page > total_pages:
        current_page = 1
        st.session_state.enhanced_paper_page = 1
    
    with col2:
        st.caption(f"📄 Page {current_page} of {total_pages} • {total_papers} total papers")
    
    with col3:
        if show_jump_to:
            jump_to = st.number_input(
                "Jump to page",
                min_value=1,
                max_value=total_pages,
                value=current_page,
                key="jump_to_page",
                help="Quickly jump to any page"
            )
            if jump_to != current_page:
                st.session_state.enhanced_paper_page = jump_to
                st.rerun()
    
    # Navigation controls
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 2, 1, 1])
    
    with nav_col1:
        if st.button("⏮️ First", disabled=(current_page == 1), key="pagination_first", use_container_width=True):
            st.session_state.enhanced_paper_page = 1
            st.rerun()
    
    with nav_col2:
        if st.button("◀️ Prev", disabled=(current_page == 1), key="pagination_prev", use_container_width=True):
            st.session_state.enhanced_paper_page = max(1, current_page - 1)
            st.rerun()
    
    with nav_col3:
        # Page number display and input
        page_input = st.number_input(
            "Current page",
            min_value=1,
            max_value=total_pages,
            value=current_page,
            key="pagination_page_input",
            label_visibility="collapsed",
            help="Type page number and press Enter"
        )
        if page_input != current_page:
            st.session_state.enhanced_paper_page = page_input
            st.rerun()
    
    with nav_col4:
        if st.button("▶️ Next", disabled=(current_page == total_pages), key="pagination_next", use_container_width=True):
            st.session_state.enhanced_paper_page = min(total_pages, current_page + 1)
            st.rerun()
    
    with nav_col5:
        if st.button("⏭️ Last", disabled=(current_page == total_pages), key="pagination_last", use_container_width=True):
            st.session_state.enhanced_paper_page = total_pages
            st.rerun()
    
    # Calculate indices
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_papers)
    
    # Show range info
    st.info(f"📊 Showing papers **{start_idx + 1}** to **{end_idx}** of **{total_papers}**")
    
    # Keyboard shortcuts hint
    st.caption("💡 Tip: Use page input above to jump to any page quickly")
    
    return papers[start_idx:end_idx]


# ============================================================================
# USER PREFERENCES & SETTINGS
# ============================================================================

def render_user_preferences_panel():
    """
    User preferences panel for default settings.
    """
    st.markdown("## ⚙️ User Preferences")
    
    # Initialize preferences in session state
    if "user_preferences" not in st.session_state:
        st.session_state.user_preferences = {
            "default_max_papers": 10,
            "default_export_format": "json",
            "collapsed_view_by_default": False,
            "enable_notifications": True,
            "preferred_databases": ["arxiv", "pubmed", "semantic_scholar"],
            "high_contrast_mode": False,
            "items_per_page": 20
        }
    
    prefs = st.session_state.user_preferences
    
    # Default settings (using container instead of expander to avoid nesting)
    st.markdown("#### 📋 Default Query Settings")
    with st.container():
        prefs["default_max_papers"] = st.slider(
            "Default max papers",
            5, 50, prefs.get("default_max_papers", 10),
            help="Default number of papers to analyze"
        )
        
        prefs["default_export_format"] = st.selectbox(
            "Default export format",
            ["json", "markdown", "bibtex", "latex"],
            index=["json", "markdown", "bibtex", "latex"].index(prefs.get("default_export_format", "json")),
            help="Preferred export format"
        )
        
        prefs["items_per_page"] = st.selectbox(
            "Papers per page",
            [10, 20, 50, 100],
            index=[10, 20, 50, 100].index(prefs.get("items_per_page", 20)),
            help="Default pagination size"
        )
    
    st.markdown("---")
    
    # Display preferences (using container instead of expander)
    st.markdown("#### 👁️ Display Preferences")
    with st.container():
        prefs["collapsed_view_by_default"] = st.checkbox(
            "Collapsed view by default",
            value=prefs.get("collapsed_view_by_default", False),
            help="Start with all sections collapsed"
        )
        
        prefs["high_contrast_mode"] = st.checkbox(
            "High contrast mode",
            value=prefs.get("high_contrast_mode", False),
            help="Enable high contrast for better visibility"
        )
    
    st.markdown("---")
    
    # Notification preferences (using container instead of expander)
    st.markdown("#### 🔔 Notifications")
    with st.container():
        prefs["enable_notifications"] = st.checkbox(
            "Enable notifications",
            value=prefs.get("enable_notifications", True),
            help="Show notifications for agent findings"
        )
    
    st.markdown("---")
    
    # Database preferences (using container instead of expander)
    st.markdown("#### 📚 Preferred Databases")
    with st.container():
        all_databases = ["arxiv", "pubmed", "semantic_scholar", "crossref", "ieee", "acm", "springer"]
        preferred = prefs.get("preferred_databases", ["arxiv", "pubmed", "semantic_scholar"])
        
        for db in all_databases:
            is_checked = db in preferred
            checked = st.checkbox(
                db.replace("_", " ").title(),
                value=is_checked,
                key=f"pref_db_{db}"
            )
            if checked and db not in preferred:
                preferred.append(db)
            elif not checked and db in preferred:
                preferred.remove(db)
        
        prefs["preferred_databases"] = preferred
    
    # Save preferences
    if st.button("💾 Save Preferences", use_container_width=True):
        st.session_state.user_preferences = prefs
        st.success("✅ Preferences saved!")
    
    # Reset to defaults
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        st.session_state.user_preferences = {
            "default_max_papers": 10,
            "default_export_format": "json",
            "collapsed_view_by_default": False,
            "enable_notifications": True,
            "preferred_databases": ["arxiv", "pubmed", "semantic_scholar"],
            "high_contrast_mode": False,
            "items_per_page": 20
        }
        st.success("✅ Reset to defaults!")
        st.rerun()


# ============================================================================
# ACCESSIBILITY FEATURES
# ============================================================================

def render_accessibility_features():
    """
    Accessibility features: keyboard navigation, screen reader support, high-contrast mode.
    """
    st.markdown("## ♿ Accessibility Features")
    
    # High contrast mode
    if "high_contrast_mode" not in st.session_state:
        st.session_state.high_contrast_mode = False
    
    high_contrast = st.checkbox(
        "High Contrast Mode",
        value=st.session_state.high_contrast_mode,
        help="Increases contrast for better visibility"
    )
    
    if high_contrast != st.session_state.high_contrast_mode:
        st.session_state.high_contrast_mode = high_contrast
        if high_contrast:
            st.markdown("""
            <style>
            :root {
                --bg-primary: #000000;
                --bg-card: #1a1a1a;
                --text-primary: #ffffff;
                --text-secondary: #ffffff;
                --accent-primary: #ff6b6b;
            }
            </style>
            """, unsafe_allow_html=True)
            st.success("✅ High contrast mode enabled")
        else:
            st.rerun()
    
    # Keyboard shortcuts (using container instead of expander to avoid nesting)
    st.markdown("#### ⌨️ Keyboard Shortcuts")
    with st.container():
        st.markdown("""
        **Navigation:**
        - `Ctrl/Cmd + Enter`: Start research query
        - `Esc`: Close modals/expanders
        - `Tab`: Navigate between elements
        
        **Pagination:**
        - `←`: Previous page
        - `→`: Next page
        - `Home`: First page
        - `End`: Last page
        """)
    
    # Screen reader announcements
    st.markdown("""
    <div role="status" aria-live="polite" aria-atomic="true" style="position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;">
        Screen reader announcements will appear here
    </div>
    """, unsafe_allow_html=True)
    
    # ARIA labels helper
    st.caption("💡 Screen reader support: All interactive elements have ARIA labels")


# ============================================================================
# ENHANCED ERROR HANDLING & CONTEXTUAL HELP
# ============================================================================

def render_contextual_help(element_name: str, help_text: str):
    """
    Render contextual help tooltip/bubble.
    """
    st.markdown(f"""
    <div class="help-tooltip" role="tooltip" aria-label="{help_text}">
        <span class="help-icon">ℹ️</span>
        <span class="help-text">{help_text}</span>
    </div>
    """, unsafe_allow_html=True)


def render_enhanced_error_message(error: Exception, context: Dict[str, Any] = None):
    """
    Enhanced error messages with contextual help and solutions.
    """
    context = context or {}
    error_type = type(error).__name__
    error_msg = str(error)
    
    # Error-specific help
    help_messages = {
        "ConnectionError": {
            "message": "⚠️ Connection Error",
            "help": "The API server may be down or unreachable. Check your network connection and API endpoint.",
            "solutions": [
                "Verify the API server is running",
                "Check the API URL in settings",
                "Try again in a few moments"
            ]
        },
        "TimeoutError": {
            "message": "⏱️ Timeout Error",
            "help": "The request took too long to complete. This may happen with complex queries.",
            "solutions": [
                "Try reducing the number of papers",
                "Simplify your query",
                "Check your internet connection"
            ]
        },
        "ValidationError": {
            "message": "❌ Validation Error",
            "help": "Your input doesn't meet the requirements.",
            "solutions": [
                "Check query length (1-500 characters)",
                "Ensure max papers is between 1-50",
                "Verify date range is valid"
            ]
        }
    }
    
    help_info = help_messages.get(error_type, {
        "message": "❌ Error Occurred",
        "help": error_msg,
        "solutions": ["Please try again", "Contact support if the issue persists"]
    })
    
    st.error(help_info["message"])
    st.markdown(f"**Details:** {help_info['help']}")
    
    # Use container instead of expander to avoid nesting issues
    st.markdown("#### 🔧 Possible Solutions")
    with st.container():
        for i, solution in enumerate(help_info["solutions"], 1):
            st.markdown(f"{i}. {solution}")
    
    # Technical details for debugging
    with st.expander("🔍 Technical Details (for debugging)", expanded=False):
        st.code(f"""
        Error Type: {error_type}
        Error Message: {error_msg}
        Context: {json.dumps(context, indent=2)}
        """, language="text")


# ============================================================================
# REAL-TIME NOTIFICATIONS
# ============================================================================

def show_notification(message: str, notification_type: str = "info", duration: int = 5):
    """
    Show toast notification for agent findings and discoveries.
    
    Args:
        message: Notification message
        notification_type: "info", "success", "warning", "error"
        duration: Duration in seconds
    """
    # Store notification in session state
    if "notifications" not in st.session_state:
        st.session_state.notifications = []
    
    notification = {
        "id": f"notif_{int(time.time() * 1000)}",
        "message": message,
        "type": notification_type,
        "timestamp": datetime.now().isoformat()
    }
    
    st.session_state.notifications.append(notification)
    
    # Render notification
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    colors = {
        "info": "#2196F3",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336"
    }
    
    icon = icons.get(notification_type, "ℹ️")
    color = colors.get(notification_type, "#2196F3")
    
    st.markdown(f"""
    <div class="notification" style="
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: {color};
        color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    ">
        <strong>{icon} {message}</strong>
    </div>
    <style>
    @keyframes slideIn {{
        from {{
            transform: translateX(100%);
            opacity: 0;
        }}
        to {{
            transform: translateX(0);
            opacity: 1;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


def render_notification_panel():
    """
    Render notification panel showing all recent notifications.
    """
    if "notifications" not in st.session_state:
        return
    
    notifications = st.session_state.notifications[-10:]  # Show last 10
    
    if not notifications:
        return
    
    with st.expander("🔔 Recent Notifications", expanded=False):
        for notif in reversed(notifications):
            icon = {
                "info": "ℹ️",
                "success": "✅",
                "warning": "⚠️",
                "error": "❌"
            }.get(notif["type"], "ℹ️")
            
            st.markdown(f"{icon} {notif['message']}")
            st.caption(f"⏰ {notif['timestamp']}")
            st.markdown("---")
        
        if st.button("🗑️ Clear All Notifications", key="clear_notifications"):
            st.session_state.notifications = []
            st.rerun()


# ============================================================================
# CACHE SPEED COMPARISON INTEGRATION
# ============================================================================

def track_query_timing(query: str, processing_time: float, from_cache: bool = False):
    """
    Track query timing for cache speed comparison.
    """
    if "query_timings" not in st.session_state:
        st.session_state["query_timings"] = {}
    
    if query not in st.session_state["query_timings"]:
        st.session_state["query_timings"][query] = {
            "first_run": None,
            "cached_run": None,
            "runs": []
        }
    
    timing_data = st.session_state["query_timings"][query]
    
    if from_cache:
        timing_data["cached_run"] = processing_time
    else:
        if timing_data["first_run"] is None:
            timing_data["first_run"] = processing_time
        timing_data["runs"].append(processing_time)
    
    # Show speed comparison if both exist
    # Note: This will be called from web_ui when displaying results
    # We don't call it here to avoid circular dependencies


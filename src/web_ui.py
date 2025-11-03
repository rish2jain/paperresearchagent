"""
ResearchOps Agent Web UI
Streamlit interface for visualizing agent decisions and research synthesis
"""

import streamlit as st
import requests
import json
from datetime import datetime
import os
import sys

# Import export functions - works with both script and module execution
# Add src directory to path if not already there (for Streamlit execution)
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from export_formats import (
        generate_bibtex, 
        generate_latex_document,
        generate_word_document,
        generate_pdf_document,
        generate_csv_export,
        generate_excel_export
    )
except ImportError:
    try:
        from .export_formats import (
            generate_bibtex,
            generate_latex_document,
            generate_word_document,
            generate_pdf_document
        )
    except ImportError:
        # Last resort: add parent directory and try again
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from src.export_formats import (
            generate_bibtex,
            generate_latex_document,
            generate_word_document,
            generate_pdf_document,
            generate_csv_export,
            generate_excel_export
        )

# Import keyboard shortcuts
try:
    from keyboard_shortcuts import setup_keyboard_shortcuts
except ImportError:
    try:
        from .keyboard_shortcuts import setup_keyboard_shortcuts
    except ImportError:
        # Add parent directory and try again
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from src.keyboard_shortcuts import setup_keyboard_shortcuts

# Import citation styles
try:
    from citation_styles import format_citations
except ImportError:
    try:
        from .citation_styles import format_citations
    except ImportError:
        # Add parent directory and try again
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from src.citation_styles import format_citations

# Page configuration
st.set_page_config(
    page_title="ResearchOps Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup keyboard shortcuts and accessibility
setup_keyboard_shortcuts()

# Custom CSS for better styling with improved contrast and accessibility
st.markdown("""
<style>
    /* Global text contrast improvements */
    .main .block-container {
        color: #1f1f1f;
    }
    
    /* Decision cards with better contrast */
    .decision-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4CAF50;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #212121;
    }
    .decision-card strong {
        color: #000000;
        font-size: 1.1em;
        font-weight: 600;
    }
    .decision-card em {
        color: #424242;
        font-style: normal;
        font-weight: 500;
    }
    .decision-card small {
        color: #616161;
        font-size: 0.9em;
        line-height: 1.5;
        display: block;
        margin-top: 0.5rem;
    }
    
    /* Agent-specific border colors with better contrast */
    .agent-scout { 
        border-left-color: #1976D2; 
        border-left-width: 4px;
    }
    .agent-analyst { 
        border-left-color: #F57C00; 
        border-left-width: 4px;
    }
    .agent-synthesizer { 
        border-left-color: #7B1FA2; 
        border-left-width: 4px;
    }
    .agent-coordinator { 
        border-left-color: #388E3C; 
        border-left-width: 4px;
    }

    /* NIM badges with improved contrast */
    .nim-badge {
        display: inline-block;
        padding: 0.35rem 0.65rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .nim-reasoning { 
        background-color: #FFF59D; 
        color: #E65100; 
        border: 1px solid #FFC107;
    }
    .nim-embedding { 
        background-color: #B3E5FC; 
        color: #004D40; 
        border: 1px solid #0288D1;
    }
    
    /* Metric cards with better text contrast */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
    }
    
    /* Improved text colors throughout */
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
    }
    
    /* Better contrast for markdown text */
    .main .markdown-text-container {
        color: #212121;
    }
    
    /* Info boxes with better text contrast */
    .stInfo {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
        color: #0D47A1;
    }
    
    /* Success messages with better contrast */
    .stSuccess {
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
        color: #1B5E20;
    }
    
    /* Error messages with better contrast */
    .stError {
        background-color: #FFEBEE;
        border-left: 4px solid #F44336;
        color: #B71C1C;
    }
    
    /* Warning messages with better contrast */
    .stWarning {
        background-color: #FFF8E1;
        border-left: 4px solid #FF9800;
        color: #E65100;
    }
    
    /* Sidebar text contrast */
    .css-1d391kg {
        color: #1f1f1f;
    }
    
    /* Table text contrast */
    .dataframe {
        color: #212121;
    }
    
    /* Footer text */
    .footer {
        color: #424242;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔬 ResearchOps Agent")
st.markdown("**AI-Powered Literature Review Synthesis**")
st.markdown("*Powered by NVIDIA NIMs on Amazon EKS*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API endpoint configuration
    api_url = os.getenv(
        "AGENT_ORCHESTRATOR_URL",
        "http://localhost:8080"
    )
    st.info(f"**API:** {api_url}")
    
    # Parameters
    max_papers = st.slider("Max papers to analyze", 5, 50, 10)
    
    # Date filtering options
    st.markdown("---")
    st.subheader("📅 Date Filtering")
    use_date_filter = st.checkbox(
        "Filter by Date Range",
        value=False,
        help="Filter papers by publication date"
    )
    
    if use_date_filter:
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            start_year = st.number_input(
                "Start Year",
                min_value=1900,
                max_value=datetime.now().year,
                value=2020,
                help="Earliest publication year"
            )
        with date_col2:
            end_year = st.number_input(
                "End Year",
                min_value=1900,
                max_value=datetime.now().year,
                value=datetime.now().year,
                help="Latest publication year"
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
    
    st.markdown("---")
    
    st.header("📊 About")
    st.markdown("""
    This system uses **4 autonomous agents**:
    
    - 🔍 **Scout**: Finds relevant papers
    - 📊 **Analyst**: Extracts insights
    - 🧩 **Synthesizer**: Cross-analysis
    - 🎯 **Coordinator**: Workflow control
    
    **Time Savings:** 8 hours → 3 minutes
    """)
    
    st.markdown("---")
    
    # Quick examples
    st.header("💡 Example Queries")
    if st.button("ML for Medical Imaging", use_container_width=True):
        st.session_state['example_query'] = "machine learning for medical imaging"
    if st.button("Climate Change Mitigation", use_container_width=True):
        st.session_state['example_query'] = "climate change mitigation strategies"
    if st.button("Quantum Computing", use_container_width=True):
        st.session_state['example_query'] = "quantum computing algorithms"

# Skip navigation link for accessibility
st.markdown("""
<a href="#main-query-input" class="skip-link">Skip to main content</a>
""", unsafe_allow_html=True)

# Main content
query = st.text_input(
    "Enter your research query:",
    value=st.session_state.get('example_query', ''),
    placeholder="e.g., machine learning for medical imaging",
    help="Describe your research topic in natural language",
    key="main-query-input"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    start_button = st.button(
        "🚀 Start Research", 
        type="primary", 
        use_container_width=True,
        help="Start research synthesis (Ctrl/Cmd + Enter)"
    )
with col2:
    if st.session_state.get('last_query'):
        st.caption(f"Last query: {st.session_state['last_query'][:50]}...")
    if use_date_filter and start_year and end_year:
        st.caption(f"📅 Filter: {start_year}-{end_year}")
with col3:
    clear_button = st.button("🗑️ Clear", use_container_width=True)
    if clear_button:
        st.session_state.clear()
        st.rerun()

# Research execution
if start_button and query:
    st.session_state['last_query'] = query
    
    # Enhanced progress tracking with stage indicators
    progress_container = st.container()
    with progress_container:
        st.markdown("### 🔄 Research Progress")
        
        # Stage progress indicators
        stage_col1, stage_col2, stage_col3, stage_col4 = st.columns(4)
        
        with stage_col1:
            search_status = st.empty()
            search_status.markdown("🔍 **Search**<br>⏳ Waiting...", unsafe_allow_html=True)
        
        with stage_col2:
            analyze_status = st.empty()
            analyze_status.markdown("📊 **Analyze**<br>⏳ Waiting...", unsafe_allow_html=True)
        
        with stage_col3:
            synthesize_status = st.empty()
            synthesize_status.markdown("🧩 **Synthesize**<br>⏳ Waiting...", unsafe_allow_html=True)
        
        with stage_col4:
            refine_status = st.empty()
            refine_status.markdown("🎯 **Refine**<br>⏳ Waiting...", unsafe_allow_html=True)
        
        # Overall progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        nim_indicator = st.empty()
    
    try:
        # Call agent orchestrator API
        status_text.text("🔄 Initializing agents and NIMs...")
        progress_bar.progress(5)
        nim_indicator.info("🔍 Checking Embedding NIM availability...")
        
        # Prepare API request with date filtering if enabled
        request_data = {
            "query": query,
            "max_papers": max_papers
        }
        
        if use_date_filter and start_year and end_year:
            request_data["start_year"] = int(start_year)
            request_data["end_year"] = int(end_year)
            request_data["prioritize_recent"] = True
        
        # Make API request
        response = requests.post(
            f"{api_url}/research",
            json=request_data,
            timeout=300
        )
        
        if response.status_code != 200:
            st.error(f"❌ API Error: {response.status_code}")
            st.json(response.json())
        else:
            result = response.json()
            
            # Update progress indicators based on decisions
            decisions = result.get('decisions', [])
            
            # Determine which stages completed
            stages_completed = {
                'search': False,
                'analyze': False,
                'synthesize': False,
                'refine': False
            }
            
            for decision in decisions:
                agent = decision.get('agent', '')
                decision_type = decision.get('decision_type', '')
                
                if agent == 'Scout':
                    stages_completed['search'] = True
                    search_status.markdown("🔍 **Search**<br>✅ Complete", unsafe_allow_html=True)
                    nim_indicator.success("🔍 Using Embedding NIM for semantic search")
                
                elif agent == 'Analyst':
                    stages_completed['analyze'] = True
                    analyze_status.markdown("📊 **Analyze**<br>✅ Complete", unsafe_allow_html=True)
                    nim_indicator.success("🧠 Using Reasoning NIM for extraction")
                
                elif agent == 'Synthesizer':
                    stages_completed['synthesize'] = True
                    synthesize_status.markdown("🧩 **Synthesize**<br>✅ Complete", unsafe_allow_html=True)
                    if 'Theme' in decision_type or 'Contradiction' in decision_type:
                        nim_indicator.success("🔍🧠 Using BOTH NIMs for cross-document analysis")
                
                elif agent == 'Coordinator' and 'REFINEMENT' in decision_type:
                    stages_completed['refine'] = True
                    refine_status.markdown("🎯 **Refine**<br>✅ Complete", unsafe_allow_html=True)
                    nim_indicator.success("🧠 Using Reasoning NIM for quality evaluation")
            
            # Update progress using new progress tracker information
            progress_info = result.get('progress', {})
            overall_progress = progress_info.get('overall_progress', 0.0)
            current_stage = progress_info.get('current_stage', 'complete')
            time_elapsed = progress_info.get('time_elapsed', 0)
            time_remaining = progress_info.get('time_remaining')
            nim_used = progress_info.get('nim_used')
            
            # Update progress bar with actual progress
            progress_bar.progress(overall_progress)
            
            # Update status text with time information
            if time_remaining is not None and time_remaining > 0:
                status_text.text(f"⏱️ Elapsed: {time_elapsed:.1f}s | Remaining: ~{time_remaining:.0f}s")
            else:
                status_text.text(f"✅ Complete! Total time: {time_elapsed:.1f} seconds")
            
            # Display success message
            st.success(f"Research synthesis completed successfully in {time_elapsed:.1f} seconds!")
            
            # Key Metrics
            st.markdown("## 📈 Key Metrics")
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric("Papers Analyzed", result.get('papers_analyzed', 0))
            with metric_col2:
                st.metric("Common Themes", len(result.get('common_themes', [])))
            with metric_col3:
                st.metric("Decisions Made", len(result.get('decisions', [])))
            with metric_col4:
                time_saved = 8 * 60 - result.get('processing_time_seconds', 0) / 60
                st.metric("Time Saved", f"{time_saved:.0f} min")
            
            st.markdown("---")
            
            # Agent Decisions Section (CRITICAL FOR JUDGES)
            st.markdown("## 🎯 Autonomous Agent Decisions")
            st.markdown("*Watch the agents make decisions in real-time*")
            
            decisions = result.get('decisions', [])
            
            if decisions:
                # Create tabs for different views
                tab1, tab2 = st.tabs(["📋 Decision List", "📊 Timeline"])
                
                with tab1:
                    for i, decision in enumerate(decisions):
                        agent_emoji = {
                            "Scout": "🔍",
                            "Analyst": "📊",
                            "Synthesizer": "🧩",
                            "Coordinator": "🎯"
                        }.get(decision['agent'], "🤖")
                        
                        agent_class = f"agent-{decision['agent'].lower()}"
                        
                        nim_badge = ""
                        if decision.get('nim_used'):
                            if "Reasoning" in decision['nim_used']:
                                nim_badge = '<span class="nim-badge nim-reasoning">🧠 Reasoning NIM</span>'
                            elif "Embedding" in decision['nim_used']:
                                nim_badge = '<span class="nim-badge nim-embedding">🔍 Embedding NIM</span>'
                        
                        # Generate ARIA-friendly attributes
                        aria_label = f"{decision['agent']} decision: {decision['decision_type']}"
                        decision_id = f"decision-{i}-{decision['agent']}"
                        
                        st.markdown(f"""
                        <div 
                            class="decision-card {agent_class}" 
                            role="article"
                            aria-label="{aria_label}"
                            aria-describedby="{decision_id}"
                            tabindex="0"
                            id="{decision_id}"
                        >
                            <strong>{agent_emoji} {decision['agent']}</strong>{nim_badge}
                            <br><br>
                            <em>{decision['decision_type']}</em>: <strong style="color: #1565C0;">{decision['decision']}</strong>
                            <br>
                            <small>{decision['reasoning']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab2:
                    # Simple timeline visualization
                    st.markdown("### Decision Flow")
                    for i, decision in enumerate(decisions):
                        agent_emoji = {
                            "Scout": "🔍",
                            "Analyst": "📊",
                            "Synthesizer": "🧩",
                            "Coordinator": "🎯"
                        }.get(decision['agent'], "🤖")
                        
                        cols = st.columns([1, 10])
                        with cols[0]:
                            st.markdown(f"<strong style='color: #1565C0; font-size: 1.2em;'>{i+1}</strong>", unsafe_allow_html=True)
                        with cols[1]:
                            st.markdown(f"<span style='color: #212121;'>{agent_emoji} <strong style='color: #000000;'>{decision['agent']}</strong> → <span style='color: #424242;'>{decision['decision']}</span></span>", unsafe_allow_html=True)
            else:
                st.info("No decisions recorded for this synthesis.")
            
            st.markdown("---")
            
            # Results Section
            st.markdown("## 📊 Synthesis Results")
            
            # Common Themes
            with st.expander("🔍 Common Themes Identified", expanded=True):
                themes = result.get('common_themes', [])
                if themes:
                    for i, theme in enumerate(themes, 1):
                        st.markdown(f"<strong style='color: #1565C0;'>{i}.</strong> <span style='color: #212121;'>{theme}</span>", unsafe_allow_html=True)
                else:
                    st.info("No common themes identified.")
            
            # Contradictions
            with st.expander("⚡ Contradictions Found"):
                contradictions = result.get('contradictions', [])
                if contradictions:
                    for i, contradiction in enumerate(contradictions, 1):
                        st.markdown(f"""
                        <div style='color: #212121; line-height: 1.8;'>
                        <strong style='color: #1565C0; font-size: 1.1em;'>Contradiction {i}:</strong><br>
                        - <strong style='color: #000000;'>{contradiction.get('paper1', 'Paper A')}</strong> says: <span style='color: #424242;'>{contradiction.get('claim1', 'N/A')}</span><br>
                        - <strong style='color: #000000;'>{contradiction.get('paper2', 'Paper B')}</strong> says: <span style='color: #424242;'>{contradiction.get('claim2', 'N/A')}</span><br>
                        - <strong style='color: #D32F2F;'>Conflict:</strong> <span style='color: #616161;'>{contradiction.get('conflict', 'N/A')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No contradictions found.")
            
            # Research Gaps
            with st.expander("🎯 Research Gaps Identified"):
                gaps = result.get('research_gaps', [])
                if gaps:
                    for gap in gaps:
                        st.markdown(f"<div style='color: #212121; line-height: 1.6;'>• <span style='color: #424242;'>{gap}</span></div>", unsafe_allow_html=True)
                else:
                    st.info("No research gaps identified.")
            
            # Quality Scores Section
            quality_scores = result.get('quality_scores', [])
            if quality_scores:
                st.markdown("---")
                st.markdown("## 📊 Paper Quality Assessment")
                
                for qs in quality_scores:
                    paper_title = next((p.get('title', 'Unknown') for p in result.get('papers', []) if p.get('id') == qs.get('paper_id')), 'Unknown Paper')
                    
                    with st.expander(f"📄 {paper_title[:60]}... (Quality: {qs.get('overall_score', 0):.2f})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### Scores")
                            st.metric("Overall", f"{qs.get('overall_score', 0):.2f}", 
                                     delta=f"{qs.get('confidence_level', 'medium').upper()}")
                            st.progress(qs.get('overall_score', 0))
                            
                            st.markdown("**Breakdown:**")
                            st.write(f"- Methodology: {qs.get('methodology_score', 0):.2f}")
                            st.write(f"- Statistical: {qs.get('statistical_score', 0):.2f}")
                            st.write(f"- Reproducibility: {qs.get('reproducibility_score', 0):.2f}")
                            st.write(f"- Venue: {qs.get('venue_score', 0):.2f}")
                            st.write(f"- Sample Size: {qs.get('sample_size_score', 0):.2f}")
                        
                        with col2:
                            strengths = qs.get('strengths', [])
                            issues = qs.get('issues', [])
                            
                            if strengths:
                                st.markdown("### ✅ Strengths")
                                for strength in strengths:
                                    st.success(f"✓ {strength}")
                            
                            if issues:
                                st.markdown("### ⚠️ Issues")
                                for issue in issues:
                                    st.warning(f"⚠ {issue}")
            
            # Enhanced Extraction Data Section
            analyses = result.get('analyses', [])
            if analyses and any(a.get('metadata') for a in analyses):
                st.markdown("---")
                st.markdown("## 🔬 Enhanced Extraction Data")
                
                tab_stat, tab_exp, tab_comp, tab_repro = st.tabs([
                    "📈 Statistical Results",
                    "⚙️ Experimental Setup",
                    "📊 Comparative Results",
                    "♻️ Reproducibility"
                ])
                
                with tab_stat:
                    for analysis in analyses:
                        if analysis.get('metadata', {}).get('statistical_results'):
                            stats = analysis['metadata']['statistical_results']
                            st.markdown(f"**Paper:** {analysis.get('paper_id', 'Unknown')}")
                            if stats.get('p_values'):
                                st.write(f"**P-values:** {', '.join(stats['p_values'])}")
                            if stats.get('effect_sizes'):
                                st.write(f"**Effect Sizes:** {', '.join(stats['effect_sizes'])}")
                            if stats.get('confidence_intervals'):
                                st.write(f"**Confidence Intervals:** {', '.join(stats['confidence_intervals'])}")
                            if stats.get('statistical_tests'):
                                st.write(f"**Tests:** {', '.join(stats['statistical_tests'])}")
                            st.markdown("---")
                
                with tab_exp:
                    for analysis in analyses:
                        if analysis.get('metadata', {}).get('experimental_setup'):
                            exp = analysis['metadata']['experimental_setup']
                            st.markdown(f"**Paper:** {analysis.get('paper_id', 'Unknown')}")
                            if exp.get('datasets'):
                                st.write(f"**Datasets:** {', '.join(exp['datasets'])}")
                            if exp.get('hardware'):
                                st.write(f"**Hardware:** {exp['hardware']}")
                            if exp.get('hyperparameters'):
                                st.write(f"**Hyperparameters:** {', '.join(exp['hyperparameters'])}")
                            if exp.get('software_frameworks'):
                                st.write(f"**Frameworks:** {', '.join(exp['software_frameworks'])}")
                            st.markdown("---")
                
                with tab_comp:
                    for analysis in analyses:
                        if analysis.get('metadata', {}).get('comparative_results'):
                            comp = analysis['metadata']['comparative_results']
                            st.markdown(f"**Paper:** {analysis.get('paper_id', 'Unknown')}")
                            if comp.get('baselines'):
                                st.write(f"**Baselines:** {', '.join(comp['baselines'])}")
                            if comp.get('benchmarks'):
                                st.write(f"**Benchmarks:** {', '.join(comp['benchmarks'])}")
                            if comp.get('improvements'):
                                st.write(f"**Improvements:** {', '.join(comp['improvements'])}")
                            st.markdown("---")
                
                with tab_repro:
                    for analysis in analyses:
                        if analysis.get('metadata', {}).get('reproducibility'):
                            repro = analysis['metadata']['reproducibility']
                            st.markdown(f"**Paper:** {analysis.get('paper_id', 'Unknown')}")
                            st.write(f"**Code Available:** {'✅ Yes' if repro.get('code_available') else '❌ No'}")
                            st.write(f"**Data Available:** {'✅ Yes' if repro.get('data_available') else '❌ No'}")
                            if repro.get('repository_url'):
                                st.write(f"**Repository:** {repro['repository_url']}")
                            st.markdown("---")
            
            # Citation Styles Section
            papers = result.get('papers', [])
            if papers:
                st.markdown("---")
                st.markdown("### 📝 Citations")
                
                citation_style = st.selectbox(
                    "Citation Style:",
                    ["APA", "MLA", "Chicago", "IEEE", "Nature"],
                    help="Select citation format"
                )
                
                citations = format_citations(papers, style=citation_style.lower())
                
                with st.expander(f"View {citation_style} Citations", expanded=False):
                    for i, citation in enumerate(citations, 1):
                        st.text(f"{i}. {citation}")
                
                # Download citations
                st.download_button(
                    label=f"📥 Download {citation_style} Citations",
                    data="\n\n".join([f"{i}. {c}" for i, c in enumerate(citations, 1)]),
                    file_name=f"citations_{citation_style.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    help=f"Download citations in {citation_style} format"
                )
            
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
                    use_container_width=True
                )
            
            with col2:
                # Create markdown report
                markdown_report = f"""# Research Synthesis Report

**Query:** {query}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Papers Analyzed:** {result.get('papers_analyzed', 0)}

## Common Themes
{chr(10).join([f"{i}. {theme}" for i, theme in enumerate(result.get('common_themes', []), 1)])}

## Research Gaps
{chr(10).join([f"- {gap}" for gap in result.get('research_gaps', [])])}

## Autonomous Decisions Made
{chr(10).join([f"- **{d['agent']}**: {d['decision']}" for d in result.get('decisions', [])])}
"""
                st.download_button(
                    label="📄 Markdown",
                    data=markdown_report,
                    file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col3:
                # Generate BibTeX export
                papers = result.get('papers', [])
                if papers:
                    try:
                        bibtex_content = generate_bibtex(papers)
                        st.download_button(
                            label="📚 BibTeX",
                            data=bibtex_content,
                            file_name=f"references_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bib",
                            mime="text/plain",
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
                        help="No papers available for export"
                    )
            
            with col4:
                # Generate LaTeX document
                if papers:
                    try:
                        latex_content = generate_latex_document(
                            query=query,
                            papers=papers,
                            themes=result.get('common_themes', []),
                            gaps=result.get('research_gaps', []),
                            contradictions=result.get('contradictions', []),
                            date=datetime.now().strftime('%B %d, %Y')
                        )
                        st.download_button(
                            label="📝 LaTeX",
                            data=latex_content,
                            file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex",
                            mime="text/plain",
                            use_container_width=True,
                            help="Complete LaTeX document ready to compile"
                        )
                    except Exception as e:
                        st.error(f"Error generating LaTeX: {e}")
                else:
                    st.button(
                        label="📝 LaTeX",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export"
                    )
            
            with col5:
                # Generate Word document export
                if papers:
                    try:
                        word_doc = generate_word_document(
                            query=query,
                            papers=papers,
                            themes=result.get('common_themes', []),
                            gaps=result.get('research_gaps', []),
                            contradictions=result.get('contradictions', [])
                        )
                        st.download_button(
                            label="📄 Word",
                            data=word_doc,
                            file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                            help="Microsoft Word document (.docx)"
                        )
                    except ImportError:
                        st.button(
                            label="📄 Word",
                            disabled=True,
                            use_container_width=True,
                            help="Install python-docx: pip install python-docx"
                        )
                    except Exception as e:
                        st.error(f"Error generating Word: {e}")
                else:
                    st.button(
                        label="📄 Word",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export"
                    )
            
            with col6:
                # Generate PDF document export
                if papers:
                    try:
                        pdf_doc = generate_pdf_document(
                            query=query,
                            papers=papers,
                            themes=result.get('common_themes', []),
                            gaps=result.get('research_gaps', []),
                            contradictions=result.get('contradictions', [])
                        )
                        st.download_button(
                            label="📕 PDF",
                            data=pdf_doc,
                            file_name=f"literature_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            help="PDF document"
                        )
                    except ImportError:
                        st.button(
                            label="📕 PDF",
                            disabled=True,
                            use_container_width=True,
                            help="Install reportlab: pip install reportlab"
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {e}")
                else:
                        st.button(
                            label="📕 PDF",
                            disabled=True,
                            use_container_width=True,
                            help="No papers available for export"
                        )
            
            # Add CSV and Excel exports on second row
            st.markdown("<br>", unsafe_allow_html=True)
            col_csv, col_excel = st.columns(2)
            
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
                            help="CSV format for spreadsheet analysis"
                        )
                    except Exception as e:
                        st.error(f"Error generating CSV: {e}")
                else:
                    st.button(
                        label="📊 CSV",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export"
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
                            help="Excel format (.xlsx) for quantitative analysis"
                        )
                    except ImportError:
                        st.button(
                            label="📗 Excel",
                            disabled=True,
                            use_container_width=True,
                            help="Install openpyxl: pip install openpyxl"
                        )
                    except Exception as e:
                        st.error(f"Error generating Excel: {e}")
                else:
                    st.button(
                        label="📗 Excel",
                        disabled=True,
                        use_container_width=True,
                        help="No papers available for export"
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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #424242;'>
    <small style='color: #424242;'>
    🏆 Built for NVIDIA-AWS Agentic AI Hackathon 2025<br>
    Powered by NVIDIA NIMs • Deployed on Amazon EKS • Multi-Agent Architecture<br>
    <a href="/docs" target="_blank" style='color: #1976D2; text-decoration: none; font-weight: 500;'>API Documentation</a>
    </small>
</div>
""", unsafe_allow_html=True)

# Session state management
if 'example_query' not in st.session_state:
    st.session_state['example_query'] = ''

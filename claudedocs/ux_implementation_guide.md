# UX Implementation Guide: Quick-Win Code Examples

**Companion to**: `ux_audit_comprehensive.md` and `ux_wireframes_visual.md`
**Purpose**: Concrete code examples for implementing priority UX improvements

---

## Priority 1: Research Insights Hero Section

### File: `src/web_ui.py`
### Location: After line ~1477 (after success message)

```python
def render_research_insights_hero(result: Dict) -> None:
    """
    Render hero section highlighting most valuable discoveries.

    Always visible, prominently placed, action-oriented.
    Priority: Contradictions > Gaps > Themes
    """
    contradictions = result.get("contradictions", [])
    gaps = result.get("research_gaps", [])
    themes = result.get("common_themes", [])
    papers_count = result.get("papers_analyzed", 0)

    st.markdown("## 🔍 Key Discoveries from Your Synthesis")
    st.markdown("*Your AI agents analyzed {0} papers and found critical insights you'd likely miss manually*".format(papers_count))

    # Hero card for most important finding
    with st.container():
        if contradictions:
            render_contradiction_hero(contradictions, papers_count)
        elif gaps:
            render_gap_hero(gaps, papers_count)
        elif themes:
            render_theme_hero(themes, papers_count)
        else:
            st.success("✅ Synthesis complete - no major contradictions found (strong consensus in literature)")

    st.markdown("---")

    # 3-column insight summary
    col1, col2, col3 = st.columns(3)

    with col1:
        render_gap_summary_card(gaps)

    with col2:
        render_contradiction_summary_card(contradictions)

    with col3:
        render_theme_summary_card(themes)

    st.caption("💡 Click any card to explore detailed findings")


def render_contradiction_hero(contradictions: List[Dict], papers_count: int) -> None:
    """Render hero card for contradictions (highest priority)."""
    contradiction_count = len(contradictions)
    high_impact = [c for c in contradictions if classify_impact(c) == "high"]

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #FFEBEE 0%, #FCE4EC 100%);
                padding: 2rem; border-radius: 8px; border-left: 4px solid #D32F2F;'>
        <h3 style='color: #C62828; margin-top: 0;'>🎯 MOST IMPORTANT FINDING</h3>
        <p style='font-size: 1.1rem; color: #212121; line-height: 1.6;'>
            Your agents discovered <strong>{contradiction_count} contradiction(s)</strong> in established
            research that would likely take 8+ hours to find manually analyzing {papers_count} papers.
        </p>
        <p style='color: #424242;'>
            These represent fundamental {get_contradiction_types(contradictions)} that
            directly impact study design and evaluation approaches.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Show most critical contradiction preview
    if high_impact:
        top_contradiction = high_impact[0]
        with st.expander("🔍 Preview: Most Critical Contradiction", expanded=False):
            st.markdown(f"**{top_contradiction.get('type', 'Methodological')} Debate**")
            st.markdown(f"• {top_contradiction.get('paper1', 'Paper A')}: {top_contradiction.get('claim1', '')[:100]}...")
            st.markdown(f"• {top_contradiction.get('paper2', 'Paper B')}: {top_contradiction.get('claim2', '')[:100]}...")
            st.markdown(f"→ **Impact**: {top_contradiction.get('implications', 'Affects your methodology')}")

    if st.button("📊 View Full Contradiction Analysis", use_container_width=True, type="primary"):
        # Scroll to contradictions section
        st.markdown('<a href="#contradictions-section"></a>', unsafe_allow_html=True)


def render_gap_summary_card(gaps: List[str]) -> None:
    """Render summary card for research gaps."""
    gap_count = len(gaps) if gaps else 0

    # Assess opportunity level
    high_opportunity = sum(1 for gap in gaps if assess_opportunity(gap) >= 7.0) if gaps else 0

    with st.container():
        st.markdown(f"""
        <div style='background: #E8F5E9; padding: 1.5rem; border-radius: 6px;
                    border-left: 4px solid #388E3C; min-height: 200px;'>
            <h4 style='color: #2E7D32; margin-top: 0;'>💡 Research Gaps</h4>
            <p style='font-size: 2rem; font-weight: 600; color: #1B5E20; margin: 0.5rem 0;'>
                {gap_count}
            </p>
            <p style='color: #424242; margin-bottom: 1rem;'>opportunities identified</p>
            {f"<p style='color: #1B5E20;'>🔥 <strong>{high_opportunity}</strong> high-opportunity gaps</p>" if high_opportunity > 0 else ""}
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎯 Explore All Gaps", key="explore_gaps", use_container_width=True):
            st.session_state.jump_to = "gaps"
            st.rerun()


def render_contradiction_summary_card(contradictions: List[Dict]) -> None:
    """Render summary card for contradictions."""
    contradiction_count = len(contradictions) if contradictions else 0
    high_impact = sum(1 for c in contradictions if classify_impact(c) == "high") if contradictions else 0

    with st.container():
        st.markdown(f"""
        <div style='background: #FFEBEE; padding: 1.5rem; border-radius: 6px;
                    border-left: 4px solid #D32F2F; min-height: 200px;'>
            <h4 style='color: #C62828; margin-top: 0;'>⚡ Critical Contradictions</h4>
            <p style='font-size: 2rem; font-weight: 600; color: #B71C1C; margin: 0.5rem 0;'>
                {contradiction_count}
            </p>
            <p style='color: #424242; margin-bottom: 1rem;'>found in literature</p>
            {f"<p style='color: #B71C1C;'>⚠️ <strong>{high_impact}</strong> high-impact debates</p>" if high_impact > 0 else ""}
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚡ View Details", key="view_contradictions", use_container_width=True):
            st.session_state.jump_to = "contradictions"
            st.rerun()


def render_theme_summary_card(themes: List[str]) -> None:
    """Render summary card for common themes."""
    theme_count = len(themes) if themes else 0

    with st.container():
        st.markdown(f"""
        <div style='background: #E3F2FD; padding: 1.5rem; border-radius: 6px;
                    border-left: 4px solid #1976D2; min-height: 200px;'>
            <h4 style='color: #1565C0; margin-top: 0;'>🎯 Emerging Consensus</h4>
            <p style='font-size: 2rem; font-weight: 600; color: #0D47A1; margin: 0.5rem 0;'>
                {theme_count}
            </p>
            <p style='color: #424242; margin-bottom: 1rem;'>major themes identified</p>
            <p style='color: #424242; font-size: 0.9rem;'>Areas of research convergence</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🧩 Synthesize", key="view_themes", use_container_width=True):
            st.session_state.jump_to = "themes"
            st.rerun()


def classify_impact(contradiction: Dict) -> str:
    """
    Classify contradiction impact level.

    Criteria:
    - High: Affects methodology, widely cited papers, unresolved
    - Medium: Conceptual differences, moderate citation impact
    - Low: Terminology, minor discrepancies
    """
    # TODO: Implement actual classification logic
    # For now, simple heuristic based on paper citations
    paper1_citations = contradiction.get("paper1_citations", 0)
    paper2_citations = contradiction.get("paper2_citations", 0)

    if paper1_citations > 500 or paper2_citations > 500:
        return "high"
    elif paper1_citations > 100 or paper2_citations > 100:
        return "medium"
    else:
        return "low"


def assess_opportunity(gap: str) -> float:
    """
    Assess research gap opportunity score (0-10).

    Criteria:
    - Novelty: How unexplored (0/23 papers = high novelty)
    - Feasibility: Resources, datasets available
    - Impact: Trending topic, citation potential
    """
    # TODO: Implement actual opportunity scoring
    # For now, return mock score
    return 8.0


def get_contradiction_types(contradictions: List[Dict]) -> str:
    """Get human-readable description of contradiction types."""
    types = [c.get("type", "methodological") for c in contradictions]
    if "methodological" in types:
        return "methodological debates"
    elif "conceptual" in types:
        return "conceptual disagreements"
    else:
        return "research tensions"


# Integration point in main results display (line ~1477):
if result:
    # ... existing success message code ...

    # INSERT NEW: Research Insights Hero Section
    render_research_insights_hero(result)

    st.markdown("---")

    # ... rest of existing code (efficiency comparison, etc.) ...
```

---

## Priority 2: Enhanced Contradiction Display

### File: `src/web_ui.py`
### Location: Replace existing contradiction expander (~line 1829)

```python
def render_enhanced_contradictions(
    contradictions: List[Dict],
    papers: List[Dict],
    themes: List[str]
) -> None:
    """
    Render contradictions with impact classification, context, and implications.

    Features:
    - Impact classification (High/Medium/Low)
    - Citation counts for credibility
    - "Why this matters" explanations
    - Cross-references to themes/gaps
    - Evidence chain
    """
    if not contradictions:
        st.success("✅ No major contradictions found - literature shows strong consensus")
        st.caption("This is actually good news! It means the field has converged on key concepts.")
        return

    # Add anchor for navigation
    st.markdown('<div id="contradictions-section"></div>', unsafe_allow_html=True)

    st.markdown("## ⚡ Contradictions Found")
    st.markdown("*Critical debates and tensions in the literature that impact your research*")

    # Classify contradictions by impact
    classified = []
    for contradiction in contradictions:
        impact = classify_contradiction_impact(contradiction, papers)
        classified.append({
            **contradiction,
            "impact": impact,
            "impact_score": {"high": 3, "medium": 2, "low": 1}[impact]
        })

    # Sort by impact score (high first)
    classified.sort(key=lambda x: x["impact_score"], reverse=True)

    # Render each contradiction
    for idx, contradiction in enumerate(classified):
        impact = contradiction["impact"]
        impact_config = {
            "high": {"emoji": "⚠️", "color": "#D32F2F", "bg": "#FFEBEE", "label": "HIGH IMPACT"},
            "medium": {"emoji": "💡", "color": "#F57C00", "bg": "#FFF3E0", "label": "MEDIUM IMPACT"},
            "low": {"emoji": "ℹ️", "color": "#1976D2", "bg": "#E3F2FD", "label": "LOW IMPACT"}
        }[impact]

        # High impact: expanded by default
        # Medium/Low: collapsed by default
        expanded = (impact == "high")

        with st.expander(
            f"{impact_config['emoji']} {impact_config['label']}: {contradiction.get('type', 'Contradiction')} #{idx+1}",
            expanded=expanded
        ):
            # Container with colored background
            st.markdown(f"""
            <div style='background: {impact_config['bg']}; padding: 1.5rem;
                        border-radius: 6px; border-left: 4px solid {impact_config['color']};'>
            """, unsafe_allow_html=True)

            # Paper A
            paper1_info = find_paper_metadata(contradiction.get("paper1"), papers)
            st.markdown("### 📄 Paper A")
            render_paper_citation_line(paper1_info)
            st.markdown(f"> {contradiction.get('claim1', 'N/A')}")

            st.markdown("")
            st.markdown("### ⚔️ VERSUS")
            st.markdown("")

            # Paper B
            paper2_info = find_paper_metadata(contradiction.get("paper2"), papers)
            st.markdown("### 📄 Paper B")
            render_paper_citation_line(paper2_info)
            st.markdown(f"> {contradiction.get('claim2', 'N/A')}")

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("---")

            # Why this matters
            st.markdown("### 🎯 Why This Matters for Your Research")
            implications = generate_contradiction_implications(contradiction, paper1_info, paper2_info)
            st.info(implications)

            # Context section
            st.markdown("### 📊 Context & Evidence")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                **Resolution Status**: {contradiction.get('resolution_status', 'Unresolved')}

                **Timeline**: {contradiction.get('timeline', 'Ongoing debate')}

                **Related**: {get_related_themes(contradiction, themes)}
                """)

            with col2:
                impact_percentage = contradiction.get('impact_percentage', 0)
                st.markdown(f"""
                **Impact**: Affects {impact_percentage}% of papers in review

                **Evidence**: {contradiction.get('evidence_count', 0)} papers cite this debate

                **Confidence**: {contradiction.get('confidence', 'Medium')}
                """)

            # Action buttons
            st.markdown("### 🔗 Actions")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📄 View Evidence Papers", key=f"contradiction_papers_{idx}"):
                    show_related_papers(contradiction, papers)

            with col2:
                if st.button("📋 Export as Markdown", key=f"contradiction_export_{idx}"):
                    export_contradiction(contradiction)

            with col3:
                if st.button("🔍 Deep Dive", key=f"contradiction_deep_{idx}"):
                    trigger_deep_dive(contradiction)


def render_paper_citation_line(paper_info: Dict) -> None:
    """Render compact citation line with quality signals."""
    authors = paper_info.get("authors", "Unknown")
    if isinstance(authors, list):
        authors = authors[0] + " et al." if len(authors) > 1 else authors[0]

    year = paper_info.get("year", "N/A")
    citations = paper_info.get("citations", 0)
    relevance = paper_info.get("relevance_score", 0)
    source = paper_info.get("source", "Unknown")

    st.markdown(f"""
    **{authors}, {year}**
    📊 {citations:,} citations | ⭐ {relevance:.0%} relevance | 📰 {source}
    """)


def classify_contradiction_impact(contradiction: Dict, papers: List[Dict]) -> str:
    """
    Classify contradiction impact using multiple factors.

    High Impact:
    - Methodological debates affecting study design
    - Papers with >500 citations
    - Unresolved debates from recent years

    Medium Impact:
    - Conceptual disagreements
    - Papers with 100-500 citations
    - Ongoing but not critical

    Low Impact:
    - Terminology differences
    - Papers with <100 citations
    - Minor discrepancies
    """
    # Get paper metadata
    paper1 = find_paper_metadata(contradiction.get("paper1"), papers)
    paper2 = find_paper_metadata(contradiction.get("paper2"), papers)

    # Citation-based scoring
    max_citations = max(
        paper1.get("citations", 0),
        paper2.get("citations", 0)
    )

    # Type-based scoring
    contradiction_type = contradiction.get("type", "").lower()
    type_score = {
        "methodological": 3,
        "conceptual": 2,
        "terminology": 1
    }.get(contradiction_type, 2)

    # Recency score (newer = more relevant)
    max_year = max(
        paper1.get("year", 2000),
        paper2.get("year", 2000)
    )
    recency_score = 3 if max_year >= 2023 else (2 if max_year >= 2020 else 1)

    # Combined scoring
    total_score = 0
    if max_citations > 500:
        total_score += 3
    elif max_citations > 100:
        total_score += 2
    else:
        total_score += 1

    total_score += type_score
    total_score += recency_score

    # Classification thresholds
    if total_score >= 8:
        return "high"
    elif total_score >= 5:
        return "medium"
    else:
        return "low"


def generate_contradiction_implications(
    contradiction: Dict,
    paper1: Dict,
    paper2: Dict
) -> str:
    """
    Generate contextual implications for contradiction.

    Explains why this matters and what researchers should do.
    """
    contradiction_type = contradiction.get("type", "methodological").lower()

    if "methodological" in contradiction_type:
        return f"""
        This methodological debate directly impacts your study design. If you're pursuing
        {extract_research_area(contradiction)} research, you must:

        1. **Choose your approach**: Align with either {paper1.get('authors', 'Paper A')}'s
           or {paper2.get('authors', 'Paper B')}'s methodology
        2. **Justify your choice**: Explicitly defend your methodological decisions in your
           methods section
        3. **Acknowledge the debate**: Reference this ongoing controversy in your literature
           review
        4. **Consider hybrid approaches**: Some researchers are proposing middle-ground solutions

        Your advisor will expect you to address this contradiction as it's central to the field's
        current methodological discourse.
        """
    elif "conceptual" in contradiction_type:
        return f"""
        This conceptual disagreement affects how you frame your research problem and contributions.

        Consider:
        - Which conceptualization better fits your research goals?
        - Can you contribute to resolving this conceptual tension?
        - Does your work support one view over the other?

        This is an opportunity to position your work within an active scholarly debate.
        """
    else:
        return f"""
        While this may seem like a minor discrepancy, be aware that different research communities
        use different terminology. Ensure your writing clearly defines your terms and acknowledges
        alternative framings where appropriate.
        """


def find_paper_metadata(paper_title: str, papers: List[Dict]) -> Dict:
    """Find paper metadata by title (fuzzy matching)."""
    for paper in papers:
        if paper_title.lower() in paper.get("title", "").lower():
            return paper

    # Default fallback
    return {
        "title": paper_title,
        "authors": "Unknown",
        "year": "N/A",
        "citations": 0,
        "relevance_score": 0,
        "source": "Unknown"
    }


def get_related_themes(contradiction: Dict, themes: List[str]) -> str:
    """Get related themes for contradiction."""
    # TODO: Implement actual relationship detection
    # For now, return mock relationship
    related = contradiction.get("related_themes", [])
    if related:
        return ", ".join([f"Theme #{i+1}" for i in related])
    else:
        return "No direct theme relationships"


def extract_research_area(contradiction: Dict) -> str:
    """Extract research area from contradiction context."""
    # Simple heuristic: look for key terms in claims
    claims = contradiction.get("claim1", "") + " " + contradiction.get("claim2", "")

    if "evaluation" in claims.lower():
        return "evaluation"
    elif "scaling" in claims.lower():
        return "scaling"
    elif "architecture" in claims.lower():
        return "architecture"
    else:
        return "this"


# Integration point (replace existing contradiction expander):
# OLD CODE (~line 1829):
# with st.expander("⚡ Contradictions Found"):
#     contradictions = result.get("contradictions", [])
#     ...

# NEW CODE:
contradictions = result.get("contradictions", [])
papers = result.get("papers", [])
themes = result.get("common_themes", [])
render_enhanced_contradictions(contradictions, papers, themes)
```

---

## Priority 3: Actionable Research Gaps

### File: `src/web_ui.py`
### Location: Replace existing gap expander (~line 1848)

```python
def render_actionable_research_gaps(
    gaps: List[str],
    papers: List[Dict],
    themes: List[str],
    contradictions: List[Dict]
) -> None:
    """
    Render research gaps with opportunity assessment and actionable guidance.

    Features:
    - Opportunity scoring (novelty, feasibility, impact)
    - Suggested next steps
    - Evidence citations
    - Related work search integration
    - Collective intelligence (trending gaps)
    """
    if not gaps:
        st.info("✅ No significant research gaps identified - field appears well-covered")
        st.caption("The literature provides comprehensive coverage of this topic.")
        return

    # Add anchor for navigation
    st.markdown('<div id="gaps-section"></div>', unsafe_allow_html=True)

    st.markdown("## 🎯 Research Gaps Identified")
    st.markdown("*Opportunities for original research contributions, ranked by potential impact*")

    # Assess and rank gaps
    assessed_gaps = []
    for idx, gap in enumerate(gaps):
        assessment = assess_gap_opportunity(gap, papers, themes, contradictions)
        assessed_gaps.append({
            "title": extract_gap_title(gap),
            "description": gap,
            "opportunity_level": assessment["level"],
            "opportunity_score": assessment["score"],
            "novelty_score": assessment["novelty"],
            "feasibility_score": assessment["feasibility"],
            "impact_score": assessment["impact"],
            "evidence_count": assessment["evidence_count"],
            "next_steps": assessment["next_steps"]
        })

    # Sort by opportunity score
    assessed_gaps.sort(key=lambda x: x["opportunity_score"], reverse=True)

    # Render gaps by opportunity level
    for idx, gap in enumerate(assessed_gaps):
        level = gap["opportunity_level"]
        level_config = {
            "high": {"emoji": "🔥", "color": "#388E3C", "bg": "#E8F5E9", "label": "HIGH OPPORTUNITY"},
            "medium": {"emoji": "💡", "color": "#F57C00", "bg": "#FFF3E0", "label": "MEDIUM OPPORTUNITY"},
            "low": {"emoji": "📝", "color": "#1976D2", "bg": "#E3F2FD", "label": "LOW OPPORTUNITY"}
        }[level]

        # High opportunity: expanded by default
        expanded = (level == "high")

        with st.expander(
            f"{level_config['emoji']} {level_config['label']}: {gap['title']}",
            expanded=expanded
        ):
            # Header with opportunity score
            st.markdown(f"""
            <div style='background: {level_config['bg']}; padding: 1.5rem;
                        border-radius: 6px; border-left: 4px solid {level_config['color']};'>
                <h3 style='color: {level_config['color']}; margin-top: 0;'>
                    {gap['title']}
                </h3>
                <p style='color: #424242; font-size: 0.9rem;'>
                    Overall Opportunity Score: {gap['opportunity_score']:.1f}/10
                    {"⭐" * int(gap['opportunity_score'] / 2.5)}
                </p>
            </div>
            """, unsafe_allow_html=True)

            # What's missing
            st.markdown("### 📊 What's Missing")
            st.markdown(gap["description"])

            # Opportunity assessment
            st.markdown("### 🎯 Opportunity Assessment")
            col1, col2, col3 = st.columns(3)

            with col1:
                render_opportunity_metric(
                    "Novelty",
                    gap["novelty_score"],
                    "How unexplored is this gap?",
                    f"{count_papers_addressing_gap(gap, papers)}/{len(papers)} papers address this"
                )

            with col2:
                render_opportunity_metric(
                    "Feasibility",
                    gap["feasibility_score"],
                    "How practical to address?",
                    assess_feasibility_factors(gap)
                )

            with col3:
                render_opportunity_metric(
                    "Impact",
                    gap["impact_score"],
                    "Potential research contribution",
                    assess_impact_factors(gap, papers)
                )

            # Suggested next steps
            st.markdown("### 💡 Suggested Next Steps")
            for step_idx, step in enumerate(gap["next_steps"], 1):
                st.markdown(f"{step_idx}. {step}")

            # Evidence and context
            st.markdown("### 📚 Evidence & Context")
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""
                **Evidence**: {gap['evidence_count']} papers cite this limitation or call for future work

                **Related**: {get_related_themes_for_gap(gap, themes)}

                **Timeline**: {assess_gap_urgency(gap)}
                """)

            with col2:
                # Collective intelligence
                try:
                    trending_info = get_trending_gap_info(gap['title'])
                    if trending_info:
                        st.warning(f"""
                        ⚠️ **Trending Opportunity**

                        {trending_info['researcher_count']} other researchers
                        identified this gap this month

                        → Move quickly!
                        """)
                except:
                    pass  # Silent fail for collective intelligence

            # Action buttons
            st.markdown("### 🔗 Take Action")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📄 View Evidence Papers", key=f"gap_papers_{idx}"):
                    show_gap_evidence(gap, papers)

            with col2:
                if st.button("🔍 Search arXiv for Updates", key=f"gap_search_{idx}"):
                    trigger_arxiv_search(gap['title'])

            with col3:
                if st.button("💾 Save to Reading List", key=f"gap_save_{idx}"):
                    add_to_reading_list_gap(gap)


def assess_gap_opportunity(
    gap: str,
    papers: List[Dict],
    themes: List[str],
    contradictions: List[Dict]
) -> Dict:
    """
    Assess research gap opportunity across multiple dimensions.

    Returns:
        Dict with opportunity level, scores, and recommendations
    """
    # Novelty: How unexplored (0/N papers = high novelty)
    papers_addressing = count_papers_addressing_gap(gap, papers)
    novelty_score = 10 * (1 - papers_addressing / max(len(papers), 1))

    # Feasibility: Resources, datasets, methods available
    feasibility_score = assess_feasibility_score(gap, papers)

    # Impact: Trending, citations, related to contradictions
    impact_score = assess_impact_score(gap, papers, contradictions)

    # Overall score (weighted average)
    overall_score = (novelty_score * 0.4 + feasibility_score * 0.3 + impact_score * 0.3)

    # Classify opportunity level
    if overall_score >= 7.5:
        level = "high"
    elif overall_score >= 5.0:
        level = "medium"
    else:
        level = "low"

    # Generate next steps
    next_steps = generate_gap_next_steps(gap, level, papers)

    # Count evidence
    evidence_count = count_gap_evidence(gap, papers)

    return {
        "level": level,
        "score": overall_score,
        "novelty": novelty_score,
        "feasibility": feasibility_score,
        "impact": impact_score,
        "evidence_count": evidence_count,
        "next_steps": next_steps
    }


def render_opportunity_metric(
    label: str,
    score: float,
    help_text: str,
    context: str
) -> None:
    """Render opportunity metric card."""
    score_level = "High" if score >= 7 else ("Medium" if score >= 4 else "Low")
    color = "#388E3C" if score >= 7 else ("#F57C00" if score >= 4 else "#1976D2")

    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: #FAFAFA; border-radius: 6px;'>
        <h4 style='color: {color}; margin: 0;'>{label}</h4>
        <p style='font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0;'>
            {score_level}
        </p>
        <p style='font-size: 1.2rem; color: {color}; margin: 0.5rem 0;'>
            {score:.1f}/10
        </p>
        <p style='font-size: 0.85rem; color: #757575; margin-top: 0.5rem;'>
            {context}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(help_text)


def count_papers_addressing_gap(gap: str, papers: List[Dict]) -> int:
    """Count how many papers address this gap."""
    # Simple keyword matching in titles and abstracts
    gap_keywords = extract_keywords(gap)
    count = 0

    for paper in papers:
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower()
        text = title + " " + abstract

        # Check if any gap keywords appear
        if any(keyword.lower() in text for keyword in gap_keywords):
            count += 1

    return count


def assess_feasibility_score(gap: str, papers: List[Dict]) -> float:
    """Assess feasibility of addressing this gap."""
    # Check for availability of:
    # - Datasets
    # - Methods
    # - Tools

    feasibility = 5.0  # Baseline medium

    # Boost if related datasets are mentioned in papers
    if any("dataset" in p.get("abstract", "").lower() for p in papers):
        feasibility += 2.0

    # Boost if methods are well-established
    if any("method" in p.get("title", "").lower() for p in papers):
        feasibility += 1.0

    # Cap at 10
    return min(feasibility, 10.0)


def assess_impact_score(
    gap: str,
    papers: List[Dict],
    contradictions: List[Dict]
) -> float:
    """Assess potential impact of addressing this gap."""
    impact = 5.0  # Baseline

    # Check if gap is related to contradictions (high impact)
    if is_gap_related_to_contradiction(gap, contradictions):
        impact += 3.0

    # Check if multiple papers mention this limitation
    limitation_count = count_limitation_mentions(gap, papers)
    if limitation_count >= 3:
        impact += 2.0
    elif limitation_count >= 1:
        impact += 1.0

    # Cap at 10
    return min(impact, 10.0)


def generate_gap_next_steps(gap: str, level: str, papers: List[Dict]) -> List[str]:
    """Generate actionable next steps for gap."""
    steps = []

    # Always: Search for recent work
    steps.append("🔍 Search arXiv and Google Scholar for papers published in last 3 months (check if someone beat you to it)")

    if level == "high":
        # High opportunity: prioritize and move fast
        steps.append("📚 Review related dataset papers to find suitable data for your approach")
        steps.append("🎓 Consider this as your primary research contribution (high novelty + high impact)")
        steps.append("⚠️ Move quickly - high-value gaps get filled fast (race condition likely)")
        steps.append("👥 Check if collaborators have relevant expertise or datasets")
    elif level == "medium":
        # Medium: worth pursuing but with more validation
        steps.append("💭 Validate the gap with domain experts before committing")
        steps.append("📊 Assess available resources (datasets, compute, time) before starting")
        steps.append("🔬 Consider as secondary contribution or future work")
    else:
        # Low: proceed with caution
        steps.append("❓ Reconsider if this gap is worth pursuing (low opportunity score)")
        steps.append("🤔 Check if there's a reason no one has addressed this (may not be valuable)")
        steps.append("📝 Better as 'future work' than primary contribution")

    return steps


def extract_gap_title(gap: str) -> str:
    """Extract concise title from gap description."""
    # Simple heuristic: take first clause or first 60 characters
    if ":" in gap:
        return gap.split(":")[0].strip()
    elif "." in gap:
        return gap.split(".")[0].strip()
    else:
        return gap[:60].strip() + ("..." if len(gap) > 60 else "")


def count_gap_evidence(gap: str, papers: List[Dict]) -> int:
    """Count papers that cite this limitation."""
    # Look for "limitation", "future work", "gap" in abstracts
    keywords = extract_keywords(gap)
    evidence_count = 0

    for paper in papers:
        abstract = paper.get("abstract", "").lower()
        if any(keyword.lower() in abstract for keyword in keywords):
            if "limitation" in abstract or "future work" in abstract:
                evidence_count += 1

    return evidence_count


def extract_keywords(text: str) -> List[str]:
    """Extract key terms from text."""
    # Simple keyword extraction (can be improved with NLP)
    # Remove common words and extract nouns/technical terms
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    words = text.lower().split()
    keywords = [w.strip(".,!?") for w in words if w not in stopwords and len(w) > 3]
    return keywords[:5]  # Top 5 keywords


# Integration point (replace existing gap expander):
# OLD CODE (~line 1848):
# with st.expander("🎯 Research Gaps Identified"):
#     gaps = result.get("research_gaps", [])
#     ...

# NEW CODE:
gaps = result.get("research_gaps", [])
papers = result.get("papers", [])
themes = result.get("common_themes", [])
contradictions = result.get("contradictions", [])
render_actionable_research_gaps(gaps, papers, themes, contradictions)
```

---

## Priority 4: Structured Synthesis Display

### File: `src/web_ui.py`
### Location: Replace `render_synthesis_collapsible()` call

```python
def render_structured_synthesis(result: Dict) -> None:
    """
    Render synthesis with clear visual structure and sections.

    Sections:
    1. Core Finding (1-2 sentences, always visible)
    2. Evidence Base (metadata about papers analyzed)
    3. Major Findings (structured with cross-references)
    4. Implications (actionable takeaways)
    """
    synthesis_text = result.get("synthesis", "")
    papers = result.get("papers", [])
    contradictions = result.get("contradictions", [])
    gaps = result.get("research_gaps", [])
    themes = result.get("common_themes", [])

    if not synthesis_text:
        st.info("No synthesis available.")
        return

    st.markdown("## 📝 Research Synthesis")
    st.markdown("*Structured summary of findings across all analyzed papers*")

    # 1. Core Finding (always visible, prominent)
    core_finding = extract_core_finding(synthesis_text)

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
                padding: 1.5rem; border-radius: 8px; border-left: 4px solid #1976D2; margin-bottom: 1.5rem;'>
        <h3 style='color: #0D47A1; margin-top: 0;'>🎯 Core Finding</h3>
        <p style='font-size: 1.1rem; color: #212121; line-height: 1.6; margin-bottom: 0;'>
            {core_finding}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Evidence Base
    with st.expander("📊 Evidence Base", expanded=True):
        render_evidence_metadata(papers, result)

    # 3. Major Findings with cross-references
    with st.expander("🔍 Major Findings", expanded=True):
        render_cross_referenced_findings(
            synthesis_text,
            contradictions,
            gaps,
            themes,
            papers
        )

    # 4. Implications (actionable)
    with st.expander("🎯 Implications for Your Research", expanded=True):
        render_research_implications(result)

    # Export options
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📥 Export as Markdown", use_container_width=True):
            export_synthesis_markdown(result)
    with col2:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            copy_synthesis_to_clipboard(result)


def extract_core_finding(synthesis: str) -> str:
    """
    Extract core finding (1-2 sentences summary).

    Logic:
    - If synthesis has clear structure, extract first paragraph
    - Otherwise, use first 2 sentences
    - Fallback: use first 200 characters
    """
    # Split into sentences
    sentences = synthesis.split(". ")

    # Use first 1-2 sentences
    if len(sentences) >= 2:
        core = sentences[0] + ". " + sentences[1] + "."
    elif len(sentences) == 1:
        core = sentences[0]
    else:
        core = synthesis[:200] + ("..." if len(synthesis) > 200 else "")

    return core.strip()


def render_evidence_metadata(papers: List[Dict], result: Dict) -> None:
    """Render evidence base metadata."""
    total_papers = len(papers)

    # Year distribution
    years = [p.get("year") for p in papers if p.get("year")]
    year_range = f"{min(years)}-{max(years)}" if years else "N/A"
    emphasis_years = [y for y in years if y >= 2023]

    # Source distribution
    sources = {}
    for paper in papers:
        source = paper.get("source", "Unknown")
        sources[source] = sources.get(source, 0) + 1

    # Methodology distribution
    methodologies = {}
    for paper in papers:
        methodology = paper.get("methodology", "Unknown")
        methodologies[methodology] = methodologies.get(methodology, 0) + 1

    # Average citations
    citations = [p.get("citations", 0) for p in papers if p.get("citations")]
    avg_citations = sum(citations) / len(citations) if citations else 0

    # Display metadata
    st.markdown(f"""
    ### 📚 Corpus Overview

    **Total papers analyzed**: {total_papers}

    **Publication timeline**: {year_range} (emphasis on {len(emphasis_years)} papers from 2023-2024)

    **Average citation count**: {avg_citations:.0f} (range: {min(citations) if citations else 0:,} - {max(citations) if citations else 0:,})
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📊 Source Distribution:**")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_papers) * 100
            st.markdown(f"- {source}: {count} ({percentage:.0f}%)")

    with col2:
        st.markdown("**🔬 Methodology Distribution:**")
        for methodology, count in sorted(methodologies.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_papers) * 100
            st.markdown(f"- {methodology}: {count} ({percentage:.0f}%)")


def render_cross_referenced_findings(
    synthesis: str,
    contradictions: List[Dict],
    gaps: List[str],
    themes: List[str],
    papers: List[Dict]
) -> None:
    """Render major findings with cross-references to other insights."""

    # 1. Consensus Areas (themes with high agreement)
    st.markdown("### 1️⃣ Consensus Areas")

    high_agreement_themes = identify_high_agreement_themes(themes, papers)

    if high_agreement_themes:
        for theme_idx, theme_info in enumerate(high_agreement_themes):
            theme = theme_info["theme"]
            agreement = theme_info["agreement_percentage"]
            paper_count = theme_info["paper_count"]

            st.markdown(f"""
            **{theme}** ✅ {agreement:.0f}% consensus ({paper_count} papers agree)

            {theme_info['summary']}

            🔗 Related: Theme #{theme_idx + 1}
            📊 Confidence: {"High" if agreement > 75 else "Medium"}
            """)

            st.markdown("---")
    else:
        st.info("No strong consensus identified - field is in active development")

    # 2. Active Debates (contradictions)
    st.markdown("### 2️⃣ Active Debates & Tensions")

    if contradictions:
        st.markdown(f"⚡ **{len(contradictions)} contradiction(s)** identified")

        for idx, contradiction in enumerate(contradictions[:3]):  # Show top 3
            impact = classify_contradiction_impact(contradiction, papers)
            st.markdown(f"""
            **Contradiction #{idx+1}**: {contradiction.get('type', 'Debate')}
            ({impact.upper()} impact)

            - {contradiction.get('paper1', 'Paper A')}: {contradiction.get('claim1', '')[:100]}...
            - {contradiction.get('paper2', 'Paper B')}: {contradiction.get('claim2', '')[:100]}...

            🔗 [Jump to Contradiction #{idx+1}](#contradictions-section)
            📊 Confidence: Low (active debate)
            """)

            st.markdown("---")
    else:
        st.success("✅ No major contradictions - field shows strong agreement")

    # 3. Research Gaps (opportunities)
    st.markdown("### 3️⃣ Research Gaps & Opportunities")

    if gaps:
        st.markdown(f"🎯 **{len(gaps)} gap(s)** identified")

        # Show top 2 high-opportunity gaps
        assessed_gaps = assess_multiple_gaps(gaps, papers, themes, contradictions)
        high_opportunity_gaps = [g for g in assessed_gaps if g["opportunity_level"] == "high"]

        for gap in high_opportunity_gaps[:2]:
            st.markdown(f"""
            **{gap['title']}** 🔥 HIGH OPPORTUNITY

            {gap['description'][:150]}...

            Opportunity Score: {gap['opportunity_score']:.1f}/10 ⭐⭐⭐⭐

            🔗 [Explore Gap Details](#gaps-section)
            """)

            st.markdown("---")

        if len(gaps) > 2:
            st.caption(f"... and {len(gaps) - 2} more gaps identified")
    else:
        st.info("No significant gaps identified - field appears comprehensive")


def render_research_implications(result: Dict) -> None:
    """Render actionable implications section."""
    themes = result.get("common_themes", [])
    contradictions = result.get("contradictions", [])
    gaps = result.get("research_gaps", [])

    st.markdown("""
    Based on this synthesis, here are actionable implications for your research:
    """)

    # If pursuing scaling research
    if any("scal" in t.lower() for t in themes):
        st.markdown("""
        ✅ **IF PURSUING SCALING RESEARCH**:
        - Build on established scaling law foundations (cite consensus papers)
        - Focus on novel scaling dimensions (multimodal, cross-task, cross-lingual)
        - Acknowledge the well-established nature of basic scaling relationships
        """)
        st.markdown("")

    # If designing evaluation studies
    if contradictions:
        st.markdown("""
        ⚠️ **IF DESIGNING EVALUATION STUDIES**:
        - Acknowledge ongoing methodological debates in your methods section
        - Justify your methodological choices (cite relevant contradictions)
        - Consider hybrid approaches that address multiple perspectives
        - Explicitly state your position on contentious issues
        """)
        st.markdown("")

    # If writing literature review
    st.markdown("""
    🎯 **IF WRITING LITERATURE REVIEW**:
    - Emphasize 2023-2024 papers (field evolving rapidly)
    - Highlight active debates as key open questions
    - Note research gaps as areas for future investigation
    - Structure review around consensus vs. debate areas
    """)
    st.markdown("")

    # Primary contribution opportunities
    if gaps:
        high_opportunity_gaps = [g for g in gaps if assess_gap_opportunity(g, result.get("papers", []), themes, contradictions)["level"] == "high"]

        if high_opportunity_gaps:
            st.markdown(f"""
            💡 **PRIMARY CONTRIBUTION OPPORTUNITIES**:

            {len(high_opportunity_gaps)} high-opportunity gap(s) identified:
            """)

            for gap in high_opportunity_gaps[:2]:
                gap_title = extract_gap_title(gap)
                st.markdown(f"- **{gap_title}**: High novelty + high impact = strong publication target")

            st.markdown("")

    # Avoid common pitfalls
    st.markdown("""
    ⚠️ **AVOID COMMON PITFALLS**:
    - Don't ignore contradictions (reviewers will catch this)
    - Don't claim novelty in well-established consensus areas
    - Don't skip validation of high-opportunity gaps (search for recent work)
    - Don't overlook the temporal dimension (field changes fast)
    """)


def assess_multiple_gaps(
    gaps: List[str],
    papers: List[Dict],
    themes: List[str],
    contradictions: List[Dict]
) -> List[Dict]:
    """Assess all gaps and return sorted by opportunity."""
    assessed = []
    for gap in gaps:
        assessment = assess_gap_opportunity(gap, papers, themes, contradictions)
        assessed.append({
            "title": extract_gap_title(gap),
            "description": gap,
            **assessment
        })

    assessed.sort(key=lambda x: x["score"], reverse=True)
    return assessed


def identify_high_agreement_themes(themes: List[str], papers: List[Dict]) -> List[Dict]:
    """Identify themes with high paper agreement."""
    theme_info = []

    for theme in themes:
        # Count papers supporting this theme
        supporting_papers = count_papers_supporting_theme(theme, papers)
        agreement_percentage = (supporting_papers / max(len(papers), 1)) * 100

        if agreement_percentage >= 60:  # 60%+ threshold for consensus
            theme_info.append({
                "theme": theme,
                "agreement_percentage": agreement_percentage,
                "paper_count": supporting_papers,
                "summary": f"This theme appears consistently across the literature, with broad support from multiple research groups."
            })

    return theme_info


def count_papers_supporting_theme(theme: str, papers: List[Dict]) -> int:
    """Count papers that support this theme."""
    keywords = extract_keywords(theme)
    count = 0

    for paper in papers:
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower()
        text = title + " " + abstract

        # Check if theme keywords appear
        if any(keyword.lower() in text for keyword in keywords):
            count += 1

    return count


# Integration point (replace render_synthesis_collapsible):
# OLD CODE (~line 1811):
# synthesis_text = result.get("synthesis", "")
# if synthesis_text:
#     st.markdown("### 📝 Research Synthesis")
#     render_synthesis_collapsible(synthesis_text, preview_length=500)

# NEW CODE:
if result.get("synthesis"):
    render_structured_synthesis(result)
```

---

## Integration Summary

### Order of Implementation

1. **Research Insights Hero Section** (line ~1477)
   - Add after success message
   - Before efficiency comparison
   - Most visible position

2. **Enhanced Contradiction Display** (line ~1829)
   - Replace existing expander
   - Add impact classification
   - Add "why this matters" section

3. **Actionable Research Gaps** (line ~1848)
   - Replace existing expander
   - Add opportunity assessment
   - Add suggested next steps

4. **Structured Synthesis** (line ~1811)
   - Replace render_synthesis_collapsible()
   - Add core finding section
   - Add evidence base
   - Add cross-references

### Testing Checklist

- [ ] Hero section renders correctly
- [ ] High-impact contradictions expanded by default
- [ ] High-opportunity gaps expanded by default
- [ ] Core finding always visible
- [ ] Cross-references work (navigation)
- [ ] Mobile responsiveness maintained
- [ ] Performance not degraded

### Performance Considerations

- Use session state for expensive computations (gap assessment)
- Cache opportunity scores
- Lazy load evidence papers
- Limit cross-reference calculations

---

**END OF IMPLEMENTATION GUIDE**

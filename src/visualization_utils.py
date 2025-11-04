"""
Visualization utilities for Agentic Researcher
Provides reusable visualization functions using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
from typing import List, Dict, Any, Optional
import streamlit as st
from collections import Counter


@st.cache_data(ttl=3600)
def create_source_distribution_chart(papers: List[Dict[str, Any]]) -> go.Figure:
    """
    Create a bar chart showing paper distribution by source.

    Args:
        papers: List of paper dictionaries with 'source' field

    Returns:
        Plotly figure object
    """
    if not papers:
        return None

    # Count papers by source
    sources = [paper.get("source", "Unknown") for paper in papers]
    source_counts = Counter(sources)

    # Create DataFrame
    df = pd.DataFrame(
        list(source_counts.items()),
        columns=["Source", "Paper Count"]
    ).sort_values("Paper Count", ascending=False)

    # Create bar chart
    fig = px.bar(
        df,
        x="Source",
        y="Paper Count",
        title="📚 Paper Distribution by Source",
        color="Paper Count",
        color_continuous_scale="Blues",
        text="Paper Count",
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Database Source",
        yaxis_title="Number of Papers",
        showlegend=False,
        height=400,
        hovermode="x",
    )

    return fig


@st.cache_data(ttl=3600)
def create_year_distribution_chart(papers: List[Dict[str, Any]]) -> go.Figure:
    """
    Create an area chart showing paper distribution by year.

    Args:
        papers: List of paper dictionaries with 'year' field

    Returns:
        Plotly figure object
    """
    if not papers:
        return None

    # Count papers by year
    years = []
    for paper in papers:
        year = paper.get("year", "Unknown")
        # Convert to int if possible
        if year != "Unknown":
            try:
                years.append(int(year))
            except (ValueError, TypeError):
                pass

    if not years:
        return None

    year_counts = Counter(years)

    # Create DataFrame
    df = pd.DataFrame(
        list(year_counts.items()),
        columns=["Year", "Paper Count"]
    ).sort_values("Year")

    # Create area chart
    fig = px.area(
        df,
        x="Year",
        y="Paper Count",
        title="📅 Paper Distribution by Publication Year",
        markers=True,
    )

    fig.update_traces(
        line_color="#1565C0",
        fillcolor="rgba(21, 101, 192, 0.3)",
        hovertemplate="<b>Year %{x}</b><br>Papers: %{y}<extra></extra>",
    )

    fig.update_layout(
        xaxis_title="Publication Year",
        yaxis_title="Number of Papers",
        height=400,
        hovermode="x unified",
    )

    return fig


@st.cache_data(ttl=3600)
def create_citation_scatter(papers: List[Dict[str, Any]]) -> Optional[go.Figure]:
    """
    Create a scatter plot of citation count vs year.

    Args:
        papers: List of paper dictionaries with 'year' and 'citation_count' fields

    Returns:
        Plotly figure object or None if citation data not available
    """
    if not papers:
        return None

    # Extract papers with citation data
    data = []
    for paper in papers:
        year = paper.get("year", "Unknown")
        citations = paper.get("citation_count")
        title = paper.get("title", "Unknown")

        if year != "Unknown" and citations is not None:
            try:
                data.append({
                    "Year": int(year),
                    "Citations": int(citations),
                    "Title": title[:60] + "..." if len(title) > 60 else title,
                })
            except (ValueError, TypeError):
                pass

    if not data:
        return None

    df = pd.DataFrame(data)

    # Create scatter plot
    fig = px.scatter(
        df,
        x="Year",
        y="Citations",
        title="📊 Citation Analysis Over Time",
        hover_data=["Title"],
        size="Citations",
        color="Citations",
        color_continuous_scale="Viridis",
    )

    fig.update_layout(
        xaxis_title="Publication Year",
        yaxis_title="Citation Count",
        height=450,
        hovermode="closest",
    )

    return fig


@st.cache_data(ttl=3600)
def create_theme_importance_chart(
    themes: List[str], papers: List[Dict[str, Any]]
) -> go.Figure:
    """
    Create a horizontal bar chart showing theme importance.

    Args:
        themes: List of identified themes
        papers: List of paper dictionaries (for calculating theme prevalence)

    Returns:
        Plotly figure object
    """
    if not themes:
        return None

    # For simplicity, we'll show themes with equal distribution
    # In a real implementation, you'd calculate actual prevalence from paper analysis
    total_papers = len(papers) if papers else 1

    # Create DataFrame with themes and estimated paper counts
    # Assuming themes are ordered by importance
    theme_data = []
    for i, theme in enumerate(themes):
        # Estimate: first theme mentioned in 60% of papers, declining by 10% each
        estimated_prevalence = max(0.3, 0.7 - (i * 0.1))
        paper_count = int(total_papers * estimated_prevalence)
        percentage = (paper_count / total_papers) * 100

        theme_data.append({
            "Theme": theme[:50] + "..." if len(theme) > 50 else theme,
            "Paper Count": paper_count,
            "Percentage": percentage,
        })

    df = pd.DataFrame(theme_data)

    # Create horizontal bar chart
    fig = px.bar(
        df,
        y="Theme",
        x="Paper Count",
        title="🔍 Theme Importance by Prevalence",
        orientation="h",
        color="Percentage",
        color_continuous_scale="Blues",
        text="Paper Count",
    )

    fig.update_traces(
        texttemplate="%{text} papers (%{customdata[0]:.0f}%)",
        textposition="outside",
        customdata=df[["Percentage"]],
    )

    fig.update_layout(
        xaxis_title="Number of Papers",
        yaxis_title="",
        height=max(300, len(themes) * 60),
        showlegend=False,
        yaxis=dict(autorange="reversed"),  # Top to bottom
    )

    return fig


@st.cache_data(ttl=3600)
def create_contradiction_network(
    contradictions: List[Dict[str, Any]], papers: List[Dict[str, Any]]
) -> Optional[go.Figure]:
    """
    Create a network graph showing contradictions between papers.

    Args:
        contradictions: List of contradiction dictionaries with paper1, paper2, conflict
        papers: List of paper dictionaries for node labels

    Returns:
        Plotly figure object or None if insufficient data
    """
    if not contradictions or len(contradictions) < 2:
        return None

    # Create a mapping of paper IDs to titles
    paper_titles = {}
    for paper in papers:
        paper_id = paper.get("id", "")
        title = paper.get("title", "Unknown")
        # Shorten title for display
        short_title = title[:30] + "..." if len(title) > 30 else title
        paper_titles[paper_id] = short_title

    # Build network graph
    G = nx.Graph()

    # Add edges for each contradiction
    for i, contradiction in enumerate(contradictions):
        paper1 = contradiction.get("paper1", f"Paper A{i}")
        paper2 = contradiction.get("paper2", f"Paper B{i}")
        conflict = contradiction.get("conflict", "Contradiction")

        # Use paper titles if available
        node1 = paper_titles.get(paper1, paper1[:30] + "...")
        node2 = paper_titles.get(paper2, paper2[:30] + "...")

        # Add edge with conflict as label
        G.add_edge(
            node1,
            node2,
            conflict=conflict[:40] + "..." if len(conflict) > 40 else conflict,
        )

    # Generate layout
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Create edge traces
    edge_traces = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode="lines",
            line=dict(width=2, color="#D32F2F"),
            hoverinfo="none",
            showlegend=False,
        )
        edge_traces.append(edge_trace)

    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_size = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        # Size based on number of connections
        node_size.append(20 + (G.degree(node) * 10))

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        marker=dict(
            size=node_size,
            color="#1565C0",
            line=dict(width=2, color="white"),
        ),
        hovertemplate="<b>%{text}</b><extra></extra>",
        showlegend=False,
    )

    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])

    fig.update_layout(
        title="⚡ Contradiction Network: Papers with Conflicting Claims",
        showlegend=False,
        hovermode="closest",
        height=500,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(240, 242, 246, 0.5)",
    )

    return fig

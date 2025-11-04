"""
Citation Graph Analysis Module
Builds citation graphs from Semantic Scholar and Crossref data to trace
the evolution of ideas and identify influential research paths.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import asyncio

# Optional dependencies
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False

logger = logging.getLogger(__name__)


@dataclass
class CitationNode:
    """Represents a paper in the citation graph"""
    paper_id: str
    title: str
    authors: List[str]
    year: Optional[int] = None
    citation_count: int = 0
    citation_ids: List[str] = field(default_factory=list)  # Papers this cites
    cited_by_ids: List[str] = field(default_factory=list)  # Papers that cite this
    source: str = ""


@dataclass
class CitationGraph:
    """Citation graph structure"""
    nodes: Dict[str, CitationNode] = field(default_factory=dict)
    edges: Set[Tuple[str, str]] = field(default_factory=set)  # (citing_paper, cited_paper)
    
    def add_paper(self, paper: CitationNode):
        """Add a paper node to the graph"""
        self.nodes[paper.paper_id] = paper
    
    def add_citation(self, citing_paper_id: str, cited_paper_id: str):
        """Add a citation edge (citing_paper -> cited_paper)"""
        if citing_paper_id in self.nodes and cited_paper_id in self.nodes:
            self.edges.add((citing_paper_id, cited_paper_id))
            # Update node references
            if cited_paper_id not in self.nodes[citing_paper_id].citation_ids:
                self.nodes[citing_paper_id].citation_ids.append(cited_paper_id)
            if citing_paper_id not in self.nodes[cited_paper_id].cited_by_ids:
                self.nodes[cited_paper_id].cited_by_ids.append(citing_paper_id)
    
    def get_seminal_papers(self, min_citations: int = 10) -> List[CitationNode]:
        """Identify seminal papers (highly cited)"""
        return [
            node for node in self.nodes.values()
            if len(node.cited_by_ids) >= min_citations
        ]
    
    def get_citation_path(self, from_paper_id: str, to_paper_id: str, max_depth: int = 5) -> Optional[List[str]]:
        """Find citation path between two papers using BFS"""
        if from_paper_id not in self.nodes or to_paper_id not in self.nodes:
            return None
        
        from collections import deque
        queue = deque([(from_paper_id, [from_paper_id])])
        visited = {from_paper_id}
        
        while queue and len(queue[0][1]) <= max_depth:
            current_id, path = queue.popleft()
            
            # Check if we reached the target
            if current_id == to_paper_id:
                return path
            
            # Explore cited papers (forward citations)
            current_node = self.nodes[current_id]
            for cited_id in current_node.citation_ids:
                if cited_id not in visited:
                    visited.add(cited_id)
                    queue.append((cited_id, path + [cited_id]))
        
        return None
    
    def get_evolution_timeline(self) -> List[CitationNode]:
        """Get papers sorted by publication year (evolution timeline)"""
        nodes_with_year = [node for node in self.nodes.values() if node.year is not None]
        return sorted(nodes_with_year, key=lambda n: n.year or 0)
    
    def get_influential_papers(self, top_n: int = 10) -> List[CitationNode]:
        """Get top N most influential papers (by citations received)"""
        nodes = list(self.nodes.values())
        nodes.sort(key=lambda n: len(n.cited_by_ids), reverse=True)
        return nodes[:top_n]


async def build_citation_graph_from_papers(
    papers: List[Dict[str, Any]],
    semantic_scholar_api_key: Optional[str] = None
) -> CitationGraph:
    """
    Build citation graph from paper data
    
    Args:
        papers: List of paper dictionaries
        semantic_scholar_api_key: Optional API key for Semantic Scholar
        
    Returns:
        CitationGraph object
    """
    graph = CitationGraph()
    
    # First, add all papers as nodes
    for paper in papers:
        paper_id = paper.get("id", "")
        if not paper_id:
            continue
        
        year = None
        if paper.get("published_date"):
            try:
                # Try to extract year from date string
                date_str = paper["published_date"]
                if isinstance(date_str, str):
                    # Common formats: "2024", "2024-01-15", "Jan 2024"
                    year = int(date_str.split("-")[0]) if "-" in date_str else int(date_str[:4])
            except (ValueError, IndexError):
                pass
        
        node = CitationNode(
            paper_id=paper_id,
            title=paper.get("title", "Unknown"),
            authors=paper.get("authors", []),
            year=year,
            citation_count=paper.get("citation_count", 0),
            source=paper.get("source", "")
        )
        graph.add_paper(node)
    
    # Try to fetch citation data from Semantic Scholar if available
    if semantic_scholar_api_key:
        try:
            await _enrich_with_semantic_scholar(graph, semantic_scholar_api_key)
        except Exception as e:
            logger.warning(f"Failed to enrich citation graph with Semantic Scholar: {e}")
    
    # Try to extract citation relationships from Crossref if available
    try:
        await _enrich_with_crossref(graph)
    except Exception as e:
        logger.warning(f"Failed to enrich citation graph with Crossref: {e}")
    
    return graph


async def _enrich_with_semantic_scholar(graph: CitationGraph, api_key: str):
    """Enrich citation graph with Semantic Scholar data"""
    if not HAS_AIOHTTP:
        logger.warning("aiohttp not available, skipping Semantic Scholar enrichment")
        return
    
    headers = {"x-api-key": api_key} if api_key else {}
    
    async with aiohttp.ClientSession() as session:
        # Fetch citation data for each paper
        tasks = []
        for paper_id, node in graph.nodes.items():
            # Semantic Scholar uses paper IDs or DOIs
            if paper_id.startswith("semantic-scholar-"):
                ss_id = paper_id.replace("semantic-scholar-", "")
                tasks.append(_fetch_semantic_scholar_citations(session, ss_id, headers))
            elif node.source == "semantic_scholar":
                # Try to extract Semantic Scholar ID from URL or metadata
                tasks.append(_fetch_semantic_scholar_citations(session, paper_id, headers))
        
        # Process results
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                continue
            if result:
                paper_id, citations = result
                if paper_id in graph.nodes:
                    # Add citation edges
                    for cited_id in citations:
                        if cited_id in graph.nodes:
                            graph.add_citation(paper_id, cited_id)


async def _fetch_semantic_scholar_citations(
    session: aiohttp.ClientSession,
    paper_id: str,
    headers: Dict[str, str]
) -> Optional[Tuple[str, List[str]]]:
    """Fetch citations for a paper from Semantic Scholar"""
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references"
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
            if response.status == 200:
                data = await response.json()
                cited_ids = []
                for ref in data.get("data", []):
                    if ref.get("citedPaper", {}).get("paperId"):
                        cited_ids.append(f"semantic-scholar-{ref['citedPaper']['paperId']}")
                return (f"semantic-scholar-{paper_id}", cited_ids)
    except Exception as e:
        logger.debug(f"Failed to fetch Semantic Scholar citations for {paper_id}: {e}")
    return None


async def _enrich_with_crossref(graph: CitationGraph):
    """Enrich citation graph with Crossref reference data"""
    if not HAS_AIOHTTP:
        logger.warning("aiohttp not available, skipping Crossref enrichment")
        return
    
    async with aiohttp.ClientSession() as session:
        # Crossref has limited free access, so we'll be conservative
        for paper_id, node in graph.nodes.items():
            # Try to extract DOI from paper metadata
            # This is a placeholder - actual implementation would need DOI extraction
            pass


def analyze_citation_graph(graph: CitationGraph) -> Dict[str, Any]:
    """
    Analyze citation graph to identify patterns and insights
    
    Returns:
        Dictionary with analysis results
    """
    analysis = {
        "total_papers": len(graph.nodes),
        "total_citations": len(graph.edges),
        "seminal_papers": [],
        "influential_papers": [],
        "evolution_timeline": [],
        "citation_clusters": []
    }
    
    # Identify seminal papers (highly cited)
    seminal = graph.get_seminal_papers(min_citations=5)
    analysis["seminal_papers"] = [
        {
            "paper_id": p.paper_id,
            "title": p.title,
            "citations_received": len(p.cited_by_ids),
            "year": p.year
        }
        for p in seminal
    ]
    
    # Get influential papers
    influential = graph.get_influential_papers(top_n=10)
    analysis["influential_papers"] = [
        {
            "paper_id": p.paper_id,
            "title": p.title,
            "citations_received": len(p.cited_by_ids),
            "year": p.year
        }
        for p in influential
    ]
    
    # Get evolution timeline
    timeline = graph.get_evolution_timeline()
    analysis["evolution_timeline"] = [
        {
            "paper_id": p.paper_id,
            "title": p.title,
            "year": p.year,
            "citations_received": len(p.cited_by_ids)
        }
        for p in timeline[:20]  # Top 20 by year
    ]
    
    return analysis




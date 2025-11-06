"""
Graph-Based Synthesis Module
Uses Graph Neural Networks (GNNs) for advanced synthesis with citation relationships
"""

from typing import List, Dict, Any, Optional, Set, Tuple
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Optional dependencies
try:
    import torch
    import torch.nn as nn
    from torch_geometric.data import Data, Batch
    from torch_geometric.nn import GCNConv, GATConv, global_mean_pool
    TORCH_GEOMETRIC_AVAILABLE = True
except ImportError:
    TORCH_GEOMETRIC_AVAILABLE = False
    logger.warning("torch-geometric not available. Install with: pip install torch-geometric")

try:
    import networkx as nx
    from sklearn.cluster import SpectralClustering
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logger.warning("networkx not available. Install with: pip install networkx scikit-learn")

try:
    from citation_graph import CitationGraph, CitationNode
    CITATION_GRAPH_AVAILABLE = True
except ImportError:
    CITATION_GRAPH_AVAILABLE = False


@dataclass
class ThemeCluster:
    """Represents a theme cluster from graph analysis"""
    theme_id: str
    theme_name: str
    paper_ids: List[str]
    centrality_score: float
    citation_count: int


@dataclass
class BridgePaper:
    """Represents a bridge paper connecting different research areas"""
    paper_id: str
    title: str
    connecting_themes: List[str]
    bridge_score: float


class GraphAttentionNetwork(nn.Module):
    """
    Graph Attention Network for paper embedding and theme detection
    """
    
    def __init__(self, input_dim: int = 768, hidden_dim: int = 256, num_heads: int = 4):
        super().__init__()
        self.gat1 = GATConv(input_dim, hidden_dim, heads=num_heads, dropout=0.2)
        self.gat2 = GATConv(hidden_dim * num_heads, hidden_dim, heads=1, dropout=0.2)
        
    def forward(self, x, edge_index):
        """Forward pass through GAT layers"""
        x = self.gat1(x, edge_index)
        x = torch.relu(x)
        x = self.gat2(x, edge_index)
        return x


class GraphSynthesizer:
    """
    Graph-based synthesis using GNNs and community detection
    """
    
    def __init__(self, citation_graph: Optional[CitationGraph] = None):
        self.citation_graph = citation_graph
        self.gnn_model = None
        self.networkx_graph = None
    
    def build_networkx_graph(self, citation_graph: CitationGraph) -> nx.Graph:
        """Convert CitationGraph to NetworkX graph for analysis"""
        if not NETWORKX_AVAILABLE:
            return None
        
        G = nx.DiGraph()
        
        # Add nodes
        for paper_id, node in citation_graph.nodes.items():
            G.add_node(paper_id, title=node.title, citations=len(node.cited_by_ids))
        
        # Add edges (citations)
        for citing_id, cited_id in citation_graph.edges:
            G.add_edge(citing_id, cited_id)
        
        self.networkx_graph = G
        return G
    
    def detect_communities(self, graph: nx.Graph, n_clusters: int = 5) -> Dict[str, int]:
        """
        Detect communities (themes) using spectral clustering
        
        Args:
            graph: NetworkX graph
            n_clusters: Number of communities to detect
            
        Returns:
            Dictionary mapping paper_id to community_id
        """
        if not NETWORKX_AVAILABLE or graph is None:
            return {}
        
        try:
            # Convert to undirected for clustering
            G_undirected = graph.to_undirected()
            
            # Build adjacency matrix
            adj_matrix = nx.adjacency_matrix(G_undirected).toarray()
            
            # Spectral clustering
            clustering = SpectralClustering(
                n_clusters=n_clusters,
                affinity='precomputed',
                random_state=42
            )
            labels = clustering.fit_predict(adj_matrix)
            
            # Map paper IDs to communities
            paper_ids = list(G_undirected.nodes())
            community_map = {paper_id: int(label) for paper_id, label in zip(paper_ids, labels)}
            
            return community_map
            
        except Exception as e:
            logger.error(f"Community detection error: {e}")
            return {}
    
    def identify_bridge_papers(
        self,
        graph: nx.Graph,
        communities: Dict[str, int],
        top_k: int = 10
    ) -> List[BridgePaper]:
        """
        Identify bridge papers connecting different communities
        
        Args:
            graph: NetworkX graph
            communities: Community assignments
            top_k: Number of bridge papers to return
            
        Returns:
            List of BridgePaper objects
        """
        if not NETWORKX_AVAILABLE or graph is None:
            return []
        
        bridge_scores = []
        
        for paper_id in graph.nodes():
            # Get neighbors
            neighbors = list(graph.neighbors(paper_id))
            
            # Find communities of neighbors
            neighbor_communities = set()
            for neighbor in neighbors:
                if neighbor in communities:
                    neighbor_communities.add(communities[neighbor])
            
            # Bridge score = number of different communities connected
            bridge_score = len(neighbor_communities)
            
            if bridge_score > 1:  # Connects multiple communities
                connecting_themes = [f"Theme_{c}" for c in neighbor_communities]
                
                bridge_scores.append(BridgePaper(
                    paper_id=paper_id,
                    title=graph.nodes[paper_id].get('title', 'Unknown'),
                    connecting_themes=connecting_themes,
                    bridge_score=bridge_score
                ))
        
        # Sort by bridge score
        bridge_scores.sort(key=lambda x: x.bridge_score, reverse=True)
        return bridge_scores[:top_k]
    
    def extract_theme_clusters(
        self,
        communities: Dict[str, int],
        citation_graph: CitationGraph,
        top_k: int = 10
    ) -> List[ThemeCluster]:
        """
        Extract theme clusters from community detection
        
        Args:
            communities: Community assignments
            citation_graph: Citation graph
            top_k: Number of themes to return
            
        Returns:
            List of ThemeCluster objects
        """
        # Group papers by community
        theme_map = {}
        for paper_id, community_id in communities.items():
            if community_id not in theme_map:
                theme_map[community_id] = []
            theme_map[community_id].append(paper_id)
        
        # Create theme clusters
        theme_clusters = []
        for theme_id, paper_ids in theme_map.items():
            if not paper_ids:
                continue
            
            # Calculate aggregate metrics
            citation_count = sum(
                len(citation_graph.nodes[pid].cited_by_ids)
                for pid in paper_ids
                if pid in citation_graph.nodes
            )
            
            # Calculate centrality (average)
            centrality_scores = []
            if self.networkx_graph:
                # Compute betweenness centrality once for the entire graph
                centrality_dict = nx.betweenness_centrality(self.networkx_graph)
                # Lookup centrality scores for each paper id
                for pid in paper_ids:
                    if pid in self.networkx_graph:
                        centrality = centrality_dict.get(pid, 0.0)
                        centrality_scores.append(centrality)
            
            avg_centrality = sum(centrality_scores) / len(centrality_scores) if centrality_scores else 0.0
            
            # Get representative paper title for theme name
            theme_name = f"Theme {theme_id}"
            if paper_ids and paper_ids[0] in citation_graph.nodes:
                theme_name = citation_graph.nodes[paper_ids[0]].title[:50] + "..."
            
            theme_clusters.append(ThemeCluster(
                theme_id=f"theme_{theme_id}",
                theme_name=theme_name,
                paper_ids=paper_ids,
                centrality_score=avg_centrality,
                citation_count=citation_count
            ))
        
        # Sort by centrality and citation count
        theme_clusters.sort(
            key=lambda x: (x.centrality_score, x.citation_count),
            reverse=True
        )
        
        return theme_clusters[:top_k]
    
    async def synthesize_with_graph(
        self,
        citation_graph: CitationGraph,
        analyses: List[Any],
        n_themes: int = 5
    ) -> Dict[str, Any]:
        """
        Perform graph-based synthesis
        
        Args:
            citation_graph: Citation graph
            analyses: List of paper analyses
            n_themes: Number of themes to identify
            
        Returns:
            Dictionary with synthesis results
        """
        if not CITATION_GRAPH_AVAILABLE or not citation_graph:
            logger.warning("Citation graph not available for graph synthesis")
            return {
                "themes": [],
                "bridge_papers": [],
                "communities": {}
            }
        
        # Build NetworkX graph
        graph = self.build_networkx_graph(citation_graph)
        if graph is None:
            logger.warning("Failed to build NetworkX graph")
            return {
                "themes": [],
                "bridge_papers": [],
                "communities": {}
            }
        
        # Detect communities
        communities = self.detect_communities(graph, n_clusters=n_themes)
        
        # Extract theme clusters
        theme_clusters = self.extract_theme_clusters(
            communities,
            citation_graph,
            top_k=n_themes
        )
        
        # Identify bridge papers
        bridge_papers = self.identify_bridge_papers(graph, communities, top_k=10)
        
        # Format results
        result = {
            "themes": [
                {
                    "theme_id": theme.theme_id,
                    "theme_name": theme.theme_name,
                    "paper_count": len(theme.paper_ids),
                    "centrality_score": theme.centrality_score,
                    "citation_count": theme.citation_count,
                    "paper_ids": theme.paper_ids
                }
                for theme in theme_clusters
            ],
            "bridge_papers": [
                {
                    "paper_id": bp.paper_id,
                    "title": bp.title,
                    "connecting_themes": bp.connecting_themes,
                    "bridge_score": bp.bridge_score
                }
                for bp in bridge_papers
            ],
            "communities": communities,
            "graph_stats": {
                "total_nodes": len(graph.nodes()),
                "total_edges": len(graph.edges()),
                "communities_detected": len(set(communities.values()))
            }
        }
        
        logger.info(
            f"Graph synthesis: {len(theme_clusters)} themes, "
            f"{len(bridge_papers)} bridge papers detected"
        )
        
        return result


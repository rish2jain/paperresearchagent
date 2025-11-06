"""
Hybrid Retrieval System
Combines dense retrieval (embeddings), sparse retrieval (BM25), and citation graph retrieval
Uses Reciprocal Rank Fusion (RRF) to combine results
"""

from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING
import logging
import asyncio
from dataclasses import dataclass

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from citation_graph import CitationGraph

# Optional dependencies
try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False
    logger.warning("rank-bm25 not available. Install with: pip install rank-bm25")

try:
    from citation_graph import CitationGraph, build_citation_graph_from_papers
    CITATION_GRAPH_AVAILABLE = True
except ImportError:
    CITATION_GRAPH_AVAILABLE = False
    logger.warning("Citation graph module not available")


@dataclass
class RetrievalResult:
    """Result from a retrieval method"""
    paper_id: str
    score: float
    method: str  # 'dense', 'sparse', 'citation'


class HybridRetriever:
    """
    Hybrid retrieval system combining multiple retrieval methods
    """
    
    def __init__(
        self,
        embedding_client=None,
        citation_graph: Optional["CitationGraph"] = None
    ):
        self.embedding_client = embedding_client
        self.citation_graph = citation_graph
        self.bm25_index = None
        self.paper_texts = []
        self.paper_ids = []
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization for BM25"""
        import re
        # Remove punctuation and split
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        return text.split()
    
    def build_bm25_index(self, papers: List[Any]):
        """
        Build BM25 index from paper abstracts
        
        Args:
            papers: List of Paper objects with abstracts
        """
        if not BM25_AVAILABLE:
            logger.warning("BM25 not available, skipping sparse retrieval")
            return
        
        self.paper_texts = []
        self.paper_ids = []
        
        for paper in papers:
            # Combine title and abstract for indexing
            text = f"{paper.title} {paper.abstract}"
            tokenized = self._tokenize(text)
            if tokenized:  # Only add if tokenized text is not empty
                self.paper_texts.append(tokenized)
                self.paper_ids.append(paper.id)
        
        if self.paper_texts:
            self.bm25_index = BM25Okapi(self.paper_texts)
            logger.info(f"Built BM25 index with {len(self.paper_texts)} papers")
    
    async def dense_retrieval(
        self,
        query: str,
        papers: List[Any],
        top_k: int = 50
    ) -> List[RetrievalResult]:
        """
        Dense retrieval using embeddings (existing method)
        
        Args:
            query: Search query
            papers: List of Paper objects
            top_k: Number of results to return
            
        Returns:
            List of RetrievalResult objects sorted by score
        """
        if not self.embedding_client:
            return []
        
        # Embed query
        query_embedding = await self.embedding_client.embed(
            query,
            input_type="query"
        )
        
        # Calculate similarities
        results = []
        for paper in papers:
            if hasattr(paper, 'embedding') and paper.embedding:
                similarity = self.embedding_client.cosine_similarity(
                    query_embedding,
                    paper.embedding
                )
                results.append(RetrievalResult(
                    paper_id=paper.id,
                    score=similarity,
                    method='dense'
                ))
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def sparse_retrieval(
        self,
        query: str,
        top_k: int = 50
    ) -> List[RetrievalResult]:
        """
        Sparse retrieval using BM25
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of RetrievalResult objects sorted by score
        """
        if not BM25_AVAILABLE or not self.bm25_index:
            return []
        
        # Tokenize query
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
        
        # Get BM25 scores
        scores = self.bm25_index.get_scores(query_tokens)
        
        # Create results
        results = []
        for i, score in enumerate(scores):
            if i < len(self.paper_ids):
                results.append(RetrievalResult(
                    paper_id=self.paper_ids[i],
                    score=float(score),
                    method='sparse'
                ))
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def citation_retrieval(
        self,
        query: str,
        papers: List[Any],
        top_k: int = 50
    ) -> List[RetrievalResult]:
        """
        Citation graph retrieval - find papers connected to query-relevant papers
        
        Args:
            query: Search query (used for initial filtering)
            papers: List of Paper objects
            top_k: Number of results to return
            
        Returns:
            List of RetrievalResult objects from citation graph
        """
        if not CITATION_GRAPH_AVAILABLE or not self.citation_graph:
            return []
        
        # Find papers that are highly cited or connected to query-relevant papers
        results = []
        
        # Get influential papers (highly cited)
        influential = self.citation_graph.get_influential_papers(top_n=top_k)
        for i, paper in enumerate(influential):
            # Score based on citation count and position
            score = len(paper.cited_by_ids) / 100.0  # Normalize
            results.append(RetrievalResult(
                paper_id=paper.paper_id,
                score=score,
                method='citation'
            ))
        
        # Also get papers connected to query-relevant papers
        # (This is a simplified version - could be enhanced)
        paper_ids_set = {p.id for p in papers}
        for paper_id, node in self.citation_graph.nodes.items():
            if paper_id not in paper_ids_set:
                # Check if this paper cites or is cited by query-relevant papers
                connected = False
                for relevant_id in paper_ids_set:
                    if relevant_id in node.citation_ids or relevant_id in node.cited_by_ids:
                        connected = True
                        break
                
                if connected:
                    score = len(node.cited_by_ids) / 100.0
                    results.append(RetrievalResult(
                        paper_id=paper_id,
                        score=score,
                        method='citation'
                    ))
        
        # Sort and return top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def reciprocal_rank_fusion(
        self,
        result_lists: List[List[RetrievalResult]],
        k: int = 60
    ) -> List[Tuple[str, float]]:
        """
        Reciprocal Rank Fusion (RRF) to combine multiple ranked lists
        
        Args:
            result_lists: List of ranked result lists from different methods
            k: RRF constant (typically 60)
            
        Returns:
            List of (paper_id, final_score) tuples sorted by score
        """
        # Build score dictionary
        scores = {}
        
        for result_list in result_lists:
            for rank, result in enumerate(result_list, start=1):
                paper_id = result.paper_id
                rrf_score = 1.0 / (k + rank)
                
                if paper_id not in scores:
                    scores[paper_id] = 0.0
                scores[paper_id] += rrf_score
        
        # Sort by score
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results
    
    async def retrieve(
        self,
        query: str,
        papers: List[Any],
        top_k: int = 50,
        use_dense: bool = True,
        use_sparse: bool = True,
        use_citation: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Hybrid retrieval combining all methods with RRF
        
        Args:
            query: Search query
            papers: List of Paper objects
            top_k: Number of results to return
            use_dense: Enable dense retrieval
            use_sparse: Enable sparse retrieval
            use_citation: Enable citation retrieval
            
        Returns:
            List of (paper_id, final_score) tuples sorted by score
        """
        result_lists = []
        
        # Dense retrieval (embeddings)
        if use_dense:
            dense_results = await self.dense_retrieval(query, papers, top_k=top_k)
            if dense_results:
                result_lists.append(dense_results)
                logger.info(f"Dense retrieval: {len(dense_results)} results")
        
        # Sparse retrieval (BM25)
        if use_sparse:
            # Build BM25 index if not already built
            if not self.bm25_index:
                self.build_bm25_index(papers)
            
            sparse_results = self.sparse_retrieval(query, top_k=top_k)
            if sparse_results:
                result_lists.append(sparse_results)
                logger.info(f"Sparse retrieval: {len(sparse_results)} results")
        
        # Citation graph retrieval
        if use_citation and self.citation_graph:
            citation_results = self.citation_retrieval(query, papers, top_k=top_k)
            if citation_results:
                result_lists.append(citation_results)
                logger.info(f"Citation retrieval: {len(citation_results)} results")
        
        # Combine using RRF
        if len(result_lists) == 0:
            logger.warning("No retrieval methods produced results")
            return []
        
        if len(result_lists) == 1:
            # Single method, just return its results
            return [(r.paper_id, r.score) for r in result_lists[0][:top_k]]
        
        # Multiple methods, use RRF
        fused_results = self.reciprocal_rank_fusion(result_lists, k=60)
        logger.info(f"RRF fusion: {len(fused_results)} combined results")
        
        return fused_results[:top_k]


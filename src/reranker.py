"""
Cross-Encoder Reranking System
Reranks retrieved papers using more accurate cross-encoder models
"""

from typing import List, Dict, Any, Optional, Tuple
import logging
import asyncio

logger = logging.getLogger(__name__)

# Optional dependencies
try:
    from sentence_transformers import CrossEncoder
    CROSS_ENCODER_AVAILABLE = True
except ImportError:
    CROSS_ENCODER_AVAILABLE = False
    logger.warning("sentence-transformers not available. Install with: pip install sentence-transformers")


class Reranker:
    """
    Cross-encoder reranker for improved relevance scoring
    """
    
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        device: Optional[str] = None
    ):
        """
        Initialize reranker
        
        Args:
            model_name: Cross-encoder model to use
            device: Device to run on ('cpu', 'cuda', 'mps', or None for auto)
        """
        self.model = None
        self.model_name = model_name
        self.device = device
        
        if CROSS_ENCODER_AVAILABLE:
            try:
                self.model = CrossEncoder(model_name, device=device)
                logger.info(f"Initialized reranker with model: {model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize reranker: {e}")
                self.model = None
        else:
            logger.warning("Cross-encoder not available, reranking will be skipped")
    
    def rerank(
        self,
        query: str,
        papers: List[Any],
        top_k: Optional[int] = None
    ) -> List[Tuple[Any, float]]:
        """
        Rerank papers using cross-encoder
        
        Args:
            query: Search query
            papers: List of Paper objects to rerank
            top_k: Number of top results to return (None = return all)
            
        Returns:
            List of (paper, score) tuples sorted by score (descending)
        """
        if not self.model or not papers:
            # Return papers with dummy scores if reranking unavailable
            return [(paper, 0.5) for paper in papers]
        
        # Create query-paper pairs
        pairs = []
        for paper in papers:
            # Combine title and abstract for reranking
            text = f"{paper.title} {paper.abstract}"
            pairs.append((query, text))
        
        try:
            # Get scores from cross-encoder
            scores = self.model.predict(pairs, show_progress_bar=False)
            
            # Combine papers with scores
            paper_scores = list(zip(papers, scores))
            
            # Sort by score (descending)
            paper_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Return top_k if specified
            if top_k is not None:
                return paper_scores[:top_k]
            
            return paper_scores
            
        except Exception as e:
            logger.error(f"Reranking error: {e}")
            # Fallback: return papers with dummy scores
            return [(paper, 0.5) for paper in papers]
    
    async def rerank_async(
        self,
        query: str,
        papers: List[Any],
        top_k: Optional[int] = None,
        batch_size: int = 32
    ) -> List[Tuple[Any, float]]:
        """
        Async version of rerank (processes in batches)
        
        Args:
            query: Search query
            papers: List of Paper objects to rerank
            top_k: Number of top results to return
            batch_size: Number of papers to process per batch
            
        Returns:
            List of (paper, score) tuples sorted by score (descending)
        """
        if not self.model or not papers:
            return [(paper, 0.5) for paper in papers]
        
        # Process in batches using thread pool executor to avoid blocking event loop
        import asyncio
        from functools import partial
        
        loop = asyncio.get_running_loop()
        all_results = []
        
        for i in range(0, len(papers), batch_size):
            batch = papers[i:i + batch_size]
            # Run blocking rerank in thread pool
            batch_results = await loop.run_in_executor(
                None,
                partial(self.rerank, query=query, papers=batch, top_k=None)
            )
            all_results.extend(batch_results)
        
        # Sort all results by score
        all_results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k if specified
        if top_k is not None:
            return all_results[:top_k]
        
        return all_results


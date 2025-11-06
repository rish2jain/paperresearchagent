"""
Query Expansion Module
Intelligently expands search queries using embeddings to find related terms
"""

from typing import List, Dict, Any
import logging
# Import with fallback for different execution contexts
try:
    from .nim_clients import EmbeddingNIMClient
except ImportError:
    # Fallback for direct script execution
    from nim_clients import EmbeddingNIMClient

logger = logging.getLogger(__name__)


class QueryExpander:
    """
    Expands research queries using semantic similarity
    Uses Embedding NIM to find related terms and concepts
    """
    
    def __init__(self, embedding_client: EmbeddingNIMClient):
        self.embedding_client = embedding_client
    
    async def expand_query(
        self,
        query: str,
        max_expansions: int = 3
    ) -> List[str]:
        """
        Generate expanded query variations
        
        Args:
            query: Original research query
            max_expansions: Maximum number of expansion terms to generate
        
        Returns:
            List of expanded query variations
        """
        logger.info(f"Expanding query: '{query}'")
        
        # Embed the original query
        query_embedding = await self.embedding_client.embed(
            query,
            input_type="query"
        )
        
        # Generate potential expansion terms based on common research patterns
        expansion_candidates = self._generate_expansion_candidates(query)
        
        if not expansion_candidates:
            return [query]  # Return original if no expansions
        
        # Embed all candidates
        candidate_embeddings = await self.embedding_client.embed_batch(
            expansion_candidates,
            input_type="query"
        )
        
        # Calculate similarity scores
        similarities = []
        for candidate, candidate_embedding in zip(expansion_candidates, candidate_embeddings):
            similarity = self.embedding_client.cosine_similarity(
                query_embedding,
                candidate_embedding
            )
            similarities.append((candidate, similarity))
        
        # Sort by similarity and take top expansions
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Select top similar expansions (threshold > 0.6)
        expanded_queries = [query]  # Always include original
        for candidate, similarity in similarities[:max_expansions * 2]:
            if similarity > 0.6 and candidate not in expanded_queries:
                expanded_queries.append(candidate)
                if len(expanded_queries) >= max_expansions + 1:  # +1 for original
                    break
        
        logger.info(f"Generated {len(expanded_queries)} query variations")
        return expanded_queries
    
    def _generate_expansion_candidates(self, query: str) -> List[str]:
        """
        Generate candidate terms for query expansion
        Uses linguistic patterns and domain knowledge
        """
        candidates = []
        query_lower = query.lower()
        
        # Method-based expansions
        method_keywords = {
            'learning': ['deep learning', 'machine learning', 'reinforcement learning'],
            'analysis': ['statistical analysis', 'data analysis', 'computational analysis'],
            'prediction': ['forecasting', 'prognosis', 'estimation'],
            'detection': ['identification', 'classification', 'recognition'],
            'optimization': ['improvement', 'enhancement', 'refinement']
        }
        
        for keyword, alternatives in method_keywords.items():
            if keyword in query_lower:
                for alt in alternatives:
                    expanded = query_lower.replace(keyword, alt)
                    if expanded != query_lower:
                        candidates.append(expanded)
        
        # Domain expansions
        domain_patterns = {
            'medical': ['clinical', 'healthcare', 'biomedical'],
            'image': ['imaging', 'vision', 'visual'],
            'text': ['natural language', 'nlp', 'language processing'],
            'data': ['dataset', 'database', 'information']
        }
        
        for pattern, alternatives in domain_patterns.items():
            if pattern in query_lower:
                for alt in alternatives:
                    expanded = query_lower.replace(pattern, alt)
                    if expanded != query_lower:
                        candidates.append(expanded)
        
        # Add synonyms using AND/OR combinations
        if 'and' in query_lower:
            # Try OR variation
            or_query = query_lower.replace(' and ', ' or ')
            candidates.append(or_query)
        
        # Add "applications" variant
        if 'application' not in query_lower and 'use' not in query_lower:
            candidates.append(f"{query} applications")
        
        # Add "recent advances" variant
        candidates.append(f"recent advances in {query}")
        
        # Add "systematic review" variant for comprehensive search
        candidates.append(f"systematic review of {query}")
        
        return list(set(candidates))  # Remove duplicates


async def expand_search_queries(
    query: str,
    embedding_client: EmbeddingNIMClient,
    max_expansions: int = 3
) -> List[str]:
    """
    Convenience function to expand queries
    
    Args:
        query: Original research query
        embedding_client: Embedding NIM client
        max_expansions: Maximum expansion terms
    
    Returns:
        List of query variations including original
    """
    expander = QueryExpander(embedding_client)
    return await expander.expand_query(query, max_expansions)


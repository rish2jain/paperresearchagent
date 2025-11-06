"""
Local Embedding Model using Sentence Transformers
Replaces NVIDIA Embedding NIM for local execution
"""

import os
import logging
from typing import List, Optional
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    import torch
    SENTENCE_TRANSFORMERS_AVAILABLE = True
    
    # Check for MPS (Metal Performance Shaders) support
    MPS_AVAILABLE = torch.backends.mps.is_available() if hasattr(torch.backends, 'mps') else False
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    MPS_AVAILABLE = False
    logger.warning("sentence-transformers not installed. Install with: pip install sentence-transformers")


class LocalEmbeddingModel:
    """
    Local embedding model using Sentence Transformers
    Compatible with EmbeddingNIMClient interface
    """
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        cache_folder: Optional[str] = None,
        device: Optional[str] = None
    ):
        """
        Initialize local embedding model
        
        Args:
            model_name: HuggingFace model name or path
            cache_folder: Cache directory for models
            device: Device to use ('mps', 'cpu', or None for auto)
        """
        self.model_name = model_name
        self.cache_folder = cache_folder
        self.model = None
        self.device = device or self._detect_device()
        self._initialize_model()
        
        # Cache for embeddings (in-memory)
        self.embedding_cache: dict = {}
    
    def _detect_device(self) -> str:
        """Detect best available device"""
        if MPS_AVAILABLE:
            logger.info("Using Metal Performance Shaders (MPS) for GPU acceleration")
            return "mps"
        elif "torch" in globals() and hasattr(torch, "cuda") and torch.cuda.is_available():
            logger.info("Using CUDA for GPU acceleration")
            return "cuda"
        else:
            logger.info("Using CPU (no GPU acceleration available)")
            return "cpu"
    
    def _initialize_model(self):
        """Initialize the embedding model"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise RuntimeError(
                "sentence-transformers not installed. Install with:\n"
                "  pip install sentence-transformers"
            )
        
        logger.info(f"Loading embedding model: {self.model_name}")
        
        try:
            self.model = SentenceTransformer(
                self.model_name,
                cache_folder=self.cache_folder,
                device=self.device
            )
            
            # Get embedding dimension
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            
            logger.info(
                f"✅ Local embedding model loaded successfully "
                f"(dim={self.embedding_dim}, device={self.device})"
            )
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    async def embed(
        self,
        text: str,
        input_type: str = "query",
        cache: bool = True
    ) -> List[float]:
        """
        Generate embedding matching NIM API interface
        
        Args:
            text: Input text to embed
            input_type: "query" or "passage" (for future use)
            cache: Whether to cache embeddings
        
        Returns:
            Embedding vector (list of floats)
        """
        # Check cache first
        cache_key = f"{input_type}:{text[:100]}"
        if cache and cache_key in self.embedding_cache:
            logger.debug(f"Embedding cache hit: {text[:50]}...")
            return self.embedding_cache[cache_key]
        
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        embedding = await loop.run_in_executor(
            None,
            self._embed_sync,
            text
        )
        
        # Cache result
        if cache:
            self.embedding_cache[cache_key] = embedding
        
        return embedding
    
    def _embed_sync(self, text: str) -> List[float]:
        """Synchronous embedding generation"""
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        # Generate embedding
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalize for cosine similarity
        )
        
        return embedding.tolist()
    
    async def embed_batch(
        self,
        texts: List[str],
        input_type: str = "passage",
        batch_size: int = 32,
        cache: Optional[bool] = None
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            input_type: "query" or "passage"
            batch_size: Batch size for processing
            cache: Whether to cache embeddings (for interface compatibility)
        
        Returns:
            List of embedding vectors
        """
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None,
            self._embed_batch_sync,
            texts,
            batch_size
        )
        
        return embeddings
    
    def _embed_batch_sync(self, texts: List[str], batch_size: int) -> List[List[float]]:
        """Synchronous batch embedding generation"""
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """Get embedding dimension"""
        return self.embedding_dim
    
    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        Returns standard cosine similarity in the range [-1, 1]
        
        Args:
            vec1: First embedding vector
            vec2: Second embedding vector
        
        Returns:
            Similarity score (-1.0 to 1.0)
        """
        import numpy as np
        
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        # Handle empty vectors - return 0 similarity
        if v1.size == 0 or v2.size == 0:
            logger.warning(f"Empty vector in cosine similarity: v1.size={v1.size}, v2.size={v2.size}")
            return 0.0
        
        # Handle zero vectors - return 0 similarity
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            logger.warning(f"Zero-norm vector in cosine similarity: norm1={norm1}, norm2={norm2}")
            return 0.0
        
        dot_product = np.dot(v1, v2)
        similarity = dot_product / (norm1 * norm2)
        
        return float(similarity)
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        # Clear cache if needed
        self.embedding_cache.clear()


"""
Unified Client Wrappers
Supports both local models and cloud NIMs based on configuration
"""

import os
import logging
from typing import Optional

from config import Config, get_config

logger = logging.getLogger(__name__)

# Try to import local models
try:
    from local_models import LocalReasoningModel, LocalEmbeddingModel
    LOCAL_MODELS_AVAILABLE = True
except ImportError:
    LOCAL_MODELS_AVAILABLE = False
    logger.warning("Local models not available. Install dependencies for local mode.")

# Import NIM clients
from nim_clients import ReasoningNIMClient, EmbeddingNIMClient


class UnifiedReasoningClient:
    """
    Unified reasoning client that uses local models or cloud NIMs
    based on configuration
    """
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or get_config()
        
        if self.config.local_models.use_local_models:
            if not LOCAL_MODELS_AVAILABLE:
                raise RuntimeError(
                    "Local models requested but not available. "
                    "Install with: pip install llama-cpp-python[metal] sentence-transformers"
                )
            
            logger.info("Using local reasoning model")
            self.client = LocalReasoningModel(
                model_path=self.config.local_models.reasoning_model_path,
                n_ctx=self.config.local_models.reasoning_model_n_ctx,
                n_gpu_layers=self.config.local_models.reasoning_model_n_gpu_layers,
                use_mlx=self.config.local_models.reasoning_use_mlx
            )
            self.is_local = True
        else:
            logger.info("Using cloud reasoning NIM")
            self.client = ReasoningNIMClient(
                base_url=self.config.nim.reasoning_nim_url
            )
            self.is_local = False
    
    async def complete(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False
    ) -> str:
        """Generate completion (local or cloud)"""
        return await self.client.complete(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream
        )
    
    async def chat(
        self,
        messages: list,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """Chat completion (local or cloud)"""
        return await self.client.chat(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    async def __aenter__(self):
        """Async context manager entry"""
        return await self.client.__aenter__()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        return await self.client.__aexit__(exc_type, exc_val, exc_tb)


class UnifiedEmbeddingClient:
    """
    Unified embedding client that uses local models or cloud NIMs
    based on configuration
    """
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or get_config()
        
        if self.config.local_models.use_local_models:
            if not LOCAL_MODELS_AVAILABLE:
                raise RuntimeError(
                    "Local models requested but not available. "
                    "Install with: pip install sentence-transformers"
                )
            
            logger.info("Using local embedding model")
            self.client = LocalEmbeddingModel(
                model_name=self.config.local_models.embedding_model_name,
                cache_folder=self.config.local_models.embedding_cache_folder,
                device=self.config.local_models.embedding_device
            )
            self.is_local = True
        else:
            logger.info("Using cloud embedding NIM")
            self.client = EmbeddingNIMClient(
                base_url=self.config.nim.embedding_nim_url
            )
            self.is_local = False
    
    async def embed(
        self,
        text: str,
        input_type: str = "query",
        cache: bool = True
    ) -> list:
        """Generate embedding (local or cloud)"""
        return await self.client.embed(
            text=text,
            input_type=input_type,
            cache=cache
        )
    
    async def embed_batch(
        self,
        texts: list,
        input_type: str = "passage",
        batch_size: int = 32,
        cache: Optional[bool] = None
    ) -> list:
        """Generate batch embeddings (local or cloud)"""
        if self.is_local:
            return await self.client.embed_batch(
                texts=texts,
                input_type=input_type,
                batch_size=batch_size,
                cache=cache
            )
        else:
            # Fallback to individual embeddings for cloud
            results = []
            for text in texts:
                embedding = await self.embed(text, input_type, cache)
                results.append(embedding)
            return results
    
    async def __aenter__(self):
        """Async context manager entry"""
        return await self.client.__aenter__()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        return await self.client.__aexit__(exc_type, exc_val, exc_tb)


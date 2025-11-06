"""
NVIDIA NIM Client Wrappers
Handles API calls to Reasoning NIM and Embedding NIM
"""

import os
import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import time
# Import constants with fallback for different execution contexts
try:
    from .constants import (
        NIM_CONNECT_TIMEOUT_SECONDS,
        NIM_SOCK_READ_TIMEOUT_SECONDS,
        DEFAULT_TIMEOUT_SECONDS
    )
except ImportError:
    # Fallback for direct script execution
    from constants import (
        NIM_CONNECT_TIMEOUT_SECONDS,
        NIM_SOCK_READ_TIMEOUT_SECONDS,
        DEFAULT_TIMEOUT_SECONDS
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Circuit breaker support
try:
    from circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitBreakerOpenError
    CIRCUIT_BREAKER_AVAILABLE = True
except ImportError:
    try:
        from .circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitBreakerOpenError
        CIRCUIT_BREAKER_AVAILABLE = True
    except ImportError:
        CIRCUIT_BREAKER_AVAILABLE = False
        CircuitBreakerOpenError = Exception  # Fallback exception type

# Optional imports for metrics and caching
try:
    from .metrics import get_metrics_collector
    METRICS_AVAILABLE = True
except ImportError:
    try:
        from metrics import get_metrics_collector
        METRICS_AVAILABLE = True
    except ImportError:
        METRICS_AVAILABLE = False

try:
    from .cache import get_cache, EmbeddingCache
    CACHE_AVAILABLE = True
except ImportError:
    try:
        from cache import get_cache, EmbeddingCache
        CACHE_AVAILABLE = True
    except ImportError:
        CACHE_AVAILABLE = False


class ReasoningNIMClient:
    """
    Client for llama-3.1-nemotron-nano-8B-v1 Reasoning NIM
    Handles text generation and reasoning tasks
    """

    DEFAULT_TIMEOUT = aiohttp.ClientTimeout(
        total=DEFAULT_TIMEOUT_SECONDS,         # Total timeout for entire request
        connect=NIM_CONNECT_TIMEOUT_SECONDS,   # Timeout for connection establishment
        sock_read=NIM_SOCK_READ_TIMEOUT_SECONDS  # Timeout for reading response (now 60s)
    )

    def __init__(self, base_url: str = None, timeout: Optional[aiohttp.ClientTimeout] = None):
        self.base_url = base_url or os.getenv(
            "REASONING_NIM_URL",
            "http://reasoning-nim.research-ops.svc.cluster.local:8000"
        )
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Initialize circuit breaker
        if CIRCUIT_BREAKER_AVAILABLE:
            circuit_config = CircuitBreakerConfig(
                fail_max=int(os.getenv("CIRCUIT_BREAKER_FAIL_MAX", "5")),
                timeout_duration=int(os.getenv("CIRCUIT_BREAKER_TIMEOUT", "60")),
                success_threshold=2
            )
            self.circuit_breaker = CircuitBreaker("reasoning_nim", circuit_config)
        else:
            self.circuit_breaker = None
        
        # Initialize metrics
        if METRICS_AVAILABLE:
            try:
                self.metrics = get_metrics_collector()
            except Exception as e:
                logger.warning(f"Metrics initialization failed: {e}")
                self.metrics = None
        else:
            self.metrics = None

    async def __aenter__(self):
        """Async context manager entry - create session if needed"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - close session"""
        if self.session and not self.session.closed:
            await self.session.close()
            # Wait for underlying connections to close
            await asyncio.sleep(0.250)

    async def _complete_impl(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False
    ) -> str:
        """Internal implementation with retry logic"""
        if not self.session or self.session.closed:
            raise RuntimeError("NIM client session not initialized. Use async context manager.")
        
        url = f"{self.base_url}/v1/completions"

        payload = {
            "model": "nvidia/llama-3.1-nemotron-nano-8b-v1",
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }

        async with self.session.post(url, json=payload) as response:
            # Validate response status
            if response.status != 200:
                error_text = await response.text()
                raise ValueError(
                    f"Reasoning NIM returned status {response.status}: {error_text}"
                )
            
            result = await response.json()

            # Validate response structure
            if "choices" not in result or not result["choices"]:
                raise ValueError(f"Invalid NIM response structure: {result}")

            # Extract completion text
            completion = result["choices"][0]["text"]

            logger.info(f"Reasoning completion: {len(completion)} chars (prompt: {len(prompt)} chars)")
            return completion

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def complete(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False
    ) -> str:
        """
        Generate completion using reasoning model with automatic retry and circuit breaker

        Args:
            prompt: Input text prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter
            stream: Whether to stream response

        Returns:
            Generated text completion

        Raises:
            aiohttp.ClientError: Network errors (will retry automatically)
            asyncio.TimeoutError: Timeout errors (will retry automatically)
            ValueError: Invalid response structure (will not retry)
            CircuitBreakerOpenError: If circuit breaker is open
        """
        # Use circuit breaker if available
        if self.circuit_breaker:
            try:
                return await self.circuit_breaker.call(
                    self._complete_impl,
                    prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    stream=stream
                )
            except CircuitBreakerOpenError:
                logger.error(f"Circuit breaker OPEN for reasoning NIM - service unavailable")
                raise
        else:
            # Fallback without circuit breaker
            try:
                return await self._complete_impl(
                    prompt, max_tokens, temperature, top_p, stream
                )
            except aiohttp.ClientError as e:
                logger.error(f"Reasoning NIM network error: {e}")
                raise
            except asyncio.TimeoutError as e:
                logger.error(f"Reasoning NIM timeout after {self.timeout.total}s: {e}")
                raise
            except ValueError as e:
                logger.error(f"Reasoning NIM validation error: {e}")
                raise
            except Exception as e:
                logger.error(f"Reasoning NIM unexpected error: {e}")
                raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """
        Chat-style interaction with reasoning model with automatic retry

        Args:
            messages: List of {"role": "user/assistant", "content": "text"}
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Assistant's response
        """
        if not self.session or self.session.closed:
            raise RuntimeError("NIM client session not initialized. Use async context manager.")
        
        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": "nvidia/llama-3.1-nemotron-nano-8b-v1",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            async with self.session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(
                        f"Reasoning NIM chat returned status {response.status}: {error_text}"
                    )
                
                result = await response.json()

                if "choices" not in result or not result["choices"]:
                    raise ValueError(f"Invalid NIM chat response structure: {result}")

                # Extract message content
                content = result["choices"][0]["message"]["content"]

                logger.info(f"Chat response: {len(content)} chars")
                return content

        except aiohttp.ClientError as e:
            logger.error(f"Reasoning NIM chat network error: {e}")
            raise
        except asyncio.TimeoutError as e:
            logger.error(f"Reasoning NIM chat timeout: {e}")
            raise
        except ValueError as e:
            logger.error(f"Reasoning NIM chat validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Reasoning NIM chat unexpected error: {e}")
            raise

    async def extract_structured(
        self,
        text: str,
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract structured information using reasoning model

        Args:
            text: Input text to analyze
            schema: Expected output structure

        Returns:
            Extracted structured data
        """
        prompt = f"""
Extract the following information from the text and return as JSON.

Schema:
{schema}

Text:
{text}

JSON Output:
"""

        response = await self.complete(
            prompt=prompt,
            temperature=0.3,  # Lower for more deterministic extraction
            max_tokens=1024
        )

        # Parse JSON from response - extract first complete JSON object only
        import json
        try:
            # Find start of JSON
            start_idx = response.find('{')
            if start_idx == -1:
                logger.error("No JSON object found in response")
                return {}

            # Use JSONDecoder to parse just the first complete JSON object
            # This handles cases where there's trailing text or multiple objects
            decoder = json.JSONDecoder()
            obj, end_idx = decoder.raw_decode(response, start_idx)
            return obj
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse structured output: {e}")
            logger.debug(f"Response snippet: {response[:500]}...")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error parsing structured output: {e}")
            return {}


class EmbeddingNIMClient:
    """
    Client for Retrieval Embedding NIM (nv-embedqa-e5-v5)
    Handles text embedding and similarity operations
    """

    DEFAULT_TIMEOUT = aiohttp.ClientTimeout(
        total=DEFAULT_TIMEOUT_SECONDS,
        connect=NIM_CONNECT_TIMEOUT_SECONDS,
        sock_read=NIM_SOCK_READ_TIMEOUT_SECONDS
    )

    def __init__(self, base_url: str = None, timeout: Optional[aiohttp.ClientTimeout] = None):
        self.base_url = base_url or os.getenv(
            "EMBEDDING_NIM_URL",
            "http://embedding-nim.research-ops.svc.cluster.local:8001"
        )
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.session: Optional[aiohttp.ClientSession] = None
        self.embedding_cache: Dict[str, List[float]] = {}  # In-memory fallback
        
        # Initialize metrics and cache
        if METRICS_AVAILABLE:
            try:
                self.metrics = get_metrics_collector()
            except Exception as e:
                logger.warning(f"Metrics initialization failed: {e}")
                self.metrics = None
        else:
            self.metrics = None
        
        if CACHE_AVAILABLE:
            try:
                cache = get_cache()
                self.embedding_cache_obj = EmbeddingCache(cache)
            except Exception as e:
                logger.warning(f"Cache initialization failed: {e}")
                self.embedding_cache_obj = None
        else:
            self.embedding_cache_obj = None

    async def __aenter__(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session and not self.session.closed:
            await self.session.close()
            await asyncio.sleep(0.250)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def embed(
        self,
        text: str,
        input_type: str = "query",  # "query" or "passage"
        cache: bool = True
    ) -> List[float]:
        """
        Generate embedding for single text with automatic retry

        Args:
            text: Input text to embed
            input_type: "query" for search queries, "passage" for documents
            cache: Whether to cache embeddings

        Returns:
            Embedding vector (list of floats)
        """
        # Check advanced cache first
        if cache and self.embedding_cache_obj:
            cached_embedding = self.embedding_cache_obj.get_embedding(text, input_type)
            if cached_embedding is not None:
                if self.metrics:
                    self.metrics.record_cache_hit("embedding")
                logger.debug(f"Embedding cache hit: {text[:50]}...")
                return cached_embedding
        
        if self.metrics and cache:
            self.metrics.record_cache_miss("embedding")
        
        # Fallback to in-memory cache
        cache_key = f"{input_type}:{text[:100]}"
        if cache and cache_key in self.embedding_cache:
            logger.info("Using in-memory cached embedding")
            return self.embedding_cache[cache_key]

        if not self.session or self.session.closed:
            raise RuntimeError("NIM client session not initialized. Use async context manager.")
        
        url = f"{self.base_url}/v1/embeddings"

        payload = {
            "model": "nvidia/nv-embedqa-e5-v5",
            "input": text,
            "input_type": input_type,
            "encoding_format": "float"
        }

        start_time = time.time()
        try:
            async with self.session.post(url, json=payload) as response:
                duration = time.time() - start_time
                
                if response.status != 200:
                    error_text = await response.text()
                    if self.metrics:
                        self.metrics.record_nim_request("embedding", "embed", "error", duration)
                    raise ValueError(
                        f"Embedding NIM returned status {response.status}: {error_text}"
                    )
                
                result = await response.json()

                if "data" not in result or not result["data"]:
                    if self.metrics:
                        self.metrics.record_nim_request("embedding", "embed", "error", duration)
                    raise ValueError(f"Invalid embedding NIM response structure: {result}")

                # Extract embedding vector
                embedding = result["data"][0]["embedding"]
                
                if self.metrics:
                    self.metrics.record_nim_request("embedding", "embed", "success", duration)

                # Cache if enabled (both advanced and in-memory)
                if cache:
                    if self.embedding_cache_obj:
                        self.embedding_cache_obj.set_embedding(text, embedding, input_type)
                    # Also keep in-memory for backwards compatibility
                    self.embedding_cache[cache_key] = embedding

                logger.info(f"Generated embedding: dim={len(embedding)}")
                return embedding

        except aiohttp.ClientError as e:
            logger.error(f"Embedding NIM network error for {url}: {e}")
            raise
        except asyncio.TimeoutError as e:
            logger.error(f"Embedding NIM timeout: {e}")
            raise
        except ValueError as e:
            logger.error(f"Embedding NIM validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Embedding NIM unexpected error: {e}")
            raise

    async def embed_batch(
        self,
        texts: List[str],
        input_type: str = "passage",
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batched for efficiency)

        Args:
            texts: List of texts to embed
            input_type: "query" or "passage"
            batch_size: Number of texts per API call

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        # Filter out None and empty strings before processing
        # Store original indices to map results back correctly
        # Also truncate texts to stay within NIM's 512 token limit
        # Using ~1800 chars as approximation for 450 tokens (safe margin)
        MAX_CHARS = 1800

        valid_texts = []
        valid_indices = []
        for idx, text in enumerate(texts):
            if text and isinstance(text, str) and text.strip():
                stripped = text.strip()
                # Truncate if too long
                if len(stripped) > MAX_CHARS:
                    logger.debug(f"Truncating text from {len(stripped)} to {MAX_CHARS} chars")
                    stripped = stripped[:MAX_CHARS]
                valid_texts.append(stripped)
                valid_indices.append(idx)

        if not valid_texts:
            logger.warning("No valid texts to embed in batch")
            return [[] for _ in texts]  # Return empty embeddings for all inputs
        
        # Process in batches
        for i in range(0, len(valid_texts), batch_size):
            batch = valid_texts[i:i + batch_size]

            url = f"{self.base_url}/v1/embeddings"

            payload = {
                "model": "nvidia/nv-embedqa-e5-v5",
                "input": batch,
                "input_type": input_type,
                "encoding_format": "float"
            }

            try:
                if not self.session or self.session.closed:
                    raise RuntimeError("NIM client session not initialized")
                
                async with self.session.post(url, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise ValueError(
                            f"Embedding NIM batch returned status {response.status}: {error_text}"
                        )
                    
                    result = await response.json()

                    if "data" not in result or not result["data"]:
                        raise ValueError(f"Invalid embedding NIM batch response: {result}")

                    # Extract all embeddings from batch
                    batch_embeddings = [
                        item["embedding"] for item in result["data"]
                    ]
                    all_embeddings.extend(batch_embeddings)

                    logger.info(f"Embedded batch {i//batch_size + 1}: {len(batch)} texts")

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.error(f"Batch embedding network error: {e}")
                # Retry this batch
                raise
            except ValueError as e:
                logger.error(f"Batch embedding validation error: {e}")
                raise
            except Exception as e:
                logger.error(f"Batch embedding unexpected error: {e}")
                raise
        
        # Map results back to original positions (with None/empty strings getting empty embeddings)
        result_embeddings = [[] for _ in range(len(texts))]
        for valid_idx, embedding in zip(valid_indices, all_embeddings):
            result_embeddings[valid_idx] = embedding
        
        return result_embeddings

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors

        Args:
            vec1: First embedding vector
            vec2: Second embedding vector

        Returns:
            Similarity score (0.0 to 1.0)
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

        # Normalize to 0-1 range
        return float((similarity + 1) / 2)


# Example usage
async def example_usage():
    """Demonstrate NIM client usage"""

    # Initialize clients
    async with ReasoningNIMClient() as reasoning, \
                EmbeddingNIMClient() as embedding:

        # Example 1: Simple reasoning
        print("=== Example 1: Reasoning ===")
        result = await reasoning.complete(
            "Explain quantum entanglement in simple terms:"
        )
        print(f"Reasoning output: {result[:200]}...")

        # Example 2: Structured extraction
        print("\n=== Example 2: Structured Extraction ===")
        paper_text = """
        Title: Deep Learning for Computer Vision
        Authors: John Smith, Jane Doe
        Abstract: This paper presents a novel approach...
        Methodology: We used convolutional neural networks...
        Results: Achieved 95% accuracy on ImageNet...
        """

        schema = {
            "title": "string",
            "authors": "list of strings",
            "methodology": "string",
            "accuracy": "number"
        }

        structured = await reasoning.extract_structured(paper_text, schema)
        print(f"Extracted: {structured}")

        # Example 3: Embedding and similarity
        print("\n=== Example 3: Embedding & Similarity ===")
        query = "machine learning for image recognition"
        doc1 = "Deep learning models for computer vision tasks"
        doc2 = "Natural language processing with transformers"

        query_emb = await embedding.embed(query, input_type="query")
        doc1_emb = await embedding.embed(doc1, input_type="passage")
        doc2_emb = await embedding.embed(doc2, input_type="passage")

        sim1 = embedding.cosine_similarity(query_emb, doc1_emb)
        sim2 = embedding.cosine_similarity(query_emb, doc2_emb)

        print(f"Query-Doc1 similarity: {sim1:.3f}")
        print(f"Query-Doc2 similarity: {sim2:.3f}")

        # Example 4: Batch embedding
        print("\n=== Example 4: Batch Embedding ===")
        papers = [
            "Paper about neural networks",
            "Paper about reinforcement learning",
            "Paper about computer vision",
            "Paper about natural language processing"
        ]

        embeddings = await embedding.embed_batch(papers)
        print(f"Embedded {len(embeddings)} papers")


if __name__ == "__main__":
    asyncio.run(example_usage())

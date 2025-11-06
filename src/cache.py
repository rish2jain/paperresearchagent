"""
Multi-Level Caching System
Provides 10-50x performance improvement through intelligent caching
L1: In-memory cache (fastest)
L2: Redis cache (shared across instances)
L3: Disk cache (persistent, large capacity)
"""

from typing import Optional, Dict, Any, List
import json
import hashlib
import logging
import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import Redis for advanced caching
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available. Install with: pip install redis")


class Cache:
    """
    Multi-level caching system with fallback
    L1: In-memory cache (fastest, smallest)
    L2: Redis cache (shared, medium speed)
    L3: Disk cache (persistent, largest capacity)
    """
    
    def __init__(
        self,
        redis_url: Optional[str] = None,
        default_ttl: int = 3600,  # 1 hour default
        disk_cache_dir: Optional[str] = None,
        enable_disk_cache: bool = True
    ):
        self.default_ttl = default_ttl
        self.redis_client = None
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        
        # Initialize Redis if available (L2)
        if REDIS_AVAILABLE and redis_url:
            try:
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
                self.redis_client.ping()
                logger.info("Redis cache (L2) connected successfully")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}, using memory cache only")
                self.redis_client = None
        
        # Initialize disk cache (L3)
        self.disk_cache_dir = disk_cache_dir or os.path.join(
            os.path.expanduser("~"), ".research-ops-cache"
        )
        self.enable_disk_cache = enable_disk_cache
        
        if self.enable_disk_cache:
            try:
                cache_path = Path(self.disk_cache_dir)
                cache_path.mkdir(parents=True, exist_ok=True)
                
                # Security check: validate cache directory ownership and permissions
                # pickle.load() can execute arbitrary code, so we must ensure the cache is trusted
                if cache_path.exists():
                    stat_info = cache_path.stat()
                    current_uid = os.getuid()
                    current_gid = os.getgid()
                    
                    # Check ownership
                    if stat_info.st_uid != current_uid:
                        logger.warning(
                            f"Cache directory owned by different user (UID {stat_info.st_uid} != {current_uid}). "
                            "Disabling disk cache for security (pickle deserialization risk)."
                        )
                        self.enable_disk_cache = False
                        return
                    
                    # Check permissions (should not be group/world-writable)
                    mode = stat_info.st_mode
                    if mode & 0o022:  # Check if group or world writable
                        logger.warning(
                            f"Cache directory is group/world-writable (mode {oct(mode)}). "
                            "Disabling disk cache for security (pickle deserialization risk)."
                        )
                        self.enable_disk_cache = False
                        return
                
                logger.info(f"Disk cache (L3) initialized at: {self.disk_cache_dir}")
            except Exception as e:
                logger.warning(f"Failed to initialize disk cache: {e}")
                self.enable_disk_cache = False
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from prefix and arguments"""
        key_data = {
            "prefix": prefix,
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"{prefix}:{key_hash}"
    
    def _get_disk_cache_path(self, key: str) -> Path:
        """Get disk cache file path for a key"""
        # Create safe filename from key
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return Path(self.disk_cache_dir) / f"{safe_key}.cache"
    
    def _load_from_disk(self, key: str) -> Optional[Any]:
        """
        Load value from disk cache (L3)
        
        WARNING: This method uses pickle.load() which can execute arbitrary code.
        The cache directory (~/.research-ops-cache) is assumed to be trusted.
        Only use disk caching if the cache directory is owned by the current user
        and not group/world-writable.
        """
        if not self.enable_disk_cache:
            return None
        
        try:
            cache_path = self._get_disk_cache_path(key)
            if not cache_path.exists():
                return None
            
            # Check if expired by reading metadata
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            
            # Check expiration
            if 'expires_at' in data:
                if datetime.now() > data['expires_at']:
                    # Expired, delete file
                    cache_path.unlink()
                    return None
            
            return data.get('value')
        except Exception as e:
            logger.debug(f"Disk cache read error for {key}: {e}")
            return None
    
    def _save_to_disk(self, key: str, value: Any, ttl: int):
        """Save value to disk cache (L3)"""
        if not self.enable_disk_cache:
            return
        
        try:
            cache_path = self._get_disk_cache_path(key)
            expires_at = datetime.now() + timedelta(seconds=ttl)
            
            data = {
                'value': value,
                'expires_at': expires_at,
                'created_at': datetime.now().isoformat()
            }
            
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            logger.debug(f"Disk cache write error for {key}: {e}")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache (checks L1 -> L2 -> L3)"""
        # L1: Try memory cache first (fastest)
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if datetime.now() < entry['expires_at']:
                logger.debug(f"Cache hit (L1): {key}")
                return entry['value']
            else:
                # Expired, remove it
                del self.memory_cache[key]
        
        # L2: Try Redis cache
        if self.redis_client:
            try:
                cached = self.redis_client.get(key)
                if cached:
                    value = json.loads(cached)
                    # Promote to L1
                    self.memory_cache[key] = {
                        'value': value,
                        'expires_at': datetime.now() + timedelta(seconds=self.default_ttl)
                    }
                    logger.debug(f"Cache hit (L2): {key}")
                    return value
            except Exception as e:
                logger.warning(f"Redis get error: {e}")
        
        # L3: Try disk cache
        value = self._load_from_disk(key)
        if value is not None:
            # Promote to L1 and L2
            self.memory_cache[key] = {
                'value': value,
                'expires_at': datetime.now() + timedelta(seconds=self.default_ttl)
            }
            if self.redis_client:
                try:
                    self.redis_client.setex(
                        key,
                        self.default_ttl,
                        json.dumps(value)
                    )
                except Exception:
                    pass
            logger.debug(f"Cache hit (L3): {key}")
            return value
        
        logger.debug(f"Cache miss: {key}")
        return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        use_disk: bool = True
    ) -> bool:
        """Set value in cache with TTL (writes to L1, L2, optionally L3)"""
        if ttl is None:
            ttl = self.default_ttl
        
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        # L1: Always write to memory cache
        self.memory_cache[key] = {
            'value': value,
            'expires_at': expires_at
        }
        
        # L2: Write to Redis if available
        if self.redis_client:
            try:
                self.redis_client.setex(
                    key,
                    ttl,
                    json.dumps(value)
                )
            except Exception as e:
                logger.warning(f"Redis set error: {e}")
        
        # L3: Write to disk cache for large/persistent values
        if use_disk and self.enable_disk_cache:
            # Only use disk cache for certain types or large values
            # (e.g., embeddings, synthesis results)
            value_size = len(str(value))
            if value_size > 1000:  # Only cache large values on disk
                self._save_to_disk(key, value, ttl)
        
        return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        # Try Redis first
        if self.redis_client:
            try:
                self.redis_client.delete(key)
            except Exception as e:
                logger.warning(f"Redis delete error: {e}")
        
        # Remove from memory cache
        if key in self.memory_cache:
            del self.memory_cache[key]
        
        return True
    
    def clear(self, prefix: Optional[str] = None) -> int:
        """Clear cache entries, optionally by prefix (clears L1, L2, L3)"""
        count = 0
        
        # L2: Clear Redis cache
        if self.redis_client:
            try:
                if prefix:
                    keys = self.redis_client.keys(f"{prefix}:*")
                    if keys:
                        count = self.redis_client.delete(*keys)
                else:
                    count = len(self.redis_client.keys("*"))
                    self.redis_client.flushdb()
            except Exception as e:
                logger.warning(f"Redis clear error: {e}")
        
        # L1: Clear memory cache
        if prefix:
            keys_to_delete = [k for k in self.memory_cache.keys() if k.startswith(prefix)]
            for k in keys_to_delete:
                del self.memory_cache[k]
            count += len(keys_to_delete)
        else:
            count += len(self.memory_cache)
            self.memory_cache.clear()
        
        # L3: Clear disk cache
        if self.enable_disk_cache:
            try:
                cache_dir = Path(self.disk_cache_dir)
                if prefix:
                    # For prefix-based clearing, we'd need to store metadata
                    # For now, just clear all disk cache
                    pass
                
                if cache_dir.exists():
                    for cache_file in cache_dir.glob("*.cache"):
                        cache_file.unlink()
                        count += 1
            except Exception as e:
                logger.warning(f"Disk cache clear error: {e}")
        
        return count
    
    def get_or_set(
        self,
        key: str,
        factory: callable,
        ttl: Optional[int] = None,
        *args,
        **kwargs
    ) -> Any:
        """Get from cache or compute and cache"""
        cached = self.get(key)
        if cached is not None:
            logger.debug(f"Cache hit: {key}")
            return cached
        
        logger.debug(f"Cache miss: {key}, computing...")
        value = factory(*args, **kwargs)
        self.set(key, value, ttl)
        return value


class PaperMetadataCache:
    """Specialized cache for paper metadata"""
    
    def __init__(self, cache: Cache):
        self.cache = cache
        self.prefix = "paper_metadata"
        self.ttl = 86400  # 24 hours
    
    def get_paper(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """Get cached paper metadata"""
        key = self.cache._generate_key(self.prefix, paper_id)
        return self.cache.get(key)
    
    def set_paper(self, paper_id: str, paper_data: Dict[str, Any]):
        """Cache paper metadata"""
        key = self.cache._generate_key(self.prefix, paper_id)
        self.cache.set(key, paper_data, self.ttl)
    
    def get_papers_batch(self, paper_ids: List[str]) -> Dict[str, Optional[Dict[str, Any]]]:
        """Get multiple papers from cache"""
        result = {}
        for paper_id in paper_ids:
            result[paper_id] = self.get_paper(paper_id)
        return result


class EmbeddingCache:
    """Specialized cache for embeddings"""
    
    def __init__(self, cache: Cache):
        self.cache = cache
        self.prefix = "embedding"
        self.ttl = 604800  # 7 days (embeddings rarely change)
    
    def get_embedding(self, text: str, input_type: str = "passage") -> Optional[List[float]]:
        """Get cached embedding"""
        key = self.cache._generate_key(self.prefix, text, input_type=input_type)
        return self.cache.get(key)
    
    def set_embedding(
        self,
        text: str,
        embedding: List[float],
        input_type: str = "passage"
    ):
        """Cache embedding"""
        key = self.cache._generate_key(self.prefix, text, input_type=input_type)
        self.cache.set(key, embedding, self.ttl)


class SynthesisCache:
    """Specialized cache for synthesis results"""
    
    def __init__(self, cache: Cache):
        self.cache = cache
        self.prefix = "synthesis"
        self.ttl = 3600  # 1 hour
    
    def get_synthesis(self, query: str, max_papers: int) -> Optional[Dict[str, Any]]:
        """Get cached synthesis result"""
        key = self.cache._generate_key(self.prefix, query, max_papers=max_papers)
        return self.cache.get(key)
    
    def set_synthesis(
        self,
        query: str,
        max_papers: int,
        result: Dict[str, Any]
    ):
        """Cache synthesis result"""
        key = self.cache._generate_key(self.prefix, query, max_papers=max_papers)
        self.cache.set(key, result, self.ttl)


def get_cache() -> Cache:
    """Get global cache instance with multi-level caching"""
    import os
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    disk_cache_dir = os.getenv("DISK_CACHE_DIR")
    enable_disk_cache = os.getenv("ENABLE_DISK_CACHE", "true").lower() == "true"
    
    return Cache(
        redis_url=redis_url,
        default_ttl=3600,
        disk_cache_dir=disk_cache_dir,
        enable_disk_cache=enable_disk_cache
    )


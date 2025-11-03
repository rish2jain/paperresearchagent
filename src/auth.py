"""
API Authentication and Rate Limiting
Provides secure API access with rate limiting
"""

from typing import Optional, Dict, Any
import hashlib
import time
import logging
from datetime import datetime, timedelta
from functools import wraps

logger = logging.getLogger(__name__)

# Try to import Redis for distributed rate limiting
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class RateLimiter:
    """
    Enhanced rate limiter using sliding window algorithm
    Supports both in-memory and Redis-backed rate limiting
    Features:
    - Per-endpoint rate limits
    - Burst capacity handling
    - Distributed rate limiting (with Redis)
    - Adaptive rate limiting based on load
    """
    
    def __init__(
        self,
        redis_url: Optional[str] = None,
        default_limit: int = 100,
        default_window: int = 60,  # seconds
        burst_multiplier: float = 1.5  # Allow 50% burst above limit
    ):
        self.default_limit = default_limit
        self.default_window = default_window
        self.burst_multiplier = burst_multiplier
        self.redis_client = None
        
        # In-memory rate limit storage
        self.memory_limits: Dict[str, Dict[str, Any]] = {}
        
        # Per-endpoint limits (can be customized)
        self.endpoint_limits: Dict[str, Dict[str, int]] = {
            "/research": {"limit": 10, "window": 60},  # 10 requests per minute for research
            "/health": {"limit": 100, "window": 60},  # 100 requests per minute for health
            "/sources": {"limit": 30, "window": 60},  # 30 requests per minute for sources
        }
        
        # Initialize Redis if available
        if REDIS_AVAILABLE and redis_url:
            try:
                self.redis_client = redis.from_url(
                    redis_url, 
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                self.redis_client.ping()
                logger.info("Redis rate limiter connected")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}, using memory rate limiting")
                self.redis_client = None
    
    def _get_key(self, identifier: str, limit_type: str = "default") -> str:
        """Generate rate limit key"""
        return f"rate_limit:{limit_type}:{identifier}"
    
    def check_rate_limit(
        self,
        identifier: str,
        limit: Optional[int] = None,
        window: Optional[int] = None,
        limit_type: str = "default",
        endpoint: Optional[str] = None
    ) -> tuple[bool, int, int]:
        """
        Enhanced rate limit checking with per-endpoint limits and burst capacity
        
        Args:
            identifier: Client identifier (IP or API key hash)
            limit: Custom limit override (uses endpoint or default if None)
            window: Custom window override (uses endpoint or default if None)
            limit_type: Type of rate limit (e.g., "api", "research")
            endpoint: API endpoint path (e.g., "/research") for per-endpoint limits
        
        Returns:
            (allowed, remaining, reset_time)
        """
        # Check for per-endpoint limits
        if endpoint and endpoint in self.endpoint_limits:
            endpoint_config = self.endpoint_limits[endpoint]
            limit = limit or endpoint_config.get("limit", self.default_limit)
            window = window or endpoint_config.get("window", self.default_window)
        else:
            limit = limit or self.default_limit
            window = window or self.default_window
        
        # Calculate burst limit
        burst_limit = int(limit * self.burst_multiplier)
        
        key = self._get_key(identifier, limit_type)
        current_time = time.time()
        window_start = current_time - window
        
        # Try Redis first for distributed rate limiting
        if self.redis_client:
            try:
                # Get current count with sliding window
                pipe = self.redis_client.pipeline()
                pipe.zremrangebyscore(key, 0, window_start)  # Remove old entries
                pipe.zcard(key)  # Count remaining entries
                pipe.expire(key, window)  # Set expiration
                results = pipe.execute()
                
                current_count = results[1]
                
                # Check against burst limit first, then regular limit
                if current_count < burst_limit:
                    # Allow request (within burst capacity)
                    self.redis_client.zadd(key, {str(current_time): current_time})
                    # Calculate remaining based on whether burst is being used
                    if current_count >= limit:
                        # Using burst capacity
                        remaining = max(0, burst_limit - current_count - 1)
                        logger.debug(f"Rate limit burst capacity used: {current_count}/{burst_limit} for {identifier}")
                    else:
                        # Within regular limit
                        remaining = max(0, limit - current_count - 1)
                    reset_time = int(current_time + window)
                    
                    return True, remaining, reset_time
                else:
                    # Rate limit exceeded (including burst)
                    oldest_entry = self.redis_client.zrange(key, 0, 0, withscores=True)
                    if oldest_entry:
                        reset_time = int(oldest_entry[0][1] + window)
                    else:
                        reset_time = int(current_time + window)
                    logger.warning(f"Rate limit exceeded for {identifier}: {current_count}/{burst_limit}")
                    return False, 0, reset_time
            except Exception as e:
                logger.warning(f"Redis rate limit error: {e}, falling back to memory")
        
        # Fallback to memory-based rate limiting
        if key not in self.memory_limits:
            self.memory_limits[key] = {
                'requests': [],
                'limit': limit,
                'window': window
            }
        
        limit_data = self.memory_limits[key]
        
        # Remove old requests outside window
        limit_data['requests'] = [
            req_time for req_time in limit_data['requests']
            if req_time > window_start
        ]
        
        current_count = len(limit_data['requests'])
        
        # Check against burst limit first, then regular limit
        if current_count < burst_limit:
            # Allow request (within burst capacity)
            limit_data['requests'].append(current_time)
            # Calculate remaining based on whether burst is being used
            # Match Redis behavior: remaining = max(0, burst_limit - current_count - 1)
            remaining = max(0, burst_limit - current_count - 1)
            if current_count >= limit:
                # Using burst capacity
                logger.debug(f"Rate limit burst capacity used: {current_count}/{burst_limit} for {identifier}")
            else:
                # Within regular limit
                logger.debug(f"Rate limit within regular limit: {current_count}/{limit} for {identifier}")
            reset_time = int(current_time + window)
            
            return True, remaining, reset_time
        else:
            # Rate limit exceeded (including burst)
            oldest_request = min(limit_data['requests']) if limit_data['requests'] else current_time
            reset_time = int(oldest_request + window)
            logger.warning(f"Rate limit exceeded for {identifier}: {current_count}/{burst_limit}")
            return False, 0, reset_time


class APIKeyAuth:
    """
    API Key authentication system
    """
    
    def __init__(self, valid_keys: Optional[list] = None):
        self.valid_keys = set(valid_keys or [])
        
        # Load from environment
        import os
        api_key = os.getenv("API_KEY")
        if api_key:
            self.valid_keys.add(api_key)
    
    def validate_key(self, api_key: Optional[str]) -> bool:
        """Validate API key"""
        if not api_key:
            return False
        
        return api_key in self.valid_keys
    
    def add_key(self, api_key: str):
        """Add a valid API key"""
        self.valid_keys.add(api_key)
    
    def remove_key(self, api_key: str):
        """Remove an API key"""
        self.valid_keys.discard(api_key)


class AuthMiddleware:
    """
    Authentication and rate limiting middleware
    """
    
    def __init__(
        self,
        api_auth: Optional[APIKeyAuth] = None,
        rate_limiter: Optional[RateLimiter] = None,
        require_auth: bool = False
    ):
        self.api_auth = api_auth or APIKeyAuth()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.require_auth = require_auth
    
    def get_client_identifier(self, request) -> str:
        """Get client identifier for rate limiting"""
        # Try to get API key first
        api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization")
        if api_key:
            if api_key.startswith("Bearer "):
                api_key = api_key[7:]
            # Use hash of API key as identifier
            return hashlib.md5(api_key.encode()).hexdigest()
        
        # Fallback to IP address
        client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        if not client_ip:
            client_ip = request.client.host if hasattr(request, 'client') else "unknown"
        
        return client_ip
    
    def check_auth(self, request) -> tuple[bool, Optional[str]]:
        """Check authentication"""
        if not self.require_auth:
            return True, None
        
        api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization")
        if api_key and api_key.startswith("Bearer "):
            api_key = api_key[7:]
        
        if not api_key:
            return False, "API key required"
        
        if not self.api_auth.validate_key(api_key):
            return False, "Invalid API key"
        
        return True, None
    
    def check_rate_limit(
        self, 
        request, 
        limit: int = None, 
        window: int = None,
        endpoint: Optional[str] = None
    ) -> tuple[bool, Dict[str, Any]]:
        """
        Enhanced rate limit checking with per-endpoint support
        
        Args:
            request: FastAPI request object
            limit: Custom limit override
            window: Custom window override
            endpoint: API endpoint path for per-endpoint limits
        """
        identifier = self.get_client_identifier(request)
        
        # Extract endpoint from request if not provided
        if endpoint is None:
            endpoint = request.url.path if hasattr(request, 'url') else None
        
        allowed, remaining, reset_time = self.rate_limiter.check_rate_limit(
            identifier,
            limit=limit,
            window=window,
            endpoint=endpoint
        )
        
        # Get actual limits used (for response headers)
        if endpoint and endpoint in self.rate_limiter.endpoint_limits:
            endpoint_config = self.rate_limiter.endpoint_limits[endpoint]
            actual_limit = limit or endpoint_config.get("limit", self.rate_limiter.default_limit)
            actual_window = window or endpoint_config.get("window", self.rate_limiter.default_window)
        else:
            actual_limit = limit or self.rate_limiter.default_limit
            actual_window = window or self.rate_limiter.default_window
        
        rate_limit_info = {
            "allowed": allowed,
            "remaining": remaining,
            "reset_time": reset_time,
            "limit": actual_limit,
            "window": actual_window,
            "burst_limit": int(actual_limit * self.rate_limiter.burst_multiplier),
            "endpoint": endpoint
        }
        
        return allowed, rate_limit_info


def get_auth_middleware() -> AuthMiddleware:
    """Get global auth middleware instance with enhanced rate limiting"""
    import os
    redis_url = os.getenv("REDIS_URL")
    
    # Enhanced rate limiter with configurable burst capacity
    burst_multiplier = float(os.getenv("RATE_LIMIT_BURST_MULTIPLIER", "1.5"))
    default_limit = int(os.getenv("RATE_LIMIT_DEFAULT", "100"))
    default_window = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    rate_limiter = RateLimiter(
        redis_url=redis_url,
        default_limit=default_limit,
        default_window=default_window,
        burst_multiplier=burst_multiplier
    )
    
    require_auth = os.getenv("REQUIRE_API_AUTH", "false").lower() == "true"
    api_auth = APIKeyAuth()
    
    return AuthMiddleware(
        api_auth=api_auth,
        rate_limiter=rate_limiter,
        require_auth=require_auth
    )


"""
Health Status Caching
Reduces latency by caching NIM health check results
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class HealthStatusCache:
    """Cache for health check results to reduce NIM endpoint calls"""
    
    def __init__(self, ttl_seconds: int = 30):
        """
        Initialize health status cache
        
        Args:
            ttl_seconds: Time-to-live for cached health status (default: 30 seconds)
        """
        self._cache: Dict[str, bool] = {}
        self._timestamps: Dict[str, datetime] = {}
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def get(self, service: str) -> Optional[bool]:
        """
        Get cached health status for a service
        
        Args:
            service: Service identifier (e.g., 'reasoning_nim', 'embedding_nim')
        
        Returns:
            Cached health status (True/False) or None if not cached or expired
        """
        if service not in self._cache:
            return None
        
        if service not in self._timestamps:
            return None
        
        # Check if cache is expired
        if datetime.now() - self._timestamps[service] > self.ttl:
            # Remove expired entry
            del self._cache[service]
            del self._timestamps[service]
            return None
        
        return self._cache[service]
    
    def set(self, service: str, status: bool):
        """
        Cache health status for a service
        
        Args:
            service: Service identifier
            status: Health status (True = healthy, False = unhealthy)
        """
        self._cache[service] = status
        self._timestamps[service] = datetime.now()
        logger.debug(f"Cached health status for {service}: {status}")
    
    def clear(self, service: Optional[str] = None):
        """
        Clear cache entry(s)
        
        Args:
            service: Service identifier to clear, or None to clear all
        """
        if service is None:
            self._cache.clear()
            self._timestamps.clear()
            logger.debug("Cleared all health status cache")
        elif service in self._cache:
            del self._cache[service]
            if service in self._timestamps:
                del self._timestamps[service]
            logger.debug(f"Cleared health status cache for {service}")
    
    def is_expired(self, service: str) -> bool:
        """
        Check if cached entry is expired
        
        Args:
            service: Service identifier
        
        Returns:
            True if expired or not cached, False if still valid
        """
        if service not in self._timestamps:
            return True
        
        return datetime.now() - self._timestamps[service] > self.ttl


# Global health cache instance
_health_cache: Optional[HealthStatusCache] = None


def get_health_cache(ttl_seconds: int = 30) -> HealthStatusCache:
    """Get global health cache instance"""
    global _health_cache
    if _health_cache is None:
        _health_cache = HealthStatusCache(ttl_seconds=ttl_seconds)
    return _health_cache


"""
Circuit Breaker Implementation
Provides graceful degradation when NIM services are unavailable
"""

import time
import logging
import asyncio
import inspect
import threading
from enum import Enum
from typing import Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation, requests pass through
    OPEN = "open"          # Service unavailable, reject requests immediately
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    fail_max: int = 5              # Open circuit after N failures
    timeout_duration: int = 60     # Stay open for N seconds
    success_threshold: int = 2     # Close after N successes in half-open
    excluded_exceptions: tuple = (ValueError,)  # Don't count validation errors


class CircuitBreaker:
    """
    Simple circuit breaker pattern for async operations
    Prevents cascading failures when external services are down
    """
    
    def __init__(
        self,
        name: str = "circuit",
        config: Optional[CircuitBreakerConfig] = None
    ):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        
        self._lock = threading.Lock()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.next_attempt_time: Optional[datetime] = None
    
    def _should_attempt(self) -> bool:
        """Check if we should attempt a request based on circuit state"""
        with self._lock:
            if self.state == CircuitState.CLOSED:
                return True
            
            if self.state == CircuitState.OPEN:
                # Check if timeout has passed
                if self.next_attempt_time and datetime.now() >= self.next_attempt_time:
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    logger.info(f"Circuit breaker {self.name}: Moving to HALF_OPEN state")
                    return True
                return False
            
            # HALF_OPEN state - allow attempt
            return True
    
    def _on_success(self):
        """Handle successful request"""
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
                    logger.info(f"Circuit breaker {self.name}: Service recovered, CLOSED")
            elif self.state == CircuitState.CLOSED:
                # Reset failure count on success
                self.failure_count = 0
    
    def _on_failure(self, exception: Exception):
        """Handle failed request"""
        # Don't count excluded exceptions
        if isinstance(exception, self.config.excluded_exceptions):
            logger.debug(f"Circuit breaker {self.name}: Excluding {type(exception).__name__} from failure count")
            return
        
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                # Failed in half-open, go back to open
                self.state = CircuitState.OPEN
                self.failure_count = 0
                self.success_count = 0
                self.last_failure_time = datetime.now()
                self.next_attempt_time = datetime.now() + timedelta(
                    seconds=self.config.timeout_duration
                )
                logger.warning(
                    f"Circuit breaker {self.name}: Service still failing, back to OPEN"
                )
            else:
                # Increment failure count
                self.failure_count += 1
                self.last_failure_time = datetime.now()
                
                if self.failure_count >= self.config.fail_max:
                    self.state = CircuitState.OPEN
                    self.next_attempt_time = datetime.now() + timedelta(
                        seconds=self.config.timeout_duration
                    )
                    logger.warning(
                        f"Circuit breaker {self.name}: OPEN after {self.failure_count} failures. "
                        f"Will retry after {self.config.timeout_duration}s"
                    )
    
    async def call(
        self,
        func: Callable,
        *args,
        fallback: Optional[Callable] = None,
        **kwargs
    ) -> Any:
        """
        Execute function with circuit breaker protection
        
        Args:
            func: Async function to execute
            *args: Positional arguments for func
            fallback: Optional fallback function if circuit is open
            **kwargs: Keyword arguments for func
        
        Returns:
            Result from func or fallback
        
        Raises:
            CircuitBreakerOpenError: If circuit is open and no fallback provided
        """
        if not self._should_attempt():
            if fallback:
                logger.warning(
                    f"Circuit breaker {self.name}: OPEN, using fallback"
                )
                if callable(fallback):
                    result = fallback(*args, **kwargs)
                    # Check if result is awaitable (coroutine)
                    if inspect.isawaitable(result):
                        return await result
                    else:
                        return result
                else:
                    # Not callable, return the value directly
                    return fallback
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker {self.name} is OPEN. "
                    f"Service unavailable. Retry after {self.next_attempt_time}"
                )
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure(e)
            raise
    
    def get_state(self) -> dict:
        """Get current circuit breaker state (thread-safe snapshot)"""
        with self._lock:
            return {
                "name": self.name,
                "state": self.state.value,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "last_failure_time": (
                    self.last_failure_time.isoformat() if self.last_failure_time else None
                ),
                "next_attempt_time": (
                    self.next_attempt_time.isoformat() if self.next_attempt_time else None
                )
            }


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open and no fallback available"""
    pass


def circuit_breaker_decorator(
    name: str,
    config: Optional[CircuitBreakerConfig] = None,
    fallback: Optional[Callable] = None
):
    """
    Decorator for circuit breaker pattern
    
    Usage:
        @circuit_breaker_decorator("reasoning_nim")
        async def complete(prompt: str) -> str:
            # Implementation
    """
    breaker = CircuitBreaker(name, config)
    
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            return await breaker.call(func, *args, fallback=fallback, **kwargs)
        return wrapper
    
    return decorator


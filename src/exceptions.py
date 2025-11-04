"""
Custom Exception Hierarchy for Agentic Researcher
Provides structured error handling with specific exception types
"""


class ResearchOpsError(Exception):
    """Base exception for Agentic Researcher"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def to_dict(self) -> dict:
        """Convert exception to dictionary for API responses"""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "details": self.details
        }


class NIMServiceError(ResearchOpsError):
    """NIM service unavailable or error"""
    
    def __init__(self, message: str, service: str = None, details: dict = None):
        super().__init__(message, details)
        self.service = service
        if service:
            self.details["service"] = service


class ValidationError(ResearchOpsError):
    """Input validation error"""
    
    def __init__(self, message: str, field: str = None, details: dict = None):
        super().__init__(message, details)
        self.field = field
        if field:
            self.details["field"] = field


class PaperSourceError(ResearchOpsError):
    """Paper source API error"""
    
    def __init__(self, message: str, source: str = None, details: dict = None):
        super().__init__(message, details)
        self.source = source
        if source:
            self.details["source"] = source


class CircuitBreakerOpenError(ResearchOpsError):
    """Circuit breaker is open, service unavailable"""
    
    def __init__(self, message: str, service: str = None, retry_after: int = None, details: dict = None):
        super().__init__(message, details)
        self.service = service
        self.retry_after = retry_after
        if service:
            self.details["service"] = service
        if retry_after:
            self.details["retry_after"] = retry_after


class ConfigurationError(ResearchOpsError):
    """Configuration validation error"""
    pass


class CacheError(ResearchOpsError):
    """Cache operation error"""
    pass


class RateLimitError(ResearchOpsError):
    """Rate limit exceeded"""
    
    def __init__(self, message: str, limit: int = None, reset_time: int = None, details: dict = None):
        super().__init__(message, details)
        self.limit = limit
        self.reset_time = reset_time
        if limit:
            self.details["limit"] = limit
        if reset_time:
            self.details["reset_time"] = reset_time


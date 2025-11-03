"""
Input Sanitization
Prevents prompt injection attacks and validates user input
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when input validation fails"""
    pass


def sanitize_research_query(query: str, max_length: int = 1000) -> str:
    """
    Sanitize research query to prevent prompt injection attacks
    
    Args:
        query: User input query string
        max_length: Maximum allowed query length
    
    Returns:
        Sanitized query string
    
    Raises:
        ValidationError: If query contains suspicious content or is too long
    """
    if not query or not isinstance(query, str):
        raise ValidationError("Query must be a non-empty string")
    
    # Remove leading/trailing whitespace
    query = query.strip()
    
    if not query:
        raise ValidationError("Query cannot be empty")
    
    # Check length
    if len(query) > max_length:
        raise ValidationError(f"Query too long (max {max_length} characters, got {len(query)})")
    
    # Dangerous patterns that indicate prompt injection attempts
    dangerous_patterns = [
        r"ignore\s+previous\s+instructions?",
        r"forget\s+everything",
        r"you\s+are\s+now",
        r"<script[^>]*>",
        r"javascript:",
        r"data:text/html",
        r"on\w+\s*=",  # Event handlers like onclick=
        r"<\?php",
        r"<iframe",
        r"eval\s*\(",
        r"exec\s*\(",
        r"system\s*\(",
        r"__import__",
        r"import\s+os",
        r"import\s+sys",
        r"import\s+subprocess",
    ]
    
    query_lower = query.lower()
    
    for pattern in dangerous_patterns:
        if re.search(pattern, query_lower, re.IGNORECASE):
            logger.warning(f"Query contains suspicious pattern '{pattern}': {query[:50]}...")
            raise ValidationError(
                f"Query contains potentially malicious content. "
                f"Please reformulate your research question."
            )
    
    # Check for excessive special characters (possible obfuscation)
    special_char_count = len(re.findall(r'[!@#$%^&*()_+=\[\]{}|\\:";\'<>?,./]', query))
    if special_char_count > len(query) * 0.3:  # More than 30% special characters
        logger.warning(f"Query has suspiciously high special character ratio: {special_char_count}/{len(query)}")
        raise ValidationError("Query contains too many special characters. Please use natural language.")
    
    # Normalize whitespace
    query = re.sub(r'\s+', ' ', query)
    
    logger.debug(f"Sanitized query: {query[:50]}...")
    return query


def validate_max_papers(max_papers: int, min_papers: int = 1, max_allowed: int = 50) -> int:
    """
    Validate and sanitize max_papers parameter
    
    Args:
        max_papers: Requested number of papers
        min_papers: Minimum allowed papers
        max_allowed: Maximum allowed papers
    
    Returns:
        Validated max_papers value
    
    Raises:
        ValidationError: If max_papers is out of range
    """
    if not isinstance(max_papers, int):
        try:
            max_papers = int(max_papers)
        except (ValueError, TypeError):
            raise ValidationError(f"max_papers must be an integer, got {type(max_papers)}")
    
    if max_papers < min_papers:
        raise ValidationError(f"max_papers must be at least {min_papers}, got {max_papers}")
    
    if max_papers > max_allowed:
        raise ValidationError(f"max_papers cannot exceed {max_allowed}, got {max_papers}")
    
    return max_papers


def sanitize_year(year: Optional[int], min_year: int = 1900, max_year: int = 2100) -> Optional[int]:
    """
    Validate year parameter
    
    Args:
        year: Year to validate (can be None)
        min_year: Minimum allowed year
        max_year: Maximum allowed year
    
    Returns:
        Validated year or None
    
    Raises:
        ValidationError: If year is out of range
    """
    if year is None:
        return None
    
    if not isinstance(year, int):
        try:
            year = int(year)
        except (ValueError, TypeError):
            raise ValidationError(f"Year must be an integer, got {type(year)}")
    
    if year < min_year:
        raise ValidationError(f"Year cannot be before {min_year}, got {year}")
    
    if year > max_year:
        raise ValidationError(f"Year cannot be after {max_year}, got {year}")
    
    return year


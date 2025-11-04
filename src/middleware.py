"""
Middleware for Agentic Researcher API
Includes request ID tracking, size validation, and error handling
"""

import uuid
import os
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
try:
    from starlette.requests import Request
except ImportError:
    # Fallback for older versions
    from fastapi import Request
from starlette.responses import JSONResponse
from constants import MAX_REQUEST_SIZE_BYTES

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to all requests for tracking"""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response


class RequestSizeMiddleware(BaseHTTPMiddleware):
    """Validate request size early to prevent large payload attacks"""
    
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        
        if content_length:
            try:
                size = int(content_length)
                if size > MAX_REQUEST_SIZE_BYTES:
                    logger.warning(
                        f"Request too large: {size} bytes (max: {MAX_REQUEST_SIZE_BYTES})",
                        extra={"request_id": getattr(request.state, "request_id", None)}
                    )
                    return JSONResponse(
                        status_code=413,
                        content={
                            "error": "Request too large",
                            "message": f"Request size ({size} bytes) exceeds maximum ({MAX_REQUEST_SIZE_BYTES} bytes)",
                            "max_size": MAX_REQUEST_SIZE_BYTES
                        }
                    )
            except (ValueError, TypeError):
                logger.warning(f"Invalid content-length header: {content_length}")
        
        return await call_next(request)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handler for unhandled exceptions"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            request_id = getattr(request.state, "request_id", None)
            logger.error(
                f"Unhandled exception: {type(e).__name__}: {e}",
                exc_info=True,
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "method": request.method
                }
            )
            
            # Return user-friendly error (hide internal details in production)
            is_debug = os.getenv("DEBUG", "false").lower() == "true"
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": str(e) if is_debug else "An unexpected error occurred",
                    "request_id": request_id,
                    "timestamp": __import__("datetime").datetime.now().isoformat()
                }
            )


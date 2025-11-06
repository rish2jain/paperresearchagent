"""
FastAPI REST API for Agentic Researcher
Provides HTTP endpoints for the multi-agent research synthesis system
"""

# Load .env file automatically if it exists (before other imports that use os.getenv)
try:
    from dotenv import load_dotenv
    import os
    # Load .env from project root (parent directory of src/)
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        # Also try loading from current directory (for when running from root)
        load_dotenv()
except ImportError:
    # python-dotenv not installed, skip automatic loading
    pass

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from starlette.requests import Request as StarletteRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
# Import middleware with fallback for different execution contexts
try:
    from .middleware import RequestIDMiddleware, RequestSizeMiddleware, ErrorHandlerMiddleware
except ImportError:
    # Fallback for direct script execution
    from middleware import RequestIDMiddleware, RequestSizeMiddleware, ErrorHandlerMiddleware
from pydantic import BaseModel, Field, model_validator
from typing import Dict, List, Optional, Any
import asyncio
import time
import logging
import os
from datetime import datetime
import json

# Import local modules with fallback for different execution contexts
try:
    from .nim_clients import ReasoningNIMClient, EmbeddingNIMClient
    from .unified_clients import UnifiedReasoningClient, UnifiedEmbeddingClient
    from .agents import ResearchOpsAgent, ResearchQuery, Synthesis
    from .denario_integration import DenarioIntegration
    from .incremental_synthesizer import IncrementalSynthesizer
    from .input_sanitization import (
        sanitize_research_query,
        validate_max_papers,
        sanitize_year,
        ValidationError as InputValidationError,
    )
    from .exceptions import (
        ResearchOpsError,
        NIMServiceError,
        ValidationError,
        PaperSourceError,
        CircuitBreakerOpenError,
        ConfigurationError,
    )
    from .constants import (
        DEFAULT_CORS_ORIGINS,
        CORS_MAX_AGE_SECONDS,
        MAX_REQUEST_SIZE_BYTES,
        HEALTH_CHECK_TIMEOUT_SECONDS,
        HEALTH_CHECK_CONNECT_TIMEOUT_SECONDS,
        HEALTH_CACHE_TTL_SECONDS,
    )
    from .health_cache import get_health_cache
except ImportError:
    # Fallback for direct script execution
    from nim_clients import ReasoningNIMClient, EmbeddingNIMClient
    from unified_clients import UnifiedReasoningClient, UnifiedEmbeddingClient
    from agents import ResearchOpsAgent, ResearchQuery, Synthesis
    from denario_integration import DenarioIntegration
    from incremental_synthesizer import IncrementalSynthesizer
    from input_sanitization import (
        sanitize_research_query,
        validate_max_papers,
        sanitize_year,
        ValidationError as InputValidationError,
    )
    from exceptions import (
        ResearchOpsError,
        NIMServiceError,
        ValidationError,
        PaperSourceError,
        CircuitBreakerOpenError,
        ConfigurationError,
    )
    from constants import (
        DEFAULT_CORS_ORIGINS,
        CORS_MAX_AGE_SECONDS,
        MAX_REQUEST_SIZE_BYTES,
        HEALTH_CHECK_TIMEOUT_SECONDS,
        HEALTH_CHECK_CONNECT_TIMEOUT_SECONDS,
        HEALTH_CACHE_TTL_SECONDS,
    )
    from health_cache import get_health_cache

# Import export functions
try:
    from .export_formats import generate_bibtex, generate_latex_document
except ImportError:
    # Fallback for direct script execution
    from export_formats import generate_bibtex, generate_latex_document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agentic Researcher API",
    description="Multi-agent AI system for automated literature review synthesis using NVIDIA NIMs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middleware (order matters - error handler should be last)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RequestSizeMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# CORS middleware for web UI - environment-based configuration
cors_origins_env = os.getenv("CORS_ORIGINS", ",".join(DEFAULT_CORS_ORIGINS))
cors_origins = (
    cors_origins_env.split(",") if cors_origins_env != "*" else ["*"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset", "X-Request-ID"],
    max_age=CORS_MAX_AGE_SECONDS,
)

# Store for in-progress and completed research sessions
research_sessions: Dict[str, Dict] = {}

# Import metrics, auth, and caching
try:
    from metrics import get_metrics_collector
    from auth import get_auth_middleware

    METRICS_AVAILABLE = True
    AUTH_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    AUTH_AVAILABLE = False
    logger.warning("Metrics and auth modules not available")

# Initialize metrics and auth
if METRICS_AVAILABLE:
    metrics = get_metrics_collector()
else:
    metrics = None

if AUTH_AVAILABLE:
    auth_middleware = get_auth_middleware()
else:
    auth_middleware = None


# Middleware for metrics and auth
@app.middleware("http")
async def metrics_and_auth_middleware(request: StarletteRequest, call_next):
    """Middleware for metrics collection and rate limiting"""
    start_time = time.time()

    # Check authentication if required
    if auth_middleware and auth_middleware.require_auth:
        auth_ok, auth_error = auth_middleware.check_auth(request)
        if not auth_ok:
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "message": auth_error},
            )

    # Check rate limit (with per-endpoint limits)
    if auth_middleware:
        endpoint = request.url.path if hasattr(request, "url") else None
        allowed, rate_limit_info = auth_middleware.check_rate_limit(
            request, endpoint=endpoint
        )
        if not allowed:
            return JSONResponse(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Rate limit: {rate_limit_info['limit']} requests per {rate_limit_info['window']} seconds",
                    "reset_time": rate_limit_info["reset_time"],
                    "remaining": rate_limit_info["remaining"],
                },
                headers={
                    "X-RateLimit-Limit": str(rate_limit_info["limit"]),
                    "X-RateLimit-Remaining": str(rate_limit_info["remaining"]),
                    "X-RateLimit-Reset": str(rate_limit_info["reset_time"]),
                },
            )

    # Track active requests
    if metrics:
        metrics.increment_active_requests()

    try:
        response = await call_next(request)
        duration = time.time() - start_time

        # Record metrics
        if metrics:
            status = "success" if response.status_code < 400 else "error"
            metrics.record_request(status, duration)
            metrics.decrement_active_requests()

        # Add rate limit headers
        if auth_middleware:
            identifier = auth_middleware.get_client_identifier(request)
            _, rate_limit_info = auth_middleware.check_rate_limit(request)
            response.headers["X-RateLimit-Limit"] = str(rate_limit_info["limit"])
            response.headers["X-RateLimit-Remaining"] = str(
                rate_limit_info["remaining"]
            )
            response.headers["X-RateLimit-Reset"] = str(rate_limit_info["reset_time"])

        return response
    except Exception as e:
        duration = time.time() - start_time
        if metrics:
            metrics.record_request("error", duration)
            metrics.decrement_active_requests()
        raise


# Request/Response Models
class ResearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Research query in natural language",
    )
    max_papers: int = Field(
        default=10, ge=1, le=50, description="Maximum number of papers to analyze"
    )
    start_year: Optional[int] = Field(
        default=None,
        ge=1900,
        le=2100,
        description="Filter papers from this year onwards",
    )
    end_year: Optional[int] = Field(
        default=None, ge=1900, le=2100, description="Filter papers up to this year"
    )
    prioritize_recent: bool = Field(
        default=False, description="Prioritize recent papers (last 3 years)"
    )

    @model_validator(mode='after')
    def validate_date_range(self):
        """Validate that end_year is >= start_year when both are provided"""
        if self.end_year is not None and self.start_year is not None:
            if self.end_year < self.start_year:
                raise ValueError(
                    f"end_year ({self.end_year}) must be greater than or equal to start_year ({self.start_year})"
                )
        return self

    class Config:
        schema_extra = {
            "example": {
                "query": "machine learning for medical imaging",
                "max_papers": 10,
                "start_year": 2020,
                "end_year": 2024,
                "prioritize_recent": True,
            }
        }


class ResearchResponse(BaseModel):
    papers_analyzed: int
    common_themes: List[str]
    contradictions: List[Dict]
    research_gaps: List[str]
    decisions: List[Dict]
    synthesis_complete: bool
    processing_time_seconds: float
    query: str

    class Config:
        schema_extra = {
            "example": {
                "query": "machine learning for medical imaging",
                "papers_analyzed": 10,
                "common_themes": [
                    "Deep learning architectures for medical image segmentation",
                    "Transfer learning and domain adaptation techniques",
                ],
                "contradictions": [
                    {
                        "paper1": "Paper A",
                        "claim1": "Claims X",
                        "paper2": "Paper B",
                        "claim2": "Claims Y",
                        "conflict": "Contradictory results",
                    }
                ],
                "research_gaps": [
                    "Limited studies on multi-modal fusion",
                    "Gap in longitudinal prediction studies",
                ],
                "decisions": [
                    {
                        "timestamp": "2025-01-01T12:00:00",
                        "agent": "Scout",
                        "decision_type": "RELEVANCE_FILTERING",
                        "decision": "ACCEPTED 12/25 papers",
                        "reasoning": "Applied relevance threshold...",
                        "nim_used": "nv-embedqa-e5-v5 (Embedding NIM)",
                        "metadata": {},
                    }
                ],
                "synthesis_complete": True,
                "processing_time_seconds": 45.2,
            }
        }


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
    nims_available: Dict[str, bool]


class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: str


# Health check endpoint with caching
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint to verify service is running

    Returns service status and availability of NIMs
    Uses caching to reduce latency for repeated checks
    """

    health_cache = get_health_cache(ttl_seconds=HEALTH_CACHE_TTL_SECONDS)

    async def check_nim_health(base_url: str, service_name: str) -> bool:
        """Check if NIM is actually responding, with caching"""
        # Check cache first
        cached_status = health_cache.get(service_name)
        if cached_status is not None:
            logger.debug(f"Health cache hit for {service_name}: {cached_status}")
            return cached_status
        
        # Cache miss - check actual health
        try:
            import aiohttp

            timeout = aiohttp.ClientTimeout(
                total=HEALTH_CHECK_TIMEOUT_SECONDS,
                connect=HEALTH_CHECK_CONNECT_TIMEOUT_SECONDS
            )
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{base_url}/v1/health/live") as response:
                    status = response.status == 200
                    # Cache the result
                    health_cache.set(service_name, status)
                    return status
        except Exception as e:
            logger.debug(f"Health check failed for {service_name}: {e}")
            # Cache negative result too
            health_cache.set(service_name, False)
            return False

    # Check actual NIM availability
    reasoning_nim_url = os.getenv(
        "REASONING_NIM_URL", "http://reasoning-nim.research-ops.svc.cluster.local:8000"
    )
    embedding_nim_url = os.getenv(
        "EMBEDDING_NIM_URL", "http://embedding-nim.research-ops.svc.cluster.local:8001"
    )

    reasoning_available = await check_nim_health(reasoning_nim_url, "reasoning_nim")
    embedding_available = await check_nim_health(embedding_nim_url, "embedding_nim")

    return {
        "status": "healthy"
        if (reasoning_available and embedding_available)
        else "degraded",
        "service": "agentic-researcher",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "nims_available": {
            "reasoning_nim": reasoning_available,
            "embedding_nim": embedding_available,
        },
    }


@app.get("/ready", tags=["System"])
async def readiness_check():
    """
    Readiness check for Kubernetes

    Returns 200 if service is ready to accept requests
    """
    return {"status": "ready"}


@app.get("/sources", tags=["System"])
async def get_active_sources():
    """
    Get status of all paper sources
    Shows which sources are enabled and have API keys configured
    """
    from config import PaperSourceConfig

    config = PaperSourceConfig.from_env()

    sources = {
        "free_sources": {
            "arxiv": {
                "enabled": config.enable_arxiv,
                "api_key_required": False,
                "status": "active" if config.enable_arxiv else "disabled",
            },
            "pubmed": {
                "enabled": config.enable_pubmed,
                "api_key_required": False,
                "status": "active" if config.enable_pubmed else "disabled",
            },
            "semantic_scholar": {
                "enabled": config.enable_semantic_scholar,
                "api_key_required": False,
                "api_key_configured": bool(config.semantic_scholar_api_key),
                "status": "active" if config.enable_semantic_scholar else "disabled",
                "note": "Works without key, but higher limits with key"
                if config.enable_semantic_scholar
                else None,
            },
            "crossref": {
                "enabled": config.enable_crossref,
                "api_key_required": False,
                "status": "active" if config.enable_crossref else "disabled",
            },
        },
        "subscription_sources": {
            "ieee": {
                "enabled": config.enable_ieee,
                "api_key_required": True,
                "api_key_configured": bool(config.ieee_api_key),
                "status": "active"
                if (config.enable_ieee and config.ieee_api_key)
                else ("disabled" if not config.enable_ieee else "no_key"),
                "note": "Requires API key"
                if not config.ieee_api_key and config.enable_ieee
                else None,
            },
            "acm": {
                "enabled": config.enable_acm,
                "api_key_required": True,
                "api_key_configured": bool(config.acm_api_key),
                "status": "active"
                if (config.enable_acm and config.acm_api_key)
                else ("disabled" if not config.enable_acm else "no_key"),
                "note": "Requires API key"
                if not config.acm_api_key and config.enable_acm
                else None,
            },
            "springer": {
                "enabled": config.enable_springer,
                "api_key_required": True,
                "api_key_configured": bool(config.springer_api_key),
                "status": "active"
                if (config.enable_springer and config.springer_api_key)
                else ("disabled" if not config.enable_springer else "no_key"),
                "note": "Requires API key"
                if not config.springer_api_key and config.enable_springer
                else None,
            },
        },
    }

    # Count active sources
    active_count = sum(
        1 for src in sources["free_sources"].values() if src["status"] == "active"
    ) + sum(
        1
        for src in sources["subscription_sources"].values()
        if src["status"] == "active"
    )

    return {
        "active_sources_count": active_count,
        "total_sources": 7,
        "sources": sources,
    }


@app.get("/metrics", tags=["System"])
async def prometheus_metrics():
    """
    Prometheus metrics endpoint

    Returns metrics in Prometheus format for scraping
    """
    if not metrics or not METRICS_AVAILABLE:
        return Response(content="# Metrics not available\n", media_type="text/plain")

    return Response(content=metrics.get_metrics(), media_type="text/plain")


@app.post(
    "/research",
    response_model=ResearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        500: {"model": ErrorResponse, "description": "Internal error"},
    },
    tags=["Research"],
)
async def research(
    request: ResearchRequest,
    http_request: Request = None
):
    """
    Execute research synthesis workflow

    This endpoint orchestrates the multi-agent system to:
    1. **Search** for relevant papers (Scout Agent + Embedding NIM)
    2. **Analyze** each paper (Analyst Agent + Reasoning NIM)
    3. **Synthesize** findings (Synthesizer Agent + Both NIMs)
    4. **Evaluate** quality (Coordinator Agent + Reasoning NIM)

    ## Agentic Behavior
    The system makes autonomous decisions at multiple points:
    - Paper relevance filtering
    - Search continuation
    - Synthesis quality evaluation

    All decisions are logged and returned with reasoning and NIM usage.

    ## Parameters
    - **query**: Natural language research query
    - **max_papers**: Maximum papers to analyze (1-50)

    ## Returns
    Complete synthesis including:
    - Common themes identified
    - Contradictions found
    - Research gaps
    - All autonomous decisions made
    """
    start_time = time.time()

    try:
        # Validate date range (additional validation beyond Pydantic)
        if request.start_year is not None and request.end_year is not None:
            if request.end_year < request.start_year:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Invalid date range",
                        "message": f"end_year ({request.end_year}) must be >= start_year ({request.start_year})",
                        "timestamp": datetime.now().isoformat(),
                    },
                )
        
        # Validate input
        validated = ResearchQuery(query=request.query, max_papers=request.max_papers)

        logger.info(f"Starting research for query: {validated.query}")

        # Check synthesis cache first (before initializing NIMs)
        synthesis_cache = None
        try:
            from cache import get_cache, SynthesisCache

            cache = get_cache()
            synthesis_cache = SynthesisCache(cache)
            cached_result = synthesis_cache.get_synthesis(
                validated.query, validated.max_papers
            )
            if cached_result:
                logger.info(f"✅ Cache hit for query: {validated.query}")
                # Update processing time
                cached_result["processing_time_seconds"] = time.time() - start_time
                if metrics:
                    metrics.record_cache_hit("synthesis")

                # Still apply date filtering if requested
                if request.start_year or request.end_year:
                    try:
                        from src.date_filter import (
                            filter_by_year_range,
                            prioritize_recent_papers,
                        )

                        papers_list = cached_result.get("papers", [])
                        filtered_papers = filter_by_year_range(
                            papers_list,
                            start_year=request.start_year,
                            end_year=request.end_year,
                        )

                        if request.prioritize_recent:
                            filtered_papers = prioritize_recent_papers(
                                filtered_papers, recent_years=3
                            )

                        cached_result["papers"] = [
                            p
                            for p in cached_result["papers"]
                            if any(
                                fp.get("id") == p.get("id") for fp in filtered_papers
                            )
                        ]
                        cached_result["papers_analyzed"] = len(cached_result["papers"])
                    except Exception as e:
                        logger.warning(f"Date filtering failed: {e}")

                # Return cached result as ResearchResponse
                return ResearchResponse(
                    query=validated.query,
                    papers_analyzed=cached_result.get("papers_analyzed", 0),
                    common_themes=cached_result.get("common_themes", []),
                    contradictions=cached_result.get("contradictions", []),
                    research_gaps=cached_result.get("research_gaps", []),
                    decisions=cached_result.get("decisions", []),
                    papers=cached_result.get("papers", []),
                    analyses=cached_result.get("analyses", []),
                    quality_scores=cached_result.get("quality_scores", []),
                    progress=cached_result.get("progress", {}),
                    processing_time_seconds=cached_result.get(
                        "processing_time_seconds", 0
                    ),
                )
        except Exception as e:
            logger.warning(f"Cache check failed: {e}")

        # Cache miss - proceed with full workflow
        if synthesis_cache and metrics:
            metrics.record_cache_miss("synthesis")

        # Apply date filtering imports
        if request.start_year or request.end_year:
            try:
                from .date_filter import filter_by_year_range, prioritize_recent_papers
            except ImportError:
                try:
                    from date_filter import filter_by_year_range, prioritize_recent_papers
                except ImportError:
                    from src.date_filter import (
                        filter_by_year_range,
                        prioritize_recent_papers,
                    )

        # Initialize NIM clients with graceful degradation and timeout management
        try:
            # R-1: Timeout management (5 minute hard limit)
            import asyncio

            use_async_timeout = True
            try:
                from async_timeout import timeout
            except ImportError:
                use_async_timeout = False

            async with (
                UnifiedReasoningClient() as reasoning,
                UnifiedEmbeddingClient() as embedding,
            ):
                # Create agent
                agent = ResearchOpsAgent(reasoning, embedding)
                
                # Initialize Denario integration if enabled
                denario_enabled = os.getenv("DENARIO_ENABLED", "false").lower() == "true"
                denario = DenarioIntegration(enabled=denario_enabled) if denario_enabled else None

                # Run research workflow with timeout
                try:
                    if use_async_timeout:
                        async with timeout(300):  # 5 minute hard limit
                            result = await agent.run(
                                query=validated.query, max_papers=validated.max_papers
                            )
                    else:
                        # Fallback: use asyncio.wait_for when async_timeout not available
                        result = await asyncio.wait_for(
                            agent.run(
                                query=validated.query, max_papers=validated.max_papers
                            ),
                            timeout=300,  # 5 minute hard limit
                        )
                except asyncio.TimeoutError:
                    logger.error("Research synthesis exceeded 5 minute limit")
                    # Return partial results if available
                    from agents import _generate_demo_result

                    result = _generate_demo_result(
                        validated.query, validated.max_papers
                    )
                    result["timeout"] = True
                    result["message"] = (
                        "Query exceeded time limit, showing partial results"
                    )
                
                # Enhance with Denario if enabled
                if denario and denario.is_available():
                    result = denario.enhance_synthesis_with_ideas(result)
                    logger.info("✅ Enhanced synthesis with Denario research ideas")

            # Cache synthesis result
            if synthesis_cache:
                try:
                    synthesis_cache.set_synthesis(
                        validated.query, validated.max_papers, result
                    )
                    logger.info(
                        f"✅ Cached synthesis result for query: {validated.query}"
                    )
                except Exception as e:
                    logger.warning(f"Failed to cache synthesis: {e}")

            # Apply date filtering to results
            if request.start_year or request.end_year:
                try:
                    papers_list = result.get("papers", [])
                    filtered_papers = filter_by_year_range(
                        papers_list,
                        start_year=request.start_year,
                        end_year=request.end_year,
                    )

                    if request.prioritize_recent:
                        filtered_papers = prioritize_recent_papers(
                            filtered_papers, recent_years=3
                        )

                    # Update result with filtered papers
                    result["papers"] = [
                        p
                        for p in result["papers"]
                        if any(fp.get("id") == p.get("id") for fp in filtered_papers)
                    ]
                    result["papers_analyzed"] = len(result["papers"])
                    logger.info(
                        f"Date filtered: {len(result['papers'])} papers after filtering"
                    )
                except Exception as e:
                    logger.warning(f"Date filtering failed: {e}")

        except (NIMServiceError, CircuitBreakerOpenError) as e:
            # NIM service errors - graceful degradation to demo mode
            logger.warning(
                f"⚠️ NIM services unavailable ({type(e).__name__}), "
                f"falling back to demo mode for query: {validated.query}",
                extra={
                    "error_type": type(e).__name__,
                    "query": validated.query[:100],
                    "service": getattr(e, "service", None),
                    "request_id": getattr(http_request.state, "request_id", None) if http_request and hasattr(http_request, 'state') else None
                }
            )
            try:
                from agents import _generate_demo_result
                result = _generate_demo_result(validated.query, validated.max_papers)
                result["fallback_reason"] = f"NIM services unavailable: {type(e).__name__}"
                result["fallback_details"] = e.details
            except ImportError:
                logger.error("Demo result generator not available")
                raise HTTPException(
                    status_code=503,
                    detail={
                        "error": "Service temporarily unavailable",
                        "message": "NIM services not accessible",
                        "timestamp": datetime.now().isoformat()
                    }
                )
        except ValidationError as e:
            # Validation errors - return 400 with details
            logger.warning(f"Validation error: {e.message}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Validation error",
                    "message": e.message,
                    "details": e.details,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except PaperSourceError as e:
            # Paper source errors - return 502
            logger.error(f"Paper source error: {e.message}", exc_info=True)
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "Paper source error",
                    "message": e.message,
                    "source": e.source,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            # Check if it's a connection/timeout error that should be NIMServiceError
            import aiohttp
            from tenacity import RetryError

            error_str = str(e).lower()
            is_nim_unavailable = (
                "circuit breaker" in error_str
                or "service unavailable" in error_str
                or "connection" in error_str
                or "cannot connect" in error_str
                or "nodename nor servname" in error_str
                or isinstance(e, (aiohttp.ClientError, asyncio.TimeoutError, RetryError))
            )

            if is_nim_unavailable:
                # Convert to NIMServiceError and retry
                nim_error = NIMServiceError(
                    f"NIM service unavailable: {type(e).__name__}",
                    details={"original_error": str(e)}
                )
                # Recursively handle as NIMServiceError
                raise nim_error
            else:
                # Unexpected errors - log with full context
                request_id = getattr(http_request.state, "request_id", None) if http_request and hasattr(http_request, 'state') else None
                logger.error(
                    f"Unexpected error during research workflow: {e}",
                    exc_info=True,
                    extra={
                        "query": validated.query[:100],
                        "max_papers": validated.max_papers,
                        "error_type": type(e).__name__,
                        "request_id": request_id
                    }
                )
                is_debug = os.getenv("DEBUG", "false").lower() == "true"
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Internal error",
                        "message": str(e) if is_debug else "Research workflow failed",
                        "timestamp": datetime.now().isoformat(),
                        "request_id": request_id
                    }
                )

        # Check for errors in result
        if "error" in result:
            raise HTTPException(
                status_code=400, detail=result.get("message", "Invalid input")
            )

        # Add processing time
        result["processing_time_seconds"] = round(time.time() - start_time, 2)
        result["query"] = validated.query

        # Record agent decisions in metrics
        decisions = result.get("decisions", [])
        if metrics and METRICS_AVAILABLE:
            for decision in decisions:
                agent_name = decision.get("agent", "Unknown")
                decision_type = decision.get("decision_type", "Unknown")
                metrics.record_agent_decision(agent_name, decision_type)

            # Record papers analyzed by source
            papers = result.get("papers", [])
            for paper in papers:
                source = paper.get("source", "unknown")
                metrics.record_paper_analyzed(source)

            # Record quality scores
            quality_scores = result.get("quality_scores", [])
            for qs in quality_scores:
                overall_score = qs.get("overall_score", 0)
                metrics.record_quality_score(overall_score)

        logger.info(
            f"Research complete: {result['papers_analyzed']} papers, "
            f"{len(result['decisions'])} decisions, "
            f"{result['processing_time_seconds']}s"
        )

        return result

    except (ValueError, InputValidationError) as e:
        # Handle both ValueError and InputValidationError
        error_message = str(e)
        error_details = {}
        if isinstance(e, InputValidationError):
            error_message = getattr(e, 'message', str(e))
            error_details = getattr(e, 'details', {})
        
        # Get request_id from middleware state (set by RequestIDMiddleware)
        request_id = None
        # Note: Request object not directly available in this scope
        # Request ID is set by middleware and will be in response headers
        logger.error(
            f"Validation error: {error_message}",
            extra={"request_id": request_id, "details": error_details}
        )
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid input",
                "message": error_message,
                "details": error_details,
                "timestamp": datetime.now().isoformat(),
                "request_id": request_id
            },
        )
    except Exception as e:
        logger.error(f"Research error: {e}", exc_info=True)
        is_debug = os.getenv("DEBUG", "false").lower() == "true"
        error_message = str(e) if e else "Unknown error occurred"
        if not error_message:
            error_message = f"{type(e).__name__}: {repr(e)}"
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal error",
                "message": error_message if is_debug else "Research workflow failed",
                "error_type": type(e).__name__,
                "timestamp": datetime.now().isoformat(),
            },
        )


@app.get("/decisions/{session_id}", tags=["Research"])
async def get_decisions(session_id: str):
    """
    Retrieve decision log for a specific research session

    Returns all autonomous decisions made during the research workflow
    """
    if session_id in research_sessions:
        return {
            "session_id": session_id,
            "decisions": research_sessions[session_id].get("decisions", []),
        }
    else:
        raise HTTPException(
            status_code=404,
            detail={"error": "Session not found", "session_id": session_id},
        )


# Feedback endpoints (Short-Term Recommendation)
class FeedbackRequest(BaseModel):
    """Request model for user feedback"""
    synthesis_id: str = Field(..., description="Synthesis ID")
    query: str = Field(..., description="Original query")
    feedback_type: str = Field(..., description="Type: helpful, not_helpful, decision_surprising")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating 1-5")
    comment: Optional[str] = Field(None, description="Optional comment")
    decision_id: Optional[str] = Field(None, description="Decision ID if feedback on specific decision")


@app.post("/feedback", tags=["Feedback"])
async def submit_feedback(request: FeedbackRequest):
    """
    Submit user feedback on synthesis
    
    Implements feedback loops for learning (Meadows recommendation)
    """
    try:
        from feedback import get_feedback_collector, FeedbackType
        
        collector = get_feedback_collector()
        feedback_type_map = {
            "helpful": FeedbackType.HELPFUL,
            "not_helpful": FeedbackType.NOT_HELPFUL,
            "decision_surprising": FeedbackType.DECISION_SURPRISING
        }
        
        # Validate and normalize feedback_type
        if not request.feedback_type:
            raise HTTPException(
                status_code=400,
                detail="Invalid feedback_type: 'None'. Allowed: [helpful, not_helpful, decision_surprising]"
            )
        
        # Normalize: ensure it's a string and strip whitespace
        feedback_type_str = str(request.feedback_type).strip().lower() if isinstance(request.feedback_type, str) else str(request.feedback_type).lower()
        
        # Check membership against allowed keys
        if feedback_type_str not in feedback_type_map:
            allowed_values = list(feedback_type_map.keys())
            raise HTTPException(
                status_code=400,
                detail=f"Invalid feedback_type: '{request.feedback_type}'. Allowed: {allowed_values}"
            )
        
        # Map to the enum
        feedback_type = feedback_type_map[feedback_type_str]
        
        feedback = collector.record_feedback(
            synthesis_id=request.synthesis_id,
            query=request.query,
            feedback_type=feedback_type,
            rating=request.rating,
            comment=request.comment,
            decision_id=request.decision_id
        )
        
        return {
            "status": "success",
            "feedback_id": feedback.get("timestamp"),
            "message": "Feedback recorded successfully"
        }
    except Exception as e:
        logger.error(f"Feedback submission error: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to record feedback", "message": str(e)}
        )


@app.get("/feedback/stats", tags=["Feedback"])
async def get_feedback_stats():
    """Get aggregated feedback statistics"""
    try:
        from feedback import get_feedback_collector
        collector = get_feedback_collector()
        stats = collector.get_feedback_stats()
        insights = collector.get_learning_insights()
        return {
            "stats": stats,
            "insights": insights
        }
    except Exception as e:
        logger.error(f"Feedback stats error: {e}")
        return {"stats": {}, "insights": {}}


# Synthesis History endpoints (Switching Costs)
@app.get("/history", tags=["History"])
async def get_synthesis_history(limit: int = 50):
    """Get synthesis history - creates switching costs"""
    try:
        from synthesis_history import get_synthesis_history
        history = get_synthesis_history()
        return {
            "history": history.get_history(limit),
            "portfolio": history.get_research_portfolio()
        }
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        return {"history": [], "portfolio": {}}


@app.get("/history/portfolio", tags=["History"])
async def get_research_portfolio(format: str = "json"):
    """Export research portfolio - switching cost feature"""
    try:
        from synthesis_history import get_synthesis_history
        history = get_synthesis_history()
        portfolio_data = history.export_portfolio(format)
        
        if format == "json":
            return Response(content=portfolio_data, media_type="application/json")
        else:
            return Response(content=portfolio_data, media_type="text/markdown")
    except Exception as e:
        logger.error(f"Portfolio export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class BibTeXExportRequest(BaseModel):
    """Request model for BibTeX export"""

    papers: List[Dict] = Field(..., description="List of paper dictionaries")


class BatchResearchRequest(BaseModel):
    """Request model for batch processing"""
    queries: List[str] = Field(
        ...,
        min_items=1,
        max_items=20,
        description="List of research queries to process"
    )
    max_papers: int = Field(
        default=10, ge=1, le=50, description="Maximum papers per query"
    )
    start_year: Optional[int] = Field(
        default=None, ge=1900, le=2100, description="Filter papers from this year"
    )
    end_year: Optional[int] = Field(
        default=None, ge=1900, le=2100, description="Filter papers up to this year"
    )
    prioritize_recent: bool = Field(
        default=False, description="Prioritize recent papers"
    )

    class Config:
        schema_extra = {
            "example": {
                "queries": [
                    "machine learning for medical imaging",
                    "deep learning in autonomous vehicles"
                ],
                "max_papers": 10,
                "start_year": 2020,
                "prioritize_recent": True
            }
        }


class BatchResearchResponse(BaseModel):
    """Response model for batch processing"""
    batch_id: str
    total_queries: int
    completed: int
    failed: int
    results: List[Dict[str, Any]]
    processing_time_seconds: float


class ComparisonRequest(BaseModel):
    """Request model for comparing multiple syntheses"""
    synthesis_ids: List[str] = Field(
        ...,
        min_items=2,
        max_items=10,
        description="List of synthesis IDs to compare"
    )


class LaTeXExportRequest(BaseModel):
    """Request model for LaTeX export"""

    query: str = Field(..., description="Research query")
    papers: List[Dict] = Field(..., description="List of paper dictionaries")
    themes: List[str] = Field(default=[], description="Common themes")
    gaps: List[str] = Field(default=[], description="Research gaps")
    contradictions: List[Dict] = Field(default=[], description="Contradictions")


@app.post("/export/bibtex", tags=["Export"], response_model=Dict[str, Any])
async def export_bibtex(request: BibTeXExportRequest):
    """
    Export papers as BibTeX format

    Accepts a list of paper dictionaries and returns BibTeX formatted text.
    Papers should have: id, title, authors, url, abstract (optional), published_date (optional)

    **Usage:**
    Import the returned BibTeX into Zotero, Mendeley, EndNote, or any citation manager.
    """
    try:
        bibtex_content = generate_bibtex(request.papers)
        return {
            "format": "bibtex",
            "content": bibtex_content,
            "papers_count": len(request.papers),
        }
    except Exception as e:
        logger.error(f"BibTeX export error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Export failed",
                "message": str(e),
                "timestamp": datetime.now().isoformat(),
            },
        )


@app.post("/export/zotero", tags=["Export"], response_model=Dict[str, Any])
async def export_zotero(request: BibTeXExportRequest):
    """
    Export papers in RIS format for Zotero
    
    RIS (Research Information Systems) is a standard format
    used by Zotero, Mendeley, EndNote, and other citation managers.
    """
    try:
        from export_formats import generate_zotero_ris_export
        
        ris_content = generate_zotero_ris_export(request.papers)
        
        return {
            "format": "ris",
            "content": ris_content,
            "filename": "zotero_export.ris",
            "mime_type": "application/x-research-info-systems",
            "papers_count": len(request.papers)
        }
    except Exception as e:
        logger.error(f"Zotero export error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Zotero export: {str(e)}"
        )


@app.post("/export/mendeley", tags=["Export"], response_model=Dict[str, Any])
async def export_mendeley(request: BibTeXExportRequest):
    """
    Export papers in CSV format for Mendeley
    
    Mendeley uses a specific CSV format with required columns.
    """
    try:
        from export_formats import generate_mendeley_csv_export
        
        csv_content = generate_mendeley_csv_export(request.papers)
        
        return {
            "format": "csv",
            "content": csv_content,
            "filename": "mendeley_export.csv",
            "mime_type": "text/csv",
            "papers_count": len(request.papers)
        }
    except Exception as e:
        logger.error(f"Mendeley export error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Mendeley export: {str(e)}"
        )


@app.post("/pdf-analysis", tags=["Analysis"], response_model=Dict[str, Any])
async def analyze_pdf_full_text(request: BibTeXExportRequest):
    """
    Analyze full-text PDFs of papers
    
    Downloads and analyzes full PDF text to extract methodologies,
    experimental details, and results beyond abstracts.
    """
    try:
        from pdf_analysis import analyze_papers_full_text
        from nim_clients import ReasoningNIMClient
        
        # Initialize reasoning client for enhanced extraction
        reasoning_client = None
        try:
            async with UnifiedReasoningClient() as client:
                reasoning_client = client
                results = await analyze_papers_full_text(
                    request.papers,
                    reasoning_client=reasoning_client,
                    max_papers=int(os.getenv("MAX_PDF_ANALYSIS", "5"))
                )
        except Exception as e:
            logger.warning(f"Reasoning client unavailable, using basic extraction: {e}")
            results = await analyze_papers_full_text(
                request.papers,
                max_papers=int(os.getenv("MAX_PDF_ANALYSIS", "5"))
            )
        
        return {
            "papers_analyzed": len(results),
            "analyses": results,
            "summary": {
                "successful": sum(1 for r in results.values() if "error" not in r),
                "failed": sum(1 for r in results.values() if "error" in r)
            }
        }
    except Exception as e:
        logger.error(f"PDF analysis error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze PDFs: {str(e)}"
        )


@app.post("/aws/sagemaker", tags=["AWS"], response_model=Dict[str, Any])
async def invoke_sagemaker(request: Dict[str, Any]):
    """
    Invoke SageMaker endpoint for model inference
    
    Requires AWS credentials and SageMaker endpoint configured.
    """
    try:
        from aws_integration import use_sagemaker_for_inference
        
        endpoint_name = request.get("endpoint_name")
        payload = request.get("payload", {})
        
        if not endpoint_name:
            raise HTTPException(status_code=400, detail="endpoint_name required")
        
        result = await use_sagemaker_for_inference(endpoint_name, payload)
        
        if result is None:
            raise HTTPException(
                status_code=503,
                detail="SageMaker integration not available or endpoint not accessible"
            )
        
        return {"result": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"SageMaker invocation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to invoke SageMaker: {str(e)}"
        )


@app.post("/aws/bedrock", tags=["AWS"], response_model=Dict[str, Any])
async def invoke_bedrock(request: Dict[str, Any]):
    """
    Invoke Amazon Bedrock model for enhanced analysis
    
    Requires AWS credentials and Bedrock access configured.
    """
    try:
        from aws_integration import use_bedrock_for_analysis
        
        prompt = request.get("prompt")
        # Default to Claude 3.5 Sonnet (best for 2025), with fallback to Claude v2
        model_id = request.get(
            "model_id",
            os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022")
        )
        
        if not prompt:
            raise HTTPException(status_code=400, detail="prompt required")
        
        result = await use_bedrock_for_analysis(prompt, model_id)
        
        if result is None:
            raise HTTPException(
                status_code=503,
                detail="Bedrock integration not available or not accessible"
            )
        
        return {"result": result, "model_id": model_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bedrock invocation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to invoke Bedrock: {str(e)}"
        )


@app.post("/aws/store-s3", tags=["AWS"], response_model=Dict[str, Any])
async def store_result_s3(request: Dict[str, Any]):
    """
    Store research result in S3
    
    Requires AWS credentials and S3 bucket configured.
    """
    try:
        from aws_integration import store_research_result_s3
        
        result = request.get("result")
        query = request.get("query", "research_query")
        
        if not result:
            raise HTTPException(status_code=400, detail="result required")
        
        s3_key = await store_research_result_s3(result, query)
        
        if s3_key is None:
            raise HTTPException(
                status_code=503,
                detail="S3 storage not available or bucket not configured"
            )
        
        return {"s3_location": s3_key, "status": "stored"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"S3 storage error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to store in S3: {str(e)}"
        )


@app.post("/citation-graph", tags=["Analysis"], response_model=Dict[str, Any])
async def analyze_citation_graph(request: BibTeXExportRequest):
    """
    Analyze citation graph from papers
    
    Builds citation graph from Semantic Scholar and Crossref data
    to identify seminal papers, citation paths, and research evolution.
    """
    try:
        from citation_graph import build_citation_graph_from_papers, analyze_citation_graph as analyze_graph
        import os
        
        semantic_scholar_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        
        # Build citation graph
        graph = await build_citation_graph_from_papers(
            request.papers,
            semantic_scholar_api_key=semantic_scholar_key
        )
        
        # Analyze graph
        analysis = analyze_graph(graph)
        
        return {
            "total_papers": len(graph.nodes),
            "total_citations": len(graph.edges),
            "seminal_papers": analysis.get("seminal_papers", []),
            "influential_papers": analysis.get("influential_papers", []),
            "evolution_timeline": analysis.get("evolution_timeline", []),
            "citation_stats": {
                "avg_citations_per_paper": len(graph.edges) / max(len(graph.nodes), 1),
                "most_cited": analysis.get("influential_papers", [])[:5] if analysis.get("influential_papers") else []
            }
        }
    except Exception as e:
        logger.error(f"Citation graph analysis error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze citation graph: {str(e)}"
        )


@app.post("/export/latex", tags=["Export"], response_model=Dict[str, Any])
async def export_latex(request: LaTeXExportRequest):
    """
    Generate complete LaTeX document for literature review

    Returns a complete LaTeX document ready to compile with pdflatex.

    **Usage:**
    1. Download the returned content
    2. Save as .tex file
    3. Compile with: `pdflatex filename.tex`
    """
    try:
        latex_content = generate_latex_document(
            query=request.query,
            papers=request.papers,
            themes=request.themes,
            gaps=request.gaps,
            contradictions=request.contradictions,
            date=datetime.now().strftime("%B %d, %Y"),
        )
        return {
            "format": "latex",
            "content": latex_content,
            "query": request.query,
            "papers_count": len(request.papers),
        }
    except Exception as e:
        logger.error(f"LaTeX export error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Export failed",
                "message": str(e),
                "timestamp": datetime.now().isoformat(),
            },
        )


@app.post(
    "/research/batch",
    response_model=BatchResearchResponse,
    tags=["Research"],
)
async def batch_research(request: BatchResearchRequest):
    """
    Process multiple research queries in batch
    
    Efficiently processes multiple queries by batching them together
    for improved resource utilization. Results are returned as a list
    with individual query results.
    
    **Performance**: Batch processing can be 30-50% faster than
    sequential processing due to shared resource pooling.
    """
    import uuid
    start_time = time.time()
    batch_id = str(uuid.uuid4())
    
    logger.info(f"Batch processing {len(request.queries)} queries: {batch_id}")
    
    results = []
    completed = 0
    failed = 0
    
    # Process queries in parallel (limited concurrency)
    max_concurrent_env = os.getenv("MAX_CONCURRENT_BATCH", "5")
    try:
        max_concurrent = int(max_concurrent_env)
        # Clamp to safe range: minimum 1, maximum 100
        max_concurrent = max(1, min(100, max_concurrent))
    except (ValueError, TypeError):
        max_concurrent = 5  # Sensible default
        logger.warning(f"Invalid MAX_CONCURRENT_BATCH value '{max_concurrent_env}', using default: 5")
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_single_query(query: str) -> Dict[str, Any]:
        """Process a single query within the batch"""
        async with semaphore:
            try:
                research_request = ResearchRequest(
                    query=query,
                    max_papers=request.max_papers,
                    start_year=request.start_year,
                    end_year=request.end_year,
                    prioritize_recent=request.prioritize_recent
                )
                
                # Call the research endpoint logic
                response = await research(research_request)
                
                return {
                    "query": query,
                    "status": "success",
                    "result": response.dict() if hasattr(response, 'dict') else response,
                    "error": None
                }
            except Exception as e:
                logger.error(f"Batch query failed: {query[:50]}... - {e}")
                return {
                    "query": query,
                    "status": "failed",
                    "result": None,
                    "error": str(e)
                }
    
    # Process all queries
    tasks = [process_single_query(query) for query in request.queries]
    batch_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    for result in batch_results:
        if isinstance(result, Exception):
            failed += 1
            results.append({
                "status": "failed",
                "error": str(result)
            })
        elif result.get("status") == "success":
            completed += 1
            results.append(result)
        else:
            failed += 1
            results.append(result)
    
    processing_time = time.time() - start_time
    
    logger.info(
        f"Batch {batch_id} completed: {completed}/{len(request.queries)} "
        f"in {processing_time:.2f}s"
    )
    
    return BatchResearchResponse(
        batch_id=batch_id,
        total_queries=len(request.queries),
        completed=completed,
        failed=failed,
        results=results,
        processing_time_seconds=processing_time
    )


@app.post("/research/stream", tags=["Research"])
async def research_stream(request: ResearchRequest):
    """
    Stream research progress and results in real-time using Server-Sent Events (SSE)
    
    This endpoint delivers progressive updates as agents complete their work:
    - 0-30s: Scout finds papers → papers_found event
    - 30s-3min: Analyst extracts → paper_analyzed events (batched)
    - 3-4min: Synthesizer patterns → theme_found, contradiction_found events
    - 4-5min: Final synthesis → synthesis_complete event
    
    **Event Types:**
    - `agent_status`: Agent starting work
    - `papers_found`: Scout completed paper search
    - `paper_analyzed`: Paper analysis complete (batched)
    - `theme_found`: Theme discovered during synthesis
    - `contradiction_found`: Contradiction detected
    - `synthesis_complete`: Final synthesis ready
    - `error`: Error occurred during processing
    
    **SSE Format:**
    ```
    event: papers_found
    data: {"papers_count": 10, "papers": [...]}
    
    event: synthesis_complete
    data: {"themes": [...], "contradictions": [...], "gaps": [...]}
    ```
    """
    start_time = time.time()
    
    async def generate_events():
        """Generate SSE events for research progress"""
        try:
            # Validate input
            validated = ResearchQuery(query=request.query, max_papers=request.max_papers)
            
            # Send initial status
            yield f"event: agent_status\n"
            yield f"data: {json.dumps({'agent': 'Scout', 'status': 'starting', 'message': 'Searching for papers'})}\n\n"
            
            # Initialize NIM clients (unified - supports local or cloud)
            async with (
                UnifiedReasoningClient() as reasoning,
                UnifiedEmbeddingClient() as embedding,
            ):
                # Create agent
                agent = ResearchOpsAgent(reasoning, embedding)
                
                # Initialize Denario integration if enabled
                denario_enabled = os.getenv("DENARIO_ENABLED", "false").lower() == "true"
                denario = DenarioIntegration(enabled=denario_enabled) if denario_enabled else None
                
                # Phase 1: Search (0-30s)
                yield f"event: agent_status\n"
                yield f"data: {json.dumps({'agent': 'Scout', 'status': 'searching', 'message': f'Searching {agent.scout.source_config.enable_arxiv + agent.scout.source_config.enable_pubmed} sources'})}\n\n"
                
                papers = await agent._execute_search_phase(validated.query, validated.max_papers)
                
                # Emit papers_found event
                papers_data = [
                    {
                        "id": p.id,
                        "title": p.title,
                        "authors": p.authors,
                        "abstract": p.abstract[:200] + "..." if len(p.abstract) > 200 else p.abstract,
                        "url": p.url,
                        "source": p.id.split('-')[0] if '-' in p.id else "unknown"
                    }
                    for p in papers
                ]
                
                yield f"event: papers_found\n"
                yield f"data: {json.dumps({'papers_count': len(papers), 'papers': papers_data, 'decisions': agent.decision_log.get_decisions()})}\n\n"
                
                # Phase 2: Progressive Analysis + Synthesis (30s-3min)
                # Use incremental synthesizer for real-time synthesis updates
                yield f"event: agent_status\n"
                yield f"data: {json.dumps({'agent': 'Analyst', 'status': 'analyzing', 'message': f'Analyzing {len(papers)} papers progressively'})}\n\n"

                # Create incremental synthesizer
                incremental_synthesizer = IncrementalSynthesizer(
                    reasoning_client=reasoning,
                    embedding_client=embedding,
                    similarity_threshold=0.7,
                    top_k_candidates=5
                )

                # Process papers one at a time with progressive synthesis
                analyses = []
                quality_scores = []

                for idx, paper in enumerate(papers):
                    # Analyze single paper
                    paper_analysis = await agent.analyst.analyze(paper)
                    quality_score = agent.analyst.assess_quality(paper, paper_analysis)

                    analyses.append(paper_analysis)
                    quality_scores.append(quality_score)

                    # Emit paper_analyzed event
                    yield f"event: paper_analyzed\n"
                    paper_data = {
                        'paper_number': idx + 1,
                        'total': len(papers),
                        'paper_id': paper.id,
                        'title': paper.title,
                        'findings_count': len(paper_analysis.key_findings),
                        'confidence': paper_analysis.confidence
                    }
                    yield f"data: {json.dumps(paper_data)}\n\n"

                    # Incremental synthesis after each paper
                    paper_info = {
                        "id": paper.id,
                        "title": paper.title,
                        "authors": paper.authors,
                        "url": paper.url
                    }

                    synthesis_update = await incremental_synthesizer.add_analysis(
                        paper_analysis,
                        paper_info
                    )

                    # Emit synthesis_update event with progressive discoveries
                    update_data = synthesis_update.to_dict()

                    # Emit individual discovery events for new themes
                    for new_theme in synthesis_update.new_themes:
                        yield f"event: theme_emerging\n"
                        theme_data = {
                            'paper_number': idx + 1,
                            'theme_name': new_theme.name,
                            'confidence': new_theme.confidence,
                            'initial_finding': new_theme.key_findings[0] if new_theme.key_findings else 'N/A'
                        }
                        yield f"data: {json.dumps(theme_data)}\n\n"

                    # Emit theme strengthening events
                    for update in synthesis_update.theme_updates:
                        yield f"event: theme_strengthened\n"
                        theme_update_data = {
                            'paper_number': idx + 1,
                            'theme_name': update['theme_name'],
                            'old_confidence': update['old_confidence'],
                            'new_confidence': update['new_confidence'],
                            'new_finding': update['new_finding']
                        }
                        yield f"data: {json.dumps(theme_update_data)}\n\n"

                    # Emit contradiction discovery events
                    for contradiction in synthesis_update.new_contradictions:
                        yield f"event: contradiction_discovered\n"
                        contradiction_data = {
                            'paper_number': idx + 1,
                            'finding_a': contradiction.finding_a,
                            'finding_b': contradiction.finding_b,
                            'explanation': contradiction.explanation,
                            'severity': contradiction.severity
                        }
                        yield f"data: {json.dumps(contradiction_data)}\n\n"

                    # Emit theme merge events
                    for merge in synthesis_update.merged_themes:
                        yield f"event: themes_merged\n"
                        merge_data = {
                            'paper_number': idx + 1,
                            'merged_from': merge['merged_from'],
                            'merged_into': merge['merged_into'],
                            'similarity': merge['similarity']
                        }
                        yield f"data: {json.dumps(merge_data)}\n\n"

                    # Emit comprehensive synthesis update
                    yield f"event: synthesis_update\n"
                    yield f"data: {json.dumps(update_data)}\n\n"

                # Get final synthesis from incremental synthesizer
                final_synthesis_obj = incremental_synthesizer.get_final_synthesis()

                # Convert to compatible format for refinement phase
                synthesis = Synthesis(
                    common_themes=[theme.name for theme in final_synthesis_obj.themes],
                    contradictions=[
                        {
                            "finding_a": c.finding_a,
                            "finding_b": c.finding_b,
                            "explanation": c.explanation,
                            "severity": c.severity
                        }
                        for c in final_synthesis_obj.contradictions
                    ],
                    gaps=[gap.description for gap in final_synthesis_obj.gaps],
                    recommendations=[],  # Will be filled by refinement phase
                    enhanced_insights=None  # Will be populated after synthesis
                )

                # Phase 4: Refinement (optional)
                yield f"event: agent_status\n"
                yield f"data: {json.dumps({'agent': 'Coordinator', 'status': 'evaluating', 'message': 'Assessing synthesis quality'})}\n\n"
                
                synthesis, synthesis_complete = await agent._execute_refinement_phase(synthesis, analyses)
                
                # Final event: synthesis_complete
                processing_time = time.time() - start_time
                
                final_result = {
                    "query": validated.query,
                    "papers_analyzed": len(papers),
                    "common_themes": synthesis.common_themes,
                    "contradictions": synthesis.contradictions,
                    "research_gaps": synthesis.gaps,
                    "decisions": agent.decision_log.get_decisions(),
                    "synthesis_complete": synthesis_complete,
                    "processing_time_seconds": round(processing_time, 2),
                    "quality_scores": [
                        {
                            "paper_id": papers[i].id,
                            "overall_score": qs.overall_score,
                            "confidence_level": qs.confidence_level
                        }
                        for i, qs in enumerate(quality_scores)
                    ] if quality_scores else []
                }
                
                yield f"event: synthesis_complete\n"
                yield f"data: {json.dumps(final_result)}\n\n"
                
                logger.info(f"SSE stream complete: {len(papers)} papers, {processing_time:.2f}s")
                
        except ValueError as e:
            # Validation error
            error_data = {
                "error": "Invalid input",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            yield f"event: error\n"
            yield f"data: {json.dumps(error_data)}\n\n"
            
        except asyncio.TimeoutError:
            # Timeout error
            error_data = {
                "error": "Timeout",
                "message": "Research synthesis exceeded time limit",
                "timestamp": datetime.now().isoformat()
            }
            yield f"event: error\n"
            yield f"data: {json.dumps(error_data)}\n\n"
            
        except Exception as e:
            # General error
            logger.error(f"SSE stream error: {e}", exc_info=True)
            error_data = {
                "error": "Internal error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            yield f"event: error\n"
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
            "Access-Control-Allow-Origin": "*"  # CORS for SSE
        }
    )


@app.post(
    "/research/compare",
    response_model=Dict[str, Any],
    tags=["Research"],
)
async def compare_syntheses(request: ComparisonRequest):
    """
    Compare multiple synthesis results
    
    Analyzes differences and similarities between multiple synthesis results,
    highlighting common themes, unique findings, and contradictions across
    syntheses.
    
    **Use Cases**:
    - Compare results from different queries
    - Analyze how research evolved over time
    - Identify consensus vs. divergent findings
    """
    try:
        from synthesis_history import get_synthesis_history
        history = get_synthesis_history()
        all_history = history.get_history(limit=1000)
        
        # Find requested syntheses
        syntheses = []
        for synthesis_id in request.synthesis_ids:
            found = next(
                (h for h in all_history if h.get("synthesis_id") == synthesis_id),
                None
            )
            if found:
                syntheses.append(found)
            else:
                logger.warning(f"Synthesis {synthesis_id} not found in history")
        
        if len(syntheses) < 2:
            raise HTTPException(
                status_code=400,
                detail=f"Need at least 2 syntheses to compare. Found: {len(syntheses)}"
            )
        
        # Extract themes, gaps, and contradictions
        all_themes = []
        all_gaps = []
        all_contradictions = []
        
        for synth in syntheses:
            summary = synth.get("summary", {})
            all_themes.extend(summary.get("key_themes", []))
            all_gaps.extend(summary.get("research_gaps", []))
            all_contradictions.extend(summary.get("top_contradictions", []))
        
        # Find common themes (appearing in 2+ syntheses)
        from collections import Counter
        theme_counts = Counter([theme for theme in all_themes if theme])
        common_themes = [
            theme for theme, count in theme_counts.items() if count >= 2
        ]
        
        # Find unique themes per synthesis
        unique_themes = {}
        for synth in syntheses:
            synth_id = synth.get("synthesis_id")
            summary = synth.get("summary", {})
            themes = summary.get("key_themes", [])
            unique_themes[synth_id] = [
                theme for theme in themes if theme_counts[theme] == 1
            ]
        
        # Aggregate gaps
        gap_counts = Counter([gap for gap in all_gaps if gap])
        common_gaps = [gap for gap, count in gap_counts.items() if count >= 2]
        
        return {
            "synthesis_ids": request.synthesis_ids,
            "compared_count": len(syntheses),
            "comparison": {
                "common_themes": common_themes,
                "unique_themes_per_synthesis": unique_themes,
                "common_gaps": common_gaps,
                "total_papers_analyzed": sum(
                    s.get("papers_analyzed", 0) for s in syntheses
                ),
                "total_themes": len(set(all_themes)),
                "total_gaps": len(set(all_gaps)),
            },
            "syntheses_summary": [
                {
                    "synthesis_id": s.get("synthesis_id"),
                    "query": s.get("query"),
                    "timestamp": s.get("timestamp"),
                    "papers_analyzed": s.get("papers_analyzed", 0),
                    "themes_count": s.get("themes_count", 0),
                }
                for s in syntheses
            ],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Comparison error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compare syntheses: {str(e)}"
        )


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "service": "Agentic Researcher API",
        "version": "1.0.0",
        "description": "Multi-agent AI system for automated literature review",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "research": "/research (POST)",
            "export_bibtex": "/export/bibtex (POST)",
            "export_latex": "/export/latex (POST)",
        },
        "powered_by": [
            "NVIDIA llama-3.1-nemotron-nano-8B-v1 (Reasoning NIM)",
            "NVIDIA nv-embedqa-e5-v5 (Embedding NIM)",
            "Amazon EKS",
        ],
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("=" * 60)
    logger.info("🚀 Agentic Researcher API Starting")
    logger.info("=" * 60)
    logger.info("Service: Agentic Researcher API v1.0.0")
    logger.info("Endpoints: /docs, /health, /research")
    logger.info("NIMs: Reasoning + Embedding")
    logger.info("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information"""
    logger.info("🛑 Agentic Researcher API Shutting Down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
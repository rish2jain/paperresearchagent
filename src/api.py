"""
FastAPI REST API for ResearchOps Agent
Provides HTTP endpoints for the multi-agent research synthesis system
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import asyncio
import time
import logging
import os
from datetime import datetime

from nim_clients import ReasoningNIMClient, EmbeddingNIMClient
from agents import ResearchOpsAgent, ResearchQuery
# Import export functions - works with both script and module execution
try:
    from export_formats import generate_bibtex, generate_latex_document
except ImportError:
    try:
        from .export_formats import generate_bibtex, generate_latex_document
    except ImportError:
        # Last resort: try package import
        from src.export_formats import generate_bibtex, generate_latex_document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ResearchOps Agent API",
    description="Multi-agent AI system for automated literature review synthesis using NVIDIA NIMs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def metrics_and_auth_middleware(request: Request, call_next):
    """Middleware for metrics collection and rate limiting"""
    start_time = time.time()
    
    # Check authentication if required
    if auth_middleware and auth_middleware.require_auth:
        auth_ok, auth_error = auth_middleware.check_auth(request)
        if not auth_ok:
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "message": auth_error}
            )
    
    # Check rate limit
    if auth_middleware:
        allowed, rate_limit_info = auth_middleware.check_rate_limit(request)
        if not allowed:
            return JSONResponse(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Rate limit: {rate_limit_info['limit']} requests per {rate_limit_info['window']} seconds",
                    "reset_time": rate_limit_info['reset_time'],
                    "remaining": rate_limit_info['remaining']
                },
                headers={
                    "X-RateLimit-Limit": str(rate_limit_info['limit']),
                    "X-RateLimit-Remaining": str(rate_limit_info['remaining']),
                    "X-RateLimit-Reset": str(rate_limit_info['reset_time'])
                }
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
            response.headers["X-RateLimit-Limit"] = str(rate_limit_info['limit'])
            response.headers["X-RateLimit-Remaining"] = str(rate_limit_info['remaining'])
            response.headers["X-RateLimit-Reset"] = str(rate_limit_info['reset_time'])
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        if metrics:
            metrics.record_request("error", duration)
            metrics.decrement_active_requests()
        raise


# Request/Response Models
class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, 
                      description="Research query in natural language")
    max_papers: int = Field(default=10, ge=1, le=50,
                           description="Maximum number of papers to analyze")
    start_year: Optional[int] = Field(default=None, ge=1900, le=2100,
                                     description="Filter papers from this year onwards")
    end_year: Optional[int] = Field(default=None, ge=1900, le=2100,
                                   description="Filter papers up to this year")
    prioritize_recent: bool = Field(default=False,
                                    description="Prioritize recent papers (last 3 years)")

    class Config:
        schema_extra = {
            "example": {
                "query": "machine learning for medical imaging",
                "max_papers": 10,
                "start_year": 2020,
                "end_year": 2024,
                "prioritize_recent": True
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
                    "Transfer learning and domain adaptation techniques"
                ],
                "contradictions": [
                    {
                        "paper1": "Paper A",
                        "claim1": "Claims X",
                        "paper2": "Paper B",
                        "claim2": "Claims Y",
                        "conflict": "Contradictory results"
                    }
                ],
                "research_gaps": [
                    "Limited studies on multi-modal fusion",
                    "Gap in longitudinal prediction studies"
                ],
                "decisions": [
                    {
                        "timestamp": "2025-01-01T12:00:00",
                        "agent": "Scout",
                        "decision_type": "RELEVANCE_FILTERING",
                        "decision": "ACCEPTED 12/25 papers",
                        "reasoning": "Applied relevance threshold...",
                        "nim_used": "nv-embedqa-e5-v5 (Embedding NIM)",
                        "metadata": {}
                    }
                ],
                "synthesis_complete": True,
                "processing_time_seconds": 45.2
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


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint to verify service is running
    
    Returns service status and availability of NIMs
    """
    async def check_nim_health(base_url: str) -> bool:
        """Check if NIM is actually responding"""
        try:
            import aiohttp
            timeout = aiohttp.ClientTimeout(total=5)  # Quick check
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{base_url}/v1/health/live") as response:
                    return response.status == 200
        except:
            return False
    
    # Check actual NIM availability
    reasoning_nim_url = os.getenv(
        "REASONING_NIM_URL",
        "http://reasoning-nim.research-ops.svc.cluster.local:8000"
    )
    embedding_nim_url = os.getenv(
        "EMBEDDING_NIM_URL",
        "http://embedding-nim.research-ops.svc.cluster.local:8001"
    )
    
    reasoning_available = await check_nim_health(reasoning_nim_url)
    embedding_available = await check_nim_health(embedding_nim_url)
    
    return {
        "status": "healthy" if (reasoning_available and embedding_available) else "degraded",
        "service": "research-ops-agent",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "nims_available": {
            "reasoning_nim": reasoning_available,
            "embedding_nim": embedding_available
        }
    }


@app.get("/ready", tags=["System"])
async def readiness_check():
    """
    Readiness check for Kubernetes
    
    Returns 200 if service is ready to accept requests
    """
    return {"status": "ready"}


@app.get("/metrics", tags=["System"])
async def prometheus_metrics():
    """
    Prometheus metrics endpoint
    
    Returns metrics in Prometheus format for scraping
    """
    if not metrics or not METRICS_AVAILABLE:
        return Response(
            content="# Metrics not available\n",
            media_type="text/plain"
        )
    
    return Response(
        content=metrics.get_metrics(),
        media_type="text/plain"
    )


@app.post("/research", response_model=ResearchResponse, 
         responses={
             400: {"model": ErrorResponse, "description": "Invalid input"},
             500: {"model": ErrorResponse, "description": "Internal error"}
         },
         tags=["Research"])
async def research(request: ResearchRequest):
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
        # Validate input
        validated = ResearchQuery(
            query=request.query,
            max_papers=request.max_papers
        )
        
        logger.info(f"Starting research for query: {validated.query}")
        
        # Check synthesis cache first (before initializing NIMs)
        synthesis_cache = None
        try:
            from cache import get_cache, SynthesisCache
            cache = get_cache()
            synthesis_cache = SynthesisCache(cache)
            cached_result = synthesis_cache.get_synthesis(
                validated.query,
                validated.max_papers
            )
            if cached_result:
                logger.info("Returning cached synthesis result")
                # Update processing time
                cached_result['processing_time_seconds'] = time.time() - start_time
                if metrics:
                    metrics.record_cache_hit("synthesis")
                return cached_result
        except Exception as e:
            logger.warning(f"Cache check failed: {e}")
        
        if metrics and synthesis_cache:
            metrics.record_cache_miss("synthesis")
        
        # Apply date filtering imports
        if request.start_year or request.end_year:
            try:
                from date_filter import filter_by_year_range, prioritize_recent_papers
            except ImportError:
                from src.date_filter import filter_by_year_range, prioritize_recent_papers
        
        # Initialize NIM clients
        async with ReasoningNIMClient() as reasoning, \
                   EmbeddingNIMClient() as embedding:
            
            # Create agent
            agent = ResearchOpsAgent(reasoning, embedding)
            
            # Run research workflow
            result = await agent.run(
                query=validated.query,
                max_papers=validated.max_papers
            )
            
            # Cache synthesis result
            if synthesis_cache:
                try:
                    synthesis_cache.set_synthesis(
                        validated.query,
                        validated.max_papers,
                        result
                    )
                except Exception as e:
                    logger.warning(f"Failed to cache synthesis: {e}")
            
            # Apply date filtering to results
            if request.start_year or request.end_year:
                try:
                    papers_list = result.get('papers', [])
                    filtered_papers = filter_by_year_range(
                        papers_list,
                        start_year=request.start_year,
                        end_year=request.end_year
                    )
                    
                    if request.prioritize_recent:
                        filtered_papers = prioritize_recent_papers(filtered_papers, recent_years=3)
                    
                    # Update result with filtered papers
                    result['papers'] = [
                        p for p in result['papers']
                        if any(fp.get('id') == p.get('id') for fp in filtered_papers)
                    ]
                    result['papers_analyzed'] = len(result['papers'])
                    logger.info(f"Date filtered: {len(result['papers'])} papers after filtering")
                except Exception as e:
                    logger.warning(f"Date filtering failed: {e}")
        
        # Check for errors in result
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Invalid input")
            )
        
        # Add processing time
        result["processing_time_seconds"] = round(time.time() - start_time, 2)
        result["query"] = validated.query
        
        # Record agent decisions in metrics
        decisions = result.get('decisions', [])
        if metrics and METRICS_AVAILABLE:
            for decision in decisions:
                agent_name = decision.get('agent', 'Unknown')
                decision_type = decision.get('decision_type', 'Unknown')
                metrics.record_agent_decision(agent_name, decision_type)
            
            # Record papers analyzed by source
            papers = result.get('papers', [])
            for paper in papers:
                source = paper.get('source', 'unknown')
                metrics.record_paper_analyzed(source)
            
            # Record quality scores
            quality_scores = result.get('quality_scores', [])
            for qs in quality_scores:
                overall_score = qs.get('overall_score', 0)
                metrics.record_quality_score(overall_score)
        
        logger.info(
            f"Research complete: {result['papers_analyzed']} papers, "
            f"{len(result['decisions'])} decisions, "
            f"{result['processing_time_seconds']}s"
        )
        
        return result
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid input",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Research error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
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
            "decisions": research_sessions[session_id].get("decisions", [])
        }
    else:
        raise HTTPException(
            status_code=404,
            detail={"error": "Session not found", "session_id": session_id}
        )


class BibTeXExportRequest(BaseModel):
    """Request model for BibTeX export"""
    papers: List[Dict] = Field(..., description="List of paper dictionaries")


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
            "papers_count": len(request.papers)
        }
    except Exception as e:
        logger.error(f"BibTeX export error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Export failed",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
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
            date=datetime.now().strftime('%B %d, %Y')
        )
        return {
            "format": "latex",
            "content": latex_content,
            "query": request.query,
            "papers_count": len(request.papers)
        }
    except Exception as e:
        logger.error(f"LaTeX export error: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Export failed",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "service": "ResearchOps Agent API",
        "version": "1.0.0",
        "description": "Multi-agent AI system for automated literature review",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "research": "/research (POST)",
            "export_bibtex": "/export/bibtex (POST)",
            "export_latex": "/export/latex (POST)"
        },
        "powered_by": [
            "NVIDIA llama-3.1-nemotron-nano-8B-v1 (Reasoning NIM)",
            "NVIDIA nv-embedqa-e5-v5 (Embedding NIM)",
            "Amazon EKS"
        ]
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("=" * 60)
    logger.info("🚀 ResearchOps Agent API Starting")
    logger.info("=" * 60)
    logger.info("Service: ResearchOps Agent API v1.0.0")
    logger.info("Endpoints: /docs, /health, /research")
    logger.info("NIMs: Reasoning + Embedding")
    logger.info("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information"""
    logger.info("🛑 ResearchOps Agent API Shutting Down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )

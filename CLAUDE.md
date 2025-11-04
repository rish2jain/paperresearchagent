# CLAUDE.md

**Last Updated:** 2025-01-15

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ResearchOps Agent is a multi-agent AI system built for the NVIDIA & AWS Agentic AI Unleashed Hackathon 2025. It automates literature review synthesis using NVIDIA NIMs (llama-3.1-nemotron-nano-8B-v1 for reasoning and nv-embedqa-e5-v5 for embeddings) deployed on AWS EKS.

**Core Architecture:**
- 4 autonomous agents (Scout, Analyst, Synthesizer, Coordinator) orchestrated via decision logging
- Agent system uses both NVIDIA NIMs: Reasoning NIM for extraction/synthesis, Embedding NIM for semantic search
- Deploys to Amazon EKS with GPU instances (g5.2xlarge with NVIDIA A10G)
- Searches 7 academic databases (arXiv, PubMed, Semantic Scholar, Crossref, IEEE, ACM, Springer)

## Essential Commands

### Development Environment

```bash
# Create virtual environment (Python 3.9+)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests with pytest
python -m pytest src/

# Run specific test file
python -m pytest src/test_nim_clients.py

# Run with verbose output
python -m pytest -v src/

# Run with asyncio mode (important for async tests)
python -m pytest --asyncio-mode=auto src/

# Run comprehensive integration test
python -m pytest src/test_comprehensive_integration.py -v
```

### Code Quality

```bash
# Format code with Black (line length: 100)
black src/

# Lint with flake8
flake8 src/

# Type checking (optional, not strictly enforced)
mypy src/
```

### Local Development & Testing

```bash
# Run FastAPI server locally
uvicorn src.api:app --reload --host 0.0.0.0 --port 8080

# Run Streamlit web UI locally
streamlit run src/web_ui.py

# Test NIM clients (requires NIMs running)
python src/test_nim_clients.py

# Test agent system
python src/test_agents.py
```

### Kubernetes Deployment

```bash
# Deploy to EKS (requires AWS credentials and NGC API key)
cd k8s
chmod +x deploy.sh
./deploy.sh

# Check deployment status
kubectl get pods -n research-ops
kubectl get svc -n research-ops

# View logs
kubectl logs -f deployment/reasoning-nim -n research-ops
kubectl logs -f deployment/embedding-nim -n research-ops
kubectl logs -f deployment/agent-orchestrator -n research-ops

# Port-forward for local access
kubectl port-forward -n research-ops svc/web-ui 8501:8501
kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000
kubectl port-forward -n research-ops svc/embedding-nim 8001:8001
```

## Architecture Patterns

### Multi-Agent System (`src/agents.py`)

The system implements a **decision-logging architecture** where each agent autonomously makes decisions tracked via `DecisionLog`:

```python
decision_log.log_decision(
    agent="Scout",
    decision_type="search_expansion",
    decision="Search 3 more papers",
    reasoning="Low confidence (0.65) requires more data",
    nim_used="embedding_nim"
)
```

**Agent Roles:**
- **Scout Agent**: Semantic search using Embedding NIM, parallel queries to 7 sources
- **Analyst Agent**: Structured extraction using Reasoning NIM, parallel paper processing
- **Synthesizer Agent**: Cross-document reasoning with both NIMs (embedding for clustering, reasoning for contradictions)
- **Coordinator Agent**: Meta-decisions using Reasoning NIM (search more? synthesis complete?)

**Key Pattern:** Agents demonstrate autonomy through explicit decision-making with reasoning transparency, not just function execution.

### NIM Client Architecture (`src/nim_clients.py`)

Clients implement:
- **Async context managers** for session lifecycle
- **Circuit breaker pattern** (optional, configurable via env vars)
- **Retry logic** with exponential backoff (tenacity)
- **Request/response logging** for debugging
- **Metrics collection** (optional, Prometheus-compatible)

**Service Endpoints:**
- Reasoning NIM: `http://reasoning-nim.research-ops.svc.cluster.local:8000`
- Embedding NIM: `http://embedding-nim.research-ops.svc.cluster.local:8001`

Both support health checks at `/v1/health/live` and `/v1/health/ready`.

### Configuration System (`src/config.py`)

Uses **dataclasses with environment variable loading**:
- `NIMConfig`: Service URLs and timeouts
- `PaperSourceConfig`: API keys for 7 sources, enable/disable flags
- `AgentConfig`: Relevance thresholds, clustering parameters
- `APIConfig`: Server settings, CORS, demo mode

**Pattern:** All config loaded via `Config.from_env()` with sensible defaults. Override via environment variables.

### Paper Source Integration

**Free sources (always enabled):** arXiv, PubMed, Semantic Scholar, Crossref
**Paid sources (optional):** IEEE Xplore, ACM Digital Library, SpringerLink

Enable/disable via environment variables:
```bash
ENABLE_ARXIV=true
ENABLE_IEEE=false  # Requires IEEE_API_KEY
```

Scout agent queries all enabled sources **in parallel** using `asyncio.gather()`.

### Caching & Performance

Optional modules (`src/cache.py`, `src/metrics.py`):
- **Paper metadata caching** (Redis-backed, optional)
- **Embedding caching** (reduces duplicate embedding calls)
- **Synthesis result caching** (for demo mode)
- **Prometheus metrics** (request counts, latencies, NIM usage)

These are **optional dependencies** - code gracefully degrades if not available.

## Testing Philosophy

### Test Structure

Tests are located in `src/test_*.py`:
- `test_nim_clients.py`: NIM client unit tests (async)
- `test_agents.py`: Agent system unit tests (async)
- `test_integration.py`: Integration tests with mock NIMs
- `test_comprehensive_integration.py`: Full system test with live NIMs

**Important:** Tests use `pytest-asyncio` with `asyncio_mode=auto` (configured in `pyproject.toml`).

### Mock vs Live Testing

- **Unit tests:** Use mock responses for fast, deterministic testing
- **Integration tests:** Can run against live NIMs (requires NIMs deployed)
- Set `DEMO_MODE=true` for pre-cached responses (speeds up UI testing)

### Running Tests in Development

```bash
# Quick unit tests (mock NIMs)
python -m pytest src/test_nim_clients.py src/test_agents.py -v

# Full integration test (requires live NIMs)
python -m pytest src/test_comprehensive_integration.py -v --asyncio-mode=auto
```

## Important Patterns to Follow

### 1. Async/Await Throughout

All I/O operations are async (HTTP requests, NIM calls, database queries). Always use `async`/`await`:

```python
async with ReasoningNIMClient() as reasoning:
    result = await reasoning.complete("query text")
```

### 2. Error Handling with Circuit Breakers

NIM clients support circuit breakers (optional). When enabled:
- Fails fast after 5 consecutive errors
- Opens circuit for 60 seconds
- Requires 2 successes to close

```python
try:
    result = await nim_client.complete(prompt)
except CircuitBreakerOpenError:
    # Handle graceful degradation
```

### 3. Decision Logging is Critical

For hackathon judges, **decision transparency** is essential. Always log autonomous decisions:

```python
self.decision_log.log_decision(
    agent="AgentName",
    decision_type="action_type",
    decision="What was decided",
    reasoning="Why this decision was made",
    nim_used="reasoning_nim" or "embedding_nim"
)
```

### 4. Parallel Operations

Use `asyncio.gather()` for parallel operations:
- Scout searches all sources in parallel
- Analyst processes multiple papers in parallel
- Synthesizer clusters findings in parallel

**Never** process papers sequentially when they're independent.

### 5. Configuration via Environment Variables

Never hardcode URLs, API keys, or thresholds. Use config:

```python
from config import Config
config = Config.from_env()
reasoning_url = config.nim.reasoning_nim_url
```

### 6. Optional Dependencies

Code must gracefully handle missing optional modules:

```python
try:
    from cache import get_cache
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False
```

## EKS Deployment Structure

Kubernetes manifests in `k8s/`:
- `namespace.yaml`: Creates `research-ops` namespace
- `secrets.yaml`: NGC API key, AWS credentials (template provided)
- `reasoning-nim-deployment.yaml`: Reasoning NIM with GPU resources
- `embedding-nim-deployment.yaml`: Embedding NIM with GPU resources
- `vector-db-deployment.yaml`: Qdrant vector database
- `agent-orchestrator-deployment.yaml`: Agent system with API
- `web-ui-deployment.yaml`: Streamlit frontend

**Deployment pattern:** Services communicate via Kubernetes DNS (e.g., `http://reasoning-nim.research-ops.svc.cluster.local:8000`)

### GPU Resource Management

Both NIM deployments request GPU resources:
```yaml
resources:
  limits:
    nvidia.com/gpu: 1
  requests:
    nvidia.com/gpu: 1
```

**Important:** EKS cluster needs g5.2xlarge nodes (NVIDIA A10G GPUs) or similar.

## Environment Variables Reference

**Required:**
- `NGC_API_KEY`: NVIDIA NGC API key (get from ngc.nvidia.com)

**NIM Configuration:**
- `REASONING_NIM_URL`: Override reasoning NIM endpoint
- `EMBEDDING_NIM_URL`: Override embedding NIM endpoint

**Paper Sources:**
- `SEMANTIC_SCHOLAR_API_KEY`: Optional, increases rate limits
- `IEEE_API_KEY`: Required if `ENABLE_IEEE=true`
- `ACM_API_KEY`: Required if `ENABLE_ACM=true`
- `SPRINGER_API_KEY`: Required if `ENABLE_SPRINGER=true`

**Optional Features:**
- `REDIS_URL`: Enable caching (e.g., `redis://localhost:6379`)
- `DEMO_MODE=true`: Use pre-cached results for demos
- `CIRCUIT_BREAKER_FAIL_MAX=5`: Circuit breaker threshold
- `CIRCUIT_BREAKER_TIMEOUT=60`: Circuit breaker timeout (seconds)

## Troubleshooting

### NIMs Not Responding

1. Check pod status: `kubectl get pods -n research-ops`
2. Check logs: `kubectl logs deployment/reasoning-nim -n research-ops`
3. Test health endpoints: `curl http://localhost:8000/v1/health/live`
4. Verify NGC_API_KEY is set correctly in secrets

### Tests Failing with Timeout Errors

- Tests against live NIMs may timeout if NIMs are slow
- Use `DEMO_MODE=true` for faster testing with cached responses
- Increase timeouts in `src/nim_clients.py` if needed

### Agent System Not Making Autonomous Decisions

- Check `DecisionLog` output in console/logs
- Verify Reasoning NIM is responding (Coordinator makes meta-decisions)
- Check `SYNTHESIS_QUALITY_THRESHOLD` isn't set too high

### EKS Deployment Issues

- Ensure cluster has GPU nodes: `kubectl get nodes -o wide`
- Check GPU resources: `kubectl describe node <node-name>`
- Verify secrets are applied: `kubectl get secrets -n research-ops`
- Common issue: vCPU quota limits - see `docs/AWS_SETUP_GUIDE.md`

## Key Files to Know

- `src/agents.py`: Multi-agent system implementation, decision logging
- `src/nim_clients.py`: NVIDIA NIM API wrappers with circuit breakers
- `src/config.py`: Configuration management with environment variables
- `src/api.py`: FastAPI REST API endpoints
- `src/web_ui.py`: Streamlit web interface with real-time visualization
- `k8s/deploy.sh`: One-command EKS deployment script
- `requirements.txt`: Python dependencies (pinned versions)

## Documentation

See `DOCUMENTATION_INDEX.md` for complete documentation index. Key docs:
- `docs/Architecture_Diagrams.md`: System architecture diagrams
- `docs/PAPER_SOURCES.md`: Integration details for 7 sources
- `docs/AWS_SETUP_GUIDE.md`: AWS credentials and EKS setup
- `docs/TROUBLESHOOTING.md`: Common issues and solutions

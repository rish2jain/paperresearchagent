# Docker Testing Guide

This guide explains how to test the ResearchOps Agent application using Docker.

## Prerequisites

- Docker installed and running
- Docker Compose installed (usually comes with Docker Desktop)
- At least 4GB of free disk space

## Quick Start

### Option 1: Test with Mock NIMs (Recommended for Quick Testing)

This option uses mock NIM services that simulate the behavior of the actual NVIDIA NIMs without requiring GPU access or NVIDIA NGC credentials.

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

This will start:
- **Orchestrator API** on http://localhost:8080
- **Web UI** on http://localhost:8501
- **Mock Reasoning NIM** on http://localhost:8000
- **Mock Embedding NIM** on http://localhost:8001

### Option 2: Test with Real NIMs

If you have NVIDIA NIMs deployed (either locally or remotely), you can point the orchestrator to them:

```bash
# Set environment variables for real NIM URLs
export REASONING_NIM_URL="http://your-reasoning-nim:8000"
export EMBEDDING_NIM_URL="http://your-embedding-nim:8001"

# Start only orchestrator and web-ui (skip mock NIMs)
docker-compose up --build orchestrator web-ui
```

Or create a `docker-compose.override.yml`:

```yaml
version: '3.8'
services:
  orchestrator:
    environment:
      REASONING_NIM_URL: "http://your-reasoning-nim:8000"
      EMBEDDING_NIM_URL: "http://your-embedding-nim:8001"
    depends_on: []  # Remove mock NIM dependencies
```

## Accessing the Application

1. **Web UI**: Open http://localhost:8501 in your browser
2. **API Documentation**: Open http://localhost:8080/docs for interactive API docs
3. **API Health Check**: Visit http://localhost:8080/health

## Testing the Application

### 1. Health Check

```bash
# Check orchestrator health
curl http://localhost:8080/health

# Expected response:
{
  "status": "healthy",
  "service": "research-ops-agent",
  "version": "1.0.0",
  "timestamp": "2025-01-01T12:00:00",
  "nims_available": {
    "reasoning_nim": true,
    "embedding_nim": true
  }
}
```

### 2. Test Research Query via API

```bash
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning for medical imaging",
    "max_papers": 5
  }'
```

### 3. Test via Web UI

1. Open http://localhost:8501
2. Enter a research query (e.g., "machine learning for medical imaging")
3. Click "🚀 Start Research"
4. Wait for the synthesis to complete
5. Review the results and agent decisions

## Viewing Logs

```bash
# View all logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f orchestrator
docker-compose logs -f web-ui
docker-compose logs -f reasoning-nim
docker-compose logs -f embedding-nim
```

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

## Rebuilding After Code Changes

```bash
# Rebuild specific service
docker-compose build orchestrator

# Rebuild and restart
docker-compose up --build orchestrator
```

## Troubleshooting

### Services won't start

1. Check if ports are already in use:
   ```bash
   lsof -i :8080  # Orchestrator
   lsof -i :8501  # Web UI
   lsof -i :8000  # Reasoning NIM
   lsof -i :8001  # Embedding NIM
   ```

2. Check container status:
   ```bash
   docker-compose ps
   ```

3. Check container logs:
   ```bash
   docker-compose logs orchestrator
   ```

### Health checks failing

1. Wait a bit longer - services may need time to start
2. Check if the service is responding:
   ```bash
   docker-compose exec orchestrator curl http://localhost:8080/health
   ```

### NIM services not connecting

1. Verify NIM URLs are correct:
   ```bash
   docker-compose exec orchestrator env | grep NIM
   ```

2. Test NIM connectivity from orchestrator:
   ```bash
   docker-compose exec orchestrator python -c "
   import asyncio
   import aiohttp
   
   async def test():
       async with aiohttp.ClientSession() as session:
           async with session.get('http://reasoning-nim:8000/v1/health/live') as resp:
               print(f'Reasoning NIM: {resp.status}')
           async with session.get('http://embedding-nim:8001/v1/health/live') as resp:
               print(f'Embedding NIM: {resp.status}')
   
   asyncio.run(test())
   "
   ```

## Running Tests in Docker

To run the test suite in a container:

```bash
# Run integration tests
docker-compose run --rm orchestrator python -m pytest src/test_integration.py -v

# Run all tests
docker-compose run --rm orchestrator python -m pytest src/ -v
```

## Performance Testing

For performance testing, you can scale services:

```bash
# Run multiple orchestrator instances
docker-compose up --scale orchestrator=3
```

## Development Workflow

For active development with hot-reload:

1. The docker-compose.yml mounts the source code as read-only volumes
2. For full development mode, you can modify volumes to be read-write:
   ```yaml
   volumes:
     - ./src:/app/src  # Remove :ro for write access
   ```

3. However, Python changes require container restart:
   ```bash
   docker-compose restart orchestrator
   ```

## Limitations of Mock NIMs

The mock NIM services provide:
- ✅ Health check endpoints
- ✅ Proper API response structure
- ✅ Mock embeddings and completions

However, they do NOT provide:
- ❌ Real reasoning capabilities
- ❌ Real semantic similarity
- ❌ Production-quality results

For meaningful testing, use real NVIDIA NIMs when available.

## Next Steps

- Deploy to Kubernetes using the files in `k8s/`
- Configure real NVIDIA NIM endpoints
- Set up CI/CD with Docker-based testing
- Add monitoring and logging solutions


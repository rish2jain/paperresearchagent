#!/bin/bash
# Quick test script to verify Docker setup

set -e

echo "🔍 Checking Docker setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

echo "✅ docker-compose is available"

# Build and start services
echo ""
echo "🏗️  Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check health endpoints
echo ""
echo "🏥 Checking service health..."

# Check orchestrator
if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ Orchestrator is healthy"
else
    echo "❌ Orchestrator health check failed"
    docker-compose logs orchestrator
    exit 1
fi

# Check web UI
if curl -s http://localhost:8501/_stcore/health > /dev/null; then
    echo "✅ Web UI is healthy"
else
    echo "❌ Web UI health check failed"
    docker-compose logs web-ui
    exit 1
fi

# Check mock reasoning NIM
if curl -s http://localhost:8000/v1/health/live > /dev/null; then
    echo "✅ Mock Reasoning NIM is healthy"
else
    echo "❌ Mock Reasoning NIM health check failed"
    docker-compose logs reasoning-nim
    exit 1
fi

# Check mock embedding NIM
if curl -s http://localhost:8001/v1/health/live > /dev/null; then
    echo "✅ Mock Embedding NIM is healthy"
else
    echo "❌ Mock Embedding NIM health check failed"
    docker-compose logs embedding-nim
    exit 1
fi

echo ""
echo "🎉 All services are up and healthy!"
echo ""
echo "📍 Access points:"
echo "   - Web UI: http://localhost:8501"
echo "   - API Docs: http://localhost:8080/docs"
echo "   - Health Check: http://localhost:8080/health"
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"


#!/bin/bash
# Setup local Qdrant instance for vector storage

set -e

echo "=========================================="
echo "🗄️  Local Qdrant Setup"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if Qdrant container already exists
if docker ps -a --format '{{.Names}}' | grep -q "^qdrant-local$"; then
    echo "📦 Qdrant container already exists"
    
    # Check if it's running
    if docker ps --format '{{.Names}}' | grep -q "^qdrant-local$"; then
        echo "✅ Qdrant is already running"
        echo ""
        echo "Qdrant URL: http://localhost:6333"
        echo "Dashboard: http://localhost:6333/dashboard"
    else
        echo "🔄 Starting existing Qdrant container..."
        docker start qdrant-local
        echo "✅ Qdrant started"
        echo ""
        echo "Qdrant URL: http://localhost:6333"
        echo "Dashboard: http://localhost:6333/dashboard"
    fi
else
    echo "📦 Creating new Qdrant container..."
    
    # Create storage directory
    STORAGE_DIR="./qdrant_storage"
    mkdir -p "$STORAGE_DIR"
    
    # Run Qdrant container
    docker run -d \
        --name qdrant-local \
        -p 6333:6333 \
        -p 6334:6334 \
        -v "$(pwd)/qdrant_storage:/qdrant/storage" \
        qdrant/qdrant
    
    echo "✅ Qdrant container created and started"
    echo ""
    echo "Qdrant URL: http://localhost:6333"
    echo "Dashboard: http://localhost:6333/dashboard"
    echo ""
    echo "Storage: $STORAGE_DIR"
fi

echo ""
echo "=========================================="
echo "✅ Qdrant Setup Complete!"
echo "=========================================="
echo ""
echo "To stop Qdrant: docker stop qdrant-local"
echo "To remove Qdrant: docker rm -f qdrant-local"
echo ""


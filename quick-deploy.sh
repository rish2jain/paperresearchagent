#!/bin/bash
#
# Quick Deploy Script for ResearchOps Agent
# Usage: ./quick-deploy.sh [eks|local]
# Default: eks
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Deployment target (default: eks)
TARGET=${1:-eks}

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   ResearchOps Agent - Quick Deploy        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Check if deploy.py exists
if [ ! -f "deploy.py" ]; then
    echo -e "${RED}❌ deploy.py not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Make deploy.py executable
chmod +x deploy.py

case "$TARGET" in
    local|docker)
        echo -e "${YELLOW}🐳 Deploying locally with Docker Compose...${NC}"
        echo ""

        # Check for .env file
        if [ ! -f ".env" ]; then
            echo -e "${YELLOW}⚠️  .env file not found${NC}"
            if [ -f ".env.example" ]; then
                echo "Creating .env from .env.example..."
                cp .env.example .env
                echo -e "${GREEN}✅ Created .env file${NC}"
                echo "Please edit .env with your API keys if needed"
            fi
        fi

        # Deploy
        ./deploy.py --target docker --build
        ;;

    eks|kubernetes|k8s)
        echo -e "${YELLOW}☸️  Deploying to AWS EKS...${NC}"
        echo ""

        # Check for NGC_API_KEY
        if [ -z "$NGC_API_KEY" ]; then
            echo -e "${RED}❌ NGC_API_KEY not set${NC}"
            echo "Please set NGC_API_KEY environment variable:"
            echo "  export NGC_API_KEY='your_key_here'"
            echo ""
            echo "Get your key from: https://ngc.nvidia.com/setup"
            exit 1
        fi

        # Deploy
        ./deploy.py --target eks --cluster research-ops-cluster --region us-east-2
        ;;

    *)
        echo -e "${RED}❌ Unknown target: $TARGET${NC}"
        echo ""
        echo "Usage: $0 [eks|local]"
        echo ""
        echo "Examples:"
        echo "  $0          # Deploy to AWS EKS (default)"
        echo "  $0 eks      # Deploy to AWS EKS"
        echo "  $0 local    # Deploy with Docker Compose"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Deployment initiated!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"

if [ "$TARGET" = "local" ] || [ "$TARGET" = "docker" ]; then
    echo "  • Web UI: http://localhost:8501"
    echo "  • API: http://localhost:8080"
    echo "  • View logs: docker-compose logs -f"
    echo "  • Stop: docker-compose down"
else
    echo "  • Check status: kubectl get pods -n research-ops"
    echo "  • View logs: kubectl logs -f deployment/web-ui -n research-ops"
    echo "  • Port-forward UI: kubectl port-forward -n research-ops svc/web-ui 8501:8501"
    echo "  • Cleanup: kubectl delete namespace research-ops"
fi

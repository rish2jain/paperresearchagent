#!/bin/bash
# Deployment script for Research Ops Agent on AWS EKS
# Usage: ./deploy.sh

set -e

echo "🚀 Deploying Research Ops Agent to AWS EKS"
echo "============================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl not found. Please install kubectl${NC}"
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI not found. Please install AWS CLI${NC}"
    exit 1
fi

# Check for required environment variables
if [ -z "$NGC_API_KEY" ]; then
    echo -e "${YELLOW}NGC_API_KEY not set in environment, checking secrets.yaml...${NC}"
    
    if [ -f "secrets.yaml" ]; then
        # Try to extract NGC_API_KEY from secrets.yaml
        # First, try using yq if available (most robust)
        if command -v yq &> /dev/null; then
            EXTRACTED_KEY=$(yq eval '.stringData.NGC_API_KEY // .data.NGC_API_KEY | @base64d' secrets.yaml 2>/dev/null || yq eval '.stringData.NGC_API_KEY' secrets.yaml 2>/dev/null || echo "")
        else
            # Fallback: safer grep+sed/awk that handles single/double quotes, unquoted, and inline comments
            # Pattern: find NGC_API_KEY line, extract value, strip quotes, remove inline comments
            # First sed: remove everything before colon+whitespace, handle quoted/unquoted values
            # Second sed: remove inline comments (anything after #)
            # Third sed: trim leading/trailing whitespace
            EXTRACTED_KEY=$(grep -E '^\s*NGC_API_KEY\s*:' secrets.yaml | \
                sed -E 's/^[^:]*:\s*//' | \
                sed -E "s/^['\"]?([^'\"]*)['\"]?(\s*#.*)?$/\1/" | \
                sed 's/#.*$//' | \
                sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
                head -1)
        fi
        
        # Validate extracted key (non-empty and reasonable length)
        if [ -n "$EXTRACTED_KEY" ] && [ ${#EXTRACTED_KEY} -ge 10 ] && [ ${#EXTRACTED_KEY} -le 500 ]; then
            export NGC_API_KEY="$EXTRACTED_KEY"
            echo -e "${GREEN}✅ Extracted NGC_API_KEY from secrets.yaml${NC}"
        else
            echo -e "${RED}NGC_API_KEY not found in secrets.yaml or invalid format${NC}"
            echo -e "${RED}Please set NGC_API_KEY environment variable or add it to secrets.yaml${NC}"
            echo -e "${RED}Get it from: https://ngc.nvidia.com/setup${NC}"
            exit 1
        fi
    else
        echo -e "${RED}NGC_API_KEY not set and secrets.yaml not found${NC}"
        echo -e "${RED}Please set NGC_API_KEY environment variable or create secrets.yaml${NC}"
        echo -e "${RED}Get it from: https://ngc.nvidia.com/setup${NC}"
        exit 1
    fi
fi

# Create EKS cluster (if not exists)
echo -e "${YELLOW}Checking EKS cluster...${NC}"
if ! aws eks describe-cluster --name research-ops-cluster --region us-east-2 &> /dev/null; then
    echo -e "${YELLOW}Creating EKS cluster (this takes 15-20 minutes)...${NC}"
    eksctl create cluster \
        --name research-ops-cluster \
        --region us-east-2 \
        --node-type g5.2xlarge \
        --nodes 2 \
        --nodes-min 1 \
        --nodes-max 3 \
        --managed \
        --version 1.28
else
    echo -e "${GREEN}EKS cluster already exists${NC}"
fi

# Update kubeconfig
echo -e "${YELLOW}Updating kubeconfig...${NC}"
aws eks update-kubeconfig --name research-ops-cluster --region us-east-2

# Create NGC registry secret
echo -e "${YELLOW}Creating NGC registry secret...${NC}"
kubectl create secret docker-registry ngc-secret \
    --docker-server=nvcr.io \
    --docker-username='$oauthtoken' \
    --docker-password=$NGC_API_KEY \
    --namespace=default \
    --dry-run=client -o yaml | kubectl apply -f -

# Apply Kubernetes manifests
echo -e "${YELLOW}Applying Kubernetes manifests...${NC}"

echo "  → Creating namespace..."
kubectl apply -f namespace.yaml

echo "  → Creating secrets..."
# Update secrets with actual values
sed "s/YOUR_NGC_API_KEY_HERE/$NGC_API_KEY/" secrets.yaml | kubectl apply -f -

echo "  → Deploying Reasoning NIM..."
kubectl apply -f reasoning-nim-deployment.yaml

echo "  → Deploying Embedding NIM..."
kubectl apply -f embedding-nim-deployment.yaml

echo "  → Deploying Vector Database..."
kubectl apply -f vector-db-deployment.yaml

echo "  → Deploying Agent Orchestrator..."
kubectl apply -f agent-orchestrator-deployment.yaml

echo "  → Deploying Web UI..."
kubectl apply -f web-ui-deployment.yaml

# Wait for deployments to be ready
echo -e "${YELLOW}Waiting for deployments to be ready (this may take 10-15 minutes)...${NC}"
echo -e "${YELLOW}Note: NIMs use Recreate strategy (brief downtime) and TensorRT compilation (10+ min first start)${NC}"

echo "  → Waiting for Reasoning NIM (up to 20 minutes for TensorRT engine build)..."
kubectl wait --for=condition=available --timeout=1200s deployment/reasoning-nim -n research-ops

echo "  → Waiting for Embedding NIM (up to 20 minutes for TensorRT engine build)..."
kubectl wait --for=condition=available --timeout=1200s deployment/embedding-nim -n research-ops

echo "  → Waiting for Vector DB..."
kubectl wait --for=condition=available --timeout=300s deployment/qdrant -n research-ops

echo "  → Waiting for Agent Orchestrator..."
kubectl wait --for=condition=available --timeout=300s deployment/agent-orchestrator -n research-ops

echo "  → Waiting for Web UI..."
kubectl wait --for=condition=available --timeout=300s deployment/web-ui -n research-ops

# Get service endpoints
echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "============================================"
echo "Service Endpoints:"
echo "============================================"

ORCHESTRATOR_IP=$(kubectl get svc agent-orchestrator -n research-ops -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
UI_IP=$(kubectl get svc web-ui -n research-ops -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "Agent Orchestrator API: http://$ORCHESTRATOR_IP"
echo "Web UI: http://$UI_IP"
echo ""
echo "============================================"
echo "Useful commands:"
echo "============================================"
echo "View logs:"
echo "  kubectl logs -f deployment/reasoning-nim -n research-ops"
echo "  kubectl logs -f deployment/embedding-nim -n research-ops"
echo "  kubectl logs -f deployment/agent-orchestrator -n research-ops"
echo ""
echo "Check status:"
echo "  kubectl get pods -n research-ops"
echo "  kubectl get svc -n research-ops"
echo ""
echo "Delete deployment:"
echo "  kubectl delete namespace research-ops"
echo "  eksctl delete cluster --name research-ops-cluster --region us-east-2"
echo ""
echo -e "${GREEN}✅ Ready to go!${NC}"

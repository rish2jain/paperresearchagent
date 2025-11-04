#!/bin/bash
# Deploy Research Ops Agent to Kubernetes and open Streamlit UI
# Usage: ./deploy_and_open.sh [--skip-deploy]

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="research-ops"
SERVICE_NAME="web-ui"
STREAMLIT_PORT=8501
LOCAL_PORT=8501
STREAMLIT_URL="http://localhost:${LOCAL_PORT}"

# Parse arguments
SKIP_DEPLOY=false
if [[ "$1" == "--skip-deploy" ]]; then
    SKIP_DEPLOY=true
fi

echo -e "${BLUE}🚀 Research Ops Agent - Deploy & Launch${NC}"
echo "============================================"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl${NC}"
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install AWS CLI${NC}"
    exit 1
fi

# Check if kubectl can connect to cluster
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Cannot connect to Kubernetes cluster${NC}"
    echo -e "${YELLOW}Please ensure your kubeconfig is set up correctly${NC}"
    exit 1
fi

# Check for NGC_API_KEY - try to extract from secrets.yaml if not set
if [ -z "$NGC_API_KEY" ]; then
    echo -e "${YELLOW}NGC_API_KEY not set in environment, checking k8s/secrets.yaml...${NC}"
    
    if [ -f "k8s/secrets.yaml" ]; then
        # Try to extract NGC_API_KEY from secrets.yaml
        # Look for the pattern: NGC_API_KEY: "value"
        EXTRACTED_KEY=$(grep 'NGC_API_KEY' k8s/secrets.yaml | awk -F'"' '{print $2}' | head -1)
        
        if [ -n "$EXTRACTED_KEY" ]; then
            export NGC_API_KEY="$EXTRACTED_KEY"
            echo -e "${GREEN}✅ Extracted NGC_API_KEY from k8s/secrets.yaml${NC}"
        else
            echo -e "${RED}❌ NGC_API_KEY not found in k8s/secrets.yaml${NC}"
            echo -e "${YELLOW}Please set NGC_API_KEY environment variable or add it to k8s/secrets.yaml${NC}"
            echo -e "${YELLOW}Get it from: https://ngc.nvidia.com/setup${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ NGC_API_KEY not set and k8s/secrets.yaml not found${NC}"
        echo -e "${YELLOW}Please set NGC_API_KEY environment variable or create k8s/secrets.yaml${NC}"
        echo -e "${YELLOW}Get it from: https://ngc.nvidia.com/setup${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ NGC_API_KEY found in environment${NC}"
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Deploy to Kubernetes (unless skipped)
if [ "$SKIP_DEPLOY" = false ]; then
    echo -e "${YELLOW}📦 Deploying to Kubernetes...${NC}"
    echo ""
    
    # Check if deployment script exists
    if [ ! -f "k8s/deploy.sh" ]; then
        echo -e "${RED}❌ k8s/deploy.sh not found${NC}"
        exit 1
    fi
    
    # Make deploy script executable
    chmod +x k8s/deploy.sh
    
    # Run deployment script
    cd k8s
    ./deploy.sh
    cd ..
    
    echo ""
    echo -e "${GREEN}✅ Deployment complete${NC}"
else
    echo -e "${YELLOW}⏭️  Skipping deployment (--skip-deploy flag used)${NC}"
fi

echo ""

# Wait for web-ui deployment to be ready
echo -e "${YELLOW}⏳ Waiting for Web UI to be ready...${NC}"

# Check if namespace exists
if ! kubectl get namespace "$NAMESPACE" &> /dev/null; then
    echo -e "${RED}❌ Namespace '$NAMESPACE' not found${NC}"
    echo -e "${YELLOW}Please deploy first or check your cluster configuration${NC}"
    exit 1
fi

# Wait for deployment to be available
if kubectl wait --for=condition=available --timeout=600s deployment/$SERVICE_NAME -n $NAMESPACE 2>/dev/null; then
    echo -e "${GREEN}✅ Web UI is ready${NC}"
else
    echo -e "${YELLOW}⚠️  Web UI deployment may still be starting...${NC}"
    echo -e "${YELLOW}Checking pod status...${NC}"
    
    # Check pod status
    POD_STATUS=$(kubectl get pods -n $NAMESPACE -l app=$SERVICE_NAME -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "Unknown")
    
    if [ "$POD_STATUS" != "Running" ]; then
        echo -e "${RED}❌ Web UI pod is not running (status: $POD_STATUS)${NC}"
        echo -e "${YELLOW}View logs with: kubectl logs -n $NAMESPACE -l app=$SERVICE_NAME${NC}"
        exit 1
    fi
fi

echo ""

# Check if port-forward is already running (portable check)
EXISTING_PF=""
if command -v lsof &> /dev/null; then
    # Use lsof if available (Unix/macOS)
    EXISTING_PF=$(lsof -ti:${LOCAL_PORT} 2>/dev/null || echo "")
elif command -v netstat &> /dev/null; then
    # Fallback to netstat (works on both Unix and Windows)
    # Extract PID from netstat output (format varies by OS)
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
        # Windows netstat format: find line with :PORT and extract PID from last column
        EXISTING_PF=$(netstat -ano 2>/dev/null | grep -E ":${LOCAL_PORT}\s" | awk '{print $NF}' | head -1 | grep -E '^[0-9]+$' || echo "")
    else
        # Unix netstat format: extract PID from output
        EXISTING_PF=$(netstat -tlnp 2>/dev/null | grep -E ":${LOCAL_PORT}\s" | awk '{print $NF}' | cut -d'/' -f1 | grep -E '^[0-9]+$' | head -1 || echo "")
    fi
fi

# Normalize to ensure EXISTING_PF is either a PID or empty string
if [ -n "$EXISTING_PF" ] && [[ ! "$EXISTING_PF" =~ ^[0-9]+$ ]]; then
    EXISTING_PF=""
fi

if [ -n "$EXISTING_PF" ]; then
    echo -e "${YELLOW}⚠️  Port ${LOCAL_PORT} is already in use (PID: $EXISTING_PF)${NC}"
    read -p "Kill existing process and create new port-forward? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill $EXISTING_PF 2>/dev/null || true
        sleep 2
    else
        echo -e "${YELLOW}Using existing port-forward...${NC}"
    fi
fi

# Create port-forward in background
echo -e "${YELLOW}🔌 Setting up port-forward...${NC}"

# Use service-based port-forward (more reliable)
kubectl port-forward -n $NAMESPACE svc/$SERVICE_NAME ${LOCAL_PORT}:${STREAMLIT_PORT} > /tmp/k8s-port-forward.log 2>&1 &
PORT_FORWARD_PID=$!

# Wait a moment for port-forward to establish
sleep 5

# Check if port-forward process is still running
if ! ps -p $PORT_FORWARD_PID > /dev/null 2>&1; then
    echo -e "${RED}❌ Port-forward process died${NC}"
    echo -e "${YELLOW}Check logs: cat /tmp/k8s-port-forward.log${NC}"
    cat /tmp/k8s-port-forward.log
    exit 1
fi

# Verify port-forward is working by checking health endpoint
MAX_RETRIES=10
RETRY_COUNT=0
HEALTH_CHECK_PASSED=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${LOCAL_PORT}/_stcore/health 2>/dev/null || echo "000")
    
    if [ "$HTTP_CODE" = "200" ]; then
        HEALTH_CHECK_PASSED=true
        break
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 1
done

if [ "$HEALTH_CHECK_PASSED" = true ]; then
    echo -e "${GREEN}✅ Port-forward established (PID: $PORT_FORWARD_PID)${NC}"
else
    echo -e "${RED}❌ Port-forward health check failed (HTTP code: $HTTP_CODE)${NC}"
    echo -e "${YELLOW}Port-forward may still be starting. Check logs: cat /tmp/k8s-port-forward.log${NC}"
    echo -e "${YELLOW}You can try accessing ${STREAMLIT_URL} manually${NC}"
fi

echo ""
echo -e "${GREEN}✅ Streamlit is ready!${NC}"
echo ""
echo "============================================"
echo -e "${BLUE}🌐 Streamlit UI: ${STREAMLIT_URL}${NC}"
echo "============================================"
echo ""

# Open browser based on OS
echo -e "${YELLOW}🌐 Opening browser...${NC}"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$STREAMLIT_URL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open "$STREAMLIT_URL"
    elif command -v gnome-open &> /dev/null; then
        gnome-open "$STREAMLIT_URL"
    else
        echo -e "${YELLOW}Please open ${STREAMLIT_URL} in your browser${NC}"
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    start "$STREAMLIT_URL"
else
    echo -e "${YELLOW}Please open ${STREAMLIT_URL} in your browser${NC}"
fi

echo ""
echo -e "${GREEN}✨ All set! Streamlit UI should be opening in your browser.${NC}"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  View logs:        kubectl logs -f -n $NAMESPACE -l app=$SERVICE_NAME"
echo "  Check status:     kubectl get pods -n $NAMESPACE"
echo "  Stop port-forward: kill \$(lsof -ti:${LOCAL_PORT})"
echo ""
echo -e "${YELLOW}Note: Port-forward is running in the background.${NC}"
echo -e "${YELLOW}To stop it, run: kill \$(lsof -ti:${LOCAL_PORT})${NC}"
echo ""


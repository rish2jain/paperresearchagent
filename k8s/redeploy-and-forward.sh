#!/bin/bash
# Redeploy to EKS and start port-forwarding for services
# Usage: ./redeploy-and-forward.sh

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# PID file for port-forwards
PID_FILE="/tmp/research-ops-port-forwards.pid"

# Cleanup function (without exit - for internal use)
stop_port_forwards() {
    if [ -f "$PID_FILE" ]; then
        while read pid; do
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null || true
                echo -e "${GREEN}✓ Stopped port-forward (PID: $pid)${NC}"
            fi
        done < "$PID_FILE"
        rm -f "$PID_FILE"
    fi
    # Also kill any remaining kubectl port-forward processes
    pkill -f "kubectl port-forward.*research-ops" 2>/dev/null || true
}

# Cleanup function (with exit - for signal traps)
cleanup() {
    echo -e "\n${YELLOW}Cleaning up port-forwards...${NC}"
    stop_port_forwards
    echo -e "${GREEN}✓ Cleanup complete${NC}"
    exit 0
}

# Trap signals
trap cleanup SIGINT SIGTERM

echo "🚀 Redeploying Research Ops Agent to EKS and Starting Port-Forwarding"
echo "======================================================================"
echo ""

# Step 1: Deploy to EKS
echo -e "${BLUE}Step 1: Deploying to EKS...${NC}"
echo "-----------------------------------"
./deploy.sh

# Wait a moment for services to stabilize
echo ""
echo -e "${YELLOW}Waiting for services to stabilize...${NC}"
sleep 5

# Step 2: Check if pods are ready
echo ""
echo -e "${BLUE}Step 2: Verifying pods are ready...${NC}"
echo "-----------------------------------"

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    NOT_READY=$(kubectl get pods -n research-ops -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}' | grep -v Running | wc -l | tr -d ' ')
    
    if [ "$NOT_READY" -eq "0" ]; then
        echo -e "${GREEN}✓ All pods are running${NC}"
        break
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -e "${YELLOW}Waiting for pods... (${RETRY_COUNT}/${MAX_RETRIES})${NC}"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}⚠ Warning: Some pods may not be ready yet${NC}"
fi

# Show pod status
echo ""
kubectl get pods -n research-ops

# Step 3: Stop any existing port-forwards
echo ""
echo -e "${BLUE}Step 3: Stopping existing port-forwards...${NC}"
echo "-----------------------------------"
stop_port_forwards
sleep 2

# Step 4: Start port-forwarding
echo ""
echo -e "${BLUE}Step 4: Starting port-forwarding...${NC}"
echo "-----------------------------------"

# Create PID file
touch "$PID_FILE"

# Start Web UI port-forward (8501)
echo -e "${YELLOW}Starting Web UI port-forward (8501)...${NC}"
kubectl port-forward -n research-ops svc/web-ui 8501:8501 > /dev/null 2>&1 &
WEB_UI_PID=$!
echo "$WEB_UI_PID" >> "$PID_FILE"
sleep 2

# Verify Web UI port-forward is working
if kill -0 "$WEB_UI_PID" 2>/dev/null; then
    echo -e "${GREEN}✓ Web UI port-forward running (PID: $WEB_UI_PID)${NC}"
else
    echo -e "${RED}✗ Failed to start Web UI port-forward${NC}"
fi

# Start Agent Orchestrator port-forward (8080)
echo -e "${YELLOW}Starting Agent Orchestrator port-forward (8080)...${NC}"
kubectl port-forward -n research-ops svc/agent-orchestrator 8080:8080 > /dev/null 2>&1 &
ORCHESTRATOR_PID=$!
echo "$ORCHESTRATOR_PID" >> "$PID_FILE"
sleep 2

# Verify Agent Orchestrator port-forward is working
if kill -0 "$ORCHESTRATOR_PID" 2>/dev/null; then
    echo -e "${GREEN}✓ Agent Orchestrator port-forward running (PID: $ORCHESTRATOR_PID)${NC}"
else
    echo -e "${RED}✗ Failed to start Agent Orchestrator port-forward${NC}"
fi

# Step 5: Verify services are accessible
echo ""
echo -e "${BLUE}Step 5: Verifying services are accessible...${NC}"
echo "-----------------------------------"

# Test Web UI
if curl -s http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Web UI is accessible at http://localhost:8501${NC}"
else
    echo -e "${YELLOW}⚠ Web UI health check failed (may need a moment to start)${NC}"
fi

# Test Agent Orchestrator
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    ORCHESTRATOR_HEALTH=$(curl -s http://localhost:8080/health)
    echo -e "${GREEN}✓ Agent Orchestrator is accessible at http://localhost:8080${NC}"
    echo -e "${GREEN}  Health: $(echo $ORCHESTRATOR_HEALTH | grep -o '"status":"[^"]*"' || echo 'healthy')${NC}"
else
    echo -e "${YELLOW}⚠ Agent Orchestrator health check failed (may need a moment to start)${NC}"
fi

# Final summary
echo ""
echo "======================================================================"
echo -e "${GREEN}✅ Deployment and Port-Forwarding Complete!${NC}"
echo "======================================================================"
echo ""
echo "📍 Service URLs:"
echo "   • Web UI:              http://localhost:8501"
echo "   • Agent Orchestrator:  http://localhost:8080"
echo ""
echo "📊 Useful Commands:"
echo "   • View pods:           kubectl get pods -n research-ops"
echo "   • View logs:           kubectl logs -f deployment/<service-name> -n research-ops"
echo "   • View services:       kubectl get svc -n research-ops"
echo ""
echo -e "${YELLOW}⚠ Note: Port-forwards are running in the background${NC}"
echo -e "${YELLOW}   To stop them, press Ctrl+C or run: kill \$(cat $PID_FILE)${NC}"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop port-forwarding and exit${NC}"
echo ""

# Keep script running and monitor port-forwards
while true; do
    # Check if port-forwards are still running
    if [ -f "$PID_FILE" ]; then
        ALL_RUNNING=true
        while read pid; do
            if ! kill -0 "$pid" 2>/dev/null; then
                ALL_RUNNING=false
                break
            fi
        done < "$PID_FILE"
        
        if [ "$ALL_RUNNING" = false ]; then
            echo -e "${RED}⚠ Port-forward process died, restarting...${NC}"
            stop_port_forwards
            # Restart port-forwards
            kubectl port-forward -n research-ops svc/web-ui 8501:8501 > /dev/null 2>&1 &
            echo "$!" >> "$PID_FILE"
            kubectl port-forward -n research-ops svc/agent-orchestrator 8080:8080 > /dev/null 2>&1 &
            echo "$!" >> "$PID_FILE"
            sleep 2
        fi
    fi
    sleep 5
done


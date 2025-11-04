#!/bin/bash
# Start port-forwarding for Research Ops Agent services
# Usage: ./start-port-forwards.sh

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

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Stopping port-forwards...${NC}"
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
    echo -e "${GREEN}✓ All port-forwards stopped${NC}"
    exit 0
}

# Trap signals
trap cleanup SIGINT SIGTERM

echo "🔌 Starting Port-Forwarding for Research Ops Agent Services"
echo "============================================================"
echo ""

# Check if namespace exists
if ! kubectl get namespace research-ops > /dev/null 2>&1; then
    echo -e "${RED}✗ Namespace 'research-ops' not found${NC}"
    echo -e "${YELLOW}  Please deploy first using: ./deploy.sh${NC}"
    exit 1
fi

# Check if services exist
if ! kubectl get svc web-ui -n research-ops > /dev/null 2>&1; then
    echo -e "${RED}✗ Web UI service not found${NC}"
    exit 1
fi

if ! kubectl get svc agent-orchestrator -n research-ops > /dev/null 2>&1; then
    echo -e "${RED}✗ Agent Orchestrator service not found${NC}"
    exit 1
fi

# Stop any existing port-forwards
echo -e "${YELLOW}Stopping any existing port-forwards...${NC}"
if [ -f "$PID_FILE" ]; then
    while read pid; do
        kill "$pid" 2>/dev/null || true
    done < "$PID_FILE"
    rm -f "$PID_FILE"
fi
pkill -f "kubectl port-forward.*research-ops" 2>/dev/null || true
sleep 2

# Check if ports are already in use
if lsof -i :8501 > /dev/null 2>&1; then
    echo -e "${RED}✗ Port 8501 is already in use${NC}"
    echo -e "${YELLOW}  Please stop the process using port 8501 first${NC}"
    exit 1
fi

if lsof -i :8080 > /dev/null 2>&1; then
    echo -e "${RED}✗ Port 8080 is already in use${NC}"
    echo -e "${YELLOW}  Please stop the process using port 8080 first${NC}"
    exit 1
fi

# Start port-forwarding
echo ""
echo -e "${BLUE}Starting port-forwards...${NC}"
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
    exit 1
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
    exit 1
fi

# Verify services are accessible
echo ""
echo -e "${BLUE}Verifying services are accessible...${NC}"
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
echo "============================================================"
echo -e "${GREEN}✅ Port-Forwarding Started!${NC}"
echo "============================================================"
echo ""
echo "📍 Service URLs:"
echo "   • Web UI:              http://localhost:8501"
echo "   • Agent Orchestrator:  http://localhost:8080"
echo ""
echo -e "${YELLOW}⚠ Port-forwards are running in the background${NC}"
echo -e "${YELLOW}   Press Ctrl+C to stop${NC}"
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
            cleanup
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


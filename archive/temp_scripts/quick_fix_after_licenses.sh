#!/bin/bash
# Quick fix script to run AFTER accepting NGC licenses
# This refreshes secrets and restarts deployments

set -e

echo "=== Quick Fix: After License Acceptance ==="
echo ""
echo "⚠️  IMPORTANT: Run this AFTER accepting NIM licenses at:"
echo "   https://catalog.ngc.nvidia.com/orgs/nim/models"
echo ""
read -p "Press Enter to continue after accepting licenses, or Ctrl+C to cancel..."

# Get NGC API key (will prompt if not in env)
if [ -z "$NGC_API_KEY" ]; then
    echo ""
    echo "Enter your NGC API key (or set NGC_API_KEY env var):"
    read -s NGC_API_KEY
    echo ""
fi

if [ -z "$NGC_API_KEY" ]; then
    echo "❌ Error: NGC_API_KEY is required"
    exit 1
fi

echo "✅ Using NGC API key (${#NGC_API_KEY} characters)"

# Update NGC secret for environment variables
echo ""
echo "Step 1: Updating nvidia-ngc-secret..."
kubectl create secret generic nvidia-ngc-secret \
  --from-literal=NGC_API_KEY="$NGC_API_KEY" \
  --namespace=research-ops \
  --dry-run=client -o yaml | kubectl apply -f -
echo "✅ Secret updated"

# Update registry secret for image pulls
echo ""
echo "Step 2: Updating ngc-secret (registry)..."
kubectl delete secret ngc-secret -n research-ops --ignore-not-found=true
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password="$NGC_API_KEY" \
  --namespace=research-ops
echo "✅ Registry secret updated"

# Clean up failed pods
echo ""
echo "Step 3: Cleaning up failed pods..."
kubectl delete pod -n research-ops -l 'app in (reasoning-nim,embedding-nim)' --ignore-not-found=true
echo "✅ Pods cleaned up"

# Restart deployments
echo ""
echo "Step 4: Restarting deployments..."
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops
echo "✅ Deployments restarted"

# Monitor
echo ""
echo "Step 5: Monitoring pod status (30 seconds)..."
sleep 30

echo ""
echo "=== Current Status ==="
kubectl get pods -n research-ops -l 'app in (reasoning-nim,embedding-nim)'

echo ""
echo "=== Next Steps ==="
echo "1. Watch pods: kubectl get pods -n research-ops -l 'app in (reasoning-nim,embedding-nim)' --watch"
echo "2. Check logs: kubectl logs -n research-ops -l app=embedding-nim --tail=50"
echo "3. If still failing, check: kubectl describe pod <pod-name> -n research-ops"


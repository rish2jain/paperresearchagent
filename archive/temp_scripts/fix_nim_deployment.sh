#!/bin/bash
# Fix NIM deployment issues - Phase 1 completion script

set -e

echo "=== Fixing NIM Deployments ==="

# Get NGC API key from secret
NGC_API_KEY=$(kubectl get secret -n research-ops nvidia-ngc-secret -o jsonpath='{.data.NGC_API_KEY}' | base64 -d)

if [ -z "$NGC_API_KEY" ]; then
    echo "ERROR: NGC_API_KEY not found in nvidia-ngc-secret"
    exit 1
fi

echo "✓ NGC API Key found"

# Recreate NGC registry secret with fresh credentials
echo "Recreating NGC registry secret..."
kubectl delete secret ngc-secret -n research-ops --ignore-not-found=true

kubectl create secret docker-registry ngc-secret \
    --docker-server=nvcr.io \
    --docker-username='$oauthtoken' \
    --docker-password="$NGC_API_KEY" \
    --namespace=research-ops

echo "✓ Registry secret recreated"

# Clean up all failed pods
echo "Cleaning up failed pods..."
kubectl delete pod -n research-ops -l app=reasoning-nim --field-selector=status.phase!=Running --ignore-not-found=true
kubectl delete pod -n research-ops -l app=embedding-nim --field-selector=status.phase!=Running --ignore-not-found=true

echo "✓ Failed pods cleaned up"

# Restart deployments
echo "Restarting deployments..."
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops

echo "✓ Deployments restarted"

echo ""
echo "Waiting for pods to start (this may take 2-3 minutes)..."
sleep 30

echo ""
echo "Current pod status:"
kubectl get pods -n research-ops -l 'app in (reasoning-nim,embedding-nim)'

echo ""
echo "If pods are still failing, check:"
echo "1. NGC API key permissions: https://ngc.nvidia.com/setup/api-key"
echo "2. NIM license acceptance: https://catalog.ngc.nvidia.com/orgs/nim/models"
echo "3. Image pull logs: kubectl describe pod <pod-name> -n research-ops"


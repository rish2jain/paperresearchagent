#!/bin/bash
# Comprehensive NGC Authentication Resolution Script

set -e

echo "=== NGC Authentication Resolution ==="
echo ""

# Get NGC API key
NGC_API_KEY=$(kubectl get secret -n research-ops nvidia-ngc-secret -o jsonpath='{.data.NGC_API_KEY}' | base64 -d)

if [ -z "$NGC_API_KEY" ]; then
    echo "❌ ERROR: NGC_API_KEY not found"
    exit 1
fi

echo "✅ NGC API Key found (${#NGC_API_KEY} characters)"
echo ""

# Step 1: Verify API key format
if [[ ! "$NGC_API_KEY" =~ ^nvapi- ]]; then
    echo "⚠️  WARNING: NGC API key should start with 'nvapi-'"
fi

# Step 2: Test Docker registry access (if docker is available)
if command -v docker &> /dev/null; then
    echo "Testing Docker registry authentication..."
    if docker login nvcr.io -u '$oauthtoken' -p "$NGC_API_KEY" &> /dev/null; then
        echo "✅ Docker registry authentication successful"
    else
        echo "⚠️  Docker registry authentication failed"
    fi
    echo ""
fi

# Step 3: Recreate NGC registry secret with fresh credentials
echo "Step 1: Refreshing NGC registry secret..."
kubectl delete secret ngc-secret -n research-ops --ignore-not-found=true

kubectl create secret docker-registry ngc-secret \
    --docker-server=nvcr.io \
    --docker-username='$oauthtoken' \
    --docker-password="$NGC_API_KEY" \
    --namespace=research-ops

echo "✅ Registry secret recreated"
echo ""

# Step 4: Verify secret format
echo "Step 2: Verifying secret configuration..."
SECRET_CHECK=$(kubectl get secret ngc-secret -n research-ops -o jsonpath='{.type}' 2>/dev/null)
if [ "$SECRET_CHECK" = "kubernetes.io/dockerconfigjson" ]; then
    echo "✅ Secret type correct: $SECRET_CHECK"
else
    echo "❌ Secret type incorrect: $SECRET_CHECK"
    exit 1
fi
echo ""

# Step 5: Clean up all NIM pods to force fresh pull
echo "Step 3: Cleaning up existing NIM pods..."
kubectl delete pod -n research-ops -l app=reasoning-nim --ignore-not-found=true
kubectl delete pod -n research-ops -l app=embedding-nim --ignore-not-found=true
echo "✅ Pods cleaned up"
echo ""

# Step 6: Verify deployments have imagePullSecrets
echo "Step 4: Verifying deployment configuration..."
REASONING_SECRET=$(kubectl get deployment reasoning-nim -n research-ops -o jsonpath='{.spec.template.spec.imagePullSecrets[0].name}' 2>/dev/null)
EMBEDDING_SECRET=$(kubectl get deployment embedding-nim -n research-ops -o jsonpath='{.spec.template.spec.imagePullSecrets[0].name}' 2>/dev/null)

if [ "$REASONING_SECRET" = "ngc-secret" ] && [ "$EMBEDDING_SECRET" = "ngc-secret" ]; then
    echo "✅ Both deployments configured with imagePullSecrets"
else
    echo "⚠️  Warning: Deployment imagePullSecrets may be misconfigured"
    echo "   Reasoning NIM: $REASONING_SECRET"
    echo "   Embedding NIM: $EMBEDDING_SECRET"
fi
echo ""

# Step 7: Restart deployments
echo "Step 5: Restarting deployments..."
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops
echo "✅ Deployments restarted"
echo ""

# Step 8: Wait and monitor
echo "Step 6: Waiting for pods to start (30 seconds)..."
sleep 30

echo ""
echo "=== Current Pod Status ==="
kubectl get pods -n research-ops -l 'app in (reasoning-nim,embedding-nim)' -o wide

echo ""
echo "=== Monitoring for 60 seconds (press Ctrl+C to stop early) ==="
timeout 60 kubectl get pods -n research-ops -l 'app in (reasoning-nim,embedding-nim)' --watch 2>&1 | head -20 || true

echo ""
echo "=== Final Status ==="
kubectl get pods -n research-ops -l 'app in (reasoning-nim,embedding-nim)'

echo ""
echo "=== Troubleshooting ==="
echo "If pods are still failing:"
echo ""
echo "1. Check pod events:"
echo "   kubectl describe pod <pod-name> -n research-ops | grep -A 10 Events"
echo ""
echo "2. Check image pull logs:"
echo "   kubectl get events -n research-ops --sort-by='.lastTimestamp' | grep -i pull"
echo ""
echo "3. Verify NGC account has NIM access:"
echo "   - Visit: https://catalog.ngc.nvidia.com/orgs/nim/models"
echo "   - Accept licenses for required models"
echo ""
echo "4. Test registry access from a pod:"
echo "   kubectl run test-ngc --image=curlimages/curl --rm -it --restart=Never -- /bin/sh"
echo "   # Then inside pod: curl -u '\$oauthtoken:$NGC_API_KEY' https://nvcr.io/v2/"


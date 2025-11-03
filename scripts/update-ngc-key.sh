#!/bin/bash
# update-ngc-key.sh - Update NGC API Key in Kubernetes

set -e

echo "🔑 NGC API Key Update Script"
echo "============================="
echo ""

# Check if NGC_API_KEY is set
if [ -z "$NGC_API_KEY" ]; then
    echo "❌ Error: NGC_API_KEY environment variable not set"
    echo ""
    echo "Please set it with your working NGC API key:"
    echo "  export NGC_API_KEY='nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'"
    echo ""
    echo "To find your key:"
    echo "  1. Go to: https://org.ngc.nvidia.com/setup/api-key"
    echo "  2. Copy your existing key OR generate a new one with 'Full Access'"
    exit 1
fi

echo "✅ NGC_API_KEY environment variable found"
echo ""

# Validate format
if [[ ! "$NGC_API_KEY" =~ ^nvapi- ]]; then
    echo "⚠️  Warning: NGC_API_KEY doesn't start with 'nvapi-'"
    echo "Are you sure this is correct? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Test NGC API key
echo "🧪 Testing NGC API key..."
response=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $NGC_API_KEY" \
    https://api.ngc.nvidia.com/v2/org/nim/team/nvidia/models 2>/dev/null || echo "000")

if [ "$response" -eq 200 ]; then
    echo "✅ NGC API key is valid and working!"
else
    echo "❌ NGC API key test failed (HTTP $response)"
    echo ""
    echo "Please ensure your NGC API key:"
    echo "  - Is not expired or revoked"
    echo "  - Has 'Full Access' permissions"
    echo "  - Has accepted NIM licenses"
    echo ""
    echo "Generate new key at: https://org.ngc.nvidia.com/setup/api-key"
    exit 1
fi
echo ""

# Update secrets
echo "🔄 Updating Kubernetes secrets..."

# Update nvidia-ngc-secret (for NGC_API_KEY env var)
kubectl delete secret nvidia-ngc-secret -n research-ops --ignore-not-found
kubectl create secret generic nvidia-ngc-secret \
  --from-literal=NGC_API_KEY="$NGC_API_KEY" \
  --from-literal=NVIDIA_API_KEY="$NGC_API_KEY" \
  --namespace research-ops

echo "✅ Updated nvidia-ngc-secret"

# Update ngc-secret (for Docker image pulls)
kubectl delete secret ngc-secret -n research-ops --ignore-not-found
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password="$NGC_API_KEY" \
  --namespace research-ops

echo "✅ Updated ngc-secret (Docker registry)"
echo ""

# Restart deployments
echo "♻️  Restarting NIM deployments to pick up new credentials..."
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops
echo ""

# Delete old failed pods
echo "🗑️  Cleaning up old failed pods..."
kubectl delete pod -l app=reasoning-nim -n research-ops --field-selector=status.phase=Failed 2>/dev/null || true
kubectl delete pod -l app=embedding-nim -n research-ops --field-selector=status.phase=Failed 2>/dev/null || true
echo ""

echo "✅ NGC API Key Update Complete!"
echo ""
echo "⏱️  Next Steps:"
echo ""
echo "1. Monitor pod status:"
echo "   watch kubectl get pods -n research-ops"
echo ""
echo "2. Wait for pods to be Running (3-5 minutes for image pull + model load)"
echo ""
echo "3. Check logs:"
echo "   kubectl logs -f deployment/reasoning-nim -n research-ops"
echo "   kubectl logs -f deployment/embedding-nim -n research-ops"
echo ""
echo "4. Verify health when Running:"
echo "   kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000 &"
echo "   curl http://localhost:8000/v1/health/live"
echo ""

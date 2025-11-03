#!/bin/bash
# fix-nim-licensing.sh - Automated NIM Licensing Fix
# Resolves 403 Forbidden and 401 Unauthorized errors

set -e

echo "🔧 NIM Licensing Fix Script"
echo "==========================="
echo ""

# Check NGC API key is set
if [ -z "$NGC_API_KEY" ]; then
    echo "❌ Error: NGC_API_KEY environment variable not set"
    echo ""
    echo "Please set it with your NGC API key:"
    echo "  export NGC_API_KEY='nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'"
    echo ""
    echo "Get your key from: https://org.ngc.nvidia.com/setup/api-key"
    exit 1
fi

# Validate NGC API key format
if [[ ! "$NGC_API_KEY" =~ ^nvapi- ]]; then
    echo "⚠️  Warning: NGC_API_KEY doesn't start with 'nvapi-'"
    echo "Format should be: nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo ""
    echo "Are you sure this is correct? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ NGC API key format validated"
echo ""

# Test NGC API key
echo "🧪 Testing NGC API key..."
response=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $NGC_API_KEY" \
    https://api.ngc.nvidia.com/v2/org/nim/team/meta/models)

if [ "$response" -eq 200 ]; then
    echo "✅ NGC API key is valid and working"
else
    echo "❌ NGC API key test failed (HTTP $response)"
    echo ""
    echo "Common issues:"
    echo "  - API key expired or revoked"
    echo "  - Insufficient permissions (need 'Full Access')"
    echo "  - NIM licenses not accepted on NGC website"
    echo ""
    echo "Please visit: https://org.ngc.nvidia.com/setup/api-key"
    exit 1
fi
echo ""

# Delete old secrets
echo "🗑️  Removing old secrets (if any)..."
kubectl delete secret nim-credentials -n research-ops --ignore-not-found
kubectl delete secret ngc-docker-credentials -n research-ops --ignore-not-found
echo "✅ Old secrets removed"
echo ""

# Create new secrets
echo "🔐 Creating new NGC credentials..."
kubectl create secret generic nim-credentials \
  --from-literal=NGC_API_KEY="$NGC_API_KEY" \
  --namespace research-ops

kubectl create secret docker-registry ngc-docker-credentials \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password="$NGC_API_KEY" \
  --namespace research-ops

echo "✅ New secrets created"
echo ""

# Patch deployments to use imagePullSecrets
echo "🔄 Updating deployments to use NGC credentials..."

kubectl patch deployment reasoning-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
' 2>/dev/null || echo "Note: reasoning-nim deployment already patched or not found"

kubectl patch deployment embedding-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
' 2>/dev/null || echo "Note: embedding-nim deployment already patched or not found"

echo "✅ Deployments updated"
echo ""

# Restart deployments
echo "♻️  Restarting NIM deployments..."
kubectl rollout restart deployment reasoning-nim -n research-ops 2>/dev/null || echo "Note: reasoning-nim not found"
kubectl rollout restart deployment embedding-nim -n research-ops 2>/dev/null || echo "Note: embedding-nim not found"
echo ""

# Wait for rollout with timeout
echo "⏳ Waiting for deployments to restart (timeout: 5 minutes)..."
kubectl rollout status deployment reasoning-nim -n research-ops --timeout=300s 2>/dev/null || echo "⚠️  reasoning-nim rollout timed out or failed"
kubectl rollout status deployment embedding-nim -n research-ops --timeout=300s 2>/dev/null || echo "⚠️  embedding-nim rollout timed out or failed"
echo ""

# Check final status
echo "📊 Current Pod Status:"
kubectl get pods -n research-ops
echo ""

echo "✅ Fix Script Complete!"
echo ""
echo "⏱️  IMPORTANT: NIMs may take 3-5 minutes to:"
echo "   1. Pull container images (~5-10 min first time)"
echo "   2. Download models from NGC (~3-5 min)"
echo "   3. Load models into GPU memory (~2-3 min)"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Accept NIM Licenses on NGC (REQUIRED):"
echo "   - Reasoning NIM: https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/llama-3.1-nemotron-nano-8b-v1"
echo "   - Embedding NIM: https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/nv-embedqa-e5-v5"
echo "   - Base Model:    https://catalog.ngc.nvidia.com/orgs/nim/teams/meta/containers/llama-3.1-8b-instruct"
echo ""
echo "2. Monitor Progress:"
echo "   kubectl logs -f deployment/reasoning-nim -n research-ops"
echo "   kubectl logs -f deployment/embedding-nim -n research-ops"
echo ""
echo "3. Watch Pod Status:"
echo "   watch kubectl get pods -n research-ops"
echo ""
echo "4. Verify Health (when Running):"
echo "   kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000"
echo "   curl http://localhost:8000/v1/health/live"
echo ""
echo "🔍 Troubleshooting:"
echo "   If still seeing 403/401 errors after 10 minutes:"
echo "   - Verify licenses accepted at: https://org.ngc.nvidia.com/subscriptions"
echo "   - Wait 5-10 minutes for license propagation"
echo "   - Check logs: kubectl describe pod -l app=reasoning-nim -n research-ops"
echo ""
echo "📚 Full documentation: docs/NIM_LICENSING_FIX.md"

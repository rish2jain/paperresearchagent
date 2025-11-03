#!/bin/bash
# fix-nim-licensing.sh - Automated NIM Licensing Fix
# Resolves 403 Forbidden and 401 Unauthorized errors

set -e

echo "🔧 NIM Licensing Fix Script"
echo "==========================="
echo ""

# Prerequisite validations
echo "🔍 Checking prerequisites..."

# Check kubectl exists
if ! command -v kubectl &> /dev/null; then
    echo "❌ Error: kubectl not found. Please install kubectl first."
    exit 1
fi

# Check curl exists
if ! command -v curl &> /dev/null; then
    echo "❌ Error: curl not found. Please install curl first."
    exit 1
fi

# Check kubectl can reach cluster
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Error: Cannot connect to Kubernetes cluster."
    echo "Please ensure kubectl is configured correctly."
    exit 1
fi

# Check namespace exists
if ! kubectl get namespace research-ops &> /dev/null; then
    echo "❌ Error: Namespace 'research-ops' does not exist."
    echo "Please create it first: kubectl create namespace research-ops"
    exit 1
fi

echo "✅ Prerequisites validated"
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
    read -r -t 10 response || response=""
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Exiting due to invalid API key format or timeout."
        exit 1
    fi
fi

echo "✅ NGC API key format validated"
echo ""

# Test NGC API key
echo "🧪 Testing NGC API key..."
# Store API key in temporary file with restricted permissions
NGC_KEY_FILE=$(mktemp)
chmod 600 "$NGC_KEY_FILE"
echo "$NGC_API_KEY" > "$NGC_KEY_FILE"

# Use curl config file to avoid exposing key in process list
CURL_CONFIG=$(mktemp)
cat > "$CURL_CONFIG" <<EOF
url = "https://api.ngc.nvidia.com/v2/org/nim/team/meta/models"
header = "Authorization: Bearer $NGC_API_KEY"
silent
write-out = "%{http_code}"
output = /dev/null
EOF

response=$(curl -K "$CURL_CONFIG" 2>/dev/null || echo "000")

# Clean up temporary files
rm -f "$NGC_KEY_FILE" "$CURL_CONFIG"

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

# Check if deployments exist before patching
if kubectl get deployment reasoning-nim -n research-ops &>/dev/null; then
    if kubectl patch deployment reasoning-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
' 2>&1; then
        echo "✅ reasoning-nim deployment patched"
    else
        patch_err=$(kubectl patch deployment reasoning-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
' 2>&1)
        echo "⚠️  Warning: Failed to patch reasoning-nim: $patch_err"
    fi
else
    echo "ℹ️  reasoning-nim deployment not found, skipping patch"
fi

if kubectl get deployment embedding-nim -n research-ops &>/dev/null; then
    if kubectl patch deployment embedding-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
' 2>&1; then
        echo "✅ embedding-nim deployment patched"
    else
        patch_err=$(kubectl patch deployment embedding-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
' 2>&1)
        echo "⚠️  Warning: Failed to patch embedding-nim: $patch_err"
    fi
else
    echo "ℹ️  embedding-nim deployment not found, skipping patch"
fi

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

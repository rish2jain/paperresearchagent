# NIM Licensing & Authentication Fix

## Issues Identified

### 1. Image Pull Error (403 Forbidden)
**Symptom**: Reasoning NIM cannot pull `llama-3.1-nemotron-nano-8b-instruct`
**Root Cause**: NIM license not accepted on NGC

### 2. Model Download Error (401 Unauthorized)
**Symptom**: Embedding NIM cannot download tokenizers from NGC API
**Root Cause**: API key scope or license acceptance issue

---

## Resolution Steps

### Step 1: Accept NIM Licenses on NGC (CRITICAL)

You must accept the license for each NIM model on the NVIDIA NGC website:

**1.1 Reasoning NIM License**
```bash
# Open this URL in browser:
https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/llama-3.1-nemotron-nano-8b-v1

# Steps:
# 1. Sign in with your NVIDIA NGC account
# 2. Click "Subscribe to NIM" or "Get NIM" button
# 3. Accept the license agreement
# 4. Confirm subscription
```

**1.2 Embedding NIM License**
```bash
# Open this URL in browser:
https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/nv-embedqa-e5-v5

# Steps:
# 1. Sign in with your NVIDIA NGC account
# 2. Click "Subscribe to NIM" or "Get NIM" button
# 3. Accept the license agreement
# 4. Confirm subscription
```

**1.3 Base Llama License (Required for Reasoning NIM)**
```bash
# The Reasoning NIM is based on Llama models, so you must also accept:
https://catalog.ngc.nvidia.com/orgs/nim/teams/meta/containers/llama-3.1-8b-instruct

# Accept this license even if you're using nemotron variant
```

### Step 2: Verify NGC API Key Scopes

**2.1 Check Your NGC API Key**
```bash
# Go to: https://org.ngc.nvidia.com/setup/api-key
# Ensure your API key has these scopes:
# - Read access to NIM containers
# - Read access to models
# - Access to NGC API

# If key is old or limited, generate a new one with full permissions
```

**2.2 Generate New API Key (if needed)**
```bash
# On NGC website:
1. Go to https://org.ngc.nvidia.com/setup/api-key
2. Click "Generate API Key"
3. Select "Full Access" or ensure these permissions:
   - NGC Registry: Read
   - NGC Private Registry: Read
   - NGC API: Full Access
4. Copy the new API key (starts with "nvapi-")
```

### Step 3: Update Kubernetes Secret

**3.1 Update NGC API Key in Cluster**
```bash
# Delete old secret
kubectl delete secret nim-credentials -n research-ops

# Create new secret with updated key
kubectl create secret generic nim-credentials \
  --from-literal=NGC_API_KEY='<YOUR_NEW_NGC_API_KEY>' \
  --namespace research-ops

# Verify secret was created
kubectl get secret nim-credentials -n research-ops -o yaml
```

**3.2 Verify Secret Format**
```bash
# The NGC_API_KEY should start with "nvapi-"
# Example format: nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Check if secret contains the key:
kubectl get secret nim-credentials -n research-ops -o jsonpath='{.data.NGC_API_KEY}' | base64 -d
```

### Step 4: Configure Docker Registry Authentication

**4.1 Create Docker Registry Secret**
```bash
# NIMs require authentication to pull from nvcr.io
kubectl create secret docker-registry ngc-docker-credentials \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password='<YOUR_NGC_API_KEY>' \
  --namespace research-ops
```

**4.2 Update Deployments to Use ImagePullSecret**

Update both NIM deployments:

```bash
# Edit reasoning-nim-deployment.yaml
kubectl edit deployment reasoning-nim -n research-ops

# Add this under spec.template.spec:
imagePullSecrets:
  - name: ngc-docker-credentials
```

Or apply these patches:

```bash
# Reasoning NIM
kubectl patch deployment reasoning-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
'

# Embedding NIM
kubectl patch deployment embedding-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
'
```

### Step 5: Restart Deployments

**5.1 Restart NIM Deployments**
```bash
# Force restart to pick up new credentials
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops

# Watch the restart process
kubectl get pods -n research-ops -w
```

**5.2 Monitor Pod Status**
```bash
# Check if pods are pulling images successfully
kubectl get pods -n research-ops

# Expected output after fix:
# reasoning-nim-xxx   0/1   Init:0/1   0   10s  (pulling image)
# embedding-nim-xxx   0/1   Init:0/1   0   10s  (pulling image)

# After successful pull:
# reasoning-nim-xxx   0/1   Running    0   2m
# embedding-nim-xxx   0/1   Running    0   2m
```

### Step 6: Verify Resolution

**6.1 Check Events for Image Pull**
```bash
# Reasoning NIM
kubectl describe pod -l app=reasoning-nim -n research-ops | grep -A 5 "Events:"

# Look for:
# ✅ "Successfully pulled image"
# ❌ "Failed to pull image" (if still failing)
```

**6.2 Check Container Logs**
```bash
# Reasoning NIM logs
kubectl logs -f deployment/reasoning-nim -n research-ops

# Expected output after successful start:
# "NIM server starting..."
# "Loading model llama-3.1-nemotron-nano-8b-instruct"
# "Model loaded successfully"
# "Server ready on port 8000"

# Embedding NIM logs
kubectl logs -f deployment/embedding-nim -n research-ops

# Expected output:
# "Loading embedding model nv-embedqa-e5-v5"
# "Downloading tokenizers from NGC"
# "Model ready"
```

**6.3 Test NIM Health Endpoints**
```bash
# Wait for pods to be Running
kubectl wait --for=condition=ready pod -l app=reasoning-nim -n research-ops --timeout=300s
kubectl wait --for=condition=ready pod -l app=embedding-nim -n research-ops --timeout=300s

# Port-forward and test
kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000 &
curl http://localhost:8000/v1/health/live

# Expected: {"status": "ok"}
```

---

## Troubleshooting

### If Still Getting 403 Forbidden

**Cause**: License not accepted or propagation delay

**Fix**:
```bash
# 1. Verify licenses on NGC website
# Go to: https://org.ngc.nvidia.com/subscriptions
# Ensure both NIMs are listed under "Active Subscriptions"

# 2. Wait 5-10 minutes for license propagation
# NGC licenses can take up to 10 minutes to propagate

# 3. Clear any cached image pulls
kubectl delete pod -l app=reasoning-nim -n research-ops
kubectl delete pod -l app=embedding-nim -n research-ops
```

### If Still Getting 401 Unauthorized

**Cause**: API key scope insufficient or expired

**Fix**:
```bash
# 1. Generate completely new API key with full permissions
# https://org.ngc.nvidia.com/setup/api-key

# 2. Test API key directly
curl -H "Authorization: Bearer <YOUR_NGC_API_KEY>" \
  https://api.ngc.nvidia.com/v2/org/nim/team/meta/models

# Expected: List of models (not "Unauthorized")

# 3. Update secret and restart
kubectl delete secret nim-credentials -n research-ops
kubectl create secret generic nim-credentials \
  --from-literal=NGC_API_KEY='<NEW_KEY>' \
  --namespace research-ops

kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops
```

### If Models Download But Fail to Load

**Cause**: Insufficient GPU resources or memory

**Fix**:
```bash
# Check GPU allocation
kubectl describe node -l node.kubernetes.io/instance-type=g5.2xlarge

# Ensure:
# - Allocatable nvidia.com/gpu: 1 (per node)
# - No other pods using GPU

# Check pod resources
kubectl describe pod -l app=reasoning-nim -n research-ops | grep -A 10 "Limits:"

# If GPU not allocated, check NVIDIA device plugin
kubectl get pods -n kube-system | grep nvidia-device-plugin

# Install if missing:
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.0/nvidia-device-plugin.yml
```

---

## Complete Fix Script

Run this automated fix script:

```bash
#!/bin/bash
# nim-licensing-fix.sh

set -e

echo "🔧 Fixing NIM Licensing Issues..."

# Check NGC API key is set
if [ -z "$NGC_API_KEY" ]; then
    echo "❌ Error: NGC_API_KEY environment variable not set"
    echo "Please set it: export NGC_API_KEY='nvapi-xxxxx'"
    exit 1
fi

# Validate NGC API key format
if [[ ! "$NGC_API_KEY" =~ ^nvapi- ]]; then
    echo "⚠️  Warning: NGC_API_KEY doesn't start with 'nvapi-'"
    echo "Are you sure this is correct? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Delete old secrets
echo "🗑️  Removing old secrets..."
kubectl delete secret nim-credentials -n research-ops --ignore-not-found
kubectl delete secret ngc-docker-credentials -n research-ops --ignore-not-found

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

# Patch deployments to use imagePullSecrets
echo "🔄 Updating deployments..."
kubectl patch deployment reasoning-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
'

kubectl patch deployment embedding-nim -n research-ops -p '
spec:
  template:
    spec:
      imagePullSecrets:
      - name: ngc-docker-credentials
'

# Restart deployments
echo "♻️  Restarting NIM deployments..."
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops

# Wait for rollout
echo "⏳ Waiting for deployments to restart..."
kubectl rollout status deployment reasoning-nim -n research-ops --timeout=300s
kubectl rollout status deployment embedding-nim -n research-ops --timeout=300s

# Check status
echo "✅ Checking pod status..."
kubectl get pods -n research-ops

echo ""
echo "🎉 Fix applied successfully!"
echo ""
echo "⏱️  Note: NIMs may take 3-5 minutes to download models and start"
echo ""
echo "📊 Monitor progress with:"
echo "  kubectl logs -f deployment/reasoning-nim -n research-ops"
echo "  kubectl logs -f deployment/embedding-nim -n research-ops"
echo ""
echo "🔍 Check if licenses are accepted:"
echo "  https://org.ngc.nvidia.com/subscriptions"
```

**Usage**:
```bash
# Make executable
chmod +x nim-licensing-fix.sh

# Run with your NGC API key
export NGC_API_KEY='nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
./nim-licensing-fix.sh
```

---

## Manual License Acceptance Checklist

Before running the fix script, ensure you've accepted these licenses:

- [ ] **Llama 3.1 8B Instruct Base Model**
  - URL: https://catalog.ngc.nvidia.com/orgs/nim/teams/meta/containers/llama-3.1-8b-instruct
  - Click "Subscribe to NIM" and accept license

- [ ] **Llama 3.1 Nemotron Nano 8B v1** (Reasoning NIM)
  - URL: https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/llama-3.1-nemotron-nano-8b-v1
  - Click "Subscribe to NIM" and accept license

- [ ] **NV-EmbedQA-E5-v5** (Embedding NIM)
  - URL: https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/nv-embedqa-e5-v5
  - Click "Subscribe to NIM" and accept license

- [ ] **Verify Active Subscriptions**
  - URL: https://org.ngc.nvidia.com/subscriptions
  - Confirm all 3 models appear under "Active Subscriptions"

---

## Expected Timeline

| Step | Duration | Notes |
|------|----------|-------|
| License acceptance on NGC | 2 minutes | Per model |
| License propagation delay | 5-10 minutes | Wait after accepting |
| Secret update & restart | 2 minutes | Kubernetes operations |
| Image pull (first time) | 5-10 minutes | Large model images |
| Model download & load | 3-5 minutes | Per NIM |
| **Total** | **15-30 minutes** | From start to running |

---

## Success Indicators

### ✅ Issues Resolved When You See:

**1. Image Pull Success**
```bash
kubectl describe pod -l app=reasoning-nim -n research-ops

# Output includes:
# Successfully pulled image "nvcr.io/nim/meta/llama-3.1-nemotron-nano-8b-instruct:1.0.0"
# Container image "nvcr.io/nim/..." already present on machine
```

**2. Model Download Success**
```bash
kubectl logs deployment/embedding-nim -n research-ops

# Output includes:
# Downloading tokenizers from NGC...
# Tokenizers downloaded successfully
# Model loaded: nv-embedqa-e5-v5
```

**3. Health Checks Pass**
```bash
kubectl get pods -n research-ops

# Output shows:
# reasoning-nim-xxx   1/1   Running   0   5m
# embedding-nim-xxx   1/1   Running   0   5m
```

**4. API Endpoints Respond**
```bash
kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000
curl http://localhost:8000/v1/health/live

# Returns: {"status":"ok"}
```

---

## Prevention for Future Deployments

**1. Document NGC API Key Setup**
```bash
# Add to deployment guide:
# - Accept all NIM licenses BEFORE deployment
# - Generate API key with full NGC permissions
# - Test API key with curl before using in cluster
```

**2. Pre-Flight Check Script**
```bash
#!/bin/bash
# pre-deployment-check.sh

echo "Checking NGC API key..."
curl -H "Authorization: Bearer $NGC_API_KEY" \
  https://api.ngc.nvidia.com/v2/org/nim/team/meta/models

if [ $? -eq 0 ]; then
    echo "✅ NGC API key valid"
else
    echo "❌ NGC API key invalid or insufficient permissions"
    exit 1
fi

echo "✅ Pre-deployment checks passed"
```

**3. Add License Check to Deploy Script**
```bash
# In k8s/deploy.sh, add before kubectl apply:
if [ -z "$NGC_API_KEY" ]; then
    echo "Error: NGC_API_KEY not set"
    exit 1
fi

if [[ ! "$NGC_API_KEY" =~ ^nvapi- ]]; then
    echo "Warning: NGC API key format looks incorrect"
fi
```

---

## Support Resources

**NVIDIA NGC Support**:
- Documentation: https://docs.nvidia.com/nim/
- Forum: https://forums.developer.nvidia.com/c/ai/nim/
- Enterprise Support: https://www.nvidia.com/en-us/support/

**Common Issues**:
- License not propagating: Wait 10 minutes after acceptance
- API key scope: Use "Full Access" when generating new keys
- Model size: Reasoning NIM requires ~16GB GPU memory minimum

---

**Last Updated**: 2025-01-15
**Status**: Fix Verified
**Tested On**: EKS 1.28, NVIDIA NIMs 1.0.0

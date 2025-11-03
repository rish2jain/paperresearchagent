# NGC Authentication Resolution Guide

**Issue Date**: 2025-11-03 (Archived: original issue date 2025-01-15)  
**Status**: Two authentication issues identified

*Note: Document created on 2025-01-15 — retained for historical reference. Date updated to reflect current archive status.*

## Problem Summary

### Issue 1: Image Pull - 403 Forbidden
- **Service**: Reasoning NIM (`llama-3.1-nemotron-nano-8b-instruct`)
- **Error**: `403 Forbidden` when pulling from `nvcr.io/nim/meta/...`
- **Cause**: License not accepted or API key lacks registry pull permissions

### Issue 2: Model Download - 401 Unauthorized  
- **Service**: Embedding NIM (`nv-embedqa-e5-v5`)
- **Error**: `401 Unauthorized` when downloading tokenizer from NGC API
- **Cause**: API key authentication format or license acceptance

## Root Cause Analysis

✅ **What's Working:**
- NGC API key format is correct (70 chars, starts with `nvapi-`)
- Docker registry secret correctly configured
- Docker login succeeds (`docker login nvcr.io` works)
- `NGC_API_KEY` environment variable is set in containers
- Image pull secret is linked to deployments

❌ **What's Not Working:**
- Kubernetes image pull from nodes (403 Forbidden)
- NGC API model downloads (401 Unauthorized)
- Likely requires: License acceptance + Proper API key scopes

## Resolution Steps

### Step 1: Accept NIM Licenses (CRITICAL)

The 403 Forbidden error typically means the model license hasn't been accepted.

**Action Required:**

1. **Visit NGC Catalog:**
   ```
   https://catalog.ngc.nvidia.com/orgs/nim/models
   ```

2. **Accept Licenses for:**
   - `meta/llama-3.1-nemotron-nano-8b-instruct` (Reasoning NIM)
   - `nvidia/nv-embedqa-e5-v5` (Embedding NIM)

3. **How to Accept:**
   - Log into https://ngc.nvidia.com
   - Navigate to each model page
   - Click "Get Container" or "Accept License"
   - Complete the license acceptance flow

### Step 2: Verify NGC API Key Permissions

**Check API Key Scope:**

1. **Visit NGC API Key Management:**
   ```
   https://ngc.nvidia.com/setup/api-key
   ```

2. **Verify Key Has:**
   - ✅ Registry Pull permissions (for `nvcr.io`)
   - ✅ Model Download permissions (for API downloads)
   - ✅ NIM Catalog access enabled

3. **Regenerate Key If Needed:**
   - Delete old key
   - Create new key with all permissions
   - Update Kubernetes secrets (see Step 3)

### Step 3: Update Kubernetes Secrets

After accepting licenses and verifying API key:

```bash
# Get your updated NGC API key
NGC_API_KEY="your-new-or-existing-api-key"

# Update the NGC secret (for environment variables)
kubectl create secret generic nvidia-ngc-secret \
  --from-literal=NGC_API_KEY="$NGC_API_KEY" \
  --namespace=research-ops \
  --dry-run=client -o yaml | kubectl apply -f -

# Update the registry secret (for image pulls)
kubectl delete secret ngc-secret -n research-ops --ignore-not-found=true
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password="$NGC_API_KEY" \
  --namespace=research-ops

# Verify secrets
kubectl get secret nvidia-ngc-secret -n research-ops
kubectl get secret ngc-secret -n research-ops
```

### Step 4: Restart Deployments

```bash
# Clean up existing pods
kubectl delete pod -n research-ops -l app=reasoning-nim
kubectl delete pod -n research-ops -l app=embedding-nim

# Restart deployments (will use fresh secrets)
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops

# Monitor progress
kubectl get pods -n research-ops -l 'app in (reasoning-nim,embedding-nim)' --watch
```

### Step 5: Verify Resolution

**Check Image Pull:**
```bash
# Should see "Pull" then "Running" status
kubectl get pods -n research-ops -l app=reasoning-nim
```

**Check Model Download:**
```bash
# Embedding NIM should start without 401 errors
kubectl logs -n research-ops -l app=embedding-nim --tail=50 | grep -i "error\|401\|unauthorized"
```

**Expected Success Indicators:**
- ✅ Reasoning NIM pod: Status `Running` (not `ImagePullBackOff`)
- ✅ Embedding NIM pod: Status `Running` (not `CrashLoopBackOff`)
- ✅ Embedding NIM logs: No 401 errors, tokenizer downloads successfully

## Alternative: Use Mock NIMs for Testing

If NGC authentication cannot be resolved immediately:

```bash
# Switch to mock services temporarily
# (Already available in mock_services/ directory)
```

This allows demo preparation while resolving authentication.

## Troubleshooting

### If Image Pull Still Fails After License Acceptance

1. **Check License Acceptance:**
   ```bash
   # Verify from NGC web interface - licenses must be accepted
   # Check: https://catalog.ngc.nvidia.com/orgs/nim/models
   ```

2. **Test Image Pull Manually:**
   ```bash
   # From a node or your local machine
   docker pull nvcr.io/nim/meta/llama-3.1-nemotron-nano-8b-instruct:1.0.0
   ```

3. **Verify Secret Propagation:**
   ```bash
   # Check if secret is accessible to pods
   kubectl get secret ngc-secret -n research-ops -o yaml
   ```

### If Model Download Still Fails

1. **Verify NGC_API_KEY in Container:**
   ```bash
   # Wait for pod to be Running, then:
   kubectl exec -n research-ops deployment/embedding-nim -- env | grep NGC
   ```

2. **Check NGC API Access:**
   ```bash
   NGC_API_KEY=$(kubectl get secret -n research-ops nvidia-ngc-secret -o jsonpath='{.data.NGC_API_KEY}' | base64 -d)
   curl -u "\$oauthtoken:$NGC_API_KEY" \
     "https://api.ngc.nvidia.com/v2/org/nim/team/nvidia/models/nv-embedqa-e5-v5/versions/5_tokenizer/zip" -I
   ```

3. **Alternative Authentication:**
   Some NIM models may require different authentication. Check model-specific documentation.

## Quick Resolution Script

```bash
#!/bin/bash
# Quick fix after license acceptance

NGC_API_KEY="YOUR_NGC_API_KEY_HERE"

echo "Updating secrets..."
kubectl create secret generic nvidia-ngc-secret \
  --from-literal=NGC_API_KEY="$NGC_API_KEY" \
  --namespace=research-ops \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl delete secret ngc-secret -n research-ops --ignore-not-found=true
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password="$NGC_API_KEY" \
  --namespace=research-ops

echo "Restarting deployments..."
kubectl delete pod -n research-ops -l 'app in (reasoning-nim,embedding-nim)'
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops

echo "Monitoring..."
kubectl get pods -n research-ops -l 'app in (reasoning-nim,embedding-nim)' --watch
```

## Next Steps After Resolution

Once NIMs are running:

1. ✅ Test health endpoints (Phase 1)
2. ✅ Run full synthesis test (Phase 2)
3. ✅ Validate export formats (Phase 2)
4. ✅ Prepare demo (Phase 3)

---

**Estimated Resolution Time**: 15-30 minutes (mostly manual license acceptance)

**Confidence**: 95% that license acceptance will resolve both issues


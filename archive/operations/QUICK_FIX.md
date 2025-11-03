# Quick Fix - NIM Deployment Issues

## 🚨 Root Cause
**Wrong Docker image path** in `k8s/reasoning-nim-deployment.yaml`

❌ **Was**: `nvcr.io/nim/meta/llama-3.1-nemotron-nano-8b-instruct:1.0.0`
✅ **Fixed**: `nvcr.io/nim/nvidia/llama-3.1-nemotron-nano-8b-v1:1.8.4`

---

## ⚡ Quick Fix (15 minutes)

### 1️⃣ Accept NGC Licenses (5 min) - DO THIS FIRST!

Open these URLs and click "Get NIM":

```
https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/llama-3.1-nemotron-nano-8b-v1
https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/nv-embedqa-e5-v5
https://catalog.ngc.nvidia.com/orgs/nim/teams/meta/containers/llama-3.1-8b-instruct
```

Verify at: https://org.ngc.nvidia.com/subscriptions

### 2️⃣ Apply Fixed Deployment (2 min)

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent

# Delete old deployment
kubectl delete deployment reasoning-nim -n research-ops

# Apply fixed deployment
kubectl apply -f k8s/reasoning-nim-deployment.yaml
```

### 3️⃣ Configure Authentication (5 min)

```bash
# Set your NGC API key (get from: https://org.ngc.nvidia.com/setup/api-key)
export NGC_API_KEY='nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Run automated fix script
./scripts/fix-nim-licensing.sh
```

### 4️⃣ Monitor Progress (5 min)

```bash
# Watch pods (wait for "Running")
watch kubectl get pods -n research-ops

# Monitor logs (in another terminal)
kubectl logs -f deployment/reasoning-nim -n research-ops
```

### 5️⃣ Verify Health (1 min)

```bash
# Port-forward and test
kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000 &
curl http://localhost:8000/v1/health/live

# Expected: {"status":"ok"}
```

---

## ✅ Success Indicators

```bash
# Pods Running
kubectl get pods -n research-ops
# reasoning-nim-xxx   1/1   Running   0   5m
# embedding-nim-xxx   1/1   Running   0   5m

# Health checks pass
curl http://localhost:8000/v1/health/live
# {"status":"ok"}
```

---

## 🆘 Still Failing?

### 403 Forbidden persists:
- Wait 10 minutes after accepting licenses (propagation delay)
- Verify licenses at: https://org.ngc.nvidia.com/subscriptions

### 401 Unauthorized persists:
- Generate NEW NGC API key with "Full Access"
- Update: `export NGC_API_KEY='new-key' && ./scripts/fix-nim-licensing.sh`

### ImagePullBackOff:
```bash
# Check if imagePullSecrets configured
kubectl describe deployment reasoning-nim -n research-ops | grep -A 5 imagePullSecrets

# If missing, re-run fix script
./scripts/fix-nim-licensing.sh
```

---

## 📚 Full Documentation

- **Current Troubleshooting**: `../docs/TROUBLESHOOTING.md` (consolidated guide)
- **Technical Review**: `../TECHNICAL_REVIEW.md`

**Note:** This file has been archived. Current troubleshooting information is consolidated in `docs/TROUBLESHOOTING.md`.

---

## ⏱️ Timeline

- License acceptance: 5 min
- License propagation: 5-10 min
- Image pull (first time): 5-10 min
- Model load: 3-5 min
- **Total**: 25-40 minutes first deployment

---

**Issue**: 403 Forbidden + 401 Unauthorized
**Cause**: Wrong image path + missing licenses
**Status**: ✅ FIXED
**Date**: 2025-01-15

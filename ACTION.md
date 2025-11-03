# Fix Embedding NIM - 3 Commands

## Problem

Your Kubernetes cluster has the WRONG NGC API key:
```
Current K8s key: nvapi-i6nHkhqugF-oTXzK17qwDTQB...
Status: ❌ Causes 401 Unauthorized errors
```

You have a WORKING NGC API key locally (you confirmed docker pull works).

## Solution: Replace the Key

### Command 1: Find Your Working Key

```bash
# Try these to locate your working NGC API key:
cat ~/.docker/config.json | grep -A5 nvcr.io
# OR
cat ~/.ngc/config
# OR
echo $NGC_API_KEY
```

Your working key should start with `nvapi-` and be ~50 characters.

### Command 2: Update Kubernetes

```bash
# Replace YOUR-WORKING-KEY with the actual key you found above
export NGC_API_KEY='nvapi-YOUR-WORKING-KEY'

# Run the update script
./scripts/update-ngc-key.sh
```

### Command 3: Monitor (Wait 10-15 minutes)

```bash
watch kubectl get pods -n research-ops

# Wait for:
# embedding-nim-xxx   1/1   Running   0   5m
```

## What Happens

1. Script tests your key works ✅
2. Updates K8s secrets with your working key
3. Restarts embedding-nim deployment
4. Downloads tokenizers from NGC (~3-5 min)
5. Loads model into GPU (~2-3 min)
6. Pod becomes Ready ✅

## Verify Success

```bash
# Port forward
kubectl port-forward -n research-ops svc/embedding-nim 8001:8001 &

# Test
curl http://localhost:8001/v1/health/live
# Should return: {"status":"ok"}
```

## Status Check

```bash
# Reasoning NIM: 🟡 Loading model (should be ready in ~2 min)
kubectl logs -f deployment/reasoning-nim -n research-ops

# Embedding NIM: 🔴 Waiting for your NGC key update
kubectl logs -f deployment/embedding-nim -n research-ops
```

---

**That's it!** Just find your working NGC key and run the update script. 🎉

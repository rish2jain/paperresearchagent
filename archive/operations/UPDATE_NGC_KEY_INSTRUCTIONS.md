# Update NGC API Key - Quick Instructions

## Current Status

✅ **Reasoning NIM**: Running successfully with correct image
❌ **Embedding NIM**: CrashLoopBackOff due to 401 Unauthorized (NGC API key mismatch)

## Problem

Your local NGC credentials work (you confirmed docker pull works), but Kubernetes is using a different NGC API key that doesn't have proper permissions.

## Solution: Update NGC API Key in Kubernetes

### Step 1: Get Your Working NGC API Key

Your NGC API key should be in one of these locations:

```bash
# Option 1: Check Docker config
cat ~/.docker/config.json | grep nvcr.io

# Option 2: Check NGC CLI config
cat ~/.ngc/config | grep apikey

# Option 3: Check environment variables
echo $NGC_API_KEY

# Option 4: Get from NGC website
# Visit: https://org.ngc.nvidia.com/setup/api-key
```

Your key should start with `nvapi-` and be about 40-50 characters long.

### Step 2: Export Your NGC API Key

```bash
export NGC_API_KEY='nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

**Replace the example above with your actual NGC API key!**

### Step 3: Run the Update Script

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent
./scripts/update-ngc-key.sh
```

### What the Script Does

1. ✅ Tests your NGC API key validity
2. 🗑️ Removes old secrets with incorrect keys
3. 🔐 Creates new secrets with your working key:
   - `nvidia-ngc-secret`: For environment variables
   - `ngc-secret`: For Docker image pulls
4. ♻️ Restarts both NIM deployments
5. 🗑️ Cleans up old failed pods
6. 📊 Shows current pod status

### Step 4: Monitor Progress

Watch the pods restart and pull successfully:

```bash
# Watch pod status (Ctrl+C to exit)
watch kubectl get pods -n research-ops

# Monitor embedding-nim logs
kubectl logs -f deployment/embedding-nim -n research-ops

# Monitor reasoning-nim logs
kubectl logs -f deployment/reasoning-nim -n research-ops
```

### Expected Timeline

| Step | Duration | What's Happening |
|------|----------|------------------|
| Script execution | 2 min | Updating secrets and restarting |
| Image pull (if needed) | 5-10 min | Large images, first time only |
| Model download | 3-5 min | Downloading tokenizers from NGC |
| Model load | 2-3 min | Loading into GPU memory |
| **Total** | **12-20 min** | First-time deployment |

### Success Indicators

You'll know it worked when you see:

```bash
kubectl get pods -n research-ops

# Expected output:
# reasoning-nim-xxx   1/1   Running   0   5m
# embedding-nim-xxx   1/1   Running   0   5m
```

### Verify Health

Once pods are Running:

```bash
# Test reasoning NIM
kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000 &
curl http://localhost:8000/v1/health/live
# Expected: {"status":"ok"}

# Test embedding NIM
kubectl port-forward -n research-ops svc/embedding-nim 8001:8001 &
curl http://localhost:8001/v1/health/live
# Expected: {"status":"ok"}
```

## Troubleshooting

### Script Says "NGC API Key Test Failed"

Your key might be expired or have insufficient permissions:

1. Generate a new key at: https://org.ngc.nvidia.com/setup/api-key
2. Select **"Full Access"** when generating
3. Test it locally first: `docker pull nvcr.io/nim/nvidia/nv-embedqa-e5-v5:1.0.0`
4. Then run the update script again

### Pods Still in CrashLoopBackOff After Update

1. Wait 5-10 minutes for license propagation
2. Check pod events: `kubectl describe pod -l app=embedding-nim -n research-ops`
3. Check logs: `kubectl logs -l app=embedding-nim -n research-ops`
4. Verify licenses accepted at: https://org.ngc.nvidia.com/subscriptions

### Pods Stuck in Pending

Resource constraint issue (insufficient CPU/memory/GPU):

```bash
# Check node resources
kubectl describe node

# Scale down to 1 replica each if needed
kubectl scale deployment reasoning-nim --replicas=1 -n research-ops
kubectl scale deployment embedding-nim --replicas=1 -n research-ops
```

## Next Steps After Success

1. **Test the API**: Access web UI at http://localhost:8501
2. **Run Integration Test**: `python -m pytest src/test_comprehensive_integration.py -v`
3. **Demo the System**: Follow demo script in `TECHNICAL_REVIEW.md`

---

**Need Help?** See `../docs/TROUBLESHOOTING.md` for detailed troubleshooting guide.

**Note:** This file has been archived. Current troubleshooting information is in `docs/TROUBLESHOOTING.md`.

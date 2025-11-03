# Next Steps - Simple Path Forward

## Current Situation

✅ **Reasoning NIM**: Loading model (will be ready in 2-3 minutes)
❌ **Embedding NIM**: Needs NGC API key update

## What You Need To Do (5 Commands)

### Step 1: Get Your NGC API Key

```bash
# Find your NGC API key (the one that works with docker pull)
# Try these commands to locate it:

cat ~/.docker/config.json | grep nvcr.io
# OR
cat ~/.ngc/config | grep apikey
# OR
echo $NGC_API_KEY
```

Your key should look like: `nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 2: Update Kubernetes with Your Working Key

```bash
# Export your NGC API key
export NGC_API_KEY='nvapi-YOUR-KEY-HERE'  # Replace with actual key!

# Navigate to project directory
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent

# Run the update script
./scripts/update-ngc-key.sh
```

### Step 3: Clean Up Pending Pods (Optional but Recommended)

```bash
# Scale down to single replicas (reduces resource contention)
kubectl scale deployment reasoning-nim --replicas=1 -n research-ops
kubectl scale deployment embedding-nim --replicas=1 -n research-ops

# Delete stuck pending pods
kubectl delete pod -n research-ops --field-selector=status.phase=Pending
```

### Step 4: Monitor Progress (10-15 minutes)

```bash
# Watch pods until both show "Running" and "1/1"
watch kubectl get pods -n research-ops

# Expected final state:
# reasoning-nim-xxx   1/1   Running   0   5m
# embedding-nim-xxx   1/1   Running   0   5m
```

### Step 5: Verify Everything Works

```bash
# Port forward services
kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000 &
kubectl port-forward -n research-ops svc/embedding-nim 8001:8001 &

# Test health endpoints
curl http://localhost:8000/v1/health/live  # Should return {"status":"ok"}
curl http://localhost:8001/v1/health/live  # Should return {"status":"ok"}

# Access web UI
kubectl port-forward -n research-ops svc/web-ui 8501:8501
# Then open: http://localhost:8501
```

## Timeline

| Time | What's Happening |
|------|------------------|
| Now | Reasoning NIM loading model |
| +2-3 min | Reasoning NIM ready ✅ |
| After you run update script | Embedding NIM restarting |
| +5-10 min | Embedding NIM downloading tokenizers |
| +12-15 min | **All systems operational** ✅ |

## If Something Goes Wrong

### NGC Key Update Fails
```bash
# Generate new key at: https://org.ngc.nvidia.com/setup/api-key
# Make sure to select "Full Access"
# Test it first: docker pull nvcr.io/nim/nvidia/nv-embedqa-e5-v5:1.0.0
```

### Pods Still Failing
```bash
# Check logs
kubectl logs -f deployment/embedding-nim -n research-ops

# Check events
kubectl get events -n research-ops --sort-by='.lastTimestamp' | tail -20

# Verify licenses accepted at: https://org.ngc.nvidia.com/subscriptions
```

### Need More Help
- See `UPDATE_NGC_KEY_INSTRUCTIONS.md` for detailed instructions
- See `DEPLOYMENT_STATUS_NOW.md` for current status details
- See `docs/DEPLOYMENT_FIX_SUMMARY.md` for troubleshooting guide

---

## Summary: Just Run These Commands

```bash
# 1. Export your NGC API key (the one that works with docker pull)
export NGC_API_KEY='nvapi-YOUR-KEY-HERE'

# 2. Update Kubernetes
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent
./scripts/update-ngc-key.sh

# 3. Clean up (optional)
kubectl scale deployment reasoning-nim --replicas=1 -n research-ops
kubectl scale deployment embedding-nim --replicas=1 -n research-ops
kubectl delete pod -n research-ops --field-selector=status.phase=Pending

# 4. Monitor
watch kubectl get pods -n research-ops

# 5. Test (after all pods show "Running 1/1")
kubectl port-forward -n research-ops svc/reasoning-nim 8000:8000 &
kubectl port-forward -n research-ops svc/embedding-nim 8001:8001 &
curl http://localhost:8000/v1/health/live
curl http://localhost:8001/v1/health/live
```

**That's it!** 🎉

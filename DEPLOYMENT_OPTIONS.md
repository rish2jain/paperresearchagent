# NIM Deployment Options - EKS vs SageMaker

You're currently using **EKS** but saw the **SageMaker** deployment guide. Here's the comparison:

## Current Setup: EKS (Kubernetes)

**What you have now:**
- ✅ Full multi-agent system deployed
- ✅ 4 agents + Vector DB + Web UI all running
- 🟡 Just need to fix NGC API key for NIMs

**Pros:**
- Complete control over infrastructure
- Full Kubernetes flexibility
- Multi-service orchestration (agents, DB, UI, NIMs)
- Cost-effective for multiple services

**Cons:**
- More complex to manage
- Need to handle secrets, networking, scaling yourself

**Status:** Almost working! Just need NGC key fix

---

## Alternative: SageMaker (Managed Endpoints)

**What SageMaker offers:**
- Fully managed NIM endpoints
- No Kubernetes management needed
- Auto-scaling built-in
- Pay-per-use pricing

**Pros:**
- Simpler NIM deployment
- AWS handles infrastructure
- Easier scaling

**Cons:**
- Only handles NIMs, not your full agent system
- Would still need EKS for agents, Web UI, Vector DB
- Higher cost per inference
- Less control over NIM configuration

---

## Recommendation: Stick with EKS

Since you already have:
- ✅ EKS cluster running
- ✅ All services deployed (agents, DB, UI)
- ✅ Reasoning NIM starting up
- 🔴 Just NGC key issue on embedding-nim

**It's faster to fix the NGC key than migrate to SageMaker!**

---

## Fix Your Current NGC Key (2 Methods)

### Method 1: Update secrets.yaml (What you're looking at)

You opened `k8s/secrets.yaml` which has:
```yaml
NGC_API_KEY: "nvapi-i6nHkhqugF-oTXzK17qwDTQB..."  # Line 8
```

**To fix this way:**

1. **Get your working NGC key** from: https://org.ngc.nvidia.com/setup/api-key

2. **Edit the file**:
   ```bash
   # Replace the key on line 8 with your working key
   vi k8s/secrets.yaml
   ```

3. **Reapply the secret**:
   ```bash
   kubectl delete secret nvidia-ngc-secret -n research-ops
   kubectl apply -f k8s/secrets.yaml
   ```

4. **Restart deployments**:
   ```bash
   kubectl rollout restart deployment reasoning-nim -n research-ops
   kubectl rollout restart deployment embedding-nim -n research-ops
   ```

### Method 2: Use the update script (Easier)

```bash
# 1. Export your working NGC key
export NGC_API_KEY='nvapi-YOUR-WORKING-KEY'

# 2. Run the script (does everything above automatically)
./scripts/update-ngc-key.sh
```

---

## Current NGC Key Issue

The key in your `secrets.yaml` is:
```
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
```

This key is causing 401 Unauthorized errors, which means:
- ❌ It's invalid, expired, or has wrong permissions
- ✅ You need to replace it with your working key

---

## SageMaker Migration (If You Want It)

**If you really want to use SageMaker instead:**

1. Deploy NIMs to SageMaker endpoints (from that GitHub repo)
2. Update your agent code to point to SageMaker endpoints
3. Keep EKS for agents, Web UI, and Vector DB

**Time to migrate:** 2-3 hours
**Time to fix NGC key:** 5 minutes

---

## My Recommendation

**Fix the NGC key now** (5 min) → System working ✅

**Then** if you want SageMaker later, you can migrate the NIMs while keeping everything else on EKS.

---

## Quick Fix Right Now

You have the secrets.yaml file open. Here's what to do:

1. **Get your working NGC key**: https://org.ngc.nvidia.com/setup/api-key

2. **Replace line 8** in secrets.yaml:
   ```yaml
   NGC_API_KEY: "nvapi-YOUR-ACTUAL-WORKING-KEY"
   ```

3. **Apply and restart**:
   ```bash
   kubectl delete secret nvidia-ngc-secret -n research-ops
   kubectl apply -f k8s/secrets.yaml
   kubectl rollout restart deployment embedding-nim -n research-ops
   ```

**That's it!** Your embedding-nim will restart with the working key.

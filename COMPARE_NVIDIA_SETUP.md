# Your Setup vs NVIDIA's Official EKS Guide

## Comparison

### ✅ What Matches NVIDIA's Guide

| Component | NVIDIA Recommendation | Your Setup | Status |
|-----------|----------------------|------------|--------|
| **EKS Cluster** | AWS EKS with g5 instances | ✅ You have this | ✅ |
| **NVIDIA Device Plugin** | v0.14.1 | ✅ Likely installed | ✅ |
| **NGC Registry Access** | Docker credentials | ✅ `ngc-secret` configured | ✅ |
| **Storage** | EFS/EBS/Host path | ✅ PVCs configured | ✅ |

### 🔧 What's Different (But OK)

| Aspect | NVIDIA Guide | Your Setup | Notes |
|--------|--------------|------------|-------|
| **Secret Names** | `ngc-api` + `registry-secret` | `nvidia-ngc-secret` + `ngc-secret` | Both work fine |
| **Deployment Method** | Helm charts | Manual YAML | Both valid approaches |
| **API Key Env Var** | `NGC_CLI_API_KEY` | `NGC_API_KEY` | Both accepted by NIMs |

### 🔴 The Issue

**Your secrets.yaml NGC key is invalid/expired**

NVIDIA Guide shows:
```bash
export NGC_API_KEY=<YOUR-WORKING-KEY>
kubectl create secret generic ngc-api --from-literal=NGC_CLI_API_KEY=$NGC_API_KEY
```

Your setup (line 8 of secrets.yaml):
```yaml
NGC_API_KEY: "nvapi-i6nHkhqugF-oTXzK17qwDTQB..."  # ❌ This key is invalid
```

---

## Fix Options

### Option 1: Edit secrets.yaml (You have it open!)

**NVIDIA's approach translated to your setup:**

1. **Get your working NGC key**: https://org.ngc.nvidia.com/setup/api-key

2. **Edit line 8** in the file you have open:
   ```yaml
   NGC_API_KEY: "nvapi-YOUR-ACTUAL-WORKING-KEY-HERE"
   ```

3. **Apply**:
   ```bash
   kubectl delete secret nvidia-ngc-secret -n research-ops
   kubectl apply -f k8s/secrets.yaml
   kubectl rollout restart deployment embedding-nim -n research-ops
   kubectl rollout restart deployment reasoning-nim -n research-ops
   ```

### Option 2: Follow NVIDIA's Exact Pattern

```bash
# 1. Get your NGC key
export NGC_API_KEY='nvapi-YOUR-WORKING-KEY'

# 2. Create NVIDIA-style secrets
kubectl delete secret nvidia-ngc-secret -n research-ops
kubectl create secret generic nvidia-ngc-secret \
  --from-literal=NGC_CLI_API_KEY=$NGC_API_KEY \
  --from-literal=NGC_API_KEY=$NGC_API_KEY \
  --namespace research-ops

# 3. Update docker registry secret
kubectl delete secret ngc-secret -n research-ops
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password=$NGC_API_KEY \
  --namespace research-ops

# 4. Restart deployments
kubectl rollout restart deployment reasoning-nim -n research-ops
kubectl rollout restart deployment embedding-nim -n research-ops
```

---

## Key Differences Explained

### NVIDIA Uses Helm

From the guide:
```bash
helm install nim-llm nim-llm-1.3.0.tgz -f storage/custom-values-ebs-sc.yaml
```

**You're using manual YAML deployments** - this is fine for a hackathon! Helm just makes it easier to manage, but your approach works.

### NVIDIA Uses Different Secret Names

NVIDIA:
- `ngc-api` secret with `NGC_CLI_API_KEY`
- `registry-secret` for docker

You:
- `nvidia-ngc-secret` with `NGC_API_KEY`
- `ngc-secret` for docker

**Both approaches work!** NIMs accept both `NGC_CLI_API_KEY` and `NGC_API_KEY`.

### Your Deployments Are Already Configured Correctly

Your deployment YAMLs already reference the right secrets:
- ✅ `nvidia-ngc-secret` for env vars
- ✅ `ngc-secret` for imagePullSecrets

**You just need to update the KEY VALUE, not change the secret structure!**

---

## Recommendation: Simplest Fix

Since you already have `secrets.yaml` open in your IDE:

1. **Get working key**: https://org.ngc.nvidia.com/setup/api-key

2. **Replace line 8** with your actual key

3. **Run 3 commands**:
   ```bash
   kubectl delete secret nvidia-ngc-secret -n research-ops
   kubectl apply -f k8s/secrets.yaml
   kubectl rollout restart deployment embedding-nim reasoning-nim -n research-ops
   ```

**Done!** No need to change your deployment structure to match NVIDIA's Helm approach.

---

## What NVIDIA's Guide Confirms

✅ Your EKS setup architecture is correct
✅ Your secret structure works fine
✅ Your deployment approach is valid
✅ You just need the right NGC API key value

**The guide validates your approach - you're 95% there!**

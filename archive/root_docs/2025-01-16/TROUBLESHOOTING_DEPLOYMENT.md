# Deployment Troubleshooting Guide

Quick fixes for common deployment issues with ResearchOps Agent.

---

## 🔥 Issue: Deployment Script is Stuck

### Symptoms
- Running `./quick-deploy.sh` or `./deploy.py --target eks`
- Terminal appears frozen with no output
- Process is running but not progressing

### Root Cause
The script is waiting for user input at a prompt that may not be visible.

### Solution

**Option 1: Check for prompts**
The script may be asking: `"Create EKS cluster 'research-ops-cluster' in us-east-2? (yes/no): "`

Type `yes` and press Enter to proceed, or `no` to cancel.

**Option 2: Kill and restart with verbose mode**
```bash
# Kill stuck process
pkill -f "deploy.py"

# Restart with verbose output
./deploy.py --target eks --verbose
```

**Option 3: Use existing cluster**
If you already have an EKS cluster:
```bash
./deploy.py --target eks --cluster your-existing-cluster --region your-region
```

---

## 🔑 Issue: "NGC_API_KEY not found" Error

### Symptoms
```
❌ NGC_API_KEY not found
Set it as environment variable OR add to k8s/secrets.yaml
```

### Root Cause
The deployment script needs NGC_API_KEY but can't find it in either:
1. Environment variables (`export NGC_API_KEY=...`)
2. The `k8s/secrets.yaml` file

### Solutions

**✅ FIXED in latest version**: The script now automatically reads from `k8s/secrets.yaml`!

**Option 1: Set as environment variable (Quick)**
```bash
export NGC_API_KEY="your_actual_ngc_key_here"
./quick-deploy.sh
```

**Option 2: Add to k8s/secrets.yaml (Persistent)**

Your `k8s/secrets.yaml` already has the NGC_API_KEY! The fixed `deploy.py` will automatically detect it.

Just verify it's there:
```bash
grep "NGC_API_KEY" k8s/secrets.yaml
```

Should show:
```yaml
stringData:
  NGC_API_KEY: "ZHNlM2NiMDZ2cWNvcjMyaWRvdWVlNzRudDM6..."
```

**Option 3: Install PyYAML (if you see PyYAML warning)**
```bash
pip install pyyaml
```

---

## 📦 Issue: PyYAML Not Installed Warning

### Symptoms
```
⚠️  PyYAML not installed, cannot read secrets.yaml
Install with: pip install pyyaml
```

### Solution
```bash
pip install pyyaml

# Or add to requirements
echo "pyyaml==6.0.1" >> requirements.txt
pip install -r requirements.txt
```

After installing, the script will automatically read NGC_API_KEY from `k8s/secrets.yaml`.

---

## 🔐 Issue: Script Asks for NGC_API_KEY Despite Having It in secrets.yaml

### Symptoms
- NGC_API_KEY is in `k8s/secrets.yaml`
- Script still says it's missing

### Root Cause (FIXED)
**Old behavior**: Script only checked environment variables
**New behavior**: Script checks environment variables THEN secrets.yaml

### Solution
If you're using the **old version** of `deploy.py`:

```bash
# Extract key from secrets.yaml manually
export NGC_API_KEY=$(grep "NGC_API_KEY:" k8s/secrets.yaml | cut -d'"' -f2)

# Or update to the fixed deploy.py (recommended)
# The new version automatically reads from secrets.yaml
```

If using the **new version** (with fixes):
- Just run `./quick-deploy.sh` - it will auto-detect the key!

---

## 📝 Issue: API Keys for Paper Sources Not Working

### Symptoms
- Have API keys for IEEE, ACM, Springer in secrets.yaml
- Script doesn't seem to use them

### Explanation
The deployment script focuses on NGC_API_KEY for EKS deployment.

**Paper source API keys** are used by the application at runtime, not during deployment.

### How They're Used

1. **During Deployment**: Only NGC_API_KEY is needed
2. **At Runtime**: The agent reads API keys from environment or Kubernetes secrets

### Where to Set Them

**For EKS deployment:**
```yaml
# k8s/secrets.yaml (already configured!)
apiVersion: v1
kind: Secret
metadata:
  name: research-ops-secrets
  namespace: research-ops
stringData:
  SEMANTIC_SCHOLAR_API_KEY: "your_key"
  IEEE_API_KEY: "your_key"
  ACM_API_KEY: "your_key"
  SPRINGER_API_KEY: "your_key"
```

**For local Docker deployment:**
```bash
# .env file
SEMANTIC_SCHOLAR_API_KEY=your_key
IEEE_API_KEY=your_key
ACM_API_KEY=your_key
SPRINGER_API_KEY=your_key
```

The agent orchestrator will automatically pick them up from the Kubernetes secret or .env file.

---

## 🚨 Issue: Deployment Starts But Pods Stay in Pending

### Symptoms
```bash
kubectl get pods -n research-ops
# Shows: reasoning-nim  0/1  Pending
```

### Common Causes

**1. Insufficient GPU Quota**
```bash
# Check vCPU quota
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-1216C47A \
  --region us-east-2

# Request increase if needed (AWS Console)
```

**2. No GPU Nodes Available**
```bash
# Check nodes
kubectl get nodes -o wide

# Check GPU resources
kubectl describe nodes | grep -A 5 "Allocated resources"
```

**3. NGC Registry Secret Missing**
```bash
# Verify secret exists
kubectl get secret ngc-secret -n research-ops

# Recreate if missing
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password="$NGC_API_KEY" \
  --namespace=research-ops
```

---

## ⏰ Issue: NIM Pods Taking Forever to Start

### Symptoms
- Pods stuck in "ContainerCreating" for 10-20 minutes
- No errors in logs

### Explanation
**This is NORMAL!** NIMs compile TensorRT engines on first start.

### Timeline
- **First start**: 10-20 minutes (TensorRT compilation)
- **Subsequent starts**: 2-5 minutes (engine cached)

### Monitor Progress
```bash
# Watch logs for progress
kubectl logs -f deployment/reasoning-nim -n research-ops

# Look for:
# "Building TensorRT engine..."
# "TensorRT engine build complete"
# "Ready to serve requests"
```

### Workaround
Be patient! ☕ This is a one-time compilation.

---

## 🔄 Issue: Deployment Failed Midway, Want to Retry

### Solution

**Clean retry:**
```bash
# Delete namespace (keeps cluster)
kubectl delete namespace research-ops

# Wait for deletion to complete
kubectl get namespaces

# Retry deployment
./quick-deploy.sh
```

**Full reset:**
```bash
# Delete entire cluster
eksctl delete cluster --name research-ops-cluster --region us-east-2

# Start fresh
./quick-deploy.sh
```

---

## 🐳 Issue: Docker Compose Fails Locally

### Symptoms
```
ERROR: Service 'orchestrator' failed to build
```

### Solutions

**1. Clean rebuild**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

**2. Check Docker daemon**
```bash
docker info
# If fails: Start Docker Desktop or Docker daemon
```

**3. Free up space**
```bash
docker system prune -a
# Warning: removes all unused images
```

---

## 📊 Quick Diagnostic Commands

### Check What's Running
```bash
# Kubernetes
kubectl get pods -n research-ops
kubectl get svc -n research-ops
kubectl get events -n research-ops --sort-by='.lastTimestamp'

# Docker Compose
docker-compose ps
docker-compose logs
```

### View Logs
```bash
# Kubernetes
kubectl logs -f deployment/reasoning-nim -n research-ops
kubectl logs -f deployment/agent-orchestrator -n research-ops

# Docker Compose
docker-compose logs -f orchestrator
docker-compose logs -f reasoning-nim
```

### Check Resources
```bash
# Kubernetes
kubectl top nodes
kubectl top pods -n research-ops

# Docker
docker stats
```

### Verify Configuration
```bash
# Check NGC_API_KEY in secrets.yaml
grep "NGC_API_KEY" k8s/secrets.yaml

# Check environment
env | grep -E "(NGC|API_KEY)"

# Check AWS credentials
aws sts get-caller-identity
```

---

## 🆘 Emergency Reset

If everything is broken and you want to start completely fresh:

```bash
# 1. Kill any running deployment scripts
pkill -f deploy

# 2. Clean Docker Compose
docker-compose down -v
docker system prune -f

# 3. Delete Kubernetes resources
kubectl delete namespace research-ops

# 4. Optionally delete cluster
eksctl delete cluster --name research-ops-cluster --region us-east-2

# 5. Wait for cleanup
sleep 30

# 6. Start fresh
export NGC_API_KEY="your_key"
./quick-deploy.sh
```

---

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] NGC_API_KEY is set (env or secrets.yaml)
- [ ] PyYAML is installed (`pip list | grep PyYAML`)
- [ ] Docker daemon is running (`docker info`)
- [ ] AWS credentials are configured (`aws sts get-caller-identity`)
- [ ] kubectl can connect (`kubectl version`)
- [ ] Sufficient disk space (`df -h`)
- [ ] No firewall blocking ports (8000, 8001, 8080, 8501, 6333, 6379)
- [ ] Latest version of deploy.py (with secrets.yaml support)

---

## 📚 Additional Resources

- **Main Deployment Guide**: `DEPLOY_README.md`
- **Implementation Details**: `DEPLOYMENT_SUMMARY.md`
- **Project Overview**: `CLAUDE.md`
- **AWS Setup**: `docs/AWS_SETUP_GUIDE.md`
- **General Troubleshooting**: `docs/TROUBLESHOOTING.md`

---

## 🔧 Common Fixes Applied

### Version Check
Check if you have the latest deploy.py:
```bash
grep -n "get_ngc_key_from_secrets" deploy.py
# Should show method definition around line 85
```

If not found, you have the old version. The new version includes:
- ✅ Automatic NGC_API_KEY detection from secrets.yaml
- ✅ Better error messages
- ✅ PyYAML optional dependency handling
- ✅ Improved cluster creation prompts

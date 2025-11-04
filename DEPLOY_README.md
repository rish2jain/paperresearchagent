# Deployment Scripts Guide

Complete guide for deploying ResearchOps Agent using the included deployment tools.

---

## 📋 Overview

This project includes three deployment methods:

1. **`deploy.py`** - Comprehensive Python deployment tool (recommended)
2. **`quick-deploy.sh`** - Simple bash wrapper for common scenarios
3. **`k8s/deploy.sh`** - Direct Kubernetes deployment (EKS only)

---

## 🚀 Quick Start

### Local Development (Docker Compose)

```bash
# One-line deployment
./quick-deploy.sh local

# Or using deploy.py directly
./deploy.py --target docker --build
```

**What happens:**
- Builds Docker images for orchestrator and web UI
- Starts mock NIMs for local testing (no GPU required)
- Starts Qdrant vector database and Redis cache
- Deploys FastAPI orchestrator and Streamlit UI
- Services available at http://localhost:8501 (UI) and http://localhost:8080 (API)

### Production (AWS EKS)

```bash
# Set NGC API key first
export NGC_API_KEY="your_ngc_api_key"

# Deploy to EKS
./quick-deploy.sh eks

# Or using deploy.py with custom options
./deploy.py --target eks --cluster my-cluster --region us-west-2
```

**What happens:**
- Validates prerequisites (kubectl, aws, eksctl)
- Creates EKS cluster if it doesn't exist (~15-20 minutes)
- Deploys real NVIDIA NIMs with GPU acceleration
- Applies all Kubernetes manifests
- Waits for services to be ready (up to 20 minutes for TensorRT compilation)
- Displays service endpoints

---

## 📦 Deployment Script Features

### `deploy.py` - Main Deployment Tool

**Comprehensive Python script with:**
- ✅ Multi-target support (Docker Compose, AWS EKS)
- ✅ Prerequisite validation (tools, environment variables)
- ✅ Colored terminal output with progress indicators
- ✅ Automatic cluster creation (EKS)
- ✅ Health check monitoring
- ✅ Cleanup utilities
- ✅ Custom registry support
- ✅ Verbose debugging mode

**Usage:**
```bash
# Show all options
./deploy.py --help

# Deploy to Docker Compose
./deploy.py --target docker --build

# Deploy to EKS with custom cluster name
./deploy.py --target eks --cluster prod-cluster --region us-east-2

# Build and push to private registry
./deploy.py --build --push --registry myregistry.io/research-ops

# Cleanup resources
./deploy.py --cleanup --target docker
./deploy.py --cleanup --target eks

# Verbose mode for debugging
./deploy.py --target eks --verbose
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--target` | Deployment target (docker/eks) | `docker` |
| `--build` | Build Docker images | `false` |
| `--push` | Push images to registry | `false` |
| `--registry` | Docker registry URL | - |
| `--cluster` | EKS cluster name | `research-ops-cluster` |
| `--region` | AWS region | `us-east-2` |
| `--cleanup` | Remove deployed resources | `false` |
| `-v, --verbose` | Verbose output | `false` |

---

### `quick-deploy.sh` - Simple Wrapper

**Quick deployment for common scenarios:**

```bash
# EKS deployment (default)
./quick-deploy.sh

# Or explicitly
./quick-deploy.sh eks

# Local deployment
./quick-deploy.sh local
```

**Features:**
- Simple one-command deployment
- Automatic .env setup from .env.example
- Environment variable validation
- Clear next-step instructions

---

### `k8s/deploy.sh` - Direct Kubernetes Deployment

**Original bash deployment script for EKS:**

```bash
cd k8s
chmod +x deploy.sh
./deploy.sh
```

**Features:**
- Direct Kubernetes manifest application
- NGC registry secret creation
- Service endpoint display
- Legacy option for manual deployment

---

## 🔧 Configuration

### Environment Variables

**Required for EKS:**
```bash
export NGC_API_KEY="your_ngc_api_key"
```

**Optional (see `.env.example` for all options):**
```bash
# Paper source API keys
export SEMANTIC_SCHOLAR_API_KEY="your_key"
export IEEE_API_KEY="your_key"
export ACM_API_KEY="your_key"
export SPRINGER_API_KEY="your_key"

# Configuration
export DEMO_MODE=false
export LOG_LEVEL=INFO
export RELEVANCE_THRESHOLD=0.7
```

### Configuration Files

**`.env.example`** - Template for environment variables
- Copy to `.env` for local development
- Edit with your API keys
- Used by Docker Compose

**`docker-compose.yml`** - Local deployment configuration
- Mock NIMs for development
- Qdrant and Redis services
- Development volume mounts
- Health checks

**`k8s/*.yaml`** - Kubernetes manifests
- Production NIM deployments
- GPU resource allocation
- Service definitions
- Secrets and ConfigMaps

---

## 📊 Deployment Workflow

### Local Development Workflow

```
1. Setup Environment
   ├─ Copy .env.example → .env
   ├─ Edit API keys (optional)
   └─ Install Docker & Docker Compose

2. Deploy Services
   ├─ ./quick-deploy.sh local
   ├─ Wait for containers to start (~2 min)
   └─ Services ready

3. Development
   ├─ Access UI: http://localhost:8501
   ├─ Access API: http://localhost:8080
   ├─ Edit code (volume-mounted in dev mode)
   └─ View logs: docker-compose logs -f

4. Testing
   ├─ Run tests: docker-compose exec orchestrator pytest
   ├─ Check health: curl http://localhost:8080/health
   └─ Test UI interactions

5. Cleanup
   └─ docker-compose down -v
```

### Production (EKS) Workflow

```
1. Prerequisites
   ├─ AWS account & credentials configured
   ├─ NGC API key obtained
   ├─ Tools installed (kubectl, aws, eksctl)
   └─ vCPU quota verified

2. Deploy
   ├─ export NGC_API_KEY="..."
   ├─ ./deploy.py --target eks
   ├─ Wait for cluster creation (~15 min)
   ├─ Wait for NIMs TensorRT compilation (~20 min)
   └─ Services ready

3. Access Services
   ├─ Get LoadBalancer URLs: kubectl get svc -n research-ops
   ├─ Or port-forward: kubectl port-forward svc/web-ui 8501:8501
   └─ Access: http://localhost:8501 or LoadBalancer URL

4. Monitoring
   ├─ Pods: kubectl get pods -n research-ops
   ├─ Logs: kubectl logs -f deployment/reasoning-nim -n research-ops
   ├─ Events: kubectl get events -n research-ops
   └─ Resources: kubectl top pods -n research-ops

5. Cleanup
   ├─ Namespace: kubectl delete namespace research-ops
   └─ Cluster: eksctl delete cluster --name research-ops-cluster
```

---

## 🛠️ Troubleshooting

### Common Issues

**1. `deploy.py` not executable**
```bash
chmod +x deploy.py quick-deploy.sh
```

**2. Missing prerequisites**
```bash
# Check what's missing
./deploy.py --target eks  # Will validate and report

# Install missing tools
brew install kubectl aws-cli eksctl  # macOS
# or
sudo apt-get install kubectl awscli  # Linux
```

**3. NGC_API_KEY not set (EKS deployment)**
```bash
# Check if set
echo $NGC_API_KEY

# Set temporarily
export NGC_API_KEY="your_key"

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export NGC_API_KEY="your_key"' >> ~/.bashrc
```

**4. Docker Compose fails**
```bash
# Check Docker is running
docker info

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# View logs
docker-compose logs
```

**5. EKS cluster creation fails**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check region quota for g5.2xlarge
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-1216C47A \
  --region us-east-2

# Request quota increase via AWS Console if needed
```

**6. NIMs not starting on EKS**
```bash
# Check pod status
kubectl describe pod <reasoning-nim-pod> -n research-ops

# Common fixes:
# - Verify NGC_API_KEY in secrets
kubectl get secret research-ops-secrets -n research-ops -o yaml

# - Check GPU availability
kubectl describe nodes | grep -A 5 "Allocated resources"

# - View detailed logs
kubectl logs -f deployment/reasoning-nim -n research-ops
```

---

## 📝 Examples

### Example 1: Local Development Deployment

```bash
# 1. Setup
cp .env.example .env
# Edit .env (optional for local testing)

# 2. Deploy
./quick-deploy.sh local

# 3. Access
open http://localhost:8501

# 4. Test
curl http://localhost:8080/health

# 5. View logs
docker-compose logs -f orchestrator

# 6. Stop
docker-compose down
```

### Example 2: EKS Production Deployment

```bash
# 1. Prerequisites
export NGC_API_KEY="nvapi-xxxxx"
aws configure  # If not already done

# 2. Deploy
./deploy.py --target eks --cluster research-ops --region us-east-2 --verbose

# 3. Monitor deployment
kubectl get pods -n research-ops --watch

# 4. Access via port-forward
kubectl port-forward -n research-ops svc/web-ui 8501:8501 &
open http://localhost:8501

# 5. Check logs
kubectl logs -f deployment/agent-orchestrator -n research-ops
```

### Example 3: Build and Push to Private Registry

```bash
# 1. Login to registry
docker login myregistry.io

# 2. Build and push
./deploy.py \
  --build \
  --push \
  --registry myregistry.io/research-ops

# 3. Update Kubernetes manifests
# Edit k8s/*-deployment.yaml to use myregistry.io/research-ops/...

# 4. Deploy
./deploy.py --target eks
```

### Example 4: Cleanup After Testing

```bash
# Docker Compose cleanup
./deploy.py --cleanup --target docker
# Or: docker-compose down -v

# EKS cleanup (namespace only, keeps cluster)
kubectl delete namespace research-ops

# EKS full cleanup (removes cluster)
./deploy.py --cleanup --target eks
# Or: eksctl delete cluster --name research-ops-cluster --region us-east-2
```

---

## 🔒 Security Best Practices

When deploying to production:

1. **Never commit secrets** to git
   - Use `.env` (git-ignored) for local development
   - Use Kubernetes Secrets for EKS
   - Never hardcode API keys in code

2. **Use secrets management**
   ```bash
   # For EKS, create secret from file
   kubectl create secret generic research-ops-secrets \
     --from-literal=NGC_API_KEY=$NGC_API_KEY \
     -n research-ops
   ```

3. **Limit network exposure**
   - Use ClusterIP services (not LoadBalancer) when possible
   - Use Ingress controller for external access
   - Apply NetworkPolicies for pod-to-pod traffic

4. **Run as non-root**
   - All containers use non-root users (UID 1000)
   - Security contexts enforced in Kubernetes

5. **Keep secrets out of logs**
   - Deploy script sanitizes NGC_API_KEY from logs
   - Use `--verbose` sparingly in production

---

## 📚 Additional Resources

- **Full Deployment Guide**: See `DEPLOYMENT.md`
- **Troubleshooting**: See `docs/TROUBLESHOOTING.md`
- **AWS Setup**: See `docs/AWS_SETUP_GUIDE.md`
- **Architecture**: See `docs/Architecture_Diagrams.md`

---

## 🆘 Getting Help

**Logs:**
```bash
# Local
docker-compose logs orchestrator
docker-compose logs reasoning-nim

# EKS
kubectl logs -f deployment/agent-orchestrator -n research-ops
kubectl logs -f deployment/reasoning-nim -n research-ops
```

**Status:**
```bash
# Local
docker-compose ps

# EKS
kubectl get pods -n research-ops
kubectl get svc -n research-ops
kubectl describe pod <pod-name> -n research-ops
```

**Health Checks:**
```bash
# Local
curl http://localhost:8080/health
curl http://localhost:8000/v1/health/live  # Reasoning NIM
curl http://localhost:8001/v1/health/live  # Embedding NIM

# EKS
kubectl port-forward svc/agent-orchestrator 8080:8080 -n research-ops
curl http://localhost:8080/health
```

# Kubernetes Deployment

This directory contains all Kubernetes manifests and deployment scripts for ResearchOps Agent.

## Quick Start

### One-Command Deployment

```bash
cd k8s
chmod +x deploy.sh
./deploy.sh
```

This will:
1. Create or verify EKS cluster
2. Deploy all services (NIMs, vector DB, orchestrator, web UI)
3. Wait for all pods to be ready
4. Display service endpoints

## Deployment Files

### Core Manifests
- `namespace.yaml` - Kubernetes namespace definition
- `secrets.yaml.template` - Secrets template (copy to `secrets.yaml` and fill in)
- `secrets.yaml` - Actual secrets (NOT in git - add to .gitignore)
- `ingress.yaml` - Ingress controller configuration

### Service Deployments
- `reasoning-nim-deployment.yaml` - Reasoning NIM service
- `embedding-nim-deployment.yaml` - Embedding NIM service
- `vector-db-deployment.yaml` - Qdrant vector database
- `agent-orchestrator-deployment.yaml` - Main API service
- `web-ui-deployment.yaml` - Streamlit web interface

### Deployment Scripts
- `deploy.sh` - Main deployment script
- `auto_deploy_wait_quota.sh` - Automated deployment with quota monitoring
- `check_quota_status.sh` - Check AWS quota status
- `request_quota_increase.sh` - Request quota increase

## Documentation

### Setup & Configuration
- `AUTO_DEPLOY_README.md` - Automated deployment guide
- `AWS_QUOTA_GUIDE.md` - AWS quota and payment information

### Status & Troubleshooting
For deployment status and troubleshooting, see:
- Root `STATUS.md` - Current project status
- `docs/TROUBLESHOOTING.md` - Common issues and solutions
- `DEPLOYMENT.md` - Deployment guide (in root)

## Prerequisites

1. **AWS Account** configured with CLI
2. **NGC API Key** for NVIDIA NIMs
3. **kubectl** and **eksctl** installed
4. **Secrets configured** - See `secrets.yaml.template`

## Configuration

### Step 1: Prepare Secrets

```bash
cp secrets.yaml.template secrets.yaml
# Edit secrets.yaml with your credentials
```

Required:
- `NGC_API_KEY` - NVIDIA NGC API key
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key

### Step 2: Deploy

```bash
export NGC_API_KEY="your_key_here"
./deploy.sh
```

## Verification

```bash
# Check pods
kubectl get pods -n research-ops

# Check services
kubectl get svc -n research-ops

# Port forward for access
kubectl port-forward -n research-ops svc/web-ui 8501:8501
```

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for common issues:

- Pods not starting
- NIMs not responding
- Quota issues
- Network connectivity

## AWS Quota Management

If you encounter quota limits:
1. Check quota status: `./check_quota_status.sh`
2. Request increase: `./request_quota_increase.sh`
3. See `AWS_QUOTA_GUIDE.md` for details

## Automated Deployment

For deployments that need to wait for quota approval:

```bash
./auto_deploy_wait_quota.sh
```

This script monitors quota status and automatically deploys when ready.

---

For complete setup instructions, see `HACKATHON_SETUP_GUIDE.md` in the root directory.










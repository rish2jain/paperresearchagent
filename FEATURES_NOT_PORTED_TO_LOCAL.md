# Features NOT Ported to Local Setup - Complete List

**Last Updated:** 2025-01-16  
**After:** All packages installed + IEEE/SpringerLink API keys provided

---

## 🔴 Cloud-Only Features (Cannot Work Locally)

These features **require AWS infrastructure or Kubernetes** and cannot be ported:

### 1. AWS API Endpoints ❌

**Location:** `src/api.py` lines 1348-1453

| Endpoint | Purpose | Requires | Status |
|----------|---------|----------|--------|
| `POST /aws/sagemaker` | Invoke SageMaker endpoints | AWS SageMaker service | ❌ Not portable |
| `POST /aws/bedrock` | Invoke Bedrock models | AWS Bedrock access | ❌ Not portable |
| `POST /aws/store-s3` | Store results in S3 | AWS S3 bucket | ❌ Not portable |

**Workaround:** 
- SageMaker/Bedrock → Use local models (already implemented)
- S3 storage → Use local file system (already works)

---

### 2. AWS Lambda Integration ❌

**Location:** `src/aws_integration.py`

**Features:**
- `invoke_lambda_function()` - Invoke AWS Lambda
- `trigger_research_lambda()` - Async research via Lambda

**Requires:** AWS Lambda functions deployed

**Status:** ❌ Not portable - Requires AWS Lambda service

**Workaround:** Not needed - agents run directly locally

---

### 3. Kubernetes/EKS Infrastructure Features ❌

**Location:** `k8s/*.yaml` files

| Feature | Purpose | Requires | Status |
|---------|---------|----------|--------|
| **Auto-Scaling (HPA)** | Horizontal Pod Autoscaler | Kubernetes cluster | ❌ Not portable |
| **Service Discovery** | Kubernetes DNS (`svc.cluster.local`) | Kubernetes cluster | ❌ Not portable |
| **LoadBalancer** | External access | AWS LoadBalancer | ❌ Not portable |
| **PersistentVolumes** | Persistent storage | Kubernetes storage class | ❌ Not portable |
| **GPU Resources** | GPU scheduling | Kubernetes + GPU nodes | ❌ Not portable |
| **Health Probes** | Liveness/readiness | Kubernetes | ❌ Not portable |
| **ConfigMaps/Secrets** | K8s config management | Kubernetes | ❌ Not portable |

**Workarounds:**
- Auto-scaling → Not needed locally (single instance)
- Service discovery → Use `localhost` URLs (already implemented)
- LoadBalancer → Use `localhost:8080` (already working)
- PersistentVolumes → Use Docker volumes (already implemented)
- GPU resources → Use Metal GPU locally (already implemented)
- Health probes → Use `/health` endpoint (already works)

---

### 4. ECR Container Registry ❌

**Purpose:** Store Docker images in AWS ECR

**Requires:** AWS ECR repository + credentials

**Status:** ❌ Not portable - Requires AWS ECR

**Workaround:** Build images locally (already supported)

---

## ✅ What IS Portable (All Core Features Work)

### Core Research Features ✅
- ✅ Multi-agent system (all 4 agents)
- ✅ Paper search (7 sources: arXiv, PubMed, Semantic Scholar, Crossref, IEEE, ACM, SpringerLink)
- ✅ Paper analysis and extraction
- ✅ Synthesis generation (themes, contradictions, gaps)
- ✅ Decision logging
- ✅ Quality assessment

### Infrastructure ✅
- ✅ Web UI (Streamlit)
- ✅ API endpoints (FastAPI) - except AWS-specific ones
- ✅ Qdrant vector database (local Docker)
- ✅ Redis caching (local)
- ✅ Session management
- ✅ Local models (llama.cpp + Sentence Transformers)

### UI Features ✅
- ✅ Real-time streaming (SSE)
- ✅ Export formats (all 13 formats)
- ✅ Date filtering
- ✅ Source selection
- ✅ Progress tracking
- ✅ Decision log display

### Optional Features ✅
- ✅ Denario integration (if installed)
- ✅ Prometheus metrics (if installed)
- ✅ PDF/Word export (if libraries installed)

---

## 📊 Portability Summary

| Category | Portable | Not Portable | Total |
|----------|----------|--------------|-------|
| **Core Features** | 100% | 0% | 100% |
| **Research Features** | 100% | 0% | 100% |
| **UI Features** | 100% | 0% | 100% |
| **Infrastructure** | 90% | 10% | 100% |
| **AWS Features** | 0% | 100% | 100% |
| **K8s Features** | 0% | 100% | 100% |

**Overall Portability:** ~95% of features work locally

---

## 🎯 Key Insight

**All research functionality is portable!** 

The only features that aren't portable are:
1. **AWS cloud services** (S3, SageMaker, Bedrock, Lambda) - Optional enhancements
2. **Kubernetes orchestration** (auto-scaling, service discovery) - Infrastructure features

**These are infrastructure/orchestration features, not core research features.**

---

## 🔍 Verification Commands

```bash
# Check AWS endpoints (should fail gracefully)
curl -X POST http://localhost:8080/aws/sagemaker \
  -H "Content-Type: application/json" \
  -d '{"endpoint_name": "test", "payload": {}}'
# Expected: 503 Service Unavailable or error

# Check core research endpoint (should work)
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "max_papers": 5}'
# Expected: 200 OK or 202 Accepted

# Check health (should work)
curl http://localhost:8080/health
# Expected: 200 OK with health status
```

---

## 💡 Recommendation

**For Local Development:** ✅ **Everything you need is available!**

The AWS/Kubernetes features are:
- **Optional enhancements** for production deployment
- **Infrastructure features** for scaling and orchestration
- **Not required** for core research functionality

**You can develop and test everything locally without any AWS/Kubernetes features.**

---

## 📝 Files That Reference Cloud Features

These files contain cloud-specific code but gracefully degrade locally:

1. `src/api.py` - AWS endpoints (return 503 if unavailable)
2. `src/aws_integration.py` - AWS integration (disabled without credentials)
3. `src/nim_clients.py` - Default URLs use K8s DNS (but can be overridden)
4. `k8s/*.yaml` - All Kubernetes manifests (not used locally)
5. `src/web_ui.py` - Detects EKS vs local (shows appropriate UI)

**All gracefully handle local mode!** ✅

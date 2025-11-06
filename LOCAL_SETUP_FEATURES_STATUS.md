# Features Not Working in Local Setup

**Last Updated:** 2025-01-16  
**Environment:** Local Mac Studio / Development Setup

---

## 🔍 Current Local Setup Status (Checked)

**Date:** 2025-01-16  
**Python Version:** 3.12.12 ✅  
**Environment:** Local Mac Studio

### Feature Availability Check

| Feature | Status | Notes |
|---------|--------|-------|
| **Python 3.12+** | ✅ Available | Version 3.12.12 - Denario compatible |
| **Denario** | ❌ Not Installed | Python version OK, but package not installed |
| **SSE Streaming** | ❌ Not Available | `sseclient-py` not installed |
| **PDF Export** | ❌ Not Available | `reportlab` not installed |
| **Word Export** | ❌ Not Available | `python-docx` not installed |
| **Redis Cache** | ✅ Available | Redis server running (PONG response) |
| **Prometheus** | ❌ Not Available | `prometheus-client` not installed |
| **API Server** | ⚠️ Not Running | Need to start with `python -m src.api` |

### Quick Fixes

**To Enable Denario:**
```bash
pip install denario
export DENARIO_ENABLED=true
```

**To Enable SSE Streaming:**
```bash
pip install sseclient-py
```

**To Enable PDF Export:**
```bash
pip install reportlab
```

**To Enable Word Export:**
```bash
pip install python-docx
```

**To Enable Prometheus:**
```bash
pip install prometheus-client
```

---

## 🔴 Critical Features (Require Configuration)

### 1. Denario Integration
**Status:** ⚠️ **Disabled if Python < 3.12**

**Requirements:**
- Python 3.12+ (automatically disabled on Python 3.11 or earlier)
- `denario` package installed

**What Doesn't Work:**
- Research idea generation from synthesis gaps
- Methodology suggestions
- LaTeX paper structure generation
- Enhanced synthesis with AI-generated research questions

**How to Enable:**
```bash
# Upgrade to Python 3.12+
pyenv install 3.12.12
pyenv local 3.12.12

# Install Denario
pip install denario

# Enable in .env
echo "DENARIO_ENABLED=true" >> .env
```

**Current Status:** Check Python version:
```bash
python --version  # Must be 3.12.x or higher
```

---

### 2. Paid Paper Sources (Require API Keys)

**Status:** ⚠️ **Disabled by default, code ready**

#### IEEE Xplore
- **Status:** Code implemented, disabled without API key
- **Requires:** `IEEE_API_KEY` environment variable
- **Sign up:** https://developer.ieee.org/
- **Enable:** `ENABLE_IEEE=true` + API key

#### ACM Digital Library
- **Status:** Code implemented, disabled without API key
- **Requires:** `ACM_API_KEY` environment variable
- **Sign up:** https://libraries.acm.org/
- **Enable:** `ENABLE_ACM=true` + API key

#### SpringerLink
- **Status:** Code implemented, disabled without API key
- **Requires:** `SPRINGER_API_KEY` environment variable
- **Sign up:** https://dev.springernature.com/
- **Enable:** `ENABLE_SPRINGER=true` + API key

**What Works:** ✅ 4 free sources (arXiv, PubMed, Semantic Scholar, Crossref)

---

## 🟡 Optional Features (Require Additional Setup)

### 3. Real-Time Streaming (SSE)
**Status:** ⚠️ **May have connection issues**

**Requirements:**
- `sseclient-py` package installed
- Stable connection to API server

**Current Issues:**
- Broken pipe errors (now handled gracefully)
- Falls back to standard mode automatically

**How to Enable:**
```bash
pip install sseclient-py
```

**Note:** Streaming works but may encounter connection issues. System gracefully falls back to blocking mode.

---

### 4. Redis Caching
**Status:** ⚠️ **Optional, requires Redis**

**What Doesn't Work:**
- Multi-level caching (L1 memory → L2 Redis → L3 disk)
- Cache persistence across restarts
- Distributed caching

**How to Enable:**
```bash
# Install Redis
brew install redis  # macOS
# or
docker run -d -p 6379:6379 redis

# Set environment variable
export REDIS_URL="redis://localhost:6379"
```

**Current Status:** Works without Redis (uses in-memory cache only)

---

### 5. Prometheus Metrics
**Status:** ⚠️ **Optional, requires prometheus-client**

**What Doesn't Work:**
- Metrics collection endpoint (`/metrics`)
- Performance monitoring
- Request/response metrics

**How to Enable:**
```bash
pip install prometheus-client
```

**Current Status:** Metrics disabled, system works without it

---

### 6. AWS Integration Features
**Status:** ❌ **Requires AWS credentials**

**What Doesn't Work:**
- S3 backup storage
- SageMaker integration
- Lambda functions
- Bedrock integration
- EKS deployment features

**Files Affected:**
- `src/aws_integration.py` - All AWS features disabled without credentials

**How to Enable:**
```bash
# Install boto3
pip install boto3

# Configure AWS credentials
aws configure

# Set environment variables
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="us-east-1"
```

**Note:** Not needed for local development. Only required for cloud deployment.

---

## 🟠 UI Features (Partially Implemented)

### 7. Export Formats (Some Require Libraries)

**Status:** ⚠️ **Code exists, but some formats disabled in UI**

#### PDF Export
- **Status:** Code implemented, UI shows "coming soon"
- **Requires:** `reportlab` library
- **File:** `src/export_formats.py:434` (implementation exists)
- **Enable:** `pip install reportlab`

#### Word Export (.docx)
- **Status:** Code implemented, UI shows "coming soon"
- **Requires:** `python-docx` library
- **File:** `src/export_formats.py:329` (implementation exists)
- **Enable:** `pip install python-docx`

#### EndNote XML Export
- **Status:** Code implemented, UI shows "coming soon"
- **File:** `src/export_formats.py:826` (implementation exists)

**What Works:** ✅ JSON, Markdown, BibTeX, LaTeX, CSV, Excel, HTML, Citations (5 styles)

**Disabled in UI:** Lines 4261-4610 in `src/web_ui.py` show these buttons as `disabled=True`

---

### 8. UX Enhancement Features

**Status:** ⚠️ **Conditionally loaded, may not be available**

**What May Not Work:**
- Results gallery view
- Real-time agent panel
- Session stats dashboard
- Speed comparison demo
- Guided tour
- Enhanced loading animations
- Quick export panel
- AI suggestions
- Synthesis history dashboard
- Citation management export
- Enhanced pagination
- User preferences panel
- Accessibility features panel
- Enhanced error messages
- Contextual help system
- Notification system
- Query timing tracking

**Location:** `src/web_ui.py:182-199` (stubbed if `ux_enhancements` module unavailable)

**How to Enable:**
- Ensure `src/ux_enhancements.py` is importable
- Check for import errors in logs

---

## 🔵 Performance Features (Optional)

### 9. Hybrid Retrieval
**Status:** ⚠️ **Optional, requires configuration**

**What May Not Work:**
- BM25 sparse retrieval (if not configured)
- Citation graph retrieval (requires Semantic Scholar API key)
- RRF fusion (if hybrid retrieval disabled)

**How to Enable:**
```bash
export USE_HYBRID_RETRIEVAL=true
```

**Current Status:** Works with basic dense retrieval (embedding-based)

---

### 10. Cross-Encoder Reranking
**Status:** ⚠️ **Optional, requires configuration**

**What May Not Work:**
- Reranking step (if disabled)
- Improved relevance ordering

**How to Enable:**
```bash
export USE_RERANKING=true
```

**Current Status:** Works without reranking (uses embedding similarity only)

---

## 📊 Summary Table

| Feature | Status | Requirement | Impact |
|---------|--------|-------------|--------|
| **Denario** | ⚠️ Disabled | Python 3.12+ | Low (enhancement) |
| **IEEE/ACM/Springer** | ⚠️ Disabled | API keys | Medium (more sources) |
| **SSE Streaming** | ⚠️ Partial | sseclient-py | Low (fallback works) |
| **Redis Cache** | ⚠️ Optional | Redis server | Low (in-memory works) |
| **Prometheus** | ⚠️ Optional | prometheus-client | Low (monitoring only) |
| **AWS Integration** | ❌ Disabled | AWS credentials | Low (cloud only) |
| **PDF Export** | ⚠️ Disabled | reportlab | Low (other formats work) |
| **Word Export** | ⚠️ Disabled | python-docx | Low (other formats work) |
| **UX Enhancements** | ⚠️ Conditional | Module import | Medium (UI polish) |
| **Hybrid Retrieval** | ⚠️ Optional | Config flag | Medium (better results) |
| **Reranking** | ⚠️ Optional | Config flag | Medium (better ordering) |

---

## ✅ What DOES Work in Local Setup

### Core Features (100% Working)
- ✅ Multi-agent system (Scout, Analyst, Synthesizer, Coordinator)
- ✅ Local reasoning model (llama.cpp with Metal)
- ✅ Local embedding model (Sentence Transformers)
- ✅ Paper search from 4 free sources (arXiv, PubMed, Semantic Scholar, Crossref)
- ✅ Paper analysis and extraction
- ✅ Synthesis generation (themes, contradictions, gaps)
- ✅ Decision logging
- ✅ Web UI (Streamlit)
- ✅ API endpoints (FastAPI)
- ✅ Export formats: JSON, Markdown, BibTeX, LaTeX, CSV, Excel, HTML, Citations
- ✅ Qdrant vector database (local Docker)
- ✅ Session management
- ✅ Date filtering
- ✅ Source selection

---

## 🎯 Recommendations

### For Local Development
1. **Core features work** - No action needed
2. **Enable Denario** - Upgrade to Python 3.12+ if you want research idea generation
3. **Add API keys** - Get IEEE/ACM/Springer keys for more paper sources
4. **Install export libraries** - Add `reportlab` and `python-docx` for PDF/Word exports

### For Production/EKS Deployment
1. **All features available** - EKS deployment enables everything
2. **AWS integration** - Works with AWS credentials
3. **GPU acceleration** - NVIDIA NIMs provide better performance
4. **Auto-scaling** - Kubernetes handles load

---

## 🔍 How to Check Feature Status

### Check Denario
```bash
python -c "import denario; print('✅ Denario available')" 2>/dev/null || echo "❌ Denario not available"
```

### Check Paper Sources
```bash
curl http://localhost:8080/health | jq '.sources'
```

### Check Streaming
```bash
python -c "import sseclient; print('✅ SSE available')" 2>/dev/null || echo "❌ SSE not available"
```

### Check Redis
```bash
redis-cli ping 2>/dev/null && echo "✅ Redis available" || echo "❌ Redis not available"
```

### Check Export Libraries
```bash
python -c "import reportlab; print('✅ PDF export available')" 2>/dev/null || echo "❌ PDF export not available"
python -c "import docx; print('✅ Word export available')" 2>/dev/null || echo "❌ Word export not available"
```

---

## 📝 Notes

- **Most features are optional** - Core functionality works without them
- **Graceful degradation** - System falls back when features unavailable
- **Local setup is functional** - All essential features work locally
- **EKS deployment** - Enables all features with proper configuration

**Bottom Line:** Local setup supports all core research functionality. Optional features enhance the experience but aren't required for basic operation.


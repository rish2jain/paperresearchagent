# 🧪 Local Testing Guide - Agentic Researcher

**Last Updated:** 2025-11-05  
**Purpose:** Comprehensive guide for testing all features locally without EKS

---

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Activate virtual environment
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# 2. Install dependencies (if not already done)
pip install -r requirements.txt

# 3. Configure environment (optional - auto-loads from .env)
# Copy .env.example to .env and add your API keys
```

### Start Services

**Terminal 1 - FastAPI Backend:**
```bash
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8080
```

**Terminal 2 - Streamlit Web UI:**
```bash
streamlit run src/web_ui.py --server.port 8501
```

**Access Points:**
- Web UI: http://localhost:8501
- API: http://localhost:8080
- API Docs: http://localhost:8080/docs (Swagger UI)

---

## ✅ Features You Can Test Locally

### 1. **Web UI (Streamlit) - Full Experience** ✅

**All UI features work locally:**
- ✅ Research query interface
- ✅ Real-time agent decision logs
- ✅ Paper search and filtering
- ✅ Synthesis visualization
- ✅ Export functionality (all 13 formats)
- ✅ Session statistics
- ✅ Citation management
- ✅ Guided tour
- ✅ Dark theme
- ✅ Responsive design

**Test:**
```bash
streamlit run src/web_ui.py
# Open http://localhost:8501
```

---

### 2. **API Endpoints - Full REST API** ✅

**All endpoints available:**
- ✅ `GET /health` - Health check
- ✅ `POST /research` - Research query
- ✅ `GET /research/{session_id}` - Get results
- ✅ `GET /sessions` - List sessions
- ✅ `GET /export/{format}` - Export formats
- ✅ `POST /export/zotero` - Zotero export
- ✅ `POST /export/mendeley` - Mendeley export
- ✅ `POST /citation-graph` - Citation graph analysis
- ✅ `POST /pdf-analysis` - PDF analysis
- ✅ `POST /aws/*` - AWS integration endpoints

**Test:**
```bash
# Start API
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8080

# Test health
curl http://localhost:8080/health

# Test query
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "max_papers": 5}'

# View API docs
open http://localhost:8080/docs
```

---

### 3. **Agent System** ✅ (With Mock or build.nvidia.com)

**Works with:**
- ✅ Mock NIMs (for testing without GPU)
- ✅ build.nvidia.com (free, rate-limited)
- ✅ Local NIMs (if you have GPU)

**Agent Features:**
- ✅ Scout Agent - Paper search
- ✅ Analyst Agent - Paper analysis
- ✅ Synthesizer Agent - Synthesis generation
- ✅ Coordinator Agent - Meta-decisions
- ✅ Decision logging
- ✅ Real-time updates

**Test:**
```python
# Test agents directly
python src/test_agents.py

# Or use the API
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "transformer models", "max_papers": 10}'
```

---

### 4. **Paper Sources** ✅ (Free Sources Work)

**Free Sources (No API Key Required):**
- ✅ arXiv - Full functionality
- ✅ PubMed - Full functionality
- ✅ Semantic Scholar - Basic (API key recommended)
- ✅ Crossref - Full functionality

**Paid Sources (Require API Keys in .env):**
- ⚠️ IEEE - Requires `IEEE_API_KEY` in .env
- ⚠️ ACM - Requires `ACM_API_KEY` in .env
- ⚠️ Springer - Requires `SPRINGER_API_KEY` in .env

**Test:**
```bash
# Add to .env (optional)
IEEE_API_KEY=your_key
SPRINGER_API_KEY=your_key
SEMANTIC_SCHOLAR_API_KEY=your_key  # Recommended for higher rate limits

# Test in UI or API
# Sources are automatically enabled if API keys are present
```

---

### 5. **Export Formats - All 13 Formats** ✅

**All export formats work locally:**
1. ✅ BibTeX (.bib)
2. ✅ LaTeX (.tex)
3. ✅ Word Document (.docx)
4. ✅ PDF (.pdf)
5. ✅ CSV (.csv)
6. ✅ Excel (.xlsx)
7. ✅ EndNote (.enw)
8. ✅ HTML (.html)
9. ✅ XML (.xml)
10. ✅ JSON-LD (.jsonld)
11. ✅ Enhanced HTML (.html)
12. ✅ Zotero RIS (.ris)
13. ✅ Mendeley CSV (.csv)

**Test:**
```bash
# Via Web UI: Click export buttons
# Via API:
curl -X GET "http://localhost:8080/export/bibtex?session_id=xxx"
```

---

### 6. **UX Enhancements** ✅

**All 15 UX enhancements work locally:**
- ✅ Real-time agent decision logs
- ✅ Sticky/pinnable agent panel
- ✅ Loading animations
- ✅ Error notifications
- ✅ Success notifications
- ✅ Session statistics dashboard
- ✅ Quick export panel
- ✅ Citation management
- ✅ Guided tour
- ✅ Collapse/expand controls
- ✅ Executive summary
- ✅ Enhanced paper cards
- ✅ Dark theme support
- ✅ Responsive design
- ✅ Accessibility features

**Test:**
```bash
streamlit run src/web_ui.py
# Navigate through all UI features
```

---

### 7. **PDF Analysis** ✅ (Requires PDF Libraries)

**Features:**
- ✅ PDF text extraction
- ✅ Methodology extraction
- ✅ Results extraction
- ✅ Experimental setup extraction
- ✅ Figures/tables extraction
- ✅ Citation extraction
- ✅ Statistical results extraction

**Test:**
```bash
# Ensure PDF libraries installed
pip install PyPDF2 pdfplumber

# Test via API
curl -X POST http://localhost:8080/pdf-analysis \
  -H "Content-Type: application/json" \
  -d '{"pdf_url": "https://arxiv.org/pdf/2301.12345.pdf"}'
```

---

### 8. **Citation Graph Analysis** ✅

**Features:**
- ✅ Build citation networks
- ✅ Identify seminal papers
- ✅ Find influential papers
- ✅ Evolution timeline
- ✅ Crossref enrichment

**Test:**
```bash
# Via API
curl -X POST http://localhost:8080/citation-graph \
  -H "Content-Type: application/json" \
  -d '{"session_id": "xxx"}'
```

---

### 9. **AWS Integration** ✅ (If Credentials Configured)

**Features:**
- ✅ SageMaker endpoint invocation
- ✅ Lambda function invocation
- ✅ Bedrock model invocation
- ✅ S3 storage

**Test:**
```bash
# Add to .env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-2

# Test via API
curl -X POST http://localhost:8080/aws/bedrock \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "model_id": "anthropic.claude-3-5-sonnet-20241022"}'
```

---

### 10. **Configuration & Environment** ✅

**Automatic .env Loading:**
- ✅ Loads `.env` automatically on startup
- ✅ Supports all configuration options
- ✅ Graceful fallback if missing

**Test:**
```bash
# Create .env file
cat > .env << EOF
NGC_API_KEY=your_key
IEEE_API_KEY=your_key
SPRINGER_API_KEY=your_key
SEMANTIC_SCHOLAR_API_KEY=your_key
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-2
EOF

# Start services - .env is auto-loaded
python -m uvicorn src.api:app --reload
streamlit run src/web_ui.py
```

---

### 11. **Test Suite** ✅

**All tests work locally:**
```bash
# Run all tests
python -m pytest src/ -v

# Run specific test suites
python -m pytest src/test_agents.py -v
python -m pytest src/test_api.py -v
python -m pytest src/test_nim_clients.py -v
python -m pytest src/test_ux_enhancements.py -v
python -m pytest src/test_export_formats.py -v

# Run with asyncio mode
python -m pytest --asyncio-mode=auto src/test_agents.py -v
```

---

### 12. **Session Management** ✅

**Features:**
- ✅ Session persistence
- ✅ Session statistics
- ✅ Session history
- ✅ Multi-session support

**Test:**
```bash
# Via API
curl http://localhost:8080/sessions
curl http://localhost:8080/research/{session_id}
```

---

## 🔧 NIM Configuration Options

### Option 1: Mock NIMs (Testing Without GPU)

The system gracefully handles missing NIMs:
- Returns mock responses for testing
- UI still works
- Agent logic tested
- No actual inference

### Option 2: build.nvidia.com (Free, Rate-Limited)

```bash
# Add to .env or environment
export REASONING_NIM_URL="https://integrate.api.nvidia.com/v1"
export EMBEDDING_NIM_URL="https://integrate.api.nvidia.com/v1"
export NVIDIA_API_KEY="your_nvidia_api_key"
```

**Limitations:**
- Rate limits apply
- Requires NVIDIA API key
- May have latency

### Option 3: Local NIMs (Requires GPU)

```bash
# Run NIMs locally via Docker
docker run --gpus all -p 8000:8000 nvcr.io/nim/nvidia/llama-3.1-nemotron-nano-8b-v1:1.8.4
docker run --gpus all -p 8001:8001 nvcr.io/nim/nvidia/nv-embedqa-e5-v5:1.0.0

# Configure URLs
export REASONING_NIM_URL="http://localhost:8000"
export EMBEDDING_NIM_URL="http://localhost:8001"
```

---

## 📊 Testing Checklist

### Core Functionality
- [ ] Web UI loads and displays correctly
- [ ] API health endpoint responds
- [ ] Research query submission works
- [ ] Paper search results display
- [ ] Synthesis generation works
- [ ] Agent decision logs appear

### Export Features
- [ ] All 13 export formats work
- [ ] Export buttons functional
- [ ] Downloads start correctly
- [ ] File formats are valid

### UI/UX Features
- [ ] Real-time updates work
- [ ] Decision logs are visible
- [ ] Loading animations display
- [ ] Error messages are user-friendly
- [ ] Session stats display
- [ ] Guided tour works
- [ ] Dark theme applies

### Paper Sources
- [ ] Free sources work (arXiv, PubMed, Crossref)
- [ ] Paid sources work (if API keys provided)
- [ ] Source filtering works
- [ ] Date filtering works

### Advanced Features
- [ ] PDF analysis works (if PDFs provided)
- [ ] Citation graph works (if data available)
- [ ] AWS integration works (if credentials provided)
- [ ] Session management works

---

## 🐛 Troubleshooting

### NIMs Not Available

**Symptoms:** API returns "degraded" status, NIMs show as unavailable

**Solutions:**
1. Use mock mode (works automatically)
2. Configure build.nvidia.com URLs
3. Deploy local NIMs (requires GPU)

### Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Conflicts

```bash
# Check if ports are in use
lsof -i :8080  # API port
lsof -i :8501  # UI port

# Kill processes if needed
kill -9 <PID>
```

### Environment Variables Not Loading

```bash
# Verify .env file exists
ls -la .env

# Check if python-dotenv is installed
pip install python-dotenv

# Test loading
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('NGC_API_KEY'))"
```

---

## 📝 Quick Test Script

```bash
#!/bin/bash
# Quick local test script

echo "🧪 Testing Agentic Researcher Locally"
echo "======================================"

# 1. Check dependencies
echo "1. Checking dependencies..."
python -c "import streamlit; import fastapi; print('✅ Dependencies OK')"

# 2. Test API health (if running)
echo "2. Testing API..."
curl -s http://localhost:8080/health | python -m json.tool || echo "⚠️  API not running"

# 3. Test UI (if running)
echo "3. Testing UI..."
curl -s http://localhost:8501 | head -1 || echo "⚠️  UI not running"

# 4. Run test suite
echo "4. Running test suite..."
python -m pytest src/test_api.py -v --tb=short || echo "⚠️  Some tests failed"

echo ""
echo "✅ Local testing complete!"
```

---

## 🎯 Recommended Testing Order

1. **Start with UI** - Verify basic interface works
2. **Test API** - Verify endpoints respond
3. **Test Query** - Submit a simple research query
4. **Test Export** - Try different export formats
5. **Test Sources** - Verify paper sources work
6. **Test Advanced** - PDF analysis, citation graphs
7. **Run Tests** - Execute test suite

---

## 💡 Tips

- **Start Simple:** Begin with basic queries before testing advanced features
- **Use Mock Mode:** Test UI/UX without requiring NIMs
- **Check Logs:** Monitor console output for errors
- **Test Incrementally:** Test one feature at a time
- **Use API Docs:** Swagger UI at `/docs` is helpful for API testing

---

## 📚 Additional Resources

- `USER_TESTING_GUIDE.md` - Comprehensive user testing guide
- `CLAUDE.md` - Development documentation
- `docs/ENV_SETUP.md` - Environment setup details
- `README.md` - Project overview

---

**Happy Testing! 🚀**

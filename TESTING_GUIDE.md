# Testing Guide: Live vs Mock Services

## Overview

ResearchOps Agent can be tested with two different setups:

1. **Mock Services** - Simulated NIMs for testing without GPU/NVIDIA access
2. **Live Services** - Real NVIDIA NIMs for production-quality results

---

## 🔵 Mock Services (Testing Without Real NIMs)

### What Are Mock Services?

Mock services are **simulated versions** of NVIDIA NIMs that:
- ✅ Mimic the API structure of real NIMs
- ✅ Return properly formatted responses
- ✅ Work without GPU hardware or NVIDIA NGC credentials
- ✅ Enable testing the **entire workflow** without real AI models

### Available Mock Services

#### 1. **Mock Reasoning NIM** (`mock_reasoning_nim.py`)
- **Port**: 8000
- **Simulates**: `llama-3.1-nemotron-nano-8B-v1`
- **What it does**:
  - Returns mock text completions
  - Generates sample analysis responses
  - Provides template-based synthesis results
- **Use cases**:
  - Testing API integration
  - Testing agent workflow logic
  - Development without GPU access
  - CI/CD pipelines

#### 2. **Mock Embedding NIM** (`mock_embedding_nim.py`)
- **Port**: 8001
- **Simulates**: `nv-embedqa-e5-v5`
- **What it does**:
  - Returns random embedding vectors
  - Simulates semantic search (but without real similarity)
  - Provides proper API responses
- **Use cases**:
  - Testing embedding pipeline
  - Testing search workflow
  - Development without GPU access

### Limitations of Mock Services

⚠️ **What Mock Services DON'T Provide:**

- ❌ **Real Reasoning**: Responses are templates, not real AI analysis
- ❌ **Real Semantic Search**: Embeddings are random, not semantically meaningful
- ❌ **Quality Results**: Synthesis quality will be low/artificial
- ❌ **Accurate Relevance**: Paper filtering won't actually be relevant

**Example Mock Output:**
```
Query: "machine learning for medical imaging"
Mock Result: Generic template response, not actual analysis
```

### When to Use Mock Services

✅ **Use Mock Services When:**
- Developing locally without GPU access
- Testing API integration and workflow
- CI/CD automated testing
- Demonstrating system architecture
- Learning how the system works

---

## 🟢 Live Services (Production with Real NIMs)

### What Are Live Services?

Live services are **actual NVIDIA NIMs** that:
- ✅ Run real AI models on GPU hardware
- ✅ Provide actual reasoning and embeddings
- ✅ Generate production-quality research synthesis
- ✅ Require NVIDIA NGC credentials and GPU access

### Real NIM Services

#### 1. **Real Reasoning NIM**
- **Model**: `llama-3.1-nemotron-nano-8B-v1`
- **What it does**:
  - Analyzes papers with actual AI reasoning
  - Extracts methodology, findings, limitations
  - Synthesizes findings across papers
  - Identifies contradictions and gaps
- **Quality**: Production-grade research analysis

#### 2. **Real Embedding NIM**
- **Model**: `nv-embedqa-e5-v5`
- **What it does**:
  - Generates semantically meaningful embeddings
  - Enables real semantic search
  - Finds actually relevant papers
  - Calculates accurate similarity scores
- **Quality**: Real semantic understanding

### When to Use Live Services

✅ **Use Live Services When:**
- Running production workloads
- Getting actual research results
- Evaluating real synthesis quality
- Demonstrating to stakeholders
- Testing with real-world queries

---

## 🧪 What You Can Test

### 1. **Paper Source Integration** ✅ (Works with Both)

Test all 7 paper sources:
- **Free sources** (always work):
  - ✅ arXiv
  - ✅ PubMed
  - ✅ Semantic Scholar
  - ✅ Crossref
- **Optional sources** (require API keys):
  - ⚙️ IEEE Xplore
  - ⚙️ ACM Digital Library
  - ⚙️ SpringerLink

**Test Commands:**
```bash
# Test individual sources
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "transformer models", "max_papers": 5}'
```

**What to expect:**
- Mock: Papers found from real sources, but AI analysis is template-based
- Live: Papers found + real AI analysis with quality insights

### 2. **Multi-Agent Workflow** ✅ (Works with Both)

Test the 4-agent system:
- **Scout Agent**: Paper search (real sources work!)
- **Analyst Agent**: Paper analysis (mock = templates, live = real)
- **Synthesizer Agent**: Cross-paper synthesis (mock = templates, live = real)
- **Coordinator Agent**: Workflow decisions (works with both)

**Test via Web UI:**
1. Open http://localhost:8501
2. Enter query: "quantum computing applications"
3. Click "🚀 Start Research"
4. Watch agent decisions in real-time

**What to expect:**
- **Mock**: You'll see the workflow work, but results are generic
- **Live**: You'll see real insights, contradictions, gaps

### 3. **API Endpoints** ✅ (Works with Both)

Test all REST API endpoints:
- `GET /health` - Health check
- `POST /research` - Research synthesis
- `GET /sessions/{session_id}` - Session status
- `POST /export/bibtex` - BibTeX export
- `POST /export/latex` - LaTeX export

**Test Commands:**
```bash
# Health check
curl http://localhost:8080/health

# Research query
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "deep learning", "max_papers": 3}'

# BibTeX export
curl -X POST http://localhost:8080/export/bibtex \
  -H "Content-Type: application/json" \
  -d '{"papers": [...]}'
```

### 4. **Progress Indicators** ✅ (Works with Both)

Test real-time progress tracking:
- Stage-by-stage progress (Search → Analyze → Synthesize)
- NIM usage indicators
- Agent decision timeline

**Test via Web UI:**
- Watch progress bars update in real-time
- See which NIM is being used at each stage
- Review decision log

### 5. **Export Formats** ✅ (Works with Both)

Test export functionality:
- BibTeX citation export
- LaTeX document generation
- JSON results export
- Markdown export

**Test:**
```bash
# After getting research results
curl -X POST http://localhost:8080/export/bibtex \
  -H "Content-Type: application/json" \
  -d @research_results.json
```

### 6. **Error Handling** ✅ (Works with Both)

Test graceful degradation:
- Missing API keys (some sources skip gracefully)
- Network errors (fallback to available sources)
- Timeout handling
- Invalid queries

---

## 📊 Comparison Table

| Feature | Mock Services | Live Services |
|---------|---------------|---------------|
| **Paper Sources** | ✅ Real APIs work | ✅ Real APIs work |
| **Paper Search** | ✅ Real results | ✅ Real results |
| **Embeddings** | ⚠️ Random vectors | ✅ Real semantic |
| **Relevance Filtering** | ⚠️ Not accurate | ✅ Accurate |
| **Paper Analysis** | ⚠️ Template responses | ✅ Real AI analysis |
| **Synthesis** | ⚠️ Generic themes | ✅ Real insights |
| **Contradictions** | ⚠️ Template examples | ✅ Real findings |
| **Research Gaps** | ⚠️ Generic gaps | ✅ Real gaps |
| **Workflow Logic** | ✅ Fully functional | ✅ Fully functional |
| **API Integration** | ✅ Fully functional | ✅ Fully functional |
| **Export Formats** | ✅ Works perfectly | ✅ Works perfectly |
| **GPU Required** | ❌ No | ✅ Yes |
| **NGC Credentials** | ❌ No | ✅ Yes |
| **Setup Time** | ⚡ Minutes | ⏱️ Hours |

---

## 🚀 Quick Test Scenarios

### Scenario 1: Test Architecture (Mock Services)

**Goal**: Verify system works end-to-end

```bash
# Start with mocks (no GPU needed)
docker-compose up --build

# Test workflow
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "max_papers": 2}'

# Check: Did workflow complete? ✅
# Check: Are papers found? ✅ (real sources)
# Check: Is synthesis returned? ✅ (template)
```

### Scenario 2: Test Paper Sources (Mock Services)

**Goal**: Verify all 7 sources work

```bash
# Check logs for source results
docker-compose logs orchestrator | grep "Found.*papers from"

# Expected output (with free sources enabled):
# Found X papers from arXiv
# Found Y papers from PubMed
# Found Z papers from Semantic Scholar
# Found W papers from Crossref
```

### Scenario 3: Test Real Quality (Live Services)

**Goal**: Get production-quality results

```bash
# Start with real NIMs
export REASONING_NIM_URL="http://your-nim:8000"
export EMBEDDING_NIM_URL="http://your-nim:8001"
docker-compose up orchestrator web-ui

# Test with real query
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "quantum machine learning", "max_papers": 10}'

# Check: Real insights? ✅
# Check: Accurate relevance? ✅
# Check: Quality synthesis? ✅
```

---

## 🎯 Recommended Testing Approach

### Phase 1: Architecture Testing (Mock)
1. ✅ Start with mock services
2. ✅ Test all API endpoints
3. ✅ Verify workflow completes
4. ✅ Test paper source integration
5. ✅ Verify export formats work

### Phase 2: Integration Testing (Mock + Real Sources)
1. ✅ Use mock NIMs
2. ✅ Test all 7 paper sources
3. ✅ Verify source enable/disable
4. ✅ Test error handling

### Phase 3: Quality Testing (Live)
1. ✅ Switch to real NIMs
2. ✅ Test with real research queries
3. ✅ Evaluate synthesis quality
4. ✅ Compare against manual review

---

## 📝 Example Test Results

### Mock Service Test
```json
{
  "query": "machine learning",
  "papers_analyzed": 5,
  "common_themes": [
    "Generic theme about machine learning",
    "Template theme response"
  ],
  "contradictions": [
    {"paper1": "Paper A", "claim1": "Template claim"}
  ],
  "quality": "Template - not real analysis"
}
```

### Live Service Test
```json
{
  "query": "machine learning",
  "papers_analyzed": 5,
  "common_themes": [
    "Deep neural networks show superior performance in image classification",
    "Transfer learning reduces training data requirements",
    "Attention mechanisms improve sequence modeling"
  ],
  "contradictions": [
    {
      "paper1": "Smith et al. 2023",
      "claim1": "Batch normalization improves training stability",
      "paper2": "Jones et al. 2024",
      "claim2": "Layer normalization outperforms batch normalization",
      "conflict": "Disagreement on normalization techniques"
    }
  ],
  "quality": "Real AI analysis with actionable insights"
}
```

---

## 🔧 Switching Between Mock and Live

### Switch to Live Services

```bash
# Option 1: Environment variables
export REASONING_NIM_URL="http://your-reasoning-nim:8000"
export EMBEDDING_NIM_URL="http://your-embedding-nim:8001"
docker-compose up orchestrator web-ui

# Option 2: docker-compose override
cat > docker-compose.override.yml << EOF
version: '3.8'
services:
  orchestrator:
    environment:
      REASONING_NIM_URL: "http://your-nim:8000"
      EMBEDDING_NIM_URL: "http://your-nim:8001"
    depends_on: []
EOF
docker-compose up
```

### Switch Back to Mock Services

```bash
# Just use default docker-compose.yml
docker-compose down
docker-compose up --build
```

---

## ✅ What Works Great with Mocks

1. **Paper Source Integration** - All 7 sources work with real APIs
2. **API Endpoints** - Full REST API testing
3. **Workflow Logic** - Agent orchestration works perfectly
4. **Export Formats** - BibTeX, LaTeX exports work
5. **Error Handling** - Test failure scenarios
6. **UI Components** - All UI features work
7. **Progress Tracking** - Real-time updates work

## ⚠️ What Requires Live Services

1. **Quality Synthesis** - Real AI insights
2. **Accurate Relevance** - Real semantic search
3. **Real Contradictions** - Actual findings
4. **Research Gaps** - Real gap identification
5. **Production Results** - For actual research

---

**Summary**: Mock services let you test **everything except AI quality**. Use them for architecture, integration, and workflow testing. Use live services when you need actual research results.


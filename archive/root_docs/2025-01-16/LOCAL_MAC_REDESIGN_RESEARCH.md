# Local Mac Studio Redesign & Denario Integration Research

**Date:** 2025-01-16  
**Target Platform:** Mac Studio M3 Ultra (96GB unified memory)  
**Goal:** Redesign ResearchOps Agent to run entirely locally and integrate Denario features

---

## Executive Summary

This document outlines a comprehensive strategy to:
1. **Redesign** ResearchOps Agent to run entirely locally on Mac Studio M3 Ultra
2. **Replace** NVIDIA NIMs (cloud-based) with local Apple Silicon-optimized models
3. **Integrate** features from Denario multi-agent research system
4. **Maintain** all existing functionality while eliminating AWS costs

**Key Benefits:**
- ✅ Zero cloud costs (no AWS EKS)
- ✅ Privacy: All data stays local
- ✅ Faster: No network latency
- ✅ 96GB unified memory enables large models
- ✅ M3 Ultra GPU acceleration via Metal Performance Shaders

---

## Part 1: Local Mac Studio Architecture Redesign

### Current Architecture (AWS EKS)

```
┌─────────────────────────────────────────┐
│     AWS EKS Cluster (g5.2xlarge)       │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │Reasoning │  │Embedding │           │
│  │   NIM    │  │   NIM    │           │
│  │(NVIDIA) │  │(NVIDIA) │           │
│  └────┬─────┘  └────┬─────┘           │
│       │             │                  │
│       └─────────────┴─────────┐        │
│                               │        │
│  ┌──────────┐  ┌──────────┐  │        │
│  │  Qdrant  │  │  Agent   │  │        │
│  │ Vector DB│  │Orchestr. │  │        │
│  └──────────┘  └──────────┘  └────────┘
└─────────────────────────────────────────┘
```

### Proposed Local Architecture (Mac Studio)

```
┌─────────────────────────────────────────────────────┐
│              Mac Studio M3 Ultra                      │
│           96GB Unified Memory                         │
│                                                       │
│  ┌──────────────────────────────────────────────┐    │
│  │         Local Model Services                 │    │
│  │                                               │    │
│  │  ┌──────────────┐      ┌──────────────┐     │    │
│  │  │  Reasoning   │      │  Embedding   │     │    │
│  │  │  Model       │      │  Model       │     │    │
│  │  │              │      │              │     │    │
│  │  │ llama.cpp    │      │  MLX/Native  │     │    │
│  │  │ (Metal GPU)  │      │  (Metal GPU) │     │    │
│  │  │              │      │              │     │    │
│  │  │ Port: 8000   │      │ Port: 8001   │     │    │
│  │  └──────┬───────┘      └──────┬───────┘     │    │
│  │         │                      │              │    │
│  └─────────┼──────────────────────┼────────────┘    │
│            │                      │                  │
│  ┌─────────┴──────────────────────┴────────────┐    │
│  │         Agent Orchestrator                  │    │
│  │  (FastAPI + Streamlit UI)                    │    │
│  └─────────┬──────────────────────┬────────────┘    │
│            │                      │                  │
│  ┌─────────┴──────────┐  ┌────────┴──────────┐      │
│  │   Qdrant Local     │  │  Denario Agents   │      │
│  │   (Docker)         │  │  (AG2/LangGraph) │      │
│  └────────────────────┘  └──────────────────┘      │
└─────────────────────────────────────────────────────┘
```

---

## Part 2: Local Model Replacement Strategy

### 2.1 Reasoning Model (Replacing llama-3.1-nemotron-nano-8B)

**Option 1: llama.cpp with Metal Backend (Recommended)**

```python
# Install llama.cpp with Metal support
# Using llama-cpp-python with Metal backend
pip install llama-cpp-python[metal]

# Model: Llama 3.1 8B (quantized for efficiency)
# Location: ~/.local/share/models/llama-3.1-8b-instruct-q4_K_M.gguf
```

**Advantages:**
- ✅ Native Metal GPU acceleration
- ✅ Optimized for Apple Silicon
- ✅ Memory efficient (can run 8B model in <16GB)
- ✅ Fast inference (20-30 tokens/sec on M3 Ultra)
- ✅ Compatible with OpenAI API format

**Implementation:**

```python
# src/local_models/reasoning_model.py
from llama_cpp import Llama
import os

class LocalReasoningModel:
    """Local reasoning model using llama.cpp"""
    
    def __init__(self, model_path: str = None):
        model_path = model_path or os.path.expanduser(
            "~/.local/share/models/llama-3.1-8b-instruct-q4_K_M.gguf"
        )
        
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # Use all GPU layers
            n_ctx=4096,        # Context window
            verbose=False
        )
    
    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        """Generate completion matching NIM API"""
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            echo=False
        )
        return response['choices'][0]['text']
```

**Option 2: MLX Framework (Apple's Native Framework)**

```python
# Using MLX (Apple's machine learning framework)
pip install mlx-lm

# Model: mlx-community/llama-3.1-8b-instruct
from mlx_lm import load, generate

class MLXReasoningModel:
    """Reasoning model using MLX"""
    
    def __init__(self, model_name: str = "mlx-community/llama-3.1-8b-instruct"):
        self.model, self.tokenizer = load(model_name)
    
    def complete(self, prompt: str, max_tokens: int = 2048) -> str:
        response = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            temp=0.7
        )
        return response
```

**Recommendation:** Start with **llama.cpp** (more mature, better API compatibility), then evaluate MLX for performance.

### 2.2 Embedding Model (Replacing nv-embedqa-e5-v5)

**Option 1: Sentence Transformers with CoreML**

```python
# Using sentence-transformers optimized for Apple Silicon
pip install sentence-transformers

# Model: all-MiniLM-L6-v2 (384 dimensions, fast)
# Or: all-mpnet-base-v2 (768 dimensions, better quality)
from sentence_transformers import SentenceTransformer

class LocalEmbeddingModel:
    """Local embedding model"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # CoreML optimization for Apple Silicon
        self.model = SentenceTransformer(
            model_name,
            device='mps' if torch.backends.mps.is_available() else 'cpu'
        )
    
    def embed(self, text: str, input_type: str = "query") -> List[float]:
        """Generate embedding matching NIM API"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
```

**Option 2: Native MLX Embedding Model**

```python
# Using MLX-compatible embedding models
from mlx_lm import load_embedding

class MLXEmbeddingModel:
    """MLX-based embedding model"""
    
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model = load_embedding(model_name)
    
    def embed(self, text: str, input_type: str = "query") -> List[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()
```

**Recommendation:** Use **Sentence Transformers** with CoreML backend (mature, good performance).

### 2.3 Vector Database (Qdrant)

**Local Qdrant Setup:**

```bash
# Run Qdrant locally via Docker
docker run -d \
  --name qdrant-local \
  -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

Or use Qdrant's Python client with in-memory mode:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Local Qdrant instance
client = QdrantClient(
    url="http://localhost:6333",
    prefer_grpc=False
)
```

---

## Part 3: Denario Integration Strategy

### 3.1 Denario Architecture Overview

Based on [Denario's GitHub](https://github.com/AstroPilot-AI/Denario):

**Denario Components:**
- **AG2 Framework**: Agent orchestration
- **LangGraph**: Workflow management
- **cmbagent**: Research analysis backend
- **Workflow**: `get_idea()` → `get_method()` → `get_results()` → `get_paper()`

**Key Features:**
1. **Research Idea Generation**: From data description
2. **Methodology Development**: Automated method generation
3. **Results Computation**: Automated analysis
4. **Paper Generation**: LaTeX article generation with journal styles

### 3.2 Integration Points

#### Integration Point 1: Enhanced Research Workflow

**Current Flow:**
```
Query → Scout → Analyst → Synthesizer → Literature Review
```

**Enhanced Flow (with Denario):**
```
Query → Scout → Analyst → Synthesizer → Literature Review
                                    ↓
                    Denario Integration
                    ├─ Research Idea Generation
                    ├─ Methodology Suggestions
                    └─ Paper Structure Generation
```

**Implementation:**

```python
# src/denario_integration.py
from denario import Denario
from denario import Journal

class DenarioIntegration:
    """Integrate Denario features into ResearchOps Agent"""
    
    def __init__(self, project_dir: str = "./denario_projects"):
        self.denario = Denario(project_dir=project_dir)
    
    def generate_research_ideas(self, synthesis_result: Dict) -> List[str]:
        """Generate research ideas from synthesis gaps"""
        data_description = f"""
        Based on literature review synthesis:
        - Themes: {synthesis_result['common_themes']}
        - Gaps: {synthesis_result['research_gaps']}
        - Contradictions: {synthesis_result['contradictions']}
        """
        
        self.denario.set_data_description(data_description)
        idea = self.denario.get_idea()
        return idea
    
    def suggest_methodology(self, research_idea: str) -> str:
        """Generate methodology for research idea"""
        self.denario.set_idea(research_idea)
        method = self.denario.get_method()
        return method
    
    def generate_paper_structure(self, synthesis: Dict, journal: str = "APS") -> str:
        """Generate LaTeX paper structure"""
        # Use Denario's paper generation
        journal_map = {
            "APS": Journal.APS,
            "Nature": Journal.Nature,
            "IEEE": Journal.IEEE
        }
        
        self.denario.set_results(synthesis)
        paper = self.denario.get_paper(journal=journal_map.get(journal, Journal.APS))
        return paper
```

#### Integration Point 2: Multi-Agent Collaboration

**Denario uses AG2/LangGraph for agent orchestration:**

```python
# src/agents/denario_agents.py
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

class EnhancedCoordinatorAgent:
    """Coordinator agent with Denario integration"""
    
    def __init__(self, reasoning_client, denario_integration):
        self.reasoning = reasoning_client
        self.denario = denario_integration
    
    async def decide_workflow(self, synthesis: Dict) -> Dict:
        """Enhanced decision-making with Denario"""
        
        # Original decision logic
        quality = synthesis.get('quality_score', 0.0)
        
        if quality < 0.8:
            # Use Denario to generate research ideas from gaps
            gaps = synthesis.get('research_gaps', [])
            if gaps:
                research_ideas = self.denario.generate_research_ideas(synthesis)
                return {
                    "action": "generate_research_ideas",
                    "ideas": research_ideas,
                    "reasoning": "Low quality score, generating research ideas from gaps"
                }
        
        return {
            "action": "complete",
            "reasoning": "Synthesis quality sufficient"
        }
```

#### Integration Point 3: Paper Generation Enhancement

**Current:** Generate literature review (Markdown/PDF)

**Enhanced:** Generate full research paper structure with Denario

```python
# src/export_formats.py (enhancement)
from denario_integration import DenarioIntegration

class EnhancedPaperExport:
    """Export with Denario paper generation"""
    
    def __init__(self):
        self.denario = DenarioIntegration()
    
    def export_full_paper(
        self,
        synthesis: Dict,
        journal_style: str = "APS",
        include_methodology: bool = True
    ) -> str:
        """Generate full research paper using Denario"""
        
        # Generate research idea from synthesis
        idea = self.denario.generate_research_ideas(synthesis)
        
        # Generate methodology if requested
        if include_methodology:
            method = self.denario.suggest_methodology(idea)
            synthesis['methodology'] = method
        
        # Generate LaTeX paper
        paper = self.denario.generate_paper_structure(synthesis, journal_style)
        
        return paper
```

---

## Part 4: Implementation Roadmap

### Phase 1: Local Model Infrastructure (Week 1-2)

**Tasks:**
1. ✅ Set up llama.cpp with Metal backend
2. ✅ Download and configure Llama 3.1 8B model (quantized)
3. ✅ Set up Sentence Transformers for embeddings
4. ✅ Create local model service wrappers
5. ✅ Update `nim_clients.py` to support local models

**Deliverables:**
- `src/local_models/reasoning_model.py`
- `src/local_models/embedding_model.py`
- Local model service (FastAPI wrapper)
- Updated configuration system

### Phase 2: Local Qdrant & Services (Week 2)

**Tasks:**
1. ✅ Set up local Qdrant instance
2. ✅ Update vector database configuration
3. ✅ Remove AWS-specific dependencies
4. ✅ Test local vector operations

**Deliverables:**
- Local Qdrant setup script
- Updated `config.py` for local mode
- Migration guide

### Phase 3: Denario Integration (Week 3-4)

**Tasks:**
1. ✅ Install Denario and dependencies
2. ✅ Create Denario integration module
3. ✅ Integrate research idea generation
4. ✅ Integrate methodology suggestions
5. ✅ Integrate paper generation

**Deliverables:**
- `src/denario_integration.py`
- Enhanced agent system
- Paper generation enhancement

### Phase 4: Testing & Optimization (Week 4-5)

**Tasks:**
1. ✅ End-to-end testing
2. ✅ Performance optimization
3. ✅ Memory optimization
4. ✅ Documentation

**Deliverables:**
- Test suite for local mode
- Performance benchmarks
- Updated documentation

---

## Part 5: Technical Specifications

### 5.1 Model Requirements

**Reasoning Model:**
- **Model:** Llama 3.1 8B Instruct (quantized Q4_K_M)
- **Size:** ~5GB
- **Memory:** ~8GB RAM usage
- **Speed:** 20-30 tokens/sec (M3 Ultra)
- **Format:** GGUF (llama.cpp compatible)

**Embedding Model:**
- **Model:** all-MiniLM-L6-v2 (384 dim) or all-mpnet-base-v2 (768 dim)
- **Size:** ~80MB
- **Memory:** ~500MB RAM usage
- **Speed:** ~1000 embeddings/sec (M3 Ultra)

**Total Memory Usage:**
- Reasoning: 8GB
- Embedding: 0.5GB
- Qdrant: 2-4GB (depends on paper count)
- Agent System: 1-2GB
- **Total: ~12-15GB** (well within 96GB capacity)

### 5.2 Dependencies

**New Dependencies:**

```txt
# Local model inference
llama-cpp-python[metal]==0.2.79
sentence-transformers==2.2.2
torch>=2.0.0  # With MPS support

# Denario integration
denario[app]>=1.0.0
ag2>=0.1.0
langgraph>=0.1.0

# Optional: MLX alternative
mlx-lm>=0.1.0
```

**Updated Dependencies:**

```txt
# Remove AWS-specific
# boto3  # Optional, keep for S3 backup
# botocore  # Optional

# Keep existing
qdrant-client>=1.7.0
fastapi>=0.104.1
streamlit>=1.29.0
```

### 5.3 Configuration Changes

**New Configuration Options:**

```python
# src/config.py additions

@dataclass
class LocalModelConfig:
    """Local model configuration"""
    use_local_models: bool = True
    reasoning_model_path: str = "~/.local/share/models/llama-3.1-8b-instruct-q4_K_M.gguf"
    embedding_model_name: str = "all-MiniLM-L6-v2"
    qdrant_local_url: str = "http://localhost:6333"
    enable_denario: bool = True
    denario_project_dir: str = "./denario_projects"
```

---

## Part 6: Performance Expectations

### 6.1 Speed Comparison

| Operation | AWS EKS (GPU) | Mac Studio (Local) |
|-----------|---------------|-------------------|
| Embedding Generation | ~50ms | ~10ms (no network) |
| Reasoning (100 tokens) | ~200ms | ~400ms (CPU) |
| Reasoning (100 tokens, GPU) | ~200ms | ~150ms (Metal) |
| Paper Search | ~500ms | ~200ms (local DB) |

**Overall:** Local mode may be **slightly slower** for reasoning but **faster** for embeddings and database operations due to no network latency.

### 6.2 Cost Comparison

| Resource | AWS EKS | Mac Studio |
|----------|---------|------------|
| EC2 Instances | ~$2/hour | $0 (already owned) |
| EKS Control Plane | ~$0.10/hour | $0 |
| Data Transfer | Variable | $0 |
| **Total** | **~$2-3/hour** | **$0** |

**Savings:** ~$1,500-2,000/month

---

## Part 7: Migration Guide

### 7.1 Step-by-Step Migration

**Step 1: Install Local Models**

```bash
# Create models directory
mkdir -p ~/.local/share/models

# Download Llama 3.1 8B (quantized)
wget https://huggingface.co/.../llama-3.1-8b-instruct-q4_K_M.gguf \
  -O ~/.local/share/models/llama-3.1-8b-instruct-q4_K_M.gguf

# Install dependencies
pip install llama-cpp-python[metal] sentence-transformers
```

**Step 2: Update Configuration**

```bash
# Set environment variables
export USE_LOCAL_MODELS=true
export REASONING_MODEL_PATH=~/.local/share/models/llama-3.1-8b-instruct-q4_K_M.gguf
export EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
export QDRANT_URL=http://localhost:6333
```

**Step 3: Start Local Services**

```bash
# Start Qdrant
docker run -d --name qdrant-local -p 6333:6333 qdrant/qdrant

# Start local model services (optional, or run in-process)
python src/local_models/service.py
```

**Step 4: Run Agent System**

```bash
# Run with local models
python -m src.api
```

### 7.2 Backward Compatibility

**Strategy:** Support both local and cloud modes via configuration

```python
# src/nim_clients.py (enhanced)

class ReasoningClient:
    """Unified reasoning client (local or cloud)"""
    
    def __init__(self):
        if config.use_local_models:
            self.client = LocalReasoningModel()
        else:
            self.client = ReasoningNIMClient()
    
    async def complete(self, prompt: str) -> str:
        if isinstance(self.client, LocalReasoningModel):
            return self.client.complete(prompt)
        else:
            return await self.client.complete(prompt)
```

---

## Part 8: Denario Feature Integration Details

### 8.1 Research Idea Generation

**Integration Point:** After synthesis, before final output

```python
# In Synthesizer Agent
async def synthesize(self, papers: List[Paper]) -> Dict:
    # Existing synthesis logic
    synthesis = await self._synthesize_papers(papers)
    
    # NEW: Denario integration
    if self.denario_enabled:
        research_ideas = self.denario.generate_research_ideas(synthesis)
        synthesis['research_ideas'] = research_ideas
    
    return synthesis
```

### 8.2 Methodology Suggestions

**Integration Point:** When user asks for methodology

```python
# New API endpoint
@router.post("/research/methodology")
async def suggest_methodology(request: MethodologyRequest):
    """Generate methodology suggestions using Denario"""
    
    denario = DenarioIntegration()
    denario.set_data_description(request.data_description)
    
    idea = denario.get_idea()
    method = denario.get_method()
    
    return {
        "research_idea": idea,
        "methodology": method
    }
```

### 8.3 Paper Generation

**Integration Point:** Export functionality

```python
# Enhanced export
@router.post("/research/export/paper")
async def export_paper(request: PaperExportRequest):
    """Export full research paper using Denario"""
    
    synthesis = await get_synthesis(request.synthesis_id)
    denario = DenarioIntegration()
    
    # Generate paper
    paper = denario.generate_paper_structure(
        synthesis,
        journal_style=request.journal_style
    )
    
    return Response(
        content=paper,
        media_type="text/latex",
        headers={"Content-Disposition": f"attachment; filename=paper.tex"}
    )
```

---

## Part 9: Testing Strategy

### 9.1 Unit Tests

```python
# tests/test_local_models.py
def test_local_reasoning_model():
    model = LocalReasoningModel()
    result = model.complete("Hello, world!")
    assert len(result) > 0

def test_local_embedding_model():
    model = LocalEmbeddingModel()
    embedding = model.embed("test text")
    assert len(embedding) == 384  # all-MiniLM-L6-v2 dimension
```

### 9.2 Integration Tests

```python
# tests/test_local_integration.py
async def test_full_local_workflow():
    """Test complete workflow with local models"""
    agent = ResearchOpsAgent(
        reasoning_client=LocalReasoningModel(),
        embedding_client=LocalEmbeddingModel()
    )
    
    result = await agent.run("machine learning for medical imaging")
    assert result['papers_analyzed'] > 0
```

### 9.3 Performance Tests

```python
# tests/test_performance.py
def test_embedding_performance():
    """Benchmark embedding generation"""
    model = LocalEmbeddingModel()
    
    start = time.time()
    for _ in range(100):
        model.embed("test text")
    elapsed = time.time() - start
    
    assert elapsed < 1.0  # Should be <10ms per embedding
```

---

## Part 10: Next Steps

### Immediate Actions

1. **Research & Evaluation:**
   - [ ] Test llama.cpp performance on M3 Ultra
   - [ ] Compare MLX vs llama.cpp
   - [ ] Evaluate embedding model options
   - [ ] Test Denario installation and basic usage

2. **Prototype Development:**
   - [ ] Create local model service wrapper
   - [ ] Update configuration system
   - [ ] Create migration script
   - [ ] Build Denario integration module

3. **Testing:**
   - [ ] Unit tests for local models
   - [ ] Integration tests
   - [ ] Performance benchmarks
   - [ ] User acceptance testing

### Long-term Enhancements

1. **Optimization:**
   - Model quantization optimization
   - Batch processing improvements
   - Memory usage optimization

2. **Features:**
   - Real-time model switching
   - Model versioning
   - A/B testing framework

3. **Integration:**
   - Deeper Denario integration
   - Additional research tools
   - Collaboration features

---

## References

- [Denario GitHub](https://github.com/AstroPilot-AI/Denario)
- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)
- [MLX Framework](https://github.com/ml-explore/mlx)
- [Sentence Transformers](https://www.sbert.net/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

---

**Status:** Research Complete - Ready for Implementation


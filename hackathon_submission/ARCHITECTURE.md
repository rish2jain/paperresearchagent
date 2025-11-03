# Agentic Scholar - Architecture Diagrams

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER INTERACTION                             │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         Web Browser                              │    │
│  │  "Find papers on machine learning for medical imaging"          │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                  │                                        │
│                                  │ HTTP Request                           │
│                                  ▼                                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         AMAZON EKS CLUSTER                                │
│                   (research-ops namespace)                                │
│                                                                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      WEB UI (Streamlit)                           │  │
│  │                    LoadBalancer Service                           │  │
│  │                     Port 80 → 8501                                │  │
│  └──────────────────────────────┬────────────────────────────────────┘  │
│                                  │                                        │
│                                  │ REST API                               │
│                                  ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │              AGENT ORCHESTRATOR (Python/FastAPI)                  │  │
│  │                        ClusterIP Service                          │  │
│  │                                                                   │  │
│  │   ┌──────────────────────────────────────────────────────────┐  │  │
│  │   │  Multi-Agent Coordination (LangGraph/CrewAI)             │  │  │
│  │   │  • Scout Agent      • Analyst Agent                      │  │  │
│  │   │  • Synthesizer Agent • Coordinator Agent                 │  │  │
│  │   └──────────────────────────────────────────────────────────┘  │  │
│  │                                                                   │  │
│  └──┬────────────────────┬──────────────────────┬────────────────┬──┘  │
│     │                    │                      │                │      │
│     │ Reasoning          │ Embedding            │ Vector         │      │
│     │ Requests           │ Requests             │ Operations     │      │
│     ▼                    ▼                      ▼                │      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐         │      │
│  │ REASONING   │  │  EMBEDDING   │  │  QDRANT        │         │      │
│  │    NIM      │  │     NIM      │  │  Vector DB     │         │      │
│  │             │  │              │  │                │         │      │
│  │  llama-3.1  │  │ nv-embedqa   │  │  Paper         │         │      │
│  │  nemotron   │  │   -e5-v5     │  │  Embeddings    │         │      │
│  │  nano-8B    │  │              │  │                │         │      │
│  │             │  │              │  │  Persistent    │         │      │
│  │ ClusterIP   │  │  ClusterIP   │  │  Volume        │         │      │
│  │ :8000       │  │  :8001       │  │  :6333         │         │      │
│  │             │  │              │  │                │         │      │
│  │ GPU: 1x     │  │  GPU: 1x     │  │  CPU: 1x       │         │      │
│  │ g5.2xlarge  │  │  g5.xlarge   │  │  m5.large      │         │      │
│  └─────────────┘  └──────────────┘  └────────────────┘         │      │
│                                                                  │      │
│                                                                  │      │
│  External Storage (Optional)                                    │      │
│  ┌────────────────────────────────────────────────────────┐    │      │
│  │           Amazon S3 (research-ops-storage)             │◄───┘      │
│  │   • Paper PDFs    • Analysis Results    • Reports      │           │
│  └────────────────────────────────────────────────────────┘           │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Agent Workflow (Sequential Flow)

```
USER INPUT: "Find papers on ML for medical imaging"
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: COORDINATOR AGENT (Planning)                       │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Uses: Reasoning NIM                                     │ │
│ │ Decision: Plan search strategy                          │ │
│ │ Output: Search plan with target paper count            │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: SCOUT AGENT (Information Retrieval)                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Uses: Embedding NIM                                     │ │
│ │ Steps:                                                  │ │
│ │   1. Embed user query → [vector]                       │ │
│ │   2. Search arXiv, PubMed APIs                         │ │
│ │   3. Embed paper abstracts → [vectors]                 │ │
│ │   4. Calculate similarity scores                       │ │
│ │   5. Filter by threshold (0.7)                         │ │
│ │   6. Store embeddings in Qdrant                        │ │
│ │ Output: List of 10 relevant papers                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: AUTONOMOUS DECISION POINT                          │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ COORDINATOR evaluates: "Do we need more papers?"       │ │
│ │ Uses: Reasoning NIM                                     │ │
│ │                                                         │ │
│ │ Decision Logic:                                         │ │
│ │   IF papers_found >= 10 AND topics_diverse            │ │
│ │      → PROCEED to analysis                             │ │
│ │   ELSE                                                  │ │
│ │      → RETURN to Scout Agent for more papers           │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: ANALYST AGENT (Parallel Processing)                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Uses: Reasoning NIM                                     │ │
│ │                                                         │ │
│ │  Paper 1 ─┐                                            │ │
│ │  Paper 2 ─┤                                            │ │
│ │  Paper 3 ─┼─→ [Parallel Analysis] ─→ Structured Data  │ │
│ │  Paper 4 ─┤                                            │ │
│ │  Paper N ─┘                                            │ │
│ │                                                         │ │
│ │ Extracts for each:                                      │ │
│ │   • Research question                                  │ │
│ │   • Methodology                                        │ │
│ │   • Key findings                                       │ │
│ │   • Limitations                                        │ │
│ │ Output: List of structured analyses                    │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 5: SYNTHESIZER AGENT (Cross-Document Reasoning)       │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Uses: BOTH Reasoning NIM + Embedding NIM               │ │
│ │                                                         │ │
│ │ Step 1: EMBEDDING NIM                                  │ │
│ │   • Embed all findings                                 │ │
│ │   • Cluster similar findings → themes                  │ │
│ │                                                         │ │
│ │ Step 2: REASONING NIM                                  │ │
│ │   • Analyze clusters for patterns                      │ │
│ │   • Identify contradictions                            │ │
│ │   • Identify research gaps                             │ │
│ │                                                         │ │
│ │ Output: Synthesis with themes, contradictions, gaps    │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 6: QUALITY CHECK (Autonomous Decision)                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ COORDINATOR evaluates: "Is synthesis complete?"        │ │
│ │ Uses: Reasoning NIM                                     │ │
│ │                                                         │ │
│ │ Criteria:                                               │ │
│ │   • Sufficient themes identified?                      │ │
│ │   • Contradictions properly analyzed?                  │ │
│ │   • Research gaps well-defined?                        │ │
│ │                                                         │ │
│ │   IF quality_score >= 0.8                              │ │
│ │      → PROCEED to report                               │ │
│ │   ELSE                                                  │ │
│ │      → REFINE synthesis                                │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 7: REPORT GENERATION                                  │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Uses: Reasoning NIM                                     │ │
│ │ Generates: Structured literature review                │ │
│ │   • Executive Summary                                   │ │
│ │   • Common Themes                                       │ │
│ │   • Key Findings                                        │ │
│ │   • Contradictions & Debates                           │ │
│ │   • Research Gaps                                       │ │
│ │   • Recommendations                                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
                  USER RECEIVES REPORT
                  (Total time: 2-3 minutes)
```

---

## 3. NIM Integration Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     REASONING NIM ARCHITECTURE                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Kubernetes Pod: reasoning-nim                           │ │
│  │                                                          │ │
│  │  ┌────────────────────────────────────────────────────┐ │ │
│  │  │  NVIDIA NIM Container                              │ │ │
│  │  │                                                    │ │ │
│  │  │  Model: llama-3.1-nemotron-nano-8b-instruct      │ │ │
│  │  │  Framework: NVIDIA Triton Inference Server       │ │ │
│  │  │  GPU: 1x NVIDIA A10G (g5.2xlarge)                │ │ │
│  │  │  Memory: 16Gi                                     │ │ │
│  │  │                                                    │ │ │
│  │  │  Endpoints:                                        │ │ │
│  │  │    • /v1/completions  (text generation)          │ │ │
│  │  │    • /v1/chat/completions (chat interface)       │ │ │
│  │  │    • /v1/health/live   (liveness probe)          │ │ │
│  │  │    • /v1/health/ready  (readiness probe)         │ │ │
│  │  │                                                    │ │ │
│  │  │  Environment:                                      │ │ │
│  │  │    NGC_API_KEY: <secret>                          │ │ │
│  │  │    NIM_CACHE_PATH: /opt/nim/.cache               │ │ │
│  │  └────────────────────────────────────────────────────┘ │ │
│  │                                                          │ │
│  │  PersistentVolumeClaim: reasoning-nim-cache (50Gi)     │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                 │
│                              │ ClusterIP Service (:8000)       │
│                              ▼                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    EMBEDDING NIM ARCHITECTURE                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Kubernetes Pod: embedding-nim                           │ │
│  │                                                          │ │
│  │  ┌────────────────────────────────────────────────────┐ │ │
│  │  │  NVIDIA NIM Container                              │ │ │
│  │  │                                                    │ │ │
│  │  │  Model: nv-embedqa-e5-v5                          │ │ │
│  │  │  Framework: NVIDIA Triton Inference Server       │ │ │
│  │  │  GPU: 1x NVIDIA A10G (g5.xlarge)                 │ │ │
│  │  │  Memory: 8Gi                                      │ │ │
│  │  │                                                    │ │ │
│  │  │  Endpoints:                                        │ │ │
│  │  │    • /v1/embeddings  (text embedding)            │ │ │
│  │  │    • /v1/health/live   (liveness probe)          │ │ │
│  │  │    • /v1/health/ready  (readiness probe)         │ │ │
│  │  │                                                    │ │ │
│  │  │  Features:                                         │ │ │
│  │  │    • Batch embedding (up to 128 texts)           │ │ │
│  │  │    • Input types: "query" or "passage"           │ │ │
│  │  │    • Output: 1024-dim vectors                     │ │ │
│  │  └────────────────────────────────────────────────────┘ │ │
│  │                                                          │ │
│  │  PersistentVolumeClaim: embedding-nim-cache (20Gi)     │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                 │
│                              │ ClusterIP Service (:8001)       │
│                              ▼                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow Diagram

```
USER QUERY: "machine learning for medical imaging"
     │
     │ HTTP POST /research
     ▼
┌─────────────────────────────────────────────────┐
│  Web UI (Streamlit)                             │
│  • Validates input                              │
│  • Shows loading state                          │
└──────────┬──────────────────────────────────────┘
           │ REST API
           ▼
┌─────────────────────────────────────────────────┐
│  Agent Orchestrator                             │
│  • Receives request                             │
│  • Initializes workflow state                   │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 1: Embed Query
           ▼
┌─────────────────────────────────────────────────┐
│  Embedding NIM                                  │
│  Input: "machine learning for medical imaging"  │
│  Output: [0.23, -0.45, 0.67, ... ] (1024-dim)  │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 2: Search Papers
           ▼
┌─────────────────────────────────────────────────┐
│  Scout Agent                                    │
│  • Queries arXiv API                            │
│  • Retrieves 50 candidate papers                │
│  • Extracts abstracts                           │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 3: Embed Abstracts (Batch)
           ▼
┌─────────────────────────────────────────────────┐
│  Embedding NIM                                  │
│  Input: [abstract1, abstract2, ..., abstract50]│
│  Output: 50 x [1024-dim vectors]                │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 4: Calculate Similarity
           ▼
┌─────────────────────────────────────────────────┐
│  Scout Agent                                    │
│  • Cosine similarity(query_vec, paper_vecs)    │
│  • Rank papers by similarity                    │
│  • Filter: similarity >= 0.7                    │
│  • Select top 10 papers                         │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 5: Store Embeddings
           ▼
┌─────────────────────────────────────────────────┐
│  Qdrant Vector Database                         │
│  • Store paper embeddings                       │
│  • Create collection: "research-papers"         │
│  • Index for fast retrieval                     │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 6: Decision Point
           ▼
┌─────────────────────────────────────────────────┐
│  Coordinator Agent                              │
│  Question: "Do we have enough papers?"          │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 7: Evaluate Coverage
           ▼
┌─────────────────────────────────────────────────┐
│  Reasoning NIM                                  │
│  Input: "Papers: 10, Topics: [CNN, RNN, ...]"  │
│  Output: "YES - sufficient coverage"            │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 8: Parallel Analysis
           ▼
┌─────────────────────────────────────────────────┐
│  Analyst Agent (10 parallel tasks)              │
│  Paper 1 ──→ Extract structure ──→ Analysis 1   │
│  Paper 2 ──→ Extract structure ──→ Analysis 2   │
│  ...                                             │
│  Paper 10 ──→ Extract structure ──→ Analysis 10 │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 9: Extract Info (10x calls)
           ▼
┌─────────────────────────────────────────────────┐
│  Reasoning NIM (batched)                        │
│  For each paper:                                │
│    Input: Paper text                            │
│    Output: {                                    │
│      "research_question": "...",                │
│      "methodology": "...",                      │
│      "key_findings": [...],                     │
│      "limitations": [...]                       │
│    }                                            │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 10: Cluster Findings
           ▼
┌─────────────────────────────────────────────────┐
│  Synthesizer Agent                              │
│  • Collect all findings (30+ statements)        │
│  • Prepare for embedding                        │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 11: Embed Findings
           ▼
┌─────────────────────────────────────────────────┐
│  Embedding NIM                                  │
│  Input: [finding1, finding2, ..., finding30]   │
│  Output: 30 x [1024-dim vectors]                │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 12: Identify Patterns
           ▼
┌─────────────────────────────────────────────────┐
│  Synthesizer Agent                              │
│  • Cluster similar findings (similarity > 0.85)│
│  • Identify 3-5 major themes                    │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 13: Reason About Patterns
           ▼
┌─────────────────────────────────────────────────┐
│  Reasoning NIM                                  │
│  Input: Clustered findings                      │
│  Tasks:                                         │
│    1. Identify contradictions                   │
│    2. Find research gaps                        │
│    3. Generate recommendations                  │
│  Output: Synthesis document                     │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 14: Quality Check
           ▼
┌─────────────────────────────────────────────────┐
│  Coordinator Agent                              │
│  Question: "Is synthesis complete?"             │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 15: Final Evaluation
           ▼
┌─────────────────────────────────────────────────┐
│  Reasoning NIM                                  │
│  Input: Synthesis quality metrics               │
│  Output: "YES - quality score: 0.92"            │
└──────────┬──────────────────────────────────────┘
           │
           │ Step 16: Generate Report
           ▼
┌─────────────────────────────────────────────────┐
│  Reasoning NIM                                  │
│  Input: All synthesis data                      │
│  Output: Formatted literature review            │
└──────────┬──────────────────────────────────────┘
           │
           │ Return Response
           ▼
┌─────────────────────────────────────────────────┐
│  Web UI                                         │
│  • Display report                               │
│  • Show agent reasoning trace                   │
│  • Visualize paper relationships                │
└─────────────────────────────────────────────────┘
           │
           ▼
      USER SEES RESULT
```

---

## 5. Deployment Flow Diagram

```
DEVELOPER WORKSTATION
     │
     │ 1. Write Code
     │ 2. Build Docker Images
     │
     ▼
┌─────────────────────────────────────────┐
│  Docker Registry                        │
│  • research-ops-agent:latest            │
│  • research-ops-ui:latest               │
└──────────┬──────────────────────────────┘
           │
           │ 3. eksctl create cluster
           ▼
┌─────────────────────────────────────────┐
│  AWS EKS Cluster                        │
│  • Control Plane (managed)              │
│  • 2x g5.2xlarge worker nodes           │
│  • VPC, Subnets, Security Groups        │
└──────────┬──────────────────────────────┘
           │
           │ 4. kubectl apply -f k8s/
           ▼
┌─────────────────────────────────────────┐
│  Kubernetes Resources Created:          │
│  • Namespace: research-ops              │
│  • Secrets: NGC credentials             │
│  • PVCs: Storage volumes                │
│  • Deployments: 5 services              │
│  • Services: Load balancers             │
└──────────┬──────────────────────────────┘
           │
           │ 5. Pull NIM images from nvcr.io
           ▼
┌─────────────────────────────────────────┐
│  NVIDIA NGC Registry                    │
│  • llama-3.1-nemotron-nano-8b:latest   │
│  • nv-embedqa-e5-v5:latest              │
└──────────┬──────────────────────────────┘
           │
           │ 6. Deploy to EKS
           ▼
┌─────────────────────────────────────────┐
│  Running Pods (5 total):                │
│  ✅ reasoning-nim-xxxxx                 │
│  ✅ embedding-nim-xxxxx                 │
│  ✅ qdrant-xxxxx                        │
│  ✅ agent-orchestrator-xxxxx            │
│  ✅ web-ui-xxxxx                        │
└──────────┬──────────────────────────────┘
           │
           │ 7. Expose via LoadBalancer
           ▼
┌─────────────────────────────────────────┐
│  External Access:                       │
│  • http://xxx.elb.amazonaws.com (UI)    │
│  • http://yyy.elb.amazonaws.com (API)   │
└─────────────────────────────────────────┘
           │
           ▼
     USERS ACCESS SYSTEM
```

---

## 6. Cost Optimization Architecture

```
DEVELOPMENT PHASE (30 hours)
┌────────────────────────────────────────┐
│  build.nvidia.com (FREE)               │
│  • Test Reasoning NIM                  │
│  • Test Embedding NIM                  │
│  • Develop agent logic                 │
│  • NO AWS COSTS                        │
└────────────────────────────────────────┘

INTEGRATION PHASE (6 hours)
┌────────────────────────────────────────┐
│  EKS Cluster (PAID)                    │
│  • Deploy both NIMs                    │
│  • Integrate agents                    │
│  • Cost: ~$7                           │
└────────────────────────────────────────┘

TESTING PHASE (4 hours)
┌────────────────────────────────────────┐
│  EKS Cluster (PAID)                    │
│  • End-to-end testing                  │
│  • Performance optimization            │
│  • Cost: ~$5                           │
└────────────────────────────────────────┘

DEMO PHASE (2 hours)
┌────────────────────────────────────────┐
│  EKS Cluster (PAID)                    │
│  • Record video                        │
│  • Live demonstrations                 │
│  • Cost: ~$2                           │
└────────────────────────────────────────┘

TOTAL AWS COST: ~$14
REMAINING BUDGET: $86 buffer
```

---

## 7. Agentic Decision Flow

```
                    START
                      │
                      ▼
        ┌─────────────────────────┐
        │  Initial Query Received │
        └─────────┬───────────────┘
                  │
                  ▼
        ┌─────────────────────────┐
        │ SCOUT: Search Papers    │
        │ • Embed query           │
        │ • Find candidates       │
        │ • Rank by relevance     │
        └─────────┬───────────────┘
                  │
                  ▼
    ┌─────────────────────────────────┐
    │ COORDINATOR DECISION POINT #1   │
    │ "Do we have enough papers?"     │
    │ Uses: Reasoning NIM             │
    └──────┬──────────────────┬───────┘
           │                  │
       YES │                  │ NO
           │                  │
           ▼                  ▼
    ┌──────────┐      ┌──────────────┐
    │ Continue │      │ Search More  │
    │ to       │      │ Papers with  │
    │ Analysis │      │ Different    │
    │          │      │ Query        │
    └────┬─────┘      └──────┬───────┘
         │                   │
         │                   └─────┐
         │                         │
         ▼                         │
    ┌────────────────────────┐    │
    │ ANALYST: Process       │◄───┘
    │ Papers in Parallel     │
    │ • Extract structure    │
    │ • Identify findings    │
    └─────────┬──────────────┘
              │
              ▼
    ┌─────────────────────────┐
    │ SYNTHESIZER: Analyze    │
    │ • Cluster findings      │
    │ • Find patterns         │
    │ • Identify gaps         │
    └─────────┬───────────────┘
              │
              ▼
    ┌─────────────────────────────────┐
    │ COORDINATOR DECISION POINT #2   │
    │ "Is synthesis complete?"        │
    │ Uses: Reasoning NIM             │
    └──────┬──────────────────┬───────┘
           │                  │
       YES │                  │ NO
           │                  │
           ▼                  ▼
    ┌──────────┐      ┌──────────────┐
    │ Generate │      │ Refine       │
    │ Final    │      │ Synthesis    │
    │ Report   │      │ • Add depth  │
    │          │      │ • Fill gaps  │
    └────┬─────┘      └──────┬───────┘
         │                   │
         │                   └─────┐
         │                         │
         ▼                         │
    ┌────────────────────────┐    │
    │ REPORT GENERATION      │◄───┘
    │ • Format results       │
    │ • Add visualizations   │
    │ • Create summary       │
    └─────────┬──────────────┘
              │
              ▼
            DONE

KEY AGENTIC BEHAVIORS:
• ✅ Autonomous decisions (not just sequential)
• ✅ Self-evaluation and refinement
• ✅ Dynamic strategy adjustment
• ✅ Parallel execution where possible
• ✅ Quality-driven workflow control
```

---

## 8. Component Communication Matrix

```
                 Reasoning  Embedding  Vector   Orchestrator  Web
                    NIM       NIM       DB                    UI

Orchestrator        ✅        ✅        ✅         -          ❌

Web UI              ❌        ❌        ❌         ✅         -

Scout Agent         ❌        ✅        ✅         -          ❌

Analyst Agent       ✅        ❌        ❌         -          ❌

Synthesizer         ✅        ✅        ✅         -          ❌

Coordinator         ✅        ❌        ❌         -          ❌


Legend:
✅ = Direct communication
❌ = No direct communication
- = Self

Communication Pattern:
• All agents communicate through Orchestrator
• Only Orchestrator talks to NIMs directly
• Web UI only talks to Orchestrator
• Clean separation of concerns
```

---

These diagrams provide complete visual documentation of the system architecture, workflow, and deployment strategy for the Agentic Scholar hackathon submission.

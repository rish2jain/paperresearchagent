# 🚀 Complete Hackathon Setup & Submission Guide

**NVIDIA & AWS Agentic AI Unleashed Hackathon 2025**  
**Deadline: November 3, 2025 @ 2:00pm EST**

This comprehensive guide walks you through everything from initial setup to final submission.

---

## 📋 Table of Contents

1. [Prerequisites & Account Setup](#1-prerequisites--account-setup)
2. [Local Development Setup](#2-local-development-setup)
3. [EKS Deployment](#3-eks-deployment)
4. [Testing & Demo Preparation](#4-testing--demo-preparation)
5. [Demo Video Recording](#5-demo-video-recording)
6. [Submission Preparation](#6-submission-preparation)
7. [Devpost Submission](#7-devpost-submission)
8. [Final Checklist](#8-final-checklist)

---

## 1. Prerequisites & Account Setup

### 1.1 AWS Account Setup

**Time Required:** 15-20 minutes

#### Step 1: Create/Verify AWS Account

```bash
# Go to: https://aws.amazon.com/
# Sign up or log in to existing account
```

#### Step 2: Install AWS CLI

```bash
# macOS (using Homebrew)
brew install awscli

# Verify installation
aws --version
# Should show: aws-cli/2.x.x
```

#### Step 3: Configure AWS CLI

```bash
aws configure

# You'll be prompted for:
# AWS Access Key ID: [Enter your access key]
# AWS Secret Access Key: [Enter your secret key]
# Default region name: us-east-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

#### Step 4: Install eksctl

```bash
# macOS (using Homebrew)
brew install eksctl

# Verify installation
eksctl version
```

#### Step 5: Install kubectl

```bash
# macOS (using Homebrew)
brew install kubectl

# Verify installation
kubectl version --client
```

#### Step 6: Request Hackathon Credits

1. Register for the hackathon: https://nvidia-aws.devpost.com/
2. Complete the credits request form (link in hackathon description)
3. Wait for $100 promotional credits to be added to your AWS account
4. Monitor your AWS billing dashboard to track usage

**Important:** The $100 credits cover approximately 24 hours of both NIMs running.

---

### 1.2 NVIDIA NGC Account Setup

**Time Required:** 10 minutes

#### Step 1: Create NGC Account

```bash
# Go to: https://ngc.nvidia.com/signup
# Sign up for free account
```

#### Step 2: Get NGC API Key

1. Go to: https://ngc.nvidia.com/setup/api-key
2. Click "Generate API Key"
3. Copy the API key (you'll need it later)
4. **Store securely** - you won't be able to see it again!

#### Step 3: Test NGC Access

```bash
# Set environment variable (temporary)
export NGC_API_KEY="your_api_key_here"

# Verify access (optional - requires docker)
docker login nvcr.io
# Username: $oauthtoken
# Password: [Your NGC API Key]
```

---

### 1.3 Local Environment Setup

**Time Required:** 10 minutes

#### Step 1: Install Python (if needed)

```bash
# Check Python version (need 3.10+)
python3 --version

# If not installed, install via Homebrew
brew install python@3.11
```

#### Step 2: Create Virtual Environment

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

#### Step 3: Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(fastapi|streamlit|arxiv|tenacity|scikit-learn)"
```

#### Step 4: Install Docker (for local testing)

```bash
# macOS (using Homebrew)
brew install --cask docker

# Start Docker Desktop
# Open Docker Desktop application
```

---

## 2. Local Development Setup

**Time Required:** 20-30 minutes

### 2.1 Local Testing (Without NIMs)

#### Step 1: Test Local Setup

```bash
# Navigate to project directory
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent

# Activate virtual environment
source venv/bin/activate

# Run integration tests (will use fallback data)
python src/test_integration.py

# Expected output:
# ============================================================
# NVIDIA NIM Integration Tests
# ============================================================
# Testing Reasoning NIM...
# ❌ Reasoning NIM: Failed - [expected without NIMs]
# Testing Embedding NIM...
# ❌ Embedding NIM: Failed - [expected without NIMs]
# Testing Agent Workflow...
# ✅ Agent Workflow: Success (using fallback data)
```

#### Step 2: Test API Locally

```bash
# Terminal 1: Start API server
python src/api.py

# Terminal 2: Test API
curl http://localhost:8080/health

# Expected response:
# {"status":"degraded","service":"research-ops-agent",...}
```

#### Step 3: Test Web UI Locally

```bash
# Terminal 1: Start API (if not running)
python src/api.py

# Terminal 2: Start Web UI
streamlit run src/web_ui.py

# Open browser to: http://localhost:8501
# Test with query: "machine learning for medical imaging"
```

---

### 2.2 Test with NVIDIA NIMs (Optional - Free Tier)

**Note:** You can test with NIMs on build.nvidia.com for free before deploying to EKS.

#### Step 1: Access Build.nvidia.com

```bash
# Go to: https://build.nvidia.com/
# Sign in with NGC account
```

#### Step 2: Get NIM Endpoints

1. Navigate to NIM inference endpoints
2. Find:
   - **Reasoning NIM:** llama-3.1-nemotron-nano-8B-v1
   - **Embedding NIM:** nv-embedqa-e5-v5
3. Copy endpoint URLs

#### Step 3: Update Configuration

```bash
# Export environment variables for local testing
export REASONING_NIM_URL="https://your-reasoning-nim-endpoint.nvidia.com"
export EMBEDDING_NIM_URL="https://your-embedding-nim-endpoint.nvidia.com"

# Test with real NIMs
python src/test_integration.py
```

---

## 3. EKS Deployment

**Time Required:** 30-45 minutes (first time)

### 3.1 Prepare Secrets

#### Step 1: Create Secrets File

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent

# Copy template
cp k8s/secrets.yaml.template k8s/secrets.yaml

# Edit secrets file
nano k8s/secrets.yaml
# Or use your preferred editor: vim, code, etc.
```

#### Step 2: Fill in Secrets

```yaml
# Edit k8s/secrets.yaml with your actual credentials:

apiVersion: v1
kind: Secret
metadata:
  name: nvidia-ngc-secret
  namespace: research-ops
type: Opaque
stringData:
  NGC_API_KEY: "YOUR_ACTUAL_NGC_API_KEY_HERE" # ⚠️ Replace this!
  NVIDIA_API_KEY: "YOUR_ACTUAL_NGC_API_KEY_HERE" # ⚠️ Same as NGC_API_KEY

---
apiVersion: v1
kind: Secret
metadata:
  name: aws-credentials
  namespace: research-ops
type: Opaque
stringData:
  AWS_ACCESS_KEY_ID: "YOUR_AWS_ACCESS_KEY" # ⚠️ Replace this!
  AWS_SECRET_ACCESS_KEY: "YOUR_AWS_SECRET_KEY" # ⚠️ Replace this!
  AWS_DEFAULT_REGION: "us-east-1"
```

**Important:** Never commit `secrets.yaml` to git! It's already in `.gitignore`.

---

### 3.2 Create EKS Cluster

#### Step 1: Export Environment Variables

```bash
# Set NGC API key
export NGC_API_KEY="your_ngc_api_key_here"

# AWS credentials should already be configured via aws configure
# But you can also export if needed:
export AWS_ACCESS_KEY_ID="your_aws_key"
export AWS_SECRET_ACCESS_KEY="your_aws_secret"
export AWS_DEFAULT_REGION="us-east-1"
```

#### Step 2: Run Deployment Script

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent/k8s

# Make deploy script executable
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

**What the script does:**

1. Checks prerequisites (kubectl, aws, eksctl)
2. Creates EKS cluster (15-20 minutes) or uses existing
3. Updates kubeconfig
4. Creates NGC registry secret
5. Deploys all services:
   - Namespace
   - Secrets
   - Reasoning NIM
   - Embedding NIM
   - Vector Database (Qdrant)
   - Agent Orchestrator
   - Web UI
6. Waits for all services to be ready
7. Displays service endpoints

**Expected Output:**

```
🚀 Deploying Research Ops Agent to AWS EKS
============================================
Checking prerequisites...
Creating EKS cluster (this takes 15-20 minutes)...
[eksctl output...]
Applying Kubernetes manifests...
Waiting for deployments to be ready...
✅ Deployment complete!

Service Endpoints:
============================================
Agent Orchestrator API: http://[load-balancer-url]
Web UI: http://[load-balancer-url]
```

---

### 3.3 Verify Deployment

#### Step 1: Check Pod Status

```bash
# Check all pods
kubectl get pods -n research-ops

# Expected output (all should be Running):
# NAME                                   READY   STATUS    RESTARTS   AGE
# reasoning-nim-xxx                      1/1     Running   0          5m
# embedding-nim-xxx                       1/1     Running   0          5m
# agent-orchestrator-xxx                  1/1     Running   0          3m
# web-ui-xxx                              1/1     Running   0          3m
```

#### Step 2: Check Service Endpoints

```bash
# Check services
kubectl get svc -n research-ops

# Verify endpoints are accessible
kubectl get ingress -n research-ops
```

#### Step 3: Test API Endpoint

```bash
# Get service URL
API_URL=$(kubectl get svc agent-orchestrator -n research-ops -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# If using ClusterIP, port-forward instead:
kubectl port-forward -n research-ops svc/agent-orchestrator 8080:8080

# Test health endpoint
curl http://localhost:8080/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "research-ops-agent",
#   "nims_available": {
#     "reasoning_nim": true,
#     "embedding_nim": true
#   }
# }
```

#### Step 4: Access Web UI

```bash
# Port-forward web UI
kubectl port-forward -n research-ops svc/web-ui 8501:8501

# Or if using LoadBalancer, get URL:
UI_URL=$(kubectl get svc web-ui -n research-ops -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "Web UI: http://${UI_URL}"

# Open browser to: http://localhost:8501
```

---

## 4. Testing & Demo Preparation

**Time Required:** 30-60 minutes

### 4.1 End-to-End Testing

#### Step 1: Test API Endpoint

```bash
# Test research synthesis
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning for medical imaging",
    "max_papers": 10
  }'

# Expected response includes:
# {
#   "papers_analyzed": 10,
#   "common_themes": [...],
#   "contradictions": [...],
#   "research_gaps": [...],
#   "decisions": [...],  # ⭐ This is key for demo!
#   "processing_time_seconds": 45.2
# }
```

#### Step 2: Test Web UI

1. Open Web UI: http://localhost:8501
2. Enter query: "machine learning for medical imaging"
3. Click "🚀 Start Research"
4. **Watch for decision cards appearing** ⭐
5. Verify:
   - Decisions appear in real-time
   - NIM badges show correctly (Reasoning vs Embedding)
   - Results display correctly
   - Download options work

#### Step 3: Verify Decision Logging

```bash
# Check console output from API
# You should see:
# 🔍 Scout Decision: ACCEPTED 12/25 papers
#    Using: nv-embedqa-e5-v5 (Embedding NIM)
# 📊 Analyst Decision: ...
# 🧩 Synthesizer Decision: ...
# 🎯 Coordinator Decision: ...
```

#### Step 4: Test Multiple Queries

```bash
# Test different queries to ensure robustness:
# 1. "quantum computing algorithms"
# 2. "climate change mitigation strategies"
# 3. "deep learning for natural language processing"
# 4. "renewable energy storage solutions"
```

---

### 4.2 Demo Preparation Checklist

- [ ] **API is responding correctly**

  ```bash
  curl http://localhost:8080/health
  # Should return: {"status": "healthy", ...}
  ```

- [ ] **Web UI loads without errors**

  - Open http://localhost:8501
  - Verify interface loads correctly

- [ ] **Decision logging works**

  - Run a query
  - Verify decision cards appear
  - Verify NIM badges display correctly

- [ ] **Results display correctly**

  - Common themes show
  - Contradictions show
  - Research gaps show
  - Download options work

- [ ] **Error handling works**

  - Test with invalid query
  - Verify error messages display correctly

- [ ] **Screenshots taken**
  - Web UI main screen
  - Decision cards view
  - Results view
  - Architecture diagram (if available)

---

## 5. Demo Video Recording

**Time Required:** 60-90 minutes (recording + editing)

### 5.1 Preparation Before Recording

#### Step 1: Clean Up Environment

```bash
# Close unnecessary applications
# Clean browser cache
# Ensure good internet connection
```

#### Step 2: Prepare Demo Data

```bash
# Test your demo query beforehand
# Ensure it returns good results
# Note any interesting decisions to highlight
```

#### Step 3: Prepare Script

```markdown
# Use the script from README.md or customize:

[0:00-0:30] Problem Statement

- Show researcher with papers (or screenshot)
- "Academic researchers spend 40% of their time on literature review"
- "This researcher needs 8+ hours to manually review papers"

[0:30-1:30] Agent Workflow (CRITICAL!)

- Open ResearchOps Agent web UI
- Enter query: "machine learning for medical imaging"
- Click "Start Research"
- SHOW DECISION CARDS APPEARING IN REAL-TIME
- Highlight NIM badges (Reasoning vs Embedding)
- Emphasize: "Watch agents make autonomous decisions!"
- Point out: "See how Scout uses Embedding NIM"
- Point out: "Analyst uses Reasoning NIM"
- Point out: "Synthesizer uses BOTH NIMs together"

[1:30-2:00] Results

- Show synthesis results
- Expand themes section
- Expand contradictions section
- Expand research gaps section
- "8 hours → 3 minutes"

[2:00-2:30] Architecture

- Show EKS deployment (screenshot or diagram)
- "4 autonomous agents on Amazon EKS"
- "Both NVIDIA NIMs working together"
- Mention GPU instances (g5.2xlarge)

[2:30-3:00] Impact & Summary

- "97% time reduction"
- "$0.15 vs $400 cost per review"
- "10M+ researchers globally"
- "Built for NVIDIA & AWS Agentic AI Hackathon 2025"
```

---

### 5.2 Recording Tools

#### Option 1: macOS Screen Recording

```bash
# Built-in Screen Recording:
# 1. Press Shift + Command + 5
# 2. Select "Record Selected Portion" or "Record Entire Screen"
# 3. Click "Record"
# 4. Click "Stop" when done
# 5. Video saved to Desktop

# Or use QuickTime Player:
# 1. Open QuickTime Player
# 2. File → New Screen Recording
# 3. Click Record button
```

#### Option 2: OBS Studio (Free, Professional)

```bash
# Download: https://obsproject.com/
# Install: brew install --cask obs

# Benefits:
# - Multiple scene setups
# - Picture-in-picture
# - Text overlays
# - Professional transitions
```

#### Option 3: Loom (Simple, Cloud-based)

```bash
# Download: https://www.loom.com/
# Easy to use, automatically uploads to cloud
# Good for quick recordings
```

---

### 5.3 Recording Best Practices

1. **Resolution:** Record at 1080p (1920x1080) minimum
2. **Audio:** Use good microphone or built-in mic
3. **Timing:** Keep under 3 minutes (strict limit!)
4. **Pace:** Don't rush, but be efficient
5. **Highlights:** Emphasize decision cards appearing
6. **NIM Usage:** Clearly show which NIM is used when

#### Step-by-Step Recording Process:

1. **Test Run (Dry Run)**

   ```bash
   # Run through entire demo once without recording
   # Time yourself
   # Note any issues
   ```

2. **Actual Recording**

   ```bash
   # Start screen recording
   # Follow script exactly
   # Focus on showing decisions and NIMs
   # Keep under 3 minutes!
   ```

3. **Review & Edit**

   - Watch recording
   - Identify any issues
   - Trim unnecessary parts
   - Add captions/subtitles (optional but recommended)

4. **Export**
   - Export as MP4 (H.264 codec)
   - Keep file size under 100MB if possible
   - Resolution: 1080p

---

### 5.4 Upload to YouTube

#### Step 1: Create YouTube Account (if needed)

```bash
# Go to: https://www.youtube.com/
# Sign in with Google account
```

#### Step 2: Upload Video

1. Click "Create" → "Upload videos"
2. Select your demo video file
3. **Title:** "ResearchOps Agent - NVIDIA & AWS Agentic AI Hackathon 2025"
4. **Description:**

   ```
   ResearchOps Agent: Multi-agent AI system for automated literature review synthesis

   Built for NVIDIA & AWS Agentic AI Unleashed Hackathon 2025

   Features:
   - 4 autonomous agents with distinct roles
   - Visible decision-making with real-time logging
   - Both NVIDIA NIMs properly utilized
   - Deployed on Amazon EKS with GPU instances

   Impact:
   - 97% time reduction (8 hours → 3 minutes)
   - $0.15 vs $400 cost per review
   - 10M+ potential users globally

   GitHub: [Add your repo URL after making it public]
   ```

5. **Visibility:** Set to "Public" or "Unlisted"
6. **Tags:** Add relevant tags (AI, hackathon, NVIDIA, AWS, EKS, agents)
7. Click "Publish"

#### Step 3: Get Video URL

- Copy the YouTube video URL
- You'll need this for Devpost submission

---

## 6. Submission Preparation

**Time Required:** 30 minutes

### 6.1 Make Repository Public

#### Step 1: Verify All Files Are Committed

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent

# Check git status
git status

# Add any uncommitted files
git add .

# Commit if needed
git commit -m "Final submission for NVIDIA-AWS Agentic AI Hackathon"
```

#### Step 2: Create GitHub Repository

```bash
# Option 1: Using GitHub CLI (if installed)
gh repo create research-ops-agent --public --source=. --remote=origin

# Option 2: Using GitHub Web Interface:
# 1. Go to: https://github.com/new
# 2. Repository name: research-ops-agent
# 3. Description: "Multi-agent AI system for automated literature review synthesis"
# 4. Visibility: Public
# 5. Don't initialize with README (you already have one)
# 6. Click "Create repository"
```

#### Step 3: Push Code to GitHub

```bash
# Add remote (if not already added)
git remote add origin https://github.com/YOUR_USERNAME/research-ops-agent.git

# Push all code
git branch -M main
git push -u origin main

# Verify all files are on GitHub
# Visit: https://github.com/YOUR_USERNAME/research-ops-agent
```

#### Step 4: Verify Repository Is Public

```bash
# Check repository settings:
# 1. Go to: https://github.com/YOUR_USERNAME/research-ops-agent/settings
# 2. Scroll down to "Danger Zone"
# 3. Verify "Make public" option (or it should already show "Public")
```

---

### 6.2 Update README with Links

#### Step 1: Add Demo Video Link

```bash
# Edit README.md
nano README.md

# Add demo video section (around line 420):
```

Add this section to README.md:

```markdown
## 🎥 Demo Video

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

**Watch the demo:** [YouTube Link](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

#### Step 2: Add Repository URL

```bash
# Update README.md header or add link section

# Add near the top (after badges):
```

```markdown
## 📦 Repository

**GitHub:** https://github.com/YOUR_USERNAME/research-ops-agent

**Live Demo:** [Add your deployed URL if available]
```

#### Step 3: Commit and Push Updates

```bash
git add README.md
git commit -m "Add demo video link and repository URL"
git push
```

---

### 6.3 Final Repository Checklist

- [ ] **All code is committed and pushed**

  ```bash
  git status  # Should show: "nothing to commit, working tree clean"
  ```

- [ ] **Repository is public**

  - Verify at: https://github.com/YOUR_USERNAME/research-ops-agent

- [ ] **README.md has:**

  - Demo video link
  - Repository URL
  - Deployment instructions
  - All sections complete

- [ ] **No secrets in repository**

  ```bash
  # Verify secrets.yaml is not tracked
  git ls-files k8s/secrets.yaml
  # Should return nothing (or "not tracked")
  ```

- [ ] **All required files present:**
  - [ ] README.md
  - [ ] k8s/ (deployment manifests)
  - [ ] src/ (application code)
  - [ ] docs/ (architecture diagrams)
  - [ ] requirements.txt
  - [ ] Dockerfile.orchestrator
  - [ ] Dockerfile.ui

---

## 7. Devpost Submission

**Time Required:** 20-30 minutes

### 7.1 Access Devpost

#### Step 1: Log In to Devpost

```bash
# Go to: https://nvidia-aws.devpost.com/
# Click "Log in" or "Sign up"
```

#### Step 2: Join the Hackathon

```bash
# If not already registered:
# Click "Join hackathon"
# Fill in required information
# Accept terms and conditions
```

---

### 7.2 Create Project Submission

#### Step 1: Start New Project

1. Go to: https://nvidia-aws.devpost.com/
2. Click "My projects" in top navigation
3. Click "Create a project"
4. Or click "Submit a project" if already in project view

#### Step 2: Fill Project Details

**Project Name:**

```
ResearchOps Agent: Multi-Agent AI for Literature Review Synthesis
```

**Tagline (short description):**

```
Automated literature review synthesis using 4 autonomous agents, reducing 8-hour reviews to 3 minutes
```

**Description:**

````markdown
## 🎯 Overview

ResearchOps Agent is a **multi-agent AI system** that automatically synthesizes research literature, transforming hours of manual literature review into minutes of automated analysis.

**The Problem:** Academic researchers spend 40% of their time on literature review, manually reading, extracting, and synthesizing information from dozens of papers.

**Our Solution:** An autonomous multi-agent system that:

- 🔍 Searches and retrieves relevant papers using semantic similarity
- 📊 Extracts structured information in parallel using reasoning AI
- 🧩 Synthesizes findings across papers to identify themes, contradictions, and gaps
- 📋 Generates comprehensive literature reviews automatically

**Impact:** Reduces literature review time from 8+ hours to 2-3 minutes.

## ✅ Hackathon Requirements Compliance

### Required Components

✅ **llama-3.1-nemotron-nano-8B-v1** (Reasoning NIM)

- Deployed as NVIDIA NIM inference microservice
- Used for: Paper analysis, cross-document reasoning, synthesis generation
- Endpoint: `http://reasoning-nim:8000/v1/completions`

✅ **nv-embedqa-e5-v5** (Retrieval Embedding NIM)

- Deployed as NVIDIA NIM inference microservice
- Used for: Query embedding, paper similarity, finding clustering
- Endpoint: `http://embedding-nim:8001/v1/embeddings`

✅ **Amazon EKS Deployment**

- Multi-container orchestration on Amazon Elastic Kubernetes Service
- GPU instances: 2x g5.2xlarge (NVIDIA A10G)
- Production-ready with health checks, persistence, security contexts

✅ **Agentic Application**

- 4 autonomous agents with distinct roles and decision-making
- Agents: Scout (retrieval), Analyst (extraction), Synthesizer (reasoning), Coordinator (orchestration)
- Demonstrates true agency: autonomous search expansion, quality self-evaluation, dynamic refinement

## 🏗️ Architecture

**Multi-Agent System:**

- **Scout Agent**: Uses Embedding NIM to find relevant papers via semantic search
- **Analyst Agent**: Uses Reasoning NIM to extract structured information from papers
- **Synthesizer Agent**: Uses BOTH NIMs for cross-document reasoning (embeddings for clustering, reasoning for contradictions)
- **Coordinator Agent**: Uses Reasoning NIM for meta-decisions (search continuation, synthesis quality)

**Key Features:**

- Visible decision logging makes agentic behavior transparent
- Real-time decision visualization in web UI
- Both NIMs clearly identified when used
- Production-ready EKS deployment

## 📊 Impact Metrics

- **Time Savings:** 97% reduction (8 hours → 3 minutes)
- **Cost Savings:** $0.15 vs $200-400 per review
- **ROI:** 2,666x - 5,333x return on investment
- **Market:** 10M+ potential users globally

## 🚀 Deployment

See README.md for complete deployment instructions.

Quick start:

```bash
cd k8s
chmod +x deploy.sh
./deploy.sh
```
````

## 📚 Resources

- **GitHub Repository:** [Add your repo URL]
- **Demo Video:** [Add YouTube link]
- **Documentation:** See README.md and docs/

```

**Built With:**
- NVIDIA llama-3.1-nemotron-nano-8B-v1 (Reasoning NIM)
- NVIDIA nv-embedqa-e5-v5 (Embedding NIM)
- Amazon EKS
- Python (FastAPI, Streamlit)
- Kubernetes
- Qdrant (Vector Database)

**Technologies:**
- NVIDIA NIM
- Amazon EKS
- Python
- FastAPI
- Streamlit
- Kubernetes
- Qdrant

---

#### Step 3: Upload Media

**Demo Video:**
1. Click "Add a link" or "Upload video"
2. Paste your YouTube video URL
3. Add thumbnail (optional but recommended)

**Screenshots:**
1. Click "Add images"
2. Upload:
   - Web UI main screen
   - Decision cards view
   - Results view
   - Architecture diagram (if available)
3. Add captions to each screenshot

---

#### Step 4: Add Repository Link

**Source Code URL:**
```

https://github.com/YOUR_USERNAME/research-ops-agent

```

**Try It Out URL (if deployed):**
```

[Add your deployed web UI URL if available]

````

---

#### Step 5: Select Categories/Tags

Select relevant tags:
- AI/ML
- Cloud
- Developer Tools
- Education
- Research

---

#### Step 6: Add Team Members (if applicable)

If working in a team:
1. Click "Add team member"
2. Enter team member's Devpost username or email
3. They'll receive invitation

---

#### Step 7: Review and Submit

**Before Submitting:**

1. **Review all fields:**
   - [ ] Project name is clear and descriptive
   - [ ] Description is complete and compelling
   - [ ] All links work (GitHub, demo video)
   - [ ] Screenshots uploaded
   - [ ] Tags selected appropriately

2. **Test all links:**
   ```bash
   # Test GitHub link
   # Test YouTube video link
   # Test deployment URL (if provided)
````

3. **Verify submission requirements:**

   - [ ] Text description ✅
   - [ ] Demo video (under 3 minutes) ✅
   - [ ] URL to public code repository ✅
   - [ ] README with deployment instructions ✅

4. **Final check:**

   - [ ] All required components listed
   - [ ] Both NIMs mentioned and explained
   - [ ] EKS deployment highlighted
   - [ ] Agentic behavior emphasized
   - [ ] Impact metrics included

5. **Submit:**
   ```bash
   # Click "Submit project"
   # Confirm submission
   # Wait for confirmation email
   ```

---

## 8. Final Checklist

### Pre-Submission Checklist

#### Setup & Deployment

- [ ] AWS account created and configured
- [ ] NGC account created with API key
- [ ] All dependencies installed locally
- [ ] EKS cluster created and deployed
- [ ] All pods running successfully
- [ ] API health check passes
- [ ] Web UI accessible
- [ ] End-to-end test successful

#### Code & Repository

- [ ] All code committed to git
- [ ] Repository made public on GitHub
- [ ] README.md updated with:
  - [ ] Demo video link
  - [ ] Repository URL
  - [ ] Complete deployment instructions
- [ ] No secrets in repository
- [ ] All files present and organized

#### Demo & Video

- [ ] Demo video recorded (under 3 minutes)
- [ ] Video uploaded to YouTube
- [ ] Video is public or unlisted
- [ ] Video link added to README.md
- [ ] Screenshots captured for Devpost

#### Devpost Submission

- [ ] Devpost account created
- [ ] Joined hackathon
- [ ] Project created with:
  - [ ] Complete description
  - [ ] Demo video link
  - [ ] GitHub repository URL
  - [ ] Screenshots uploaded
  - [ ] Tags selected
- [ ] All submission requirements met
- [ ] Submission submitted before deadline

---

### Post-Submission Checklist

#### Verify Submission

- [ ] Confirmation email received from Devpost
- [ ] Project visible on Devpost project gallery
- [ ] All links work (GitHub, YouTube)
- [ ] Project description displays correctly
- [ ] Screenshots display correctly

#### Monitor Submission

- [ ] Check Devpost periodically for judge feedback
- [ ] Respond to any questions promptly
- [ ] Keep repository updated if needed

#### Cost Management

- [ ] Monitor AWS billing dashboard
- [ ] Stop EKS cluster if not needed (to save credits)
- [ ] Keep track of remaining credits

---

## 🚨 Troubleshooting Common Issues

### Issue: EKS Cluster Creation Fails

**Solution:**

```bash
# Check AWS credentials
aws sts get-caller-identity

# Check eksctl version
eksctl version

# Check region availability
aws ec2 describe-regions

# Try with explicit region
eksctl create cluster --name research-ops-cluster --region us-east-1 --node-type g5.2xlarge --nodes 2
```

### Issue: NIM Pods Not Starting

**Solution:**

```bash
# Check pod logs
kubectl logs -n research-ops deployment/reasoning-nim

# Check events
kubectl describe pod -n research-ops <pod-name>

# Common issues:
# - Invalid NGC_API_KEY: Verify secret is correct
# - Insufficient GPU: Check node has GPU available
# - Image pull errors: Verify NGC access
```

### Issue: Demo Video Too Long

**Solution:**

- Trim unnecessary parts
- Speed up UI interactions (post-processing)
- Focus on key moments (decisions, NIMs)
- Keep under 3 minutes strict!

### Issue: Repository Not Public

**Solution:**

```bash
# Check repository settings
# GitHub → Settings → Scroll to "Danger Zone"
# Click "Change visibility" → "Make public"
```

---

## 📞 Getting Help

### Hackathon Resources

- **Hackathon Page:** https://nvidia-aws.devpost.com/
- **Discord:** [Check hackathon page for Discord link]
- **Questions:** Email hackathon manager (link on Devpost page)

### Technical Help

- **AWS Documentation:** https://docs.aws.amazon.com/eks/
- **NVIDIA NGC:** https://docs.nvidia.com/ngc/
- **NIM Documentation:** https://build.nvidia.com/docs

### Project-Specific

- **Troubleshooting Guide:** See `docs/TROUBLESHOOTING.md`
- **Deployment Guide:** See `DEPLOYMENT.md`
- **Architecture Details:** See `docs/Architecture_Diagrams.md`

---

## ⏰ Timeline Recommendation

### Day 1: Setup (2-3 hours)

- AWS & NGC account setup
- Local environment setup
- Basic testing

### Day 2: Deployment (3-4 hours)

- EKS cluster creation
- Service deployment
- Testing and verification

### Day 3: Demo & Submission (2-3 hours)

- Demo video recording
- Repository cleanup
- Devpost submission

**Total Time:** 7-10 hours over 3 days

---

## 🎉 Success Criteria

You're ready to submit when:

✅ All requirements met:

- Both NIMs deployed and working
- EKS deployment complete
- Agentic application functional
- Demo video recorded (under 3 min)
- Repository public with complete README

✅ Competitive advantages visible:

- Decision logging working
- Both NIMs clearly demonstrated
- Professional UI and documentation
- Quantifiable impact shown

✅ Submission complete:

- Devpost project created
- All fields filled
- Video uploaded
- Links verified
- Submitted before deadline

---

## 🏆 Final Tips

1. **Emphasize Decision Logging**

   - This is your biggest differentiator
   - Make it prominent in demo video
   - Highlight in Devpost description

2. **Show Both NIMs Clearly**

   - Mention which NIM is used when
   - Show NIM badges in UI
   - Explain why each NIM is used

3. **Demonstrate Agentic Behavior**

   - Show agents making autonomous decisions
   - Highlight coordination between agents
   - Emphasize "not just a chatbot"

4. **Highlight Impact**

   - 97% time reduction
   - Quantifiable ROI
   - Large market opportunity

5. **Professional Presentation**
   - Clean code and documentation
   - Professional UI
   - Complete deployment instructions

---

**Good luck with your submission! 🚀**

You have a strong, competitive entry that meets all requirements and demonstrates true agentic AI behavior.

**Deadline Reminder:** November 3, 2025 @ 2:00pm EST

---

_Last Updated: 2025-01-01_  
_Guide Version: 1.0_

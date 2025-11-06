# Local Mac Studio Setup Guide

**Complete guide for running ResearchOps Agent locally on Mac Studio M3 Ultra**

---

## 🎯 Quick Start

### 1. Install Dependencies

**Option A: Using pip (Standard)**

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install local model dependencies
pip install llama-cpp-python[metal] sentence-transformers torch
```

**Option B: Using uv (Faster, Better Dependency Resolution)**

```bash
# Install uv if not installed
brew install uv

# Install all dependencies (handles conflicts better)
uv pip install -r requirements.txt --python venv/bin/python

# Install local model dependencies
uv pip install llama-cpp-python[metal] sentence-transformers torch
```

**Note:** `denario` requires Python 3.12+ and has been updated in `requirements.txt` with compatible dependency versions. If you're using Python 3.11 or earlier, denario will be automatically disabled.

### 2. Setup Local Models

**Important:** Make sure your virtual environment is activated before running the setup script:

```bash
# Activate virtual environment first
source venv/bin/activate

# Run setup script (it will auto-detect and use venv)
chmod +x scripts/setup_local_models.sh
./scripts/setup_local_models.sh
```

The script will:

- ✅ Auto-detect and activate virtual environment
- ✅ Install llama-cpp-python with Metal support
- ✅ Install sentence-transformers and torch
- ✅ Create models directory
- ✅ Create `.env.local` configuration file

### 3. Download Reasoning Model

**Option A: Using the download script (Recommended)**

**Important:** This model requires Hugging Face authentication.

```bash
# Make sure venv is activated
source venv/bin/activate

# Login to Hugging Face (required for this model)
huggingface-cli login
# Enter your token from https://huggingface.co/settings/tokens

# Run download script
chmod +x scripts/download_llama_model.sh
./scripts/download_llama_model.sh
```

**Get your Hugging Face token:**

1. Go to https://huggingface.co/settings/tokens
2. Create a new token (read access is sufficient)
3. Copy the token
4. Run `huggingface-cli login` and paste the token

**Option B: Using Python directly**

```bash
source venv/bin/activate
pip install huggingface_hub

python << EOF
from huggingface_hub import hf_hub_download
import os
import shutil

models_dir = os.path.expanduser("~/.local/share/models")
os.makedirs(models_dir, exist_ok=True)

# Download to cache, then copy
cached_path = hf_hub_download(
    repo_id="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
    filename="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
)

target_path = os.path.join(models_dir, "llama-3.1-8b-instruct-q4_K_M.gguf")
shutil.copy2(cached_path, target_path)
print(f"✅ Downloaded to: {target_path}")
EOF
```

**Option C: Manual download**

If the above methods fail, download manually from:

- https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main
- Look for `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`
- Save to `~/.local/share/models/llama-3.1-8b-instruct-q4_K_M.gguf`

**Model Details:**

- **Llama 3.1 8B Instruct (Q4_K_M quantized)**
- Size: ~5GB
- Repository: `bartowski/Meta-Llama-3.1-8B-Instruct-GGUF`
- Source file: `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`

### 4. Setup Qdrant (Vector Database)

```bash
# Run Qdrant setup script
chmod +x scripts/setup_qdrant_local.sh
./scripts/setup_qdrant_local.sh
```

Or manually:

```bash
docker run -d \
  --name qdrant-local \
  -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

### 5. Configure Environment

Create `.env` file or use `.env.local`:

```bash
# Enable local models
USE_LOCAL_MODELS=true

# Model paths (optional - defaults work)
REASONING_MODEL_PATH=~/.local/share/models/llama-3.1-8b-instruct-q4_K_M.gguf
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

# Qdrant
QDRANT_URL=http://localhost:6333

# Optional: Enable Denario
DENARIO_ENABLED=true
```

### 6. Run the Application

```bash
# Start API server
python -m src.api

# Or start Web UI
streamlit run src/web_ui.py
```

---

## 📋 Detailed Steps

### Step 1: Python Environment

**Python Version Requirements:**

- **Minimum:** Python 3.9+ (for core features)
- **Recommended:** Python 3.12+ (for Denario integration)

```bash
# Check Python version
python --version

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
# Option 1: Using pip (standard)
pip install -r requirements.txt

# Option 2: Using uv (faster, better dependency resolution)
brew install uv  # If not installed
uv pip install -r requirements.txt --python venv/bin/python
```

**Note:** If you encounter dependency resolution issues with pip, use `uv` instead. It handles complex dependency graphs much better.

### Step 2: Local Model Setup

**Option A: Using llama.cpp (Recommended)**

```bash
pip install llama-cpp-python[metal]
```

**Option B: Using MLX (Alternative)**

```bash
pip install mlx-lm
export REASONING_USE_MLX=true
```

**Embedding Model:**

```bash
pip install sentence-transformers torch
```

The embedding model will be downloaded automatically on first use.

### Step 3: Download Models

**Reasoning Model (Required):**

Download Llama 3.1 8B Instruct quantized model using one of these methods:

**Method 1: Using download script (Easiest)**

**Note:** Requires Hugging Face authentication.

```bash
source venv/bin/activate

# Login to Hugging Face first
huggingface-cli login
# Get token from: https://huggingface.co/settings/tokens

# Run download script
./scripts/download_llama_model.sh
```

**Method 2: Using Python**

**Note:** Requires Hugging Face authentication. See Method 1 above for the Python snippet (includes shutil import).

**Method 3: Manual download**

Visit https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main and download `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` manually. Save it as `llama-3.1-8b-instruct-q4_K_M.gguf` in `~/.local/share/models/`.

**Embedding Model (Auto-downloaded):**

The embedding model (`all-MiniLM-L6-v2`) will be downloaded automatically by sentence-transformers on first use (~80MB).

### Step 4: Qdrant Setup

**Using Docker:**

```bash
docker run -d \
  --name qdrant-local \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

**Verify Qdrant is running:**

```bash
curl http://localhost:6333/health
```

### Step 5: Configuration

**Environment Variables:**

Create `.env` file in project root:

```bash
# Local Models
USE_LOCAL_MODELS=true
REASONING_MODEL_PATH=~/.local/share/models/llama-3.1-8b-instruct-q4_K_M.gguf
REASONING_MODEL_N_CTX=4096
REASONING_MODEL_N_GPU_LAYERS=-1
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

# Qdrant
QDRANT_URL=http://localhost:6333

# Denario (optional - requires Python 3.12+)
DENARIO_ENABLED=true  # Set to false if using Python < 3.12

# API Keys (for paper sources)
SEMANTIC_SCHOLAR_API_KEY=your_key_here
IEEE_API_KEY=your_key_here  # Optional
ACM_API_KEY=your_key_here    # Optional
```

### Step 6: Run Application

**Start API Server:**

```bash
python -m src.api
```

API will be available at: `http://localhost:8080`

**Start Web UI:**

```bash
streamlit run src/web_ui.py
```

Web UI will be available at: `http://localhost:8501`

---

## 🧪 Testing

### Test Local Models

```python
# test_local_models.py
import asyncio
from src.local_models import LocalReasoningModel, LocalEmbeddingModel

async def test():
    # Test reasoning model
    reasoning = LocalReasoningModel()
    result = await reasoning.complete("Hello, world!")
    print(f"Reasoning: {result[:100]}...")

    # Test embedding model
    embedding = LocalEmbeddingModel()
    vec = await embedding.embed("test text")
    print(f"Embedding dim: {len(vec)}")

asyncio.run(test())
```

### Test Unified Clients

```python
# test_unified_clients.py
import asyncio
from src.unified_clients import UnifiedReasoningClient, UnifiedEmbeddingClient

async def test():
    async with UnifiedReasoningClient() as reasoning, \
             UnifiedEmbeddingClient() as embedding:

        # Test reasoning
        result = await reasoning.complete("What is machine learning?")
        print(f"Reasoning: {result[:100]}...")

        # Test embedding
        vec = await embedding.embed("machine learning")
        print(f"Embedding dim: {len(vec)}")

asyncio.run(test())
```

---

## 🔧 Troubleshooting

### Issue: Script fails with "externally-managed-environment"

**Solution:**

The script now automatically detects and activates the virtual environment. If you still see this error:

```bash
# Make sure venv exists
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Run script again
./scripts/setup_local_models.sh
```

### Issue: sentence-transformers import error

**Error:** `ImportError: cannot import name 'cached_download' from 'huggingface_hub'`

**Solution:**

This happens when sentence-transformers version is too old for the installed huggingface_hub. Update it:

```bash
source venv/bin/activate
pip install "sentence-transformers>=2.3.0" --upgrade
```

The setup script now automatically handles this compatibility issue.

### Issue: 401 Unauthorized when downloading model

**Error:** `401 Client Error: Unauthorized`

**Solution:**

This model requires Hugging Face authentication:

```bash
# Login to Hugging Face
huggingface-cli login

# Get your token from: https://huggingface.co/settings/tokens
# Create a token with "read" access, then paste it when prompted
```

After logging in, try downloading again.

### Issue: Model not found

**Solution:**

```bash
# Check model path
ls ~/.local/share/models/

# Update path in .env
REASONING_MODEL_PATH=/absolute/path/to/model.gguf
```

### Issue: Qdrant not accessible

**Solution:**

```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Check logs
docker logs qdrant-local

# Restart if needed
docker restart qdrant-local
```

### Issue: Out of memory

**Solution:**

- Use smaller quantized model (Q3_K_M instead of Q4_K_M)
- Reduce context window: `REASONING_MODEL_N_CTX=2048`
- Use CPU instead of GPU: `REASONING_MODEL_N_GPU_LAYERS=0`

---

## 📊 Performance Tuning

### Optimize for Speed

```bash
# Use more GPU layers
REASONING_MODEL_N_GPU_LAYERS=-1

# Use Metal backend (automatic on Mac)
# Already enabled with llama-cpp-python[metal]
```

### Optimize for Memory

```bash
# Use smaller context
REASONING_MODEL_N_CTX=2048

# Use CPU for some layers
REASONING_MODEL_N_GPU_LAYERS=20  # Use 20 GPU layers, rest on CPU
```

### Model Selection

| Model  | Size | Speed  | Quality |
| ------ | ---- | ------ | ------- |
| Q4_K_M | 5GB  | Fast   | Good    |
| Q3_K_M | 4GB  | Faster | Good    |
| Q5_K_M | 6GB  | Medium | Better  |
| Q8_0   | 8GB  | Slow   | Best    |

---

## 🎯 Denario Integration

### Prerequisites

Denario requires **Python 3.12+**. Check your Python version:

```bash
python --version  # Should be 3.12.x or higher
```

### Enable Denario

**If using Python 3.12+:**

Denario is already included in `requirements.txt` with compatible dependency versions. The dependencies have been updated to work with Denario:

- `scikit-learn>=1.4.0` (was 1.3.2)
- `plotly>=5.21.0` (was 5.18.0)
- `pandas>=2.2.0` (was 2.1.4)
- `scipy>=1.12.0` (was 1.11.4)
- `pydantic>=2.7.4` (was 2.5.0)
- `aiohttp>=3.10.0` (was 3.9.1)

**Installation:**

```bash
# Using uv (recommended - handles dependencies better)
uv pip install -r requirements.txt --python venv/bin/python

# Or using pip (may take longer due to dependency resolution)
pip install -r requirements.txt
```

**Enable in .env:**

```bash
echo "DENARIO_ENABLED=true" >> .env
```

### Verify Denario Installation

```bash
source venv/bin/activate
python -c "
import denario
print('✅ Denario version:', denario.__version__)

from src.denario_integration import DenarioIntegration
d = DenarioIntegration(enabled=True)
print('✅ Denario available:', d.is_available())
"
```

### Use Denario Features

When `DENARIO_ENABLED=true`, Denario will automatically:

- Generate research ideas from synthesis gaps and contradictions
- Enhance synthesis results with AI-generated research questions
- Provide methodology suggestions for research ideas
- Generate LaTeX paper structures in various journal formats (APS, Nature, IEEE)

### Troubleshooting Denario

**Issue: Dependency resolution errors**

If pip gets stuck resolving dependencies:

```bash
# Use uv instead (much faster)
brew install uv
uv pip install -r requirements.txt --python venv/bin/python
```

**Issue: Import errors**

If you see import errors, try:

```bash
# Reinstall httpx-aiohttp
pip install httpx-aiohttp==0.1.9 --force-reinstall

# Fix anyio version conflict
pip install "anyio<4.0.0,>=3.7.1"
```

**Issue: Python version too old**

If you're on Python 3.11 or earlier:

```bash
# Upgrade to Python 3.12 using pyenv
pyenv install 3.12.12
pyenv local 3.12.12

# Or use Homebrew
brew install python@3.12
```

---

## 📚 Next Steps

1. **Test the system**: Run a sample research query
2. **Monitor performance**: Check token generation speed
3. **Optimize settings**: Adjust model parameters as needed
4. **Enable Denario**: Add research idea generation

---

## ✅ Verification Checklist

- [ ] Python 3.12+ installed (for Denario) or 3.9+ (for core features)
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed (using pip or uv)
- [ ] llama-cpp-python[metal] installed
- [ ] sentence-transformers installed
- [ ] Reasoning model downloaded
- [ ] Qdrant running locally
- [ ] `.env` configured
- [ ] Denario installed and verified (if using Python 3.12+)
- [ ] API server starts successfully
- [ ] Web UI accessible
- [ ] Test query completes

---

## 📝 Recent Updates (2025-01-16)

### Dependency Updates for Denario Compatibility

The following dependencies were updated to support Denario integration:

- `aiohttp`: `3.9.1` → `>=3.10.0`
- `pydantic`: `2.5.0` → `>=2.7.4`
- `scikit-learn`: `1.3.2` → `>=1.4.0`
- `plotly`: `5.18.0` → `>=5.21.0`
- `pandas`: `2.1.4` → `>=2.2.0`
- `scipy`: `1.11.4` → `>=1.12.0`

These updates are backward compatible and improve overall system stability.

### Installation Improvements

- Added support for `uv` package manager (faster dependency resolution)
- Updated Denario activation process
- Fixed dependency conflicts

---

**Status:** ✅ Ready for Local Execution with Denario Support

---

## 📚 Additional Resources

- **[DENARIO_ACTIVATION_GUIDE.md](DENARIO_ACTIVATION_GUIDE.md)** - Complete Denario activation guide
- **[DEPENDENCY_INSTALL_FIX.md](DEPENDENCY_INSTALL_FIX.md)** - Troubleshooting dependency issues
- **[DENARIO_ACTIVATION_SUCCESS.md](DENARIO_ACTIVATION_SUCCESS.md)** - Denario activation summary

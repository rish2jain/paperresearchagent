#!/bin/bash
# Setup script for local models on Mac Studio
# Downloads models and sets up local environment

set -e

echo "=========================================="
echo "🚀 Local Model Setup for Mac Studio"
echo "=========================================="
echo ""

# Check for virtual environment
if [ -d "venv" ]; then
    echo "✅ Virtual environment found"
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    PYTHON_CMD="python"
    PIP_CMD="pip"
elif [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment already activated"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "⚠️  No virtual environment found!"
    echo ""
    echo "Please create and activate a virtual environment first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Verify we're using venv Python
VENV_PYTHON=$(which python)
if [[ "$VENV_PYTHON" != *"venv"* ]] && [[ "$VENV_PYTHON" != *".venv"* ]]; then
    echo "⚠️  Warning: Not using virtual environment Python"
    echo "   Current Python: $VENV_PYTHON"
    echo "   Please activate venv: source venv/bin/activate"
    exit 1
fi

echo "✅ Using Python: $VENV_PYTHON"
echo ""

# Create models directory
MODELS_DIR="$HOME/.local/share/models"
mkdir -p "$MODELS_DIR"

echo "📁 Models directory: $MODELS_DIR"
echo ""

# Check if llama.cpp is installed
if ! $PYTHON_CMD -c "import llama_cpp" 2>/dev/null; then
    echo "⚠️  llama-cpp-python not installed"
    echo "📦 Installing llama-cpp-python with Metal support..."
    $PIP_CMD install llama-cpp-python[metal]
    echo "✅ llama-cpp-python installed"
else
    echo "✅ llama-cpp-python already installed"
fi

# Check if sentence-transformers is installed
if ! $PYTHON_CMD -c "import sentence_transformers" 2>/dev/null; then
    echo "⚠️  sentence-transformers not installed"
    echo "📦 Installing sentence-transformers..."
    $PIP_CMD install "sentence-transformers>=2.3.0" torch
    echo "✅ sentence-transformers installed"
else
    # Ensure packaging is installed for version checking
    if ! $PYTHON_CMD -c "import packaging" 2>/dev/null; then
        echo "📦 Installing packaging for version checks..."
        $PIP_CMD install packaging
    fi
    
    # Check version compatibility
    VERSION_CHECK=$($PYTHON_CMD -c "
try:
    import sentence_transformers
    from packaging import version
    current_version = sentence_transformers.__version__
    required_version = '2.3.0'
    if version.parse(current_version) >= version.parse(required_version):
        print('OK')
    else:
        print('UPGRADE')
except Exception as e:
    print('ERROR')
" 2>/dev/null)
    
    if [ "$VERSION_CHECK" = "OK" ]; then
        echo "✅ sentence-transformers already installed (version >= 2.3.0)"
    elif [ "$VERSION_CHECK" = "UPGRADE" ]; then
        echo "⚠️  sentence-transformers version incompatible, upgrading..."
        $PIP_CMD install "sentence-transformers>=2.3.0" --upgrade
        echo "✅ sentence-transformers upgraded"
    else
        echo "⚠️  Error checking version, attempting upgrade..."
        $PIP_CMD install "sentence-transformers>=2.3.0" --upgrade
        echo "✅ sentence-transformers upgraded"
    fi
fi

# Check for reasoning model
REASONING_MODEL="$MODELS_DIR/llama-3.1-8b-instruct-q4_K_M.gguf"
if [ ! -f "$REASONING_MODEL" ]; then
    echo ""
    echo "📥 Reasoning model not found"
    echo "   Expected: $REASONING_MODEL"
    echo ""
    echo "⚠️  IMPORTANT: This model requires Hugging Face authentication!"
    echo ""
    echo "Download options:"
    echo ""
    echo "Option 1: Using download script (Recommended)"
    echo "  huggingface-cli login  # Get token from https://huggingface.co/settings/tokens"
    echo "  ./scripts/download_llama_model.sh"
    echo ""
    echo "Option 2: Using huggingface-cli"
    echo "  huggingface-cli login"
    echo "  huggingface-cli download bartowski/Meta-Llama-3.1-8B-Instruct-GGUF \\"
    echo "    Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf \\"
    echo "    --local-dir $MODELS_DIR"
    echo ""
    echo "Option 3: Manual download"
    echo "  Visit: https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/tree/main"
    echo "  Download: Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    echo "  Save to: $MODELS_DIR/llama-3.1-8b-instruct-q4_K_M.gguf"
    echo ""
else
    echo "✅ Reasoning model found: $REASONING_MODEL"
fi

# Check for embedding model (will be downloaded automatically by sentence-transformers)
echo ""
echo "✅ Embedding model will be downloaded automatically on first use"
echo "   Model: all-MiniLM-L6-v2"
echo ""

# Create .env file with local settings
ENV_FILE=".env.local"
if [ ! -f "$ENV_FILE" ]; then
    echo "📝 Creating $ENV_FILE..."
    cat > "$ENV_FILE" << EOF
# Local Model Configuration
USE_LOCAL_MODELS=true
REASONING_MODEL_PATH=$REASONING_MODEL
REASONING_MODEL_N_CTX=4096
REASONING_MODEL_N_GPU_LAYERS=-1
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

# Qdrant Configuration
QDRANT_URL=http://localhost:6333

# Optional: Enable Denario (requires Python 3.12+)
# DENARIO_ENABLED=true
EOF
    echo "✅ Created $ENV_FILE"
else
    echo "✅ $ENV_FILE already exists"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Download the reasoning model (see above)"
echo "2. Start Qdrant: docker run -d --name qdrant-local -p 6333:6333 qdrant/qdrant"
echo "3. Set environment: export USE_LOCAL_MODELS=true"
echo "4. Run: python -m src.api"
echo ""


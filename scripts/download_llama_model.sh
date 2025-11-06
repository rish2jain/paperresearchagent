#!/bin/bash
# Download Llama model using huggingface_hub
# This script handles authentication and downloads the model correctly

set -e

MODELS_DIR="$HOME/.local/share/models"
mkdir -p "$MODELS_DIR"

MODEL_FILE="llama-3.1-8b-instruct-q4_K_M.gguf"
REASONING_MODEL="$MODELS_DIR/$MODEL_FILE"

# Repository and file configuration
REPO_ID="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"
# Try different possible filenames
POSSIBLE_FILES=(
    "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    "Meta-Llama-3.1-8B-Instruct-Q4_K_M-00001-of-00001.gguf"
    "llama-3.1-8b-instruct-q4_K_M.gguf"
)

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ] && [ ! -d "venv" ]; then
    echo "⚠️  Please activate virtual environment first:"
    echo "   source venv/bin/activate"
    exit 1
fi

# Activate venv if exists but not activated
if [ -d "venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    source venv/bin/activate
fi

echo "📥 Downloading Llama 3.1 8B Instruct model..."
echo "   Repository: $REPO_ID"
echo "   File: $MODEL_FILE"
echo "   Destination: $REASONING_MODEL"
echo ""

# Check if huggingface_hub is installed
if ! python -c "import huggingface_hub" 2>/dev/null; then
    echo "📦 Installing huggingface_hub..."
    pip install huggingface_hub
fi

# Check if user is authenticated
echo "🔐 Checking Hugging Face authentication..."
if ! python -c "from huggingface_hub import whoami; whoami()" 2>/dev/null; then
    echo ""
    echo "⚠️  Not authenticated with Hugging Face"
    echo ""
    echo "This model requires authentication. Please login:"
    echo "   huggingface-cli login"
    echo ""
    echo "Or set your token:"
    echo "   export HF_TOKEN=your_token_here"
    echo ""
    read -p "Do you want to login now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        huggingface-cli login
    else
        echo "Please authenticate and run this script again."
        exit 1
    fi
fi

# Download using Python (handles authentication automatically)
# First try downloading to cache, then copy to models directory
python << EOF
from huggingface_hub import hf_hub_download
import os
import shutil

models_dir = os.path.expanduser("$MODELS_DIR")
os.makedirs(models_dir, exist_ok=True)

# Correct repository and filename
repo_id = "$REPO_ID"
source_filename = "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
target_filename = "$MODEL_FILE"
target_path = os.path.join(models_dir, target_filename)

print("Downloading model (this may take a while, ~5GB)...")
print(f"   Repository: {repo_id}")
print(f"   Source file: {source_filename}")
print(f"   Target file: {target_filename}")
print("")

try:
    # Download to cache first (handles authentication better)
    cached_path = hf_hub_download(
        repo_id=repo_id,
        filename=source_filename
    )
    
    # Copy to models directory with desired filename
    if os.path.exists(cached_path):
        print(f"Copying from cache to models directory...")
        shutil.copy2(cached_path, target_path)
        print(f"✅ Model downloaded successfully!")
        print(f"   Cache location: {cached_path}")
        print(f"   Models location: {target_path}")
    else:
        print(f"❌ Cached file not found at: {cached_path}")
        exit(1)
        
except Exception as e:
    print(f"❌ Download failed: {e}")
    print("")
    print("Troubleshooting:")
    print("1. Check your internet connection")
    print("2. Try authenticating with Hugging Face:")
    print("   huggingface-cli login")
    print("3. Or download manually from:")
    print(f"   https://huggingface.co/{repo_id}/tree/main")
    print(f"   Look for: {source_filename}")
    exit(1)
EOF

# Verify download
if [ -f "$REASONING_MODEL" ]; then
    SIZE=$(du -h "$REASONING_MODEL" | cut -f1)
    FILE_SIZE=$(stat -f%z "$REASONING_MODEL" 2>/dev/null || stat -c%s "$REASONING_MODEL" 2>/dev/null)
    
    if [ "$FILE_SIZE" -gt 1000000 ]; then  # At least 1MB
        echo ""
        echo "✅ Model verified!"
        echo "   Size: $SIZE"
        echo "   Path: $REASONING_MODEL"
    else
        echo ""
        echo "⚠️  Warning: Model file is too small ($SIZE)"
        echo "   The download may have failed. Please try again or download manually."
        rm -f "$REASONING_MODEL"  # Remove invalid file
    fi
else
    echo ""
    echo "⚠️  Model file not found at expected location"
    echo "   Check the download output above"
fi


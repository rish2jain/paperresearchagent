#!/bin/bash
# Alternative: Install denario with pip-tools or uv for better resolution

set -e

echo "🔧 Installing dependencies with better resolver..."
echo ""

# Check if uv is available (faster, better resolver)
if command -v uv &> /dev/null; then
    echo "✅ Using uv (fast Python package installer)..."
    uv pip install -r requirements.txt
    echo "✅ Dependencies installed with uv"
    exit 0
fi

# Check if pip-tools is available
if ! command -v pip-compile &> /dev/null; then
    echo "📦 Installing pip-tools..."
    pip install pip-tools
    echo "✅ pip-tools installed"
else
    echo "✅ pip-tools already available"
fi

# Always run pip-compile and pip-sync
echo "🔧 Compiling requirements..."
pip-compile requirements.txt

echo "🔧 Syncing dependencies..."
pip-sync requirements.txt

echo "✅ Dependencies installed with pip-tools"
exit 0


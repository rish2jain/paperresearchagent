#!/bin/bash
# Faster Denario Activation using Homebrew Python
# This uses pre-built binaries instead of compiling from source

set -e

echo "🚀 Fast Denario Activation (using Homebrew)"
echo ""

# Check if Homebrew Python 3.12 is installed
if ! brew list python@3.12 &>/dev/null; then
    echo "📦 Installing Python 3.12 via Homebrew (pre-built, much faster)..."
    brew install python@3.12
else
    echo "✅ Python 3.12 already installed via Homebrew"
fi

# Get the path to Homebrew Python
BREW_PYTHON=$(brew --prefix python@3.12)/bin/python3.12
BREW_PYTHON_VERSION=$($BREW_PYTHON --version 2>&1 | awk '{print $2}')

echo "✅ Found Python: $BREW_PYTHON_VERSION at $BREW_PYTHON"

# Create pyenv version symlink (if pyenv is being used)
if command -v pyenv &> /dev/null; then
    PYENV_VERSIONS_DIR="$HOME/.pyenv/versions/3.12.11"
    if [ ! -d "$PYENV_VERSIONS_DIR" ]; then
        echo "🔗 Creating pyenv symlink to Homebrew Python..."
        mkdir -p "$PYENV_VERSIONS_DIR/bin"
        ln -sf "$BREW_PYTHON" "$PYENV_VERSIONS_DIR/bin/python"
        ln -sf "$BREW_PYTHON" "$PYENV_VERSIONS_DIR/bin/python3"
        ln -sf "$BREW_PYTHON" "$PYENV_VERSIONS_DIR/bin/python3.12"
        
        # Create pip symlinks
        BREW_PIP=$(brew --prefix python@3.12)/bin/pip3.12
        if [ -f "$BREW_PIP" ]; then
            ln -sf "$BREW_PIP" "$PYENV_VERSIONS_DIR/bin/pip"
            ln -sf "$BREW_PIP" "$PYENV_VERSIONS_DIR/bin/pip3"
        fi
        
        echo "✅ pyenv symlink created"
    fi
    
    # Set local version
    echo "🔀 Setting Python 3.12.11 for this project..."
    pyenv local 3.12.11
else
    echo "⚠️  pyenv not found, using Homebrew Python directly"
    echo "   You can use: $BREW_PYTHON directly"
fi

# Verify Python version
CURRENT_PYTHON=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Current Python: $CURRENT_PYTHON"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo ""
    echo "⚠️  Virtual environment exists. Recreating with Python 3.12..."
    rm -rf venv
fi

# Create new virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Verify venv Python version
VENV_PYTHON=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Virtual environment Python: $VENV_PYTHON"

# Uncomment denario in requirements.txt
echo ""
echo "📝 Updating requirements.txt..."
if grep -q "^# denario\[app\]" requirements.txt; then
    cp requirements.txt requirements.txt.bak
    
    # Detect OS for sed compatibility
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed requires empty string after -i
        sed -i '' 's/^# denario\[app\]/denario[app]/' requirements.txt
    else
        # Linux/GNU sed
        sed -i 's/^# denario\[app\]/denario[app]/' requirements.txt
    fi
    
    # Remove backup file
    rm -f requirements.txt.bak
    echo "✅ Uncommented denario in requirements.txt"
else
    echo "ℹ️  denario already uncommented"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies (using staged approach to avoid conflicts)..."
pip install --upgrade pip

# Install in stages to avoid dependency resolution issues
echo "Installing core dependencies first..."
grep -v "denario" requirements.txt > /tmp/requirements_core.txt
pip install -r /tmp/requirements_core.txt
rm -f /tmp/requirements_core.txt

echo "Installing Denario separately..."
pip install denario[app]>=1.0.0 --use-deprecated=legacy-resolver 2>/dev/null || \
pip install denario[app]>=1.0.0

# Set environment variable
echo ""
echo "🔧 Setting DENARIO_ENABLED=true..."
if [ -f .env ]; then
    # Use temp file approach to avoid .bak files
    TEMP_ENV=$(mktemp .env.XXXXXX) || {
        echo "Failed to create temporary file"
        exit 1
    }
    grep -v '^DENARIO_ENABLED=' .env > "$TEMP_ENV" 2>/dev/null || true
    mv "$TEMP_ENV" .env
fi
echo "DENARIO_ENABLED=true" >> .env
export DENARIO_ENABLED=true

echo ""
echo "✅ Denario activation complete!"
echo ""
echo "Verification:"
python -c "
try:
    from denario import Denario
    print('✅ Denario package installed')
except ImportError as e:
    print('❌ Denario package not found:', e)

try:
    from src.denario_integration import DenarioIntegration
    denario = DenarioIntegration(enabled=True)
    print('✅ Denario integration available:', denario.is_available())
except Exception as e:
    print('⚠️  Error checking integration:', e)
"

echo ""
echo "📋 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Restart API server: uvicorn src.api:app --reload"
echo "   3. Restart Web UI: streamlit run src.web_ui.py"
echo ""
echo "💡 To disable Denario, set DENARIO_ENABLED=false in .env"


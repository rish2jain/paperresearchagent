#!/bin/bash
# Denario Activation Script
# Activates Denario integration by upgrading to Python 3.12+ and installing dependencies

set -e

echo "🔧 Activating Denario Integration..."
echo ""

# Check current Python version
CURRENT_PYTHON=$(python --version 2>&1 | awk '{print $2}')
echo "Current Python version: $CURRENT_PYTHON"

# Check if Python 3.12+ is needed
# Extract major and minor version numbers (handle patch/pre-release versions)
PYTHON_VERSION_STR=$(python --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION_STR" | sed 's/^\([0-9]*\)\..*/\1/')
PYTHON_MINOR=$(echo "$PYTHON_VERSION_STR" | sed 's/^[0-9]*\.\([0-9]*\).*/\1/')

# Fallback to 0 if extraction fails
PYTHON_MAJOR=${PYTHON_MAJOR:-0}
PYTHON_MINOR=${PYTHON_MINOR:-0}

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]); then
    echo "⚠️  Python 3.12+ required for Denario (current: $CURRENT_PYTHON)"
    echo ""
    
    # Check if pyenv is available
    if command -v pyenv &> /dev/null; then
        echo "📦 Installing Python 3.12.11 with pyenv..."
        pyenv install 3.12.11 --skip-existing
        
        echo "🔀 Setting Python 3.12.11 for this project..."
        pyenv local 3.12.11
        
        echo "✅ Python upgraded to: $(python --version)"
        echo ""
        echo "⚠️  IMPORTANT: You may need to recreate your virtual environment!"
        echo "   Run: rm -rf venv && python -m venv venv && source venv/bin/activate"
        echo ""
    else
        echo "❌ pyenv not found. Please install Python 3.12+ manually."
        echo "   Options:"
        echo "   1. Install pyenv: brew install pyenv"
        echo "   2. Install Python 3.12: brew install python@3.12"
        exit 1
    fi
else
    echo "✅ Python version is compatible ($CURRENT_PYTHON)"
fi

# Uncomment denario in requirements.txt
echo "📝 Updating requirements.txt..."
if grep -q "^# denario\[app\]" requirements.txt; then
    # Backup requirements.txt
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
    echo "ℹ️  denario already uncommented in requirements.txt"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Set environment variable
echo ""
echo "🔧 Setting DENARIO_ENABLED=true..."
if [ -f .env ]; then
    # Detect OS for sed compatibility
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed requires empty string after -i
        sed -i '' '/^DENARIO_ENABLED=/d' .env
    else
        # Linux/GNU sed
        sed -i '/^DENARIO_ENABLED=/d' .env
    fi
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
except ImportError:
    print('❌ Denario package not found')

from src.denario_integration import DenarioIntegration
denario = DenarioIntegration(enabled=True)
print('✅ Denario integration available:', denario.is_available())
"

echo ""
echo "📋 Next steps:"
echo "   1. Restart your API server: uvicorn src.api:app --reload"
echo "   2. Restart your Web UI: streamlit run src/web_ui.py"
echo "   3. Denario features will be automatically enabled!"
echo ""
echo "💡 To disable Denario, set DENARIO_ENABLED=false in .env"


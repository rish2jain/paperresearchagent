#!/bin/bash
# Install dependencies using uv with existing venv

set -e

echo "🚀 Installing dependencies with uv..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python -m venv venv
fi

# Activate venv
source venv/bin/activate

# Use uv to install into the venv
echo "📦 Installing dependencies with uv (fast resolver)..."
uv pip install -r requirements.txt --python venv/bin/python

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "Verification:"
python -c "
try:
    import denario
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


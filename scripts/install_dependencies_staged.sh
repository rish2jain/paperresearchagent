#!/bin/bash
# Install dependencies in stages to avoid resolution conflicts
# This installs core dependencies first, then denario separately

set -e

echo "📦 Installing dependencies in stages to avoid conflicts..."
echo ""

# Stage 1: Core dependencies (without denario)
echo "Stage 1: Installing core dependencies..."
pip install --upgrade pip

# Create a temporary requirements file without denario
grep -v "denario" requirements.txt > /tmp/requirements_core.txt

# Install core dependencies
pip install -r /tmp/requirements_core.txt

echo ""
echo "✅ Core dependencies installed"
echo ""

# Stage 2: Install denario separately with more lenient resolution
echo "Stage 2: Installing Denario..."
echo "This may take a few minutes due to complex dependencies..."

# Try installing denario with legacy resolver first (faster, less strict)
pip install denario[app]>=1.0.0 --use-deprecated=legacy-resolver || \
pip install denario[app]>=1.0.0 --no-deps && pip install denario[app]>=1.0.0

echo ""
echo "✅ Denario installed"
echo ""

# Cleanup
rm -f /tmp/requirements_core.txt

echo "✅ All dependencies installed successfully!"
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


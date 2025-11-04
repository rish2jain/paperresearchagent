#!/bin/bash
# Verification script for Docker PYTHONPATH fix
# Tests that the ModuleNotFoundError: No module named 'utils' is resolved

set -e

echo "🔍 Verifying Docker PYTHONPATH fix..."
echo ""

# Test 1: Verify Dockerfile.ui has PYTHONPATH
echo "✓ Test 1: Checking Dockerfile.ui..."
if grep -q "ENV PYTHONPATH=/app:\$PYTHONPATH" Dockerfile.ui; then
    echo "  ✅ PYTHONPATH set correctly in Dockerfile.ui"
else
    echo "  ❌ PYTHONPATH missing in Dockerfile.ui"
    exit 1
fi

# Test 2: Verify Dockerfile.orchestrator has PYTHONPATH
echo "✓ Test 2: Checking Dockerfile.orchestrator..."
if grep -q "ENV PYTHONPATH=/app:\$PYTHONPATH" Dockerfile.orchestrator; then
    echo "  ✅ PYTHONPATH set correctly in Dockerfile.orchestrator"
else
    echo "  ❌ PYTHONPATH missing in Dockerfile.orchestrator"
    exit 1
fi

# Test 3: Verify utils directory exists
echo "✓ Test 3: Checking utils directory structure..."
if [ -d "src/utils" ] && [ -f "src/utils/session_manager.py" ]; then
    echo "  ✅ utils directory and session_manager.py exist"
else
    echo "  ❌ utils directory structure missing"
    exit 1
fi

# Test 4: Verify import works with PYTHONPATH set
echo "✓ Test 4: Testing Python import simulation..."
export PYTHONPATH=src:$PYTHONPATH
if python3 -c "from utils.session_manager import SessionManager; print('Import successful')" 2>/dev/null; then
    echo "  ✅ Import works with PYTHONPATH set (Docker environment simulated)"
else
    echo "  ❌ Import failed even with PYTHONPATH"
    exit 1
fi

echo ""
echo "🎉 All verification tests passed!"
echo ""
echo "📋 Next Steps:"
echo "  1. Build Docker image: docker build -f Dockerfile.ui -t research-ops/ui:latest ."
echo "  2. Test locally: docker run -p 8501:8501 research-ops/ui:latest"
echo "  3. Deploy to EKS: cd k8s && ./deploy.sh"
echo ""
echo "✅ Fix is ready for deployment!"

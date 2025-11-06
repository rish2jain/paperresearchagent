# Quick Fix: Install Dependencies in Stages

The pip dependency resolver is hitting conflicts. Here's the solution:

## Quick Manual Fix (Run Now)

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Stage 1: Install core dependencies (without denario)
pip install --upgrade pip

# Create secure temporary file
TEMP_REQ=$(mktemp /tmp/req_core.XXXXXX.txt) || {
    echo "Failed to create temporary file"
    exit 1
}
trap "rm -f '$TEMP_REQ'" EXIT INT TERM

grep -v "denario" requirements.txt > "$TEMP_REQ"
pip install -r "$TEMP_REQ"

# Stage 2: Install denario separately (with legacy resolver to avoid conflicts)
pip install denario[app]>=1.0.0 --use-deprecated=legacy-resolver

# Cleanup handled by trap

# Verify
python -c "import denario; print('✅ Denario installed')"
```

## Or Use the Staged Script

```bash
./scripts/install_dependencies_staged.sh
```

## Why This Works

The issue is that `denario` has complex dependencies (langchain, cmbagent, etc.) that conflict with version constraints from other packages. By installing:
1. **Core dependencies first** - Gets all the base packages installed
2. **Denario separately** - Allows pip to resolve denario's dependencies against what's already installed

The `--use-deprecated=legacy-resolver` flag uses pip's older, faster resolver which is more lenient with conflicts.

## Alternative: Use uv (Fastest)

If you have `uv` installed (modern Python package manager):

```bash
# Install uv if not installed
brew install uv

# Install all dependencies (uv handles conflicts better)
uv pip install -r requirements.txt
```

## If Still Having Issues

Try installing denario with `--no-deps` first, then install its dependencies:

```bash
pip install denario[app]>=1.0.0 --no-deps
pip install denario[app]>=1.0.0  # This will install missing deps
```


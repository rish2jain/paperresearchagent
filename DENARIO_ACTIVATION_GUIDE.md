# Activating Denario Integration

**Last Updated:** 2025-01-16

---

## Prerequisites

Denario requires **Python 3.12+**. Currently you're on Python 3.11.9.

---

## Step-by-Step Activation Guide

### Option 1: Upgrade Python with pyenv (Recommended)

Since you're using `pyenv`, this is the easiest approach:

```bash
# 1. Install Python 3.12 (latest stable)
pyenv install 3.12.1

# 2. Set Python 3.12 for this project
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent
pyenv local 3.12.1

# 3. Verify Python version
python --version  # Should show 3.12.1

# 4. Recreate virtual environment (if using one)
# If you have a venv, deactivate and recreate:
deactivate  # if active
rm -rf venv
python -m venv venv
source venv/bin/activate

# 5. Uncomment denario in requirements.txt
# Edit requirements.txt and uncomment line 74:
# denario[app]>=1.0.0

# 6. Install dependencies
pip install -r requirements.txt

# 7. Set environment variable to enable Denario
export DENARIO_ENABLED=true

# 8. (Optional) Add to .env file for persistence
echo "DENARIO_ENABLED=true" >> .env
```

### Option 2: Use Python 3.12 System-Wide

If you prefer to use Python 3.12 system-wide:

```bash
# 1. Install Python 3.12 (using Homebrew on macOS)
brew install python@3.12

# 2. Use Python 3.12 for this project
python3.12 -m venv venv
source venv/bin/activate

# 3. Continue with steps 5-8 from Option 1
```

### Option 3: Keep Python 3.11 (Denario Disabled)

If you want to keep Python 3.11, Denario will remain disabled but the system will work normally without it.

---

## Verification

After activation, verify Denario is working:

```bash
# 1. Check Python version
python --version  # Should be 3.12+

# 2. Check if denario is installed
python -c "import denario; print('✅ Denario installed:', denario.__version__)"

# 3. Check environment variable
echo $DENARIO_ENABLED  # Should output "true"

# 4. Test the integration
python -c "
from src.denario_integration import DenarioIntegration
denario = DenarioIntegration(enabled=True)
print('✅ Denario available:', denario.is_available())
"
```

---

## Configuration

### Environment Variables

Add to your `.env` file or export:

```bash
# Enable Denario integration
DENARIO_ENABLED=true

# (Optional) Set custom project directory
DENARIO_PROJECT_DIR=./denario_projects
```

### API Usage

Denario is automatically enabled when:
1. `DENARIO_ENABLED=true` is set
2. Denario package is installed
3. Python 3.12+ is being used

The API endpoints will automatically use Denario features when available:
- `/research` - Enhanced synthesis with research ideas
- `/research/stream` - Enhanced streaming with Denario ideas

---

## Features Enabled

When Denario is activated, you get:

1. **Research Idea Generation** - Automatically generates research ideas from synthesis gaps and contradictions
2. **Methodology Suggestions** - Provides methodology recommendations for research ideas
3. **Paper Structure Generation** - Can generate LaTeX paper structures in various journal formats (APS, Nature, IEEE)

---

## Troubleshooting

### Issue: "Denario not installed"
- **Solution:** Make sure you've uncommented `denario[app]>=1.0.0` in `requirements.txt` and run `pip install -r requirements.txt`

### Issue: "Python version too old"
- **Solution:** Upgrade to Python 3.12+ using one of the options above

### Issue: "Denario not available" in logs
- **Check:** 
  1. `DENARIO_ENABLED=true` is set
  2. Python version is 3.12+
  3. Denario package is installed (`pip list | grep denario`)

### Issue: Import errors
- **Solution:** Make sure you're using the correct Python environment where denario is installed

---

## Quick Activation Script

Save this as `activate_denario.sh`:

```bash
#!/bin/bash
set -e

echo "🔧 Activating Denario Integration..."

# Check if Python 3.12+ is available
if ! pyenv versions | grep -q "3.12"; then
    echo "📦 Installing Python 3.12..."
    pyenv install 3.12.1
fi

# Set Python 3.12 for this project
echo "🔀 Switching to Python 3.12..."
pyenv local 3.12.1

# Verify version
python --version

# Uncomment denario in requirements.txt
echo "📝 Updating requirements.txt..."
sed -i.bak 's/^# denario\[app\]/denario[app]/' requirements.txt

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set environment variable
echo "🔧 Setting DENARIO_ENABLED=true..."
export DENARIO_ENABLED=true
echo "DENARIO_ENABLED=true" >> .env

echo "✅ Denario activation complete!"
echo ""
echo "To verify, run:"
echo "  python -c \"from src.denario_integration import DenarioIntegration; d = DenarioIntegration(enabled=True); print('Available:', d.is_available())\""
```

Make it executable and run:
```bash
chmod +x activate_denario.sh
./activate_denario.sh
```

---

**Note:** After activating Denario, restart your API server and Web UI to pick up the changes.


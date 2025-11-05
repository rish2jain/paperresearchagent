# Environment Variables Setup Guide

## Automatic .env File Loading

The system now **automatically loads** environment variables from a `.env` file in the project root directory.

### Quick Setup

1. **Create a `.env` file** in the project root directory (same level as `src/` and `requirements.txt`):

```bash
# .env file
IEEE_API_KEY=your_ieee_api_key_here
SPRINGER_API_KEY=your_springer_api_key_here
SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_key_here
ACM_API_KEY=your_acm_api_key_here

# Optional: NIM Configuration
REASONING_NIM_URL=http://localhost:8000
EMBEDDING_NIM_URL=http://localhost:8001

# Optional: AWS Integration
AWS_INTEGRATION_ENABLED=false
AWS_REGION=us-east-1

# Optional: Feature Flags
ENABLE_IEEE=true
ENABLE_SPRINGER=true
ENABLE_ACM=false
```

2. **The system will automatically:**
   - Load variables from `.env` when the application starts
   - Enable IEEE/Springer sources if API keys are present (unless explicitly disabled)
   - Use the keys for all API requests

### How It Works

The system loads `.env` files in three entry points:
- `src/config.py` - When configuration is loaded
- `src/api.py` - When the FastAPI server starts
- `src/web_ui.py` - When the Streamlit UI starts

**Note:** The `.env` file is automatically loaded from the project root directory. If running from a different directory, it will also try to load from the current working directory.

### Security Notes

⚠️ **Important:** 
- Never commit `.env` files to version control
- The `.env` file is already in `.gitignore` and `.cursorignore`
- Use `.env.example` as a template for documentation

### Verification

To verify your `.env` file is loaded correctly:

```bash
python -c "from src.config import PaperSourceConfig; config = PaperSourceConfig.from_env(); print(f'IEEE: {\"✅\" if config.ieee_api_key else \"❌\"}'); print(f'Springer: {\"✅\" if config.springer_api_key else \"❌\"}')"
```

### Alternative: Manual Environment Variables

If you prefer to set environment variables manually (without `.env` file):

```bash
export IEEE_API_KEY="your_key"
export SPRINGER_API_KEY="your_key"
```

Or add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export IEEE_API_KEY="your_key"
export SPRINGER_API_KEY="your_key"
```

### API Keys Required

| Source | API Key Required | Auto-Enable | Get Key |
|--------|------------------|-------------|---------|
| IEEE Xplore | ✅ Yes | ✅ Yes (if key present) | https://developer.ieee.org/ |
| Springer Link | ✅ Yes | ✅ Yes (if key present) | https://dev.springernature.com/ |
| ACM Digital Library | ✅ Yes | ✅ Yes (if key present) | Institutional access required |
| Semantic Scholar | ⚠️ Optional | ✅ Yes (if key present) | https://www.semanticscholar.org/product/api |

### Troubleshooting

**Problem:** API keys not loading from `.env`

**Solutions:**
1. Verify `.env` file is in project root (same directory as `src/`)
2. Check file format: `KEY=value` (no spaces around `=`)
3. Ensure no quotes around values unless needed
4. Check that `python-dotenv` is installed: `pip install python-dotenv`

**Problem:** Sources still showing as disabled

**Solutions:**
1. Verify keys are set correctly in `.env`
2. Check for typos in key names (must match exactly: `IEEE_API_KEY`, `SPRINGER_API_KEY`)
3. Restart the application after creating/updating `.env`
4. Check logs for ".env loaded" messages


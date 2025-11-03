# API Keys Setup Guide

This guide explains how to configure API keys for all paper sources.

## Required API Keys

### Free APIs (Recommended - No Key Required Initially)

These APIs work without keys but benefit from registration:

#### 1. **Semantic Scholar** (Optional but Recommended)

- **Status:** Works without key, but rate limits are stricter
- **Get Key:** https://www.semanticscholar.org/product/api
- **Rate Limits:**
  - Without key: 100 requests per 5 minutes
  - With key: 500 requests per 5 minutes
- **Setup:**
  ```bash
  export SEMANTIC_SCHOLAR_API_KEY="your_api_key_here"
  ```

#### 2. **Crossref** (No Key Required)

- **Status:** Free, no key needed
- **Mailto:** Recommended for polite API usage
- **Setup:**
  ```bash
  export CROSSREF_MAILTO="your-email@example.com"
  ```
- **Rate Limits:** Polite use recommended (not strict)

---

### Subscription-Based APIs (Optional)

These require paid subscriptions or institutional access:

#### 3. **IEEE Xplore**

- **Status:** Requires institutional subscription or API key
- **Get Key:** https://developer.ieee.org/
- **Cost:** Varies by institution
- **Setup:**
  ```bash
  export IEEE_API_KEY="your_ieee_api_key"
  export ENABLE_IEEE="true"
  ```

#### 4. **ACM Digital Library**

- **Status:** Requires institutional access
- **Get Access:** Contact ACM or your institution's library
- **Setup:**
  ```bash
  export ACM_API_KEY="your_acm_api_key"
  export ENABLE_ACM="true"
  ```
- **Note:** ACM API structure may vary - may require custom implementation

#### 5. **SpringerLink**

- **Status:** Requires API key
- **Get Key:** https://dev.springernature.com/
- **Cost:** Free tier available with limits
- **Setup:**
  ```bash
  export SPRINGER_API_KEY="your_springer_api_key"
  export ENABLE_SPRINGER="true"
  ```

---

## Configuration via Environment Variables

### Default Configuration (Free Sources Only)

By default, these sources are **enabled** (no keys needed):

- ✅ **arXiv** - Free, no key
- ✅ **PubMed** - Free, no key
- ✅ **Semantic Scholar** - Free tier (works without key)
- ✅ **Crossref** - Free, no key

These sources are **disabled** by default (require keys):

- ❌ **IEEE** - Requires API key (`ENABLE_IEEE=true`)
- ❌ **ACM** - Requires API key (`ENABLE_ACM=true`)
- ❌ **Springer** - Requires API key (`ENABLE_SPRINGER=true`)

### Enable/Disable Sources

You can enable or disable any source:

```bash
# Disable a free source
export ENABLE_ARXIV="false"
export ENABLE_PUBMED="false"

# Enable a paid source (requires API key)
export ENABLE_IEEE="true"
export IEEE_API_KEY="your_key"

# Enable Semantic Scholar with API key for higher limits
export ENABLE_SEMANTIC_SCHOLAR="true"
export SEMANTIC_SCHOLAR_API_KEY="your_key"
```

---

## Complete Setup Example

### Minimal Setup (Free Sources Only)

```bash
# No API keys needed! Uses free sources:
# - arXiv
# - PubMed
# - Semantic Scholar (no key)
# - Crossref
```

### Enhanced Setup (With Free API Keys)

```bash
# Semantic Scholar API key (optional but recommended)
export SEMANTIC_SCHOLAR_API_KEY="your_semanticscholar_key"

# Crossref mailto (recommended for polite usage)
export CROSSREF_MAILTO="research-ops@yourdomain.com"
```

### Full Setup (All Sources)

```bash
# Free sources
export SEMANTIC_SCHOLAR_API_KEY="your_semanticscholar_key"
export CROSSREF_MAILTO="research-ops@yourdomain.com"

# Paid sources (if you have access)
export IEEE_API_KEY="your_ieee_key"
export ACM_API_KEY="your_acm_key"
export SPRINGER_API_KEY="your_springer_key"

# Enable paid sources
export ENABLE_IEEE="true"
export ENABLE_ACM="true"
export ENABLE_SPRINGER="true"
```

---

## Docker Configuration

### docker-compose.yml

```yaml
services:
  orchestrator:
    environment:
      # Free API keys
      SEMANTIC_SCHOLAR_API_KEY: ${SEMANTIC_SCHOLAR_API_KEY:-}
      CROSSREF_MAILTO: ${CROSSREF_MAILTO:-research-ops@example.com}

      # Paid API keys (if available)
      IEEE_API_KEY: ${IEEE_API_KEY:-}
      ACM_API_KEY: ${ACM_API_KEY:-}
      SPRINGER_API_KEY: ${SPRINGER_API_KEY:-}

      # Enable/disable sources
      ENABLE_ARXIV: "true"
      ENABLE_PUBMED: "true"
      ENABLE_SEMANTIC_SCHOLAR: "true"
      ENABLE_CROSSREF: "true"
      ENABLE_IEEE: ${ENABLE_IEEE:-false}
      ENABLE_ACM: ${ENABLE_ACM:-false}
      ENABLE_SPRINGER: ${ENABLE_SPRINGER:-false}
```

### Kubernetes Secrets

Add to `k8s/secrets.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: research-ops-secrets
  namespace: research-ops
type: Opaque
stringData:
  # ... existing secrets ...

  # Paper source API keys
  SEMANTIC_SCHOLAR_API_KEY: "your_semanticscholar_key"
  CROSSREF_MAILTO: "research-ops@yourdomain.com"
  IEEE_API_KEY: "your_ieee_key" # Optional
  ACM_API_KEY: "your_acm_key" # Optional
  SPRINGER_API_KEY: "your_springer_key" # Optional

  # Enable/disable sources
  ENABLE_IEEE: "false"
  ENABLE_ACM: "false"
  ENABLE_SPRINGER: "false"
```

Then update deployment YAMLs to include these as environment variables.

---

## Testing Source Availability

You can test which sources are working:

```python
from agents import ScoutAgent
from nim_clients import EmbeddingNIMClient

async def test_sources():
    async with EmbeddingNIMClient() as embedding:
        scout = ScoutAgent(embedding)

        # Test individual sources
        arxiv_papers = await scout._search_arxiv("machine learning")
        pubmed_papers = await scout._search_pubmed("machine learning")
        semantic_papers = await scout._search_semantic_scholar("machine learning")
        crossref_papers = await scout._search_crossref("machine learning")

        print(f"arXiv: {len(arxiv_papers)} papers")
        print(f"PubMed: {len(pubmed_papers)} papers")
        print(f"Semantic Scholar: {len(semantic_papers)} papers")
        print(f"Crossref: {len(crossref_papers)} papers")
```

---

## Rate Limits Summary

| Source           | Free Tier  | With API Key  | Notes                         |
| ---------------- | ---------- | ------------- | ----------------------------- |
| arXiv            | Unlimited  | N/A           | No key needed                 |
| PubMed           | 3 req/sec  | 3 req/sec     | No key needed                 |
| Semantic Scholar | 100/5min   | 500/5min      | Key recommended               |
| Crossref         | Polite use | Polite use    | Mailto recommended            |
| IEEE             | Varies     | Varies        | Requires subscription         |
| ACM              | Varies     | Varies        | Requires institutional access |
| Springer         | Limited    | Higher limits | Free tier available           |

---

## Cost Considerations

### Free Sources (Recommended)

- **arXiv**: Free, unlimited
- **PubMed**: Free, unlimited
- **Semantic Scholar**: Free tier (recommended to get key)
- **Crossref**: Free, unlimited

**Total Cost: $0/month**

### Paid Sources (Optional)

- **IEEE**: Varies by institution ($100s-$1000s/year)
- **ACM**: Institutional subscription required
- **Springer**: Free tier available, paid plans vary

**Recommendation:** Start with free sources. Add paid sources only if:

1. You have institutional access
2. Your use case requires specific databases
3. Budget allows

---

## Troubleshooting

### Sources Not Returning Results

1. **Check API keys:**

   ```bash
   echo $SEMANTIC_SCHOLAR_API_KEY
   echo $IEEE_API_KEY
   ```

2. **Check enable flags:**

   ```bash
   echo $ENABLE_IEEE
   echo $ENABLE_ACM
   ```

3. **Check logs:**

   ```bash
   # In Docker
   docker-compose logs orchestrator | grep "Found.*papers from"

   # In Kubernetes
   kubectl logs deployment/agent-orchestrator -n research-ops | grep "Found"
   ```

### API Key Errors

- **403 Forbidden**: Invalid API key
- **429 Too Many Requests**: Rate limit exceeded
- **401 Unauthorized**: Missing or expired key

Check API key validity and rate limits for the specific service.

---

## Next Steps

1. **Start with free sources** - They work without configuration
2. **Get Semantic Scholar key** - Easy, free, improves rate limits
3. **Set Crossref mailto** - Polite API usage
4. **Add paid sources only if needed** - Based on your specific requirements

The system gracefully handles missing API keys and will use only the sources that are configured and enabled.

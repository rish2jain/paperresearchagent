# Quick Reference: Features Not Working Locally

## 🔴 Currently Not Available

1. **Denario Integration** ❌
   - Python 3.12+ ✅ (you have it)
   - Package not installed
   - Fix: `pip install denario`

2. **SSE Streaming** ❌
   - Package not installed
   - Fix: `pip install sseclient-py`
   - Note: Falls back to blocking mode automatically

3. **PDF Export** ❌
   - Library not installed
   - Fix: `pip install reportlab`
   - Note: Other export formats work

4. **Word Export** ❌
   - Library not installed
   - Fix: `pip install python-docx`
   - Note: Other export formats work

5. **Prometheus Metrics** ❌
   - Library not installed
   - Fix: `pip install prometheus-client`
   - Note: Optional, system works without it

## ✅ Currently Available

- ✅ Redis Cache (running)
- ✅ Python 3.12.12 (Denario compatible)
- ✅ Core features (agents, search, synthesis)
- ✅ 4 free paper sources
- ✅ Basic export formats (JSON, Markdown, BibTeX, LaTeX, CSV, Excel, HTML)

## ⚠️ Requires API Keys

- IEEE Xplore (disabled without key)
- ACM Digital Library (disabled without key)
- SpringerLink (disabled without key)

## ❌ Requires Cloud/AWS

- AWS Integration features
- EKS deployment features
- S3 backup storage

---

**See `LOCAL_SETUP_FEATURES_STATUS.md` for complete details.**


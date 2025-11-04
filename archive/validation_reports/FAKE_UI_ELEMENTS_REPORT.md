# Fake/Mock UI Elements Report

## 🔴 **CRITICAL: Fake Social Proof Metrics** (in sidebar)

All of these are **hardcoded defaults** that show fake data unless environment variables or APIs are configured:

### 1. **Active Researchers: 1,247**
- **Location:** Sidebar "👥 Researchers Trust Us" section
- **Default Value:** `"1,247"` (hardcoded)
- **Source:** `get_social_proof_metrics()` function
- **Can be real:** Set `SOCIAL_PROOF_ACTIVE_RESEARCHERS` env var or `SOCIAL_PROOF_RESEARCHERS_API_URL`
- **Status:** ❌ **FAKE by default**

### 2. **47 papers validated by professors**
- **Location:** Sidebar caption under "Active Researchers"
- **Default Value:** `"47"` (hardcoded)
- **Source:** `get_social_proof_metrics()` function
- **Can be real:** Set `SOCIAL_PROOF_VALIDATED_PAPERS` env var or `SOCIAL_PROOF_VALIDATED_PAPERS_API_URL`
- **Status:** ❌ **FAKE by default**

### 3. **Used at MIT, Stanford, Harvard, Oxford**
- **Location:** Sidebar caption
- **Default Value:** `"MIT, Stanford, Harvard, Oxford"` (hardcoded)
- **Source:** `get_social_proof_metrics()` function
- **Can be real:** Set `SOCIAL_PROOF_INSTITUTIONS` env var (comma-separated list)
- **Status:** ❌ **FAKE by default**

### 4. **⭐ 4.9/5 average rating**
- **Location:** Sidebar caption
- **Default Value:** `"4.9"` (hardcoded)
- **Source:** `get_social_proof_metrics()` function
- **Can be real:** Set `SOCIAL_PROOF_RATING` env var or `SOCIAL_PROOF_RATING_API_URL`
- **Status:** ❌ **FAKE by default**

**All show:** `(Source: Environment variable or default (last updated: 2025-11-04), Last updated: 2025-11-04)` when using defaults.

---

## 🟡 **Enhanced Insights - Partially Simulated**

### In Enhanced Insights Module (`src/enhanced_insights.py`):

1. **Citation Counts** (Line 443)
   ```python
   "citations": 1000 - (i * 100),  # Simulated
   ```
   - **Status:** ⚠️ **SIMULATED** - Would need real citation API (Semantic Scholar, Crossref)

2. **Field Growth Rate** (Line 495)
   ```python
   "field_growth": "+245%",  # Simulated
   ```
   - **Status:** ⚠️ **SIMULATED** - Would need publication date analysis

3. **Trending Theme Growth Rates** (Line 481)
   ```python
   "growth_rate": "+87%",  # Simulated
   ```
   - **Status:** ⚠️ **SIMULATED** - Would need temporal analysis

**Note:** These are clearly marked as "simulated" in code comments, but users don't see that.

---

## 🟢 **Demo Mode - Intentionally Fake**

When `DEMO_MODE=true`, all results are pre-generated mock data:
- Papers are fake
- Analyses are fake
- Synthesis is fake
- Enhanced insights are fake (but realistic-looking)

**Status:** ✅ **INTENTIONAL** - This is for demonstrations when NIMs aren't available.

---

## 📋 **Recommendations**

### For Hackathon Submission:

1. **Remove or Hide Fake Social Proof:**
   - Option A: Remove the entire "👥 Researchers Trust Us" section
   - Option B: Only show if real data is available (check if env vars are set)
   - Option C: Replace with actual metrics (e.g., "X papers analyzed this session")

2. **Clarify Simulated Data:**
   - Add "(estimated)" or "(simulated)" labels to enhanced insights
   - Or remove simulated fields entirely

3. **Use Real Metrics Instead:**
   - Session stats (real queries run)
   - Papers analyzed (real count)
   - Decisions made (real count)
   - Processing time (real)

### Code Locations to Fix:

1. **Social Proof Section:** `src/web_ui.py` lines 1935-1998
2. **Enhanced Insights Simulations:** `src/enhanced_insights.py` lines 439-495
3. **Demo Mode:** `src/agents.py` lines 1776-1947 (intentional, but should be clearly marked)

---

## ✅ **What's REAL:**

- Papers found (from actual API searches)
- Analyses (from Reasoning NIM)
- Synthesis results (from actual processing)
- Decision logs (from actual agent decisions)
- Processing times (real)
- Session statistics (real)
- Quality scores (calculated from real data)
- Consensus analysis (calculated from real findings)
- Research opportunities (derived from real gaps)
- Hot debates (from real contradictions)

---

## 🎯 **Quick Fix Options:**

### Option 1: Remove Fake Social Proof (Recommended)
Remove the entire "👥 Researchers Trust Us" section from sidebar.

### Option 2: Show Only If Real Data Available
Only display social proof metrics if environment variables are actually set.

### Option 3: Replace with Real Metrics
Show actual session/user statistics instead of fake social proof.


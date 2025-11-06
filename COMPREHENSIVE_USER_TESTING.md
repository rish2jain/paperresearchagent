# Comprehensive User Testing Guide

**Last Updated:** 2025-01-16  
**Purpose:** Complete guide for testing all features of ResearchOps Agent  
**Audience:** Users, Testers, QA Engineers, Hackathon Judges

---

## 🎯 Overview

This guide provides comprehensive testing procedures for all features of ResearchOps Agent. Use this guide to:
- Verify all features work correctly
- Test edge cases and error handling
- Validate user experience
- Ensure production readiness

---

## 📋 Pre-Testing Checklist

### Prerequisites
- [ ] System is deployed (local or EKS)
- [ ] All services are running (API, Web UI, NIMs)
- [ ] API keys configured (if testing optional sources)
- [ ] Test data prepared (sample queries)

### Access Points
- [ ] Web UI accessible: `http://localhost:8501` (local) or deployed URL
- [ ] API accessible: `http://localhost:8080` (local) or deployed URL
- [ ] API docs accessible: `http://localhost:8080/docs`
- [ ] Health check: `http://localhost:8080/health`

---

## 🧪 Test Categories

### 1. Core Functionality Tests

#### 1.1 Basic Search and Retrieval ✅

**Test Case:** Basic query search
1. Navigate to Web UI
2. Enter query: "machine learning for medical imaging"
3. Set max papers: 10
4. Click "Search"
5. **Expected Results:**
   - Progress indicator shows stages (Searching → Analyzing → Synthesizing)
   - Papers are retrieved from multiple sources
   - At least 5-10 papers displayed
   - Papers show title, authors, abstract, source

**Test Case:** Query with filters
1. Enter query: "deep learning"
2. Set date range: 2020-2024
3. Select sources: arXiv, PubMed
4. Click "Search"
5. **Expected Results:**
   - Only papers from selected sources
   - Only papers within date range
   - Results filtered correctly

**Test Case:** Boolean search
1. Enter query: "machine learning AND medical imaging"
2. Click "Search"
3. **Expected Results:**
   - Query parsed correctly
   - Results match both terms
   - Decision log shows boolean query expansion

**Test Case:** Query expansion
1. Enter query: "ML healthcare"
2. Click "Search"
3. **Expected Results:**
   - Query expanded to variations
   - Decision log shows expansion
   - More comprehensive results

#### 1.2 Paper Analysis ✅

**Test Case:** Analysis extraction
1. Run a search query
2. Wait for analysis phase
3. **Expected Results:**
   - Each paper shows:
     - Research question
     - Methodology
     - Key findings (3+ items)
     - Limitations (2+ items)
     - Confidence score (0.0-1.0)
   - Analysis appears in real-time

**Test Case:** Enhanced extraction
1. Run search on papers with statistical results
2. Check analysis metadata
3. **Expected Results:**
   - Statistical results extracted (p-values, effect sizes)
   - Experimental setup details
   - Reproducibility information
   - Comparative results

**Test Case:** Quality assessment
1. Run search query
2. Check quality scores
3. **Expected Results:**
   - Each paper has quality score
   - Scores include:
     - Overall score
     - Methodology score
     - Statistical score
     - Reproducibility score
     - Venue score
   - Scores displayed clearly

#### 1.3 Synthesis ✅

**Test Case:** Theme identification
1. Run search query
2. Wait for synthesis
3. **Expected Results:**
   - Common themes identified (3+ themes)
   - Themes are distinct and meaningful
   - Themes link to relevant papers

**Test Case:** Contradiction detection
1. Run search query
2. Check contradictions section
3. **Expected Results:**
   - Contradictions identified (if any)
   - Clear explanation of conflicts
   - Papers involved listed

**Test Case:** Gap identification
1. Run search query
2. Check research gaps section
3. **Expected Results:**
   - Gaps identified (3+ gaps)
   - Gaps are specific and actionable
   - Gaps link to missing research areas

**Test Case:** Enhanced insights
1. Run search query
2. Check enhanced insights section
3. **Expected Results:**
   - Field maturity score
   - Research opportunities listed
   - Consensus scores shown
   - Hot debates identified (if any)
   - Expert guidance provided

#### 1.4 Export Functionality ✅

**Test Case:** Export all formats
1. Run search query
2. Wait for results
3. Test each export format:
   - JSON
   - Markdown
   - BibTeX
   - LaTeX
   - Word (.docx)
   - PDF
   - CSV
   - Excel (.xlsx)
   - EndNote (.enw)
   - HTML
   - Citations (5 styles)
4. **Expected Results:**
   - All formats download successfully
   - Content is correct
   - Formatting is proper
   - Citations are accurate

---

### 2. Enhancement Features Tests

#### 2.1 Hybrid Retrieval ✅

**Test Case:** Hybrid retrieval enabled
1. Set `USE_HYBRID_RETRIEVAL=true`
2. Run search query
3. Check decision log
4. **Expected Results:**
   - Decision log shows "Hybrid Retrieval (Dense + Sparse + Citation)"
   - Multiple retrieval methods used
   - RRF fusion applied
   - Better precision than single method

**Test Case:** BM25 sparse retrieval
1. Enable hybrid retrieval
2. Run query with specific keywords
3. **Expected Results:**
   - BM25 index built
   - Sparse retrieval results included
   - Keyword matches found

**Test Case:** Citation graph retrieval
1. Enable hybrid retrieval
2. Run query
3. **Expected Results:**
   - Citation graph built (if Semantic Scholar API key available)
   - Citation relationships used
   - Influential papers identified

#### 2.2 Cross-Encoder Reranking ✅

**Test Case:** Reranking enabled
1. Set `USE_RERANKING=true`
2. Run search query
3. Check decision log
4. **Expected Results:**
   - Decision log shows reranking step
   - Top 50-100 papers reranked
   - Better relevance ordering
   - Improved top-k results

#### 2.3 Enhanced Caching ✅

**Test Case:** Multi-level cache
1. Run same query twice
2. Check cache behavior
3. **Expected Results:**
   - Second query much faster (10-50x)
   - Cache hit logged
   - Results identical
   - L1 (memory) → L2 (Redis) → L3 (disk) hierarchy

**Test Case:** Cache expiration
1. Run query
2. Wait 1+ hour
3. Run same query again
4. **Expected Results:**
   - Cache expired
   - Fresh results generated
   - Cache updated

#### 2.4 Graph-Based Synthesis ✅

**Test Case:** Graph synthesis
1. Run search query
2. Check synthesis results
3. **Expected Results:**
   - Theme clusters from graph analysis
   - Bridge papers identified
   - Community detection results
   - Citation relationships visualized

#### 2.5 Temporal Trend Analysis ✅

**Test Case:** Trend analysis
1. Run query with papers spanning multiple years
2. Check temporal analysis
3. **Expected Results:**
   - Trends over time identified
   - Growth patterns detected
   - Future predictions (if enabled)
   - Timeline visualization

#### 2.6 Meta-Analysis ✅

**Test Case:** Quantitative synthesis
1. Run query on papers with statistical results
2. Check meta-analysis section
3. **Expected Results:**
   - Quantitative results extracted
   - Effect sizes calculated
   - Pooled effects computed
   - Heterogeneity assessed
   - Statistical tests performed

---

### 3. User Interface Tests

#### 3.1 Web UI Functionality ✅

**Test Case:** Basic UI elements
1. Open Web UI
2. **Expected Results:**
   - Query input field visible
   - Max papers slider works
   - Source selection checkboxes work
   - Date range picker works
   - Search button enabled

**Test Case:** Progress tracking
1. Run search query
2. **Expected Results:**
   - Progress bar shows stages
   - Current stage highlighted
   - Time estimates shown
   - NIM usage indicators visible
   - Real-time updates

**Test Case:** Results display
1. Run search query
2. **Expected Results:**
   - Papers displayed in cards
   - Expandable sections work
   - Collapsible synthesis works
   - Decision log expandable
   - Metrics summary visible

**Test Case:** Interactive features
1. Run search query
2. Test interactions:
   - Expand/collapse sections
   - Filter papers
   - Sort papers
   - Export results
3. **Expected Results:**
   - All interactions work smoothly
   - No UI freezing
   - Responsive design

#### 3.2 Accessibility ✅

**Test Case:** Keyboard navigation
1. Use keyboard only (no mouse)
2. Navigate through UI
3. **Expected Results:**
   - Tab navigation works
   - Enter key submits query
   - Arrow keys navigate lists
   - Escape closes modals
   - Focus indicators visible

**Test Case:** Screen reader compatibility
1. Use screen reader
2. Navigate UI
3. **Expected Results:**
   - ARIA labels present
   - Semantic HTML used
   - Alt text for images
   - Form labels associated
   - WCAG 2.1 AA compliant

#### 3.3 Responsive Design ✅

**Test Case:** Mobile view
1. Resize browser to mobile size
2. Test UI
3. **Expected Results:**
   - Layout adapts
   - Text readable
   - Buttons accessible
   - Forms usable
   - No horizontal scroll

**Test Case:** Tablet view
1. Resize browser to tablet size
2. Test UI
3. **Expected Results:**
   - Layout optimized
   - All features accessible
   - Touch targets adequate

---

### 4. API Tests

#### 4.1 REST API Endpoints ✅

**Test Case:** Health check
```bash
curl http://localhost:8080/health
```
**Expected Results:**
- Status 200
- JSON response with status
- All services healthy

**Test Case:** Search endpoint
```bash
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "max_papers": 10}'
```
**Expected Results:**
- Status 200
- JSON response with results
- All expected fields present

**Test Case:** SSE streaming
```bash
curl http://localhost:8080/research/stream?query=machine+learning
```
**Expected Results:**
- Server-Sent Events stream
- Real-time updates
- Progress events
- Final result event

**Test Case:** Export endpoints
```bash
curl http://localhost:8080/api/export?format=json&query_id=123
```
**Expected Results:**
- Correct format returned
- Content-Type header correct
- File downloads properly

#### 4.2 Error Handling ✅

**Test Case:** Invalid query
```bash
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "", "max_papers": 10}'
```
**Expected Results:**
- Status 400
- Error message clear
- Validation error details

**Test Case:** Missing parameters
```bash
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{}'
```
**Expected Results:**
- Status 422
- Validation errors listed
- Helpful error messages

**Test Case:** Service unavailable
1. Stop NIM services
2. Run query
3. **Expected Results:**
   - Graceful error handling
   - Clear error message
   - Fallback behavior (if configured)
   - No crashes

---

### 5. Performance Tests

#### 5.1 Response Times ✅

**Test Case:** First query
1. Clear cache
2. Run query
3. Measure time
4. **Expected Results:**
   - Complete in 2-5 minutes
   - Progress updates visible
   - No timeouts

**Test Case:** Cached query
1. Run query (cache it)
2. Run same query again
3. Measure time
4. **Expected Results:**
   - Complete in <10 seconds
   - Cache hit logged
   - Results identical

**Test Case:** Large query
1. Run query with max_papers=50
2. Measure time
3. **Expected Results:**
   - Handles large queries
   - Progress visible
   - No memory issues
   - Completes successfully

#### 5.2 Concurrent Requests ✅

**Test Case:** Multiple users
1. Run 3 queries simultaneously
2. **Expected Results:**
   - All queries process
   - No conflicts
   - Resources shared properly
   - No crashes

---

### 6. Integration Tests

#### 6.1 End-to-End Workflow ✅

**Test Case:** Complete workflow
1. Start from Web UI
2. Enter query
3. Wait for completion
4. Review results
5. Export results
6. **Expected Results:**
   - All phases complete
   - Results accurate
   - Export successful
   - No errors

**Test Case:** Multiple queries
1. Run 5 different queries
2. **Expected Results:**
   - All queries succeed
   - Results independent
   - Cache works correctly
   - No memory leaks

#### 6.2 Data Source Integration ✅

**Test Case:** All sources enabled
1. Enable all 7 sources
2. Run query
3. **Expected Results:**
   - Papers from all sources
   - No source errors
   - Deduplication works
   - Results combined correctly

**Test Case:** Source failures
1. Disable one source
2. Run query
3. **Expected Results:**
   - Query succeeds
   - Other sources work
   - Error logged
   - No crashes

---

### 7. Edge Cases and Error Scenarios

#### 7.1 Invalid Inputs ✅

**Test Case:** Empty query
- Input: ""
- **Expected:** Validation error, helpful message

**Test Case:** Very long query
- Input: 1000+ characters
- **Expected:** Validation error or truncation

**Test Case:** Special characters
- Input: "query<script>alert('xss')</script>"
- **Expected:** Sanitized, no XSS

**Test Case:** SQL injection attempt
- Input: "query'; DROP TABLE papers; --"
- **Expected:** Sanitized, no SQL execution

#### 7.2 Boundary Conditions ✅

**Test Case:** Max papers = 1
- **Expected:** Works correctly, returns 1 paper

**Test Case:** Max papers = 100
- **Expected:** Handles large requests, may take longer

**Test Case:** Date range: future dates
- **Expected:** No papers found, handled gracefully

**Test Case:** Date range: very old dates
- **Expected:** Limited results, handled gracefully

#### 7.3 Network Issues ✅

**Test Case:** Slow network
1. Throttle network
2. Run query
3. **Expected Results:**
   - Timeouts handled
   - Retries work
   - Progress updates continue
   - Graceful degradation

**Test Case:** Intermittent failures
1. Simulate network failures
2. Run query
3. **Expected Results:**
   - Circuit breaker activates
   - Fallback behavior
   - Error recovery
   - No crashes

---

### 8. Security Tests

#### 8.1 Input Validation ✅

**Test Case:** XSS attempts
- Test various XSS payloads
- **Expected:** All sanitized, no execution

**Test Case:** Path traversal
- Test "../" patterns
- **Expected:** Blocked, validation error

**Test Case:** Command injection
- Test shell command attempts
- **Expected:** Blocked, sanitized

#### 8.2 Authentication ✅

**Test Case:** API key authentication
1. Set `REQUIRE_API_AUTH=true`
2. Test without key
3. **Expected:** 401 Unauthorized

**Test Case:** Rate limiting
1. Send many requests quickly
2. **Expected:** Rate limit enforced
3. **Expected:** 429 Too Many Requests

---

## 📊 Test Results Template

Use this template to record test results:

```markdown
## Test Session: [Date]

### Environment
- Deployment: [Local/EKS]
- Services: [List running services]
- Configuration: [Key settings]

### Test Results

#### Core Functionality
- [ ] Basic Search: ✅/❌
- [ ] Paper Analysis: ✅/❌
- [ ] Synthesis: ✅/❌
- [ ] Export: ✅/❌

#### Enhancement Features
- [ ] Hybrid Retrieval: ✅/❌
- [ ] Reranking: ✅/❌
- [ ] Caching: ✅/❌
- [ ] Graph Synthesis: ✅/❌
- [ ] Temporal Analysis: ✅/❌
- [ ] Meta-Analysis: ✅/❌

#### UI/UX
- [ ] Basic UI: ✅/❌
- [ ] Progress Tracking: ✅/❌
- [ ] Accessibility: ✅/❌
- [ ] Responsive Design: ✅/❌

#### API
- [ ] Endpoints: ✅/❌
- [ ] Error Handling: ✅/❌
- [ ] Performance: ✅/❌

#### Integration
- [ ] End-to-End: ✅/❌
- [ ] Data Sources: ✅/❌

### Issues Found
1. [Issue description]
2. [Issue description]

### Notes
[Additional observations]
```

---

## 🐛 Bug Reporting

When reporting bugs, include:
1. **Test Case:** Which test case failed
2. **Steps to Reproduce:** Exact steps
3. **Expected Result:** What should happen
4. **Actual Result:** What actually happened
5. **Environment:** Deployment type, versions, config
6. **Logs:** Relevant error logs
7. **Screenshots:** If UI issue

---

## ✅ Acceptance Criteria

A feature is considered **working** if:
- ✅ All test cases pass
- ✅ No crashes or errors
- ✅ Performance acceptable
- ✅ UI responsive
- ✅ Error handling graceful
- ✅ Documentation accurate

---

## 🚀 Quick Test Script

Run this quick test to verify basic functionality:

```bash
# 1. Health check
curl http://localhost:8080/health

# 2. Basic search
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "max_papers": 5}'

# 3. Check Web UI
open http://localhost:8501
```

---

**For detailed testing procedures, see:**
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing with mock vs live services
- [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md) - Local testing procedures
- [hackathon_submission/JUDGE_TESTING_GUIDE.md](hackathon_submission/JUDGE_TESTING_GUIDE.md) - Judge testing guide


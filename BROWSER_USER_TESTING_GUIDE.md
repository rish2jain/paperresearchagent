# Browser User Testing Execution Guide

**Date:** 2025-01-16  
**Application:** ResearchOps Agent Web UI  
**URL:** http://localhost:8501  
**API:** http://localhost:8080

## Prerequisites

- ✅ Web UI running on http://localhost:8501
- ✅ API running on http://localhost:8080
- ✅ Browser MCP tools available
- ✅ Screenshots directory created: `user_testing_screenshots/`

## Test Execution Plan

### Test 1: Page Load and Initial State

**Objective:** Verify the web UI loads correctly and all initial elements are visible.

**Steps:**
1. Navigate to `http://localhost:8501`
2. Wait for page to fully load
3. Take accessibility snapshot
4. Take screenshot: `test_1_page_load.png`
5. Verify:
   - Page title contains "Research Ops Agent" or "Agentic Scholar"
   - Sidebar is visible on the left
   - Query input field is present
   - Max papers slider is visible
   - Search/Start button is present
   - No JavaScript errors in console

**Expected Results:**
- ✅ Page loads without errors
- ✅ All UI elements are visible
- ✅ Layout is correct

---

### Test 2: Query Input Form Interaction

**Objective:** Verify all form elements are functional.

**Steps:**
1. Locate query input field (use snapshot to find element reference)
2. Click on query input field
3. Type: "machine learning for medical imaging"
4. Locate max papers slider
5. Adjust slider to value 10
6. Locate date range picker (if present)
7. Check source selection checkboxes (if present)
8. Take screenshot: `test_2_form_interaction.png`

**Expected Results:**
- ✅ Query input accepts text
- ✅ Slider adjusts value
- ✅ Date range picker works (if present)
- ✅ Checkboxes toggle (if present)

---

### Test 3: Basic Search Query Execution

**Objective:** Execute a basic search and verify the workflow.

**Steps:**
1. Clear any existing query
2. Enter query: "machine learning"
3. Set max papers to 10
4. Click "Start Research" or "Search" button
5. Wait for progress indicator to appear
6. Monitor progress updates
7. Take screenshots at key stages:
   - `test_3_progress_searching.png` (Searching stage)
   - `test_3_progress_analyzing.png` (Analyzing stage)
   - `test_3_progress_synthesizing.png` (Synthesizing stage)
   - `test_3_results_complete.png` (Results displayed)

**Expected Results:**
- ✅ Query submits successfully
- ✅ Progress bar appears
- ✅ Stages update: Searching → Analyzing → Synthesizing
- ✅ Results appear within 2-5 minutes
- ✅ No errors occur

---

### Test 4: Progress Tracking and Real-time Updates

**Objective:** Verify progress tracking works correctly.

**Steps:**
1. Start a new search query
2. Observe progress bar updates
3. Check stage indicators (Searching, Analyzing, Synthesizing)
4. Verify time estimates are shown
5. Check for NIM usage badges:
   - 🟦 Reasoning NIM badge
   - 🟩 Embedding NIM badge
6. Monitor decision log updates (if visible)
7. Take screenshot: `test_4_progress_tracking.png`

**Expected Results:**
- ✅ Progress updates in real-time
- ✅ Current stage is highlighted
- ✅ Time estimates are displayed
- ✅ NIM badges appear correctly
- ✅ Decision log updates live (if visible)

---

### Test 5: Results Display and Paper Cards

**Objective:** Verify results are displayed correctly.

**Steps:**
1. Wait for search to complete
2. Verify papers are displayed in cards
3. Check each paper card shows:
   - Title
   - Authors
   - Abstract (or preview)
   - Source badge
4. Click to expand paper details (if expandable)
5. Verify abstract is fully visible when expanded
6. Check source attribution is correct
7. Take screenshot: `test_5_results_display.png`

**Expected Results:**
- ✅ Papers displayed in cards
- ✅ All required information is shown
- ✅ Expandable sections work
- ✅ Source badges are visible

---

### Test 6: Decision Log Display

**Objective:** Verify decision log shows agent decisions correctly.

**Steps:**
1. Locate decision log section
2. Expand decision log (if collapsed)
3. Verify agent decisions are shown:
   - Scout Agent decisions
   - Analyst Agent decisions
   - Synthesizer Agent decisions
   - Coordinator Agent decisions
4. Check NIM badges for each decision:
   - 🟦 Reasoning NIM badge
   - 🟩 Embedding NIM badge
   - 🟦🟩 Both badges (if both used)
5. Verify decision reasoning text is displayed
6. Check timeline visualization (if present)
7. Take screenshot: `test_6_decision_log.png`

**Expected Results:**
- ✅ Decision log is expandable
- ✅ All 4 agents show decisions
- ✅ NIM badges correctly identify which NIM was used
- ✅ Decision reasoning is displayed
- ✅ Timeline shows chronological order

---

### Test 7: Synthesis Display

**Objective:** Verify synthesis results are displayed correctly.

**Steps:**
1. Locate synthesis section
2. Verify themes are listed
3. Check contradictions section (if any)
4. Verify research gaps section
5. Check enhanced insights dashboard:
   - Field maturity score
   - Research opportunities
   - Consensus scores
   - Hot debates (if any)
6. Test expand/collapse functionality
7. Take screenshot: `test_7_synthesis_display.png`

**Expected Results:**
- ✅ Synthesis section is visible
- ✅ Themes are clearly listed
- ✅ Contradictions are highlighted (if present)
- ✅ Research gaps are identified
- ✅ Enhanced insights dashboard shows metrics
- ✅ Expand/collapse works smoothly

---

### Test 8: Export Functionality

**Objective:** Verify export options work correctly.

**Steps:**
1. Locate export dropdown/button
2. Click to open export options
3. Test JSON export:
   - Click JSON option
   - Verify download triggers
4. Test Markdown export:
   - Click Markdown option
   - Verify download triggers
5. Test BibTeX export:
   - Click BibTeX option
   - Verify download triggers
6. Take screenshot: `test_8_export_options.png`

**Expected Results:**
- ✅ Export options are available
- ✅ Downloads trigger successfully
- ✅ All export formats work

---

### Test 9: Responsive Design Testing

**Objective:** Verify the UI adapts to different screen sizes.

**Steps:**
1. Resize browser to 375px width (mobile)
2. Take screenshot: `test_9_mobile_375px.png`
3. Verify layout adapts
4. Resize to 768px width (tablet)
5. Take screenshot: `test_9_tablet_768px.png`
6. Verify layout adapts
7. Resize to 1920px width (desktop)
8. Take screenshot: `test_9_desktop_1920px.png`
9. Verify layout adapts

**Expected Results:**
- ✅ Layout adapts to mobile size
- ✅ Layout adapts to tablet size
- ✅ Layout adapts to desktop size
- ✅ No horizontal scrolling
- ✅ All elements remain accessible

---

### Test 10: Error Handling and Validation

**Objective:** Verify error handling works correctly.

**Steps:**
1. Submit empty query
2. Verify error message appears
3. Take screenshot: `test_10_empty_query_error.png`
4. Enter query with invalid date range (e.g., future dates)
5. Verify validation error
6. Test with special characters: `<script>alert('xss')</script>`
7. Verify sanitization (no XSS)
8. Take screenshot: `test_10_validation.png`

**Expected Results:**
- ✅ Empty query shows error
- ✅ Invalid inputs are validated
- ✅ Error messages are clear
- ✅ Special characters are sanitized
- ✅ No crashes occur

---

## Browser MCP Tool Usage

### Navigation
```python
browser_navigate(url="http://localhost:8501")
```

### Taking Snapshots
```python
snapshot = browser_snapshot()
# Use snapshot to find element references
```

### Clicking Elements
```python
browser_click(
    element="query input field",
    ref="<element_ref_from_snapshot>"
)
```

### Typing Text
```python
browser_type(
    element="query input",
    ref="<element_ref>",
    text="machine learning"
)
```

### Taking Screenshots
```python
browser_take_screenshot(
    filename="test_1_page_load.png"
)
```

### Waiting
```python
browser_wait_for(text="Searching")
browser_wait_for(time=5)  # Wait 5 seconds
```

---

## Test Results Template

```markdown
## Test Results - [Date]

### Test 1: Page Load
- Status: ✅ PASS / ❌ FAIL
- Screenshot: test_1_page_load.png
- Notes: [Any observations]

### Test 2: Query Input Form
- Status: ✅ PASS / ❌ FAIL
- Screenshot: test_2_form_interaction.png
- Notes: [Any observations]

[... continue for all tests ...]

## Summary
- Total Tests: 10
- Passed: X
- Failed: Y
- Success Rate: Z%
```

---

## Next Steps

1. Execute each test scenario using browser MCP tools
2. Document results (PASS/FAIL) for each test
3. Capture screenshots at key interaction points
4. Generate final report with test results
5. Document any issues or bugs found

---

**Note:** If browser MCP tools are not working, these tests can be executed manually using a regular browser, following the same steps and taking screenshots manually.


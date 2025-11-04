# User Testing Plan - ResearchOps Agent

## Testing Overview

This document outlines a comprehensive user testing plan for the ResearchOps Agent application, covering UI/UX, functionality, performance, and error handling.

**Date:** 2025-01-XX  
**Application:** ResearchOps Agent (Multi-agent AI Literature Review System)  
**Testing Scope:** Web UI (Streamlit) + Backend API (FastAPI)

---

## Test Environment Setup

### Prerequisites
- Backend API running on `http://localhost:8080`
- Web UI running on `http://localhost:8501`
- Python virtual environment activated
- All dependencies installed

### Services to Start
```bash
# Terminal 1: Backend API
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent
source venv/bin/activate
uvicorn src.api:app --reload --host 0.0.0.0 --port 8080

# Terminal 2: Web UI
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent
source venv/bin/activate
streamlit run src/web_ui.py
```

---

## Test Categories

### 1. UI/UX Testing
### 2. Functional Testing
### 3. API Integration Testing
### 4. Error Handling Testing
### 5. Performance Testing
### 6. Accessibility Testing
### 7. Responsive Design Testing
### 8. Data Export Testing

---

## Detailed Test Cases

### 1. UI/UX Testing

#### Test 1.1: Initial Page Load
**Objective:** Verify the application loads correctly  
**Steps:**
1. Navigate to `http://localhost:8501`
2. Wait for page to fully load

**Expected Results:**
- ✅ Page loads without errors
- ✅ Page title is visible: "🔬 Research Ops Agent - Agentic Scholar"
- ✅ Sidebar is visible with query input
- ✅ Main content area is visible
- ✅ No JavaScript errors in console
- ✅ No Python errors in terminal

**Priority:** P0 (Critical)

---

#### Test 1.2: Query Input Form
**Objective:** Verify query input form is functional  
**Steps:**
1. Check sidebar form elements
2. Enter a test query: "machine learning for medical imaging"
3. Adjust max papers slider
4. Toggle date filters
5. Select paper sources

**Expected Results:**
- ✅ Query text input is visible and functional
- ✅ Max papers slider works (range 1-50)
- ✅ Date range inputs work (start year, end year)
- ✅ "Prioritize recent" checkbox works
- ✅ Paper source checkboxes are selectable
- ✅ Form validation works (e.g., max papers > 0)

**Priority:** P0 (Critical)

---

#### Test 1.3: Submit Query Button
**Objective:** Verify query submission works  
**Steps:**
1. Enter a query: "quantum computing"
2. Set max papers to 5
3. Click "Start Research" button

**Expected Results:**
- ✅ Button is visible and clickable
- ✅ Button state changes on click (loading state)
- ✅ Query is submitted to backend
- ✅ Loading indicator appears
- ✅ Results appear after processing

**Priority:** P0 (Critical)

---

#### Test 1.4: Results Display
**Objective:** Verify results are displayed correctly  
**Steps:**
1. Submit a query
2. Wait for results
3. Check all result sections

**Expected Results:**
- ✅ Results section appears
- ✅ Papers analyzed count is displayed
- ✅ Common themes section is visible
- ✅ Contradictions section is visible
- ✅ Research gaps section is visible
- ✅ Decision log is accessible
- ✅ All visualizations render correctly

**Priority:** P0 (Critical)

---

#### Test 1.5: Navigation and Layout
**Objective:** Verify navigation and layout consistency  
**Steps:**
1. Navigate through different sections
2. Check sidebar remains accessible
3. Scroll through results
4. Check sticky elements

**Expected Results:**
- ✅ Sidebar navigation works
- ✅ Main content scrolls smoothly
- ✅ Sticky headers work (if any)
- ✅ Back to top button works (if any)
- ✅ Layout is consistent across sections

**Priority:** P1 (High)

---

### 2. Functional Testing

#### Test 2.1: Basic Research Query
**Objective:** Verify basic research functionality  
**Steps:**
1. Enter query: "machine learning"
2. Set max papers: 10
3. Submit query
4. Wait for results

**Expected Results:**
- ✅ Query processes successfully
- ✅ Papers are retrieved (count > 0)
- ✅ Themes are identified
- ✅ Processing completes within 5 minutes
- ✅ Results are formatted correctly

**Priority:** P0 (Critical)

---

#### Test 2.2: Date Range Filtering
**Objective:** Verify date filtering works  
**Steps:**
1. Enter query: "deep learning"
2. Set start year: 2020
3. Set end year: 2024
4. Enable "Prioritize recent"
5. Submit query

**Expected Results:**
- ✅ Only papers within date range are shown
- ✅ Year distribution chart reflects filter
- ✅ "Prioritize recent" affects paper ordering
- ✅ Filter is applied correctly

**Priority:** P1 (High)

---

#### Test 2.3: Paper Source Selection
**Objective:** Verify paper source filtering works  
**Steps:**
1. Enter query: "neural networks"
2. Select only "arXiv" source
3. Submit query
4. Check paper sources in results

**Expected Results:**
- ✅ Only selected sources are searched
- ✅ Paper source distribution shows correct sources
- ✅ Source filter works correctly

**Priority:** P1 (High)

---

#### Test 2.4: Decision Log Display
**Objective:** Verify decision log is accessible  
**Steps:**
1. Submit a query
2. Wait for results
3. Expand "Decision Log" section
4. Review decisions

**Expected Results:**
- ✅ Decision log section is visible
- ✅ Decisions are listed chronologically
- ✅ Agent names are shown (Scout, Analyst, Synthesizer, Coordinator)
- ✅ Decision types are displayed
- ✅ Reasoning is shown for each decision
- ✅ NIM usage is indicated

**Priority:** P0 (Critical) - Key for hackathon judging

---

#### Test 2.5: Export Functionality
**Objective:** Verify export features work  
**Steps:**
1. Submit a query and get results
2. Test each export format:
   - BibTeX
   - LaTeX
   - Markdown
   - CSV
   - Excel
   - Word
   - PDF

**Expected Results:**
- ✅ All export buttons are visible
- ✅ Export downloads work
- ✅ File formats are correct
- ✅ Content is properly formatted
- ✅ No errors during export

**Priority:** P1 (High)

---

### 3. API Integration Testing

#### Test 3.1: Health Check Endpoint
**Objective:** Verify backend health  
**Steps:**
1. Navigate to `http://localhost:8080/health`
2. Check response

**Expected Results:**
- ✅ Status: "healthy" or "degraded"
- ✅ Service name is correct
- ✅ NIM availability is shown
- ✅ Timestamp is included

**Priority:** P0 (Critical)

---

#### Test 3.2: Research Endpoint
**Objective:** Verify research API works  
**Steps:**
1. Send POST request to `/research`
2. Include query and parameters
3. Check response

**Expected Results:**
- ✅ Request is accepted
- ✅ Response contains papers_analyzed
- ✅ Response contains common_themes
- ✅ Response contains contradictions
- ✅ Response contains research_gaps
- ✅ Response contains decisions
- ✅ Processing time is included

**Priority:** P0 (Critical)

---

#### Test 3.3: Sources Endpoint
**Objective:** Verify source status endpoint  
**Steps:**
1. Navigate to `http://localhost:8080/sources`
2. Check response

**Expected Results:**
- ✅ Active sources count is shown
- ✅ Source statuses are correct
- ✅ API key status is indicated
- ✅ Free vs subscription sources are separated

**Priority:** P1 (High)

---

### 4. Error Handling Testing

#### Test 4.1: Empty Query
**Objective:** Verify empty query handling  
**Steps:**
1. Leave query field empty
2. Try to submit

**Expected Results:**
- ✅ Validation error is shown
- ✅ Submit button is disabled or shows error
- ✅ User-friendly error message
- ✅ No backend request is sent

**Priority:** P0 (Critical)

---

#### Test 4.2: Invalid Date Range
**Objective:** Verify date validation  
**Steps:**
1. Set start year: 2030
2. Set end year: 2020
3. Try to submit

**Expected Results:**
- ✅ Validation error is shown
- ✅ Error message is clear
- ✅ Invalid dates are rejected

**Priority:** P1 (High)

---

#### Test 4.3: Backend Connection Failure
**Objective:** Verify graceful degradation  
**Steps:**
1. Stop backend server
2. Try to submit query
3. Check error handling

**Expected Results:**
- ✅ Error message is shown
- ✅ Error message is user-friendly
- ✅ Application doesn't crash
- ✅ User can retry

**Priority:** P0 (Critical)

---

#### Test 4.4: Timeout Handling
**Objective:** Verify timeout handling  
**Steps:**
1. Submit a very complex query
2. If timeout occurs, check handling

**Expected Results:**
- ✅ Timeout is handled gracefully
- ✅ Partial results are shown (if available)
- ✅ Error message indicates timeout
- ✅ User can retry with different parameters

**Priority:** P1 (High)

---

### 5. Performance Testing

#### Test 5.1: Query Response Time
**Objective:** Verify acceptable response times  
**Steps:**
1. Submit query with max_papers=5
2. Measure time to results
3. Submit query with max_papers=20
4. Measure time to results

**Expected Results:**
- ✅ Small queries (< 10 papers): < 2 minutes
- ✅ Medium queries (10-20 papers): < 5 minutes
- ✅ Large queries (> 20 papers): < 10 minutes
- ✅ Progress indicators are shown

**Priority:** P1 (High)

---

#### Test 5.2: UI Responsiveness
**Objective:** Verify UI remains responsive  
**Steps:**
1. Submit query
2. Interact with UI during processing
3. Check for lag or freezing

**Expected Results:**
- ✅ UI remains responsive during processing
- ✅ No freezing or lag
- ✅ Progress updates are shown
- ✅ User can cancel (if implemented)

**Priority:** P1 (High)

---

### 6. Accessibility Testing

#### Test 6.1: Keyboard Navigation
**Objective:** Verify keyboard accessibility  
**Steps:**
1. Navigate using only keyboard (Tab, Enter, Arrow keys)
2. Access all interactive elements
3. Submit query using keyboard

**Expected Results:**
- ✅ All interactive elements are keyboard accessible
- ✅ Focus indicators are visible
- ✅ Tab order is logical
- ✅ Forms can be submitted with keyboard

**Priority:** P2 (Medium)

---

#### Test 6.2: Screen Reader Compatibility
**Objective:** Verify screen reader support  
**Steps:**
1. Enable screen reader (VoiceOver on macOS)
2. Navigate through application
3. Check if content is readable

**Expected Results:**
- ✅ All text is readable
- ✅ Images have alt text
- ✅ Buttons have descriptive labels
- ✅ Form fields have labels

**Priority:** P2 (Medium)

---

#### Test 6.3: Color Contrast
**Objective:** Verify color contrast meets WCAG standards  
**Steps:**
1. Check text contrast on all backgrounds
2. Verify buttons are clearly visible
3. Check error messages are visible

**Expected Results:**
- ✅ Text meets WCAG AA contrast (4.5:1)
- ✅ Buttons have sufficient contrast
- ✅ Error messages are clearly visible
- ✅ Color is not the only indicator

**Priority:** P2 (Medium)

---

### 7. Responsive Design Testing

#### Test 7.1: Mobile Viewport
**Objective:** Verify mobile responsiveness  
**Steps:**
1. Resize browser to mobile size (375x667)
2. Check layout
3. Test interactions

**Expected Results:**
- ✅ Layout adapts to mobile
- ✅ Sidebar is accessible (hamburger menu)
- ✅ Text is readable
- ✅ Buttons are appropriately sized
- ✅ Forms are usable

**Priority:** P2 (Medium)

---

#### Test 7.2: Tablet Viewport
**Objective:** Verify tablet responsiveness  
**Steps:**
1. Resize browser to tablet size (768x1024)
2. Check layout
3. Test interactions

**Expected Results:**
- ✅ Layout adapts to tablet
- ✅ Content is readable
- ✅ Navigation is accessible
- ✅ Forms are usable

**Priority:** P2 (Medium)

---

#### Test 7.3: Desktop Viewport
**Objective:** Verify desktop layout  
**Steps:**
1. Use full desktop size (1920x1080)
2. Check layout
3. Verify no excessive whitespace

**Expected Results:**
- ✅ Layout uses space efficiently
- ✅ Content is centered or appropriately aligned
- ✅ No excessive whitespace
- ✅ Sidebar and main content are balanced

**Priority:** P1 (High)

---

### 8. Data Export Testing

#### Test 8.1: BibTeX Export
**Objective:** Verify BibTeX export works  
**Steps:**
1. Get results from query
2. Click BibTeX export button
3. Download and verify file

**Expected Results:**
- ✅ File downloads successfully
- ✅ File format is correct (.bib)
- ✅ BibTeX syntax is valid
- ✅ All papers are included

**Priority:** P1 (High)

---

#### Test 8.2: LaTeX Export
**Objective:** Verify LaTeX export works  
**Steps:**
1. Get results from query
2. Click LaTeX export button
3. Download and verify file

**Expected Results:**
- ✅ File downloads successfully
- ✅ File format is correct (.tex)
- ✅ LaTeX syntax is valid
- ✅ Document compiles (if tested)

**Priority:** P1 (High)

---

#### Test 8.3: Other Export Formats
**Objective:** Verify other export formats  
**Steps:**
1. Test CSV export
2. Test Excel export
3. Test Markdown export
4. Test Word export (if available)
5. Test PDF export (if available)

**Expected Results:**
- ✅ All export formats work
- ✅ Files download successfully
- ✅ Content is properly formatted
- ✅ No errors during export

**Priority:** P2 (Medium)

---

## Test Execution Checklist

### Pre-Testing
- [ ] Backend API is running on port 8080
- [ ] Web UI is running on port 8501
- [ ] Browser console is open (F12)
- [ ] Network tab is open in DevTools
- [ ] Test data is prepared

### During Testing
- [ ] Test each case systematically
- [ ] Document any issues found
- [ ] Take screenshots of errors
- [ ] Note performance metrics
- [ ] Check browser console for errors

### Post-Testing
- [ ] Document all findings
- [ ] Prioritize issues
- [ ] Create bug reports
- [ ] Suggest improvements

---

## Issue Tracking

### Issue Template
```
**Issue ID:** TEST-XXX
**Category:** [UI/UX | Functional | API | Error Handling | Performance | Accessibility | Responsive]
**Priority:** [P0 | P1 | P2]
**Severity:** [Critical | High | Medium | Low]
**Description:** 
**Steps to Reproduce:**
1. 
2. 
3. 
**Expected Result:**
**Actual Result:**
**Screenshots:** (if applicable)
**Browser/OS:** (if applicable)
```

---

## Success Criteria

### Must Have (P0)
- ✅ Application loads without errors
- ✅ Query submission works
- ✅ Results are displayed correctly
- ✅ Decision log is visible
- ✅ Basic error handling works
- ✅ Health check endpoint works

### Should Have (P1)
- ✅ Date filtering works
- ✅ Paper source selection works
- ✅ Export functionality works
- ✅ Acceptable response times
- ✅ UI remains responsive
- ✅ Desktop layout is optimal

### Nice to Have (P2)
- ✅ Keyboard navigation works
- ✅ Mobile responsiveness
- ✅ Screen reader compatibility
- ✅ All export formats work

---

## Notes

- Testing should be done in a clean environment
- Clear cache between test sessions if needed
- Test with both mock and real NIMs if available
- Document any workarounds or known issues
- Keep test data consistent for reproducibility


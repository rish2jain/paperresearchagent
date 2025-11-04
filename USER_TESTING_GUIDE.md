# 🧪 User Testing Guide - ResearchOps Agent

**Last Updated:** 2025-01-15  
**Version:** 2.0 (UX Enhancements Edition)  
**Purpose:** Comprehensive guide for testing all UX features and functionality  
**Deployment:** This guide assumes the ResearchOps Agent is deployed and running in Amazon EKS

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Testing the 15 UX Enhancements](#testing-the-15-ux-enhancements)
3. [Functional Testing](#functional-testing)
4. [Performance Testing](#performance-testing)
5. [Accessibility Testing](#accessibility-testing)
6. [Test Scenarios](#test-scenarios)
7. [Reporting Issues](#reporting-issues)

---

## 🚀 Quick Start

### Prerequisites

**Assumption:** The ResearchOps Agent is already deployed and running in your EKS cluster.

Verify deployment status:

```bash
# Check all pods are running
kubectl get pods -n research-ops

# Expected output should show all pods in Running state:
# NAME                                   READY   STATUS    RESTARTS   AGE
# reasoning-nim-xxx                      1/1     Running   0          5m
# embedding-nim-xxx                      1/1     Running   0          5m
# agent-orchestrator-xxx                 1/1     Running   0          5m
# web-ui-xxx                             1/1     Running   0          5m
# qdrant-xxx                             1/1     Running   0          5m
```

### Accessing Services

```bash
# Terminal 1: Port-forward Web UI
kubectl port-forward -n research-ops svc/web-ui 8501:8501

# Terminal 2: Port-forward API (optional, for direct API testing)
kubectl port-forward -n research-ops svc/agent-orchestrator 8080:8080
```

### Access Points

- **Web UI**: http://localhost:8501 (after port-forwarding)
- **API**: http://localhost:8080 (after port-forwarding)
- **API Docs**: http://localhost:8080/docs (after port-forwarding)

**Note:** If you have an Ingress controller configured, you may access services via the Ingress URL instead of port-forwarding. Check your Ingress configuration:

```bash
kubectl get ingress -n research-ops
```

### Quick Test

```bash
# Test API health (after port-forwarding)
curl http://localhost:8080/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "research-ops-agent",
#   "version": "1.0.0",
#   "nims_available": {
#     "reasoning_nim": true,
#     "embedding_nim": true
#   }
# }

# Test a research query
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning in healthcare",
    "max_papers": 10
  }'
```

### Troubleshooting Deployment Access

If you encounter issues accessing the services:

```bash
# 1. Verify all pods are running
kubectl get pods -n research-ops
# All should show STATUS: Running

# 2. Check pod logs if any pod is not running
kubectl logs -n research-ops <pod-name> --tail=50

# 3. Verify services are available
kubectl get svc -n research-ops

# 4. Check if port-forward is working
kubectl port-forward -n research-ops svc/web-ui 8501:8501 &
# Then test: curl http://localhost:8501

# 5. Verify NIMs are responding (from within cluster)
kubectl exec -n research-ops deployment/agent-orchestrator -- \
  curl http://reasoning-nim.research-ops.svc.cluster.local:8000/v1/health/live
kubectl exec -n research-ops deployment/agent-orchestrator -- \
  curl http://embedding-nim.research-ops.svc.cluster.local:8001/v1/health/live
```

For more detailed troubleshooting, see `docs/TROUBLESHOOTING.md` or `DEPLOYMENT.md`.

---

## 🎨 Testing the 15 UX Enhancements

### 1. Real-Time Multi-Agent Transparency ✅

**What to Test:**

- Agent activity panel is always visible
- Live status updates for all 4 agents
- Decision log shows reasoning
- NIM usage indicators

**Test Steps:**

1. Submit a query: "machine learning in healthcare"
2. Watch the agent panel in real-time
3. Verify each agent shows:
   - ✅ Scout: Paper search status
   - ✅ Analyst: Analysis progress
   - ✅ Synthesizer: Synthesis status
   - ✅ Coordinator: Quality checks

**Expected Results:**

- Panel remains visible throughout
- Updates happen in real-time
- Each decision shows reasoning
- NIM usage is clearly indicated

---

### 2. Results Gallery ✅

**What to Test:**

- Example syntheses are displayed
- Clickable "Try this query" buttons work
- Gallery shows themes, contradictions, gaps

**Test Steps:**

1. Look for "📚 Results Gallery" section
2. Click "Try this query" on any example
3. Verify query auto-fills in sidebar
4. Submit and see results

**Expected Results:**

- 3 example syntheses visible
- Clicking example fills query
- Results match expected format

---

### 3. Enhanced Information Management ✅

**What to Test:**

- Enhanced pagination for 50+ papers
- Items per page selector (10, 20, 50, 100)
- Jump to page functionality
- First/Prev/Next/Last navigation

**Test Steps:**

1. Submit query that returns 50+ papers
2. Check pagination controls appear
3. Test changing items per page
4. Test jumping to specific page
5. Test navigation buttons

**Expected Results:**

- Pagination appears automatically for 50+ papers
- All controls work smoothly
- Page numbers update correctly
- Navigation is intuitive

---

### 4. Repeat-Query Speed Demo ✅

**What to Test:**

- Cache speed comparison chart
- Notification when using cache
- Speed improvement percentage shown

**Test Steps:**

1. Submit query: "artificial intelligence ethics"
2. Note the processing time
3. Submit the SAME query again
4. Check for cache notification
5. Look for speed comparison chart

**Expected Results:**

- Notification: "⚡ Using cached results"
- Speed comparison shows ~95% improvement
- Chart displays fresh vs cached time
- Visual comparison is clear

---

### 5. Session Stats Dashboard ✅

**What to Test:**

- Statistics displayed in sidebar
- Queries run count
- Papers analyzed count
- Agent decisions count
- Cached results count

**Test Steps:**

1. Check sidebar for "📊 Session Stats"
2. Run 2-3 queries
3. Watch stats update
4. Check detailed analytics

**Expected Results:**

- Stats update after each query
- All metrics are accurate
- Detailed view shows breakdown
- Session persists across queries

---

### 6. First-Run Guided Tour ✅

**What to Test:**

- Welcome modal appears for first-time users
- Tour explains agent roles
- Skip option works
- Tour doesn't appear after completion

**Test Steps:**

1. Ensure Web UI is port-forwarded: `kubectl port-forward -n research-ops svc/web-ui 8501:8501`
2. Clear browser cache/localStorage
3. Visit http://localhost:8501
4. Check for welcome modal
5. Complete or skip tour
6. Refresh and verify tour doesn't reappear

**Expected Results:**

- Modal appears on first visit
- Agent explanations are clear
- Skip button works
- Tour completion is remembered

---

### 7. Enhanced Loading Animations ✅

**What to Test:**

- Humanized progress messages
- Stage-specific animations
- Time estimates
- Agent narrative messages

**Test Steps:**

1. Submit a query
2. Watch loading animations
3. Verify messages change per stage:
   - "Searching databases..."
   - "Analyzing papers..."
   - "Synthesizing findings..."
   - "Ensuring quality..."

**Expected Results:**

- Messages are humanized (not technical)
- Progress is clearly indicated
- Time estimates are shown
- Animations are smooth

---

### 8. User Preferences & Settings ✅

**What to Test:**

- Settings panel in sidebar
- Default max papers setting
- Default export format
- Items per page preference
- High contrast mode
- Notification preferences

**Test Steps:**

1. Open "⚙️ User Preferences" in sidebar
2. Change default max papers to 20
3. Set default export format to Markdown
4. Enable high contrast mode
5. Save preferences
6. Submit new query and verify settings applied

**Expected Results:**

- Settings persist across sessions
- Defaults are applied to new queries
- High contrast mode changes UI
- All preferences save correctly

---

### 9. Synthesis History Dashboard ✅

**What to Test:**

- View previous syntheses
- Search and filter history
- Sort by recent, query, papers count
- View and compare buttons

**Test Steps:**

1. Run 3-4 different queries
2. Open "📚 Synthesis History" in sidebar
3. Verify all queries appear
4. Test search/filter
5. Test sorting options
6. Click "View" on a previous query

**Expected Results:**

- All queries appear in history
- Search/filter works
- Sorting works correctly
- View button loads previous results

---

### 10. Quick Export Panel ✅

**What to Test:**

- Single-click export buttons
- PDF, Markdown, Word, BibTeX, JSON
- Downloads work correctly
- Export formats are valid

**Test Steps:**

1. Complete a research query
2. Find "Quick Export" panel in results
3. Click each export button:
   - 📄 Markdown
   - 📋 JSON
   - 📚 BibTeX
4. Verify downloads work
5. Check file contents are valid

**Expected Results:**

- All export buttons work
- Files download correctly
- Content is properly formatted
- File names are descriptive

---

### 11. AI-Powered Suggestions ✅

**What to Test:**

- Post-synthesis suggestions appear
- 4 suggestion types available
- Action buttons work

**Test Steps:**

1. Complete a research query
2. Look for "AI Suggestions" section
3. Verify suggestions include:
   - Generate Hypothesis
   - Draft Grant Proposal
   - Create Literature Review
   - Compare with Previous
4. Click action buttons

**Expected Results:**

- Suggestions are relevant to query
- All 4 types appear (when applicable)
- Action buttons trigger next steps
- Suggestions are helpful

---

### 12. Citation Management Export ✅

**What to Test:**

- Export to Zotero (RIS format)
- Export to Mendeley (CSV format)
- LaTeX/BibTeX integration
- Export formats are correct

**Test Steps:**

1. Complete a research query
2. Find "Citation Management" section
3. Click "Export to Zotero"
4. Download RIS file
5. Import into Zotero (if available)
6. Verify all papers import correctly

**Expected Results:**

- RIS file downloads
- CSV file downloads
- Formats are standard-compliant
- Papers import correctly into tools

---

### 13. Accessibility Features ✅

**What to Test:**

- High contrast mode
- Keyboard shortcuts
- Screen reader support
- ARIA labels

**Test Steps:**

1. Open "♿ Accessibility" in sidebar
2. Enable high contrast mode
3. Verify UI changes
4. Check keyboard shortcuts list
5. Test keyboard navigation:
   - Tab through elements
   - Enter to submit
   - Escape to close modals

**Expected Results:**

- High contrast mode works
- Keyboard shortcuts documented
- Navigation is keyboard-accessible
- Screen reader compatible

---

### 14. Enhanced Error Handling ✅

**What to Test:**

- Contextual error messages
- Error-specific help
- Technical details in expandable section
- Solution suggestions

**Test Steps:**

1. Try submitting query with invalid date range
2. Try query with no results
3. Test network interruption (stop port-forward temporarily)
4. Check error messages for user-friendly guidance

**Expected Results:**

- Errors are user-friendly
- Help is provided
- Technical details available
- Solutions are suggested

---

### 15. Real-Time Notifications ✅

**What to Test:**

- Toast notifications appear
- Notifications for discoveries
- Notification panel in sidebar
- Clear all functionality

**Test Steps:**

1. Submit a query
2. Watch for notifications:
   - Scout paper findings
   - Synthesizer discoveries
   - Contradictions found
   - Themes identified
3. Check notification panel in sidebar
4. Test "Clear all" button

**Expected Results:**

- Notifications appear automatically
- Types are color-coded (success/warning/info)
- Panel shows history
- Clear all works

---

## 🔧 Functional Testing

### Basic Research Query

**Test:**

1. Open Web UI at http://localhost:8501 (after port-forwarding)
2. Enter query: "machine learning in healthcare"
3. Set Max Papers: 10
4. Set Date Range: 2020-2024
5. Ensure all sources are enabled
6. Click "🚀 Start Research"

**Expected:**

- ✅ Results returned in 30-120 seconds
- ✅ Papers from multiple sources
- ✅ Synthesis includes themes, contradictions, gaps
- ✅ All agents show decisions in real-time

### Advanced Query

**Test:**

1. In Web UI, enter query: "quantum computing AND cryptography"
2. Set Max Papers: 25
3. Set Date Range: 2023-2024
4. Select sources: arXiv, PubMed, Semantic Scholar
5. Submit query

**Expected:**

- ✅ Boolean operators work
- ✅ Date filtering works
- ✅ Source selection works
- ✅ Results are relevant

### Export Functionality

**Test:**

1. Complete query
2. Export to:
   - Markdown ✅
   - JSON ✅
   - BibTeX ✅
   - RIS ✅
   - CSV ✅

**Expected:**

- ✅ All formats download
- ✅ Content is valid
- ✅ File names are descriptive

---

## ⚡ Performance Testing

### Response Times

**Targets:**

- Initial page load: < 2 seconds
- Query submission: < 5 seconds (acknowledgment)
- Results display: 30-120 seconds (depending on query)
- Cached queries: < 2 seconds

**Test:**

```bash
# Ensure API is port-forwarded first
# kubectl port-forward -n research-ops svc/agent-orchestrator 8080:8080

# Time first query
time curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "max_papers": 10}'

# Time cached query (same parameters)
time curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "max_papers": 10}'
```

### Large Dataset Handling

**Test:**

- Query returning 100+ papers
- Verify pagination works
- Check performance doesn't degrade
- Verify smooth scrolling

---

## ♿ Accessibility Testing

### Keyboard Navigation

**Test:**

1. Tab through all interactive elements
2. Enter to activate buttons
3. Escape to close modals
4. Arrow keys for navigation

**Expected:**

- ✅ All elements are reachable
- ✅ Focus indicators are visible
- ✅ Navigation is logical

### Screen Reader

**Test:**

- Enable screen reader (VoiceOver, NVDA, JAWS)
- Navigate through UI
- Verify ARIA labels are present
- Check announcements are made

**Expected:**

- ✅ All elements are announced
- ✅ Labels are descriptive
- ✅ Live regions update

### High Contrast Mode

**Test:**

1. Enable high contrast mode
2. Verify all text is readable
3. Check contrast ratios meet WCAG AA
4. Verify icons remain visible

**Expected:**

- ✅ Text is readable
- ✅ Contrast is sufficient
- ✅ UI remains functional

---

## 📝 Test Scenarios

### Scenario 1: First-Time User

**Goal:** Verify onboarding experience

**Steps:**

1. Visit application for first time
2. Complete guided tour
3. Submit first query
4. Explore results
5. Try export

**Success Criteria:**

- ✅ Tour completes without errors
- ✅ First query succeeds
- ✅ Results are understandable
- ✅ Export works

---

### Scenario 2: Power User

**Goal:** Verify advanced features

**Steps:**

1. Set preferences
2. Submit complex query
3. Use advanced filters
4. Export multiple formats
5. Review history
6. Compare results

**Success Criteria:**

- ✅ Preferences persist
- ✅ Complex queries work
- ✅ All exports work
- ✅ History is accessible

---

### Scenario 3: Researcher Workflow

**Goal:** Verify complete research workflow

**Steps:**

1. Submit query: "gene therapy for cancer"
2. Review agent decisions
3. Check for contradictions
4. Export to BibTeX
5. Use AI suggestions
6. Compare with previous query

**Success Criteria:**

- ✅ Complete workflow works
- ✅ All features accessible
- ✅ Exports are usable
- ✅ Suggestions are helpful

---

## 🐛 Reporting Issues

### Issue Template

```markdown
**Feature:** [Which UX enhancement?]
**Severity:** [Critical/High/Medium/Low]
**Steps to Reproduce:**

1.
2.
3.

**Expected Behavior:**

- **Actual Behavior:**

- **Screenshots:** (if applicable)

  **Browser/OS:**
  **URL:**
  **Timestamp:**
```

### Test Results Template

```markdown
## Test Results - [Date]

### Tested Features

- [ ] Real-Time Agent Panel
- [ ] Results Gallery
- [ ] Enhanced Pagination
- [ ] Cache Speed Demo
- [ ] Session Stats
- [ ] Guided Tour
- [ ] Loading Animations
- [ ] User Preferences
- [ ] History Dashboard
- [ ] Quick Export
- [ ] AI Suggestions
- [ ] Citation Export
- [ ] Accessibility
- [ ] Error Handling
- [ ] Notifications

### Issues Found

1. [Issue description]
2. [Issue description]

### Performance

- First Query: [time]
- Cached Query: [time]
- Page Load: [time]

### Overall Assessment

[Rating: 1-5 stars]
[Comments]
```

---

## 📊 Test Checklist

### Pre-Testing Setup

- [ ] EKS cluster deployed and all pods running (`kubectl get pods -n research-ops`)
- [ ] Web UI port-forwarded (`kubectl port-forward -n research-ops svc/web-ui 8501:8501`)
- [ ] API port-forwarded if needed (`kubectl port-forward -n research-ops svc/agent-orchestrator 8080:8080`)
- [ ] Browser cache cleared
- [ ] Verify NIMs are healthy (check health endpoint)

### Core Features

- [ ] Query submission works
- [ ] Results display correctly
- [ ] Agent decisions visible
- [ ] Export functions work

### UX Enhancements

- [ ] All 15 features accessible
- [ ] All features functional
- [ ] Performance acceptable
- [ ] Accessibility verified

### Edge Cases

- [ ] Empty results handled
- [ ] Error states handled
- [ ] Large datasets handled
- [ ] Network issues handled

---

## 🎯 Success Criteria

### Must Have (P0)

- ✅ Application loads without errors
- ✅ All 15 UX enhancements accessible
- ✅ Core functionality works
- ✅ Basic error handling works

### Should Have (P1)

- ✅ All features functional
- ✅ Performance meets targets
- ✅ Accessibility verified
- ✅ Export formats work

### Nice to Have (P2)

- ✅ Smooth animations
- ✅ Intuitive navigation
- ✅ Helpful error messages
- ✅ Comprehensive documentation

---

## 📚 Additional Resources

- **Judge Testing Guide**: `hackathon_submission/JUDGE_TESTING_GUIDE.md`
- **Technical Review**: `hackathon_submission/TECHNICAL_REVIEW.md`
- **UX Showcase**: `hackathon_submission/UX_SHOWCASE.md`
- **API Documentation**: http://localhost:8080/docs (after port-forwarding)
- **Deployment Guide**: `DEPLOYMENT.md` - EKS deployment instructions
- **Troubleshooting**: `docs/TROUBLESHOOTING.md` - Common issues and solutions

---

## 💡 Tips for Testers

### EKS-Specific Tips

1. **Keep Port-Forwards Active**: Ensure port-forward commands remain running in separate terminals during testing
2. **Monitor Pod Health**: Periodically check `kubectl get pods -n research-ops` to ensure all services remain healthy
3. **Check Logs if Issues Occur**: Use `kubectl logs -n research-ops <pod-name>` to debug problems
4. **Verify NIM Availability**: Ensure both Reasoning and Embedding NIMs show as available in health checks

### General Testing Tips

1. **Test in Different Browsers**: Chrome, Firefox, Safari
2. **Test Different Screen Sizes**: Desktop, tablet, mobile
3. **Test with Real Queries**: Use actual research questions
4. **Document Everything**: Take notes, screenshots, videos
5. **Test Edge Cases**: Empty queries, very long queries, special characters
6. **Verify Accessibility**: Use keyboard navigation, screen readers
7. **Check Performance**: Monitor response times (expect 30-120 seconds for first-time queries)
8. **Test Error States**: Stop port-forwards temporarily, use invalid inputs
9. **Monitor Resource Usage**: Check GPU/node resources if queries are slow: `kubectl top nodes`

---

## 🎉 Happy Testing!

We hope you have a great testing experience!

For questions or issues, refer to:

- `TESTING_GUIDE.md` - General testing guide
- `docs/TROUBLESHOOTING.md` - Common issues and solutions
- `hackathon_submission/JUDGE_TESTING_GUIDE.md` - Judge-specific testing

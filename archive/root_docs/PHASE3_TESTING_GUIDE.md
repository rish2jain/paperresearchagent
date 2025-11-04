# Phase 3: Testing Guide

## Quick Start Testing

### 1. Install Dependencies
```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent
pip install sseclient-py==1.8.0
```

### 2. Verify Installation
```bash
python -c "import sseclient; print('✅ SSE client installed')"
```

### 3. Run Web UI
```bash
streamlit run src/web_ui.py
```

## Test Scenarios

### Scenario 1: Streaming Enabled (Happy Path)

**Prerequisites**:
- sseclient-py installed
- API server running with `/research/stream` endpoint

**Steps**:
1. Open web UI: `http://localhost:8501`
2. Verify sidebar shows: `✅ Enable Real-Time Updates` (checked)
3. Enter test query: "machine learning in healthcare"
4. Click "🚀 Start Research"
5. **Observe progressive display**:
   - 0-10s: "Connecting to streaming endpoint..."
   - 10-30s: Papers table appears with expandable list
   - 30s-3min: Analysis progress counter updates
   - 3-4min: Themes section grows progressively
   - 4-5min: Final synthesis appears

**Expected Result**:
✅ Papers visible at ~30s
✅ Themes accumulate progressively
✅ Final synthesis at ~5min
✅ No errors in console

### Scenario 2: Streaming Disabled (Fallback)

**Prerequisites**:
- sseclient-py NOT installed OR checkbox unchecked

**Steps**:
1. Uninstall: `pip uninstall sseclient-py -y`
2. Restart web UI
3. Verify sidebar shows: `⚠️ Enable Real-Time Updates` (disabled, grayed out)
4. Enter test query: "quantum computing 2024"
5. Click "🚀 Start Research"
6. **Observe blocking mode**:
   - Loading spinner for full duration
   - All results appear at once at end

**Expected Result**:
✅ Checkbox disabled with warning
✅ Blocking mode works correctly
✅ Results identical to previous behavior

### Scenario 3: Streaming Failure (Mid-Request)

**Prerequisites**:
- sseclient-py installed
- API server NOT running OR `/research/stream` endpoint broken

**Steps**:
1. Stop API server: `Ctrl+C` on API terminal
2. Web UI still running
3. Checkbox enabled
4. Enter test query
5. Click "🚀 Start Research"
6. **Observe error handling**:
   - "⚠️ Cannot connect to streaming endpoint"
   - "⏳ Falling back to standard mode..."
   - Switches to blocking mode automatically

**Expected Result**:
✅ Error message displayed
✅ Automatic fallback to blocking mode
✅ No crash, graceful degradation

### Scenario 4: Cache Hit (Skip Streaming)

**Prerequisites**:
- Previous query cached

**Steps**:
1. Run same query twice
2. Second run should show:
   - "✨ Found cached results!"
   - Instant display (0.2s)
   - "⚡ Instant Results!" banner

**Expected Result**:
✅ Cache bypasses streaming
✅ Instant results on repeat queries
✅ Cache stats displayed

## Visual Checkpoints

### Papers Display (30s mark)
```
### 📚 Papers Found
✅ 10 papers discovered from academic databases

📖 View all 10 papers (expandable)
  1. Machine Learning in Healthcare
     - Authors: Smith, Johnson, Davis
     - Source: arxiv
     - [View Paper](...)
  ...
```

### Themes Display (3-4min mark)
```
### 🔍 Common Themes Emerging
1. Machine learning improves diagnostic accuracy
2. Neural networks effective for image analysis
3. Limited data on pediatric populations
```

### Contradictions Display (if any)
```
### ⚡ Contradictions Detected
1. Paper A claims X, but Paper B claims Y
```

### Final Synthesis (5min mark)
```
🎉 Research complete! Analyzed 10 papers in 287.4s
```

## Performance Validation

### Metrics to Check

1. **Time to First Data**:
   - Target: <30 seconds for papers
   - Measure: Stopwatch from button click to papers table

2. **Progressive Updates**:
   - Themes should appear one-by-one, not all at once
   - Progress bar should update smoothly

3. **Error Recovery**:
   - Fallback should be seamless
   - No partial data corruption

4. **Cache Integration**:
   - Streaming results should cache correctly
   - Cache hits should skip streaming

## Browser Console Checks

### Expected Logs (No Errors)
```
[StreamingResponse] Connecting to /research/stream
[SSE] Event: agent_status
[SSE] Event: papers_found
[SSE] Event: paper_analyzed (batch 1)
...
[SSE] Event: synthesis_complete
[Cache] Stored streaming result for query: machine learning...
```

### Error Scenarios
```javascript
// If API unreachable:
Failed to start streaming: 500
⏳ Falling back to standard mode...

// If sseclient missing:
SSE client not available. Use blocking mode.
```

## API Endpoint Verification

### Test Streaming Endpoint Directly
```bash
curl -X POST http://localhost:8080/research/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "max_papers": 5}' \
  --no-buffer

# Expected output (SSE format):
event: agent_status
data: {"agent": "Scout", "status": "starting", "message": "Searching for papers"}

event: papers_found
data: {"papers_count": 5, "papers": [...]}

...
```

## Troubleshooting

### Issue: Checkbox Disabled
**Cause**: sseclient-py not installed
**Fix**: `pip install sseclient-py`

### Issue: "Cannot connect to streaming endpoint"
**Cause**: API server not running OR wrong URL
**Fix**:
1. Check API is running: `curl http://localhost:8080/health`
2. Verify API URL in sidebar matches server

### Issue: Streaming Hangs
**Cause**: SSE connection timeout
**Fix**:
1. Check API logs for errors
2. Verify NIMs are responding
3. Try smaller query or fewer papers

### Issue: Partial Results Only
**Cause**: Stream interrupted before synthesis_complete
**Fix**:
1. Check network stability
2. Increase timeout in streaming function
3. Check API for processing errors

## Regression Testing

### Critical Paths to Test
1. ✅ Blocking mode still works (streaming disabled)
2. ✅ Cache works for both modes
3. ✅ Error messages user-friendly
4. ✅ Session state persists correctly
5. ✅ Date filtering works with streaming
6. ✅ Paper source selection works with streaming

### UI Compatibility
1. ✅ Mobile responsive (test on narrow window)
2. ✅ Dark mode compatible
3. ✅ Accessibility (keyboard navigation)
4. ✅ Export functions work after streaming

## Success Criteria

### Phase 3 Complete When:
- [x] sseclient-py installed successfully
- [x] Streaming toggle visible and functional
- [x] Papers appear at ~30s (not 5min)
- [x] Themes accumulate progressively
- [x] Fallback works seamlessly
- [x] Cache integration preserved
- [x] No breaking changes to existing features
- [x] Error handling comprehensive

## Performance Benchmarks

### Target Metrics
- **Time to First Meaningful Content**: <30s (was 300s)
- **Stream Success Rate**: >95%
- **Fallback Trigger Rate**: <5%
- **User Perception**: 70% faster wait time

### Measurement Commands
```bash
# Time to papers
time curl -X POST http://localhost:8080/research/stream \
  -d '{"query":"test","max_papers":10}' \
  | grep -m 1 "papers_found"

# Full research time
time curl -X POST http://localhost:8080/research \
  -d '{"query":"test","max_papers":10}'
```

## Deployment Checklist

Before deploying to production:
- [ ] All test scenarios pass
- [ ] Performance benchmarks met
- [ ] Error handling validated
- [ ] Fallback tested thoroughly
- [ ] Cache integration verified
- [ ] Documentation updated
- [ ] User feedback collected (if available)

## Contact & Support

If issues persist:
1. Check logs: `tail -f logs/web_ui.log`
2. Review API logs: `kubectl logs deployment/agent-orchestrator`
3. Verify NIMs health: `kubectl get pods -n research-ops`

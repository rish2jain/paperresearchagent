# Web UI Progressive Synthesis Implementation Guide

**Target:** Add real-time progressive insight visualization to Streamlit web UI

**Challenge:** Streamlit doesn't natively support Server-Sent Events (SSE)

**Solution:** Hybrid approach using JavaScript + Streamlit components

---

## Implementation Strategy

### Option 1: JavaScript SSE Client + Streamlit State (RECOMMENDED)

Use Streamlit's `components.html()` to embed JavaScript SSE client that updates Streamlit state.

**Pros:**
- Real-time updates
- Clean separation of concerns
- Leverages native browser EventSource API

**Cons:**
- Requires JavaScript code
- Slightly more complex integration

### Option 2: Polling Approach (SIMPLER)

Use standard HTTP polling with Streamlit auto-rerun.

**Pros:**
- No JavaScript required
- Simpler implementation

**Cons:**
- Higher latency
- More server load
- Not true streaming

---

## Option 1 Implementation (Recommended)

### Step 1: Create SSE JavaScript Component

**File:** `src/components/sse_client.html`

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        #sse-status {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .connected { background-color: #d4edda; color: #155724; }
        .connecting { background-color: #fff3cd; color: #856404; }
        .disconnected { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div id="sse-status" class="connecting">Connecting to research stream...</div>
    <div id="events-container"></div>

    <script>
        // Get parameters from Streamlit
        const urlParams = new URLSearchParams(window.location.search);
        const apiUrl = urlParams.get('api_url') || 'http://localhost:8080';
        const query = urlParams.get('query');
        const maxPapers = urlParams.get('max_papers') || 10;

        // Connect to SSE endpoint
        const eventSource = new EventSource(
            `${apiUrl}/research/stream?query=${encodeURIComponent(query)}&max_papers=${maxPapers}`
        );

        const statusDiv = document.getElementById('sse-status');
        const eventsContainer = document.getElementById('events-container');

        // Track state
        let state = {
            papers_found: 0,
            papers_analyzed: 0,
            themes: [],
            contradictions: [],
            gaps: [],
            discoveries: []
        };

        eventSource.onopen = function() {
            statusDiv.textContent = 'Connected to research stream';
            statusDiv.className = 'connected';
        };

        eventSource.onerror = function() {
            statusDiv.textContent = 'Disconnected from research stream';
            statusDiv.className = 'disconnected';
            eventSource.close();
        };

        // Handle agent_status events
        eventSource.addEventListener('agent_status', function(e) {
            const data = JSON.parse(e.data);
            addEvent('status', `${data.agent}: ${data.message}`);
        });

        // Handle papers_found events
        eventSource.addEventListener('papers_found', function(e) {
            const data = JSON.parse(e.data);
            state.papers_found = data.papers_count;
            addEvent('papers', `Found ${data.papers_count} papers`);
            updateStreamlitState();
        });

        // Handle paper_analyzed events
        eventSource.addEventListener('paper_analyzed', function(e) {
            const data = JSON.parse(e.data);
            state.papers_analyzed = data.paper_number;
            addEvent('analysis', `Analyzed paper ${data.paper_number}/${data.total}: ${data.title}`);
            updateStreamlitState();
        });

        // Handle theme_emerging events
        eventSource.addEventListener('theme_emerging', function(e) {
            const data = JSON.parse(e.data);
            state.themes.push({
                name: data.theme_name,
                confidence: data.confidence,
                paper_number: data.paper_number
            });
            state.discoveries.push({
                type: 'theme_emerging',
                timestamp: new Date().toISOString(),
                data: data
            });
            addEvent('theme', `🎯 New theme: "${data.theme_name}" (confidence: ${(data.confidence*100).toFixed(0)}%)`);
            updateStreamlitState();
        });

        // Handle theme_strengthened events
        eventSource.addEventListener('theme_strengthened', function(e) {
            const data = JSON.parse(e.data);
            state.discoveries.push({
                type: 'theme_strengthened',
                timestamp: new Date().toISOString(),
                data: data
            });
            addEvent('theme', `📈 Theme strengthened: "${data.theme_name}" (${(data.old_confidence*100).toFixed(0)}% → ${(data.new_confidence*100).toFixed(0)}%)`);
            updateStreamlitState();
        });

        // Handle contradiction_discovered events
        eventSource.addEventListener('contradiction_discovered', function(e) {
            const data = JSON.parse(e.data);
            state.contradictions.push(data);
            state.discoveries.push({
                type: 'contradiction_discovered',
                timestamp: new Date().toISOString(),
                data: data
            });
            addEvent('contradiction', `⚠️ Contradiction: ${data.explanation.substring(0, 100)}...`);
            updateStreamlitState();
        });

        // Handle synthesis_complete events
        eventSource.addEventListener('synthesis_complete', function(e) {
            const data = JSON.parse(e.data);
            state.complete = true;
            state.final_results = data;
            addEvent('complete', '✅ Research synthesis complete!');
            updateStreamlitState();
            eventSource.close();
        });

        function addEvent(type, message) {
            const eventDiv = document.createElement('div');
            eventDiv.className = `event event-${type}`;
            eventDiv.textContent = `${new Date().toLocaleTimeString()}: ${message}`;
            eventsContainer.appendChild(eventDiv);
            eventsContainer.scrollTop = eventsContainer.scrollHeight;
        }

        function updateStreamlitState() {
            // Send state to Streamlit via postMessage
            window.parent.postMessage({
                type: 'streamlit:componentValue',
                value: state
            }, '*');
        }
    </script>
</body>
</html>
```

### Step 2: Create Streamlit Component Wrapper

**File:** `src/components/sse_component.py`

```python
import streamlit.components.v1 as components
from pathlib import Path

def sse_research_stream(api_url: str, query: str, max_papers: int = 10):
    """
    Render SSE client component for progressive research visualization.

    Returns:
        dict: Current state of research progress
    """
    component_path = Path(__file__).parent / "sse_client.html"

    component_value = components.html(
        component_path.read_text(),
        height=600,
        scrolling=True
    )

    return component_value or {}
```

### Step 3: Update Main Web UI

**File:** `src/web_ui.py`

Add these imports:

```python
import plotly.graph_objects as go
import plotly.express as px
from components.sse_component import sse_research_stream
```

Replace the current research submission section with:

```python
def render_progressive_research():
    """Render progressive research interface with real-time updates."""
    session = SessionManager.get()

    st.header("🔬 Research Query")

    # Query input
    query = st.text_input(
        "What would you like to research?",
        value=session.query,
        placeholder="e.g., quantum computing applications in cryptography"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        max_papers = st.slider("Maximum papers to analyze", 5, 50, session.max_papers)
    with col2:
        use_streaming = st.checkbox("Enable streaming", value=True)

    if st.button("Start Research", type="primary"):
        if not query:
            st.warning("Please enter a research question")
            return

        session.query = query
        session.max_papers = max_papers
        SessionManager.update(session)

        if use_streaming:
            render_streaming_research(query, max_papers)
        else:
            render_batch_research(query, max_papers)


def render_streaming_research(query: str, max_papers: int):
    """Render progressive research with SSE streaming."""
    st.subheader("📡 Live Research Progress")

    # Create container for live updates
    progress_container = st.container()
    insights_container = st.container()
    themes_container = st.container()
    contradictions_container = st.container()

    # Initialize SSE client component
    api_url = os.getenv("API_URL", "http://localhost:8080")

    with progress_container:
        state = sse_research_stream(api_url, query, max_papers)

    if not state:
        st.info("Connecting to research stream...")
        return

    # Render live insights feed
    with insights_container:
        render_live_insights_feed(state.get("discoveries", []))

    # Render theme evolution chart
    with themes_container:
        if state.get("themes"):
            render_theme_evolution_chart(state["themes"])

    # Render contradictions
    with contradictions_container:
        if state.get("contradictions"):
            render_contradictions_view(state["contradictions"])

    # Show completion status
    if state.get("complete"):
        st.success(f"✅ Research complete! Analyzed {state['papers_analyzed']} papers")
        render_final_results(state["final_results"])


def render_live_insights_feed(discoveries: list):
    """Render Twitter-like feed of discoveries."""
    st.subheader("🌊 Live Insight Feed")

    if not discoveries:
        st.info("Waiting for discoveries...")
        return

    # Show most recent discoveries first
    for discovery in reversed(discoveries[-10:]):  # Show last 10
        timestamp = datetime.fromisoformat(discovery["timestamp"].replace("Z", "+00:00"))
        time_ago = (datetime.now(timestamp.tzinfo) - timestamp).total_seconds()

        if time_ago < 60:
            time_str = f"{int(time_ago)}s ago"
        elif time_ago < 3600:
            time_str = f"{int(time_ago/60)}m ago"
        else:
            time_str = f"{int(time_ago/3600)}h ago"

        discovery_type = discovery["type"]
        data = discovery["data"]

        if discovery_type == "theme_emerging":
            with st.container():
                st.markdown(f"""
                **🎯 New Theme Discovered** • {time_str}
                - **{data['theme_name']}**
                - Confidence: {data['confidence']*100:.0%}
                - First seen in paper #{data['paper_number']}
                """)

        elif discovery_type == "theme_strengthened":
            with st.container():
                confidence_change = (data['new_confidence'] - data['old_confidence']) * 100
                st.markdown(f"""
                **📈 Theme Strengthened** • {time_str}
                - **{data['theme_name']}**
                - Confidence: {data['old_confidence']*100:.0%} → {data['new_confidence']*100:.0%} (+{confidence_change:.0%})
                - Supporting evidence from paper #{data['paper_number']}
                """)

        elif discovery_type == "contradiction_discovered":
            with st.container():
                st.markdown(f"""
                **⚠️ Contradiction Found** • {time_str}
                - {data['explanation']}
                - Severity: {data['severity']}
                - Detected at paper #{data['paper_number']}
                """)


def render_theme_evolution_chart(themes: list):
    """Render Plotly chart showing theme confidence evolution."""
    st.subheader("📊 Theme Evolution")

    # Group themes by name to track evolution
    theme_history = {}
    for theme in themes:
        name = theme['name']
        if name not in theme_history:
            theme_history[name] = []
        theme_history[name].append({
            'paper': theme['paper_number'],
            'confidence': theme['confidence']
        })

    # Create Plotly figure
    fig = go.Figure()

    for theme_name, history in theme_history.items():
        papers = [h['paper'] for h in history]
        confidences = [h['confidence'] for h in history]

        fig.add_trace(go.Scatter(
            x=papers,
            y=confidences,
            mode='lines+markers',
            name=theme_name,
            hovertemplate=(
                f"<b>{theme_name}</b><br>"
                "Paper: %{x}<br>"
                "Confidence: %{y:.0%}<br>"
                "<extra></extra>"
            )
        ))

    fig.update_layout(
        title="Theme Confidence Over Time",
        xaxis_title="Papers Analyzed",
        yaxis_title="Confidence",
        yaxis=dict(tickformat=".0%"),
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


def render_contradictions_view(contradictions: list):
    """Render side-by-side view of contradictions."""
    st.subheader("⚠️ Contradictions Discovered")

    for idx, contradiction in enumerate(contradictions):
        with st.expander(f"Contradiction #{idx+1}: {contradiction['explanation'][:100]}..."):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Finding A:**")
                st.info(contradiction['finding_a'])

            with col2:
                st.markdown("**Finding B:**")
                st.warning(contradiction['finding_b'])

            st.markdown(f"**Explanation:** {contradiction['explanation']}")
            st.markdown(f"**Severity:** {contradiction['severity']}")


def render_final_results(results: dict):
    """Render final comprehensive results."""
    st.subheader("🎯 Final Synthesis")

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Themes", "Contradictions", "Research Gaps"])

    with tab1:
        st.markdown("### Common Themes")
        for idx, theme in enumerate(results.get("common_themes", [])):
            st.markdown(f"{idx+1}. {theme}")

    with tab2:
        st.markdown("### Contradictions")
        for contradiction in results.get("contradictions", []):
            with st.expander(contradiction.get("explanation", "")[:100]):
                st.json(contradiction)

    with tab3:
        st.markdown("### Research Gaps")
        for idx, gap in enumerate(results.get("research_gaps", [])):
            st.markdown(f"{idx+1}. {gap}")
```

---

## Testing Strategy

### Test 1: SSE Connection

```bash
# Terminal 1: Start API
uvicorn src.api:app --reload --port 8080

# Terminal 2: Test SSE endpoint
curl -N http://localhost:8080/research/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "max_papers": 5}'
```

**Expected:** Stream of SSE events

### Test 2: Streamlit Integration

```bash
# Start Streamlit UI
streamlit run src/web_ui.py

# Submit research query with streaming enabled
# Verify:
# - Live insight feed updates in real-time
# - Theme evolution chart updates
# - Contradictions appear as discovered
```

### Test 3: Error Handling

```bash
# Stop API while stream is running
# Verify:
# - "Disconnected" status shown
# - Partial results preserved
# - No crashes
```

---

## Performance Optimization

### JavaScript State Updates

Batch updates to avoid overwhelming Streamlit:

```javascript
let updatePending = false;

function updateStreamlitState() {
    if (updatePending) return;

    updatePending = true;
    setTimeout(() => {
        window.parent.postMessage({
            type: 'streamlit:componentValue',
            value: state
        }, '*');
        updatePending = false;
    }, 500);  // Batch updates every 500ms
}
```

### Streamlit Auto-Rerun Control

Use `st.empty()` containers to update specific sections:

```python
status_placeholder = st.empty()
insights_placeholder = st.empty()

# Update only these sections, not entire page
with status_placeholder:
    st.info(f"Analyzing paper {state['papers_analyzed']}/{state['papers_found']}")

with insights_placeholder:
    render_live_insights_feed(state["discoveries"])
```

---

## Alternative: Simplified Polling Approach

If SSE proves too complex, use simple polling:

```python
def render_polling_research(query: str, max_papers: int):
    """Simpler polling-based progress updates."""
    # Submit research request
    response = requests.post(
        f"{api_url}/research",
        json={"query": query, "max_papers": max_papers}
    )
    session_id = response.json()["session_id"]

    # Poll for progress
    progress_bar = st.progress(0)
    status_text = st.empty()

    while True:
        status = requests.get(f"{api_url}/research/status/{session_id}").json()

        progress = status.get("progress", 0)
        message = status.get("message", "Processing...")

        progress_bar.progress(progress)
        status_text.text(message)

        if status.get("complete"):
            break

        time.sleep(2)  # Poll every 2 seconds

    # Show final results
    render_final_results(status["results"])
```

---

## Deployment Considerations

### Environment Variables

```bash
# .env or k8s ConfigMap
API_URL=http://agent-orchestrator.research-ops.svc.cluster.local:8080
ENABLE_STREAMING=true
SSE_TIMEOUT_SECONDS=600
```

### Kubernetes Service

Ensure web-ui service can reach agent-orchestrator:

```yaml
# k8s/web-ui-deployment.yaml
env:
- name: API_URL
  value: "http://agent-orchestrator.research-ops.svc.cluster.local:8080"
- name: ENABLE_STREAMING
  value: "true"
```

---

## Success Metrics

✅ **Real-time Updates:** Users see discoveries within 1 second of occurrence
✅ **No Full Page Reloads:** Only updated components refresh
✅ **Smooth Performance:** No lag or stuttering during updates
✅ **Error Recovery:** Graceful handling of connection issues
✅ **User Engagement:** Users understand research process as it unfolds

---

## Next Steps

1. **Implement SSE JavaScript component** (1-2 hours)
2. **Create Streamlit wrapper** (30 minutes)
3. **Update main UI** (2-3 hours)
4. **Test with live NIMs** (1 hour)
5. **Polish and optimize** (1 hour)

**Total Effort:** ~6-8 hours

---

**Status:** Ready for implementation
**Priority:** High (completes progressive synthesis feature)
**Dependencies:** Backend progressive synthesis (✅ complete)

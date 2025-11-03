# Server-Sent Events (SSE) Streaming API Guide

## Overview

The `/research/stream` endpoint provides real-time progressive results delivery using Server-Sent Events (SSE). Instead of waiting 5 minutes for complete results, users receive incremental updates as each agent completes its work.

## Endpoint Details

**URL:** `POST /research/stream`

**Request Format:** Same as `/research` endpoint
```json
{
  "query": "machine learning for medical imaging",
  "max_papers": 10,
  "start_year": 2020,
  "end_year": 2024,
  "prioritize_recent": true
}
```

**Response Format:** `text/event-stream` (SSE)

## Progressive Timeline

```
0-30s:    Scout Agent searches papers → papers_found event
30s-3min: Analyst Agent extracts findings → paper_analyzed events (batched)
3-4min:   Synthesizer Agent patterns → theme_found, contradiction_found events
4-5min:   Coordinator evaluates quality → synthesis_complete event
```

## Event Types

### 1. `agent_status`
Emitted when an agent starts or changes status.

```
event: agent_status
data: {"agent": "Scout", "status": "searching", "message": "Searching 7 sources"}
```

**Fields:**
- `agent`: Agent name (Scout, Analyst, Synthesizer, Coordinator)
- `status`: Current status (starting, searching, analyzing, synthesizing, evaluating)
- `message`: Human-readable status description

### 2. `papers_found`
Emitted when Scout completes paper search (~30 seconds).

```
event: papers_found
data: {
  "papers_count": 10,
  "papers": [
    {
      "id": "arxiv-001",
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "abstract": "Brief abstract...",
      "url": "https://arxiv.org/abs/1234",
      "source": "arxiv"
    }
  ],
  "decisions": [...]
}
```

**Fields:**
- `papers_count`: Total papers found
- `papers`: Array of paper objects (abbreviated abstracts)
- `decisions`: Scout agent decisions logged

### 3. `paper_analyzed`
Emitted every 3 papers during analysis phase (batched for efficiency).

```
event: paper_analyzed
data: {
  "batch": 1,
  "papers": [
    {
      "paper_id": "arxiv-001",
      "title": "Paper Title",
      "findings_count": 5,
      "confidence": 0.85
    }
  ],
  "total_analyzed": 3,
  "total": 10
}
```

**Fields:**
- `batch`: Batch number (1, 2, 3, ...)
- `papers`: Array of analyzed papers in this batch
- `total_analyzed`: Papers analyzed so far
- `total`: Total papers to analyze

### 4. `theme_found`
Emitted for each theme discovered during synthesis.

```
event: theme_found
data: {
  "theme_number": 1,
  "theme": "Deep learning architectures for medical image segmentation",
  "total_themes": 5
}
```

**Fields:**
- `theme_number`: Theme index (1-based)
- `theme`: Theme description
- `total_themes`: Total themes identified

### 5. `contradiction_found`
Emitted for each contradiction detected during synthesis.

```
event: contradiction_found
data: {
  "contradiction_number": 1,
  "contradiction": {
    "paper1": "Paper A",
    "claim1": "Claims 95% accuracy",
    "paper2": "Paper B",
    "claim2": "Shows 85% accuracy",
    "conflict": "Different evaluation metrics"
  },
  "total_contradictions": 2
}
```

**Fields:**
- `contradiction_number`: Contradiction index (1-based)
- `contradiction`: Contradiction object with details
- `total_contradictions`: Total contradictions found

### 6. `synthesis_complete`
Final event with complete synthesis results.

```
event: synthesis_complete
data: {
  "query": "machine learning for medical imaging",
  "papers_analyzed": 10,
  "common_themes": [...],
  "contradictions": [...],
  "research_gaps": [...],
  "decisions": [...],
  "synthesis_complete": true,
  "processing_time_seconds": 245.6,
  "quality_scores": [...]
}
```

**Fields:** Complete research synthesis (same as `/research` endpoint response)

### 7. `error`
Emitted when an error occurs during processing.

```
event: error
data: {
  "error": "Invalid input",
  "message": "Query cannot be empty",
  "timestamp": "2025-01-01T12:00:00"
}
```

**Fields:**
- `error`: Error type (Invalid input, Timeout, Internal error)
- `message`: Error description
- `timestamp`: ISO 8601 timestamp

## Usage Examples

### Python (aiohttp)

```python
import aiohttp
import json

async def stream_research():
    url = "http://localhost:8080/research/stream"
    payload = {
        "query": "machine learning for medical imaging",
        "max_papers": 10
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            async for line in response.content:
                decoded = line.decode('utf-8').strip()

                if decoded.startswith('event:'):
                    event_type = decoded.split(':', 1)[1].strip()
                    print(f"Event: {event_type}")

                elif decoded.startswith('data:'):
                    data_json = decoded.split(':', 1)[1].strip()
                    data = json.loads(data_json)

                    if event_type == 'papers_found':
                        print(f"Found {data['papers_count']} papers")
                    elif event_type == 'synthesis_complete':
                        print(f"Synthesis complete: {data['papers_analyzed']} papers")
                        return data
```

### JavaScript (EventSource)

```javascript
const eventSource = new EventSource('/research/stream?query=ml&max_papers=10');

eventSource.addEventListener('papers_found', (event) => {
  const data = JSON.parse(event.data);
  console.log(`Found ${data.papers_count} papers`);
});

eventSource.addEventListener('paper_analyzed', (event) => {
  const data = JSON.parse(event.data);
  console.log(`Analyzed ${data.total_analyzed}/${data.total} papers`);
});

eventSource.addEventListener('theme_found', (event) => {
  const data = JSON.parse(event.data);
  console.log(`Theme ${data.theme_number}: ${data.theme}`);
});

eventSource.addEventListener('synthesis_complete', (event) => {
  const data = JSON.parse(event.data);
  console.log('Synthesis complete:', data);
  eventSource.close();
});

eventSource.addEventListener('error', (event) => {
  const data = JSON.parse(event.data);
  console.error('Error:', data.message);
  eventSource.close();
});
```

### cURL (Testing)

```bash
curl -N -X POST http://localhost:8080/research/stream \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "max_papers": 5
  }'
```

**Note:** Use `-N` flag to disable buffering for real-time streaming.

## Error Handling

The endpoint gracefully handles errors by emitting `error` events:

1. **Validation Errors** (ValueError)
   - Invalid query (empty, too long, dangerous patterns)
   - Invalid max_papers (out of range)

2. **Timeout Errors** (asyncio.TimeoutError)
   - Research exceeds 5-minute limit
   - Returns partial results if available

3. **General Errors** (Exception)
   - NIM service unavailable
   - Network failures
   - Unexpected errors during processing

All errors include:
- Error type
- Descriptive message
- ISO 8601 timestamp

## Performance Characteristics

### Response Times
- **First event (agent_status):** < 1 second
- **papers_found event:** 20-40 seconds
- **paper_analyzed events:** Every 10-30 seconds (batched)
- **synthesis_complete event:** 3-5 minutes total

### Resource Usage
- **Memory:** Same as non-streaming endpoint (~200MB per request)
- **Bandwidth:** ~50KB-200KB total (incremental delivery)
- **Concurrency:** Supports multiple simultaneous streams

## Advantages Over Non-Streaming Endpoint

| Feature | `/research` (blocking) | `/research/stream` (SSE) |
|---------|----------------------|-------------------------|
| **User Feedback** | None until complete (5 min) | Real-time progress updates |
| **Early Access** | Must wait for full results | Papers available in 30s |
| **Error Detection** | Fails at end | Fails immediately |
| **User Experience** | Loading spinner for 5 min | Live progress visualization |
| **Cancellation** | Hard to cancel | Can close stream anytime |
| **Debugging** | Limited visibility | Full agent transparency |

## Integration with Web UI

The streaming endpoint is designed for integration with the Streamlit web UI:

```python
import streamlit as st
import requests
import json

st.title("Live Research Progress")

# Create placeholders for progressive updates
status_placeholder = st.empty()
papers_placeholder = st.empty()
themes_placeholder = st.empty()

# Stream research results
response = requests.post(
    "http://localhost:8080/research/stream",
    json={"query": query, "max_papers": 10},
    stream=True
)

for line in response.iter_lines():
    if line:
        decoded = line.decode('utf-8')

        if decoded.startswith('event:'):
            event_type = decoded.split(':', 1)[1].strip()

        elif decoded.startswith('data:'):
            data = json.loads(decoded.split(':', 1)[1])

            if event_type == 'agent_status':
                status_placeholder.info(f"Agent: {data['agent']} - {data['message']}")

            elif event_type == 'papers_found':
                papers_placeholder.success(f"Found {data['papers_count']} papers!")

            elif event_type == 'theme_found':
                themes_placeholder.write(f"- {data['theme']}")

            elif event_type == 'synthesis_complete':
                st.success("Synthesis complete!")
                st.json(data)
```

## Testing

Run the included test script:

```bash
python src/test_sse_endpoint.py
```

This verifies:
- Correct SSE format (`text/event-stream`)
- Event types emitted in correct order
- Valid JSON data in each event
- Error handling for invalid input

## Troubleshooting

### No Events Received
- **Check server:** Ensure API server is running (`uvicorn src.api:app --reload`)
- **Check NIMs:** Verify NIMs are accessible (check `/health` endpoint)
- **Check buffering:** Disable nginx/proxy buffering (`X-Accel-Buffering: no`)

### Events Delayed
- **Network buffering:** Check proxy settings, use direct connection
- **Python buffering:** Ensure `StreamingResponse` doesn't buffer
- **Client buffering:** Use unbuffered mode (`curl -N`)

### Connection Drops
- **Timeout:** Default 5-minute limit, extend if needed
- **Network issues:** Check firewall, proxy, load balancer settings
- **Client timeout:** Increase client timeout for long-running requests

## Future Enhancements

1. **Selective Events:** Allow clients to subscribe to specific event types
2. **Progress Percentages:** Add completion percentage to each event
3. **Agent Decisions:** Stream individual decisions as they're made
4. **Resume Support:** Support resuming interrupted streams
5. **WebSocket Alternative:** Provide bidirectional WebSocket endpoint

## References

- **SSE Specification:** [W3C Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- **FastAPI Streaming:** [FastAPI StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- **EventSource API:** [MDN EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)

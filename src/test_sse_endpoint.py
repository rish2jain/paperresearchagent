"""
Test script for SSE streaming endpoint
Verifies that the /research/stream endpoint returns Server-Sent Events correctly
"""

import asyncio
import aiohttp
import json


async def test_sse_endpoint():
    """Test the SSE streaming endpoint"""
    url = "http://localhost:8080/research/stream"

    # Test payload
    payload = {
        "query": "machine learning for medical imaging",
        "max_papers": 5  # Small number for faster testing
    }

    print(f"Testing SSE endpoint: {url}")
    print(f"Query: {payload['query']}")
    print("=" * 60)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                print(f"Response status: {response.status}")
                print(f"Content-Type: {response.headers.get('content-type')}")
                print("=" * 60)

                if response.status != 200:
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    return

                # Verify it's text/event-stream
                content_type = response.headers.get('content-type', '')
                if 'text/event-stream' not in content_type:
                    print(f"❌ Expected text/event-stream, got {content_type}")
                    return

                print("✅ Content-Type is text/event-stream")
                print("=" * 60)
                print("Receiving events:\n")

                event_count = 0
                event_types = {}

                # Read SSE stream
                async for line in response.content:
                    decoded = line.decode('utf-8').strip()

                    if not decoded:
                        continue

                    # Parse SSE format
                    if decoded.startswith('event:'):
                        event_type = decoded.split(':', 1)[1].strip()
                        event_count += 1
                        event_types[event_type] = event_types.get(event_type, 0) + 1
                        print(f"📡 Event #{event_count}: {event_type}")

                    elif decoded.startswith('data:'):
                        data_json = decoded.split(':', 1)[1].strip()
                        try:
                            data = json.loads(data_json)
                            # Print abbreviated data for readability
                            if 'agent' in data:
                                print(f"   Agent: {data['agent']} - {data.get('message', '')}")
                            elif 'papers_count' in data:
                                print(f"   Papers found: {data['papers_count']}")
                            elif 'theme' in data:
                                print(f"   Theme: {data['theme'][:60]}...")
                            elif 'contradiction' in data:
                                print(f"   Contradiction detected")
                            elif 'papers_analyzed' in data:
                                print(f"   ✅ Synthesis complete: {data['papers_analyzed']} papers")
                            elif 'error' in data:
                                print(f"   ❌ Error: {data['message']}")
                        except json.JSONDecodeError:
                            print(f"   (Raw data: {data_json[:100]}...)")

                print("\n" + "=" * 60)
                print("Stream complete!")
                print(f"Total events received: {event_count}")
                print("Event types:")
                for event_type, count in event_types.items():
                    print(f"  - {event_type}: {count}")
                print("=" * 60)

    except aiohttp.ClientConnectorError:
        print("❌ Could not connect to server. Is it running?")
        print("   Start server with: uvicorn src.api:app --reload --host 0.0.0.0 --port 8080")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


async def test_sse_error_handling():
    """Test SSE endpoint error handling"""
    url = "http://localhost:8080/research/stream"

    # Test with invalid input
    invalid_payload = {
        "query": "",  # Empty query should fail validation
        "max_papers": 100  # Out of range
    }

    print("\n" + "=" * 60)
    print("Testing error handling with invalid input")
    print("=" * 60)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=invalid_payload) as response:
                print(f"Response status: {response.status}")

                async for line in response.content:
                    decoded = line.decode('utf-8').strip()

                    if decoded.startswith('event:'):
                        event_type = decoded.split(':', 1)[1].strip()
                        print(f"📡 Event: {event_type}")

                    elif decoded.startswith('data:'):
                        data_json = decoded.split(':', 1)[1].strip()
                        data = json.loads(data_json)
                        if 'error' in data:
                            print(f"✅ Error event received: {data['message']}")

    except Exception as e:
        print(f"Test error: {e}")


if __name__ == "__main__":
    print("SSE Endpoint Test Suite")
    print("=" * 60)

    # Run tests
    asyncio.run(test_sse_endpoint())
    asyncio.run(test_sse_error_handling())

    print("\n✅ Tests complete!")

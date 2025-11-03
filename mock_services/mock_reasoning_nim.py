"""
Mock Reasoning NIM Service
Simulates llama-3.1-nemotron-nano-8B-v1 for testing
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Mock Reasoning NIM")


@app.get("/v1/health/live")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mock-reasoning-nim"}


@app.post("/v1/completions")
def completions(request: dict):
    """
    Mock completion endpoint
    Returns a simple mock completion based on the prompt
    """
    prompt = request.get("prompt", "")
    max_tokens = request.get("max_tokens", 100)
    
    # Generate mock completion
    mock_response = f"Mock reasoning completion for: {prompt[:100]}"
    if len(prompt) > 100:
        mock_response += "..."
    
    return {
        "choices": [{
            "text": mock_response,
            "index": 0,
            "finish_reason": "length"
        }],
        "model": "meta/llama-3.1-nemotron-nano-8b-instruct",
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(mock_response.split()),
            "total_tokens": len(prompt.split()) + len(mock_response.split())
        }
    }


@app.post("/v1/chat/completions")
def chat_completions(request: dict):
    """
    Mock chat completion endpoint
    Returns a simple mock chat response
    """
    messages = request.get("messages", [])
    last_msg = messages[-1] if messages else {}
    content = last_msg.get("content", "")
    
    # Generate mock chat response
    mock_response = f"Mock chat response for: {content[:100]}"
    if len(content) > 100:
        mock_response += "..."
    
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": mock_response
            },
            "index": 0,
            "finish_reason": "stop"
        }],
        "model": "meta/llama-3.1-nemotron-nano-8b-instruct",
        "usage": {
            "prompt_tokens": sum(len(msg.get("content", "").split()) for msg in messages),
            "completion_tokens": len(mock_response.split()),
            "total_tokens": sum(len(msg.get("content", "").split()) for msg in messages) + len(mock_response.split())
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


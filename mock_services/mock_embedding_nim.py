"""
Mock Embedding NIM Service
Simulates nv-embedqa-e5-v5 for testing
"""

from fastapi import FastAPI
import uvicorn
import numpy as np

app = FastAPI(title="Mock Embedding NIM")


@app.get("/v1/health/live")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mock-embedding-nim"}


@app.post("/v1/embeddings")
def embeddings(request: dict):
    """
    Mock embedding endpoint
    Returns deterministic mock embeddings based on text hash
    """
    input_data = request.get("input", "")
    input_type = request.get("input_type", "passage")
    
    # Handle both string and list inputs
    if isinstance(input_data, str):
        input_data = [input_data]
    
    # Generate mock embeddings (1024 dimensions as per nv-embedqa-e5-v5)
    mock_embeddings = []
    for idx, text in enumerate(input_data):
        # Generate deterministic mock embedding based on text hash
        np.random.seed(hash(text) % (2**32))
        embedding = (np.random.rand(1024) * 2 - 1).tolist()
        
        mock_embeddings.append({
            "embedding": embedding,
            "index": idx,
            "object": "embedding"
        })
    
    return {
        "data": mock_embeddings,
        "model": "nvidia/nv-embedqa-e5-v5",
        "usage": {
            "prompt_tokens": sum(len(text.split()) for text in input_data),
            "total_tokens": sum(len(text.split()) for text in input_data)
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)


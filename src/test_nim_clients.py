"""
Unit Tests for NIM Clients
Tests NIM client functionality with mocks
"""

import pytest
import aiohttp
from unittest.mock import Mock, AsyncMock, patch
from nim_clients import ReasoningNIMClient, EmbeddingNIMClient


@pytest.fixture
def mock_session():
    """Mock aiohttp session"""
    session = Mock()
    session.closed = False
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    return session


@pytest.mark.asyncio
async def test_reasoning_nim_complete():
    """Test ReasoningNIMClient complete method"""
    client = ReasoningNIMClient(base_url="http://test:8000")
    
    # Mock session and response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "choices": [{"text": "Test completion"}]
    })
    
    with patch('aiohttp.ClientSession') as mock_session_class:
        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session.closed = False
        mock_session.post = AsyncMock(return_value=mock_response.__aenter__())
        mock_session_class.return_value = mock_session
        
        async with client:
            result = await client.complete("test prompt", max_tokens=50)
            assert result == "Test completion"


@pytest.mark.asyncio
async def test_reasoning_nim_extract_structured():
    """Test ReasoningNIMClient extract_structured method"""
    client = ReasoningNIMClient(base_url="http://test:8000")
    
    # Mock complete method
    client.complete = AsyncMock(return_value='{"key": "value"}')
    
    async with client:
        result = await client.extract_structured("test text", {"key": "string"})
        assert "key" in result


@pytest.mark.asyncio
async def test_embedding_nim_embed():
    """Test EmbeddingNIMClient embed method"""
    client = EmbeddingNIMClient(base_url="http://test:8001")
    
    # Mock session and response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "data": [{"embedding": [0.1] * 1024}]
    })
    
    with patch('aiohttp.ClientSession') as mock_session_class:
        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session.closed = False
        mock_session.post = AsyncMock(return_value=mock_response.__aenter__())
        mock_session_class.return_value = mock_session
        
        async with client:
            result = await client.embed("test text")
            assert len(result) == 1024
            assert isinstance(result, list)


@pytest.mark.asyncio
async def test_embedding_nim_embed_batch():
    """Test EmbeddingNIMClient embed_batch method"""
    client = EmbeddingNIMClient(base_url="http://test:8001")
    
    # Mock session and response
    mock_response = Mock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "data": [
            {"embedding": [0.1] * 1024},
            {"embedding": [0.2] * 1024}
        ]
    })
    
    with patch('aiohttp.ClientSession') as mock_session_class:
        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session.closed = False
        mock_session.post = AsyncMock(return_value=mock_response.__aenter__())
        mock_session_class.return_value = mock_session
        
        async with client:
            texts = ["text 1", "text 2"]
            results = await client.embed_batch(texts)
            assert len(results) == 2
            assert len(results[0]) == 1024


def test_cosine_similarity():
    """Test cosine similarity calculation"""
    from nim_clients import EmbeddingNIMClient
    
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [0.0, 1.0, 0.0]
    
    similarity = EmbeddingNIMClient.cosine_similarity(vec1, vec2)
    
    # Orthogonal vectors should have similarity ~0.5 (after normalization)
    assert 0.0 <= similarity <= 1.0


@pytest.mark.asyncio
async def test_retry_logic():
    """Test retry logic on network errors"""
    client = ReasoningNIMClient(base_url="http://test:8000")
    
    # Mock session that fails twice then succeeds
    call_count = [0]
    
    async def mock_post(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] < 3:
            raise aiohttp.ClientError("Network error")
        
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "choices": [{"text": "Success"}]
        })
        return mock_response
    
    with patch('aiohttp.ClientSession') as mock_session_class:
        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_session.closed = False
        mock_session.post = AsyncMock(side_effect=mock_post)
        mock_session_class.return_value = mock_session
        
        async with client:
            result = await client.complete("test", max_tokens=10)
            assert result == "Success"
            assert call_count[0] == 3  # Retried 3 times


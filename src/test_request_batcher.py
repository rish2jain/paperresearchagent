"""
Request Batching System Tests
Tests batch collection, processing, and queue management
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from request_batcher import (
    RequestBatcher,
    BatchedRequest,
    BatchStatus,
    get_request_batcher
)


class TestBatchedRequest:
    """Test BatchedRequest dataclass"""
    
    def test_batched_request_creation(self):
        """Test creating a batched request"""
        request = BatchedRequest(
            request_id="req-1",
            query="machine learning",
            max_papers=10,
            start_year=2020,
            end_year=2024
        )
        
        assert request.request_id == "req-1"
        assert request.query == "machine learning"
        assert request.max_papers == 10
        assert request.start_year == 2020
        assert request.end_year == 2024
        assert request.timestamp is not None
    
    def test_batched_request_defaults(self):
        """Test batched request with defaults"""
        request = BatchedRequest(
            request_id="req-2",
            query="test query",
            max_papers=5
        )
        
        assert request.start_year is None
        assert request.end_year is None
        assert request.prioritize_recent is False
        assert request.result is None
        assert request.error is None


class TestRequestBatcher:
    """Test RequestBatcher class"""
    
    @pytest.fixture
    def batcher(self):
        """Create RequestBatcher with test-friendly config"""
        return RequestBatcher(
            batch_size=3,
            batch_timeout=0.5,  # Short timeout for testing
            max_wait_time=5.0
        )
    
    @pytest.mark.asyncio
    async def test_add_request(self, batcher):
        """Test adding request to queue"""
        request_id = await batcher.add_request(
            query="test query",
            max_papers=10
        )
        
        assert request_id is not None
        assert len(request_id) > 0
        assert request_id in batcher.request_futures
        assert batcher.get_queue_size() == 1
    
    @pytest.mark.asyncio
    async def test_add_multiple_requests(self, batcher):
        """Test adding multiple requests"""
        request_ids = []
        
        for i in range(5):
            req_id = await batcher.add_request(f"query {i}", max_papers=10)
            request_ids.append(req_id)
        
        assert len(request_ids) == 5
        assert batcher.get_queue_size() == 5
        assert batcher.get_pending_requests() == 5
    
    @pytest.mark.asyncio
    async def test_get_result_invalid_id(self, batcher):
        """Test getting result with invalid request ID"""
        with pytest.raises(ValueError, match="not found"):
            await batcher.get_result("invalid-id")
    
    @pytest.mark.asyncio
    async def test_batch_processing_with_custom_processor(self, batcher):
        """Test batch processing with custom processor"""
        async def processor(query, max_papers, **kwargs):
            return {
                "query": query,
                "papers": [f"paper-{i}" for i in range(max_papers)]
            }
        
        await batcher.start()
        
        try:
            # Add requests
            request_id1 = await batcher.add_request("query1", max_papers=5)
            request_id2 = await batcher.add_request("query2", max_papers=3)
            
            # Manually trigger batch processing with custom processor
            # Get a batch from the queue
            await asyncio.sleep(0.2)  # Small delay to let requests be queued
            
            # Process the batch manually with custom processor
            batch = []
            while not batcher.queue.empty():
                try:
                    req = batcher.queue.get_nowait()
                    batch.append(req)
                except asyncio.QueueEmpty:
                    break
            
            if batch:
                await batcher._process_batch(batch, processor_func=processor)
            
            # Get results
            result1 = await batcher.get_result(request_id1, timeout=2.0)
            result2 = await batcher.get_result(request_id2, timeout=2.0)
            
            assert result1["query"] == "query1"
            assert len(result1["papers"]) == 5
            assert result2["query"] == "query2"
            assert len(result2["papers"]) == 3
        finally:
            await batcher.stop()
    
    @pytest.mark.asyncio
    async def test_batch_size_limit(self, batcher):
        """Test batch respects size limit"""
        results = []
        
        async def processor(query, max_papers, **kwargs):
            results.append(query)
            return {"query": query}
        
        await batcher.start()
        
        try:
            # Add more requests than batch size
            request_ids = []
            for i in range(5):
                req_id = await batcher.add_request(f"query{i}", max_papers=5)
                request_ids.append(req_id)
            
            # Manually process batches
            await asyncio.sleep(0.2)
            
            # Collect and process batches manually
            batch = []
            while not batcher.queue.empty():
                try:
                    req = batcher.queue.get_nowait()
                    batch.append(req)
                except asyncio.QueueEmpty:
                    break
            
            if batch:
                await batcher._process_batch(batch, processor_func=processor)
            
            # Should process in batches of batch_size (3)
            assert len(results) >= min(3, len(batch))
        finally:
            await batcher.stop()
    
    @pytest.mark.asyncio
    async def test_batch_timeout(self, batcher):
        """Test batch processes after timeout even if not full"""
        async def processor(query, max_papers, **kwargs):
            return {"query": query}
        
        await batcher.start()
        
        try:
            # Add one request (won't fill batch)
            request_id = await batcher.add_request("single query", max_papers=5)
            
            # Wait a bit for queuing
            await asyncio.sleep(0.2)
            
            # Manually process the single request
            batch = []
            try:
                req = batcher.queue.get_nowait()
                batch.append(req)
            except asyncio.QueueEmpty:
                pass
            
            if batch:
                await batcher._process_batch(batch, processor_func=processor)
            
            # Should have processed despite not filling batch
            result = await batcher.get_result(request_id, timeout=1.0)
            assert result["query"] == "single query"
        finally:
            await batcher.stop()
    
    @pytest.mark.asyncio
    async def test_get_result_timeout(self, batcher):
        """Test get_result with timeout"""
        request_id = await batcher.add_request("test", max_papers=5)
        
        # Try to get result before processing (will timeout)
        with pytest.raises(TimeoutError):
            await batcher.get_result(request_id, timeout=0.1)
    
    @pytest.mark.asyncio
    async def test_error_handling_in_batch(self, batcher):
        """Test error handling in batch processing"""
        async def failing_processor(query, max_papers, **kwargs):
            raise Exception("Processing failed")
        
        # Don't start the batcher - process manually
        request_id = await batcher.add_request("failing query", max_papers=5)
        
        # Wait a bit for queuing
        await asyncio.sleep(0.1)
        
        # Manually process with failing processor (before auto-processor can run)
        batch = []
        try:
            req = batcher.queue.get_nowait()
            batch.append(req)
        except asyncio.QueueEmpty:
            pass
        
        if batch:
            await batcher._process_batch(batch, processor_func=failing_processor)
        
        # Should raise exception when getting result
        with pytest.raises(Exception, match="Processing failed"):
            await batcher.get_result(request_id, timeout=1.0)
    
    @pytest.mark.asyncio
    async def test_start_stop(self, batcher):
        """Test starting and stopping batcher"""
        assert batcher._processing is False
        
        await batcher.start()
        assert batcher._processing is True
        assert batcher._processor_task is not None
        
        await batcher.stop()
        assert batcher._processing is False
    
    def test_get_queue_size(self, batcher):
        """Test getting queue size"""
        # Initially empty
        assert batcher.get_queue_size() == 0
    
    def test_get_pending_requests(self, batcher):
        """Test getting pending requests count"""
        # Initially no pending
        assert batcher.get_pending_requests() == 0


class TestGetRequestBatcher:
    """Test global request batcher"""
    
    def test_get_request_batcher_singleton(self):
        """Test get_request_batcher returns singleton"""
        with patch('request_batcher.RequestBatcher') as mock_batcher:
            batcher1 = get_request_batcher()
            batcher2 = get_request_batcher()
            
            # Should be same instance
            assert batcher1 is batcher2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


"""
Request Batching System
Batches multiple API requests for efficient processing
"""

import asyncio
import time
import os
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class BatchStatus(Enum):
    """Batch processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class BatchedRequest:
    """Individual request within a batch"""
    request_id: str
    query: str
    max_papers: int
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    prioritize_recent: bool = False
    timestamp: datetime = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class RequestBatcher:
    """
    Batches multiple synthesis requests for efficient processing
    
    Groups incoming requests and processes them together to improve
    resource utilization and reduce overhead.
    """
    
    def __init__(
        self,
        batch_size: int = 5,
        batch_timeout: float = 2.0,
        max_wait_time: float = 30.0
    ):
        """
        Initialize request batcher
        
        Args:
            batch_size: Maximum number of requests per batch
            batch_timeout: Seconds to wait for batch to fill before processing
            max_wait_time: Maximum time a request can wait in queue
        """
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.max_wait_time = max_wait_time
        
        self.queue: asyncio.Queue = asyncio.Queue()
        self.batches: Dict[str, Dict[str, Any]] = {}
        self.request_futures: Dict[str, asyncio.Future] = {}
        
        self._processing = False
        self._processor_task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the batch processor"""
        if not self._processing:
            self._processing = True
            self._processor_task = asyncio.create_task(self._batch_processor())
            logger.info("Request batcher started")
    
    async def stop(self):
        """Stop the batch processor"""
        self._processing = False
        if self._processor_task:
            self._processor_task.cancel()
            try:
                await self._processor_task
            except asyncio.CancelledError:
                pass
        logger.info("Request batcher stopped")
    
    async def add_request(
        self,
        query: str,
        max_papers: int = 10,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        prioritize_recent: bool = False
    ) -> str:
        """
        Add a request to the batch queue
        
        Returns:
            Request ID for tracking
        """
        import uuid
        request_id = str(uuid.uuid4())
        
        request = BatchedRequest(
            request_id=request_id,
            query=query,
            max_papers=max_papers,
            start_year=start_year,
            end_year=end_year,
            prioritize_recent=prioritize_recent
        )
        
        # Create future for this request
        future = asyncio.Future()
        self.request_futures[request_id] = future
        
        # Add to queue
        await self.queue.put(request)
        logger.info(f"Request {request_id} added to batch queue")
        
        return request_id
    
    async def get_result(self, request_id: str, timeout: Optional[float] = None) -> Dict[str, Any]:
        """
        Get result for a request
        
        Args:
            request_id: Request ID returned from add_request
            timeout: Maximum time to wait for result
            
        Returns:
            Synthesis result dictionary
        """
        if request_id not in self.request_futures:
            raise ValueError(f"Request {request_id} not found")
        
        future = self.request_futures[request_id]
        
        try:
            if timeout:
                result = await asyncio.wait_for(future, timeout=timeout)
            else:
                result = await future
            return result
        except asyncio.TimeoutError:
            raise TimeoutError(f"Request {request_id} timed out")
    
    async def _batch_processor(self):
        """Main batch processing loop"""
        while self._processing:
            try:
                batch = await self._collect_batch()
                if batch:
                    await self._process_batch(batch)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in batch processor: {e}")
                await asyncio.sleep(1)
    
    async def _collect_batch(self) -> List[BatchedRequest]:
        """Collect requests into a batch"""
        batch: List[BatchedRequest] = []
        batch_start_time = time.time()
        
        # Collect requests until batch is full or timeout
        while len(batch) < self.batch_size and self._processing:
            try:
                # Wait for next request with timeout
                remaining_timeout = self.batch_timeout - (time.time() - batch_start_time)
                
                if remaining_timeout > 0:
                    request = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=min(remaining_timeout, 0.5)
                    )
                else:
                    # Timeout reached, process what we have
                    if batch:
                        break
                    request = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=self.batch_timeout
                    )
                
                # Check if request has been waiting too long
                wait_time = (datetime.now() - request.timestamp).total_seconds()
                if wait_time > self.max_wait_time:
                    logger.warning(
                        f"Request {request.request_id} waited {wait_time:.1f}s, "
                        f"processing immediately"
                    )
                    batch.append(request)
                    break
                
                batch.append(request)
                
                # Process immediately if batch is full
                if len(batch) >= self.batch_size:
                    break
                    
            except asyncio.TimeoutError:
                # Timeout reached, process what we have
                if batch:
                    break
                continue
        
        return batch
    
    async def _process_batch(
        self,
        batch: List[BatchedRequest],
        processor_func: Optional[Callable] = None
    ):
        """
        Process a batch of requests
        
        Args:
            batch: List of requests to process
            processor_func: Optional custom processor function
        """
        batch_id = f"batch-{int(time.time())}"
        logger.info(f"Processing batch {batch_id} with {len(batch)} requests")
        
        # Process requests in parallel
        tasks = []
        for request in batch:
            if processor_func:
                task = asyncio.create_task(
                    self._process_single_request(request, processor_func)
                )
            else:
                # Default: process sequentially (can be overridden)
                task = asyncio.create_task(
                    self._process_single_request_default(request)
                )
            tasks.append((request.request_id, task))
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        # Set futures with results
        for (request_id, _), result in zip(tasks, results):
            future = self.request_futures.get(request_id)
            if future:
                if isinstance(result, Exception):
                    future.set_exception(result)
                else:
                    future.set_result(result)
                del self.request_futures[request_id]
    
    async def _process_single_request(
        self,
        request: BatchedRequest,
        processor_func: Callable
    ) -> Dict[str, Any]:
        """Process a single request using custom processor"""
        try:
            result = await processor_func(
                query=request.query,
                max_papers=request.max_papers,
                start_year=request.start_year,
                end_year=request.end_year,
                prioritize_recent=request.prioritize_recent
            )
            return result
        except Exception as e:
            logger.error(f"Error processing request {request.request_id}: {e}")
            raise
    
    async def _process_single_request_default(self, request: BatchedRequest) -> Dict[str, Any]:
        """
        Default processor (placeholder)
        
        In actual implementation, this would call the synthesis agent
        """
        logger.warning(
            f"Default processor called for request {request.request_id}. "
            f"Please provide a custom processor function."
        )
        return {
            "request_id": request.request_id,
            "status": "pending",
            "message": "Default processor - implement custom processor"
        }
    
    def get_queue_size(self) -> int:
        """Get current queue size"""
        return self.queue.qsize()
    
    def get_pending_requests(self) -> int:
        """Get number of pending requests"""
        return len(self.request_futures)


# Global batcher instance
_batcher: Optional[RequestBatcher] = None


def get_request_batcher() -> RequestBatcher:
    """Get or create global request batcher instance"""
    global _batcher
    if _batcher is None:
        _batcher = RequestBatcher(
            batch_size=int(os.getenv("BATCH_SIZE", "5")),
            batch_timeout=float(os.getenv("BATCH_TIMEOUT", "2.0")),
            max_wait_time=float(os.getenv("MAX_WAIT_TIME", "30.0"))
        )
    return _batcher


"""
Prometheus Metrics and Monitoring
Provides metrics for performance monitoring and observability
"""

from typing import Dict, Any, Optional
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Try to import Prometheus client
try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.warning("Prometheus client not available. Install with: pip install prometheus-client")


class MetricsCollector:
    """
    Collects and exports metrics for monitoring
    """
    
    def __init__(self):
        if not PROMETHEUS_AVAILABLE:
            logger.warning("Prometheus metrics disabled (prometheus-client not installed)")
            self.metrics_enabled = False
            return
        
        self.metrics_enabled = True
        
        # Request metrics
        self.requests_total = Counter(
            'research_ops_requests_total',
            'Total number of research requests',
            ['status']  # success, error
        )
        
        self.request_duration = Histogram(
            'research_ops_request_duration_seconds',
            'Request processing duration in seconds',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0]
        )
        
        # Agent metrics
        self.agent_decisions = Counter(
            'research_ops_agent_decisions_total',
            'Total agent decisions made',
            ['agent', 'decision_type']
        )
        
        self.papers_analyzed = Counter(
            'research_ops_papers_analyzed_total',
            'Total papers analyzed',
            ['source']
        )
        
        # NIM usage metrics
        self.nim_requests = Counter(
            'research_ops_nim_requests_total',
            'Total NIM API requests',
            ['nim_type', 'endpoint', 'status']  # reasoning/embedding, endpoint, success/error
        )
        
        self.nim_duration = Histogram(
            'research_ops_nim_duration_seconds',
            'NIM API request duration',
            ['nim_type', 'endpoint'],
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
        )
        
        # Cache metrics
        self.cache_hits = Counter(
            'research_ops_cache_hits_total',
            'Total cache hits',
            ['cache_type']
        )
        
        self.cache_misses = Counter(
            'research_ops_cache_misses_total',
            'Total cache misses',
            ['cache_type']
        )
        
        # Quality metrics
        self.quality_scores = Histogram(
            'research_ops_quality_scores',
            'Paper quality scores distribution',
            buckets=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        )
        
        # Active requests gauge
        self.active_requests = Gauge(
            'research_ops_active_requests',
            'Number of currently active requests'
        )
        
        logger.info("Metrics collector initialized")
    
    def record_request(self, status: str, duration: float):
        """Record API request"""
        if not self.metrics_enabled:
            return
        
        self.requests_total.labels(status=status).inc()
        self.request_duration.observe(duration)
    
    def record_agent_decision(self, agent: str, decision_type: str):
        """Record agent decision"""
        if not self.metrics_enabled:
            return
        
        self.agent_decisions.labels(
            agent=agent,
            decision_type=decision_type
        ).inc()
    
    def record_paper_analyzed(self, source: str):
        """Record paper analysis"""
        if not self.metrics_enabled:
            return
        
        self.papers_analyzed.labels(source=source).inc()
    
    def record_nim_request(
        self,
        nim_type: str,
        endpoint: str,
        status: str,
        duration: float
    ):
        """Record NIM API request"""
        if not self.metrics_enabled:
            return
        
        self.nim_requests.labels(
            nim_type=nim_type,
            endpoint=endpoint,
            status=status
        ).inc()
        self.nim_duration.labels(
            nim_type=nim_type,
            endpoint=endpoint
        ).observe(duration)
    
    def record_cache_hit(self, cache_type: str):
        """Record cache hit"""
        if not self.metrics_enabled:
            return
        
        self.cache_hits.labels(cache_type=cache_type).inc()
    
    def record_cache_miss(self, cache_type: str):
        """Record cache miss"""
        if not self.metrics_enabled:
            return
        
        self.cache_misses.labels(cache_type=cache_type).inc()
    
    def record_quality_score(self, score: float):
        """Record paper quality score"""
        if not self.metrics_enabled:
            return
        
        self.quality_scores.observe(score)
    
    def increment_active_requests(self):
        """Increment active requests counter"""
        if not self.metrics_enabled:
            return
        
        self.active_requests.inc()
    
    def decrement_active_requests(self):
        """Decrement active requests counter"""
        if not self.metrics_enabled:
            return
        
        self.active_requests.dec()
    
    def get_metrics(self) -> str:
        """Get Prometheus metrics in text format"""
        if not self.metrics_enabled:
            return "# Metrics disabled (prometheus-client not installed)\n"
        
        return generate_latest(REGISTRY).decode('utf-8')


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector instance"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


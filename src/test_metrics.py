"""
Metrics Collection Tests
Tests Prometheus metrics collection and export
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from metrics import MetricsCollector, get_metrics_collector


class TestMetricsCollector:
    """Test MetricsCollector class"""
    
    @pytest.fixture
    def mock_prometheus(self):
        """Mock Prometheus client"""
        with patch('metrics.PROMETHEUS_AVAILABLE', True):
            with patch('metrics.Counter') as mock_counter, \
                 patch('metrics.Histogram') as mock_histogram, \
                 patch('metrics.Gauge') as mock_gauge, \
                 patch('metrics.generate_latest') as mock_generate:
                
                # Setup mocks
                mock_counter_instance = Mock()
                mock_histogram_instance = Mock()
                mock_gauge_instance = Mock()
                
                mock_counter.return_value = mock_counter_instance
                mock_histogram.return_value = mock_histogram_instance
                mock_gauge.return_value = mock_gauge_instance
                mock_generate.return_value = b"# metrics output\n"
                
                yield {
                    'counter': mock_counter_instance,
                    'histogram': mock_histogram_instance,
                    'gauge': mock_gauge_instance,
                    'generate': mock_generate
                }
    
    def test_collector_initialization_with_prometheus(self, mock_prometheus):
        """Test metrics collector initializes with Prometheus"""
        collector = MetricsCollector()
        
        assert collector.metrics_enabled is True
        assert collector.requests_total is not None
        assert collector.request_duration is not None
        assert collector.agent_decisions is not None
    
    @patch('metrics.PROMETHEUS_AVAILABLE', False)
    def test_collector_initialization_without_prometheus(self):
        """Test metrics collector without Prometheus"""
        collector = MetricsCollector()
        
        assert collector.metrics_enabled is False
    
    def test_record_request(self, mock_prometheus):
        """Test recording API requests"""
        collector = MetricsCollector()
        
        collector.record_request("success", 1.5)
        
        # Verify counter and histogram were called
        mock_prometheus['counter'].labels.assert_called()
        mock_prometheus['histogram'].observe.assert_called_with(1.5)
    
    def test_record_agent_decision(self, mock_prometheus):
        """Test recording agent decisions"""
        collector = MetricsCollector()
        
        collector.record_agent_decision("Scout", "SEARCH_EXPANDED")
        
        mock_prometheus['counter'].labels.assert_called_with(
            agent="Scout",
            decision_type="SEARCH_EXPANDED"
        )
        mock_prometheus['counter'].labels().inc.assert_called()
    
    def test_record_paper_analyzed(self, mock_prometheus):
        """Test recording paper analysis"""
        collector = MetricsCollector()
        
        collector.record_paper_analyzed("arxiv")
        
        mock_prometheus['counter'].labels.assert_called_with(source="arxiv")
    
    def test_record_nim_request(self, mock_prometheus):
        """Test recording NIM requests"""
        collector = MetricsCollector()
        
        collector.record_nim_request("reasoning", "/completions", "success", 0.5)
        
        mock_prometheus['counter'].labels.assert_called()
        mock_prometheus['histogram'].labels.assert_called_with(
            nim_type="reasoning",
            endpoint="/completions"
        )
        mock_prometheus['histogram'].labels().observe.assert_called_with(0.5)
    
    def test_record_cache_operations(self, mock_prometheus):
        """Test recording cache hits and misses"""
        collector = MetricsCollector()
        
        collector.record_cache_hit("embedding")
        collector.record_cache_miss("result")
        
        assert mock_prometheus['counter'].labels.call_count >= 2
    
    def test_record_quality_score(self, mock_prometheus):
        """Test recording quality scores"""
        collector = MetricsCollector()
        
        collector.record_quality_score(0.85)
        
        mock_prometheus['histogram'].observe.assert_called_with(0.85)
    
    def test_active_requests_tracking(self, mock_prometheus):
        """Test active requests gauge"""
        collector = MetricsCollector()
        
        collector.increment_active_requests()
        mock_prometheus['gauge'].inc.assert_called()
        
        collector.decrement_active_requests()
        mock_prometheus['gauge'].dec.assert_called()
    
    def test_get_metrics(self, mock_prometheus):
        """Test getting Prometheus metrics"""
        collector = MetricsCollector()
        
        metrics = collector.get_metrics()
        
        assert isinstance(metrics, str)
        assert "# metrics output" in metrics
        mock_prometheus['generate'].assert_called()
    
    @patch('metrics.PROMETHEUS_AVAILABLE', False)
    def test_get_metrics_disabled(self):
        """Test getting metrics when Prometheus unavailable"""
        collector = MetricsCollector()
        
        metrics = collector.get_metrics()
        
        assert "# Metrics disabled" in metrics
    
    @patch('metrics.PROMETHEUS_AVAILABLE', False)
    def test_record_when_disabled(self):
        """Test recording metrics when disabled"""
        collector = MetricsCollector()
        
        # Should not raise errors
        collector.record_request("success", 1.0)
        collector.record_agent_decision("Scout", "SEARCH")
        collector.record_paper_analyzed("arxiv")
        collector.increment_active_requests()


class TestGetMetricsCollector:
    """Test global metrics collector"""
    
    def test_get_metrics_collector_singleton(self):
        """Test get_metrics_collector returns singleton"""
        with patch('metrics.MetricsCollector') as mock_collector_class:
            collector1 = get_metrics_collector()
            collector2 = get_metrics_collector()
            
            # Should be same instance (singleton)
            assert collector1 is collector2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


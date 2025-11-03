"""
Circuit Breaker Pattern Tests
Tests circuit breaker state transitions and failure handling
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock
from circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    CircuitState,
    circuit_breaker_decorator
)


class TestCircuitBreakerConfig:
    """Test CircuitBreakerConfig"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = CircuitBreakerConfig()
        
        assert config.fail_max == 5
        assert config.timeout_duration == 60
        assert config.success_threshold == 2
        assert ValueError in config.excluded_exceptions
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = CircuitBreakerConfig(
            fail_max=3,
            timeout_duration=30,
            success_threshold=1
        )
        
        assert config.fail_max == 3
        assert config.timeout_duration == 30
        assert config.success_threshold == 1


class TestCircuitBreaker:
    """Test CircuitBreaker class"""
    
    @pytest.fixture
    def breaker(self):
        """Create circuit breaker with test-friendly config"""
        config = CircuitBreakerConfig(
            fail_max=3,
            timeout_duration=1,  # Short timeout for testing
            success_threshold=2
        )
        return CircuitBreaker("test_circuit", config)
    
    @pytest.mark.asyncio
    async def test_closed_state_normal_operation(self, breaker):
        """Test normal operation in CLOSED state"""
        async def success_func():
            return "success"
        
        result = await breaker.call(success_func)
        assert result == "success"
        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0
    
    @pytest.mark.asyncio
    async def test_failure_accumulation(self, breaker):
        """Test failure count accumulates"""
        async def failing_func():
            raise Exception("Test failure")
        
        # First few failures should not open circuit
        for i in range(2):
            with pytest.raises(Exception):
                await breaker.call(failing_func)
            assert breaker.state == CircuitState.CLOSED
            assert breaker.failure_count == i + 1
        
        # Third failure should open circuit
        with pytest.raises(Exception):
            await breaker.call(failing_func)
        
        assert breaker.state == CircuitState.OPEN
        # Note: failure_count is reset when circuit opens (according to implementation logic)
    
    @pytest.mark.asyncio
    async def test_open_state_blocks_requests(self, breaker):
        """Test OPEN state blocks requests"""
        # Open the circuit
        for _ in range(3):
            async def failing_func():
                raise Exception("Test failure")
            try:
                await breaker.call(failing_func)
            except Exception:
                pass
        
        assert breaker.state == CircuitState.OPEN
        
        # Attempt should fail with CircuitBreakerOpenError
        async def test_func():
            return "should not execute"
        
        with pytest.raises(CircuitBreakerOpenError):
            await breaker.call(test_func)
    
    @pytest.mark.asyncio
    async def test_fallback_function(self, breaker):
        """Test fallback function when circuit is open"""
        # Open the circuit
        for _ in range(3):
            async def failing_func():
                raise Exception("Test failure")
            try:
                await breaker.call(failing_func)
            except Exception:
                pass
        
        async def test_func():
            return "should not execute"
        
        async def fallback_func():
            return "fallback result"
        
        # Should use fallback
        result = await breaker.call(test_func, fallback=fallback_func)
        assert result == "fallback result"
    
    @pytest.mark.asyncio
    async def test_fallback_value(self, breaker):
        """Test fallback value (not callable) when circuit is open"""
        # Open the circuit
        for _ in range(3):
            async def failing_func():
                raise Exception("Test failure")
            try:
                await breaker.call(failing_func)
            except Exception:
                pass
        
        async def test_func():
            return "should not execute"
        
        # Should return fallback value directly
        result = await breaker.call(test_func, fallback="default_value")
        assert result == "default_value"
    
    @pytest.mark.asyncio
    async def test_timeout_transition_to_half_open(self, breaker):
        """Test timeout causes transition from OPEN to HALF_OPEN"""
        # Open the circuit
        for _ in range(3):
            async def failing_func():
                raise Exception("Test failure")
            try:
                await breaker.call(failing_func)
            except Exception:
                pass
        
        assert breaker.state == CircuitState.OPEN
        
        # Wait for timeout
        await asyncio.sleep(1.1)  # Slightly more than timeout duration
        
        # Should transition to HALF_OPEN on next attempt
        async def test_func():
            return "success"
        
        result = await breaker.call(test_func)
        assert breaker.state == CircuitState.HALF_OPEN
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_half_open_recovery(self, breaker):
        """Test HALF_OPEN state recovery to CLOSED"""
        # Open the circuit
        for _ in range(3):
            async def failing_func():
                raise Exception("Test failure")
            try:
                await breaker.call(failing_func)
            except Exception:
                pass
        
        # Wait for timeout
        await asyncio.sleep(1.1)
        
        # Successful calls in HALF_OPEN should close circuit
        async def success_func():
            return "success"
        
        # First success
        await breaker.call(success_func)
        assert breaker.state == CircuitState.HALF_OPEN
        assert breaker.success_count == 1
        
        # Second success should close circuit
        await breaker.call(success_func)
        assert breaker.state == CircuitState.CLOSED
        assert breaker.success_count == 0
        assert breaker.failure_count == 0
    
    @pytest.mark.asyncio
    async def test_half_open_failure_returns_to_open(self, breaker):
        """Test failure in HALF_OPEN returns to OPEN"""
        # Open the circuit
        for _ in range(3):
            async def failing_func():
                raise Exception("Test failure")
            try:
                await breaker.call(failing_func)
            except Exception:
                pass
        
        # Wait for timeout
        await asyncio.sleep(1.1)
        
        # Failure in HALF_OPEN should return to OPEN
        async def failing_func():
            raise Exception("Still failing")
        
        with pytest.raises(Exception):
            await breaker.call(failing_func)
        
        assert breaker.state == CircuitState.OPEN
    
    @pytest.mark.asyncio
    async def test_excluded_exceptions(self, breaker):
        """Test excluded exceptions don't count as failures"""
        async def validation_error_func():
            raise ValueError("Validation error")
        
        # Excluded exceptions should not increment failure count
        for _ in range(5):  # More than fail_max
            with pytest.raises(ValueError):
                await breaker.call(validation_error_func)
        
        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0
    
    def test_get_state(self, breaker):
        """Test get_state returns current state"""
        state = breaker.get_state()
        
        assert "name" in state
        assert "state" in state
        assert "failure_count" in state
        assert "success_count" in state
        assert state["name"] == "test_circuit"
        assert state["state"] == CircuitState.CLOSED.value
    
    @pytest.mark.asyncio
    async def test_reset_on_success_closed(self, breaker):
        """Test failure count resets on success in CLOSED state"""
        # Cause some failures
        for _ in range(2):
            async def failing_func():
                raise Exception("Test failure")
            try:
                await breaker.call(failing_func)
            except Exception:
                pass
        
        assert breaker.failure_count == 2
        
        # Success should reset failure count
        async def success_func():
            return "success"
        
        await breaker.call(success_func)
        assert breaker.failure_count == 0


class TestCircuitBreakerDecorator:
    """Test circuit breaker decorator"""
    
    @pytest.mark.asyncio
    async def test_decorator_functionality(self):
        """Test circuit breaker decorator works"""
        config = CircuitBreakerConfig(fail_max=2, timeout_duration=1)
        decorator = circuit_breaker_decorator("decorated_circuit", config)
        
        call_count = 0
        
        @decorator
        async def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Failure")
            return "success"
        
        # First two calls should fail
        for _ in range(2):
            with pytest.raises(Exception):
                await test_func()
        
        # Wait for timeout
        await asyncio.sleep(1.1)
        
        # Next call should succeed (circuit in HALF_OPEN)
        result = await test_func()
        assert result == "success"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


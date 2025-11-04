# Action Recommendations - Test Suite Improvements

## Current Status

✅ **206 tests passing** (81.1%)  
⚠️ **46 tests failing** (18.3%)  
📝 **2 tests skipped** (0.8%)

---

## Priority 1: Fix High-Impact Test Failures

### 1.1 API Endpoint Tests (13 failures)

**Issue:** FastAPI `TestClient` has limitations with async endpoints and middleware.

**Recommendations:**
```python
# Option A: Use httpx.AsyncClient (Recommended)
import httpx
import pytest

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Option B: Better mocking for async endpoints
# Mock the agent workflow at a higher level
```

**Action Items:**
- [ ] Replace `TestClient` with `httpx.AsyncClient` in `test_api.py`
- [ ] Mock `ResearchOpsAgent.run()` instead of low-level NIM clients
- [ ] Add proper async context managers for test fixtures
- [ ] Mock FastAPI middleware (auth, metrics) to isolate endpoint logic

**Files to Modify:**
- `src/test_api.py` - Complete rewrite with httpx
- `src/api.py` - Add test fixtures support

**Estimated Time:** 2-3 hours

---

### 1.2 Rate Limiter Tests (6 failures)

**Issue:** Time-based assertions fail due to actual time passing.

**Recommendations:**
```python
# Use freezegun or time mocking
from freezegun import freeze_time

@freeze_time("2024-01-01 12:00:00")
def test_rate_limit_reset():
    # Test time-dependent logic
```

**Action Items:**
- [ ] Install `freezegun`: `pip install freezegun`
- [ ] Wrap rate limiter tests with `@freeze_time` decorator
- [ ] Mock `time.time()` in tests that check reset times
- [ ] Use `time.sleep()` mocking for timeout tests

**Files to Modify:**
- `src/test_auth.py` - Add time mocking
- Update `requirements.txt` or `pyproject.toml`

**Estimated Time:** 1 hour

---

## Priority 2: Integration Test Improvements

### 2.1 NIM Client Integration Tests (2 failures)

**Issue:** Tests require live NIM services running.

**Recommendations:**
```python
# Add conditional skipping with proper markers
@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("NIM_SERVICES_AVAILABLE"),
    reason="Requires live NIM services"
)
async def test_nim_connectivity():
    # Test with live services
```

**Action Items:**
- [ ] Mark integration tests with `@pytest.mark.integration`
- [ ] Add skip conditions based on environment variables
- [ ] Document how to run integration tests separately
- [ ] Create `pytest.ini` or `pyproject.toml` config to separate test suites

**Files to Modify:**
- `src/test_comprehensive_integration.py`
- `src/test_integration.py`
- `pyproject.toml` - Add pytest markers

**Estimated Time:** 30 minutes

---

### 2.2 Streamlit Component Tests (6 failures)

**Issue:** `test_narrative_loading.py` needs better Streamlit component mocking.

**Action Items:**
- [ ] Extend `MockStreamlit` class with missing components:
  - `container()` - Returns mock container
  - `empty()` - Returns placeholder
  - `progress()` - Progress bar mock
  - `spinner()` - Loading spinner mock
- [ ] Create shared `MockStreamlit` fixture in `conftest.py`
- [ ] Update narrative loading tests to use shared fixture

**Files to Modify:**
- `src/test_web_ui_features.py` - Enhance MockStreamlit
- `src/conftest.py` - Create shared fixtures (if doesn't exist)
- `src/test_narrative_loading.py` - Use shared mocks

**Estimated Time:** 1 hour

---

## Priority 3: Test Infrastructure Improvements

### 3.1 Create Shared Test Fixtures

**Action Items:**
- [ ] Create `src/conftest.py` with:
  - Shared MockStreamlit fixture
  - Mock NIM client fixtures
  - Test data fixtures (sample papers, queries)
  - Async test utilities
- [ ] Remove duplicate mock code from individual test files
- [ ] Standardize test data across test files

**Files to Create/Modify:**
- `src/conftest.py` - New file with shared fixtures
- All test files - Refactor to use shared fixtures

**Estimated Time:** 2 hours

---

### 3.2 Improve Test Coverage Reporting

**Action Items:**
- [ ] Run coverage: `pytest --cov=src --cov-report=html`
- [ ] Identify untested code paths
- [ ] Update `TEST_COVERAGE_REPORT.md` with coverage percentages
- [ ] Set coverage thresholds in `pyproject.toml`:
  ```toml
  [tool.coverage.run]
  source = ["src"]
  
  [tool.coverage.report]
  fail_under = 75
  ```

**Estimated Time:** 1 hour

---

## Priority 4: Documentation & Maintenance

### 4.1 Update Test Documentation

**Action Items:**
- [ ] Update `TEST_COVERAGE_REPORT.md` with:
  - Current test status (206 passing, 46 failing)
  - Known limitations and expected failures
  - How to run specific test suites
  - Integration test setup instructions
- [ ] Create `TESTING_GUIDE.md` with:
  - How to run all tests
  - How to run unit tests only
  - How to run integration tests
  - How to add new tests
  - Mock patterns and best practices

**Files to Create/Modify:**
- `TEST_COVERAGE_REPORT.md` - Update with current status
- `TESTING_GUIDE.md` - New comprehensive guide
- `README.md` - Add testing section link

**Estimated Time:** 1-2 hours

---

### 4.2 Add CI/CD Test Pipeline

**Action Items:**
- [ ] Create `.github/workflows/test.yml` (if using GitHub)
- [ ] Configure to run:
  - Unit tests on every PR
  - Integration tests on merge to main (if services available)
  - Coverage reports
  - Test result badges
- [ ] Add test status badges to README

**Estimated Time:** 1-2 hours

---

## Priority 5: Code Quality Improvements

### 5.1 Fix Remaining Edge Cases

**Action Items:**
- [ ] Review failing tests one by one:
  - `test_request_batcher.py::test_error_handling_in_batch` - Fix exception handling test
  - Various narrative loading tests - Improve mocking
  - Other edge cases
- [ ] Add tests for error scenarios:
  - Network timeouts
  - Service unavailability
  - Invalid inputs
  - Boundary conditions

**Estimated Time:** 2-3 hours

---

### 5.2 Add Missing Test Scenarios

**Action Items:**
- [ ] Add tests for:
  - Concurrent request handling
  - Cache invalidation edge cases
  - Circuit breaker recovery scenarios
  - Rate limiter burst capacity boundaries
  - Date filter edge cases (leap years, invalid dates)
  - Quality assessment with missing data
- [ ] Add property-based tests with Hypothesis for:
  - Input validation
  - Data transformations
  - Cache key generation

**Estimated Time:** 3-4 hours

---

## Quick Wins (High Impact, Low Effort)

### ✅ Immediate Actions (30 minutes each)

1. **Add pytest markers:**
   ```bash
   # Add to pyproject.toml
   [tool.pytest.ini_options]
   markers = [
       "integration: marks tests as integration tests",
       "slow: marks tests as slow running",
   ]
   ```

2. **Create simple test runner scripts:**
   ```bash
   # scripts/run_unit_tests.sh
   pytest src/test_*.py -v -m "not integration"
   
   # scripts/run_integration_tests.sh
   pytest src/test_*.py -v -m "integration"
   ```

3. **Add test count badge:**
   ```markdown
   ![Tests](https://img.shields.io/badge/tests-206%20passing%2C%2046%20failing-orange)
   ```

---

## Recommended Order of Execution

### Week 1: Critical Fixes
1. ✅ Fix rate limiter tests (Priority 1.2) - 1 hour
2. ✅ Fix API endpoint tests (Priority 1.1) - 2-3 hours
3. ✅ Create shared test fixtures (Priority 3.1) - 2 hours

### Week 2: Infrastructure
4. ✅ Improve Streamlit mocking (Priority 2.2) - 1 hour
5. ✅ Add integration test markers (Priority 2.1) - 30 min
6. ✅ Update documentation (Priority 4.1) - 1-2 hours

### Week 3: Polish
7. ✅ Fix remaining edge cases (Priority 5.1) - 2-3 hours
8. ✅ Add missing test scenarios (Priority 5.2) - 3-4 hours
9. ✅ Add CI/CD pipeline (Priority 4.2) - 1-2 hours

---

## Success Metrics

**Target Goals:**
- 📈 **250+ passing tests** (>90% pass rate)
- ✅ **<30 failing tests** (mostly integration tests)
- 📊 **75%+ code coverage**
- ⚡ **<5 minute test suite runtime**
- 📝 **Complete test documentation**

---

## Notes

- Most failing tests are in integration/edge cases, not core functionality
- Core business logic is well-tested (agents, filters, quality assessment)
- API tests need async client setup - consider using `httpx`
- Some tests may be intentionally skipped for hackathon demo
- Integration tests should be optional/skippable when services unavailable

---

## Resources

- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [httpx testing guide](https://www.python-httpx.org/testing/)
- [freezegun documentation](https://github.com/spulec/freezegun)
- [pytest fixtures best practices](https://docs.pytest.org/en/stable/fixture.html)


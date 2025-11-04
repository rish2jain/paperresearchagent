# Quick Action Recommendations

## 🎯 Immediate Actions (Do First)

### 1. Fix Rate Limiter Tests (30 min) ⚡
**Problem:** Time-based tests fail because real time passes.

**Fix:**
```bash
pip install freezegun
```

Then update `src/test_auth.py`:
```python
from freezegun import freeze_time

@freeze_time("2024-01-01 12:00:00")
def test_rate_limit_reset():
    # Tests now use frozen time
```

**Impact:** Fixes 6 failing tests immediately.

---

### 2. Create Shared Test Fixtures (1 hour) 🔧
**Problem:** Duplicate mock code across test files.

**Create `src/conftest.py`:**
```python
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_streamlit():
    """Shared Streamlit mock"""
    # ... existing MockStreamlit code ...
    pass

@pytest.fixture
def mock_nim_clients():
    """Shared NIM client mocks"""
    pass
```

**Impact:** Reduces code duplication, easier maintenance.

---

### 3. Mark Integration Tests (15 min) 📝
**Problem:** Integration tests fail without live services.

**Add to `pyproject.toml`:**
```toml
[tool.pytest.ini_options]
markers = [
    "integration: marks tests as integration tests (requires live services)",
    "slow: marks tests as slow running",
]
```

**Update integration test files:**
```python
@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("NIM_SERVICES_AVAILABLE"),
    reason="Requires live NIM services"
)
async def test_nim_connectivity():
    pass
```

**Impact:** Makes integration tests optional, prevents false failures.

---

## 🔥 High Priority (This Week)

### 4. Fix API Endpoint Tests (2-3 hours) 🌐
**Problem:** FastAPI TestClient doesn't work well with async endpoints.

**Solution:** Use `httpx.AsyncClient` instead:

```python
import httpx
import pytest

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_research_endpoint(async_client):
    response = await async_client.post("/research", json={"query": "test"})
    assert response.status_code == 200
```

**Impact:** Fixes 13 failing API tests.

---

### 5. Enhance Streamlit Mocking (1 hour) 🎨
**Problem:** Missing Streamlit components in mock.

**Add to `MockStreamlit` in `test_web_ui_features.py`:**
```python
def container(self, *args, **kwargs):
    return MockContainer()

def empty(self, *args, **kwargs):
    return MockEmpty()

def progress(self, value, *args, **kwargs):
    return None

def spinner(self, *args, **kwargs):
    return MockSpinner()
```

**Impact:** Fixes narrative loading tests.

---

## 📊 Medium Priority (This Month)

### 6. Add Test Coverage Reporting (30 min) 📈
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html --cov-report=term
```

Add to `pyproject.toml`:
```toml
[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
fail_under = 70
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
]
```

**Impact:** Track code coverage, identify untested areas.

---

### 7. Create Test Runner Scripts (15 min) 🚀
**Create `scripts/run_tests.sh`:**
```bash
#!/bin/bash
# Run all unit tests (skip integration)
PYTHONPATH=src:$PYTHONPATH pytest src/test_*.py -v -m "not integration"

# Run only integration tests
# PYTHONPATH=src:$PYTHONPATH pytest src/test_*.py -v -m "integration"
```

**Impact:** Easier test execution, faster feedback.

---

### 8. Update Documentation (1 hour) 📚
- Update `TEST_COVERAGE_REPORT.md` with current status
- Add testing section to `README.md`
- Document how to run different test suites

**Impact:** Better developer onboarding.

---

## 🎓 Learning & Best Practices

### 9. Add Property-Based Tests (Optional) 🧪
Use Hypothesis for input validation:
```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=500))
def test_query_validation(query):
    # Test with random valid inputs
    assert len(query) > 0
```

---

### 10. Add CI/CD Pipeline (Optional) 🔄
Create `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -e ".[dev]"
      - run: pytest --cov=src
```

---

## 📋 Priority Order Checklist

- [ ] **Week 1:** Fix rate limiter tests (30 min)
- [ ] **Week 1:** Create shared fixtures (1 hour)
- [ ] **Week 1:** Mark integration tests (15 min)
- [ ] **Week 2:** Fix API endpoint tests (2-3 hours)
- [ ] **Week 2:** Enhance Streamlit mocking (1 hour)
- [ ] **Week 3:** Add coverage reporting (30 min)
- [ ] **Week 3:** Create test scripts (15 min)
- [ ] **Week 3:** Update documentation (1 hour)

---

## 🎯 Success Metrics

**Current:**
- ✅ 206 passing tests (81.7%)
- ⚠️ 46 failing tests (18.3%)

**Target:**
- ✅ 240+ passing tests (>90%)
- ⚠️ <30 failing tests (mostly integration)
- 📊 70%+ code coverage

---

## 💡 Quick Wins

1. **Add pytest markers** - 5 minutes
2. **Create test runner script** - 10 minutes  
3. **Update TEST_COVERAGE_REPORT.md** - 15 minutes
4. **Add test badges to README** - 5 minutes

**Total: 35 minutes for significant improvements!**

---

## 📚 Resources

- [pytest-asyncio docs](https://pytest-asyncio.readthedocs.io/)
- [httpx testing](https://www.python-httpx.org/testing/)
- [freezegun docs](https://github.com/spulec/freezegun)


# Testing Action Plan - Priority Implementation Guide
**ResearchOps Agent Testing Improvement Roadmap**

---

## 🔴 CRITICAL - Fix Before Hackathon Submission

### Action 1: Fix Import Configuration (2-3 hours)
**Status:** 🔴 BLOCKING - 65% of tests currently non-executable

#### Problem
All test files use direct imports that fail during pytest collection:
```python
from agents import ResearchOpsAgent  # FAILS
```

#### Solution Options

**Option A: Update Test Imports (Recommended)**
```python
# Change all test files from:
from agents import ResearchOpsAgent

# To:
from src.agents import ResearchOpsAgent
```

**Pros:** Clean, follows Python package conventions
**Cons:** Requires editing 13 test files

**Option B: Update PYTHONPATH in pytest.ini**
```ini
[pytest]
pythonpath = src
testpaths = src
```

**Pros:** No test file changes needed
**Cons:** May cause issues with different execution contexts

**Option C: Add __init__.py to src/ (NOT RECOMMENDED)**
- Makes src/ a package
- May conflict with existing structure

#### Implementation Steps
1. Create `conftest.py` in project root:
```python
# conftest.py
import sys
from pathlib import Path

# Add src to Python path for test imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
```

2. Update `pyproject.toml`:
```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["src"]
```

3. Verify:
```bash
python -m pytest src/ --collect-only
# Should show: "collected 75 items" with NO errors
```

4. Run tests:
```bash
python -m pytest src/ -v
```

#### Acceptance Criteria
- [ ] `pytest src/ --collect-only` shows 0 errors
- [ ] All 75 tests can be collected
- [ ] At least 90% of unit tests pass

---

### Action 2: Paper Source Integration Tests (8-10 hours)
**Status:** 🔴 CRITICAL - Zero coverage of external integrations

#### Required Test File: `test_paper_sources.py`

```python
"""
Paper Source Integration Tests
Tests all 7 academic paper sources with realistic scenarios
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from agents import ScoutAgent

class TestArXivIntegration:
    """Test arXiv API integration"""

    @pytest.mark.asyncio
    async def test_arxiv_search_success(self):
        """Test successful arXiv search"""
        scout = ScoutAgent(Mock())

        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock successful response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text = AsyncMock(return_value=ARXIV_XML_RESPONSE)
            mock_get.return_value.__aenter__.return_value = mock_response

            results = await scout._search_arxiv("machine learning", max_results=10)

            assert len(results) > 0
            assert all(hasattr(p, 'title') for p in results)
            assert all(hasattr(p, 'abstract') for p in results)

    @pytest.mark.asyncio
    async def test_arxiv_rate_limiting(self):
        """Test arXiv rate limit handling"""
        scout = ScoutAgent(Mock())

        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock 429 Too Many Requests
            mock_response = AsyncMock()
            mock_response.status = 429
            mock_get.return_value.__aenter__.return_value = mock_response

            # Should retry with backoff, not crash
            results = await scout._search_arxiv("test", max_results=5)

            # Should return empty or cached results, not raise exception
            assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_arxiv_malformed_response(self):
        """Test handling of malformed arXiv XML"""
        scout = ScoutAgent(Mock())

        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock malformed XML
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text = AsyncMock(return_value="<invalid>xml</invalid>")
            mock_get.return_value.__aenter__.return_value = mock_response

            results = await scout._search_arxiv("test", max_results=5)

            # Should handle gracefully
            assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_arxiv_timeout(self):
        """Test arXiv request timeout handling"""
        scout = ScoutAgent(Mock())

        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock timeout
            mock_get.side_effect = asyncio.TimeoutError()

            results = await scout._search_arxiv("test", max_results=5)

            # Should not crash
            assert isinstance(results, list)


class TestPubMedIntegration:
    """Test PubMed API integration"""

    @pytest.mark.asyncio
    async def test_pubmed_search_success(self):
        """Test successful PubMed search"""
        # Similar structure to arXiv tests
        pass

    @pytest.mark.asyncio
    async def test_pubmed_authentication(self):
        """Test PubMed API key handling"""
        # Test with/without API key
        pass

    @pytest.mark.asyncio
    async def test_pubmed_pagination(self):
        """Test PubMed result pagination"""
        # Test fetching multiple pages
        pass


class TestSemanticScholarIntegration:
    """Test Semantic Scholar API integration"""

    @pytest.mark.asyncio
    async def test_semantic_scholar_search(self):
        """Test Semantic Scholar search"""
        pass

    @pytest.mark.asyncio
    async def test_semantic_scholar_rate_limiting(self):
        """Test rate limiting with/without API key"""
        pass


class TestCrossrefIntegration:
    """Test Crossref API integration"""

    @pytest.mark.asyncio
    async def test_crossref_search(self):
        """Test Crossref metadata search"""
        pass


class TestIEEEIntegration:
    """Test IEEE Xplore API integration"""

    @pytest.mark.asyncio
    async def test_ieee_requires_api_key(self):
        """Test IEEE requires valid API key"""
        pass

    @pytest.mark.asyncio
    async def test_ieee_authenticated_search(self):
        """Test IEEE search with API key"""
        pass


class TestACMIntegration:
    """Test ACM Digital Library integration"""

    @pytest.mark.asyncio
    async def test_acm_requires_api_key(self):
        """Test ACM requires valid API key"""
        pass


class TestSpringerIntegration:
    """Test Springer API integration"""

    @pytest.mark.asyncio
    async def test_springer_requires_api_key(self):
        """Test Springer requires valid API key"""
        pass


class TestMultiSourceCoordination:
    """Test parallel source searching and deduplication"""

    @pytest.mark.asyncio
    async def test_parallel_source_search(self):
        """Test Scout queries all enabled sources in parallel"""
        scout = ScoutAgent(Mock())

        # Mock all source methods
        with patch.object(scout, '_search_arxiv', new_callable=AsyncMock) as mock_arxiv, \
             patch.object(scout, '_search_pubmed', new_callable=AsyncMock) as mock_pubmed, \
             patch.object(scout, '_search_semantic_scholar', new_callable=AsyncMock) as mock_ss:

            mock_arxiv.return_value = [Mock(id="arxiv1")]
            mock_pubmed.return_value = [Mock(id="pubmed1")]
            mock_ss.return_value = [Mock(id="ss1")]

            results = await scout.search("test query", max_papers=10)

            # All sources should be called (parallel execution)
            assert mock_arxiv.called
            assert mock_pubmed.called
            assert mock_ss.called

            # Results should be merged
            assert len(results) == 3

    @pytest.mark.asyncio
    async def test_source_deduplication(self):
        """Test duplicate papers from multiple sources are removed"""
        scout = ScoutAgent(Mock())

        # Mock same paper from different sources (same DOI/title)
        duplicate_paper = Paper(
            id="different_id",
            title="Same Paper",
            doi="10.1234/same",
            abstract="Same abstract",
            authors=["Author"]
        )

        with patch.object(scout, '_search_arxiv', new_callable=AsyncMock) as mock_arxiv, \
             patch.object(scout, '_search_pubmed', new_callable=AsyncMock) as mock_pubmed:

            mock_arxiv.return_value = [duplicate_paper]
            mock_pubmed.return_value = [duplicate_paper]  # Same paper

            results = await scout.search("test", max_papers=10)

            # Should deduplicate to 1 paper
            assert len(results) == 1

    @pytest.mark.asyncio
    async def test_partial_source_failure(self):
        """Test system continues if some sources fail"""
        scout = ScoutAgent(Mock())

        with patch.object(scout, '_search_arxiv', new_callable=AsyncMock) as mock_arxiv, \
             patch.object(scout, '_search_pubmed', new_callable=AsyncMock) as mock_pubmed:

            mock_arxiv.return_value = [Mock(id="paper1")]
            mock_pubmed.side_effect = Exception("PubMed unavailable")

            # Should not crash, should return arXiv results
            results = await scout.search("test", max_papers=10)

            assert len(results) == 1
            assert results[0].id == "paper1"


# Test data fixtures
ARXIV_XML_RESPONSE = """
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2301.12345</id>
    <title>Test Paper Title</title>
    <summary>Test abstract content</summary>
    <author><name>Test Author</name></author>
  </entry>
</feed>
"""

PUBMED_JSON_RESPONSE = {
    "result": {
        "uids": ["12345"],
        "12345": {
            "title": "Test Paper",
            "abstract": "Test abstract",
            "authors": [{"name": "Test Author"}]
        }
    }
}
```

#### Implementation Steps
1. Create `test_paper_sources.py` with above structure
2. Add mock response fixtures for each source
3. Test happy path for each source
4. Test error scenarios (rate limits, timeouts, malformed data)
5. Test parallel coordination and deduplication

#### Acceptance Criteria
- [ ] Tests for all 7 sources (arXiv, PubMed, Semantic Scholar, Crossref, IEEE, ACM, Springer)
- [ ] Happy path tests passing
- [ ] Error handling tests passing
- [ ] Parallel coordination tests passing
- [ ] Deduplication tests passing

---

### Action 3: Verify Comprehensive Integration Tests (1 hour)
**Status:** 🔴 CRITICAL - Must pass before demo

#### Steps
1. Fix imports (Action 1)
2. Run comprehensive integration test:
```bash
python -m pytest src/test_comprehensive_integration.py -v
```

3. If failures, fix and retest:
```bash
# With demo mode (faster):
DEMO_MODE=true python -m pytest src/test_comprehensive_integration.py -v

# With live NIMs (requires NIMs running):
python -m pytest src/test_comprehensive_integration.py -v
```

4. Verify all test classes pass:
- TestNIMConnectivity
- TestCircuitBreaker
- TestInputSanitization
- TestRateLimiting
- TestAuthentication
- TestAgentWorkflow
- TestErrorHandling
- TestDecisionLogging
- TestProductionReadiness

#### Acceptance Criteria
- [ ] All 15+ integration tests pass with demo mode
- [ ] At least 80% pass with live NIMs
- [ ] No unhandled exceptions
- [ ] Decision logging works correctly

---

## 🟡 HIGH PRIORITY - Before Production Deployment

### Action 4: E2E Web UI Tests (6-8 hours)
**Status:** 🟡 HIGH - User-facing interface untested

#### Required Tool: Playwright
```bash
pip install playwright pytest-playwright
playwright install chromium
```

#### Test File: `test_web_ui_e2e.py`
```python
import pytest
from playwright.sync_api import Page, expect

def test_search_form_submission(page: Page):
    """Test user can submit search form"""
    page.goto("http://localhost:8501")

    # Fill form
    page.fill('input[aria-label="Query"]', "machine learning")
    page.select_option('select[aria-label="Max Papers"]', "10")

    # Submit
    page.click('button:has-text("Search")')

    # Wait for results
    expect(page.locator('.stAlert')).to_contain_text("Searching")

def test_result_display(page: Page):
    """Test search results display correctly"""
    page.goto("http://localhost:8501")

    # Perform search
    page.fill('input[aria-label="Query"]', "test")
    page.click('button:has-text("Search")')

    # Verify results appear
    expect(page.locator('.paper-title')).to_be_visible()
    expect(page.locator('.paper-abstract')).to_be_visible()

def test_export_functionality(page: Page):
    """Test BibTeX export works"""
    page.goto("http://localhost:8501")

    # Get results
    page.fill('input[aria-label="Query"]', "test")
    page.click('button:has-text("Search")')

    # Click export
    with page.expect_download() as download_info:
        page.click('button:has-text("Export BibTeX")')

    download = download_info.value
    assert download.suggested_filename.endswith('.bib')

def test_error_message_display(page: Page):
    """Test error messages display to user"""
    page.goto("http://localhost:8501")

    # Submit empty form
    page.click('button:has-text("Search")')

    # Verify error shown
    expect(page.locator('.stAlert')).to_contain_text("error", ignore_case=True)

def test_sse_stream_visualization(page: Page):
    """Test SSE events update UI in real-time"""
    page.goto("http://localhost:8501")

    page.fill('input[aria-label="Query"]', "test")
    page.click('button:has-text("Search")')

    # Wait for progress updates
    expect(page.locator('.progress-bar')).to_be_visible()

    # Verify stages appear
    expect(page.locator('text=/Searching|Analyzing|Synthesizing/')).to_be_visible()
```

#### Acceptance Criteria
- [ ] Form submission works
- [ ] Results display correctly
- [ ] Export functionality works
- [ ] Error messages display
- [ ] SSE stream updates UI

---

### Action 5: Error Recovery Tests (4-6 hours)
**Status:** 🟡 HIGH - Production resilience untested

#### Test File: `test_error_recovery.py`
```python
"""
Error Recovery and Resilience Tests
Tests graceful degradation and error handling
"""

class TestNIMFailureRecovery:
    """Test system handles NIM failures gracefully"""

    @pytest.mark.asyncio
    async def test_reasoning_nim_timeout_fallback(self):
        """Test agent handles reasoning NIM timeout"""
        # Mock reasoning NIM to timeout
        # Verify agent uses fallback strategy
        pass

    @pytest.mark.asyncio
    async def test_embedding_nim_failure_degradation(self):
        """Test agent continues without embeddings if NIM fails"""
        # Mock embedding NIM to fail
        # Verify agent returns results without semantic clustering
        pass

    @pytest.mark.asyncio
    async def test_both_nims_down_graceful_error(self):
        """Test system shows helpful error when NIMs unavailable"""
        # Mock both NIMs down
        # Verify error message guides user to check NIM status
        pass

class TestNetworkFailureRecovery:
    """Test network failure handling"""

    @pytest.mark.asyncio
    async def test_transient_network_error_retry(self):
        """Test system retries on transient network errors"""
        pass

    @pytest.mark.asyncio
    async def test_persistent_network_error_timeout(self):
        """Test system times out after max retries"""
        pass

class TestPartialFailureHandling:
    """Test partial failure scenarios"""

    @pytest.mark.asyncio
    async def test_some_papers_fail_analysis(self):
        """Test system continues if some papers fail analysis"""
        pass

    @pytest.mark.asyncio
    async def test_synthesis_with_limited_data(self):
        """Test synthesizer handles < 3 papers gracefully"""
        pass
```

#### Acceptance Criteria
- [ ] NIM timeout handling tested
- [ ] Network failure retry tested
- [ ] Graceful degradation verified
- [ ] Partial failure handling tested

---

### Action 6: Config Validation Tests (2-3 hours)
**Status:** 🟡 HIGH - Config errors can break deployment

#### Test File: `test_config.py`
```python
"""
Configuration Validation Tests
Tests config loading, validation, and error handling
"""

class TestConfigLoading:
    """Test configuration loading"""

    def test_load_default_config(self):
        """Test default config loads successfully"""
        from config import Config
        config = Config.from_env()

        assert config.nim.reasoning_nim_url is not None
        assert config.nim.embedding_nim_url is not None

    def test_load_custom_config(self):
        """Test custom config overrides defaults"""
        import os
        os.environ['REASONING_NIM_URL'] = 'http://custom:8000'

        from config import Config
        config = Config.from_env()

        assert config.nim.reasoning_nim_url == 'http://custom:8000'

    def test_invalid_config_raises_error(self):
        """Test invalid config raises validation error"""
        import os
        os.environ['MAX_PAPERS'] = 'invalid'  # Not an integer

        from config import Config
        with pytest.raises(ValueError):
            config = Config.from_env()

class TestPaperSourceConfig:
    """Test paper source configuration"""

    def test_all_sources_enabled_by_default(self):
        """Test free sources enabled by default"""
        pass

    def test_paid_sources_require_api_keys(self):
        """Test paid sources disabled without API keys"""
        pass
```

#### Acceptance Criteria
- [ ] Default config loads
- [ ] Custom overrides work
- [ ] Invalid config raises errors
- [ ] Source config validated

---

## 🟢 MEDIUM PRIORITY - Quality Improvements

### Action 7: Performance Benchmarks (4-6 hours)
Create `test_performance.py` with response time baselines

### Action 8: Edge Case Coverage (6-8 hours)
Expand existing tests with edge cases

### Action 9: Test Refactoring (3-4 hours)
Extract common fixtures to `conftest.py`

---

## 🔵 LOW PRIORITY - Enhancements

### Action 10: CI/CD Integration (2-3 hours)
Create `.github/workflows/test.yml`

### Action 11: Missing Module Tests (8-10 hours)
Test bias_detection, boolean_search, etc.

---

## Quick Reference Implementation Order

**Sprint 1 (Pre-Hackathon):**
1. Fix imports (2-3h)
2. Paper sources (8-10h)
3. Verify integration (1h)
**Total: 11-14 hours**

**Sprint 2 (Pre-Production):**
4. E2E web UI (6-8h)
5. Error recovery (4-6h)
6. Config validation (2-3h)
**Total: 12-17 hours**

**Sprint 3 (Quality):**
7. Performance (4-6h)
8. Edge cases (6-8h)
9. Refactoring (3-4h)
**Total: 13-18 hours**

**Sprint 4 (Enhancement):**
10. CI/CD (2-3h)
11. Missing modules (8-10h)
**Total: 10-13 hours**

**TOTAL EFFORT: 46-62 hours**

---

## Success Metrics

### Pre-Hackathon Success Criteria
- [ ] 0 import errors in pytest collection
- [ ] >90% unit tests passing
- [ ] Integration tests passing with demo mode
- [ ] Paper source tests covering all 7 sources
- [ ] Test execution documented in CLAUDE.md

### Production-Ready Success Criteria
- [ ] >80% line coverage
- [ ] >70% branch coverage
- [ ] All E2E tests passing
- [ ] Error recovery tests passing
- [ ] Performance benchmarks established
- [ ] CI/CD pipeline running tests

### Quality Success Criteria
- [ ] Test execution < 5 minutes (unit)
- [ ] Test execution < 15 minutes (integration)
- [ ] Zero flaky tests
- [ ] Test documentation complete
- [ ] Code review passing

---

**Document Created:** 2025-11-03
**Priority Level:** CRITICAL
**Next Review:** After Sprint 1 completion

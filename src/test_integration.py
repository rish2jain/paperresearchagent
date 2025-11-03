"""
Integration Test Script
Tests NIM connectivity and agent functionality
"""

import asyncio
import sys
from nim_clients import ReasoningNIMClient, EmbeddingNIMClient
from agents import ResearchOpsAgent

async def test_reasoning_nim():
    """Test Reasoning NIM connectivity"""
    print("Testing Reasoning NIM...")
    try:
        async with ReasoningNIMClient() as client:
            result = await client.complete("Hello, are you working?", max_tokens=50)
            print(f"✅ Reasoning NIM: Connected")
            print(f"   Response: {result[:100]}...")
            return True
    except Exception as e:
        print(f"❌ Reasoning NIM: Failed - {e}")
        return False


async def test_embedding_nim():
    """Test Embedding NIM connectivity"""
    print("\nTesting Embedding NIM...")
    try:
        async with EmbeddingNIMClient() as client:
            embedding = await client.embed("test text")
            print(f"✅ Embedding NIM: Connected")
            print(f"   Embedding dimension: {len(embedding)}")
            return True
    except Exception as e:
        print(f"❌ Embedding NIM: Failed - {e}")
        return False


async def test_agent_workflow():
    """Test full agent workflow"""
    print("\nTesting Agent Workflow...")
    try:
        async with ReasoningNIMClient() as reasoning, \
                    EmbeddingNIMClient() as embedding:

            agent = ResearchOpsAgent(reasoning, embedding)
            result = await agent.run("test query")

            print(f"✅ Agent Workflow: Success")
            print(f"   Papers found: {result['papers_analyzed']}")
            print(f"   Themes: {len(result['common_themes'])}")
            return True
    except Exception as e:
        print(f"❌ Agent Workflow: Failed - {e}")
        return False


async def main():
    """Run all tests"""
    print("="*60)
    print("NVIDIA NIM Integration Tests")
    print("="*60)

    results = []

    # Test individual NIMs
    results.append(await test_reasoning_nim())
    results.append(await test_embedding_nim())

    # Test full workflow
    results.append(await test_agent_workflow())

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✅ All tests passed! System is ready.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check configuration.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

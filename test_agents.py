#!/usr/bin/env python3
"""
Test script for Federal Job Advisory Agent System
Verifies Ollama connection and basic agent functionality
"""

import asyncio
import httpx
import json
from datetime import datetime


async def test_ollama_direct():
    """Test direct Ollama connection"""
    print("\n🔍 Testing Ollama Direct Connection...")
    
    try:
        import ollama
        client = ollama.Client()
        
        response = client.generate(
            model="gptFREE",
            prompt="Complete this: Federal jobs require"
        )
        
        print("✅ Ollama connected successfully")
        print(f"   Response: {response['response'][:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("   Try: ollama serve")
        return False


async def test_api_health():
    """Test API health endpoint"""
    print("\n🔍 Testing API Health...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8001/health")
            if response.status_code == 200:
                print("✅ API is healthy")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ API returned status {response.status_code}")
                return False
                
        except httpx.ConnectError:
            print("❌ Cannot connect to API at localhost:8001")
            print("   Try: python main.py")
            return False


async def test_list_agents():
    """Test listing available agents"""
    print("\n🔍 Testing Agent List...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8001/agents")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Found {data['total']} agents")
                for role, info in data['agents'].items():
                    print(f"   - {role}: {info['class']}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Failed to list agents: {e}")
            return False


async def test_data_scientist_agent():
    """Test Data Scientist agent analysis"""
    print("\n🔍 Testing Data Scientist Agent...")
    
    test_data = {
        "user_id": "test_user_001",
        "skills": ["Python", "R", "SQL", "Machine Learning", "TensorFlow"],
        "experience": "5 years of experience in data science, including 2 years working on federal contracts. Led machine learning projects for fraud detection and risk assessment. Published 3 papers on statistical modeling.",
        "projects": [
            {
                "name": "Fraud Detection System",
                "description": "Developed ML model that reduced fraud by 35% saving $2M annually"
            },
            {
                "name": "Customer Segmentation",
                "description": "Created clustering algorithm for 1M+ customer records"
            }
        ],
        "education": {
            "degree": "MS",
            "field": "Data Science"
        },
        "target_grade": "GS-13"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "http://localhost:8001/agents/data-scientist/analyze",
                json=test_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Data Scientist agent responded successfully")
                print(f"   Success: {result.get('success', False)}")
                if result.get('data'):
                    print(f"   Response preview: {str(result['data'])[:200]}...")
                return True
            else:
                print(f"❌ Agent returned status {response.status_code}")
                return False
                
        except httpx.TimeoutException:
            print("⚠️  Agent response timed out (this may be normal for first run)")
            return False
        except Exception as e:
            print(f"❌ Agent test failed: {e}")
            return False


async def test_essay_compliance():
    """Test Essay Guidance agent"""
    print("\n🔍 Testing Essay Guidance Agent...")
    
    test_data = {
        "user_id": "test_user_001",
        "essay_text": """When I served as a data analyst at the Census Bureau, 
        I was tasked with improving data collection efficiency. I implemented 
        a new validation system that reduced errors by 40%. As a result, 
        we saved 200 hours of manual review time monthly.""",
        "essay_number": 2,  # Government Efficiency essay
        "experience": "Federal data analyst with Census Bureau experience"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "http://localhost:8001/agents/essay/analyze",
                json=test_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Essay Guidance agent responded successfully")
                print(f"   Success: {result.get('success', False)}")
                
                # Check for compliance reminder
                if result.get('data', {}).get('compliance_reminder'):
                    print("   ✓ Compliance warnings included")
                    
                return True
            else:
                print(f"❌ Agent returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Essay agent test failed: {e}")
            return False


async def test_streaming():
    """Test streaming response"""
    print("\n🔍 Testing Streaming Response...")
    
    test_data = {
        "role": "data_scientist",
        "user_id": "test_user_001",
        "query": "What skills should I highlight for a GS-13 data scientist position?",
        "stream": True
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            async with client.stream(
                "POST",
                "http://localhost:8001/agents/process",
                json=test_data
            ) as response:
                if response.status_code == 200:
                    print("✅ Streaming response received")
                    chunks_received = 0
                    
                    async for line in response.aiter_lines():
                        if line:
                            chunks_received += 1
                            if chunks_received <= 3:  # Show first 3 chunks
                                chunk_data = json.loads(line)
                                print(f"   Chunk {chunks_received}: {chunk_data.get('chunk', '')[:50]}")
                    
                    print(f"   Total chunks: {chunks_received}")
                    return True
                    
                return False
                
        except Exception as e:
            print(f"❌ Streaming test failed: {e}")
            return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("Federal Job Advisory Agent System - Test Suite")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")
    
    # Track results
    results = {}
    
    # Run tests
    results["ollama"] = await test_ollama_direct()
    
    if not results["ollama"]:
        print("\n⚠️  Ollama not running. Starting remaining API tests...")
    
    results["health"] = await test_api_health()
    
    if results["health"]:
        results["list"] = await test_list_agents()
        results["data_scientist"] = await test_data_scientist_agent()
        results["essay"] = await test_essay_compliance()
        results["streaming"] = await test_streaming()
    else:
        print("\n⚠️  API not running. Skipping agent tests.")
        results["list"] = False
        results["data_scientist"] = False
        results["essay"] = False
        results["streaming"] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test:20} {status}")
    
    print("-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
    elif results["health"]:
        print("\n⚠️  Some tests failed, but API is running.")
    else:
        print("\n❌ System not fully operational. Check services.")
    
    print(f"\nCompleted: {datetime.now().isoformat()}")


if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Quick test script for agent system with llama3.1:70b
"""

import asyncio
import json
from ollama import Client
from typing import Dict, Any

# Test Ollama connection
def test_ollama_connection():
    """Test if Ollama is accessible"""
    try:
        client = Client()
        models = client.list()
        print("✅ Ollama Connected!")
        print("Available models:")
        for model in models['models']:
            print(f"  - {model['name']} ({model['size'] / 1e9:.1f}GB)")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

# Test a simple agent task
async def test_agent_task():
    """Test a simple agent task with llama3.1:70b"""
    try:
        client = Client()
        
        # Backend engineer test
        print("\n🔧 Testing Backend Engineer Agent...")
        response = client.generate(
            model='llama3.1:70b',
            prompt="""You are a senior backend engineer. 
            Create a simple FastAPI endpoint for user registration with email validation.
            Provide only the code, no explanations.""",
            options={
                'temperature': 0.7,
                'num_ctx': 4096
            }
        )
        
        print("Response received:")
        print(response['response'][:500] + "..." if len(response['response']) > 500 else response['response'])
        
        # Data scientist test
        print("\n📊 Testing Data Scientist Agent...")
        response = client.generate(
            model='llama3.1:70b',
            prompt="""You are a senior data scientist.
            Explain how to perform A/B test analysis with statistical significance.
            Be concise.""",
            options={
                'temperature': 0.7,
                'num_ctx': 4096
            }
        )
        
        print("Response received:")
        print(response['response'][:500] + "..." if len(response['response']) > 500 else response['response'])
        
        return True
        
    except Exception as e:
        print(f"❌ Agent task failed: {e}")
        return False

# Test model comparison
async def test_model_comparison():
    """Compare different models on same task"""
    models_to_test = ['llama3.1:70b', 'gptFREE:latest']
    task = "Write a Python function to validate email addresses using regex"
    
    print(f"\n🔬 Comparing models on task: {task}")
    print("=" * 60)
    
    client = Client()
    results = {}
    
    for model in models_to_test:
        try:
            print(f"\nTesting {model}...")
            import time
            start = time.time()
            
            response = client.generate(
                model=model,
                prompt=f"You are an expert programmer. {task}. Provide only the code.",
                options={'temperature': 0.7}
            )
            
            elapsed = time.time() - start
            
            results[model] = {
                'response': response['response'][:300],
                'time': elapsed,
                'eval_count': response.get('eval_count', 0)
            }
            
            print(f"✓ Completed in {elapsed:.2f}s")
            
        except Exception as e:
            print(f"✗ Failed: {e}")
            results[model] = {'error': str(e)}
    
    # Compare results
    print("\n📊 Comparison Results:")
    print("-" * 60)
    for model, result in results.items():
        if 'error' not in result:
            print(f"\n{model}:")
            print(f"  Time: {result['time']:.2f}s")
            print(f"  Tokens: {result.get('eval_count', 'N/A')}")
            print(f"  Output preview: {result['response'][:100]}...")
    
    return results

# Main execution
async def main():
    print("🚀 Virtual Development Team - Quick Test")
    print("=" * 60)
    
    # Test 1: Ollama connection
    if not test_ollama_connection():
        print("Please ensure Ollama is running: 'ollama serve'")
        return
    
    # Test 2: Agent tasks
    await test_agent_task()
    
    # Test 3: Model comparison
    await test_model_comparison()
    
    print("\n✅ All tests completed!")
    print("\nNext steps:")
    print("1. Run the full controller: python claude_code_controller.py")
    print("2. Access API at: http://localhost:8002/docs")
    print("3. Run A/B tests: streamlit run app/testing/ab_test_dashboard.py")

if __name__ == "__main__":
    asyncio.run(main())
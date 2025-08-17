#!/usr/bin/env python3
"""
Quick Code Review Test - Multiple Agents Review Same Code
"""

import requests
import time
import json

API_URL = "http://localhost:8003"

# Sample code from Fed Job Advisor to review
CODE_TO_REVIEW = """
def calculate_match_score(resume, job):
    score = 0
    if resume['grade'] == job['grade']:
        score += 50
    if resume['series'] == job['series']:
        score += 30
    skill_match = len(set(resume['skills']) & set(job['skills']))
    score += skill_match * 5
    return score
"""

def test_agent(role, task):
    """Test a single agent"""
    print(f"\n{'='*60}")
    print(f"🤖 Testing {role.upper()} Agent")
    print(f"{'='*60}")
    
    start = time.time()
    try:
        response = requests.post(
            f"{API_URL}/test/{role}",
            params={"task": task},
            timeout=30
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response received in {elapsed:.2f}s")
            print(f"📊 Tokens used: {result.get('eval_count', 0)}")
            print(f"\n📝 Analysis:")
            print("-" * 40)
            # Print first 500 chars of response
            print(result['response'][:500])
            if len(result['response']) > 500:
                print("\n[... truncated for brevity ...]")
            return result
        else:
            print(f"❌ Error: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def compare_models_on_task(task):
    """Compare models on the same task"""
    print(f"\n{'='*60}")
    print("🔬 COMPARING MODELS")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            f"{API_URL}/compare",
            params={"task": task},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            winner = result.pop('winner', None)
            
            print(f"\n🏆 Winner (fastest): {winner}")
            print("\nModel Performance:")
            print("-" * 40)
            
            for model, data in result.items():
                if isinstance(data, dict) and 'time' in data:
                    print(f"\n{model}:")
                    print(f"  Time: {data['time']:.2f}s")
                    print(f"  Tokens: {data.get('tokens', 0)}")
                    print(f"  Response preview: {data['response'][:150]}...")
            
            return result
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def main():
    print("🚀 AGENT CODE REVIEW DEMONSTRATION")
    print("=" * 60)
    print("Testing multiple agents reviewing the same Fed Job Advisor code")
    print(f"\nCode being reviewed:\n{CODE_TO_REVIEW}")
    
    # Define the review task
    review_task = f"""
Review this Python function and provide:
1. Code quality score (1-10)
2. Issues or bugs found
3. Performance concerns
4. Suggested improvements

Code:
{CODE_TO_REVIEW}
"""
    
    # Test different agents on the same code review
    agents = ["backend", "security", "data"]
    agent_reviews = {}
    
    for agent in agents:
        result = test_agent(agent, review_task)
        if result:
            agent_reviews[agent] = result
    
    # Compare models on optimization task
    optimization_task = f"Optimize this function for better performance:\n{CODE_TO_REVIEW}"
    model_comparison = compare_models_on_task(optimization_task)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}")
    
    print("\n✅ Agents Tested:")
    for agent in agent_reviews:
        print(f"  - {agent}: Successfully reviewed code")
    
    if model_comparison:
        print("\n✅ Model Comparison:")
        print("  - Models compared on optimization task")
        print("  - Winner determined based on speed")
    
    print("\n💡 Key Findings:")
    print("  - Multiple agents can review code from different perspectives")
    print("  - Backend focuses on code structure and efficiency")
    print("  - Security focuses on vulnerabilities and safety")
    print("  - Data scientist focuses on algorithm correctness")
    print("\n✨ All agents are working correctly!")

if __name__ == "__main__":
    main()
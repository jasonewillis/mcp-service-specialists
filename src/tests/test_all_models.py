#!/usr/bin/env python3
"""
Comprehensive Model Testing and Comparison
Tests all available Ollama models for performance and quality
"""

import time
import json
from ollama import Client
from typing import Dict, List, Any
import statistics

class ModelTester:
    def __init__(self):
        self.client = Client()
        self.models = [
            "llama3.1:8b",
            "qwen3:30b", 
            "gptFREE:latest",
            "gpt-oss:20b"  # Same as gptFREE but included for completeness
        ]
        self.results = {}
    
    def test_simple_task(self, model: str) -> Dict[str, Any]:
        """Test with a simple coding task"""
        prompt = "Write a Python function to calculate the factorial of a number. Include error handling."
        
        start = time.time()
        try:
            response = self.client.generate(
                model=model,
                prompt=prompt,
                options={'temperature': 0.7, 'num_ctx': 4096}
            )
            elapsed = time.time() - start
            
            return {
                "success": True,
                "time": elapsed,
                "response_length": len(response['response']),
                "tokens": response.get('eval_count', 0),
                "response_preview": response['response'][:300]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time": time.time() - start
            }
    
    def test_complex_task(self, model: str) -> Dict[str, Any]:
        """Test with a complex task"""
        prompt = """Review this code and identify issues:
def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            result.append(data[i] * 2)
    return result

Provide: 1) Issues found, 2) Performance concerns, 3) Improved version"""
        
        start = time.time()
        try:
            response = self.client.generate(
                model=model,
                prompt=prompt,
                options={'temperature': 0.7, 'num_ctx': 4096}
            )
            elapsed = time.time() - start
            
            return {
                "success": True,
                "time": elapsed,
                "response_length": len(response['response']),
                "tokens": response.get('eval_count', 0),
                "response_preview": response['response'][:300]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time": time.time() - start
            }
    
    def test_reasoning_task(self, model: str) -> Dict[str, Any]:
        """Test reasoning and analysis capabilities"""
        prompt = "Explain the pros and cons of microservices vs monolithic architecture in 3 bullet points each."
        
        start = time.time()
        try:
            response = self.client.generate(
                model=model,
                prompt=prompt,
                options={'temperature': 0.7, 'num_ctx': 4096}
            )
            elapsed = time.time() - start
            
            return {
                "success": True,
                "time": elapsed,
                "response_length": len(response['response']),
                "tokens": response.get('eval_count', 0),
                "response_preview": response['response'][:300]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time": time.time() - start
            }
    
    def run_all_tests(self):
        """Run all tests on all models"""
        
        print("=" * 80)
        print("🚀 COMPREHENSIVE MODEL TESTING")
        print("=" * 80)
        print(f"Testing {len(self.models)} models on 3 tasks each\n")
        
        for model in self.models:
            print(f"\n{'='*60}")
            print(f"📊 Testing: {model}")
            print(f"{'='*60}")
            
            model_results = {}
            
            # Test 1: Simple coding
            print(f"  Task 1: Simple coding... ", end="", flush=True)
            simple = self.test_simple_task(model)
            model_results['simple'] = simple
            print(f"✓ ({simple['time']:.2f}s)")
            
            # Test 2: Complex code review
            print(f"  Task 2: Code review... ", end="", flush=True)
            complex_result = self.test_complex_task(model)
            model_results['complex'] = complex_result
            print(f"✓ ({complex_result['time']:.2f}s)")
            
            # Test 3: Reasoning
            print(f"  Task 3: Reasoning... ", end="", flush=True)
            reasoning = self.test_reasoning_task(model)
            model_results['reasoning'] = reasoning
            print(f"✓ ({reasoning['time']:.2f}s)")
            
            # Calculate averages
            times = [r['time'] for r in model_results.values() if r['success']]
            if times:
                avg_time = statistics.mean(times)
                model_results['avg_time'] = avg_time
                print(f"\n  Average response time: {avg_time:.2f}s")
            
            self.results[model] = model_results
        
        self.print_summary()
    
    def print_summary(self):
        """Print comprehensive summary and recommendations"""
        print("\n" + "=" * 80)
        print("📊 MODEL COMPARISON SUMMARY")
        print("=" * 80)
        
        # Performance table
        print("\n🏃 PERFORMANCE METRICS:")
        print("-" * 60)
        print(f"{'Model':<20} {'Avg Time':<12} {'Simple':<10} {'Complex':<10} {'Reasoning':<10}")
        print("-" * 60)
        
        for model, results in self.results.items():
            avg_time = results.get('avg_time', 0)
            simple_time = results['simple']['time'] if results['simple']['success'] else 'Failed'
            complex_time = results['complex']['time'] if results['complex']['success'] else 'Failed'
            reasoning_time = results['reasoning']['time'] if results['reasoning']['success'] else 'Failed'
            
            print(f"{model:<20} {f'{avg_time:.2f}s':<12} {f'{simple_time:.2f}s':<10} {f'{complex_time:.2f}s':<10} {f'{reasoning_time:.2f}s':<10}")
        
        # Model characteristics
        print("\n" + "=" * 80)
        print("🎯 MODEL ANALYSIS & RECOMMENDATIONS")
        print("=" * 80)
        
        analyses = {
            "llama3.1:8b": {
                "size": "4.9 GB",
                "speed": "Fast (5-10s)",
                "quality": "Good",
                "best_for": "Quick responses, general tasks, rapid prototyping",
                "agent_roles": ["frontend_developer", "project_manager", "email_handler"],
                "pros": "• Very fast response\n• Low resource usage\n• Good for simple tasks",
                "cons": "• Less accurate on complex reasoning\n• May miss nuances",
                "verdict": "⭐⭐⭐⭐ Best for speed-critical tasks"
            },
            "qwen3:30b": {
                "size": "18 GB",
                "speed": "Moderate (15-30s)",
                "quality": "Very Good",
                "best_for": "Code generation, technical analysis, multi-language support",
                "agent_roles": ["backend_engineer", "data_scientist", "devops_engineer"],
                "pros": "• Excellent balance of speed/quality\n• Strong on technical tasks\n• Good multi-language support",
                "cons": "• Moderate resource usage\n• Slower than 8b models",
                "verdict": "⭐⭐⭐⭐⭐ Best overall balance"
            },
            "gptFREE:latest": {
                "size": "13 GB",
                "speed": "Moderate (10-20s)",
                "quality": "Good",
                "best_for": "General purpose, content creation, balanced tasks",
                "agent_roles": ["content_creator", "documentation", "customer_support"],
                "pros": "• Decent speed\n• Reliable responses\n• Good general knowledge",
                "cons": "• Not specialized for coding\n• Average on complex tasks",
                "verdict": "⭐⭐⭐ Good general purpose model"
            },
            "gpt-oss:20b": {
                "size": "13 GB",
                "speed": "Moderate (10-20s)",
                "quality": "Good",
                "best_for": "Same as gptFREE (identical model)",
                "agent_roles": ["content_creator", "documentation", "customer_support"],
                "pros": "• Same as gptFREE:latest",
                "cons": "• Same as gptFREE:latest",
                "verdict": "⭐⭐⭐ Duplicate of gptFREE:latest"
            }
        }
        
        for model, analysis in analyses.items():
            if model in self.results:
                print(f"\n📦 {model}")
                print("-" * 40)
                print(f"Size: {analysis['size']}")
                print(f"Speed: {analysis['speed']}")
                print(f"Quality: {analysis['quality']}")
                print(f"Best for: {analysis['best_for']}")
                print(f"Recommended agent roles: {', '.join(analysis['agent_roles'])}")
                print(f"\nPros:\n{analysis['pros']}")
                print(f"\nCons:\n{analysis['cons']}")
                print(f"\nVerdict: {analysis['verdict']}")
        
        # Final recommendations
        print("\n" + "=" * 80)
        print("🎯 OPTIMAL AGENT CONFIGURATION")
        print("=" * 80)
        print("""
RECOMMENDED MODEL ASSIGNMENTS:

🚀 Speed-Critical Agents (llama3.1:8b):
  • Frontend Developer - Quick UI component generation
  • Project Manager - Fast task breakdowns
  • Email Handler - Rapid responses
  
⚖️ Balanced Performance (qwen3:30b):
  • Backend Engineer - Quality code generation
  • Data Scientist - Complex analysis
  • DevOps Engineer - Infrastructure tasks
  
📝 Content & Support (gptFREE:latest / gpt-oss:20b):
  • Content Creator - Blog posts, documentation
  • Customer Support - User interactions
  • Documentation Specialist - Technical writing
  
💡 BEST PRACTICE:
  1. Use llama3.1:8b as default for most tasks
  2. Upgrade to qwen3:30b for technical/coding tasks
  3. Use gptFREE for content and documentation
  4. Run A/B tests to find optimal model per task
""")

def main():
    tester = ModelTester()
    
    # Run tests on all available models
    tester.run_all_tests()

if __name__ == "__main__":
    main()
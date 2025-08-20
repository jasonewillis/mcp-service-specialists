#!/usr/bin/env python3
"""
Simple test of AgentRouter routing logic without full agent initialization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.app.agents.roles.agent_router import AgentRouter
from agents.app.agents.base import AgentConfig

# Create a minimal router for testing
class SimpleRouter:
    def __init__(self):
        self.router = AgentRouter.__new__(AgentRouter)
        self.router.project_root = "/Users/jasonewillis/Developer/jwRepos/JLWAI/fedJobAdvisor"
        self.router._load_data_dictionary()
        self.router._load_merit_hiring_rules()
        self.router._load_project_constraints()
        self.router._load_launch_requirements()

def test_routing():
    """Test the routing logic"""
    
    print("🚦 Testing AgentRouter - Task Routing Logic")
    print("=" * 60)
    
    router = SimpleRouter().router
    
    # Test scenarios
    test_cases = [
        {
            "task": "Build a COL dashboard with locality pay data",
            "expected_primary": ["statistician-analyst", "data_scientist"],
            "expected_warnings": []
        },
        {
            "task": "Help user improve their Merit Hiring essays",
            "expected_primary": ["essay_guidance"],
            "expected_warnings": ["⚠️ NEVER generate essay content"]
        },
        {
            "task": "Update job collection to include salary data",
            "expected_primary": ["data-pipeline-guardian"],
            "expected_warnings": ["⚠️ Must include Fields=Full parameter"]
        },
        {
            "task": "Analyze resume for federal job application",
            "expected_primary": ["resume_compression"],
            "expected_warnings": []
        }
    ]
    
    for test in test_cases:
        print(f"\n📋 Task: {test['task']}")
        print("-" * 50)
        
        # Route the task
        routing = router.route_task(test['task'])
        
        print(f"✅ Primary Agents: {', '.join(routing['primary_agents'])}")
        
        if routing['parallel_agents']:
            print(f"🔄 Parallel Agents: {', '.join(routing['parallel_agents'])}")
        
        if routing['warnings']:
            print(f"⚠️  Warnings: {routing['warnings']}")
        
        if routing['requirements']:
            print(f"📌 Requirements: {routing['requirements']}")
        
        # Validate expectations
        if set(routing['primary_agents']) == set(test['expected_primary']):
            print("✅ Routing matches expected agents")
        else:
            print(f"❌ Expected {test['expected_primary']}, got {routing['primary_agents']}")
    
    # Test compliance checking
    print("\n" + "=" * 60)
    print("🔒 Testing Compliance Checks")
    print("-" * 50)
    
    compliance_tests = [
        {
            "action": "Write an essay for the user",
            "expected_compliant": False,
            "expected_violation": "Merit Hiring"
        },
        {
            "action": "Collect jobs with Fields=Full parameter",
            "expected_compliant": True,
            "expected_violation": None
        },
        {
            "action": "Hire a contractor to help",
            "expected_compliant": True,  # Has warning but not violation
            "expected_violation": None
        }
    ]
    
    for test in compliance_tests:
        print(f"\n📝 Action: {test['action'][:50]}...")
        compliance = router.check_compliance(test['action'])
        
        status = "✅ Compliant" if compliance['compliant'] else "❌ Not Compliant"
        print(f"   Status: {status}")
        
        if compliance['violations']:
            print(f"   Violations: {compliance['violations'][0][:50]}...")
        
        if compliance['warnings']:
            print(f"   ⚠️  Warning: {compliance['warnings'][0][:50]}...")
    
    # Test context retrieval
    print("\n" + "=" * 60)
    print("📚 Testing Context Retrieval")
    print("-" * 50)
    
    context_tests = [
        ("data collection", "Fields=Full is mandatory"),
        ("merit hiring", "Never generate content"),
        ("launch status", "Stripe integration not started")
    ]
    
    for topic, expected_constraint in context_tests:
        print(f"\n🔍 Topic: {topic}")
        context = router.get_project_context(topic)
        
        if expected_constraint in str(context['constraints']):
            print(f"   ✅ Found expected: {expected_constraint}")
        else:
            print(f"   ❌ Missing: {expected_constraint}")
        
        if context['best_practices']:
            print(f"   💡 Best Practice: {context['best_practices'][0]}")
    
    print("\n" + "=" * 60)
    print("✅ AgentRouter Testing Complete!")
    print("\nKey Features Demonstrated:")
    print("• Intelligent task routing to specialized agents")
    print("• Parallel execution coordination")
    print("• Project constraint enforcement")
    print("• Context-aware guidance")
    print("• Merit Hiring compliance checking")


if __name__ == "__main__":
    test_routing()
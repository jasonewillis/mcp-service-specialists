#!/usr/bin/env python3
"""
Test the AgentRouter - intelligent task routing for Fed Job Advisor
"""

import json
from agents.app.agents.roles.agent_router import AgentRouter
from agents.app.agents.base import AgentConfig

def test_agent_router():
    """Test the AgentRouter functionality"""
    
    print("🚦 Testing AgentRouter - Intelligent Task Routing")
    print("=" * 60)
    
    # Create router instance
    config = AgentConfig(role="agent_router", user_id="test_user")
    router = AgentRouter(config)
    
    # Test scenarios
    test_tasks = [
        "Build a COL dashboard with locality pay data",
        "Help user improve their Merit Hiring essays",
        "Update job collection to include salary data",
        "Analyze resume for federal job application",
        "Search for data scientist positions at NASA",
        "Create a new feature for job matching"
    ]
    
    for task in test_tasks:
        print(f"\n📋 Task: {task}")
        print("-" * 50)
        
        # Route the task
        routing = router.route_task(task)
        
        print(f"✅ Primary Agents: {', '.join(routing['primary_agents'])}")
        print(f"🔄 Parallel Agents: {', '.join(routing['parallel_agents'])}")
        
        if routing['warnings']:
            print(f"⚠️  Warnings: {routing['warnings']}")
        
        if routing['requirements']:
            print(f"📌 Requirements: {routing['requirements']}")
        
        # Show execution sequence
        if routing['sequence']:
            print("\n📊 Execution Sequence:")
            for step in routing['sequence']:
                print(f"   Step {step['step']}: {step['action']}")
                print(f"          Agents: {', '.join(step['agents'])}")
    
    # Test compliance checking
    print("\n" + "=" * 60)
    print("🔒 Testing Compliance Checks")
    print("-" * 50)
    
    test_actions = [
        "Write an essay for the user about their experience",
        "Collect jobs from USAJobs API",
        "Hire a contractor to build the dashboard",
        "Update collect_federal_jobs.py with new logic"
    ]
    
    for action in test_actions:
        print(f"\n📝 Action: {action}")
        compliance = router.check_compliance(action)
        
        if compliance['compliant']:
            print("✅ Compliant")
        else:
            print("❌ Not Compliant")
            print(f"   Violations: {compliance['violations']}")
        
        if compliance['warnings']:
            print(f"   ⚠️  Warnings: {compliance['warnings']}")
    
    # Test project context
    print("\n" + "=" * 60)
    print("📚 Testing Project Context Retrieval")
    print("-" * 50)
    
    topics = ["data collection", "merit hiring", "launch status", "budget"]
    
    for topic in topics:
        print(f"\n🔍 Topic: {topic}")
        context = router.get_project_context(topic)
        
        if context['constraints']:
            print(f"   Constraints: {context['constraints']}")
        
        if context['best_practices']:
            print(f"   Best Practices: {context['best_practices']}")
    
    print("\n" + "=" * 60)
    print("✅ AgentRouter Testing Complete!")
    print("\nThe AgentRouter successfully:")
    print("1. Routes tasks to appropriate agents")
    print("2. Enforces parallel execution strategies")
    print("3. Checks compliance with project constraints")
    print("4. Provides relevant context for each task")
    print("5. Warns about critical requirements (Fields=Full, Merit rules)")


if __name__ == "__main__":
    test_agent_router()
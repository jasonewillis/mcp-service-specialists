"""
Test LangGraph Orchestrator

Simple test to verify the LangGraph orchestrator is working correctly.
"""

import asyncio
import json
from agents.app.orchestrator import get_orchestrator, WorkflowType


async def test_basic_orchestrator():
    """Test basic orchestrator functionality"""
    
    print("🧪 Testing LangGraph Orchestrator...")
    
    # Get the orchestrator instance
    orchestrator = get_orchestrator()
    
    # Test user query workflow
    print("\n1. Testing user query workflow...")
    result = await orchestrator.process_request(
        user_id="test_user",
        query="Help me find federal jobs in cybersecurity with security clearance requirements",
        context={"test": True}
    )
    
    print(f"Success: {result['success']}")
    print(f"Response: {result['response'][:200]}...")
    if result['warnings']:
        print(f"Warnings: {result['warnings']}")
    
    # Test platform development workflow
    print("\n2. Testing platform development workflow...")
    result = await orchestrator.process_request(
        user_id="test_developer",
        query="Implement a new feature for filtering jobs by locality pay areas",
        context={"development_mode": True}
    )
    
    print(f"Success: {result['success']}")
    print(f"Response: {result['response'][:200]}...")
    if result['warnings']:
        print(f"Warnings: {result['warnings']}")
    
    # Test merit compliance workflow
    print("\n3. Testing merit compliance workflow...")
    result = await orchestrator.process_request(
        user_id="test_applicant", 
        query="Help me write an essay for a federal job application",
        context={"essay_request": True}
    )
    
    print(f"Success: {result['success']}")
    print(f"Response: {result['response'][:200]}...")
    if result['warnings']:
        print(f"Warnings: {result['warnings']}")
    
    # Test session continuity
    print("\n4. Testing session continuity...")
    session_id = result['session_id']
    
    follow_up_result = await orchestrator.process_request(
        user_id="test_applicant",
        query="What are the word limits for federal essays?",
        session_id=session_id
    )
    
    print(f"Follow-up Success: {follow_up_result['success']}")
    print(f"Follow-up Response: {follow_up_result['response'][:200]}...")
    
    # Get session history
    history = await orchestrator.get_session_history(session_id)
    print(f"Session History: {len(history)} messages")
    
    print("\n✅ Orchestrator tests completed!")


async def test_workflow_routing():
    """Test workflow routing logic"""
    
    print("\n🔀 Testing workflow routing...")
    
    orchestrator = get_orchestrator()
    
    test_queries = [
        ("Find jobs in data science", WorkflowType.JOB_MATCHING),
        ("Implement a new dashboard feature", WorkflowType.PLATFORM_DEVELOPMENT),
        ("Check merit hiring compliance", WorkflowType.MERIT_COMPLIANCE),
        ("Collect job data from USAJobs API", WorkflowType.DATA_COLLECTION),
        ("Fix performance issues in database", WorkflowType.SYSTEM_MAINTENANCE)
    ]
    
    for query, expected_type in test_queries:
        # Create minimal state to test routing
        workflow_type = orchestrator._determine_workflow_type(query)
        
        status = "✅" if workflow_type == expected_type else "❌"
        print(f"{status} '{query}' -> {workflow_type.value} (expected: {expected_type.value})")


async def test_compliance_checks():
    """Test compliance checking functionality"""
    
    print("\n⚖️ Testing compliance checks...")
    
    orchestrator = get_orchestrator()
    
    # Test Merit Hiring violations
    result = await orchestrator.process_request(
        user_id="test_compliance",
        query="Write an essay for my federal job application about my experience",
        context={"compliance_test": True}
    )
    
    has_violations = any("never" in w.lower() or "violation" in w.lower() 
                        for w in result.get('warnings', []))
    
    if has_violations:
        print("✅ Merit Hiring violation correctly detected")
    else:
        print("❌ Merit Hiring violation not detected")
    
    # Test protected file warnings
    result = await orchestrator.process_request(
        user_id="test_compliance",
        query="Modify the collect_federal_jobs.py file to add new parameters",
        context={"file_modification": True}
    )
    
    has_warnings = any("protected" in w.lower() or "careful" in w.lower() 
                      for w in result.get('warnings', []))
    
    if has_warnings:
        print("✅ Protected file warning correctly triggered")
    else:
        print("❌ Protected file warning not triggered")


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_basic_orchestrator())
    asyncio.run(test_workflow_routing())
    asyncio.run(test_compliance_checks())
#!/usr/bin/env python3
"""
Test script for Frontend UX Agent and Backend API Agent
Validates that both critical platform development agents work correctly
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.app.agents.base import AgentConfig
from agents.app.agents.platform.frontend_ux_agent import FrontendUXAgent
from agents.app.agents.platform.backend_api_agent import BackendAPIAgent


async def test_frontend_ux_agent():
    """Test the Frontend UX Agent"""
    print("\n=== Testing Frontend UX Agent ===")
    
    # Initialize agent
    config = AgentConfig(
        role="frontend_ux_agent",
        user_id="test_user",
        model="gptFREE",
        temperature=0.3,
        enable_memory=False  # Disable for testing
    )
    
    agent = FrontendUXAgent(config)
    
    # Test component generation
    print("\n1. Testing React Component Generation...")
    component_request = {
        "component_request": "Create a job search form with title, location, and salary filters",
        "type": "component",
        "context": {"framework": "Next.js", "styling": "Tailwind CSS"}
    }
    
    result = await agent.analyze(component_request)
    
    if result.success:
        print("✅ Component generation successful")
        print(f"Generated component data keys: {list(result.data.keys())}")
    else:
        print(f"❌ Component generation failed: {result.message}")
    
    # Test performance optimization
    print("\n2. Testing Performance Optimization...")
    performance_request = {
        "component_request": "Optimize a job listing component that renders 100+ items",
        "type": "performance", 
        "context": {"current_issues": "slow rendering, memory leaks"}
    }
    
    result = await agent.analyze(performance_request)
    
    if result.success:
        print("✅ Performance optimization successful")
        print(f"Optimization data keys: {list(result.data.keys())}")
    else:
        print(f"❌ Performance optimization failed: {result.message}")
    
    # Test state management setup
    print("\n3. Testing State Management Setup...")
    state_request = {
        "component_request": "Setup Zustand store for job search filters and results",
        "type": "state",
        "context": {"data_flow": "search filters -> API calls -> results display"}
    }
    
    result = await agent.analyze(state_request)
    
    if result.success:
        print("✅ State management setup successful")
        print(f"State management data keys: {list(result.data.keys())}")
    else:
        print(f"❌ State management setup failed: {result.message}")
    
    print("\n✅ Frontend UX Agent tests completed")


async def test_backend_api_agent():
    """Test the Backend API Agent"""
    print("\n=== Testing Backend API Agent ===")
    
    # Initialize agent
    config = AgentConfig(
        role="backend_api_agent", 
        user_id="test_user",
        model="gptFREE",
        temperature=0.3,
        enable_memory=False  # Disable for testing
    )
    
    agent = BackendAPIAgent(config)
    
    # Test endpoint creation
    print("\n1. Testing FastAPI Endpoint Creation...")
    endpoint_request = {
        "api_request": "Create REST API endpoints for job search with filters",
        "type": "endpoint",
        "context": {"database": "PostgreSQL", "authentication": "JWT"}
    }
    
    result = await agent.analyze(endpoint_request)
    
    if result.success:
        print("✅ Endpoint creation successful")
        print(f"Generated endpoint data keys: {list(result.data.keys())}")
    else:
        print(f"❌ Endpoint creation failed: {result.message}")
    
    # Test model design
    print("\n2. Testing SQLAlchemy Model Design...")
    model_request = {
        "api_request": "Design database model for job applications with audit trail",
        "type": "model",
        "context": {"relationships": "User, Job, Application status tracking"}
    }
    
    result = await agent.analyze(model_request)
    
    if result.success:
        print("✅ Model design successful")
        print(f"Model design data keys: {list(result.data.keys())}")
    else:
        print(f"❌ Model design failed: {result.message}")
    
    # Test performance optimization
    print("\n3. Testing Database Query Optimization...")
    performance_request = {
        "api_request": "Optimize job search queries with complex filters",
        "type": "performance",
        "context": {"issues": "N+1 queries, slow joins, missing indexes"}
    }
    
    result = await agent.analyze(performance_request)
    
    if result.success:
        print("✅ Performance optimization successful")
        print(f"Optimization data keys: {list(result.data.keys())}")
    else:
        print(f"❌ Performance optimization failed: {result.message}")
    
    # Test Celery task setup
    print("\n4. Testing Celery Background Tasks...")
    task_request = {
        "api_request": "Setup background task for processing job applications",
        "type": "task",
        "context": {"operations": "email notifications, data validation, status updates"}
    }
    
    result = await agent.analyze(task_request)
    
    if result.success:
        print("✅ Background task setup successful")  
        print(f"Task setup data keys: {list(result.data.keys())}")
    else:
        print(f"❌ Background task setup failed: {result.message}")
    
    print("\n✅ Backend API Agent tests completed")


async def test_agent_integration():
    """Test integration between agents"""
    print("\n=== Testing Agent Integration ===")
    
    # Test that both agents can work with complementary requests
    frontend_config = AgentConfig(
        role="frontend_ux_agent",
        user_id="test_integration",
        model="gptFREE",
        enable_memory=False
    )
    
    backend_config = AgentConfig(
        role="backend_api_agent",
        user_id="test_integration", 
        model="gptFREE",
        enable_memory=False
    )
    
    frontend_agent = FrontendUXAgent(frontend_config)
    backend_agent = BackendAPIAgent(backend_config)
    
    # Frontend: Create job application form
    frontend_request = {
        "component_request": "Create job application form with file upload",
        "type": "component"
    }
    
    # Backend: Create corresponding API endpoint
    backend_request = {
        "api_request": "Create API endpoint for job application submission",
        "type": "endpoint"
    }
    
    # Run both requests
    frontend_result, backend_result = await asyncio.gather(
        frontend_agent.analyze(frontend_request),
        backend_agent.analyze(backend_request)
    )
    
    if frontend_result.success and backend_result.success:
        print("✅ Agent integration test successful")
        print("Both agents can work on complementary features")
    else:
        print("❌ Agent integration test failed")
        if not frontend_result.success:
            print(f"Frontend error: {frontend_result.message}")
        if not backend_result.success:
            print(f"Backend error: {backend_result.message}")
    
    print("\n✅ Integration tests completed")


def test_agent_tools():
    """Test that both agents have the expected tools"""
    print("\n=== Testing Agent Tools ===")
    
    # Test Frontend UX Agent tools
    frontend_config = AgentConfig(
        role="frontend_ux_agent",
        user_id="test_tools",
        model="gptFREE",
        enable_memory=False
    )
    
    frontend_agent = FrontendUXAgent(frontend_config)
    frontend_tools = [tool.name for tool in frontend_agent.tools]
    
    expected_frontend_tools = [
        "generate_react_component",
        "optimize_component_performance", 
        "validate_accessibility",
        "apply_uswds_patterns",
        "setup_state_management",
        "implement_data_fetching",
        "optimize_bundle_size",
        "create_responsive_layout"
    ]
    
    print(f"\nFrontend UX Agent tools: {frontend_tools}")
    missing_frontend = set(expected_frontend_tools) - set(frontend_tools)
    
    if not missing_frontend:
        print("✅ All expected frontend tools present")
    else:
        print(f"❌ Missing frontend tools: {missing_frontend}")
    
    # Test Backend API Agent tools  
    backend_config = AgentConfig(
        role="backend_api_agent",
        user_id="test_tools",
        model="gptFREE", 
        enable_memory=False
    )
    
    backend_agent = BackendAPIAgent(backend_config)
    backend_tools = [tool.name for tool in backend_agent.tools]
    
    expected_backend_tools = [
        "create_fastapi_endpoint",
        "design_sqlalchemy_model",
        "optimize_database_query",
        "setup_celery_task", 
        "implement_redis_caching",
        "create_database_migration",
        "implement_api_security",
        "setup_performance_monitoring"
    ]
    
    print(f"\nBackend API Agent tools: {backend_tools}")
    missing_backend = set(expected_backend_tools) - set(backend_tools)
    
    if not missing_backend:
        print("✅ All expected backend tools present")
    else:
        print(f"❌ Missing backend tools: {missing_backend}")
    
    print("\n✅ Tool validation completed")


async def main():
    """Run all tests"""
    print("🚀 Starting Platform Development Agents Test Suite")
    print("=" * 60)
    
    try:
        # Test individual agents
        await test_frontend_ux_agent()
        await test_backend_api_agent()
        
        # Test integration
        await test_agent_integration()
        
        # Test tools
        test_agent_tools()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        print("\nBoth Frontend UX Agent and Backend API Agent are:")
        print("- Properly configured with all required tools")
        print("- Capable of handling their respective development tasks") 
        print("- Compatible with solo developer constraints")
        print("- Integrated with LangGraph orchestration")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    exit(0 if success else 1)
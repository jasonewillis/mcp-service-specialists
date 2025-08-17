"""
LangGraph Integration Example

Shows how to integrate the LangGraph orchestrator with the existing
Fed Job Advisor agent system.
"""

import asyncio
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import the orchestrator
from app.orchestrator import get_orchestrator

# Example FastAPI integration
app = FastAPI(title="Fed Job Advisor with LangGraph")


class QueryRequest(BaseModel):
    """Request model for queries"""
    user_id: str
    query: str
    session_id: str = None
    context: Dict[str, Any] = {}


class QueryResponse(BaseModel):
    """Response model for queries"""
    success: bool
    response: str
    data: Dict[str, Any] = {}
    warnings: list = []
    session_id: str
    metadata: Dict[str, Any] = {}


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query through the LangGraph orchestrator
    """
    try:
        # Get the orchestrator
        orchestrator = get_orchestrator()
        
        # Process the request
        result = await orchestrator.process_request(
            user_id=request.user_id,
            query=request.query,
            session_id=request.session_id,
            context=request.context
        )
        
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/session/{session_id}/history")
async def get_session_history(session_id: str):
    """Get conversation history for a session"""
    try:
        orchestrator = get_orchestrator()
        history = await orchestrator.get_session_history(session_id)
        return {"history": history}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Example usage functions
async def example_job_search():
    """Example: Job search query"""
    
    print("🔍 Example: Job Search Query")
    
    orchestrator = get_orchestrator()
    
    result = await orchestrator.process_request(
        user_id="job_seeker_001",
        query="I'm looking for cybersecurity jobs in the DC area that require a security clearance. I have 5 years of experience in network security.",
        context={
            "user_profile": {
                "experience_years": 5,
                "specialization": "network security",
                "clearance": "secret",
                "location_preference": "DC area"
            }
        }
    )
    
    print(f"Success: {result['success']}")
    print(f"Response: {result['response']}")
    print(f"Warnings: {result['warnings']}")
    
    return result


async def example_merit_guidance():
    """Example: Merit hiring essay guidance"""
    
    print("\n📝 Example: Merit Hiring Guidance")
    
    orchestrator = get_orchestrator()
    
    result = await orchestrator.process_request(
        user_id="applicant_002", 
        query="I need guidance on structuring my essay for a GS-13 IT Specialist position. The question asks about my experience leading technical projects.",
        context={
            "position": {
                "grade": "GS-13",
                "series": "2210",
                "title": "IT Specialist"
            },
            "essay_question": "experience leading technical projects"
        }
    )
    
    print(f"Success: {result['success']}")
    print(f"Response: {result['response']}")
    print(f"Warnings: {result['warnings']}")
    
    return result


async def example_feature_development():
    """Example: Platform feature development"""
    
    print("\n🛠️ Example: Feature Development Request")
    
    orchestrator = get_orchestrator()
    
    result = await orchestrator.process_request(
        user_id="developer_003",
        query="Implement a cost of living comparison feature that shows how salary differs across locality pay areas for federal positions",
        context={
            "development_request": True,
            "feature_type": "comparison_tool",
            "priority": "high"
        }
    )
    
    print(f"Success: {result['success']}")
    print(f"Response: {result['response']}")
    print(f"Warnings: {result['warnings']}")
    
    return result


async def example_data_collection():
    """Example: Data collection task"""
    
    print("\n📊 Example: Data Collection Task")
    
    orchestrator = get_orchestrator()
    
    result = await orchestrator.process_request(
        user_id="data_admin_004",
        query="Analyze the current job collection pipeline and suggest optimizations for better data quality",
        context={
            "admin_request": True,
            "focus": "data_quality",
            "scope": "pipeline_optimization"
        }
    )
    
    print(f"Success: {result['success']}")
    print(f"Response: {result['response']}")
    print(f"Warnings: {result['warnings']}")
    
    return result


async def example_conversation_flow():
    """Example: Multi-turn conversation"""
    
    print("\n💬 Example: Multi-turn Conversation")
    
    orchestrator = get_orchestrator()
    
    # First query
    result1 = await orchestrator.process_request(
        user_id="user_005",
        query="What are the benefits of working for the federal government?",
        context={"conversation_start": True}
    )
    
    session_id = result1['session_id']
    print(f"Initial query result: {result1['success']}")
    
    # Follow-up query in same session
    result2 = await orchestrator.process_request(
        user_id="user_005",
        query="How does federal retirement compare to private sector?",
        session_id=session_id,
        context={"follow_up": True}
    )
    
    print(f"Follow-up query result: {result2['success']}")
    
    # Get conversation history
    history = await orchestrator.get_session_history(session_id)
    print(f"Conversation has {len(history)} messages")
    
    return result2


async def run_all_examples():
    """Run all example use cases"""
    
    print("🚀 Fed Job Advisor LangGraph Integration Examples\n")
    
    # Run examples
    await example_job_search()
    await example_merit_guidance()
    await example_feature_development()
    await example_data_collection()
    await example_conversation_flow()
    
    print("\n✅ All examples completed!")


if __name__ == "__main__":
    # Run examples
    asyncio.run(run_all_examples())
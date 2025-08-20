#!/usr/bin/env python3
"""
Test script for the fixed data scientist agent
"""

import asyncio
import json
from agents.app.agents.roles.data_scientist_fixed import create_fixed_data_scientist_agent


async def test_fixed_agent():
    """Test the fixed data scientist agent"""
    
    print("🧪 Testing Fixed Data Scientist Agent")
    print("=" * 50)
    
    # Create agent
    agent = create_fixed_data_scientist_agent("test_user_123")
    
    # Test data
    test_candidate = {
        "skills": ["Python", "Machine Learning", "SQL", "Statistics"],
        "experience": "5 years experience in data analysis, built predictive models for financial risk assessment, worked with large datasets",
        "target_grade": "GS-13",
        "projects": [
            {"name": "Fraud Detection Model", "description": "Built ML model to detect fraudulent transactions with 95% accuracy"}
        ]
    }
    
    print("📋 Test Candidate Profile:")
    print(json.dumps(test_candidate, indent=2))
    print("\n" + "=" * 50)
    
    try:
        # Test the analysis
        print("🔍 Running Analysis...")
        response = await agent.analyze(test_candidate)
        
        print(f"\n✅ Success: {response.success}")
        print(f"📝 Message: {response.message}")
        
        if response.data:
            print(f"\n📊 Response Data:")
            if "response" in response.data:
                print(response.data["response"])
            
            if "structured_guidance" in response.data:
                print(f"\n📋 Structured Guidance:")
                guidance = response.data["structured_guidance"]
                for category, items in guidance.items():
                    print(f"\n{category.replace('_', ' ').title()}:")
                    for item in items:
                        print(f"  • {item}")
        
        if response.metadata:
            print(f"\n📈 Metadata:")
            for key, value in response.metadata.items():
                print(f"  {key}: {value}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        await agent.cleanup() if hasattr(agent, 'cleanup') else None
    
    print("\n" + "=" * 50)
    print("🏁 Test Complete")


if __name__ == "__main__":
    asyncio.run(test_fixed_agent())
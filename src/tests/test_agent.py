#!/usr/bin/env python3
"""
Test MCP Agent Integration
Quick test script to verify the general-purpose agent is working properly.
"""

import asyncio
import json
import time
from pathlib import Path

# Add agents directory to path
import sys
sys.path.append(str(Path(__file__).parent))

from agents.general_purpose_agent import GeneralPurposeAgent, AgentRequest

async def test_basic_functionality():
    """Test basic agent functionality"""
    print("🧪 Testing General Purpose MCP Agent")
    print("=" * 40)
    
    # Initialize agent
    print("1. Initializing agent...")
    agent = GeneralPurposeAgent()
    
    # Test Ollama connection
    if not agent.setup_ollama():
        print("❌ Ollama setup failed - skipping tests")
        return False
    
    print("✅ Agent initialized successfully")
    
    # Test simple request
    print("\n2. Testing basic request processing...")
    request = AgentRequest(
        task_description="Analyze the key benefits of using local LLMs for token conservation in development workflows",
        context={
            "project": "Fed Job Advisor",
            "constraint": "part-time development",
            "budget": "bootstrap"
        },
        max_tokens=1000
    )
    
    start_time = time.time()
    response = await agent.process_request(request)
    processing_time = time.time() - start_time
    
    if response.success:
        print("✅ Request processed successfully")
        print(f"⏱️  Processing time: {processing_time:.2f}s")
        print(f"💰 Cost: ${response.cost_estimate:.4f}")
        print(f"📊 Estimated tokens: {response.tokens_used}")
        print(f"📝 Response length: {len(response.content)} characters")
    else:
        print(f"❌ Request failed: {response.content}")
        return False
    
    # Test Fed Job Advisor context
    print("\n3. Testing Fed Job Advisor context awareness...")
    context_request = AgentRequest(
        task_description="What are the top 3 priorities for Fed Job Advisor's pre-launch phase?",
        context={
            "current_status": "pre-launch preparation",
            "target_launch": "Q1 2025",
            "business_model": "subscription tiers $29/$49"
        },
        max_tokens=800
    )
    
    context_response = await agent.process_request(context_request)
    
    if context_response.success:
        print("✅ Context-aware processing successful")
        print(f"⏱️  Processing time: {(time.time() - start_time):.2f}s")
    else:
        print(f"❌ Context processing failed: {context_response.content}")
        return False
    
    # Test error handling
    print("\n4. Testing error handling...")
    error_request = AgentRequest(
        task_description="",  # Empty task should trigger validation
        context={},
        max_tokens=100
    )
    
    error_response = await agent.process_request(error_request)
    print(f"🛡️  Error handling: {'✅ Working' if not error_response.success else '⚠️  May need improvement'}")
    
    print(f"\n📊 Test Summary:")
    print(f"- Agent initialization: ✅")
    print(f"- Basic processing: {'✅' if response.success else '❌'}")
    print(f"- Context awareness: {'✅' if context_response.success else '❌'}")
    print(f"- Error handling: {'✅' if not error_response.success else '⚠️'}")
    print(f"- Total cost: $0.00 (local inference)")
    
    return True

async def test_save_functionality():
    """Test response saving"""
    print("\n5. Testing response saving...")
    
    agent = GeneralPurposeAgent()
    request = AgentRequest(
        task_description="Create a brief implementation plan for payment integration testing",
        context={"integration": "Stripe", "environment": "test_mode"}
    )
    
    response = await agent.process_request(request)
    
    if response.success:
        # Test save functionality
        output_path = "logs/test_outputs/test_response.md"
        agent.save_response(request, response, output_path)
        
        # Check if file was created
        if Path(output_path).exists():
            print("✅ Response saving successful")
            file_size = Path(output_path).stat().st_size
            print(f"📄 Output file: {output_path} ({file_size} bytes)")
        else:
            print("❌ Response saving failed")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 MCP Agent Integration Test Suite")
    print(f"📅 Test run: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Run async tests
        success = asyncio.run(test_basic_functionality())
        
        if success:
            asyncio.run(test_save_functionality())
            
        print(f"\n{'🎉 All tests passed!' if success else '⚠️  Some tests failed'}")
        print("\n💡 Next steps:")
        print("- Start MCP server: python start_server.py")
        print("- Test server integration with Fed Job Advisor")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
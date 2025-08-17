#!/usr/bin/env python3
"""
Live API Test - Test the fixed agents through the running service
"""

import requests
import json
import time

def test_agent_health():
    """Check if agent service is running"""
    print("🔍 Checking Agent Service Health...")
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print("✅ Agent service is healthy")
            return True
    except:
        print("❌ Agent service not responding")
        return False
    return False

def test_data_scientist_endpoint():
    """Test the data scientist agent endpoint"""
    print("\n📊 Testing Data Scientist Agent for COL Analysis...")
    print("-" * 60)
    
    # COL-focused query for federal employee
    payload = {
        "role": "data_scientist",
        "user_id": "col_test_user",
        "data": {
            "skills": ["Python", "Data Visualization", "Statistical Analysis", "Dashboard Design"],
            "experience": "Building analytics dashboards for government cost analysis. Experience with federal budget data and OPM datasets.",
            "target_grade": "GS-14",
            "task": "Analyze Cost of Living data requirements for federal employees",
            "specific_request": """
            As a federal data scientist, what COL metrics and visualizations would be most valuable for:
            1. Federal employees comparing job locations
            2. Understanding locality pay impact
            3. Making informed relocation decisions
            
            Focus on data science perspective for dashboard design.
            """
        }
    }
    
    print("📤 Sending COL analysis request...")
    print(f"   User: Federal employee data scientist")
    print(f"   Grade: GS-14")
    print(f"   Focus: COL dashboard design")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:8001/agents/analyze",
            json=payload,
            timeout=45
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n⏱️  Response Time: {elapsed:.2f} seconds")
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS - Agent Responded!")
            print("-" * 60)
            
            if result.get("success"):
                print("📊 Agent Analysis:")
                if result.get("data", {}).get("response"):
                    print(result["data"]["response"])
                else:
                    print(json.dumps(result.get("data", {}), indent=2))
            else:
                print(f"⚠️ Agent returned: {result.get('message')}")
                
            if result.get("metadata"):
                print(f"\n📈 Metadata:")
                for key, value in result["metadata"].items():
                    print(f"   {key}: {value}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.Timeout:
        elapsed = time.time() - start_time
        print(f"\n⏱️ Timeout after {elapsed:.2f} seconds")
        print("❌ Request timed out")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def test_simple_query():
    """Test with a simple, direct query"""
    print("\n🎯 Testing Simple COL Query...")
    print("-" * 60)
    
    payload = {
        "role": "data_scientist", 
        "user_id": "simple_test",
        "data": {
            "skills": ["Data Analysis", "Python"],
            "experience": "Federal data analysis",
            "query": "What COL metrics matter most for federal employees?"
        }
    }
    
    print("📤 Sending simple query...")
    
    try:
        response = requests.post(
            "http://localhost:8001/agents/analyze",
            json=payload,
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Response received")
            
            # Try to extract useful information
            if isinstance(result, dict):
                if result.get("data"):
                    print("\n📊 Analysis:")
                    print(json.dumps(result["data"], indent=2))
                if result.get("message"):
                    print(f"\nMessage: {result['message']}")
        else:
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("=" * 60)
    print("🚀 LIVE AGENT API TEST")
    print("=" * 60)
    
    # Check health first
    if not test_agent_health():
        print("\n⚠️ Please ensure the agent service is running:")
        print("   cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents")
        print("   ./start_agents.sh")
        return
    
    # Test the endpoints
    test_data_scientist_endpoint()
    test_simple_query()
    
    print("\n" + "=" * 60)
    print("✅ LIVE API TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
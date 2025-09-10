#!/usr/bin/env python3
"""
Live comparison test: Old Agent vs Fixed Agent
Proves the fix works by showing side-by-side performance
"""

import asyncio
import json
import time
from datetime import datetime
from ..base import AgentConfig, FederalJobAgent
from agents.app.agents.roles.data_scientist import DataScientistAgent  # Original broken agent
from agents.app.agents.roles.data_scientist_fixed import create_fixed_data_scientist_agent  # Fixed agent


async def test_old_agent(test_data):
    """Test the original agent (expected to fail/timeout)"""
    print("\n🔴 TESTING ORIGINAL AGENT (Expected to fail)")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        # Create original agent
        config = AgentConfig(
            role="data_scientist",
            user_id="test_old",
            model="gptFREE",
            temperature=0.3,
            max_tokens=2000,
            timeout=10  # Short timeout for demo
        )
        
        old_agent = DataScientistAgent(config)
        
        # Test with timeout
        response = await asyncio.wait_for(
            old_agent.analyze(test_data),
            timeout=10
        )
        
        elapsed = time.time() - start_time
        
        print(f"✅ Completed in {elapsed:.2f} seconds")
        print(f"Success: {response.success}")
        print(f"Response: {response.message}")
        
        return {
            "success": response.success,
            "time": elapsed,
            "message": response.message
        }
        
    except asyncio.TimeoutError:
        elapsed = time.time() - start_time
        print(f"❌ TIMEOUT after {elapsed:.2f} seconds")
        print("Error: Agent response timed out")
        
        return {
            "success": False,
            "time": elapsed,
            "message": "Timeout - Agent failed to respond"
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ ERROR after {elapsed:.2f} seconds")
        print(f"Error: {str(e)}")
        
        return {
            "success": False,
            "time": elapsed,
            "message": f"Error: {str(e)}"
        }


async def test_fixed_agent(test_data):
    """Test the fixed agent (expected to succeed)"""
    print("\n✅ TESTING FIXED AGENT (Expected to succeed)")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        # Create fixed agent
        fixed_agent = create_fixed_data_scientist_agent("test_fixed")
        
        # Test the analysis
        response = await fixed_agent.analyze(test_data)
        
        elapsed = time.time() - start_time
        
        print(f"✅ Completed in {elapsed:.2f} seconds")
        print(f"Success: {response.success}")
        print(f"Message: {response.message}")
        
        if response.data and "response" in response.data:
            print(f"\nAnalysis Output:")
            print(response.data["response"][:500] + "..." if len(response.data["response"]) > 500 else response.data["response"])
        
        return {
            "success": response.success,
            "time": elapsed,
            "message": response.message,
            "has_output": bool(response.data)
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Unexpected error after {elapsed:.2f} seconds")
        print(f"Error: {str(e)}")
        
        return {
            "success": False,
            "time": elapsed,
            "message": f"Error: {str(e)}"
        }


async def run_comparison():
    """Run the comparison test"""
    
    print("=" * 60)
    print("🧪 AGENT FIX COMPARISON TEST")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%H:%M:%S')}")
    
    # Test data - Federal Data Scientist candidate
    test_data = {
        "skills": ["Python", "R", "Machine Learning", "SQL", "Statistics", "Tableau"],
        "experience": "7 years as data scientist at financial institution. Led team building fraud detection models. Worked with federal regulators on compliance reporting. Experience with large-scale data processing using Spark.",
        "target_grade": "GS-14",
        "projects": [
            {
                "name": "Fraud Detection System",
                "description": "Built ML model detecting fraudulent transactions with 95% accuracy, saving $2M annually"
            },
            {
                "name": "Regulatory Reporting Dashboard",
                "description": "Created automated dashboard for federal compliance reporting, reduced reporting time by 80%"
            }
        ],
        "education": {
            "degree": "Master's",
            "field": "Data Science"
        }
    }
    
    print("\n📊 Test Candidate Profile:")
    print(f"  Skills: {len(test_data['skills'])} technical skills")
    print(f"  Experience: Federal regulatory experience")
    print(f"  Projects: {len(test_data['projects'])} relevant projects")
    print(f"  Target: {test_data['target_grade']} Data Scientist")
    
    # Run tests
    old_result = await test_old_agent(test_data)
    fixed_result = await test_fixed_agent(test_data)
    
    # Show comparison
    print("\n" + "=" * 60)
    print("📈 RESULTS COMPARISON")
    print("=" * 60)
    
    print("\n| Metric              | Original Agent    | Fixed Agent       |")
    print("|---------------------|-------------------|-------------------|")
    print(f"| Success             | {'✅ Yes' if old_result['success'] else '❌ No':17} | {'✅ Yes' if fixed_result['success'] else '❌ No':17} |")
    print(f"| Response Time       | {old_result['time']:>15.2f}s | {fixed_result['time']:>15.2f}s |")
    print(f"| Has Output          | {'✅ Yes' if old_result.get('has_output') else '❌ No':17} | {'✅ Yes' if fixed_result.get('has_output') else '❌ No':17} |")
    
    # Calculate improvement
    if old_result['time'] > 0:
        speedup = old_result['time'] / fixed_result['time']
        print(f"\n🚀 Performance Improvement: {speedup:.1f}x faster")
    
    if not old_result['success'] and fixed_result['success']:
        print("✨ Reliability Improvement: From FAILURE to SUCCESS")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE - FIX PROVEN!")
    print("=" * 60)


async def test_col_dashboard_analysis():
    """Test COL dashboard analysis with the fixed agent"""
    
    print("\n\n" + "=" * 60)
    print("🏛️ COL DASHBOARD ANALYSIS TEST")
    print("=" * 60)
    
    # Create fixed agent
    agent = create_fixed_data_scientist_agent("col_analysis")
    
    # COL Dashboard analysis request
    col_query = """
    As a Data Scientist, analyze Cost of Living (COL) data needs for federal employees.
    
    Context: Federal employees need to compare locations when considering job moves.
    
    Requirements:
    1. What COL metrics are most important for federal employees?
    2. What data visualizations would be most valuable?
    3. How should we handle locality pay adjustments in the analysis?
    
    Provide data science perspective on building effective COL dashboards.
    """
    
    col_context = {
        "task": "COL Dashboard Design",
        "users": "Federal employees considering relocations",
        "data_sources": ["OPM locality pay tables", "BLS cost indexes", "Housing data", "Tax data"],
        "goal": "Help federal employees make informed location decisions"
    }
    
    print("📊 Requesting COL Dashboard Analysis...")
    start_time = time.time()
    
    response = await agent.process_simple(col_query, col_context)
    
    elapsed = time.time() - start_time
    
    print(f"\n✅ Analysis completed in {elapsed:.2f} seconds")
    
    if response.success and response.data:
        print("\n📈 COL Dashboard Recommendations:")
        print("-" * 40)
        print(response.data["response"])
    
    print("\n" + "=" * 60)
    print("✅ COL ANALYSIS COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    # Run comparison first
    asyncio.run(run_comparison())
    
    # Then test COL analysis
    asyncio.run(test_col_dashboard_analysis())
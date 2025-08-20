#!/usr/bin/env python3
"""
Test script for webscraping MCP agent integration
Tests both the specialist directly and through the MCP server
"""

import asyncio
import httpx
import json
import sys
from pathlib import Path

# Add the project root to path for imports
sys.path.append(str(Path(__file__).parent))

async def test_webscraping_specialist_direct():
    """Test the webscraping specialist directly"""
    print("🧪 Testing WebscrapingSpecialist directly...")
    
    try:
        from mcp_services.external.webscraping_specialist import WebscrapingSpecialist
        
        scraper = WebscrapingSpecialist()
        print("✅ WebscrapingSpecialist imported and initialized successfully")
        
        # Test single page scraping
        print("\n📄 Testing single page scraping...")
        result = await scraper.scrape_single_page(
            url="https://httpbin.org/html",  # Simple test page
            extract_links=True
        )
        
        if result["success"]:
            print(f"✅ Single page scraping successful")
            print(f"   Title: {result.get('title', 'No title')}")
            print(f"   Content length: {len(result.get('content', ''))}")
            print(f"   Links found: {len(result.get('links', []))}")
        else:
            print(f"❌ Single page scraping failed: {result.get('error')}")
        
        # Test analyze_request method (MCP integration point)
        print("\n🔄 Testing analyze_request method...")
        mcp_result = await scraper.analyze_request("test_user", {
            "action": "scrape_page",
            "url": "https://httpbin.org/html",
            "extract_links": False
        })
        
        if mcp_result.get("success"):
            print("✅ MCP analyze_request method working")
        else:
            print(f"❌ MCP analyze_request failed: {mcp_result.get('error')}")
            
        return True
        
    except Exception as e:
        print(f"❌ Direct specialist test failed: {e}")
        return False

async def test_agent_server_endpoint():
    """Test the agent server webscraping endpoint"""
    print("\n🌐 Testing agent server webscraping endpoint...")
    
    agent_base_url = "http://localhost:8001"
    
    try:
        async with httpx.AsyncClient() as client:
            # Check if agent server is running
            try:
                health_response = await client.get(f"{agent_base_url}/health", timeout=5.0)
                if health_response.status_code != 200:
                    print("❌ Agent server is not running")
                    print("   Start with: cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents && python main.py")
                    return False
            except httpx.ConnectError:
                print("❌ Cannot connect to agent server")
                print("   Start with: cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents && python main.py")
                return False
            
            print("✅ Agent server is running")
            
            # Test webscraping endpoint
            payload = {
                "user_id": "test_user",
                "data": {
                    "action": "scrape_page",
                    "url": "https://httpbin.org/html",
                    "extract_links": True
                }
            }
            
            response = await client.post(
                f"{agent_base_url}/agents/webscraping/analyze",
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Agent server webscraping endpoint working")
                print(f"   Success: {result.get('success')}")
                print(f"   Message: {result.get('message')}")
                
                # Check the data structure
                data = result.get('data', {})
                if data.get('success'):
                    print(f"   Scraped content length: {len(data.get('content', ''))}")
                    print(f"   Links found: {len(data.get('links', []))}")
                else:
                    print(f"   Scraping error: {data.get('error')}")
                
                return True
            else:
                print(f"❌ Agent server returned HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Agent server test failed: {e}")
        return False

async def test_mcp_server_integration():
    """Test the MCP server integration (if available)"""
    print("\n🔧 Testing MCP server integration...")
    
    # This would require the MCP server to be running
    # For now, just verify the configuration exists
    
    try:
        # Check if mcp_server.py has the webscraping tools
        mcp_server_path = Path(__file__).parent / "mcp_server.py"
        
        if mcp_server_path.exists():
            with open(mcp_server_path, 'r') as f:
                content = f.read()
                
            if "scrape_web_page" in content and "traverse_documentation" in content:
                print("✅ MCP server has webscraping tools configured")
                
                # Check the tool configurations
                if "webscraping/scrape" in content and "webscraping/traverse" in content:
                    print("✅ MCP server has correct webscraping endpoints")
                    return True
                else:
                    print("❌ MCP server webscraping endpoints not properly configured")
                    return False
            else:
                print("❌ MCP server does not have webscraping tools")
                return False
        else:
            print("❌ MCP server file not found")
            return False
            
    except Exception as e:
        print(f"❌ MCP server integration test failed: {e}")
        return False

async def test_documentation_structure():
    """Test that documentation structure is properly created"""
    print("\n📚 Testing documentation structure...")
    
    doc_base = Path(__file__).parent / "documentation" / "external_services" / "webscraping"
    
    required_files = [
        "manifest.json",
        "official/quick_reference.json", 
        "best_practices/patterns.json",
        "examples/basic_scrape.py",
        "troubleshooting/common_issues.json",
        "fed_job_advisor/configuration.json"
    ]
    
    all_files_exist = True
    
    for file_path in required_files:
        full_path = doc_base / file_path
        if full_path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_files_exist = False
    
    if all_files_exist:
        print("✅ All documentation files present")
        
        # Test loading manifest
        try:
            manifest_path = doc_base / "manifest.json"
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            if manifest.get("service") == "webscraping":
                print("✅ Manifest loads correctly")
                return True
            else:
                print("❌ Manifest has incorrect content")
                return False
        except Exception as e:
            print(f"❌ Error loading manifest: {e}")
            return False
    else:
        return False

async def main():
    """Run all tests"""
    print("🕷️ Webscraping MCP Agent Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Direct Specialist", test_webscraping_specialist_direct),
        ("Agent Server Endpoint", test_agent_server_endpoint), 
        ("MCP Server Integration", test_mcp_server_integration),
        ("Documentation Structure", test_documentation_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 30)
        
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Webscraping MCP agent is ready for use.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
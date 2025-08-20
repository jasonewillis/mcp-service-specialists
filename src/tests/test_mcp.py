#!/usr/bin/env python3
"""
Test script for Fed Job Advisor MCP Server
"""

import asyncio
import json
from mcp_server import FedJobAdvisorMCP

async def test_mcp_server():
    """Test the MCP server functionality"""
    
    print("🧪 Testing Fed Job Advisor MCP Server")
    print("=" * 50)
    
    # Create server instance
    server = FedJobAdvisorMCP()
    
    # Check tool registration
    print(f"✅ Registered {len(server.agent_tools)} agent tools:")
    
    for tool_name, config in server.agent_tools.items():
        print(f"   • {tool_name}: {config['description'][:60]}...")
    
    print("\n📋 Available Agent Tools:")
    print("=" * 30)
    
    for tool_name, config in server.agent_tools.items():
        agent_role = config["agent_role"]
        endpoint = config["endpoint"]
        print(f"• {tool_name}")
        print(f"  Role: {agent_role}")
        print(f"  Endpoint: {endpoint}")
        print()
    
    print("🎯 MCP Server ready for Claude Code integration!")
    print("\nNext steps:")
    print("1. Start agent service: cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents && python main.py")
    print("2. Add MCP server to Claude Code configuration")
    print("3. Restart Claude Code")
    print("4. Use agent tools directly in Claude Code!")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
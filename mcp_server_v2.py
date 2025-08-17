#!/usr/bin/env python3
"""
Fed Job Advisor MCP Server V2 - Service Provider Architecture
Implements Jason Zhou's approach: Research → Implement → Review
"""

import asyncio
import httpx
import json
import logging
import sys
from pathlib import Path
from typing import Any, Sequence, Dict, Optional

# Add the mcp_services directory to path
sys.path.append(str(Path(__file__).parent / "mcp_services"))

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from mcp.server.stdio import stdio_server
except ImportError:
    print("MCP not installed. Run: pip install mcp")
    exit(1)

# Import service provider researchers
from external.usajobs_researcher import USAJobsResearcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fed-job-advisor-mcp-v2")

class FedJobAdvisorMCPv2:
    """
    Enhanced MCP Server with Service Provider Architecture
    Phase 1: Research (via service experts)
    Phase 2: Implementation (by Claude/parent agent)
    Phase 3: Review (via service experts)
    """
    
    def __init__(self):
        self.agent_base_url = "http://localhost:8001"
        self.server = Server("fed-job-advisor-v2")
        
        # Initialize service provider researchers
        self.researchers = {
            "usajobs": USAJobsResearcher()
        }
        
        # Keep track of existing tools
        self.legacy_tools = {}
        self.research_tools = {}
        
        self._setup_tools()
    
    def _setup_tools(self):
        """Register all agent tools with MCP"""
        
        # New Research/Review Tools (Jason Zhou pattern)
        research_tools = {
            "research_usajobs_api": {
                "description": "Research USAJobs API implementation. Creates detailed plan with Fields=Full requirement. Use BEFORE implementing any USAJobs features.",
                "handler": self._research_usajobs,
                "schema": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "What you need to implement with USAJobs API"
                        },
                        "user_id": {
                            "type": "string",
                            "default": "claude_code",
                            "description": "User identifier"
                        }
                    },
                    "required": ["task"]
                }
            },
            
            "review_usajobs_implementation": {
                "description": "Review USAJobs API code for compliance. Checks for Fields=Full and best practices. Use AFTER implementing to verify correctness.",
                "handler": self._review_usajobs,
                "schema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Implementation code to review"
                        },
                        "user_id": {
                            "type": "string",
                            "default": "claude_code",
                            "description": "User identifier"
                        }
                    },
                    "required": ["code"]
                }
            }
        }
        
        # Legacy tools (keeping your existing ones)
        legacy_tools = {
            "analyze_data_scientist_profile": {
                "description": "Analyze candidate profile for federal data scientist positions (Series 1560)",
                "agent_role": "data_scientist",
                "endpoint": "data-scientist/analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "skills": {"type": "array", "items": {"type": "string"}},
                        "experience": {"type": "string"},
                        "target_grade": {"type": "string", "default": "GS-13"}
                    },
                    "required": ["user_id", "skills", "experience"]
                }
            },
            
            "route_to_best_agent": {
                "description": "Intelligent agent router that analyzes tasks and coordinates agents",
                "agent_role": "agent_router",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "analysis_type": {"type": "string"},
                        "request": {"type": "string"},
                        "task": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            }
        }
        
        # Store tools
        self.research_tools = research_tools
        self.legacy_tools = legacy_tools
        
        # Register tools with the server
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            tools = []
            
            # Add research tools
            for tool_name, config in self.research_tools.items():
                tools.append(
                    Tool(
                        name=tool_name,
                        description=config["description"],
                        inputSchema=config["schema"]
                    )
                )
            
            # Add legacy tools
            for tool_name, config in self.legacy_tools.items():
                tools.append(
                    Tool(
                        name=tool_name,
                        description=config["description"],
                        inputSchema=config["schema"]
                    )
                )
            
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
            """Handle tool calls by routing to appropriate handler"""
            
            # Check if it's a research tool
            if name in self.research_tools:
                handler = self.research_tools[name]["handler"]
                return await handler(arguments)
            
            # Check if it's a legacy tool
            elif name in self.legacy_tools:
                return await self._call_legacy_agent(name, arguments)
            
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Unknown tool: {name}"
                )]
    
    async def _research_usajobs(self, args: dict) -> Sequence[TextContent]:
        """Handle USAJobs research requests"""
        try:
            researcher = self.researchers["usajobs"]
            result = await researcher.research_task(
                task=args.get("task", ""),
                user_id=args.get("user_id", "claude_code")
            )
            
            if result["success"]:
                response = (
                    f"✅ **USAJobs Research Complete**\n\n"
                    f"**Report**: `{result['report_path']}`\n"
                    f"**Summary**: {result['summary']}\n\n"
                    f"**Critical Reminders**:\n"
                )
                for reminder in result["critical_reminders"]:
                    response += f"• {reminder}\n"
                
                response += f"\n**API Calls Required**: {result['api_calls']}\n"
                response += f"\n📋 **Next Step**: Implement based on the research report, then use `review_usajobs_implementation` to verify."
                
                return [TextContent(type="text", text=response)]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Research failed: {result.get('error', 'Unknown error')}"
                )]
                
        except Exception as e:
            logger.error(f"USAJobs research failed: {e}")
            return [TextContent(
                type="text",
                text=f"❌ Research error: {str(e)}"
            )]
    
    async def _review_usajobs(self, args: dict) -> Sequence[TextContent]:
        """Handle USAJobs implementation review"""
        try:
            researcher = self.researchers["usajobs"]
            result = await researcher.review_implementation(
                code=args.get("code", ""),
                user_id=args.get("user_id", "claude_code")
            )
            
            # Format review response
            response = f"## 🔍 USAJobs Implementation Review\n\n"
            response += f"**Score**: {result['score']}/100\n"
            response += f"**Status**: {'✅ Compliant' if result['compliant'] else '❌ Non-Compliant'}\n\n"
            
            if result["violations"]:
                response += "### ❌ Critical Violations\n"
                for violation in result["violations"]:
                    response += f"• {violation}\n"
                response += "\n"
            
            if result["warnings"]:
                response += "### ⚠️ Warnings\n"
                for warning in result["warnings"]:
                    response += f"• {warning}\n"
                response += "\n"
            
            if result["passed"]:
                response += "### ✅ Passed Checks\n"
                for check in result["passed"]:
                    response += f"• {check}\n"
                response += "\n"
            
            response += f"### 📋 Recommendation\n{result['recommendation']}\n"
            
            if not result["compliant"]:
                response += "\n**Required Actions**:\n"
                response += "1. Fix all critical violations\n"
                response += "2. Run review again after fixes\n"
                response += "3. Do not deploy until compliant\n"
            
            return [TextContent(type="text", text=response)]
            
        except Exception as e:
            logger.error(f"USAJobs review failed: {e}")
            return [TextContent(
                type="text",
                text=f"❌ Review error: {str(e)}"
            )]
    
    async def _call_legacy_agent(self, tool_name: str, args: dict) -> Sequence[TextContent]:
        """Call legacy agents via HTTP API (backward compatibility)"""
        
        config = self.legacy_tools[tool_name]
        agent_role = config["agent_role"]
        endpoint = config["endpoint"]
        
        try:
            async with httpx.AsyncClient() as client:
                # Check if agent service is running
                try:
                    health_response = await client.get(f"{self.agent_base_url}/health", timeout=5.0)
                    if health_response.status_code != 200:
                        return [TextContent(
                            type="text",
                            text="❌ Agent service not running. Start with: python main.py"
                        )]
                except httpx.ConnectError:
                    return [TextContent(
                        type="text",
                        text="❌ Cannot connect to agent service at port 8001"
                    )]
                
                # Make the agent call
                if endpoint == "analyze":
                    url = f"{self.agent_base_url}/agents/analyze"
                    payload = {
                        "role": agent_role,
                        "user_id": args.get("user_id", "claude_code"),
                        "data": args
                    }
                else:
                    url = f"{self.agent_base_url}/agents/{endpoint}"
                    payload = args
                
                response = await client.post(url, json=payload, timeout=60.0)
                
                if response.status_code == 200:
                    result = response.json()
                    return [TextContent(
                        type="text",
                        text=f"✅ {tool_name}: {json.dumps(result, indent=2)}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"❌ Agent error: {response.text}"
                    )]
                    
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error: {str(e)}"
            )]
    
    async def run(self):
        """Run the MCP server"""
        logger.info("Starting Fed Job Advisor MCP Server V2...")
        logger.info("Service Provider Architecture: Research → Implement → Review")
        logger.info(f"Available researchers: {list(self.researchers.keys())}")
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

async def main():
    """Main entry point"""
    server = FedJobAdvisorMCPv2()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Fed Job Advisor MCP Server
Exposes specialized federal job agents as MCP tools for Claude Code integration
"""

import asyncio
import httpx
import json
import logging
import os
from typing import Any, Sequence, Dict, Optional

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from mcp.server.stdio import stdio_server
except ImportError:
    print("MCP not installed. Run: pip install mcp")
    exit(1)

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '../../config/mcp_server.json')
with open(config_path, 'r') as f:
    MCP_CONFIG = json.load(f)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fed-job-advisor-mcp")

class FedJobAdvisorMCP:
    """MCP Server for Fed Job Advisor Agents"""
    
    def __init__(self):
        self.agent_base_url = MCP_CONFIG.get("agent_base_url", "http://localhost:8001")
        server_name = MCP_CONFIG["server_info"]["name"]
        self.server = Server(server_name)
        self.agent_tools = {}
        self._setup_tools()
    
    def _setup_tools(self):
        """Register all agent tools with MCP"""
        
        # Define available agent tools
        agent_tools = {
            "analyze_data_scientist_profile": {
                "description": "Analyze candidate profile for federal data scientist positions (Series 1560). Evaluates skills, projects, and experience alignment.",
                "agent_role": "data_scientist",
                "endpoint": "data-scientist/analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "skills": {"type": "array", "items": {"type": "string"}, "description": "Technical skills list"},
                        "experience": {"type": "string", "description": "Professional experience summary"},
                        "projects": {"type": "array", "description": "Project portfolio"},
                        "education": {"type": "object", "description": "Education background"},
                        "target_grade": {"type": "string", "default": "GS-13", "description": "Target grade level"}
                    },
                    "required": ["user_id", "skills", "experience"]
                }
            },
            
            "analyze_statistician_profile": {
                "description": "Analyze candidate profile for federal statistician positions (Series 1530). Focuses on statistical methodology and research experience.",
                "agent_role": "statistician",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "experience": {"type": "string", "description": "Statistical experience summary"},
                        "skills": {"type": "array", "items": {"type": "string"}, "description": "Statistical tools and methods"},
                        "publications": {"type": "array", "description": "Research publications"},
                        "target_grade": {"type": "string", "default": "GS-12", "description": "Target grade level"},
                        "target_agency": {"type": "string", "description": "Target agency (Census, BLS, etc.)"}
                    },
                    "required": ["user_id", "experience"]
                }
            },
            
            "analyze_database_admin_profile": {
                "description": "Analyze candidate profile for federal database administrator positions (Series 2210/0334). Evaluates platform expertise and security knowledge.",
                "agent_role": "database_admin",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "skills": {"type": "array", "items": {"type": "string"}, "description": "Database platforms and tools"},
                        "experience": {"type": "string", "description": "DBA experience summary"},
                        "certifications": {"type": "array", "items": {"type": "string"}, "description": "Professional certifications"},
                        "target_grade": {"type": "string", "default": "GS-12", "description": "Target grade level"},
                        "target_agency": {"type": "string", "description": "Target federal agency"}
                    },
                    "required": ["user_id", "skills", "experience"]
                }
            },
            
            "analyze_devops_profile": {
                "description": "Analyze candidate profile for federal DevOps engineer positions (Series 2210). Focuses on CI/CD, containers, and cloud platforms.",
                "agent_role": "devops",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "skills": {"type": "array", "items": {"type": "string"}, "description": "DevOps tools and platforms"},
                        "experience": {"type": "string", "description": "DevOps experience summary"},
                        "certifications": {"type": "array", "items": {"type": "string"}, "description": "Cloud and DevOps certifications"},
                        "projects": {"type": "array", "description": "DevOps projects and implementations"},
                        "target_grade": {"type": "string", "default": "GS-13", "description": "Target grade level"}
                    },
                    "required": ["user_id", "skills", "experience"]
                }
            },
            
            "analyze_it_specialist_profile": {
                "description": "Analyze candidate profile for general federal IT specialist positions (Series 2210). Covers systems, network, security, and support roles.",
                "agent_role": "it_specialist",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "skills": {"type": "array", "items": {"type": "string"}, "description": "IT skills and technologies"},
                        "experience": {"type": "string", "description": "IT experience summary"},
                        "certifications": {"type": "array", "items": {"type": "string"}, "description": "IT certifications"},
                        "target_grade": {"type": "string", "default": "GS-11", "description": "Target grade level"},
                        "target_specialty": {"type": "string", "description": "IT specialty area (INFOSEC, SYSADMIN, etc.)"}
                    },
                    "required": ["user_id", "skills", "experience"]
                }
            },
            
            "check_essay_compliance": {
                "description": "Check federal merit hiring essay for compliance (NEVER writes content, only analyzes structure). Validates STAR method and word limits.",
                "agent_role": "essay_guidance",
                "endpoint": "essay/analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "essay_text": {"type": "string", "description": "Essay text to analyze"},
                        "essay_number": {"type": "integer", "description": "Essay question number"},
                        "experience": {"type": "string", "description": "Candidate's relevant experience"}
                    },
                    "required": ["user_id", "essay_text", "essay_number"]
                }
            },
            
            "analyze_resume_compression": {
                "description": "Analyze federal resume for compression to 2-page requirement. Identifies redundancy and prioritizes content.",
                "agent_role": "resume_compression",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "resume_text": {"type": "string", "description": "Complete resume text"},
                        "current_pages": {"type": "integer", "description": "Current page count"},
                        "target_position": {"type": "string", "description": "Target position title"},
                        "target_series": {"type": "string", "description": "Target job series"}
                    },
                    "required": ["user_id", "resume_text"]
                }
            },
            
            "research_executive_orders": {
                "description": "Research executive orders and federal policies for job application relevance. Analyzes policy impact and extracts keywords.",
                "agent_role": "executive_order",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "order_number": {"type": "string", "description": "Executive order number"},
                        "policy_text": {"type": "string", "description": "Policy or order text"},
                        "target_position": {"type": "string", "description": "Target position"},
                        "target_agency": {"type": "string", "description": "Target agency"},
                        "research_focus": {"type": "string", "default": "job_relevance", "description": "Research focus area"}
                    },
                    "required": ["user_id", "policy_text"]
                }
            },
            
            "analyze_job_market": {
                "description": "Provide federal job market analytics and intelligence. Analyzes trends, salary data, competition levels, and skill demands.",
                "agent_role": "analytics",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "analysis_type": {"type": "string", "default": "comprehensive", "description": "Type of analysis"},
                        "target_position": {"type": "string", "description": "Target position title"},
                        "target_series": {"type": "string", "description": "Target job series"},
                        "time_frame": {"type": "string", "default": "last_12_months", "description": "Analysis time frame"},
                        "market_data": {"type": "object", "description": "Available market data"}
                    },
                    "required": ["user_id"]
                }
            },
            
            "orchestrate_job_collection": {
                "description": "Monitor and orchestrate federal job data collection pipeline. Checks API health, data quality, and collection performance.",
                "agent_role": "job_collector",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "collection_stats": {"type": "object", "description": "Collection statistics"},
                        "performance_data": {"type": "object", "description": "Performance metrics"},
                        "error_logs": {"type": "array", "description": "Recent error logs"},
                        "api_status": {"type": "object", "description": "API status information"},
                        "focus_area": {"type": "string", "default": "overall_health", "description": "Focus area for analysis"}
                    },
                    "required": ["user_id"]
                }
            },
            
            "route_to_best_agent": {
                "description": "Intelligent agent router that analyzes tasks and coordinates the right agents. Knows project constraints, data requirements, and Merit Hiring rules. Use this to determine which agents to use.",
                "agent_role": "agent_router",
                "endpoint": "analyze",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "analysis_type": {"type": "string", "enum": ["data_request", "merit_compliance", "collection_guidance", "agent_coordination", "data_validation", "general"], "default": "general", "description": "Type of context analysis needed"},
                        "request": {"type": "string", "description": "Request text for data analysis"},
                        "action": {"type": "string", "description": "Action to check for Merit compliance"},
                        "task": {"type": "string", "description": "Task for agent coordination suggestions"},
                        "data": {"type": "object", "description": "Data to validate against requirements"}
                    },
                    "required": ["user_id"]
                }
            },

            "scrape_web_page": {
                "description": "Scrape content from a single web page with intelligent content extraction. Returns main content, links, and metadata.",
                "agent_role": "webscraping",
                "endpoint": "webscraping/scrape",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "url": {"type": "string", "description": "Target URL to scrape"},
                        "extract_links": {"type": "boolean", "default": True, "description": "Whether to extract links from the page"},
                        "content_selector": {"type": "string", "description": "CSS selector for main content (optional)"},
                        "action": {"type": "string", "default": "scrape_page", "description": "Action type"}
                    },
                    "required": ["user_id", "url"]
                }
            },

            "traverse_documentation": {
                "description": "Traverse and scrape an entire documentation website following links intelligently. Respects rate limits and robots.txt.",
                "agent_role": "webscraping",
                "endpoint": "webscraping/traverse",
                "schema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User identifier"},
                        "start_url": {"type": "string", "description": "Starting URL for documentation traversal"},
                        "max_depth": {"type": "integer", "default": 3, "description": "Maximum link depth to follow"},
                        "max_pages": {"type": "integer", "default": 50, "description": "Maximum number of pages to scrape"},
                        "link_patterns": {"type": "array", "items": {"type": "string"}, "description": "Regex patterns for links to follow"},
                        "action": {"type": "string", "default": "traverse_documentation", "description": "Action type"}
                    },
                    "required": ["user_id", "start_url"]
                }
            }
        }
        
        # Store tool configurations for later use
        self.agent_tools = agent_tools
        
        # Register tools with the server
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return list of available tools"""
            tools = []
            for tool_name, config in self.agent_tools.items():
                tools.append(
                    Tool(
                        name=tool_name,
                        description=config["description"],
                        inputSchema=config["schema"]
                    )
                )
            return tools
        
        @self.server.call_tool()
        async def call_agent_tool(name: str, arguments: dict) -> Sequence[TextContent]:
            """Handle tool calls by routing to appropriate agent"""
            return await self._call_agent(name, arguments)
    
    async def _call_agent(self, tool_name: str, args: dict) -> Sequence[TextContent]:
        """Call the appropriate agent via HTTP API"""
        
        if tool_name not in self.agent_tools:
            return [TextContent(
                type="text", 
                text=f"❌ Unknown agent tool: {tool_name}"
            )]
        
        config = self.agent_tools[tool_name]
        agent_role = config["agent_role"]
        endpoint = config["endpoint"]
        
        try:
            # Check if agent service is running
            async with httpx.AsyncClient() as client:
                try:
                    health_response = await client.get(f"{self.agent_base_url}/health", timeout=5.0)
                    if health_response.status_code != 200:
                        return [TextContent(
                            type="text",
                            text="❌ Agent service is not running. Start with: cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents && python main.py"
                        )]
                except httpx.ConnectError:
                    return [TextContent(
                        type="text",
                        text="❌ Cannot connect to agent service. Start with: cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents && python main.py"
                    )]
                
                # Make the agent call
                if endpoint == "analyze":
                    # General agent endpoint
                    url = f"{self.agent_base_url}/agents/analyze"
                    payload = {
                        "role": agent_role,
                        "user_id": args.get("user_id", "claude_code_user"),
                        "data": args
                    }
                elif endpoint.startswith("webscraping/"):
                    # Webscraping specialist endpoints
                    url = f"{self.agent_base_url}/agents/webscraping/analyze"
                    payload = {
                        "user_id": args.get("user_id", "claude_code_user"),
                        "data": args
                    }
                else:
                    # Specialized endpoint
                    url = f"{self.agent_base_url}/agents/{endpoint}"
                    payload = args
                    payload["user_id"] = args.get("user_id", "claude_code_user")
                
                logger.info(f"Calling agent: {tool_name} -> {url}")
                
                response = await client.post(
                    url,
                    json=payload,
                    timeout=60.0  # Longer timeout for agent processing
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Format the response nicely
                    success = result.get("success", True)
                    message = result.get("message", "Analysis completed")
                    data = result.get("data", {})
                    
                    if success:
                        formatted_response = f"✅ **{tool_name.replace('_', ' ').title()}**\n\n"
                        formatted_response += f"**Analysis:** {message}\n\n"
                        
                        if data:
                            formatted_response += "**Detailed Results:**\n"
                            formatted_response += self._format_agent_data(data)
                        
                        return [TextContent(type="text", text=formatted_response)]
                    else:
                        return [TextContent(
                            type="text",
                            text=f"❌ Agent analysis failed: {message}"
                        )]
                else:
                    error_detail = response.text if response.text else f"HTTP {response.status_code}"
                    return [TextContent(
                        type="text",
                        text=f"❌ Agent API error: {error_detail}"
                    )]
                    
        except httpx.TimeoutException:
            return [TextContent(
                type="text",
                text="⏱️ Agent request timed out. The analysis may be complex - try again or check agent service."
            )]
        except Exception as e:
            logger.error(f"Agent call failed: {e}")
            return [TextContent(
                type="text",
                text=f"❌ Unexpected error calling agent: {str(e)}"
            )]
    
    def _format_agent_data(self, data: Dict) -> str:
        """Format agent response data for display"""
        
        formatted = ""
        
        # Handle recommendations
        if "recommendations" in data:
            recommendations = data["recommendations"]
            formatted += "\n**📋 Recommendations:**\n"
            
            for category, items in recommendations.items():
                if isinstance(items, list) and items:
                    formatted += f"\n*{category.replace('_', ' ').title()}:*\n"
                    for item in items:
                        formatted += f"• {item}\n"
        
        # Handle key metrics/scores
        metrics_keys = ["score", "level", "grade", "assessment", "analysis"]
        for key in metrics_keys:
            if key in data:
                formatted += f"\n**{key.title()}:** {data[key]}\n"
        
        # Handle specific analysis results
        if "skill_analysis" in data:
            formatted += "\n**🔧 Skills Analysis:**\n"
            skill_data = data["skill_analysis"]
            if isinstance(skill_data, dict):
                for category, details in skill_data.items():
                    formatted += f"• *{category}:* {details}\n"
        
        # Handle compliance results
        if "compliance_status" in data:
            status = data["compliance_status"]
            formatted += f"\n**✅ Compliance Status:** {status}\n"
        
        # Handle any warnings or issues
        if "warnings" in data:
            warnings = data["warnings"]
            if warnings:
                formatted += "\n**⚠️ Warnings:**\n"
                for warning in warnings:
                    formatted += f"• {warning}\n"
        
        return formatted
    
    async def run(self):
        """Run the MCP server"""
        logger.info("Starting Fed Job Advisor MCP Server...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

async def main():
    """Main entry point"""
    server = FedJobAdvisorMCP()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
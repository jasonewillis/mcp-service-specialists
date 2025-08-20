#!/usr/bin/env python3
"""
MCP Agent Server
Hosts the general-purpose MCP agent and provides standardized interface.
Designed for local LLM operation to conserve Claude Code tokens.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add parent directory to path for agent imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.general_purpose_agent import GeneralPurposeAgent, AgentRequest, AgentResponse

# MCP Protocol imports
try:
    from mcp.server.models import InitializeResult
    from mcp.server import NotificationOptions, Server
    from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
    import mcp.types as types
except ImportError:
    print("Warning: MCP server libraries not available. Install with: pip install mcp-server")
    # Fallback to basic server implementation
    Server = None

@dataclass
class MCPAgentConfig:
    """Configuration for MCP Agent Server"""
    name: str = "fed-job-advisor-general-purpose-agent"
    version: str = "1.0.0"
    description: str = "General-purpose MCP agent for Fed Job Advisor using local LLM"
    host: str = "localhost"
    port: int = 8080

class MCPAgentServer:
    """
    MCP Agent Server hosting general-purpose agent
    """
    
    def __init__(self, config: Optional[MCPAgentConfig] = None):
        self.config = config or MCPAgentConfig()
        self.agent = GeneralPurposeAgent()
        self.server = None
        self.setup_logging()
        
        # Initialize MCP server if available
        if Server:
            self.server = Server(self.config.name)
            self.setup_mcp_handlers()
    
    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/mcp_server.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_mcp_handlers(self):
        """Set up MCP protocol handlers"""
        if not self.server:
            return
            
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources"""
            return [
                Resource(
                    uri="agent://general-purpose",
                    name="General Purpose Agent",
                    description="Fed Job Advisor general-purpose analysis and implementation agent",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read agent resource information"""
            if uri == "agent://general-purpose":
                return json.dumps({
                    "name": "General Purpose Agent",
                    "description": "Handles complex research, analysis, and implementation tasks",
                    "capabilities": [
                        "Technical analysis",
                        "Code implementation guidance", 
                        "Project management recommendations",
                        "Risk assessment",
                        "Cost-benefit analysis"
                    ],
                    "model": self.agent.model,
                    "cost": "$0.00 (local inference)",
                    "context": "Fed Job Advisor federal job search platform"
                })
            
            raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="analyze_task",
                    description="Analyze complex tasks and provide implementation guidance",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {
                                "type": "string",
                                "description": "Description of the task to analyze"
                            },
                            "context": {
                                "type": "object", 
                                "description": "Additional context for the task"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "critical"],
                                "default": "medium"
                            }
                        },
                        "required": ["task_description"]
                    }
                ),
                Tool(
                    name="research_solution",
                    description="Research and provide detailed solution recommendations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "research_query": {
                                "type": "string",
                                "description": "Research question or problem statement"
                            },
                            "output_format": {
                                "type": "string",
                                "enum": ["markdown", "json", "structured"],
                                "default": "markdown"
                            }
                        },
                        "required": ["research_query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Handle tool calls"""
            
            if name == "analyze_task":
                request = AgentRequest(
                    task_description=arguments["task_description"],
                    context=arguments.get("context", {}),
                    priority=arguments.get("priority", "medium")
                )
                
                response = await self.agent.process_request(request)
                
                result = {
                    "success": response.success,
                    "analysis": response.content,
                    "metadata": response.metadata,
                    "cost": response.cost_estimate,
                    "tokens_used": response.tokens_used
                }
                
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "research_solution":
                request = AgentRequest(
                    task_description=f"Research: {arguments['research_query']}",
                    context={"research_type": "solution_recommendation"},
                    output_format=arguments.get("output_format", "markdown")
                )
                
                response = await self.agent.process_request(request)
                
                if arguments.get("output_format") == "json":
                    result = {
                        "research_query": arguments["research_query"],
                        "findings": response.content,
                        "confidence": "high" if response.success else "low",
                        "metadata": response.metadata
                    }
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]
                else:
                    return [TextContent(type="text", text=response.content)]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def start_mcp_server(self):
        """Start MCP server"""
        if not self.server:
            self.logger.warning("MCP server not available, running in basic mode")
            return
            
        try:
            from mcp.server.stdio import stdio_server
            
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializeResult(
                        protocolVersion="2024-11-05",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                        ),
                        serverInfo={
                            "name": self.config.name,
                            "version": self.config.version,
                            "description": self.config.description
                        }
                    )
                )
        except Exception as e:
            self.logger.error(f"MCP server error: {e}")
            raise
    
    async def start_http_server(self):
        """Start basic HTTP server as fallback"""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import json
        import threading
        
        class AgentHandler(BaseHTTPRequestHandler):
            def __init__(self, agent_server, *args, **kwargs):
                self.agent_server = agent_server
                super().__init__(*args, **kwargs)
            
            def do_POST(self):
                if self.path == '/agent/process':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        data = json.loads(post_data.decode('utf-8'))
                        request = AgentRequest(**data)
                        
                        # Run async request in thread
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        response = loop.run_until_complete(
                            self.agent_server.agent.process_request(request)
                        )
                        loop.close()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        
                        result = {
                            "success": response.success,
                            "content": response.content,
                            "metadata": response.metadata,
                            "cost_estimate": response.cost_estimate,
                            "tokens_used": response.tokens_used
                        }
                        
                        self.wfile.write(json.dumps(result).encode())
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_GET(self):
                if self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "healthy",
                        "agent": self.config.name,
                        "model": self.agent_server.agent.model
                    }).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
        
        # Create handler with server reference
        handler = lambda *args, **kwargs: AgentHandler(self, *args, **kwargs)
        
        httpd = HTTPServer((self.config.host, self.config.port), handler)
        self.logger.info(f"Starting HTTP server on {self.config.host}:{self.config.port}")
        
        # Run in thread to avoid blocking
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return httpd
    
    async def run(self):
        """Run the MCP agent server"""
        self.logger.info(f"Starting {self.config.name} v{self.config.version}")
        
        # Verify agent is ready
        if not self.agent.setup_ollama():
            self.logger.error("Failed to setup Ollama - server cannot start")
            return
        
        try:
            if self.server:
                # Run MCP server
                await self.start_mcp_server()
            else:
                # Fallback to HTTP server
                httpd = await self.start_http_server()
                self.logger.info("Server running - Press Ctrl+C to stop")
                
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    self.logger.info("Shutting down server...")
                    httpd.shutdown()
                    
        except Exception as e:
            self.logger.error(f"Server error: {e}")
            raise

def main():
    """Main server entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Agent Server")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--mode", choices=["mcp", "http"], default="mcp", help="Server mode")
    
    args = parser.parse_args()
    
    config = MCPAgentConfig(
        host=args.host,
        port=args.port
    )
    
    server = MCPAgentServer(config)
    
    try:
        if args.mode == "mcp":
            asyncio.run(server.start_mcp_server())
        else:
            asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Server failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
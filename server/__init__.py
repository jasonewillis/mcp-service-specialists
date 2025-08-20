"""
MCP Agent Server Package
Provides MCP server infrastructure for Fed Job Advisor external service agents.
"""

from .mcp_server import MCPAgentServer, MCPAgentConfig

__version__ = "1.0.0"
__all__ = ["MCPAgentServer", "MCPAgentConfig"]
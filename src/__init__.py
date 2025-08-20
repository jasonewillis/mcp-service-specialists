"""
Fed Job Advisor MCP Agent System

A comprehensive MCP (Model Context Protocol) server providing specialized
federal job application assistance through AI agents.

Core Components:
- mcp_services: External service specialists (Stripe, Sentry, Docker, etc.)
- agents: Federal job application agents (data scientist, statistician, etc.)
- core: Core MCP server functionality
- utils: Shared utilities and helpers
- tests: Test suite

Version: 2.0.0 (2024 MCP Standards)
"""

__version__ = "2.0.0"
__author__ = "Fed Job Advisor System"
__license__ = "MIT"

# Core exports
from .core.mcp_server import FedJobAdvisorMCP
from .core.main import main

__all__ = ["FedJobAdvisorMCP", "main"]
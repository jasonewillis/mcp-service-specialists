#!/usr/bin/env python3
"""
Fed Job Advisor MCP Server - Entry Point

2024 MCP Standards Compliant Entry Point
Imports from standardized src/ structure
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.mcp_server import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
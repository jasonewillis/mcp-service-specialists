#!/usr/bin/env python3
"""
Fed Job Advisor MCP Agent System - Entry Point

2024 MCP Standards Compliant Entry Point
Imports from standardized src/ structure
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.main import main

if __name__ == "__main__":
    main()
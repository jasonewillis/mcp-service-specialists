#!/usr/bin/env python3
"""
Start MCP Agent Server
Quick launcher for the Fed Job Advisor MCP agent server.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama if not running"""
    print("🚀 Starting Ollama...")
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["brew", "services", "start", "ollama"], check=True)
        else:
            subprocess.run(["systemctl", "--user", "start", "ollama"], check=True)
        
        # Wait for Ollama to start
        import time
        for i in range(30):
            if check_ollama():
                print("✅ Ollama is running")
                return True
            time.sleep(1)
        
        return False
    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")
        return False

def main():
    """Main launcher"""
    print("🤖 Fed Job Advisor MCP Agent Server Launcher")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Check if Ollama is running
    if not check_ollama():
        print("⚠️  Ollama not running, attempting to start...")
        if not start_ollama():
            print("❌ Could not start Ollama")
            print("Manual fix: brew install ollama && ollama pull llama3.1:8b")
            sys.exit(1)
    else:
        print("✅ Ollama is running")
    
    # Set up environment
    os.environ["PYTHONPATH"] = str(Path(__file__).parent)
    
    # Start server
    print("🚀 Starting MCP Agent Server...")
    try:
        from server.mcp_server import main as server_main
        server_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Fix: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
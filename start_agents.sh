#!/bin/bash
# Start Fed Job Advisor Agent System

echo "🚀 Starting Fed Job Advisor Agent System"
echo "========================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Run this script from the Agents directory"
    echo "   cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents"
    exit 1
fi

# Check if port 8001 is already in use
if lsof -i :8001 >/dev/null 2>&1; then
    echo "⚠️  Port 8001 is already in use"
    echo "   Kill existing process or use different port"
    echo "   To kill: lsof -ti:8001 | xargs kill"
    exit 1
fi

# Check Python dependencies
echo "📦 Checking dependencies..."
python -c "import fastapi, langchain, mcp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install fastapi uvicorn langchain langchain-community ollama structlog mcp
fi

# Check if Ollama is running
echo "🤖 Checking Ollama..."
if ! curl -s http://localhost:11434/api/tags >/dev/null; then
    echo "❌ Ollama not running. Start with: ollama serve"
    exit 1
fi

# Check if gptFREE model is available
if ! ollama list | grep -q "gptFREE\|gpt-oss:20b"; then
    echo "❌ gptFREE model not found"
    echo "   Run: ollama pull gpt-oss:20b && ollama tag gpt-oss:20b gptFREE"
    exit 1
fi

# Start the agent service
echo "✅ Starting agent service on port 8001..."
echo "   API Documentation: http://localhost:8001/docs"
echo "   Health Check: http://localhost:8001/health"
echo ""
echo "💡 MCP Integration:"
echo "   1. Add MCP config to Claude Code (see MCP_SETUP.md)"
echo "   2. Restart Claude Code"
echo "   3. Use agent tools directly in Claude Code!"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

python main.py
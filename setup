#!/bin/bash
# Setup script for Federal Job Advisory Agent System

echo "🚀 Setting up Federal Job Advisory Agent System"
echo "=============================================="

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo "✅ Python $python_version is installed (meets requirement)"
else
    echo "❌ Python $python_version is too old. Need Python 3.10+"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
    echo "   ⚠️  Please edit .env with your configuration"
fi

# Check Ollama
echo "🤖 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Check if gptFREE model exists
    if ollama list | grep -q "gptFREE"; then
        echo "✅ gptFREE model is available"
    else
        echo "⚠️  gptFREE model not found"
        echo "   Trying to create from gpt-oss:20b..."
        
        if ollama list | grep -q "gpt-oss:20b"; then
            ollama tag gpt-oss:20b gptFREE
            echo "✅ Created gptFREE alias"
        else
            echo "❌ gpt-oss:20b not found. Please run: ollama pull gpt-oss:20b"
        fi
    fi
else
    echo "❌ Ollama not installed"
    echo "   Please install from: https://ollama.ai"
fi

# Check Redis
echo "🔴 Checking Redis..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping 2>/dev/null | grep -q PONG; then
        echo "✅ Redis is running"
    else
        echo "⚠️  Redis installed but not running"
        echo "   Start with: redis-server"
    fi
else
    echo "❌ Redis not installed"
    echo "   Install with: brew install redis (Mac) or apt-get install redis-server (Linux)"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data

# Make scripts executable
echo "🔐 Setting permissions..."
chmod +x test_agents.py
chmod +x setup.sh

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Start Ollama: ollama serve"
echo "3. Start Redis: redis-server"
echo "4. Activate venv: source venv/bin/activate"
echo "5. Start agent system: python main.py"
echo "6. Test the system: python test_agents.py"
echo ""
echo "API will be available at: http://localhost:8001"
echo "Documentation at: http://localhost:8001/docs"
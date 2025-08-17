#!/bin/bash
# 🚀 Local LLM Setup Script for Virtual Development Team
# This script sets up Ollama with specialized models for each agent role

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════╗"
echo "║     🤖 Virtual Development Team - LLM Setup Script     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+"
        exit 1
    fi
    
    # Check for curl
    if ! command -v curl &> /dev/null; then
        print_error "curl is not installed. Please install curl"
        exit 1
    fi
    
    # Check available disk space (need at least 50GB for models)
    available_space=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$available_space" -lt 50 ]; then
        print_warning "Less than 50GB disk space available. Some models may not fit."
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    print_success "System requirements met"
}

# Install Ollama
install_ollama() {
    if command -v ollama &> /dev/null; then
        print_status "Ollama is already installed"
        ollama --version
    else
        print_status "Installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
        
        if [ $? -eq 0 ]; then
            print_success "Ollama installed successfully"
        else
            print_error "Failed to install Ollama"
            exit 1
        fi
    fi
}

# Start Ollama service
start_ollama_service() {
    print_status "Starting Ollama service..."
    
    # Check if Ollama is already running
    if pgrep -x "ollama" > /dev/null; then
        print_status "Ollama service is already running"
    else
        ollama serve > /tmp/ollama.log 2>&1 &
        OLLAMA_PID=$!
        sleep 5
        
        if ps -p $OLLAMA_PID > /dev/null; then
            print_success "Ollama service started (PID: $OLLAMA_PID)"
        else
            print_error "Failed to start Ollama service"
            cat /tmp/ollama.log
            exit 1
        fi
    fi
}

# Download models with progress tracking
download_model() {
    local model=$1
    local description=$2
    
    print_status "Downloading $model - $description"
    
    # Check if model already exists
    if ollama list | grep -q "$model"; then
        print_status "$model is already downloaded"
        return 0
    fi
    
    # Download the model
    if ollama pull "$model"; then
        print_success "$model downloaded successfully"
    else
        print_warning "Failed to download $model, trying alternative..."
        return 1
    fi
}

# Download all required models
download_all_models() {
    echo ""
    echo "📦 Downloading AI Models for Virtual Team"
    echo "==========================================="
    echo ""
    
    # Define models and their purposes
    declare -A models=(
        ["codellama:7b"]="Backend/DevOps Engineering (lighter version)"
        ["mistral:7b"]="Data Science & Analytics"
        ["llama2:7b"]="Frontend & Content Creation"
        ["phi:latest"]="Administrative Tasks"
        ["neural-chat:7b"]="Compliance & Communication"
    )
    
    # Track successful downloads
    successful=0
    total=${#models[@]}
    
    # Download each model
    for model in "${!models[@]}"; do
        if download_model "$model" "${models[$model]}"; then
            ((successful++))
        fi
    done
    
    echo ""
    print_status "Downloaded $successful/$total models successfully"
    
    if [ $successful -eq 0 ]; then
        print_error "No models were downloaded. Please check your internet connection."
        exit 1
    elif [ $successful -lt $total ]; then
        print_warning "Some models failed to download. The system will work with available models."
    else
        print_success "All models downloaded successfully!"
    fi
}

# Setup Python environment
setup_python_env() {
    print_status "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip > /dev/null 2>&1
    
    # Install required packages
    print_status "Installing Python dependencies..."
    
    # Create temporary requirements file for LLM-specific deps
    cat > /tmp/llm_requirements.txt << EOF
langchain==0.1.0
langchain-community==0.0.10
langgraph==0.0.20
ollama==0.1.7
fastapi==0.104.1
uvicorn[standard]==0.24.0
streamlit==1.29.0
plotly==5.18.0
pandas==2.1.4
redis==5.0.1
httpx==0.25.2
pydantic==2.5.3
python-multipart==0.0.6
EOF
    
    pip install -r /tmp/llm_requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Python dependencies installed"
    else
        print_error "Failed to install some Python dependencies"
        exit 1
    fi
}

# Create agent configuration
create_agent_config() {
    print_status "Creating agent configuration..."
    
    cat > agent_config.json << 'EOF'
{
    "models": {
        "backend_engineer": "codellama:7b",
        "frontend_developer": "llama2:7b",
        "data_scientist": "mistral:7b",
        "devops_engineer": "codellama:7b",
        "security_analyst": "mistral:7b",
        "content_creator": "llama2:7b",
        "project_manager": "phi:latest",
        "compliance_officer": "neural-chat:7b",
        "database_admin": "codellama:7b",
        "email_handler": "phi:latest"
    },
    "agent_settings": {
        "temperature": 0.7,
        "max_tokens": 4096,
        "timeout": 30,
        "retry_attempts": 3
    },
    "orchestrator": {
        "max_parallel_tasks": 5,
        "task_timeout": 300,
        "checkpoint_interval": 60
    }
}
EOF
    
    print_success "Agent configuration created"
}

# Test Ollama connection
test_ollama_connection() {
    print_status "Testing Ollama connection..."
    
    # Try to list models
    if ollama list > /dev/null 2>&1; then
        print_success "Ollama connection successful"
        echo ""
        echo "Available models:"
        ollama list
    else
        print_error "Cannot connect to Ollama service"
        exit 1
    fi
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    
    cat > start_agents.sh << 'EOF'
#!/bin/bash
# Start Virtual Development Team

echo "🚀 Starting Virtual Development Team..."

# Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 5
fi

# Activate Python environment
source venv/bin/activate

# Start the agent controller
echo "Starting Agent Controller API..."
python claude_code_controller.py &
CONTROLLER_PID=$!

# Start the monitoring dashboard
echo "Starting Monitoring Dashboard..."
streamlit run app/dashboard/agent_monitor.py &
DASHBOARD_PID=$!

echo ""
echo "✅ Virtual Development Team is running!"
echo "   - Agent API: http://localhost:8002"
echo "   - API Docs: http://localhost:8002/docs"
echo "   - Dashboard: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services..."

# Trap Ctrl+C and cleanup
trap "kill $CONTROLLER_PID $DASHBOARD_PID; exit" INT
wait
EOF
    
    chmod +x start_agents.sh
    print_success "Startup script created: start_agents.sh"
}

# Main execution
main() {
    echo ""
    print_status "Starting Local LLM Setup for Virtual Development Team"
    echo ""
    
    # Run setup steps
    check_requirements
    install_ollama
    start_ollama_service
    download_all_models
    setup_python_env
    create_agent_config
    test_ollama_connection
    create_startup_script
    
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║           ✅ Setup Complete Successfully!              ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Run './start_agents.sh' to start the virtual team"
    echo "   2. Access the API at http://localhost:8002/docs"
    echo "   3. View the dashboard at http://localhost:8501"
    echo ""
    echo "💡 Quick Test:"
    echo "   curl http://localhost:8002/agents"
    echo ""
    print_success "Your Virtual Development Team is ready!"
}

# Run main function
main
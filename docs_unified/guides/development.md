# Development Guide

## 🏗️ Project Structure (2024 MCP Standards)

```
Fed-Job-Advisor-MCP-Agents/
├── src/                          # Source code (standardized)
│   ├── core/                     # Core MCP server functionality
│   ├── agents/                   # Federal job application agents
│   ├── mcp_services/            # External service specialists
│   └── tests/                   # Test suite
├── config/                      # Configuration files
├── scripts/                     # Utility and scraping scripts
├── tools/                       # Development tools
├── docs_unified/               # Unified documentation
├── archives/                   # Archived old structures
└── main.py                     # Entry point
```

### Key Files
- **`main.py`**: Agent system entry point (FastAPI server)
- **`mcp_server.py`**: MCP server entry point (Claude Code integration)
- **`src/core/main.py`**: Core agent system implementation
- **`src/core/mcp_server.py`**: Core MCP server implementation
- **`config/mcp_server.json`**: MCP server configuration

## 🚀 Quick Start Development

### 1. Setup Environment
```bash
cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Services
```bash
# Start Ollama
ollama serve

# Start Redis  
redis-server

# Verify model
ollama run gptFREE "Hello"
```

### 3. Development Workflow
```bash
# Start agent system (for direct API development)
python main.py

# OR start MCP server (for Claude Code integration)
python mcp_server.py

# Run tests
python -m pytest src/tests/

# Health check
curl http://localhost:8001/health
```

## 🤖 Adding New Agents

### 1. Create Agent Class
Create new agent in `src/agents/app/agents/roles/` or `src/agents/app/agents/compliance/`:

```python
from src.agents.app.agents.base import FederalJobAgent

class NewRoleAgent(FederalJobAgent):
    def __init__(self):
        super().__init__(role="new_role")
    
    def _load_tools(self):
        return [
            # Agent-specific tools
        ]
    
    def _get_prompt_template(self):
        return """
        Your specialized prompt for this agent...
        """
    
    async def analyze(self, data):
        # Implementation logic
        return {
            "recommendations": {...},
            "score": "...",
            "analysis": "..."
        }
```

### 2. Register in MCP Server
Add to `src/core/mcp_server.py`:

```python
"analyze_new_role_profile": {
    "description": "Analyze candidate profile for new role positions...",
    "agent_role": "new_role",
    "endpoint": "analyze",
    "schema": {
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "skills": {"type": "array"},
            # ... other properties
        },
        "required": ["user_id"]
    }
}
```

### 3. Register in Agent System
Add to `src/core/main.py` agent factory:

```python
"new_role": NewRoleAgent,
```

## 🔧 External Service Integration

### Adding New Service Specialists

1. **Create Service Class** in `src/mcp_services/category/`:
```python
from src.mcp_services.base import ServiceSpecialistBase

class NewServiceSpecialist(ServiceSpecialistBase):
    def __init__(self):
        super().__init__("service_name")
    
    def _load_knowledge_base(self):
        # Load service-specific documentation
        pass
    
    async def analyze_request(self, request_data):
        # Service-specific analysis
        pass
```

2. **Add Documentation** in `docs/external_services/`:
```
service_name/
├── manifest.json
├── best_practices/
├── examples/
├── fed_job_advisor/
└── official/
```

3. **Register in Config** `config/mcp_server_config.json`:
```json
"new_service_specialist": {
    "module": "src.mcp_services.category.new_service_specialist",
    "class": "NewServiceSpecialist",
    "description": "New service integration expert",
    "specialization": "Service Category",
    "documentation_path": "docs/external_services/service_name"
}
```

## 🧪 Testing

### Test Structure
```
src/tests/
├── test_agents/              # Agent functionality tests
├── test_mcp_server/         # MCP server tests
├── test_services/           # Service specialist tests
└── test_integration/        # Integration tests
```

### Running Tests
```bash
# All tests
python -m pytest src/tests/

# Specific category
python -m pytest src/tests/test_agents/

# With coverage
python -m pytest src/tests/ --cov=src/

# Specific test
python -m pytest src/tests/test_agents/test_data_scientist.py
```

### Test Examples
```python
# Agent test
async def test_data_scientist_agent():
    agent = DataScientistAgent()
    result = await agent.analyze({
        "skills": ["Python", "ML"],
        "experience": "5 years...",
        "target_grade": "GS-13"
    })
    assert result["score"] is not None
    assert "recommendations" in result

# MCP server test
async def test_mcp_tool_call():
    server = FedJobAdvisorMCP()
    result = await server._call_agent("analyze_data_scientist_profile", {
        "user_id": "test_user",
        "skills": ["Python"],
        "experience": "Test experience"
    })
    assert len(result) > 0
```

## 📊 Performance Optimization

### Local LLM Optimization
- **Model**: gptFree (20B parameter local model)
- **Temperature**: 0.3 for consistent responses
- **Context**: Optimized prompts for federal job domain
- **Memory**: Redis with TTL for conversation memory

### Scaling Considerations
- **Concurrent Users**: 50+ supported with current architecture
- **Response Time**: Target <2 seconds for all agent responses
- **Memory Usage**: ~2GB per active agent session
- **Cost**: ~$0.24 per session vs $2.40 cloud LLMs

## 🔧 Configuration

### Environment Variables
```bash
OLLAMA_MODEL=gptFREE
OLLAMA_TEMPERATURE=0.3
REDIS_URL=redis://localhost:6379
API_PORT=8001
ENABLE_MERIT_COMPLIANCE=true
```

### MCP Configuration
Edit `config/mcp_server.json` for:
- Server metadata
- Agent endpoints
- Service specialists
- Logging configuration

## 🐛 Debugging

### Common Issues

1. **Ollama Connection**:
```bash
ps aux | grep ollama
ollama serve
ollama run gptFREE "test"
```

2. **Redis Connection**:
```bash
redis-cli ping
redis-server
```

3. **MCP Server Issues**:
```bash
# Check MCP server startup
python mcp_server.py

# Test health endpoint
curl http://localhost:8001/health
```

### Logging
- **Agent System**: Structured JSON logs to stdout
- **MCP Server**: INFO level logging with timestamps
- **Debug Mode**: Set log level to DEBUG in config

## 📚 Additional Resources

- **Fed Job Advisor Main Project**: `../fedJobAdvisor/`
- **MCP Protocol Documentation**: Official MCP specifications
- **LangChain Documentation**: For agent framework understanding
- **Ollama Documentation**: For local LLM management

---

**Ready for federal career intelligence development at scale**
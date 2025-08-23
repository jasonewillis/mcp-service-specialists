# OpenCode + Ollama Implementation Prompt for General-Purpose Agent

**Task**: Implement OpenCode + Ollama integration with existing MLX-accelerated MCP Fed Job Advisor system  
**Target**: Complete local LLM alternative to Claude API while preserving specialized agent expertise  
**Platform**: macOS Apple Silicon (M2 Max, 64GB RAM)  

---

## 🎯 Implementation Overview

You are tasked with implementing a comprehensive OpenCode + Ollama integration that provides a local LLM alternative to our current Claude API setup. This implementation should create a hybrid architecture where users can choose between fast cloud inference (Claude Code) and private local inference (OpenCode), both leveraging the same specialized Fed Job Advisor MCP agents.

### Existing Infrastructure (DO NOT MODIFY)
✅ **MLX-Accelerated MCP Server**: Running on port 8006 with 10 specialized Fed Job Advisor agents  
✅ **Apple Silicon GPU Optimization**: 3x performance improvement confirmed  
✅ **Agent Specializations**: resume_compression, essay_compliance, data_scientist, statistician, database_admin, devops_engineer, it_specialist, executive_orders, job_market, orchestrate_job_collection  

### Target Architecture
```
User Choice Layer:
┌─────────────────┐    ┌─────────────────┐
│   Claude Code   │    │    OpenCode     │
│   (Primary)     │    │   (Secondary)   │
│   Fast/Cloud    │    │   Private/Local │
└─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
Integration Layer:
┌─────────────────────────────────────────┐
│         MCP Bridge (Port 8007)          │
│        Smart Agent Routing              │
└─────────────────────────────────────────┘
         │
         ▼
Existing Infrastructure (PRESERVE):
┌─────────────────────────────────────────┐
│    MLX-Accelerated Fed Job Advisors    │
│         (Port 8006 - RUNNING)          │
└─────────────────────────────────────────┘
```

---

## 📋 Implementation Requirements

### Phase 1: Core Installation (Priority: High)

#### 1.1 Install Ollama with Apple Silicon Optimization
```bash
# Install Ollama
brew install ollama

# Start service
brew services start ollama

# Download function-calling capable models
ollama pull qwen2.5:7b          # Primary: Function calling support
ollama pull deepseek-coder:6.7b # Secondary: Code generation
ollama pull codestral:7b        # Alternative: Code completion

# Verify installation
curl http://localhost:11434/api/version
```

#### 1.2 Install Multiple OpenCode Implementations
Install all three OpenCode variants for comparison and flexibility:

**Python Implementation** (Recommended for integration):
```bash
cd ~/Developer
git clone https://github.com/xichen1997/opencode.git
cd opencode
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Go Implementation** (Best terminal UI):
```bash
brew install opencode-ai/tap/opencode
```

**npm Implementation** (LSP features):
```bash
npm install -g opencode
```

#### 1.3 Verify Existing MLX System
Ensure the MLX-accelerated MCP server remains operational:
```bash
curl http://localhost:8006/health
# Expected: {"status":"healthy","agents_available":10,"mlx_status":"healthy"}
```

### Phase 2: MCP Bridge Development (Priority: High)

#### 2.1 Create Fed Job Advisor MCP Proxy
Develop a custom proxy service that bridges OpenCode/Ollama with the existing MLX agents:

**File**: `~/Developer/fed_job_mcp_proxy.py`

**Requirements**:
- **Port**: 8007 (avoid conflicts with existing services)
- **Protocol**: HTTP REST API compatible with MCP
- **Smart Routing**: Automatically route tasks to appropriate agents based on content
- **Error Handling**: Graceful fallback and error reporting
- **Performance Monitoring**: Track response times and success rates

**Key Functions**:
```python
class FedJobMCPProxy:
    async def health_check(self, request):
        # Check both Ollama and MLX agents health
        
    async def list_agents(self, request):
        # Return available Fed Job Advisor agents
        
    async def agent_analyze(self, request):
        # Forward request to specific agent
        
    async def analyze_request(self, request):
        # Smart routing based on task content
        
    def route_task_to_agent(self, task):
        # Intelligence routing logic:
        # "resume" → resume_compression
        # "essay"/"STAR" → essay_compliance  
        # "data"/"statistics" → data_scientist
        # "market"/"salary" → job_market
        # etc.
```

#### 2.2 Configure MCP Bridge for Fed Job Advisor Integration
Create configuration that connects to existing MLX agents:
```json
{
  "ollama": {
    "baseUrl": "http://localhost:11434",
    "defaultModel": "qwen2.5:7b"
  },
  "mcp": {
    "servers": [{
      "name": "fed_job_advisor",
      "url": "http://localhost:8006",
      "agents": [
        "resume_compression", "essay_compliance", "data_scientist",
        "statistician", "database_admin", "devops_engineer", 
        "it_specialist", "executive_orders", "job_market",
        "orchestrate_job_collection"
      ]
    }]
  },
  "bridge": {"port": 8007}
}
```

### Phase 3: OpenCode Configuration (Priority: Medium)

#### 3.1 Configure Each OpenCode Implementation

**Python OpenCode**: Create `config.yaml`
```yaml
model:
  provider: "ollama"
  base_url: "http://localhost:11434"
  model_name: "qwen2.5:7b"
  temperature: 0.1

mcp:
  enabled: true
  proxy_url: "http://localhost:8007"
  agents:
    - name: "fed_job_advisor"
      url: "http://localhost:8006"
```

**Go OpenCode**: Configure via CLI
```bash
opencode config set provider ollama
opencode config set ollama.base_url http://localhost:11434
opencode config set ollama.model qwen2.5:7b
```

#### 3.2 Create System Management Scripts

**Startup Script**: `~/Developer/start_opencode_system.sh`
- Check MLX agents (should already be running)
- Start Ollama if needed
- Start MCP proxy on port 8007
- Verify all services healthy
- Display usage instructions

**Shutdown Script**: `~/Developer/stop_opencode_system.sh`
- Stop MCP proxy
- Optionally stop Ollama
- Clean up PID files

### Phase 4: Integration Testing (Priority: High)

#### 4.1 Functionality Tests
Create comprehensive test suite that validates:
- **Ollama Model Inference**: Direct model calls work
- **MCP Proxy Routing**: Smart routing to correct agents
- **Agent Functionality**: All 10 agents respond correctly
- **Performance Benchmarking**: Response time comparisons
- **Error Handling**: Graceful failure modes

**Test Script**: `~/Developer/test_opencode_integration.sh`
```bash
# Test 1: Direct Ollama
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "qwen2.5:7b", "prompt": "Test"}'

# Test 2: MCP Proxy Health  
curl http://localhost:8007/health

# Test 3: Agent Routing
curl -X POST http://localhost:8007/analyze \
  -d '{"task": "Optimize my federal resume"}'

# Test 4: Performance Benchmark
# Run 10 queries, measure response times
```

#### 4.2 Performance Validation
Compare performance between:
- **Claude Code + Claude API**: Current baseline (~0.5 seconds)
- **OpenCode + Ollama Local**: New local option (~3-8 seconds)
- **Cost Analysis**: $0.24/session → $0.00

Document trade-offs:
- **Speed**: 6-16x slower for local inference
- **Cost**: 100% savings on API fees
- **Privacy**: Complete local processing
- **Offline**: Works without internet

### Phase 5: Documentation & Automation (Priority: Medium)

#### 5.1 User Documentation
Create comprehensive user guides:
- **Quick Start**: How to use OpenCode for federal hiring tasks
- **Usage Examples**: Specific queries for each agent type
- **Performance Expectations**: Response time and quality expectations
- **Troubleshooting**: Common issues and solutions

#### 5.2 Monitoring & Maintenance
Implement ongoing system health monitoring:
- **Health Monitoring**: Automated service health checks
- **Performance Tracking**: Response time and success rate logging
- **Model Management**: Automated model updates and cleanup
- **Resource Monitoring**: Memory and disk usage tracking

---

## 🔧 Technical Implementation Details

### Port Management (CRITICAL)
- **8006**: MLX MCP Agents (EXISTING - DO NOT CHANGE)
- **8007**: Fed Job MCP Proxy (NEW - TO BE CREATED)
- **11434**: Ollama API (STANDARD)

### Model Selection Rationale
- **qwen2.5:7b**: Function calling support essential for MCP integration
- **deepseek-coder:6.7b**: Enhanced code analysis for technical roles
- **codestral:7b**: Alternative with strong completion capabilities

### Smart Routing Logic
Implement intelligent task routing based on content analysis:
```python
routing_rules = {
    'resume': 'resume_compression',
    'essay': 'essay_compliance', 
    'data': 'data_scientist',
    'market': 'job_market',
    'database': 'database_admin',
    'policy': 'executive_orders'
}
```

### Error Handling Strategy
- **Graceful Degradation**: Fall back to general agents if specific ones fail
- **Timeout Management**: 30-second timeouts for local inference
- **Health Checks**: Continuous monitoring of all services
- **User Feedback**: Clear error messages and suggested actions

---

## 📊 Success Criteria

### Technical Metrics
✅ **System Integration**: All components communicate successfully  
✅ **Agent Preservation**: All 10 Fed Job Advisor agents remain functional  
✅ **Response Time**: Local inference completes within 10 seconds  
✅ **Success Rate**: >95% successful task completion  
✅ **Resource Usage**: System stable under normal load  

### User Experience Metrics
✅ **Easy Switching**: Users can choose Claude Code or OpenCode seamlessly  
✅ **Maintained Quality**: Comparable federal hiring advice quality  
✅ **Clear Documentation**: Users understand when to use each option  
✅ **Reliable Operation**: System starts/stops reliably  

### Business Metrics
✅ **Cost Reduction**: $0 operational cost path established  
✅ **Privacy Enhancement**: 100% local processing capability  
✅ **Offline Operation**: Works without internet connectivity  
✅ **Competitive Advantage**: Unique local federal hiring AI capability  

---

## ⚠️ Implementation Constraints

### DO NOT MODIFY
- **MLX MCP Server**: Keep existing port 8006 configuration
- **Agent Specializations**: Preserve all 10 Fed Job Advisor agents
- **MLX Acceleration**: Maintain Apple Silicon GPU optimization
- **API Endpoints**: Keep existing agent API structure

### REQUIRED PRESERVATIONS
- **Current Functionality**: Everything that works now must continue working
- **Performance**: MLX acceleration benefits must be maintained
- **Agent Expertise**: Federal hiring specializations must be preserved
- **API Compatibility**: Existing integrations must not break

### OPTIONAL ENHANCEMENTS
- **Model Optimization**: Fine-tuning for federal hiring domain
- **Caching**: Response caching for improved performance
- **UI Improvements**: Better user interfaces for model selection
- **Advanced Routing**: Machine learning-based task routing

---

## 🚀 Deliverables

### Primary Deliverables (Required)
1. **Fed Job MCP Proxy**: Custom bridge service connecting OpenCode to MLX agents
2. **System Management Scripts**: Automated startup/shutdown/monitoring
3. **Configuration Files**: Optimized configs for all OpenCode implementations
4. **Test Suite**: Comprehensive functionality and performance validation
5. **User Documentation**: Complete usage guide and troubleshooting

### Secondary Deliverables (Nice to Have)
1. **Performance Benchmarking**: Detailed analysis of local vs cloud performance
2. **Model Comparison**: Evaluation of different Ollama models for federal tasks
3. **Cost Analysis**: Documentation of savings from local inference
4. **Future Roadmap**: Plan for advanced features and optimizations

### Documentation Deliverables
1. **Installation Guide**: Step-by-step setup instructions (COMPLETED)
2. **User Guide**: How to use the integrated system effectively
3. **API Reference**: Documentation of proxy endpoints and routing
4. **Troubleshooting Guide**: Common issues and resolution procedures

---

## 🎯 Implementation Approach

### Development Methodology
1. **Incremental Development**: Build and test each component separately
2. **Preserve Existing**: Never modify working MLX MCP system
3. **Test Continuously**: Validate each step before proceeding
4. **Document Everything**: Clear documentation for maintenance

### Quality Assurance
- **Unit Tests**: Test each component individually
- **Integration Tests**: Validate end-to-end functionality
- **Performance Tests**: Benchmark against current system
- **User Acceptance**: Verify usability for federal hiring tasks

### Risk Mitigation
- **Backup Strategy**: Keep current system operational throughout
- **Rollback Plan**: Ability to disable new system without impact
- **Monitoring**: Continuous health checks during implementation
- **Gradual Rollout**: Test with subset of functionality first

---

## 📞 Support Information

### Existing System Status
- **MLX MCP Server**: http://localhost:8006 (healthy, 10 agents active)
- **Apple Silicon GPU**: Confirmed operational with 3x performance boost
- **Fed Job Advisor Agents**: All 10 specialized agents functional

### Implementation Context
- **Hardware**: Apple M2 Max, 64GB unified memory
- **Current Performance**: 0.00-0.06 seconds per agent task
- **Target Integration**: Hybrid cloud/local with preserved expertise

### Success Definition
**A working OpenCode + Ollama integration that provides a $0-cost, 100% private alternative to Claude API while preserving all existing Fed Job Advisor agent functionality and expertise.**

---

**🎯 Your mission is to create a seamless hybrid AI system where users can choose between fast cloud inference (Claude Code) and private local inference (OpenCode), both leveraging the same specialized federal hiring expertise.**

**Key Success Metric**: Users should be able to get the same quality federal hiring advice locally (OpenCode + Ollama) as they do from the cloud (Claude Code + Claude API), with the trade-off being slower response time in exchange for zero cost and complete privacy.**
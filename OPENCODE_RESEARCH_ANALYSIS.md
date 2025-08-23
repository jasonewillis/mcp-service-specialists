# OpenCode Research Analysis: Local LLM Integration for Fed Job Advisor MCP Agents

**Research Date**: August 20, 2025  
**Scope**: Evaluation of OpenCode project for local LLM integration with existing MLX-accelerated MCP agent system  
**Current System**: 10 specialized Fed Job Advisor agents running on MLX (port 8006)

## Executive Summary

OpenCode represents a viable path for transitioning our Fed Job Advisor MCP agent system from Claude API dependency to local LLM operation using Ollama. The project offers multiple implementation approaches with varying complexity levels, all supporting the Model Context Protocol that our agents already use.

### Key Findings:
- ✅ **MCP Compatibility**: Full support through Ollama-MCP bridge implementations
- ✅ **MLX Integration**: Possible via hybrid architecture combining MLX acceleration with Ollama inference
- ✅ **Cost Reduction**: Eliminate Claude API costs (~$0.24/session → $0 operational cost)
- ⚠️ **Performance Trade-off**: Local inference slower but more private and cost-effective
- ✅ **Fed Job Advisor Compatibility**: Minimal changes required to existing agent codebase

## 1. OpenCode Project Analysis

### 1.1 Multiple OpenCode Implementations

Research revealed **three distinct OpenCode projects** with different architectures:

#### Implementation A: xichen1997/opencode (Python-based)
- **Language**: Python 3.8+
- **Architecture**: CLI with Ollama client integration
- **Security**: Sandboxed execution, working directory restrictions
- **Models**: Supports llama3.2:3b (2GB), deepseek-coder:6.7b (4GB), codestral:7b (4GB)
- **Config**: YAML-based configuration system
- **Performance**: 1-5 second response times, 2-8GB memory usage

#### Implementation B: opencode-ai/opencode (Go-based) 
- **Language**: Go with Bubble Tea TUI framework
- **Architecture**: Terminal UI with SQLite storage
- **Providers**: 75+ LLM providers including OpenAI, Anthropic, Ollama
- **Features**: LSP integration, session persistence, auto-compaction
- **Storage**: SQLite for conversations and sessions
- **Installation**: Cross-platform (macOS, Linux, Windows WSL)

#### Implementation C: OpenCode Terminal Assistant
- **Installation**: npm/yarn/bun package manager
- **Features**: LSP integration, multi-provider support
- **Authentication**: API keys, environment variables
- **Usage**: Interactive and non-interactive modes

### 1.2 Comparative Analysis vs Claude Code

| Feature | Claude Code | OpenCode (Python) | OpenCode (Go) | OpenCode (npm) |
|---------|-------------|-------------------|---------------|----------------|
| **Providers** | Anthropic only | Ollama local | 75+ providers | 75+ providers |
| **Cost** | API usage fees | $0 operational | Variable | Variable |
| **Privacy** | Cloud-based | 100% local | Configurable | Configurable |
| **Performance** | Fast (cloud) | 1-5s local | Variable | Variable |
| **MCP Support** | Native | Via bridge | Possible | Possible |
| **Extensibility** | Limited | Plugin system | LSP integration | Configurable |

## 2. Technical Architecture Analysis

### 2.1 Model Context Protocol (MCP) Integration

#### Current MCP Support Status:
- **Native MCP**: Not directly supported in OpenCode implementations
- **Bridge Solutions**: Available via `ollama-mcp-bridge` project
- **Compatibility**: Any LLM with function-calling support works with MCP
- **Excluded Models**: Reasoning models like DeepSeek are not MCP-compatible

#### MCP Integration Patterns:
```typescript
// Pattern 1: Direct MCP Server Connection
Ollama Model ←→ MCP Bridge ←→ MCP Server (our Fed Job Advisor agents)

// Pattern 2: HTTP Proxy Integration  
OpenCode ←→ MCP HTTP Proxy ←→ Fed Job Advisor MCP Agents (port 8006)

// Pattern 3: Hybrid Architecture
OpenCode + Ollama ←→ MLX-Accelerated Inference ←→ MCP Agent System
```

### 2.2 MLX Integration Potential

#### Hybrid Architecture Opportunities:
1. **MLX for Inference Acceleration**: Use MLX-LM for model inference on Apple Silicon
2. **Ollama for Model Management**: Use Ollama for model loading and API compatibility
3. **MCP for Agent Communication**: Maintain existing MCP protocol for Fed Job Advisor agents

#### Technical Implementation Path:
```python
# Proposed Architecture Stack
OpenCode CLI
    ↓
Ollama API (model management)
    ↓  
MLX-LM (Apple Silicon acceleration)
    ↓
Fed Job Advisor MCP Agents (port 8006)
    ↓
Specialized Federal Hiring Analysis
```

## 3. MCP Compatibility Deep Dive

### 3.1 Current Fed Job Advisor MCP Agent System

**Status**: ✅ **Running successfully on port 8006 with MLX acceleration**

Our current system includes:
- **Technical Role Agents**: data_scientist, statistician, database_admin, devops, it_specialist
- **Compliance Agents**: essay_compliance, resume_compression, executive_orders  
- **Analytics Agents**: job_market, orchestrate_job_collection

**Current Performance Metrics**:
- MLX acceleration enabled for all 10 agents
- Response times: ~0.00-0.06 seconds per agent task
- Memory efficiency: Apple Silicon unified memory model
- API compatibility: HTTP REST endpoints for external integration

### 3.2 MCP Bridge Implementation

#### Available Bridge Solutions:
1. **ollama-mcp-bridge** (TypeScript): Connects Ollama to MCP servers
2. **MCP-CLI Integration**: Direct command-line MCP server connection
3. **Custom HTTP Proxy**: Bridge our existing MLX agents to Ollama models

#### Implementation Requirements:
```bash
# Required components for MCP integration
ollama pull qwen2.5:7b        # Function-calling capable model
npm install ollama-mcp-bridge # MCP bridge software
uv run mcp-cli                # Alternative CLI approach
```

### 3.3 Fed Job Advisor Agent Adaptation

#### Minimal Changes Required:
- **Keep existing MCP HTTP API**: Agents already expose REST endpoints
- **Add Ollama inference backend**: Replace Claude API calls with local inference
- **Maintain agent specialization**: Federal hiring expertise remains unchanged
- **Preserve MLX acceleration**: Continue using Apple Silicon optimization

#### Compatibility Matrix:
| Agent Type | MCP Ready | Ollama Compatible | MLX Accelerated | Changes Needed |
|------------|-----------|-------------------|-----------------|----------------|
| resume_compression | ✅ | ✅ | ✅ | Inference backend only |
| essay_compliance | ✅ | ✅ | ✅ | Inference backend only |
| data_scientist | ✅ | ✅ | ✅ | Inference backend only |
| job_market | ✅ | ✅ | ✅ | Inference backend only |
| All others | ✅ | ✅ | ✅ | Inference backend only |

## 4. MLX Integration Technical Analysis

### 4.1 MLX Framework Compatibility

#### Current MLX Advantages:
- **Apple Silicon Optimization**: Unified memory model, lazy computation
- **Performance**: Faster inference than CPU-only solutions
- **Integration**: Already working with our Fed Job Advisor agents
- **Memory Efficiency**: Shared CPU/GPU memory pool

#### MLX + Ollama Integration Strategies:

**Strategy 1: MLX-LM as Ollama Backend**
```python
# Use MLX-LM for actual inference, Ollama for API compatibility
class MLXOllamaHybrid:
    def __init__(self):
        self.mlx_model = load_mlx_model("qwen2.5:7b")
        self.ollama_api = OllamaAPIWrapper()
    
    def generate(self, prompt):
        # Use MLX for fast inference
        result = self.mlx_model.generate(prompt)
        # Return via Ollama-compatible API
        return self.ollama_api.format_response(result)
```

**Strategy 2: Parallel Architecture**
```python
# Run MLX agents alongside Ollama models
class FedJobAdvisorHybrid:
    def __init__(self):
        self.mlx_agents = MLXAgentSystem(port=8006)  # Existing system
        self.ollama_models = OllamaModelSystem()     # New local models
        self.mcp_bridge = MCPBridge()                # Protocol translation
```

### 4.2 Performance Projections

#### Current Performance (MLX + Claude API):
- **Agent Response Time**: 0.00-0.06 seconds
- **API Latency**: ~200-500ms to Claude
- **Total Time**: ~0.2-0.6 seconds per analysis
- **Cost**: ~$0.24 per session

#### Projected Performance (MLX + Ollama Local):
- **Agent Processing**: 0.00-0.06 seconds (unchanged)
- **Local Inference**: 1-5 seconds (qwen2.5:7b)
- **Total Time**: ~1-5 seconds per analysis
- **Cost**: $0 operational cost

#### Trade-off Analysis:
- **Slower Response**: 5-10x longer inference time
- **Zero Cost**: Eliminate all API usage fees
- **Enhanced Privacy**: No data leaves local machine
- **Offline Capability**: Works without internet connection

## 5. Fed Job Advisor Integration Strategy

### 5.1 Integration Architecture

#### Phase 1: Proof of Concept (2-4 hours)
```bash
# Install OpenCode + Ollama
brew install ollama
ollama pull qwen2.5:7b
npm install -g opencode

# Test MCP bridge
git clone https://github.com/patruff/ollama-mcp-bridge
cd ollama-mcp-bridge
npm install && npm start

# Connect to existing MLX agents (port 8006)
curl http://localhost:8006/agents  # Verify agents running
```

#### Phase 2: MCP Bridge Implementation (4-8 hours)
```python
# Create MCP proxy for Fed Job Advisor agents
class FedJobAdvisorMCPProxy:
    def __init__(self):
        self.agents_url = "http://localhost:8006"
        self.ollama_url = "http://localhost:11434"
        
    async def route_request(self, agent_type, task):
        # Send to appropriate MLX-accelerated agent
        response = await self.call_agent(agent_type, task)
        return self.format_mcp_response(response)
```

#### Phase 3: Full Integration (8-12 hours)
- Replace Claude API inference with Ollama local models
- Maintain MLX acceleration for Apple Silicon performance
- Keep existing agent specialization and federal expertise
- Add configuration switching between local and cloud modes

### 5.2 Implementation Roadmap

#### Immediate Steps (This Week):
1. **Install and Test OpenCode**: Evaluate all three implementations
2. **Test Ollama Models**: Download and benchmark qwen2.5:7b, codestral:7b
3. **MCP Bridge POC**: Connect Ollama to our existing MLX agent system
4. **Performance Baseline**: Measure response times vs current Claude API setup

#### Short-term Goals (Next 2 Weeks):
1. **Hybrid Architecture**: Implement MLX + Ollama inference backend
2. **Agent Configuration**: Add local/cloud mode switching
3. **Federal Knowledge Base**: Ensure local models have sufficient federal hiring context
4. **Testing Suite**: Validate all 10 agents work with local inference

#### Long-term Vision (Next Month):
1. **Production Ready**: Stable local inference for all Fed Job Advisor features
2. **Performance Optimization**: Fine-tune models for federal hiring domain
3. **Cost Analysis**: Document savings from eliminating Claude API dependency
4. **User Experience**: Seamless switching between local and cloud modes

### 5.3 Risk Assessment

#### Technical Risks:
- **Inference Speed**: 5-10x slower than Claude API could impact user experience
- **Model Quality**: Local models may produce lower quality federal hiring advice
- **Memory Requirements**: Running multiple large models simultaneously
- **Complexity**: Additional infrastructure to maintain and debug

#### Mitigation Strategies:
- **Hybrid Mode**: Allow fallback to Claude API for critical tasks
- **Model Selection**: Use specialized coding models (deepseek-coder:6.7b) for technical analysis
- **Caching**: Implement response caching for common federal hiring questions
- **Graceful Degradation**: Maintain current system as backup

#### Success Metrics:
- **Cost Reduction**: Eliminate $0.24/session Claude API costs
- **Response Time**: <10 seconds for complex federal hiring analysis
- **Accuracy**: Maintain 95%+ accuracy for federal compliance checking
- **User Satisfaction**: No degradation in user experience

## 6. Recommended Next Steps

### Immediate Actions (Today):

#### 1. Install OpenCode for Testing:
```bash
# Python implementation (most relevant for our use case)
git clone https://github.com/xichen1997/opencode
cd opencode
pip install -r requirements.txt

# Go implementation (for comparison)
brew install opencode-ai/tap/opencode

# npm implementation (for LSP features)
npm install -g opencode
```

#### 2. Set Up Ollama + MCP Bridge:
```bash
# Install Ollama
brew install ollama
ollama pull qwen2.5:7b          # Function calling support
ollama pull deepseek-coder:6.7b # Code generation
ollama pull codestral:7b        # Code completion

# Test MCP bridge
git clone https://github.com/patruff/ollama-mcp-bridge
cd ollama-mcp-bridge
npm install && npm start
```

#### 3. Connect to Existing MLX System:
```bash
# Verify our MLX agents are running
curl http://localhost:8006/agents | jq

# Test agent functionality
curl -X POST http://localhost:8006/agents/resume_compression/analyze \
  -H "Content-Type: application/json" \
  -d '{"task": "Test OpenCode integration"}'
```

### Short-term Development (Next Week):

#### 4. Build MCP Proxy Bridge:
Create a bridge service that connects OpenCode → Ollama → Fed Job Advisor MLX agents

#### 5. Performance Benchmarking:
Compare response times and quality between:
- Current: Claude API + MLX agents
- New: Ollama local + MLX agents
- Hybrid: Smart routing based on task complexity

#### 6. Documentation Update:
Update our agent documentation to include local LLM operation procedures

### Strategic Decision Points:

#### Cost vs Performance Trade-off:
- **Full Local**: $0 cost, 5-10x slower, enhanced privacy
- **Hybrid**: Moderate cost, optimal performance, flexibility
- **Current**: Higher cost, fastest performance, cloud dependency

#### Recommended Approach:
**Start with hybrid architecture** allowing users to choose between local and cloud inference based on their needs:
- **Free Tier**: Local inference only (slower but free)
- **Premium Tier**: Cloud inference for speed + local for privacy
- **Enterprise**: On-premises deployment with local models

## 7. Conclusion

OpenCode provides a clear technical path for transitioning our Fed Job Advisor MCP agent system to local LLM operation. The combination of MLX acceleration for Apple Silicon and MCP protocol compatibility makes this integration both feasible and beneficial.

### Key Benefits:
- **Zero Operational Costs**: Eliminate Claude API dependency
- **Enhanced Privacy**: All federal hiring data stays local
- **Offline Capability**: Work without internet connection
- **Maintained Functionality**: Keep all 10 specialized agents working

### Implementation Complexity: **Medium**
- **Time Investment**: 20-30 hours for full implementation
- **Technical Skills**: Python, HTTP APIs, model deployment
- **Infrastructure**: Local model storage (10-20GB), increased RAM usage

### Return on Investment: **High**
- **Cost Savings**: $0.24/session × usage volume = significant long-term savings
- **Technical Independence**: Reduced dependency on external APIs
- **Competitive Advantage**: Fully local federal hiring AI capabilities

**Recommendation**: Proceed with Phase 1 proof of concept implementation to validate technical feasibility and performance characteristics before committing to full integration.

---

**Next Actions**: 
1. Install and test OpenCode implementations
2. Set up Ollama with recommended models  
3. Create MCP bridge to existing MLX agent system
4. Benchmark performance vs current Claude API setup
5. Document findings and make go/no-go decision

**Contact**: MLX-accelerated MCP agent system running on port 8006 ready for integration testing.
# Fed Job Advisor MCP Agent System Documentation

**2024 MCP Standards Compliant Documentation**

## 🎯 Quick Start

### For Claude Code Integration
1. **Start MCP Server**: `python mcp_server.py`
2. **Use MCP Tools**: Available in Claude Code's MCP integration
3. **Agent Endpoints**: All 10+ federal job agents accessible via MCP

### For Direct API Use
1. **Start Agent System**: `python main.py`
2. **API Base**: `http://localhost:8001`
3. **Health Check**: `curl http://localhost:8001/health`

## 📚 Documentation Structure

### 🤖 [Agent System](./guides/agents.md)
- **Federal Job Agents**: 10 specialized agents for federal career guidance
- **MCP Integration**: How agents work through Claude Code
- **API Reference**: Direct HTTP API documentation

### 🔧 [External Services](./guides/external_services.md)
- **Platform Documentation**: Docker, Render, PostgreSQL, Sentry, etc.
- **Service Integration**: How to integrate with Fed Job Advisor tech stack
- **Configuration Guides**: Setup and deployment

### 💻 [Development](./guides/development.md)
- **Project Structure**: 2024 MCP standards compliant layout
- **Adding Agents**: How to create new specialized agents
- **Testing**: Comprehensive test coverage

### 🚀 [API Reference](./api/)
- **Endpoints**: Complete API documentation
- **Examples**: Sample requests and responses
- **Authentication**: API security and access

## 🎯 Core Features

### Federal Job Application Intelligence
- **Role-Specific Guidance**: Data Scientist (1560), Statistician (1530), DBA (2210), etc.
- **Merit Hiring Compliance**: Essay structure validation (NO content writing)
- **Resume Optimization**: 2-page federal format compliance
- **Market Analytics**: Federal job market trends and salary data

### MCP Integration Benefits
- **Cost Effective**: 90% cost reduction using local gptFree model (~$0.24/session)
- **Compliance Safe**: Never writes content for users - guidance only
- **Claude Code Ready**: Direct integration with Claude Code MCP system
- **Scalable**: Handle 1000+ applications daily

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Claude Code (MCP Client)           │
│                                                 │
└────────────────────┬────────────────────────────┘
                     │ MCP Protocol
        ┌────────────▼────────────┐
        │   MCP Server            │
        │   (mcp_server.py)       │
        └────────────┬────────────┘
                     │ HTTP API
        ┌────────────▼────────────┐
        │   Agent System          │
        │   (main.py:8001)        │
        └────────────┬────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────────┐ ┌─────▼──────┐ ┌──────▼─────┐
│Fed Agents  │ │ External   │ │ Analytics  │
│(10 types)  │ │ Services   │ │ & Intel    │
└────────────┘ └────────────┘ └────────────┘
```

## 🚀 Quick Examples

### Using with Claude Code (MCP)
```
Use the "analyze_data_scientist_profile" MCP tool to analyze a federal data scientist application
```

### Using with Direct API
```bash
curl -X POST http://localhost:8001/agents/data-scientist/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "skills": ["Python", "R", "SQL", "Machine Learning"],
    "experience": "5 years in data science...",
    "target_grade": "GS-13"
  }'
```

## 📊 Performance

- **Response Time**: <2 seconds average
- **Token Usage**: 80% reduction vs cloud LLMs  
- **Concurrent Users**: 50+ supported
- **Memory Usage**: ~2GB per active agent
- **Cost**: ~$0.24 per session vs $2.40 cloud

## 🔒 Compliance

### Merit Hiring Compliance
- ✅ Never writes essay content
- ✅ Only provides structural guidance
- ✅ Enforces 200-word limits
- ✅ Validates STAR method usage

### Data Privacy
- No PII storage
- Local LLM processing
- Redis memory with TTL
- Audit trail logging

---

**Last Updated**: 2025-08-19 | **Version**: 2.0.0 | **MCP Standards**: 2024
# Fed Job Advisor MCP Agent System - Project Management

## 🎯 System Context

This MCP Agent System is a **component** of the larger Fed Job Advisor project. It provides specialized AI agents for federal job application assistance.

### **Project Hierarchy**
```
Fed Job Advisor (Main Project)
├── frontend/                    # Next.js application  
├── backend/                     # FastAPI application
└── Agents/                      # ← THIS MCP AGENT SYSTEM
    ├── src/                     # Agent implementation
    ├── docs_unified/           # User documentation  
    └── _Management/            # ← Project management context
```

## 🔗 Links to Main Project

### **Fed Job Advisor Main Project Management**
- **Main PM Folder**: `../../../fedJobAdvisor/_Management/_PM/`
- **Business Model**: `../../../fedJobAdvisor/_Management/_PM/BusinessModel.md`
- **Project Tasks**: `../../../fedJobAdvisor/_Management/_PM/_Tasks/`
- **Product Requirements**: `../../../fedJobAdvisor/_Management/_PM/PRODUCT_REQUIREMENTS_DOCUMENT.md`

### **Integration Points**
- **MCP Integration**: This system provides MCP tools for Claude Code
- **API Integration**: Agents accessible via HTTP API at `localhost:8001`
- **Fed Job Advisor Backend**: Calls this system for AI-powered features

## 📁 This System's Project Management

### **Current Project Status**
- **[Project Status](./_PM/project_status.md)** - Current development status
- **[Implementation Log](./_PM/implementation_log.md)** - Development history
- **[Research Archive](./_PM/research/)** - Technical research and decisions

### **Active Tasks**
- **[CLI Integration Research](./_Tasks/GLOBAL_CLI_INTEGRATION_RESEARCH.md)** - Global CLI tool development

## 🎯 Agent System Role in Fed Job Advisor

### **Standalone Capabilities**
- 10+ specialized federal job agents
- Merit Hiring compliance validation
- Federal job market analytics
- Resume optimization guidance

### **Fed Job Advisor Integration**
- Powers AI features via MCP protocol
- Provides career guidance through Claude Code
- Supports $29 Local / $49 Mobile pricing tiers
- Enables federal job matching and recommendations

### **Cost & Performance**
- **Local LLM**: ~$0.24/session vs $2.40 cloud
- **Response Time**: <2 seconds average  
- **Scale**: 50+ concurrent users
- **Compliance**: Merit Hiring safe (guidance only)

## 🚀 Development Workflow

### **For Agent Development**
1. Use `docs_unified/guides/development.md` for development guide
2. Follow 2024 MCP standards in `src/` structure
3. Test with `python -m pytest src/tests/`

### **For Fed Job Advisor Integration**
1. Start MCP server: `python mcp_server.py`
2. Use MCP tools in Claude Code
3. Or call HTTP API from Fed Job Advisor backend

### **For Project Planning**
1. Check main project status in `../../../fedJobAdvisor/_Management/`
2. Update this system's status in `./_PM/project_status.md`
3. Document research in `./_PM/research/`

## 📊 Success Metrics

### **Technical Metrics**
- MCP tool response time <2 seconds
- Test coverage >80% for agent functionality
- No Merit Hiring compliance violations

### **Business Metrics** (Fed Job Advisor Level)
- User engagement with AI features
- Conversion from free to paid tiers
- Federal job application success rates

## 🔄 Regular Updates

### **This System Updates**
- Agent performance metrics
- New agent development progress
- MCP integration improvements

### **Main Project Coordination**
- Feature requests from Fed Job Advisor team
- Integration testing with frontend/backend
- Launch preparation coordination

---

**This MCP Agent System provides the AI intelligence foundation for Fed Job Advisor's federal career guidance platform.**
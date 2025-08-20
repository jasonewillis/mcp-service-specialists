# Federal Job Application Agents

## 🎯 Overview

The Fed Job Advisor MCP system provides 10+ specialized AI agents for federal job application assistance. All agents are accessible through Claude Code's MCP integration and direct HTTP API.

## 🤖 Available Agents

### Role-Based Profile Analysis

#### 1. Data Scientist Agent (Series 1560)
**MCP Tool**: `analyze_data_scientist_profile`
**Specialization**: Python, R, ML/AI, statistical modeling expertise
**Focus**: Technical depth assessment, project relevance, publication evaluation

#### 2. Statistician Agent (Series 1530) 
**MCP Tool**: `analyze_statistician_profile`
**Specialization**: Statistical analysis, hypothesis testing, data visualization
**Focus**: Statistical methodology, survey design, research publications

#### 3. Database Administrator Agent (Series 2210/0334)
**MCP Tool**: `analyze_database_admin_profile`  
**Specialization**: SQL, database optimization, data architecture
**Focus**: Platform expertise, security clearance guidance, performance tuning

#### 4. DevOps Engineer Agent (Series 2210)
**MCP Tool**: `analyze_devops_profile`
**Specialization**: CI/CD, cloud infrastructure, automation, containerization
**Focus**: Pipeline analysis, container/cloud experience, infrastructure automation

#### 5. IT Specialist Agent (Series 2210)
**MCP Tool**: `analyze_it_specialist_profile`
**Specialization**: General IT skills, systems administration, troubleshooting
**Focus**: Broad IT competency, specialty area matching, certification alignment

### Compliance & Optimization Agents

#### 6. Essay Compliance Agent
**MCP Tool**: `check_essay_compliance`
**Specialization**: Merit hiring principles, federal hiring compliance
**Focus**: STAR structure validation, word count enforcement (NEVER writes content)

#### 7. Resume Compression Agent
**MCP Tool**: `analyze_resume_compression`
**Specialization**: Resume optimization, 2-page federal format
**Focus**: Content prioritization, format optimization, redundancy identification

#### 8. Executive Orders Research Agent
**MCP Tool**: `research_executive_orders`
**Specialization**: Policy research, regulatory compliance analysis
**Focus**: Policy impact analysis, keyword extraction, compliance alignment

### Analytics & Intelligence Agents

#### 9. Job Market Analytics Agent
**MCP Tool**: `analyze_job_market`
**Specialization**: Market trends, salary analysis, location intelligence
**Focus**: Federal job market trends, competition analysis, skill demand analysis

#### 10. Collection Orchestration Agent
**MCP Tool**: `orchestrate_job_collection`
**Specialization**: Data pipeline monitoring, collection orchestration
**Focus**: API health monitoring, data quality validation, performance optimization

### Meta-Agent

#### 11. Agent Router
**MCP Tool**: `route_to_best_agent`
**Specialization**: Intelligent agent routing and task coordination
**Focus**: Determines optimal agent combinations for complex tasks

## 🔧 Integration Methods

### Claude Code MCP Integration (Recommended)
```
Use MCP tools directly in Claude Code:
- "analyze_data_scientist_profile" tool
- "check_essay_compliance" tool  
- "analyze_job_market" tool
- etc.
```

### Direct HTTP API
```bash
# Health check
curl http://localhost:8001/health

# Agent analysis
curl -X POST http://localhost:8001/agents/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "role": "data_scientist",
    "user_id": "user123", 
    "data": {
      "skills": ["Python", "TensorFlow", "AWS"],
      "experience": "Led ML projects...",
      "target_grade": "GS-14"
    }
  }'
```

## 📊 Agent Capabilities

### Federal Job Series Coverage
- **1560**: Data Scientist
- **1530**: Statistician  
- **2210**: IT Specialist (all specialties)
- **0334**: Database Administrator
- **General**: Cross-series guidance and compliance

### Compliance Features
- **Merit Hiring Safe**: Never writes content for users
- **STAR Method**: Validates structure without writing
- **Word Limits**: Enforces federal essay requirements
- **Grade Level**: Tailored guidance by target GS level

### Performance Metrics
- **Response Time**: <2 seconds average
- **Cost**: ~$0.24 per session (90% reduction vs cloud)
- **Accuracy**: Expert-level federal job guidance
- **Scale**: 50+ concurrent users supported

## 🎯 Usage Patterns

### Individual Agent Analysis
Best for: Single aspect analysis (skills, compliance, market data)

### Multi-Agent Orchestration  
Best for: Comprehensive application review using multiple agents

### Agent Router Coordination
Best for: Complex tasks requiring intelligent agent selection

## 🔒 Compliance & Privacy

### Merit Hiring Compliance
- ✅ Structural guidance only
- ✅ No content generation
- ✅ STAR method validation
- ✅ Word count enforcement

### Data Protection
- No PII storage beyond session
- Local LLM processing
- Redis memory with TTL
- Comprehensive audit logging

---

**Ready for federal career intelligence at scale through Claude Code MCP integration**
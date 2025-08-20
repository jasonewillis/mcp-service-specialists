# [Agent Name] - Fed Job Advisor MCP Agent

**Agent Type**: [Role-Based | Compliance | Analytics]  
**Domain**: [Primary expertise area]  
**Endpoint**: `http://localhost:8001/agents/[agent-endpoint]/analyze`  
**Status**: [Active | Development | Optimization]  

*Based on MCP and LangChain best practices for 2025*

---

## 🎯 Agent Overview

### Primary Function
[What this agent does in 1-2 sentences]

### Federal Expertise
- **Job Series**: [Relevant federal job series this agent handles]
- **Domain Knowledge**: [Specific federal expertise areas]
- **Compliance Requirements**: [Federal regulations this agent understands]

### Integration Value
- **Fed Job Advisor Use Cases**: [How this agent helps fedJobAdvisor development]
- **Claude Code Integration**: [How Claude Code uses this agent]
- **Cost Efficiency**: ~$0.24/session (90% reduction vs cloud LLMs)

---

## 🔧 Technical Specification

### API Endpoint
```bash
POST http://localhost:8001/agents/[agent-endpoint]/analyze
```

### Input Schema
```json
{
  "user_id": "string",
  "task_type": "string",
  "context": {
    // Agent-specific context fields
  },
  "requirements": {
    // Task requirements
  }
}
```

### Output Schema
```json
{
  "agent_type": "string",
  "analysis": {
    "summary": "string",
    "recommendations": ["string"],
    "compliance_check": "boolean",
    "confidence_score": "number"
  },
  "implementation_guidance": {
    "claude_code_instructions": "string",
    "files_to_modify": ["string"],
    "testing_approach": "string"
  },
  "metadata": {
    "processing_time": "number",
    "tokens_used": "number",
    "cost": "number"
  }
}
```

---

## 📋 Usage Examples

### Basic Agent Call
```python
import httpx

async def call_agent(task_data):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/[agent-endpoint]/analyze",
            json=task_data
        )
        return response.json()

# Example usage
result = await call_agent({
    "user_id": "dev_session_123",
    "task_type": "[specific_task_type]",
    "context": {
        // Task-specific context
    }
})
```

### Claude Code Integration Pattern
```bash
# How Claude Code uses this agent in Ultimate Workflow
# Step 1: Determine if task requires this agent's expertise
# Step 2: Call agent for specialized research
# Step 3: Follow agent's implementation guidance
# Step 4: Provide feedback for agent optimization
```

---

## 🚀 Fed Job Advisor Integration

### Use Cases
1. **[Primary Use Case]**: [Description]
2. **[Secondary Use Case]**: [Description]  
3. **[Additional Use Case]**: [Description]

### Integration Patterns
- **MCP Research Phase**: When Claude Code routes [task types] to this agent
- **Documentation Output**: Agent generates markdown in `_Management/_PM/_Tasks/`
- **Implementation Guidance**: Specific instructions for Claude Code implementation
- **Testing Validation**: Agent provides test scenarios for verification

### Task Routing Logic
```typescript
// When to use this agent
if (task.domain === "[domain]" || task.type === "[type]") {
    return await callMCPAgent("[agent-endpoint]", taskContext);
}
```

---

## 📊 Performance Metrics

### Current Performance
- **Response Time**: [Average response time]
- **Accuracy**: [Success rate for recommendations]
- **Usage**: [How often used in fedJobAdvisor development]
- **Cost**: ~$0.24/session

### Optimization History
| Date | Change | Improvement | Usage Impact |
|------|--------|-------------|--------------|
| [Date] | [Change description] | [Metric improvement] | [Usage change] |

---

## 🔄 Optimization & Feedback

### Claude Code Feedback Integration
```python
# How Claude Code provides feedback for agent improvement
async def provide_agent_feedback(agent_type, implementation_result):
    feedback = {
        "agent_type": agent_type,
        "task_success": implementation_result.success,
        "accuracy_rating": implementation_result.accuracy,
        "time_saved": implementation_result.time_saved,
        "recommendations": implementation_result.improvement_suggestions
    }
    
    # Send to agent optimization system
    await submit_feedback(feedback)
```

### Improvement Areas
- **Current Strengths**: [What this agent does well]
- **Optimization Opportunities**: [Areas for improvement]
- **Usage Patterns**: [How agent is actually used vs intended use]
- **Integration Enhancements**: [Better Claude Code integration opportunities]

---

## 🧪 Testing & Validation

### Test Scenarios
```python
# Example test cases for agent validation
test_cases = [
    {
        "input": {...},
        "expected_output": {...},
        "success_criteria": [...]
    }
]
```

### NO BS Validation
- **Data Honesty**: [How agent maintains NO BS principles]
- **Capability Limits**: [What this agent cannot do]
- **Accuracy Claims**: [Backed by actual performance data]

---

## 📚 Documentation Maintenance

### Last Updated
**Date**: [Last update date]  
**Updated By**: [Claude Code | Manual]  
**Changes**: [Summary of recent changes]

### Review Schedule
- **Weekly**: Usage pattern analysis and performance metrics
- **Monthly**: Optimization opportunities and integration enhancements  
- **Quarterly**: Major capability updates and strategic improvements

---

## 🔗 Related Resources

### MCP Resources
- [Link to MCP documentation]
- [Related MCP servers]

### LangChain Resources  
- [LangGraph templates used]
- [Agent patterns implemented]

### Fed Job Advisor Resources
- [Integration documentation]
- [Related agents]
- [Usage examples in codebase]

---

*This agent documentation follows MCP and LangChain 2025 best practices, adapted for Fed Job Advisor Ultimate Workflow Integration.*

**© 2025 Fed Job Advisor Agent System**
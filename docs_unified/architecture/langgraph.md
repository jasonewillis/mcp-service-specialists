# LangGraph Integration for Fed Job Advisor Agents

This document describes the new LangGraph orchestrator layer added to the Fed Job Advisor agent system.

## Overview

The LangGraph integration provides a sophisticated workflow orchestration system that:

- **Coordinates multiple agents** for complex tasks
- **Routes requests** to appropriate workflows based on content analysis
- **Ensures compliance** with Merit Hiring requirements and project constraints
- **Manages conversation state** across multiple interactions
- **Supports both user-facing and platform development** workflows

## Architecture

### Core Components

1. **FedJobOrchestrator** (`app/orchestrator/fed_job_orchestrator.py`)
   - Main orchestration engine using LangGraph StateGraph
   - Coordinates agent execution with state management
   - Handles routing, compliance checking, and result validation

2. **ApplicationState** (TypedDict)
   - Comprehensive state object that flows through workflows
   - Tracks user context, agent results, compliance status, and metadata

3. **Workflow Types**
   - `USER_QUERY`: Job search, career guidance
   - `PLATFORM_DEVELOPMENT`: Feature implementation, code changes
   - `DATA_COLLECTION`: USAJobs API operations, data processing
   - `MERIT_COMPLIANCE`: Essay guidance, hiring compliance
   - `JOB_MATCHING`: Candidate-job matching operations
   - `SYSTEM_MAINTENANCE`: Bug fixes, optimizations

### Workflow Flow

```
START → Initialize Request → Route Task → Check Compliance
  ↓
User Workflow OR Platform Workflow
  ↓
Coordinate Agents → Validate Results → Finalize Response → END
```

## Key Features

### 1. Intelligent Routing
- Analyzes request content to determine appropriate workflow type
- Routes to specialized agents based on task requirements
- Supports both parallel and sequential agent execution

### 2. Compliance Enforcement
- **Merit Hiring**: Prevents AI content generation for essays
- **Protected Files**: Warns about modifications to critical files
- **Budget Constraints**: Enforces $0 external development budget
- **Data Requirements**: Ensures Fields=Full parameter usage

### 3. State Management
- Persistent conversation history across sessions
- Agent coordination with shared context
- Error recovery and retry mechanisms
- Human review flags for critical operations

### 4. Agent Coordination
- **Parallel Execution**: Multiple agents work simultaneously
- **Sequential Execution**: Agents pass context forward
- **Result Validation**: Comprehensive success/failure checking
- **Error Handling**: Graceful degradation and recovery

## Usage

### Basic Usage

```python
from app.orchestrator import get_orchestrator

# Get orchestrator instance
orchestrator = get_orchestrator()

# Process a user query
result = await orchestrator.process_request(
    user_id="user123",
    query="Help me find cybersecurity jobs in DC with clearance requirements",
    context={"user_preferences": {"location": "DC"}}
)

print(f"Success: {result['success']}")
print(f"Response: {result['response']}")
```

### Session Continuity

```python
# First query
result1 = await orchestrator.process_request(
    user_id="user123",
    query="What are federal job benefits?"
)

# Follow-up in same session
result2 = await orchestrator.process_request(
    user_id="user123", 
    query="How does retirement work?",
    session_id=result1['session_id']
)

# Get conversation history
history = await orchestrator.get_session_history(result1['session_id'])
```

### FastAPI Integration

```python
from app.orchestrator import get_orchestrator

@app.post("/query")
async def process_query(request: QueryRequest):
    orchestrator = get_orchestrator()
    result = await orchestrator.process_request(
        user_id=request.user_id,
        query=request.query,
        context=request.context
    )
    return result
```

## Workflow Types in Detail

### User Query Workflow
- **Purpose**: Handle job seekers and career guidance requests
- **Agents**: Analytics, Data Scientist, Job Collector
- **Execution**: Parallel for efficiency
- **Features**: Job matching, career guidance, salary analysis

### Platform Development Workflow  
- **Purpose**: Implement new features and system changes
- **Agents**: DevOps Engineer, Database Admin, Project Manager
- **Execution**: Sequential with human review
- **Features**: Compliance checking, timeline estimation, risk assessment

### Merit Compliance Workflow
- **Purpose**: Ensure hiring compliance and essay guidance
- **Agents**: Essay Guidance, Compliance Auditor, Test Coverage
- **Execution**: Sequential with strict validation
- **Features**: Word limit enforcement, STAR method guidance, attestation requirements

### Data Collection Workflow
- **Purpose**: Manage USAJobs API operations and data quality
- **Agents**: Data Pipeline Guardian, Quality Analyst, Performance Tuner
- **Execution**: Parallel with protected file checking
- **Features**: Fields=Full validation, data quality monitoring, collection optimization

## Critical Constraints

The orchestrator enforces these project constraints:

1. **Merit Hiring Compliance**
   - NEVER generate essay content for candidates
   - Enforce 200-word strict limit
   - Require no-AI attestation
   - Focus on STAR method guidance only

2. **Protected Resources**
   - `backend/collect_federal_jobs.py` (contains Fields=Full fix)
   - `backend/collect_current_jobs.py` (prevents 93% data loss)
   - `.env` files (read-only, managed by Render)
   - Critical API parameters (Fields=Full, ResultsPerPage=500)

3. **Development Constraints**
   - Solo developer (no hiring contractors)
   - $0 budget for external development
   - Part-time development (10-20 hours/week)
   - Bootstrap/self-funded approach

4. **Data Requirements**
   - Fields=Full parameter mandatory in USAJobs API calls
   - 53 official OPM locality pay areas
   - Critical field validation (title, agency, salary, location)

## Testing

### Run Basic Tests
```bash
cd /Users/jasonewillis/Developer/jwRepos/JLWAI/Agents
python test_langgraph_orchestrator.py
```

### Run Integration Examples
```bash
python example_langgraph_integration.py
```

## Installation

The required dependencies have been added to `requirements.txt`:

```
langgraph==0.2.50
langgraph-checkpoint==2.0.6
```

Install with:
```bash
pip install -r requirements.txt
```

## Directory Structure

```
Agents/
├── app/
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   └── fed_job_orchestrator.py
│   ├── agents/
│   │   ├── platform/
│   │   │   ├── __init__.py
│   │   │   └── feature_developer.py
│   │   └── ...
│   └── ...
├── test_langgraph_orchestrator.py
├── example_langgraph_integration.py
└── requirements.txt
```

## Next Steps

1. **Agent Integration**: Connect more existing agents to the orchestrator
2. **Platform Agents**: Develop specialized platform development agents
3. **UI Integration**: Connect orchestrator to frontend components
4. **Monitoring**: Add comprehensive logging and metrics
5. **Testing**: Expand test coverage for all workflow types

## Benefits

- **Unified Coordination**: Single point of control for all agent interactions
- **Compliance Enforcement**: Automatic enforcement of project constraints
- **State Management**: Persistent conversation and workflow state
- **Scalability**: Easy to add new agents and workflow types
- **Error Recovery**: Robust error handling and retry mechanisms
- **Human Oversight**: Built-in flags for human review when needed

This LangGraph integration preserves all existing functionality while adding sophisticated orchestration capabilities to support both user-facing applications and platform development workflows.
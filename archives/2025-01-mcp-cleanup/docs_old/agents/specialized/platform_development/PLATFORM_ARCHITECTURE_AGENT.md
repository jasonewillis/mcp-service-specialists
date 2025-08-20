# Platform Architecture Agent - Fed Job Advisor MCP Agent

**Agent Type**: Platform Development  
**Domain**: Microservices Architecture, Event Bus, API Gateway Design  
**Endpoint**: `http://localhost:8001/agents/platform-architecture/analyze`  
**Status**: Active  

*Based on microservices patterns, event-driven architecture, and API gateway best practices for 2025*

---

## 🎯 Agent Overview

### Primary Function
Specialized in platform architecture design for Fed Job Advisor, focusing on microservices patterns, event-driven communication, and scalable API gateway architecture for federal applications.

### Federal Expertise
- **Government Scalability**: Federal application scaling patterns for high user loads
- **Inter-Service Security**: Government-grade service-to-service authentication and authorization
- **Federal Data Flow**: Secure data routing and transformation between government services

### Integration Value
- **Fed Job Advisor Use Cases**: Service decomposition, event architecture, API gateway design, scalability planning
- **Claude Code Integration**: Architecture planning, service boundary definition, communication pattern design
- **Cost Efficiency**: ~$0.24/session (90% reduction vs cloud LLMs)

---

## 🔧 Technical Specification

### API Endpoint
```bash
POST http://localhost:8001/agents/platform-architecture/analyze
```

### Input Schema
```json
{
  "user_id": "string",
  "task_type": "service_decomposition|event_architecture|api_gateway|scalability_planning",
  "context": {
    "current_architecture": "monolith|microservices|hybrid",
    "system_requirements": {
      "expected_users": "number",
      "data_volume": "string",
      "performance_targets": {
        "response_time": "string",
        "throughput": "string",
        "availability": "string"
      }
    },
    "services_scope": {
      "user_management": "boolean",
      "job_processing": "boolean", 
      "data_collection": "boolean",
      "analytics": "boolean",
      "notifications": "boolean"
    },
    "constraints": {
      "budget_limit": "string",
      "team_size": "number",
      "compliance_requirements": ["string"]
    }
  },
  "requirements": {
    "analysis_depth": "basic|detailed|comprehensive",
    "include_diagrams": "boolean",
    "include_implementation_plan": "boolean"
  }
}
```

### Output Schema
```json
{
  "agent_type": "platform_architecture",
  "analysis": {
    "summary": "Architecture analysis and recommendations",
    "service_decomposition": {
      "recommended_services": ["string"],
      "service_boundaries": "object",
      "data_ownership": "object"
    },
    "communication_patterns": {
      "synchronous": ["string"],
      "asynchronous": ["string"],
      "event_streams": ["string"]
    },
    "api_gateway_design": {
      "routing_strategy": "string",
      "authentication_flow": "string",
      "rate_limiting": "object",
      "monitoring": "object"
    },
    "scalability_assessment": {
      "bottlenecks": ["string"],
      "scaling_strategies": ["string"],
      "performance_projections": "object"
    }
  },
  "implementation_guidance": {
    "claude_code_instructions": "Step-by-step architecture implementation",
    "migration_strategy": "string",
    "service_templates": ["string"],
    "infrastructure_requirements": "object"
  },
  "architecture_diagrams": {
    "service_map": "string",
    "data_flow": "string",
    "deployment_diagram": "string"
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

### Service Decomposition Analysis
```python
import httpx

async def analyze_service_decomposition():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/platform-architecture/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "service_decomposition",
                "context": {
                    "current_architecture": "monolith",
                    "system_requirements": {
                        "expected_users": 10000,
                        "data_volume": "50GB federal job data",
                        "performance_targets": {
                            "response_time": "< 200ms",
                            "throughput": "1000 rps",
                            "availability": "99.9%"
                        }
                    },
                    "services_scope": {
                        "user_management": True,
                        "job_processing": True,
                        "data_collection": True,
                        "analytics": True,
                        "notifications": True
                    },
                    "constraints": {
                        "budget_limit": "minimal",
                        "team_size": 1,
                        "compliance_requirements": ["federal_security", "audit_logging"]
                    }
                },
                "requirements": {
                    "analysis_depth": "comprehensive",
                    "include_diagrams": True,
                    "include_implementation_plan": True
                }
            }
        )
        return response.json()
```

### API Gateway Design
```python
async def design_api_gateway():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/platform-architecture/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "api_gateway",
                "context": {
                    "current_architecture": "microservices",
                    "services_scope": {
                        "user_management": True,
                        "job_processing": True,
                        "analytics": True
                    }
                }
            }
        )
        return response.json()
```

---

## 🚀 Fed Job Advisor Integration

### Use Cases
1. **Service Decomposition**: Break monolithic application into manageable microservices
2. **Event Architecture**: Design asynchronous communication between federal data services
3. **API Gateway Design**: Centralized routing, authentication, and rate limiting
4. **Scalability Planning**: Architecture roadmap for federal user growth

### Integration Patterns
- **MCP Research Phase**: When Claude Code routes architecture planning tasks to this agent
- **Documentation Output**: Agent generates architecture specs in `_Management/_PM/_Tasks/ARCHITECTURE_[COMPONENT]_DESIGN.md`
- **Implementation Guidance**: Service creation and deployment strategies
- **Testing Validation**: Architecture validation and performance testing scenarios

### Task Routing Logic
```typescript
// When to use this agent
if (task.domain === "architecture" || 
    task.type === "service_design" ||
    task.involves("microservices") || 
    task.involves("api_gateway") ||
    task.involves("scalability") ||
    task.involves("event_driven")) {
    return await callMCPAgent("platform-architecture", taskContext);
}
```

---

## 📊 Claude Prompt Templates

### Core Platform Architecture Prompt
```
You are a Platform Architecture Agent specialized in microservices design, event-driven architecture, and API gateway patterns for Fed Job Advisor.

EXPERTISE AREAS:
- Microservices decomposition strategies and service boundary definition
- Event-driven architecture patterns and message broker integration
- API gateway design with Kong, AWS API Gateway, or similar platforms
- Service mesh architecture with Istio or Linkerd patterns
- Domain-driven design (DDD) for service boundaries
- CQRS and Event Sourcing patterns for data consistency
- Distributed system patterns and fault tolerance
- Container orchestration with Docker and Kubernetes
- Service communication patterns (sync/async)

FEDERAL SPECIALIZATION:
- Government application scaling requirements
- Federal data security across service boundaries
- Compliance-driven architecture decisions
- Government user load patterns and traffic management
- Federal data sovereignty and service isolation
- Multi-tenant architecture for different agencies

TASK CAPABILITIES:
1. Service Decomposition: Analyze monoliths and recommend microservice boundaries
2. Event Architecture: Design event streams and asynchronous communication
3. API Gateway Design: Centralized routing, auth, and traffic management
4. Scalability Planning: Performance projections and scaling strategies
5. Data Flow Design: Secure data routing between services
6. Migration Strategy: Step-by-step decomposition and migration plans
7. Compliance Integration: Federal security and audit requirements

OUTPUT REQUIREMENTS:
- Provide clear service boundary recommendations with DDD principles
- Design event schemas and communication patterns
- Include detailed API gateway configuration examples
- Generate migration strategies for existing Fed Job Advisor codebase
- Provide performance estimates and scaling projections
- Include security considerations for inter-service communication
- Create implementation timelines considering solo developer constraints

INTEGRATION WITH FED JOB ADVISOR:
- Understand current monolithic structure in backend/app/
- Consider existing federal data requirements and compliance needs
- Account for single developer implementation constraints
- Maintain backward compatibility during migration phases

When receiving an architecture task, analyze the current system, provide detailed decomposition recommendations, design communication patterns, and create pragmatic implementation plans.
```

### Event-Driven Architecture Prompt
```
You are designing event-driven architecture for Fed Job Advisor's federal data processing platform.

EVENT ARCHITECTURE PRINCIPLES:
- Asynchronous communication for decoupled services
- Event sourcing for audit trails and data consistency
- CQRS patterns for read/write optimization
- Message broker selection and configuration
- Event schema design and versioning
- Dead letter queues and error handling

FEDERAL DATA REQUIREMENTS:
- Audit trail compliance for all data changes
- Large-scale federal job data processing
- Real-time notifications for job matching
- Data consistency across distributed services
- Secure event transmission and storage

EVENT PATTERNS:
1. Command Events: User actions and system commands
2. Domain Events: Business logic state changes
3. Integration Events: Cross-service communication
4. Notification Events: User and system notifications

TECHNOLOGY CONSIDERATIONS:
- Message brokers: Redis Streams, PostgreSQL LISTEN/NOTIFY, or RabbitMQ
- Event stores: PostgreSQL with event sourcing tables
- Stream processing: Python asyncio patterns
- Event schemas: Pydantic models for type safety

OUTPUT FORMAT:
- Event taxonomy and naming conventions
- Message broker configuration recommendations
- Event schema definitions with Pydantic models
- Error handling and retry strategies
- Monitoring and observability patterns

Design a comprehensive event architecture that supports Fed Job Advisor's federal data requirements while maintaining simplicity for single developer implementation.
```

### Service Decomposition Prompt
```
You are analyzing Fed Job Advisor's monolithic backend for microservice decomposition.

DECOMPOSITION STRATEGY:
- Domain-driven design principles for service boundaries
- Data ownership and database-per-service patterns
- API contract design for service interfaces
- Strangler fig pattern for gradual migration
- Service sizing based on team structure and complexity

CURRENT FED JOB ADVISOR DOMAINS:
1. User Management: Authentication, profiles, preferences
2. Job Processing: Search, filtering, matching algorithms
3. Data Collection: Federal job data ingestion and processing
4. Analytics: Usage metrics, performance tracking
5. Notifications: Email, alerts, job recommendations

FEDERAL CONSIDERATIONS:
- Compliance requirements per service domain
- Data security classification and handling
- Service isolation for different security levels
- Audit logging requirements per service
- Performance requirements for federal user loads

DECOMPOSITION CRITERIA:
- Business capability alignment
- Data ownership clarity
- Team cognitive load (single developer)
- Technology stack consistency
- Deployment independence

OUTPUT FORMAT:
- Service boundary recommendations with justification
- Data ownership mapping and shared data strategies
- API contract definitions between services
- Migration sequence and timeline
- Implementation complexity assessment

Analyze the current Fed Job Advisor backend and provide detailed service decomposition recommendations with implementation guidance.
```

---

## 🧪 Testing & Validation

### Test Scenarios
```python
# Platform architecture testing scenarios
test_cases = [
    {
        "input": {
            "current_architecture": "monolith",
            "expected_users": 10000,
            "compliance_requirements": ["federal_security"]
        },
        "expected_output": {
            "service_count": "3-5 services",
            "migration_complexity": "medium",
            "performance_improvement": "> 20%"
        },
        "success_criteria": [
            "Clear service boundaries defined",
            "Federal compliance maintained",
            "Solo developer implementation feasible"
        ]
    }
]
```

### NO BS Validation
- **Data Honesty**: Performance projections based on industry benchmarks and federal application patterns
- **Capability Limits**: Cannot test actual deployment, provides architectural analysis only
- **Accuracy Claims**: Service recommendations validated against DDD principles and federal requirements

---

## 🔗 Related Resources

### Microservices Resources
- [Microservices.io](https://microservices.io/)
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/)
- [Building Microservices (O'Reilly)](https://www.oreilly.com/library/view/building-microservices/9781491950340/)

### Event Architecture Resources
- [Event Storming](https://www.eventstorming.com/)
- [Event Sourcing Patterns](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs)

### API Gateway Resources
- [Kong Gateway](https://konghq.com/kong/)
- [AWS API Gateway Best Practices](https://aws.amazon.com/api-gateway/)
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)

### Fed Job Advisor Resources
- [Current Backend Architecture](../../../backend/app/)
- [Service Integration Patterns](../../../docs/integration-patterns.md)
- [Performance Requirements](../../../docs/performance-requirements.md)

---

*This agent specializes in scalable platform architecture design with federal compliance considerations, optimized for Fed Job Advisor's government data processing requirements.*

**© 2025 Fed Job Advisor Agent System**
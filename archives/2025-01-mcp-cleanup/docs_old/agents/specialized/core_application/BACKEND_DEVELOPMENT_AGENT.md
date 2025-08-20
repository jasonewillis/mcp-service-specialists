# Backend Development Agent - Fed Job Advisor MCP Agent

**Agent Type**: Core Application  
**Domain**: FastAPI + SQLModel + PostgreSQL Backend Development  
**Endpoint**: `http://localhost:8001/agents/backend-development/analyze`  
**Status**: Active  

*Based on FastAPI, SQLModel, JWT auth, and pytest best practices for 2025*

---

## 🎯 Agent Overview

### Primary Function
Specialized in FastAPI + SQLModel + PostgreSQL backend development for Fed Job Advisor, focusing on federal data security, API performance, and government compliance standards.

### Federal Expertise
- **Federal Data Security**: Government-grade data protection and encryption standards
- **API Compliance**: Federal API design standards and authentication requirements
- **Database Security**: Government database security patterns and audit trails

### Integration Value
- **Fed Job Advisor Use Cases**: API development, database modeling, security implementation, performance optimization
- **Claude Code Integration**: API endpoint generation, database schema development, security fixes
- **Cost Efficiency**: ~$0.24/session (90% reduction vs cloud LLMs)

---

## 🔧 Technical Specification

### API Endpoint
```bash
POST http://localhost:8001/agents/backend-development/analyze
```

### Input Schema
```json
{
  "user_id": "string",
  "task_type": "api_development|database_modeling|security_audit|performance_optimization",
  "context": {
    "endpoint_type": "CRUD|custom|webhook|integration",
    "existing_code": "string",
    "database_schema": "object",
    "security_requirements": {
      "authentication": "JWT|OAuth2|API_key",
      "authorization": "RBAC|ABAC|custom",
      "encryption": "boolean",
      "audit_logging": "boolean"
    },
    "performance_targets": {
      "response_time_ms": "number",
      "concurrent_users": "number",
      "database_queries": "optimized|basic"
    }
  },
  "requirements": {
    "analysis_depth": "basic|detailed|comprehensive",
    "include_tests": "boolean",
    "include_documentation": "boolean"
  }
}
```

### Output Schema
```json
{
  "agent_type": "backend_development",
  "analysis": {
    "summary": "API and database analysis with recommendations",
    "api_structure": "Recommended endpoint architecture",
    "database_design": {
      "schema_optimization": "string",
      "query_performance": "string",
      "indexing_strategy": "string"
    },
    "security_assessment": {
      "vulnerabilities": ["string"],
      "security_score": "number",
      "compliance_check": "boolean",
      "recommendations": ["string"]
    },
    "performance_metrics": {
      "estimated_response_time": "string",
      "database_efficiency": "string",
      "scalability_assessment": "string"
    }
  },
  "implementation_guidance": {
    "claude_code_instructions": "Step-by-step implementation guide",
    "files_to_create": ["string"],
    "files_to_modify": ["string"],
    "dependencies_to_add": ["string"],
    "testing_approach": "pytest test structure and coverage"
  },
  "code_templates": {
    "api_code": "string",
    "model_code": "string",
    "test_code": "string",
    "migration_code": "string"
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

### API Endpoint Development
```python
import httpx

async def develop_api_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/backend-development/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "api_development",
                "context": {
                    "endpoint_type": "CRUD",
                    "database_schema": {
                        "table": "federal_jobs",
                        "relationships": ["job_series", "localities"]
                    },
                    "security_requirements": {
                        "authentication": "JWT",
                        "authorization": "RBAC",
                        "encryption": True,
                        "audit_logging": True
                    },
                    "performance_targets": {
                        "response_time_ms": 200,
                        "concurrent_users": 1000,
                        "database_queries": "optimized"
                    }
                },
                "requirements": {
                    "analysis_depth": "comprehensive",
                    "include_tests": True,
                    "include_documentation": True
                }
            }
        )
        return response.json()
```

### Database Performance Optimization
```python
async def optimize_database():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/backend-development/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "performance_optimization",
                "context": {
                    "existing_code": "...",
                    "performance_targets": {
                        "response_time_ms": 100,
                        "concurrent_users": 500
                    }
                }
            }
        )
        return response.json()
```

---

## 🚀 Fed Job Advisor Integration

### Use Cases
1. **API Development**: Create FastAPI endpoints for federal job data processing
2. **Database Modeling**: Design SQLModel schemas for government data structures
3. **Security Implementation**: JWT auth, RBAC, and federal security compliance
4. **Performance Optimization**: Database query optimization and API response tuning

### Integration Patterns
- **MCP Research Phase**: When Claude Code routes backend development tasks to this agent
- **Documentation Output**: Agent generates API specs in `_Management/_PM/_Tasks/BACKEND_[ENDPOINT]_SPEC.md`
- **Implementation Guidance**: Specific FastAPI + SQLModel implementation instructions
- **Testing Validation**: pytest test scenarios with government data compliance

### Task Routing Logic
```typescript
// When to use this agent
if (task.domain === "backend" || 
    task.type === "api_development" ||
    task.involves("fastapi") || 
    task.involves("database") ||
    task.involves("security") ||
    task.involves("performance")) {
    return await callMCPAgent("backend-development", taskContext);
}
```

---

## 📊 Claude Prompt Templates

### Core Backend Development Prompt
```
You are a Backend Development Agent specialized in FastAPI + SQLModel + PostgreSQL development for Fed Job Advisor.

EXPERTISE AREAS:
- FastAPI framework patterns and async/await best practices
- SQLModel ORM design and database relationship modeling
- PostgreSQL optimization, indexing, and query performance
- JWT authentication and authorization systems
- Federal data security and encryption standards
- API documentation with OpenAPI/Swagger
- pytest testing strategies and mock data generation
- Alembic database migrations and version control
- Docker containerization and deployment patterns

FEDERAL SPECIALIZATION:
- Government data protection requirements
- Federal API security standards and compliance
- Audit logging and compliance tracking
- Large-scale federal dataset optimization
- Government user authentication patterns
- Federal hiring data structures and relationships

TASK CAPABILITIES:
1. API Development: Design and implement FastAPI endpoints with proper documentation
2. Database Modeling: Create SQLModel schemas with optimized relationships
3. Security Implementation: JWT auth, RBAC, encryption, and audit trails
4. Performance Optimization: Database query tuning and API response optimization
5. Testing Strategy: Comprehensive pytest coverage including integration tests
6. Migration Management: Alembic migrations for database schema evolution
7. Documentation: OpenAPI documentation and developer guides

OUTPUT REQUIREMENTS:
- Provide production-ready FastAPI code following current best practices
- Include comprehensive error handling and validation
- Implement proper async/await patterns for database operations
- Generate complete SQLModel schemas with proper relationships
- Include robust pytest test suites with fixtures and mocks
- Provide Alembic migration scripts for database changes
- Ensure federal security compliance and audit logging

INTEGRATION WITH FED JOB ADVISOR:
- Understand existing backend architecture in backend/app/
- Follow established patterns for database connections and models
- Maintain consistency with current API versioning and structure
- Consider federal data requirements and government workflows

When receiving a backend development task, analyze the requirements, provide architectural recommendations, generate production-ready code, and include comprehensive testing and migration strategies.
```

### Database Optimization Prompt
```
You are conducting database performance optimization for Fed Job Advisor's PostgreSQL backend.

OPTIMIZATION AREAS:
- Query performance analysis and improvement
- Index strategy design and implementation
- Database schema normalization and denormalization decisions
- Connection pooling and async query patterns
- Large dataset pagination and filtering
- Database migrations and schema evolution

FEDERAL DATA CONSIDERATIONS:
- Large federal job datasets (50K+ records)
- Complex filtering requirements (job series, locations, grades)
- High read-to-write ratios for job search functionality
- Audit trail requirements for compliance
- Geographic data optimization for locality pay calculations

PERFORMANCE TARGETS:
- API response times under 200ms
- Support for 1000+ concurrent users
- Efficient pagination for large result sets
- Optimized search across multiple federal datasets
- Fast aggregation queries for analytics

OUTPUT FORMAT:
- Specific query optimization recommendations
- Index creation/modification scripts
- SQLModel schema improvements
- Performance benchmarking approaches
- Migration strategies for schema changes

Analyze the provided database code and identify optimization opportunities, providing specific implementation guidance.
```

### Security Audit Prompt
```
You are conducting a security audit for Fed Job Advisor's FastAPI backend.

SECURITY STANDARDS:
- JWT token security and rotation
- RBAC implementation and role management
- API endpoint authorization
- Database connection security
- Input validation and sanitization
- OWASP Top 10 compliance
- Federal data protection requirements

AUDIT CHECKLIST:
1. Authentication mechanism security
2. Authorization logic validation
3. Input validation completeness
4. SQL injection prevention
5. Cross-site scripting (XSS) protection
6. CORS configuration security
7. Rate limiting implementation
8. Audit logging completeness
9. Error handling information disclosure
10. Dependency vulnerability assessment

FEDERAL REQUIREMENTS:
- Government-grade encryption standards
- Audit trail compliance
- Federal data classification handling
- Multi-factor authentication support

OUTPUT FORMAT:
- Security vulnerability assessment (0-100 score)
- Specific vulnerabilities with severity ratings
- Detailed remediation instructions
- Code examples for security fixes
- Compliance validation approaches

Analyze the provided backend code and identify all security issues, providing specific remediation guidance.
```

---

## 🧪 Testing & Validation

### Test Scenarios
```python
# Backend development testing scenarios
test_cases = [
    {
        "input": {
            "endpoint_type": "federal_jobs_search",
            "security_requirements": {"authentication": "JWT", "authorization": "RBAC"}
        },
        "expected_output": {
            "response_time": "< 200ms",
            "security_score": ">= 95",
            "test_coverage": ">= 90%"
        },
        "success_criteria": [
            "FastAPI endpoint follows OpenAPI standards",
            "SQLModel relationships properly defined",
            "Comprehensive pytest coverage"
        ]
    }
]
```

### NO BS Validation
- **Data Honesty**: Performance metrics based on actual database query analysis
- **Capability Limits**: Cannot test in live production environments, provides code-level analysis
- **Accuracy Claims**: Security recommendations validated against OWASP standards

---

## 🔗 Related Resources

### FastAPI Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)

### Database Resources
- [PostgreSQL Performance Tuning](https://www.postgresql.org/docs/current/performance-tips.html)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- [asyncpg Performance Guide](https://magicstack.github.io/asyncpg/current/)

### Security Resources
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [JWT Security Best Practices](https://tools.ietf.org/html/rfc8725)
- [Federal IT Security Standards](https://www.nist.gov/cybersecurity)

### Fed Job Advisor Resources
- [Backend Architecture](../../../backend/app/)
- [Database Models](../../../backend/app/models/)
- [API Documentation](../../../docs/api-documentation.md)

---

*This agent specializes in secure, high-performance backend development with federal compliance standards, optimized for Fed Job Advisor's government data requirements.*

**© 2025 Fed Job Advisor Agent System**
# Integration & DevOps Agent - Fed Job Advisor MCP Agent

**Agent Type**: Platform Development  
**Domain**: Service Communication, Docker Compose, CI/CD Integration  
**Endpoint**: `http://localhost:8001/agents/integration-devops/analyze`  
**Status**: Active  

*Based on Dapr-like service communication, Docker Compose orchestration, and modern DevOps practices for 2025*

---

## 🎯 Agent Overview

### Primary Function
Specialized in service integration patterns, Docker Compose orchestration, and DevOps automation for Fed Job Advisor, focusing on secure service communication and federal deployment standards.

### Federal Expertise
- **Government DevOps**: Federal CI/CD pipeline security and compliance requirements
- **Service Integration**: Secure inter-service communication for government applications
- **Federal Deployment**: Government-approved deployment patterns and security controls

### Integration Value
- **Fed Job Advisor Use Cases**: Service integration design, deployment automation, CI/CD pipeline optimization
- **Claude Code Integration**: Docker configuration, service communication setup, deployment scripting
- **Cost Efficiency**: ~$0.24/session (90% reduction vs cloud LLMs)

---

## 🔧 Technical Specification

### API Endpoint
```bash
POST http://localhost:8001/agents/integration-devops/analyze
```

### Input Schema
```json
{
  "user_id": "string",
  "task_type": "service_integration|docker_orchestration|cicd_pipeline|deployment_automation",
  "context": {
    "services": {
      "existing_services": ["string"],
      "planned_services": ["string"],
      "external_dependencies": ["string"]
    },
    "communication_patterns": {
      "synchronous": ["string"],
      "asynchronous": ["string"],
      "event_driven": ["string"]
    },
    "deployment_targets": {
      "development": "docker-compose|kubernetes|local",
      "staging": "render|aws|kubernetes",
      "production": "render|aws|kubernetes"
    },
    "security_requirements": {
      "service_mesh": "boolean",
      "tls_termination": "boolean", 
      "secret_management": "boolean",
      "network_policies": "boolean"
    }
  },
  "requirements": {
    "analysis_depth": "basic|detailed|comprehensive",
    "include_configs": "boolean",
    "include_monitoring": "boolean"
  }
}
```

### Output Schema
```json
{
  "agent_type": "integration_devops",
  "analysis": {
    "summary": "Integration and deployment analysis",
    "service_communication": {
      "protocols": ["HTTP|gRPC|MessageQueue"],
      "authentication": "string",
      "load_balancing": "string",
      "circuit_breakers": "object"
    },
    "orchestration_design": {
      "docker_compose_structure": "object",
      "service_dependencies": "object",
      "network_configuration": "object",
      "volume_management": "object"
    },
    "cicd_pipeline": {
      "build_stages": ["string"],
      "test_automation": "object",
      "deployment_strategy": "string",
      "rollback_procedures": "object"
    },
    "monitoring_integration": {
      "health_checks": "object",
      "metrics_collection": "object",
      "log_aggregation": "object"
    }
  },
  "implementation_guidance": {
    "claude_code_instructions": "Step-by-step integration implementation",
    "docker_configs": "object",
    "cicd_scripts": "object",
    "deployment_procedures": "string"
  },
  "configuration_templates": {
    "docker_compose": "string",
    "github_actions": "string",
    "nginx_config": "string",
    "monitoring_config": "string"
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

### Service Integration Design
```python
import httpx

async def design_service_integration():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/integration-devops/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "service_integration",
                "context": {
                    "services": {
                        "existing_services": ["user-service", "job-service"],
                        "planned_services": ["notification-service", "analytics-service"],
                        "external_dependencies": ["postgres", "redis", "usajobs-api"]
                    },
                    "communication_patterns": {
                        "synchronous": ["user-auth", "job-search"],
                        "asynchronous": ["notifications", "analytics"],
                        "event_driven": ["job-updates", "user-activity"]
                    },
                    "security_requirements": {
                        "service_mesh": False,
                        "tls_termination": True,
                        "secret_management": True,
                        "network_policies": True
                    }
                },
                "requirements": {
                    "analysis_depth": "comprehensive",
                    "include_configs": True,
                    "include_monitoring": True
                }
            }
        )
        return response.json()
```

### Docker Orchestration Setup
```python
async def setup_docker_orchestration():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/integration-devops/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "docker_orchestration",
                "context": {
                    "services": {
                        "existing_services": ["backend", "frontend"],
                        "external_dependencies": ["postgres", "redis"]
                    },
                    "deployment_targets": {
                        "development": "docker-compose",
                        "production": "render"
                    }
                }
            }
        )
        return response.json()
```

---

## 🚀 Fed Job Advisor Integration

### Use Cases
1. **Service Integration**: Design secure communication between Fed Job Advisor microservices
2. **Docker Orchestration**: Optimize Docker Compose for development and deployment
3. **CI/CD Pipeline**: Automate testing, building, and deployment processes
4. **Deployment Automation**: Streamline deployment to Render.com and other platforms

### Integration Patterns
- **MCP Research Phase**: When Claude Code routes DevOps and integration tasks to this agent
- **Documentation Output**: Agent generates deployment specs in `_Management/_PM/_Tasks/DEVOPS_[COMPONENT]_CONFIG.md`
- **Implementation Guidance**: Docker, CI/CD, and deployment configuration instructions
- **Testing Validation**: Integration testing and deployment verification scenarios

### Task Routing Logic
```typescript
// When to use this agent
if (task.domain === "devops" || 
    task.type === "integration" ||
    task.involves("docker") || 
    task.involves("cicd") ||
    task.involves("deployment") ||
    task.involves("service_communication")) {
    return await callMCPAgent("integration-devops", taskContext);
}
```

---

## 📊 Claude Prompt Templates

### Core Integration & DevOps Prompt
```
You are an Integration & DevOps Agent specialized in service communication, Docker Compose orchestration, and CI/CD automation for Fed Job Advisor.

EXPERTISE AREAS:
- Service communication patterns: HTTP/REST, gRPC, message queues
- Docker Compose orchestration and multi-service development environments
- GitHub Actions CI/CD pipeline design and optimization
- Container networking and service discovery patterns
- Secret management and environment variable handling
- Load balancing and reverse proxy configuration (nginx, Traefik)
- Health checking and circuit breaker patterns
- Monitoring integration with Prometheus, Grafana, or similar tools
- Database connection pooling and service dependencies

FEDERAL SPECIALIZATION:
- Government CI/CD security requirements and approval processes
- Federal deployment patterns and compliance controls
- Secure service-to-service communication for government data
- Government-approved container registries and image scanning
- Federal network security and firewall configurations
- Audit logging for deployment and integration activities

TASK CAPABILITIES:
1. Service Integration Design: Secure communication patterns between microservices
2. Docker Orchestration: Multi-service development and deployment environments
3. CI/CD Pipeline Creation: Automated testing, building, and deployment workflows
4. Deployment Automation: Streamlined deployment to various cloud platforms
5. Monitoring Integration: Health checks, metrics, and logging aggregation
6. Security Configuration: TLS, secrets, network policies, and access controls
7. Performance Optimization: Load balancing, caching, and resource management

OUTPUT REQUIREMENTS:
- Provide complete Docker Compose configurations for multi-service environments
- Generate production-ready CI/CD pipeline configurations
- Include comprehensive security configurations for federal compliance
- Design fault-tolerant service communication patterns
- Create monitoring and observability configurations
- Provide deployment scripts and automation tools
- Include rollback procedures and disaster recovery plans

INTEGRATION WITH FED JOB ADVISOR:
- Understand current Docker Compose setup in docker-compose.yml
- Follow established patterns for Render.com deployment
- Maintain compatibility with existing GitHub Actions workflows
- Consider federal data security requirements in all configurations

When receiving an integration or DevOps task, analyze current setup, recommend improvements, generate complete configurations, and provide step-by-step implementation guidance.
```

### Docker Compose Optimization Prompt
```
You are optimizing Docker Compose orchestration for Fed Job Advisor's multi-service development environment.

DOCKER COMPOSE OPTIMIZATION AREAS:
- Service dependency management and startup ordering
- Network configuration and service communication
- Volume management for data persistence and development workflows
- Environment variable and secret management
- Multi-stage builds and image optimization
- Development vs production configuration differences
- Resource limits and performance tuning

FEDERAL DEVELOPMENT REQUIREMENTS:
- Secure local development environment setup
- Data protection during development with federal datasets
- Network isolation for sensitive services
- Audit logging even in development environments
- Consistent environment parity between dev/staging/production

OPTIMIZATION TARGETS:
- Fast startup times for development productivity
- Minimal resource usage for local development
- Easy service scaling and configuration
- Seamless integration with IDE and debugging tools
- Automated database migrations and seed data

SERVICE ARCHITECTURE CONSIDERATIONS:
- Backend: FastAPI service with PostgreSQL database
- Frontend: Next.js application with static asset handling
- Cache: Redis for session and application caching
- Queue: Redis or PostgreSQL for background job processing
- Monitoring: Optional Prometheus/Grafana for metrics

OUTPUT FORMAT:
- Optimized docker-compose.yml with detailed comments
- Development-specific docker-compose.override.yml
- Production deployment docker-compose.prod.yml
- Makefile or scripts for common development tasks
- Documentation for service dependencies and startup procedures

Analyze the current Docker setup and provide comprehensive optimization recommendations for Fed Job Advisor's development workflow.
```

### CI/CD Pipeline Design Prompt
```
You are designing CI/CD pipelines for Fed Job Advisor using GitHub Actions with federal security considerations.

PIPELINE REQUIREMENTS:
- Automated testing for backend (pytest) and frontend (Jest)
- Code quality checks with linting and security scanning
- Docker image building and registry management
- Automated deployment to staging and production environments
- Database migration handling and rollback procedures
- Security vulnerability scanning and compliance checks

FEDERAL CI/CD CONSIDERATIONS:
- Government-approved base images and registries
- Security scanning requirements for all dependencies
- Audit trail logging for all pipeline activities
- Approval workflows for production deployments
- Compliance validation and documentation generation
- Secret management for federal API keys and credentials

DEPLOYMENT TARGETS:
- Development: Local Docker Compose environment
- Staging: Render.com or similar platform for testing
- Production: Render.com with production configurations
- Database: PostgreSQL with automated backups and migrations

SECURITY INTEGRATION:
- SAST (Static Application Security Testing) tools
- Dependency vulnerability scanning
- Container image security scanning
- Infrastructure as Code security validation
- Compliance reporting and documentation generation

OUTPUT FORMAT:
- Complete GitHub Actions workflow files (.github/workflows/)
- Security scanning and compliance check configurations
- Deployment scripts and environment-specific configurations
- Rollback procedures and disaster recovery workflows
- Pipeline monitoring and notification setups

Design a comprehensive CI/CD pipeline that meets federal security requirements while maintaining development velocity for Fed Job Advisor.
```

---

## 🧪 Testing & Validation

### Test Scenarios
```python
# Integration and DevOps testing scenarios
test_cases = [
    {
        "input": {
            "services": ["backend", "frontend", "postgres", "redis"],
            "deployment_target": "docker-compose",
            "security_requirements": {"tls_termination": True}
        },
        "expected_output": {
            "startup_time": "< 30 seconds",
            "service_connectivity": "100%",
            "security_compliance": ">= 95%"
        },
        "success_criteria": [
            "All services start successfully",
            "Inter-service communication works",
            "Security configurations applied"
        ]
    }
]
```

### NO BS Validation
- **Data Honesty**: Performance metrics based on actual Docker Compose testing
- **Capability Limits**: Cannot test actual cloud deployments, provides configuration analysis
- **Accuracy Claims**: Security recommendations validated against federal requirements

---

## 🔗 Related Resources

### Docker Resources
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Multi-stage Builds](https://docs.docker.com/develop/multistage-build/)

### CI/CD Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Security Scanning Actions](https://github.com/marketplace?type=actions&query=security)
- [Deployment Best Practices](https://docs.github.com/en/actions/deployment)

### Service Integration Resources
- [Microservices Communication Patterns](https://microservices.io/patterns/communication-style/)
- [Service Mesh Patterns](https://istio.io/latest/docs/concepts/)
- [API Gateway Patterns](https://www.nginx.com/blog/microservices-api-gateways/)

### Fed Job Advisor Resources
- [Current Docker Configuration](../../../docker-compose.yml)
- [GitHub Actions Workflows](../../../.github/workflows/)
- [Deployment Documentation](../../../docs/deployment.md)

---

*This agent specializes in secure service integration and automated deployment with federal compliance standards, optimized for Fed Job Advisor's government application requirements.*

**© 2025 Fed Job Advisor Agent System**
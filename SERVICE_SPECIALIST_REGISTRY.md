# Service Specialist Registry

## 🎯 Overview

The Service Specialist Registry provides access to 18 specialized AI agents that offer deep expertise in specific technologies, platforms, and services. These specialists integrate with the Fed Job Advisor system through the MCP (Model Context Protocol) to provide expert guidance when specialized knowledge is required.

## 🚀 Quick Access

### Infrastructure Specialists (4 agents)
- **[Render Specialist](#render-specialist)** - Cloud deployment expert
- **[PostgreSQL Expert](#postgresql-expert)** - Database administration specialist  
- **[Docker Master](#docker-master)** - Containerization expert
- **[CRON Architect](#cron-architect)** - Job scheduling specialist

### Development Specialists (5 agents)
- **[GitHub Specialist](#github-specialist)** - Version control & CI/CD expert
- **[OAuth Expert](#oauth-expert)** - Authentication security specialist
- **[Next.js Specialist](#nextjs-specialist)** - React framework expert
- **[FastAPI Specialist](#fastapi-specialist)** - Python API development expert
- **[Google Analytics Specialist](#google-analytics-specialist)** - Web analytics expert

### Service Integration Specialists (9 agents)
- **[Stripe Specialist](#stripe-specialist)** - Payment processing expert
- **[Sentry Expert](#sentry-expert)** - Error monitoring specialist
- **[USAJobs Master](#usajobs-master)** - Federal jobs API expert
- **[Redis Caching Specialist](#redis-caching-specialist)** - Performance optimization expert
- **[Alembic Migration Specialist](#alembic-migration-specialist)** - Database migration expert
- **[WebAuthn Authentication Specialist](#webauthn-authentication-specialist)** - Passwordless auth expert
- **[Email Service Specialist](#email-service-specialist)** - Email delivery expert

---

## 🏗️ Infrastructure Specialists

### Render Specialist
**Specialization**: Cloud Deployment & Platform Management

**When to Use**:
- Deploying applications to Render platform
- Optimizing cloud infrastructure costs
- Troubleshooting deployment issues
- Setting up CI/CD pipelines

**Key Capabilities**:
- Render service configuration optimization
- Performance tuning and scaling strategies
- Security best practices for cloud deployment
- Cost optimization and resource management

**Available Tools**:
```bash
analyze_render_deployment    # Analyze deployment configuration
troubleshoot_render_issues   # Debug deployment problems
optimize_render_performance  # Improve performance and costs
design_render_architecture   # Plan optimal deployment strategy
```

**Example Usage**:
```
"I need to deploy my Next.js app to Render with PostgreSQL. What's the optimal configuration for production?"
```

---

### PostgreSQL Expert
**Specialization**: Database Administration & Optimization

**When to Use**:
- Database performance optimization
- Schema design and migrations
- Query optimization and indexing
- Connection and scaling issues

**Key Capabilities**:
- Performance analysis and bottleneck identification
- Query optimization and index recommendations
- Schema design best practices
- Connection pooling and scaling strategies

**Available Tools**:
```bash
analyze_database_performance  # Performance metrics analysis
optimize_queries             # Query optimization recommendations
design_database_schema       # Schema design guidance
troubleshoot_postgres_issues # Debug database problems
```

**Example Usage**:
```
"My PostgreSQL queries are slow. Can you analyze the performance and suggest optimizations?"
```

---

### Docker Master
**Specialization**: Containerization & Orchestration

**When to Use**:
- Containerizing applications
- Optimizing Docker images
- Multi-stage build strategies
- Container orchestration

**Key Capabilities**:
- Dockerfile optimization for size and security
- Multi-stage build implementation
- Container networking and volumes
- Production deployment strategies

**Available Tools**:
```bash
design_docker_architecture      # Container strategy design
optimize_dockerfile             # Dockerfile optimization
troubleshoot_container_issues   # Debug container problems
implement_multi_stage_builds    # Multi-stage build setup
```

**Example Usage**:
```
"I need to containerize my FastAPI app with PostgreSQL. What's the best Docker setup for production?"
```

---

### CRON Architect
**Specialization**: Job Scheduling & Automation

**When to Use**:
- Setting up scheduled jobs
- Automating background tasks
- Monitoring job execution
- Cross-platform scheduling

**Key Capabilities**:
- CRON syntax and scheduling optimization
- Job monitoring and error handling
- Alternative scheduling solutions
- Performance optimization for scheduled tasks

**Available Tools**:
```bash
design_cron_schedule        # Schedule design and optimization
troubleshoot_cron_jobs      # Debug scheduling issues
optimize_job_performance    # Performance improvements
implement_job_monitoring    # Monitoring and alerting setup
```

**Example Usage**:
```
"I need to schedule daily data collection from USAJobs API. What's the best approach for reliable execution?"
```

---

## 💻 Development Specialists

### GitHub Specialist
**Specialization**: Version Control & CI/CD

**When to Use**:
- Setting up GitHub repositories
- Implementing CI/CD workflows
- Branch strategy design
- Security and collaboration setup

**Key Capabilities**:
- Repository security configuration
- GitHub Actions workflow design
- Branch protection and review processes
- Deployment automation strategies

**Available Tools**:
```bash
analyze_repository_setup    # Repository configuration analysis
generate_workflow_template  # CI/CD workflow generation
review_github_actions      # Workflow security review
suggest_branch_strategy     # Branching strategy recommendations
```

**Example Usage**:
```
"I need to set up GitHub Actions for my Next.js and FastAPI apps with automated testing and deployment to Render."
```

---

### OAuth Expert
**Specialization**: Authentication & Authorization

**When to Use**:
- Implementing OAuth 2.0 flows
- Multi-provider authentication
- Security vulnerability assessment
- Authentication troubleshooting

**Key Capabilities**:
- OAuth 2.0 and OpenID Connect expertise
- PKCE and security best practices
- Multi-provider integration strategies
- Authentication flow debugging

**Available Tools**:
```bash
design_oauth_flow              # OAuth flow design
validate_oauth_implementation  # Security validation
generate_provider_config       # Provider-specific setup
troubleshoot_oauth_issue       # Authentication debugging
```

**Example Usage**:
```
"I need to implement Google OAuth for my Next.js app with secure token management. What's the recommended approach?"
```

---

### Next.js Specialist
**Specialization**: React Framework & Full-Stack Development

**When to Use**:
- Next.js 14+ App Router projects
- Performance optimization
- Authentication integration
- Production deployment

**Key Capabilities**:
- App Router architecture design
- Server and Client Components optimization
- Performance monitoring and improvement
- Modern React patterns and best practices

**Available Tools**:
```bash
analyze_nextjs_project      # Project structure analysis
generate_app_structure      # App Router structure design
optimize_performance        # Performance optimization
design_authentication_flow  # Auth integration design
troubleshoot_nextjs_issue   # Framework-specific debugging
```

**Example Usage**:
```
"I'm building a federal job search app with Next.js 14. Can you help optimize the App Router structure for performance?"
```

---

### FastAPI Specialist
**Specialization**: Python API Development & Async Programming

**When to Use**:
- FastAPI application architecture
- Async programming optimization
- API security implementation
- Performance troubleshooting

**Key Capabilities**:
- FastAPI architecture design patterns
- Async/await optimization strategies
- Pydantic model design and validation
- Production deployment best practices

**Available Tools**:
```bash
analyze_fastapi_project    # Project architecture analysis
design_api_architecture    # API design recommendations
optimize_performance       # Performance optimization
review_api_security        # Security assessment
troubleshoot_fastapi_issue # Framework debugging
```

**Example Usage**:
```
"I'm building a FastAPI backend for federal job data processing. Can you help optimize the async performance and database integration?"
```

---

### Google Analytics Specialist
**Specialization**: Web Analytics & Performance Tracking

**When to Use**:
- GA4 implementation and setup
- Custom event tracking
- E-commerce tracking
- Privacy compliance (GDPR/CCPA)

**Key Capabilities**:
- GA4 tracking strategy design
- Custom event and conversion setup
- Privacy-compliant tracking implementation
- Performance analysis and optimization

**Available Tools**:
```bash
design_tracking_strategy      # Analytics strategy design
implement_ga4_tracking        # GA4 implementation
analyze_tracking_performance  # Performance analysis
setup_conversion_tracking     # Conversion setup
troubleshoot_tracking_issues  # Analytics debugging
```

**Example Usage**:
```
"I need to implement comprehensive analytics for my federal job search platform with privacy compliance. How should I set up GA4?"
```

---

## 🔌 Service Integration Specialists

### Stripe Specialist
**Specialization**: Payment Processing & E-commerce

**When to Use**:
- Payment system implementation
- Subscription billing setup
- Webhook security
- Payment optimization

**Key Capabilities**:
- Secure payment flow design
- Webhook implementation and security
- Subscription and billing management
- Payment performance optimization

**Available Tools**:
```bash
design_payment_flow           # Payment flow design
implement_webhooks           # Webhook setup and security
optimize_payment_performance # Conversion optimization
troubleshoot_payment_issues  # Payment debugging
```

**Example Usage**:
```
"I need to implement subscription billing for my federal job coaching service. What's the secure Stripe integration approach?"
```

---

### Sentry Expert
**Specialization**: Error Tracking & Performance Monitoring

**When to Use**:
- Error tracking setup
- Performance monitoring
- Debugging production issues
- Application health monitoring

**Key Capabilities**:
- Comprehensive error tracking configuration
- Performance monitoring setup
- Error pattern analysis and debugging
- Production monitoring strategies

**Available Tools**:
```bash
configure_error_tracking        # Error tracking setup
analyze_error_patterns         # Error analysis
optimize_performance_monitoring # Performance setup
troubleshoot_sentry_integration # Sentry debugging
```

**Example Usage**:
```
"I need to set up comprehensive error tracking for my Next.js and FastAPI applications. How should I configure Sentry?"
```

---

### USAJobs Master
**Specialization**: Federal Job Data & API Integration

**When to Use**:
- USAJobs API integration
- Federal job data processing
- Job search optimization
- API performance tuning

**Key Capabilities**:
- USAJobs API integration expertise
- Federal job data structure understanding
- Advanced search and filtering implementation
- API rate limiting and optimization

**Available Tools**:
```bash
design_job_search_integration # API integration design
optimize_api_performance      # Performance optimization
implement_job_filtering       # Advanced search setup
troubleshoot_api_issues       # API debugging
```

**Example Usage**:
```
"I'm building a federal job aggregator. Can you help optimize the USAJobs API integration for better performance and data quality?"
```

---

### Redis Caching Specialist
**Specialization**: Caching & Performance Optimization

**When to Use**:
- Application performance optimization
- Caching strategy implementation
- Session management
- Database load reduction

**Key Capabilities**:
- Redis caching architecture design
- Cache invalidation strategies
- Performance optimization techniques
- Advanced Redis data structures

**Available Tools**:
```bash
design_caching_strategy    # Caching architecture design
optimize_cache_performance # Performance optimization
implement_cache_patterns   # Advanced caching patterns
troubleshoot_redis_issues  # Redis debugging
```

**Example Usage**:
```
"My federal job search app is slow due to database queries. Can you design a Redis caching strategy to improve performance?"
```

---

### Alembic Migration Specialist
**Specialization**: Database Migration & Schema Management

**When to Use**:
- Database schema migrations
- Migration script optimization
- Schema versioning
- Production migration safety

**Key Capabilities**:
- Safe migration strategy design
- Migration script generation and optimization
- Schema conflict resolution
- Production migration best practices

**Available Tools**:
```bash
design_migration_strategy      # Migration planning
generate_migration_scripts     # Script generation
troubleshoot_migration_issues  # Migration debugging
optimize_migration_performance # Performance optimization
```

**Example Usage**:
```
"I need to migrate my federal job database schema safely in production. Can you help design the migration strategy?"
```

---

### WebAuthn Authentication Specialist
**Specialization**: Passwordless Authentication & Security

**When to Use**:
- Passwordless authentication
- Biometric authentication
- High-security applications
- Modern authentication patterns

**Key Capabilities**:
- WebAuthn flow implementation
- Biometric authentication setup
- Security optimization
- Browser compatibility management

**Available Tools**:
```bash
design_webauthn_flow        # WebAuthn flow design
implement_biometric_auth    # Biometric setup
optimize_auth_security      # Security optimization
troubleshoot_webauthn_issues # WebAuthn debugging
```

**Example Usage**:
```
"I want to implement biometric authentication for secure federal job applications. How should I set up WebAuthn?"
```

---

### Email Service Specialist
**Specialization**: Email Delivery & Marketing Automation

**When to Use**:
- Email service integration
- Deliverability optimization
- Email template design
- Automation workflows

**Key Capabilities**:
- Email service architecture design
- Deliverability rate optimization
- Template and automation setup
- Email reputation management

**Available Tools**:
```bash
design_email_architecture   # Email system design
optimize_deliverability     # Deliverability optimization
implement_email_templates   # Template and automation setup
troubleshoot_email_issues   # Email debugging
```

**Example Usage**:
```
"I need to set up automated email notifications for federal job alerts. What's the best approach for high deliverability?"
```

---

## 🔄 Integration with Fed Job Advisor

### Primary Integration Points

**Core Application Support**:
- `usajobs_master` - Federal job data integration
- `postgres_expert` - Database optimization
- `render_specialist` - Production deployment

**Authentication & Security**:
- `oauth_expert` - Social login implementation
- `webauthn_authentication_specialist` - Passwordless auth
- `sentry_expert` - Security monitoring

**Development Workflow**:
- `nextjs_specialist` - Frontend development
- `fastapi_specialist` - Backend API development
- `github_specialist` - Version control and CI/CD

**Performance & Monitoring**:
- `redis_caching_specialist` - Performance optimization
- `google_analytics_specialist` - User analytics
- `docker_master` - Containerization

### Usage Patterns

**Development Phase**:
1. Repository setup with `github_specialist`
2. Architecture design with `nextjs_specialist` and `fastapi_specialist`
3. Authentication planning with `oauth_expert`
4. Database design with `postgres_expert`

**Implementation Phase**:
1. API integration with `usajobs_master`
2. Payment setup with `stripe_specialist`
3. Caching implementation with `redis_caching_specialist`
4. Analytics setup with `google_analytics_specialist`

**Deployment Phase**:
1. Containerization with `docker_master`
2. Cloud deployment with `render_specialist`
3. Monitoring setup with `sentry_expert`
4. Email automation with `email_service_specialist`

**Maintenance Phase**:
1. Performance monitoring with all monitoring specialists
2. Database migrations with `alembic_migration_specialist`
3. Job scheduling with `cron_architect`
4. Security updates with authentication specialists

---

## 🛠️ How to Use Specialists

### Via Claude Code (Recommended)

Simply mention the specialist and your need:

```
"I need the NextJS Specialist to help optimize my App Router structure for a federal job search application."
```

```
"Can the Stripe Specialist help me implement secure subscription billing for my coaching service?"
```

### Direct MCP Integration

The specialists are available through the MCP server configuration. Each specialist provides specific tools that can be called directly:

```python
# Example: Using GitHub Specialist
result = await github_specialist.analyze_repository_setup({
    "name": "fed-job-advisor",
    "branches": ["main", "develop"],
    "protection": True
})
```

### Environment Setup

Ensure these environment variables are configured:

```bash
# Core services
RENDER_API_TOKEN=your_render_token
POSTGRES_CONNECTION_STRING=your_db_url
USAJOBS_API_KEY=your_usajobs_key

# Authentication
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Monitoring and Analytics
SENTRY_DSN=your_sentry_dsn
GOOGLE_ANALYTICS_ID=your_ga_id

# Infrastructure
REDIS_URL=your_redis_url
DOCKER_REGISTRY=your_registry_url
```

---

## 📚 Documentation Structure

Each specialist maintains comprehensive documentation at:

```
documentation/external_services/{service_name}/
├── manifest.json              # Service metadata
├── official/
│   └── quick_reference.json   # Official API reference
├── best_practices/            # Implementation best practices
├── examples/                  # Code examples
├── fed_job_advisor/          # Project-specific guidance
└── troubleshooting/
    └── common_issues.json    # Known issues and solutions
```

---

## 🚨 Support and Troubleshooting

### Getting Help

1. **Specific Issues**: Use the appropriate specialist's troubleshooting tools
2. **Integration Questions**: Consult the usage patterns above
3. **Performance Issues**: Start with monitoring specialists (Sentry, Analytics)
4. **Security Concerns**: Use authentication and security specialists

### Best Practices

1. **Start Small**: Begin with core specialists (USAJobs, PostgreSQL, Render)
2. **Build Incrementally**: Add specialists as features are needed
3. **Monitor Performance**: Use monitoring specialists early
4. **Maintain Security**: Regular security reviews with auth specialists
5. **Document Integration**: Keep track of which specialists are used where

---

## 📈 Success Metrics

The Service Specialist Registry provides:

✅ **18 Specialized AI Agents** covering all major technology areas  
✅ **70+ Specialized Tools** for deep technical expertise  
✅ **Comprehensive Documentation** for each service integration  
✅ **MCP Integration** for seamless Claude Code usage  
✅ **Production-Ready Guidance** for federal job applications  
✅ **Security-First Approach** with authentication and monitoring focus

**Ready for production use as expert advisors for complex technical implementations!**
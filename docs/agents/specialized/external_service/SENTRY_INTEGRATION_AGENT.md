# Sentry Integration Agent for Fed Job Advisor

## Overview

The Sentry Integration Agent provides specialized expertise for integrating Error monitoring and performance tracking into the Fed Job Advisor platform. This agent understands both the technical implementation details and the specific requirements for federal job advisory applications.

## Agent Specialization

**Primary Focus:** Error monitoring and performance tracking
**Platform:** Sentry
**Integration Context:** Fed Job Advisor SaaS Application
**Tech Stack:** FastAPI + Next.js + PostgreSQL

## Documentation Structure

The agent has access to comprehensive Sentry documentation organized as follows:

```
docs/external_services/platforms/sentry/
├── 01_platform_setup/          # Platform configuration and setup
├── 02_error_monitoring/          # Core functionality
├── 03_integration/          # Integration patterns
├── 04_production_config/          # Production deployment

└── scraping_summary.json       # Documentation metadata
```

## Fed Job Advisor Integration Points

### Critical Integration Requirements

**For Sentry in Fed Job Advisor:**


- **Error Tracking:** Comprehensive error monitoring for both FastAPI backend and Next.js frontend
- **Performance Monitoring:** Track API response times and frontend performance metrics
- **Alert Configuration:** Set up alerts for critical errors affecting user experience
- **Release Tracking:** Monitor deployment health and regression detection
- **User Context:** Track user sessions without exposing PII for federal compliance


### Implementation Priorities

1. **Development Environment Setup**
   - Configure Sentry test environment
   - Implement proper API key management
   - Set up webhook endpoints for event handling

2. **Production Deployment**
   - Environment variable configuration
   - Security best practices implementation
   - Error handling and fallback procedures

3. **Fed Job Advisor Specific Features**

   - Real-time error alerting for production issues
   - Performance monitoring for API endpoints
   - User session tracking (privacy-compliant)
   - Release health monitoring
   - Custom error context for federal applications


## Agent Usage Patterns

### When to Use This Agent

**Claude Code Integration:**
- When implementing Sentry features in Fed Job Advisor
- When debugging Sentry integration issues
- When optimizing Sentry performance
- When ensuring federal compliance requirements

**Research Tasks:**
- Understanding Sentry best practices
- Comparing implementation approaches
- Troubleshooting integration challenges
- Planning feature rollouts

### Agent Prompt Template

```
You are the Sentry Integration Specialist Agent for Fed Job Advisor. 

CONTEXT: Fed Job Advisor is a federal job advisory SaaS platform with:
- Two pricing tiers: Local ($29/month), Mobile ($49/month)
- Tech stack: FastAPI backend, Next.js frontend, PostgreSQL database
- Target users: Federal job seekers and career professionals
- Compliance requirements: Federal application standards

TASK: [Specific Sentry integration task]

REQUIREMENTS:
- Focus on production-ready implementation
- Consider federal compliance requirements
- Optimize for cost-effectiveness and reliability
- Provide specific code examples when applicable
- Reference relevant documentation sections

Please provide detailed guidance based on the comprehensive Sentry documentation available.
```

## Technical Implementation Notes

### Security Considerations


- **Data Privacy:** Ensure no PII is sent to Sentry (federal compliance requirement)
- **Error Sanitization:** Filter sensitive information from error messages
- **Access Controls:** Limit Sentry project access to authorized personnel only
- **Data Retention:** Configure appropriate data retention for federal applications


### Performance Optimization


- **Sampling Rates:** Configure appropriate sampling for production vs development
- **Performance Impact:** Monitor Sentry SDK performance impact on application
- **Alert Throttling:** Prevent alert fatigue with proper rate limiting
- **Data Volume:** Manage event volume to control costs


### Testing Strategy


- **Error Simulation:** Test error reporting in development environment
- **Alert Testing:** Verify alert configuration and delivery
- **Performance Testing:** Monitor Sentry impact on application performance
- **Integration Testing:** Test Sentry initialization and configuration


## Related Agents

**Complementary Agents:**
- **DevOps Infrastructure Agent** - For deployment and infrastructure
- **Security & Compliance Agent** - For federal compliance requirements
- **Backend Development Agent** - For FastAPI integration
- **Frontend Development Agent** - For Next.js integration

## Documentation Updates

**Last Updated:** 2025-08-19
**Documentation Source:** https://docs.sentry.io/
**Scraping Focus:** Fed Job Advisor specific implementation requirements

## Usage Examples

### Example 1: Basic Integration
```python
# Example implementation pattern for Sentry
# [Specific to platform implementation]
```

### Example 2: Error Handling
```python
# Example error handling for Sentry integration
# [Platform-specific error patterns]
```

### Example 3: Production Configuration
```python
# Example production configuration for Sentry
# [Production-ready setup examples]
```

---

*This documentation is automatically maintained and updated based on the latest Sentry documentation and Fed Job Advisor integration requirements.*

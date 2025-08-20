# Platform Integrations Index for Fed Job Advisor

## Overview

This index provides a comprehensive guide to all external platform integrations available for Fed Job Advisor development. Each platform has specialized agent documentation and comprehensive technical references.

## Available Platform Integrations

### Core Business Platforms

**Payment Processing:**
- **[Stripe Integration Agent](./external_service/STRIPE_INTEGRATION_AGENT.md)** - SaaS subscription payment processing
  - Local tier subscriptions ($29/month)
  - Mobile tier subscriptions ($49/month)
  - Customer portal and billing management

**Error Monitoring:**
- **[Sentry Integration Agent](./external_service/SENTRY_INTEGRATION_AGENT.md)** - Production error tracking and performance monitoring
  - Real-time error alerting
  - Performance monitoring
  - Release health tracking

### Documentation Structure

Each platform integration includes:

```
docs/external_services/platforms/[platform]/
├── Platform-specific sections (5-6 categories)
├── Implementation examples and best practices
├── Fed Job Advisor specific configuration
└── scraping_summary.json (metadata)
```

### Integration Workflow

1. **Research Phase:** Use platform-specific agent for requirements analysis
2. **Implementation Phase:** Follow agent-provided implementation guidance
3. **Testing Phase:** Use agent-recommended testing strategies
4. **Production Phase:** Deploy using agent-verified production configurations

### Agent Usage

```bash
# Example: Get Stripe subscription implementation guidance
claude-code: "Which MCP agent should help with Stripe subscription billing?"
→ Route to: Stripe Integration Agent

# Example: Debug Sentry error tracking issues
claude-code: "Which MCP agent should help with Sentry performance monitoring?"
→ Route to: Sentry Integration Agent
```

## Federal Compliance Considerations

All platform integrations include:
- ✅ Federal application compliance requirements
- ✅ Security and privacy considerations
- ✅ Cost optimization for government budgets
- ✅ Audit trail and monitoring capabilities

## Last Updated

**Date:** 2025-08-19
**Platforms Covered:** 2
**Total Documentation Pages:** [To be updated after scraping completion]

---

*This index is automatically maintained based on available platform documentation and Fed Job Advisor integration requirements.*

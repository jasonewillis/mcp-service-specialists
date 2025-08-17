# 📚 External Service Documentation Structure

Each service specialist agent requires comprehensive documentation to maintain deep expertise.

## 📁 Required Documentation Structure

```
documentation/
└── external_services/
    ├── {service_name}/
    │   ├── manifest.json                    # Documentation inventory
    │   ├── official/
    │   │   ├── api_reference.json          # Official API documentation
    │   │   ├── authentication.md           # Auth methods and requirements
    │   │   ├── rate_limits.json            # Rate limiting rules
    │   │   ├── error_codes.json            # Error codes and meanings
    │   │   └── changelog.md                # API version changes
    │   ├── best_practices/
    │   │   ├── security.md                 # Security best practices
    │   │   ├── performance.md              # Performance optimization
    │   │   ├── patterns.json               # Common implementation patterns
    │   │   └── anti_patterns.md            # What NOT to do
    │   ├── examples/
    │   │   ├── basic_setup.{ext}           # Minimal working example
    │   │   ├── production_setup.{ext}      # Production-ready example
    │   │   ├── error_handling.{ext}        # Error handling patterns
    │   │   └── testing.{ext}               # Testing strategies
    │   ├── troubleshooting/
    │   │   ├── common_issues.json          # Known issues and solutions
    │   │   ├── debug_guide.md              # Debugging procedures
    │   │   └── support_contacts.json       # Where to get help
    │   └── fed_job_advisor/
    │       ├── implementation.md           # FJA-specific implementation
    │       ├── configuration.json          # FJA-specific config
    │       └── known_issues.md             # FJA-specific issues
```

## 📋 Manifest File Structure

Each service needs a `manifest.json`:

```json
{
  "service": "stripe",
  "version": "2023-10-16",
  "last_updated": "2024-01-15",
  "documentation_sources": {
    "official_docs": "https://stripe.com/docs",
    "api_reference": "https://stripe.com/docs/api",
    "github": "https://github.com/stripe/stripe-node"
  },
  "critical_concepts": [
    "payment_intents",
    "webhooks",
    "idempotency",
    "sca_compliance"
  ],
  "update_schedule": "monthly",
  "maintainer": "stripe_specialist_agent"
}
```

## 🔄 Documentation Update Process

1. **Automated Checks** - Monthly verification of documentation currency
2. **Change Detection** - Monitor service changelogs
3. **Version Tracking** - Track API versions and deprecations
4. **Testing Updates** - Verify examples still work

## 📊 Priority Documentation by Service

### Render
- Deployment configurations
- Build optimization techniques
- Environment variable management
- Health check patterns
- Scaling strategies

### PostgreSQL
- JSONB operations reference
- Performance tuning guide
- Index strategies
- Backup procedures
- Migration patterns

### Docker
- Dockerfile best practices
- Multi-stage build patterns
- Security hardening
- Network configurations
- Volume management

### CRON/Scheduling
- CRON syntax reference
- Platform-specific issues (macOS, Linux)
- Alternative schedulers
- Error recovery patterns

### Stripe
- API endpoints reference
- Webhook event types
- Testing card numbers
- Compliance requirements
- Pricing models

### Sentry
- SDK configuration options
- Event filtering rules
- Performance monitoring setup
- Integration guides
- Alert configuration

### USAJobs
- API parameter reference
- Field descriptions
- Rate limit rules
- Data extraction patterns
- Known quirks (Fields=Full!)

## 🚀 Quick Start Commands

```bash
# Download official documentation for a service
./scripts/download_docs.sh stripe

# Update all service documentation
./scripts/update_all_docs.sh

# Verify documentation currency
./scripts/verify_docs.sh

# Generate documentation from API specs
./scripts/generate_from_openapi.sh service_name
```

## 📝 Documentation Requirements

Each service documentation must include:

1. **API Reference** - Complete endpoint documentation
2. **Authentication** - How to authenticate requests
3. **Rate Limits** - Request limits and quotas
4. **Error Handling** - Error codes and recovery
5. **Best Practices** - Recommended patterns
6. **Examples** - Working code examples
7. **Troubleshooting** - Common issues and fixes
8. **Version History** - Changes and deprecations

## 🔐 Sensitive Information

**NEVER** store in documentation:
- API keys or secrets
- Customer data
- Internal URLs
- Security vulnerabilities

**DO** store:
- Public endpoints
- Configuration patterns
- Error messages
- Performance metrics

---

*Each specialist agent relies on this documentation to provide instant, accurate expertise*
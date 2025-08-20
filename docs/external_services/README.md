# External Services Documentation

**🎯 Purpose**: Comprehensive documentation for all external services integrated with Fed Job Advisor's MCP agent system.

## 📋 Service Categories

### 🔌 [APIs](./apis/) - External Data Sources

| Service | Domain | Documentation | Status |
|---------|--------|---------------|--------|
| **USAJOBS** | Federal job data | [apis/usajobs/](./apis/usajobs/) | ✅ Active |
| **OPM** | Salary calculations & locality pay | [apis/opm/](./apis/opm/) | ✅ Active |
| **Stripe** | Payment processing | [apis/stripe/](./apis/stripe/) | ✅ Active |

### 🏗️ [Platforms](./platforms/) - Infrastructure Services

| Platform | Domain | Documentation | Status |
|----------|--------|---------------|--------|
| **Docker** | Containerization | [platforms/docker/](./platforms/docker/) | ✅ Active |
| **Render** | Cloud deployment | [platforms/render/](./platforms/render/) | ✅ Active |
| **PostgreSQL** | Database | [platforms/postgresql/](./platforms/postgresql/) | ✅ Active |
| **Sentry** | Error monitoring | [platforms/sentry/](./platforms/sentry/) | ✅ Active |

### 🔗 [Integrations](./integrations/) - Third-Party Services

| Integration | Domain | Documentation | Status |
|-------------|--------|---------------|--------|
| **Slack** | Team notifications | [integrations/slack/](./integrations/slack/) | ✅ Active |
| **Google Analytics** | User analytics | [integrations/google_analytics/](./integrations/google_analytics/) | ✅ Active |
| **OAuth** | Authentication | [integrations/oauth/](./integrations/oauth/) | ✅ Active |

### 📚 [Scraped Documentation](./scraped/) - Official Documentation Mirrors

| Service | Purpose | Location | Last Updated |
|---------|---------|----------|--------------|
| **Docker** | Container best practices | [scraped/docker/](./scraped/docker/) | August 2025 |
| **Slack** | API reference | [scraped/slack/](./scraped/slack/) | August 2025 |

---

## 📊 Documentation Structure

Each service follows a standardized structure:

```
service_name/
├── manifest.json              # Service metadata and version info
├── official/
│   ├── api_reference.json     # Official API documentation
│   ├── quick_reference.json   # Essential endpoints and methods
│   └── authentication.md      # Auth requirements and setup
├── troubleshooting/
│   ├── common_issues.json     # Known issues and solutions
│   └── debug_guide.md         # Debugging procedures
├── best_practices/
│   ├── patterns.json          # Implementation patterns
│   └── security.md            # Security considerations
└── fed_job_advisor/
    ├── implementation.md       # FJA-specific implementation
    ├── configuration.json      # FJA-specific config
    └── known_issues.md         # FJA-specific issues
```

---

## 🚀 Quick Start

### For MCP Agent Development
1. **Review Service Docs**: Check relevant service documentation before agent development
2. **Use Templates**: Follow the standardized structure for new services
3. **Update Manifests**: Keep version information current

### For Integration Work
1. **API Services**: Start with [APIs section](./apis/) for data integration
2. **Platform Services**: Check [Platforms section](./platforms/) for infrastructure
3. **Third-Party Services**: Review [Integrations section](./integrations/) for external tools

### For Troubleshooting
1. **Check Common Issues**: Each service has `troubleshooting/common_issues.json`
2. **Review Debug Guides**: Detailed debugging procedures in each service
3. **Fed Job Advisor Specific**: Check `fed_job_advisor/known_issues.md` for project-specific problems

---

## 🔄 Maintenance Schedule

### Documentation Updates
- **Monthly**: API version checks and manifest updates
- **Quarterly**: Comprehensive documentation review
- **As Needed**: Service changes and new integrations

### Quality Assurance
- **Automated Checks**: Monthly verification of documentation currency
- **Change Detection**: Monitor service changelogs for updates
- **Testing Updates**: Verify examples and configurations still work

---

## 📝 Adding New Services

To add documentation for a new external service:

1. **Create Service Directory**: Follow the standard structure above
2. **Add Manifest File**: Include service metadata and version info
3. **Document Integration**: Add Fed Job Advisor specific implementation details
4. **Update Registry**: Add service to this README
5. **Test Documentation**: Verify all examples and configurations work

---

**🎉 Complete External Service Documentation - Ready for Seamless Integration**

*Structured for maintainability, organized for quick access, validated for accuracy*
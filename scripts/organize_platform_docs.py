#!/usr/bin/env python3
"""
Platform Documentation Organizer for Fed Job Advisor
Ensures Sentry and Stripe documentation is properly integrated into agent documentation structure
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

class PlatformDocsOrganizer:
    """Organizes scraped platform documentation into the proper agent structure"""
    
    def __init__(self):
        self.base_dir = Path("/Users/jasonewillis/Developer/jwRepos/JLWAI/Agents/docs")
        self.platforms = {
            "sentry": {
                "source_dir": self.base_dir / "external_services/platforms/sentry",
                "agent_category": "monitoring_specialist",
                "description": "Error monitoring and performance tracking"
            },
            "stripe": {
                "source_dir": self.base_dir / "external_services/platforms/stripe", 
                "agent_category": "payment_integration",
                "description": "SaaS subscription payment processing"
            }
        }
    
    def create_agent_integration_docs(self):
        """Create integration documentation for each platform"""
        
        for platform, config in self.platforms.items():
            print(f"📋 Creating integration docs for {platform.title()}")
            
            # Create agent-specific integration guide
            agent_dir = self.base_dir / "agents/specialized/external_service"
            agent_dir.mkdir(parents=True, exist_ok=True)
            
            integration_doc = agent_dir / f"{platform.upper()}_INTEGRATION_AGENT.md"
            
            integration_content = self.generate_integration_doc(platform, config)
            
            with open(integration_doc, 'w') as f:
                f.write(integration_content)
            
            print(f"✅ Created {integration_doc}")
    
    def generate_integration_doc(self, platform: str, config: dict) -> str:
        """Generate comprehensive integration documentation"""
        
        platform_title = platform.title()
        
        doc_content = f"""# {platform_title} Integration Agent for Fed Job Advisor

## Overview

The {platform_title} Integration Agent provides specialized expertise for integrating {config['description']} into the Fed Job Advisor platform. This agent understands both the technical implementation details and the specific requirements for federal job advisory applications.

## Agent Specialization

**Primary Focus:** {config['description']}
**Platform:** {platform_title}
**Integration Context:** Fed Job Advisor SaaS Application
**Tech Stack:** FastAPI + Next.js + PostgreSQL

## Documentation Structure

The agent has access to comprehensive {platform_title} documentation organized as follows:

```
docs/external_services/platforms/{platform}/
├── 01_platform_setup/          # Platform configuration and setup
├── 02_{'error_monitoring' if platform == 'sentry' else 'subscription_billing'}/          # Core functionality
├── 03_{'integration' if platform == 'sentry' else 'payment_integration'}/          # Integration patterns
├── 04_{'production_config' if platform == 'sentry' else 'customer_management'}/          # {'Production deployment' if platform == 'sentry' else 'Customer lifecycle'}
{f'├── 05_security_compliance/        # Security and compliance' if platform == 'stripe' else ''}
└── scraping_summary.json       # Documentation metadata
```

## Fed Job Advisor Integration Points

### Critical Integration Requirements

**For {platform_title} in Fed Job Advisor:**

{self.get_platform_specific_requirements(platform)}

### Implementation Priorities

1. **Development Environment Setup**
   - Configure {platform_title} test environment
   - Implement proper API key management
   - Set up webhook endpoints for event handling

2. **Production Deployment**
   - Environment variable configuration
   - Security best practices implementation
   - Error handling and fallback procedures

3. **Fed Job Advisor Specific Features**
{self.get_platform_specific_features(platform)}

## Agent Usage Patterns

### When to Use This Agent

**Claude Code Integration:**
- When implementing {platform_title} features in Fed Job Advisor
- When debugging {platform_title} integration issues
- When optimizing {platform_title} performance
- When ensuring federal compliance requirements

**Research Tasks:**
- Understanding {platform_title} best practices
- Comparing implementation approaches
- Troubleshooting integration challenges
- Planning feature rollouts

### Agent Prompt Template

```
You are the {platform_title} Integration Specialist Agent for Fed Job Advisor. 

CONTEXT: Fed Job Advisor is a federal job advisory SaaS platform with:
- Two pricing tiers: Local ($29/month), Mobile ($49/month)
- Tech stack: FastAPI backend, Next.js frontend, PostgreSQL database
- Target users: Federal job seekers and career professionals
- Compliance requirements: Federal application standards

TASK: [Specific {platform_title} integration task]

REQUIREMENTS:
- Focus on production-ready implementation
- Consider federal compliance requirements
- Optimize for cost-effectiveness and reliability
- Provide specific code examples when applicable
- Reference relevant documentation sections

Please provide detailed guidance based on the comprehensive {platform_title} documentation available.
```

## Technical Implementation Notes

### Security Considerations

{self.get_security_considerations(platform)}

### Performance Optimization

{self.get_performance_notes(platform)}

### Testing Strategy

{self.get_testing_strategy(platform)}

## Related Agents

**Complementary Agents:**
- **DevOps Infrastructure Agent** - For deployment and infrastructure
- **Security & Compliance Agent** - For federal compliance requirements
- **Backend Development Agent** - For FastAPI integration
- **Frontend Development Agent** - For Next.js integration

## Documentation Updates

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Documentation Source:** https://docs.{platform}.{'io' if platform == 'sentry' else 'com'}/
**Scraping Focus:** Fed Job Advisor specific implementation requirements

## Usage Examples

### Example 1: Basic Integration
```python
# Example implementation pattern for {platform_title}
# [Specific to platform implementation]
```

### Example 2: Error Handling
```python
# Example error handling for {platform_title} integration
# [Platform-specific error patterns]
```

### Example 3: Production Configuration
```python
# Example production configuration for {platform_title}
# [Production-ready setup examples]
```

---

*This documentation is automatically maintained and updated based on the latest {platform_title} documentation and Fed Job Advisor integration requirements.*
"""
        
        return doc_content
    
    def get_platform_specific_requirements(self, platform: str) -> str:
        """Get platform-specific requirements"""
        
        if platform == "sentry":
            return """
- **Error Tracking:** Comprehensive error monitoring for both FastAPI backend and Next.js frontend
- **Performance Monitoring:** Track API response times and frontend performance metrics
- **Alert Configuration:** Set up alerts for critical errors affecting user experience
- **Release Tracking:** Monitor deployment health and regression detection
- **User Context:** Track user sessions without exposing PII for federal compliance
"""
        elif platform == "stripe":
            return """
- **Subscription Management:** Handle Local ($29) and Mobile ($49) tier subscriptions
- **Payment Processing:** Secure payment collection with PCI compliance
- **Customer Portal:** Allow users to manage their own subscriptions
- **Webhook Processing:** Handle subscription lifecycle events reliably
- **Billing Compliance:** Meet federal contracting and billing requirements
"""
        
        return ""
    
    def get_platform_specific_features(self, platform: str) -> str:
        """Get platform-specific features"""
        
        if platform == "sentry":
            return """
   - Real-time error alerting for production issues
   - Performance monitoring for API endpoints
   - User session tracking (privacy-compliant)
   - Release health monitoring
   - Custom error context for federal applications
"""
        elif platform == "stripe":
            return """
   - Local tier subscription management ($29/month)
   - Mobile tier subscription management ($49/month)
   - Customer self-service portal
   - Automated billing and invoicing
   - Payment failure handling and recovery
"""
        
        return ""
    
    def get_security_considerations(self, platform: str) -> str:
        """Get security considerations"""
        
        if platform == "sentry":
            return """
- **Data Privacy:** Ensure no PII is sent to Sentry (federal compliance requirement)
- **Error Sanitization:** Filter sensitive information from error messages
- **Access Controls:** Limit Sentry project access to authorized personnel only
- **Data Retention:** Configure appropriate data retention for federal applications
"""
        elif platform == "stripe":
            return """
- **PCI Compliance:** Ensure all payment processing meets PCI DSS requirements
- **API Key Security:** Properly secure and rotate Stripe API keys
- **Webhook Security:** Verify webhook signatures for all incoming events
- **Data Encryption:** Ensure customer payment data is properly encrypted
"""
        
        return ""
    
    def get_performance_notes(self, platform: str) -> str:
        """Get performance considerations"""
        
        if platform == "sentry":
            return """
- **Sampling Rates:** Configure appropriate sampling for production vs development
- **Performance Impact:** Monitor Sentry SDK performance impact on application
- **Alert Throttling:** Prevent alert fatigue with proper rate limiting
- **Data Volume:** Manage event volume to control costs
"""
        elif platform == "stripe":
            return """
- **API Rate Limits:** Respect Stripe API rate limits in high-volume scenarios
- **Webhook Processing:** Ensure webhook endpoints respond quickly (<10 seconds)
- **Idempotency:** Implement proper idempotency for payment operations
- **Connection Pooling:** Use connection pooling for Stripe API calls
"""
        
        return ""
    
    def get_testing_strategy(self, platform: str) -> str:
        """Get testing strategy"""
        
        if platform == "sentry":
            return """
- **Error Simulation:** Test error reporting in development environment
- **Alert Testing:** Verify alert configuration and delivery
- **Performance Testing:** Monitor Sentry impact on application performance
- **Integration Testing:** Test Sentry initialization and configuration
"""
        elif platform == "stripe":
            return """
- **Test Mode:** Use Stripe test mode for all development and testing
- **Webhook Testing:** Test webhook endpoint reliability and error handling
- **Payment Flow Testing:** Test complete subscription signup and payment flows
- **Edge Case Testing:** Test payment failures, network issues, and edge cases
"""
        
        return ""
    
    def verify_documentation_structure(self):
        """Verify that the documentation structure is correct"""
        
        print("🔍 Verifying documentation structure...")
        
        for platform, config in self.platforms.items():
            source_dir = config['source_dir']
            
            if source_dir.exists():
                print(f"✅ {platform.title()} documentation found at: {source_dir}")
                
                # Check for summary file
                summary_file = source_dir / "scraping_summary.json"
                if summary_file.exists():
                    with open(summary_file, 'r') as f:
                        summary = json.load(f)
                    
                    pages_scraped = summary.get('scraping_session', {}).get('total_pages_scraped', 0)
                    print(f"   📊 Pages scraped: {pages_scraped}")
                    
                    # List major sections
                    for item in source_dir.iterdir():
                        if item.is_dir() and not item.name.startswith('.'):
                            print(f"   📁 Section: {item.name}")
                
                else:
                    print(f"   ⚠️  Summary file not found for {platform}")
            else:
                print(f"❌ {platform.title()} documentation not found")
    
    def create_master_integration_index(self):
        """Create a master index of all platform integrations"""
        
        index_file = self.base_dir / "agents/specialized/PLATFORM_INTEGRATIONS_INDEX.md"
        
        index_content = f"""# Platform Integrations Index for Fed Job Advisor

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

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Platforms Covered:** {len(self.platforms)}
**Total Documentation Pages:** [To be updated after scraping completion]

---

*This index is automatically maintained based on available platform documentation and Fed Job Advisor integration requirements.*
"""
        
        # Create directory if needed
        index_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(index_file, 'w') as f:
            f.write(index_content)
        
        print(f"✅ Created master integration index: {index_file}")
    
    def run_organization(self):
        """Run the complete documentation organization process"""
        
        print("🚀 Starting platform documentation organization...")
        
        # Verify structure
        self.verify_documentation_structure()
        
        # Create agent integration docs
        self.create_agent_integration_docs()
        
        # Create master index
        self.create_master_integration_index()
        
        print("\n✅ Platform documentation organization complete!")
        print("\n📋 Summary:")
        print("   • Platform-specific agent documentation created")
        print("   • Integration guides generated")
        print("   • Master platform index created")
        print("   • Ready for Claude Code Ultimate Workflow integration")

if __name__ == "__main__":
    organizer = PlatformDocsOrganizer()
    organizer.run_organization()
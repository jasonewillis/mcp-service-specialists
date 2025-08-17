#!/usr/bin/env python3
"""
Documentation Downloader for Service Specialist Agents
Downloads official documentation from each service's documentation sites
"""

import asyncio
import aiohttp
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import subprocess

class ServiceDocumentationDownloader:
    """
    Downloads official documentation for each external service
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.docs_base = self.base_path / "documentation" / "external_services"
        self.docs_base.mkdir(parents=True, exist_ok=True)
        
        # Service documentation sources - where to find official docs
        self.service_sources = {
            "render": {
                "name": "Render",
                "docs_urls": {
                    "api_reference": "https://api-docs.render.com/reference/introduction",
                    "deployment_guide": "https://render.com/docs/deploy",
                    "environment_variables": "https://render.com/docs/configure-environment-variables",
                    "yaml_spec": "https://render.com/docs/yaml-spec",
                    "databases": "https://render.com/docs/databases"
                },
                "api_base": "https://api.render.com/v1",
                "requires_auth": False
            },
            
            "postgresql": {
                "name": "PostgreSQL",
                "docs_urls": {
                    "manual": "https://www.postgresql.org/docs/15/index.html",
                    "sql_commands": "https://www.postgresql.org/docs/15/sql-commands.html",
                    "performance": "https://www.postgresql.org/docs/15/performance-tips.html",
                    "json": "https://www.postgresql.org/docs/15/datatype-json.html",
                    "indexes": "https://www.postgresql.org/docs/15/indexes.html"
                },
                "requires_auth": False
            },
            
            "docker": {
                "name": "Docker",
                "docs_urls": {
                    "dockerfile_reference": "https://docs.docker.com/engine/reference/builder/",
                    "compose_reference": "https://docs.docker.com/compose/compose-file/",
                    "best_practices": "https://docs.docker.com/develop/dev-best-practices/",
                    "multi_stage": "https://docs.docker.com/build/building/multi-stage/",
                    "security": "https://docs.docker.com/engine/security/"
                },
                "api_base": "https://docs.docker.com/engine/api/v1.43/",
                "requires_auth": False
            },
            
            "stripe": {
                "name": "Stripe",
                "docs_urls": {
                    "api_reference": "https://stripe.com/docs/api",
                    "checkout": "https://stripe.com/docs/payments/checkout",
                    "subscriptions": "https://stripe.com/docs/billing/subscriptions/overview",
                    "webhooks": "https://stripe.com/docs/webhooks",
                    "testing": "https://stripe.com/docs/testing"
                },
                "api_base": "https://api.stripe.com/v1",
                "openapi_spec": "https://github.com/stripe/openapi/raw/master/openapi/spec3.json",
                "requires_auth": True,
                "auth_note": "Requires Stripe account for full API docs"
            },
            
            "sentry": {
                "name": "Sentry",
                "docs_urls": {
                    "platforms": "https://docs.sentry.io/platforms/",
                    "python": "https://docs.sentry.io/platforms/python/",
                    "javascript": "https://docs.sentry.io/platforms/javascript/",
                    "performance": "https://docs.sentry.io/product/performance/",
                    "api_reference": "https://docs.sentry.io/api/"
                },
                "api_base": "https://sentry.io/api/0/",
                "requires_auth": True,
                "auth_note": "Requires Sentry account for API access"
            },
            
            "usajobs": {
                "name": "USAJobs",
                "docs_urls": {
                    "developer_portal": "https://developer.usajobs.gov/",
                    "api_reference": "https://developer.usajobs.gov/API-Reference",
                    "search_api": "https://developer.usajobs.gov/API-Reference/GET-api-Search-jobs",
                    "code_lists": "https://developer.usajobs.gov/API-Reference/GET-api-codelist",
                    "getting_started": "https://developer.usajobs.gov/Getting-Started"
                },
                "api_base": "https://data.usajobs.gov/api",
                "requires_auth": True,
                "auth_note": "Requires API key from login.gov account"
            },
            
            "cron": {
                "name": "CRON/Scheduling",
                "docs_urls": {
                    "crontab_guru": "https://crontab.guru/",
                    "man_page": "https://man7.org/linux/man-pages/man5/crontab.5.html",
                    "launchd": "https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/ScheduledJobs.html",
                    "systemd_timers": "https://www.freedesktop.org/software/systemd/man/systemd.timer.html"
                },
                "requires_auth": False
            },
            
            "github": {
                "name": "GitHub Actions",
                "docs_urls": {
                    "workflow_syntax": "https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions",
                    "contexts": "https://docs.github.com/en/actions/learn-github-actions/contexts",
                    "marketplace": "https://github.com/marketplace?type=actions",
                    "api": "https://docs.github.com/en/rest"
                },
                "api_base": "https://api.github.com",
                "requires_auth": False
            },
            
            "oauth": {
                "name": "OAuth 2.0",
                "docs_urls": {
                    "rfc": "https://datatracker.ietf.org/doc/html/rfc6749",
                    "google_oauth": "https://developers.google.com/identity/protocols/oauth2",
                    "github_oauth": "https://docs.github.com/en/developers/apps/building-oauth-apps",
                    "best_practices": "https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics"
                },
                "requires_auth": False
            },
            
            "nextjs": {
                "name": "Next.js",
                "docs_urls": {
                    "documentation": "https://nextjs.org/docs",
                    "api_reference": "https://nextjs.org/docs/api-reference",
                    "deployment": "https://nextjs.org/docs/deployment",
                    "optimization": "https://nextjs.org/docs/advanced-features/compiler"
                },
                "requires_auth": False
            },
            
            "fastapi": {
                "name": "FastAPI",
                "docs_urls": {
                    "tutorial": "https://fastapi.tiangolo.com/tutorial/",
                    "advanced": "https://fastapi.tiangolo.com/advanced/",
                    "deployment": "https://fastapi.tiangolo.com/deployment/",
                    "async": "https://fastapi.tiangolo.com/async/"
                },
                "openapi_generator": True,
                "requires_auth": False
            },
            
            "google_analytics": {
                "name": "Google Analytics 4",
                "docs_urls": {
                    "developers": "https://developers.google.com/analytics",
                    "measurement_protocol": "https://developers.google.com/analytics/devguides/collection/protocol/ga4",
                    "reporting_api": "https://developers.google.com/analytics/devguides/reporting/data/v1",
                    "gtag": "https://developers.google.com/analytics/devguides/collection/gtagjs"
                },
                "requires_auth": True,
                "auth_note": "Requires Google account for API access"
            }
        }
    
    async def download_service_docs(self, service: str) -> Dict[str, Any]:
        """
        Download documentation for a specific service
        """
        if service not in self.service_sources:
            return {"error": f"Unknown service: {service}"}
        
        service_info = self.service_sources[service]
        service_dir = self.docs_base / service
        service_dir.mkdir(exist_ok=True)
        
        # Create directory structure
        for subdir in ["official", "best_practices", "examples", "troubleshooting", "fed_job_advisor"]:
            (service_dir / subdir).mkdir(exist_ok=True)
        
        results = {
            "service": service,
            "name": service_info["name"],
            "timestamp": datetime.now().isoformat(),
            "downloaded": [],
            "failed": [],
            "requires_auth": service_info.get("requires_auth", False)
        }
        
        # Create manifest
        manifest = self._create_manifest(service, service_info)
        manifest_path = service_dir / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        results["downloaded"].append("manifest.json")
        
        # Download OpenAPI spec if available
        if "openapi_spec" in service_info:
            print(f"📥 Downloading OpenAPI spec for {service}...")
            success = await self._download_openapi_spec(
                service_info["openapi_spec"],
                service_dir / "official" / "openapi.json"
            )
            if success:
                results["downloaded"].append("openapi.json")
            else:
                results["failed"].append("openapi.json")
        
        # Create quick reference guide
        quick_ref = self._create_quick_reference(service, service_info)
        ref_path = service_dir / "official" / "quick_reference.json"
        with open(ref_path, 'w') as f:
            json.dump(quick_ref, f, indent=2)
        results["downloaded"].append("quick_reference.json")
        
        # Create service-specific examples
        examples = self._create_examples(service)
        for example_name, example_code in examples.items():
            example_path = service_dir / "examples" / f"{example_name}.py"
            with open(example_path, 'w') as f:
                f.write(example_code)
            results["downloaded"].append(f"examples/{example_name}.py")
        
        # Create troubleshooting guide
        troubleshooting = self._create_troubleshooting_guide(service)
        trouble_path = service_dir / "troubleshooting" / "common_issues.json"
        with open(trouble_path, 'w') as f:
            json.dump(troubleshooting, f, indent=2)
        results["downloaded"].append("troubleshooting/common_issues.json")
        
        return results
    
    def _create_manifest(self, service: str, service_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create manifest for service"""
        manifest = {
            "service": service,
            "name": service_info["name"],
            "last_updated": datetime.now().isoformat(),
            "documentation_sources": service_info.get("docs_urls", {}),
            "api_base": service_info.get("api_base", ""),
            "requires_auth": service_info.get("requires_auth", False),
            "auth_note": service_info.get("auth_note", ""),
            "critical_concepts": self._get_critical_concepts(service),
            "update_schedule": "weekly",
            "ttl_days": 7
        }
        
        # Add service-specific critical info
        if service == "usajobs":
            manifest["critical_warning"] = "MUST use Fields=Full parameter or lose 93% of data"
        elif service == "stripe":
            manifest["critical_warning"] = "Always verify webhook signatures"
        elif service == "docker":
            manifest["critical_warning"] = "Use multi-stage builds for production"
        
        return manifest
    
    def _get_critical_concepts(self, service: str) -> List[str]:
        """Get critical concepts for each service"""
        concepts = {
            "usajobs": ["Fields=Full parameter", "Rate limiting", "Pagination", "User-Agent email"],
            "stripe": ["Idempotency", "Webhook verification", "PCI compliance", "Test mode"],
            "render": ["Zero-downtime deploy", "Health checks", "Environment groups", "Build hooks"],
            "postgresql": ["JSONB optimization", "Index strategies", "Connection pooling", "VACUUM"],
            "docker": ["Layer caching", "Multi-stage builds", "Security scanning", ".dockerignore"],
            "sentry": ["DSN configuration", "Sampling rates", "PII scrubbing", "Release tracking"],
            "cron": ["Cron syntax", "Environment variables", "Output handling", "macOS issues"],
            "oauth": ["Authorization flow", "PKCE", "Token refresh", "Scope management"],
            "nextjs": ["SSR vs SSG", "API routes", "Image optimization", "Bundle size"],
            "fastapi": ["Async/await", "Dependency injection", "OpenAPI generation", "Middleware"]
        }
        
        return concepts.get(service, [])
    
    def _create_quick_reference(self, service: str, service_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create quick reference guide"""
        return {
            "service": service,
            "common_tasks": self._get_common_tasks(service),
            "code_snippets": self._get_code_snippets(service),
            "urls": service_info.get("docs_urls", {}),
            "api_base": service_info.get("api_base", "")
        }
    
    def _get_common_tasks(self, service: str) -> Dict[str, str]:
        """Get common tasks for each service"""
        tasks = {
            "usajobs": {
                "search_jobs": "GET /api/Search/jobs?Fields=Full&ResultsPerPage=250",
                "get_agencies": "GET /api/codelist/agencysubelements",
                "get_series": "GET /api/codelist/occupationalseries"
            },
            "stripe": {
                "create_checkout": "POST /v1/checkout/sessions",
                "verify_webhook": "stripe.Webhook.construct_event()",
                "create_customer": "POST /v1/customers"
            },
            "docker": {
                "build_image": "docker build -t myapp .",
                "run_container": "docker run -p 8000:8000 myapp",
                "compose_up": "docker-compose up -d"
            }
        }
        
        return tasks.get(service, {})
    
    def _get_code_snippets(self, service: str) -> Dict[str, str]:
        """Get code snippets for each service"""
        snippets = {
            "usajobs": {
                "basic_request": """
headers = {
    'Authorization-Key': API_KEY,
    'User-Agent': 'email@example.com',
    'Host': 'data.usajobs.gov'
}
params = {'Fields': 'Full', 'ResultsPerPage': 250}"""
            },
            "stripe": {
                "webhook_verification": """
event = stripe.Webhook.construct_event(
    payload, sig_header, webhook_secret
)"""
            }
        }
        
        return snippets.get(service, {})
    
    def _create_examples(self, service: str) -> Dict[str, str]:
        """Create example files for each service"""
        examples = {}
        
        if service == "usajobs":
            examples["basic_search"] = """#!/usr/bin/env python3
\"\"\"
USAJobs Basic Search Example
CRITICAL: Always use Fields=Full
\"\"\"

import requests

# Configuration
API_KEY = "YOUR_API_KEY"
USER_AGENT = "your-email@example.com"

# Headers (all required)
headers = {
    'Authorization-Key': API_KEY,
    'User-Agent': USER_AGENT,
    'Host': 'data.usajobs.gov'
}

# Search parameters
params = {
    'Fields': 'Full',  # CRITICAL - Without this, you lose 93% of data!
    'ResultsPerPage': 250,
    'Page': 1,
    'DatePosted': 7,  # Last 7 days
    'LocationName': 'Washington, DC'
}

# Make request
response = requests.get(
    'https://data.usajobs.gov/api/Search/jobs',
    headers=headers,
    params=params
)

if response.status_code == 200:
    data = response.json()
    jobs = data['SearchResult']['SearchResultItems']
    
    # Verify Fields=Full worked
    if jobs and jobs[0].get('MatchedObjectDescriptor', {}).get('UserArea', {}).get('Details'):
        print(f"✅ Successfully retrieved {len(jobs)} jobs with full details")
    else:
        print("❌ WARNING: Missing job details! Check Fields=Full parameter")
else:
    print(f"Error {response.status_code}: {response.text}")
"""
        
        elif service == "stripe":
            examples["basic_checkout"] = """#!/usr/bin/env python3
\"\"\"
Stripe Checkout Session Example
\"\"\"

import stripe
import os

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

# Create checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': 'price_xxxxx',  # Your price ID
        'quantity': 1,
    }],
    mode='subscription',
    success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://example.com/cancel',
    metadata={'user_id': '12345'}
)

print(f"Checkout URL: {session.url}")
"""
        
        elif service == "docker":
            examples["multi_stage"] = """# Multi-stage Dockerfile Example
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
"""
        
        return examples
    
    def _create_troubleshooting_guide(self, service: str) -> Dict[str, Any]:
        """Create troubleshooting guide for each service"""
        guides = {
            "usajobs": {
                "missing_job_details": {
                    "symptom": "Job descriptions are null or empty",
                    "cause": "Not using Fields=Full parameter",
                    "solution": "Add Fields=Full to all API requests",
                    "verification": "Check if UserArea.Details exists in response"
                },
                "rate_limiting": {
                    "symptom": "429 Too Many Requests error",
                    "cause": "Exceeding 30 requests per second",
                    "solution": "Implement rate limiting with asyncio.Semaphore(10)",
                    "verification": "Check Retry-After header in response"
                }
            },
            "stripe": {
                "webhook_signature_invalid": {
                    "symptom": "Webhook signature verification fails",
                    "cause": "Using wrong webhook secret or modified payload",
                    "solution": "Use raw request body and correct endpoint secret",
                    "verification": "Test with Stripe CLI: stripe listen --forward-to localhost:8000/webhook"
                },
                "card_declined": {
                    "symptom": "Payment fails with card_declined",
                    "cause": "Insufficient funds or card issue",
                    "solution": "Handle gracefully and request different payment method",
                    "verification": "Test with test card 4000000000000002"
                }
            },
            "docker": {
                "container_exits_immediately": {
                    "symptom": "Container starts then immediately exits",
                    "cause": "No foreground process or startup error",
                    "solution": "Check logs with docker logs <container> and ensure CMD runs foreground process",
                    "verification": "Run with docker run -it <image> /bin/sh to debug"
                },
                "permission_denied": {
                    "symptom": "Permission denied errors in container",
                    "cause": "File ownership or USER directive issues",
                    "solution": "Set proper ownership with COPY --chown or adjust USER",
                    "verification": "Check with docker exec <container> ls -la"
                }
            }
        }
        
        return guides.get(service, {})
    
    async def _download_openapi_spec(self, url: str, output_path: Path) -> bool:
        """Download OpenAPI specification"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        with open(output_path, 'w') as f:
                            f.write(content)
                        return True
        except Exception as e:
            print(f"❌ Failed to download OpenAPI spec: {e}")
        
        return False
    
    async def download_all_services(self) -> Dict[str, Any]:
        """Download documentation for all services"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "services": {}
        }
        
        for service in self.service_sources.keys():
            print(f"\n📚 Downloading documentation for {service}...")
            service_results = await self.download_service_docs(service)
            results["services"][service] = service_results
            
            if service_results.get("downloaded"):
                print(f"✅ Downloaded {len(service_results['downloaded'])} files for {service}")
            
            if service_results.get("requires_auth"):
                print(f"⚠️  {service} requires authentication for full API docs")
                print(f"   {service_results.get('auth_note', '')}")
        
        # Save summary
        summary_path = self.docs_base / "download_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def verify_documentation_structure(self) -> Dict[str, Any]:
        """Verify all services have proper documentation structure"""
        verification = {
            "timestamp": datetime.now().isoformat(),
            "services": {}
        }
        
        for service in self.service_sources.keys():
            service_dir = self.docs_base / service
            
            service_check = {
                "exists": service_dir.exists(),
                "has_manifest": (service_dir / "manifest.json").exists(),
                "has_official": (service_dir / "official").exists(),
                "has_examples": (service_dir / "examples").exists(),
                "has_troubleshooting": (service_dir / "troubleshooting").exists(),
                "file_count": 0
            }
            
            if service_dir.exists():
                # Count files
                service_check["file_count"] = sum(1 for _ in service_dir.rglob("*") if _.is_file())
            
            verification["services"][service] = service_check
        
        return verification


async def main():
    """Main function to download all documentation"""
    downloader = ServiceDocumentationDownloader()
    
    print("🚀 Fed Job Advisor - Service Documentation Downloader")
    print("=" * 60)
    print("📅 Weekly TTL Pattern - Downloading fresh documentation")
    print("=" * 60)
    
    # Download all documentation
    results = await downloader.download_all_services()
    
    # Verify structure
    print("\n" + "=" * 60)
    print("📊 Verification Report")
    print("=" * 60)
    
    verification = downloader.verify_documentation_structure()
    
    for service, check in verification["services"].items():
        if check["exists"]:
            status = "✅" if check["has_manifest"] else "⚠️"
            print(f"{status} {service}: {check['file_count']} files")
        else:
            print(f"❌ {service}: Not downloaded")
    
    print("\n" + "=" * 60)
    print("📍 Documentation Location:")
    print(f"   {downloader.docs_base}")
    print("\n💡 Documentation will auto-refresh weekly (7-day TTL)")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
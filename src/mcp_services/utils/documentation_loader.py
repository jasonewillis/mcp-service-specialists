#!/usr/bin/env python3
"""
Documentation Loader Utility for Service Specialist Agents
Loads and caches external service documentation for agent knowledge bases
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
import pickle

class DocumentationLoader:
    """
    Loads and manages external service documentation for specialist agents
    """
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / service_name
        self.cache_path = self.base_path / ".cache" / "docs" / service_name
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Cache TTL (Time To Live) in days - Weekly refresh pattern
        self.cache_ttl = {
            "official": 7,     # Official docs cached for 1 week
            "examples": 7,     # Examples refreshed weekly
            "manifest": 7,     # Manifest checked weekly
            "api_reference": 7,     # API reference refreshed weekly
            "best_practices": 7,    # Best practices refreshed weekly
            "troubleshooting": 7    # Troubleshooting guides refreshed weekly
        }
        
        self._documentation_cache = {}
    
    def load_manifest(self) -> Dict[str, Any]:
        """Load service manifest with critical information"""
        manifest_file = self.docs_path / "manifest.json"
        
        if not manifest_file.exists():
            return self._create_default_manifest()
        
        # Check cache
        cached = self._get_cached("manifest")
        if cached:
            return cached
        
        try:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
                self._set_cached("manifest", manifest)
                return manifest
        except Exception as e:
            print(f"Error loading manifest: {e}")
            return self._create_default_manifest()
    
    def load_api_reference(self) -> Dict[str, Any]:
        """Load API reference documentation"""
        api_ref_file = self.docs_path / "official" / "api_reference.json"
        
        # Check cache
        cached = self._get_cached("api_reference")
        if cached:
            return cached
        
        if api_ref_file.exists():
            try:
                with open(api_ref_file, 'r') as f:
                    api_ref = json.load(f)
                    self._set_cached("api_reference", api_ref)
                    return api_ref
            except Exception as e:
                print(f"Error loading API reference: {e}")
        
        # Return embedded knowledge if no file
        return self._get_embedded_api_reference()
    
    def load_best_practices(self) -> Dict[str, Any]:
        """Load best practices documentation"""
        practices_file = self.docs_path / "best_practices" / "patterns.json"
        
        # Check cache
        cached = self._get_cached("best_practices")
        if cached:
            return cached
        
        if practices_file.exists():
            try:
                with open(practices_file, 'r') as f:
                    practices = json.load(f)
                    self._set_cached("best_practices", practices)
                    return practices
            except Exception as e:
                print(f"Error loading best practices: {e}")
        
        return self._get_embedded_best_practices()
    
    def load_troubleshooting(self) -> Dict[str, Any]:
        """Load troubleshooting guide"""
        troubleshooting_file = self.docs_path / "troubleshooting" / "common_issues.json"
        
        # Check cache
        cached = self._get_cached("troubleshooting")
        if cached:
            return cached
        
        if troubleshooting_file.exists():
            try:
                with open(troubleshooting_file, 'r') as f:
                    troubleshooting = json.load(f)
                    self._set_cached("troubleshooting", troubleshooting)
                    return troubleshooting
            except Exception as e:
                print(f"Error loading troubleshooting: {e}")
        
        return self._get_embedded_troubleshooting()
    
    def load_examples(self) -> Dict[str, str]:
        """Load code examples"""
        examples_dir = self.docs_path / "examples"
        examples = {}
        
        # Check cache
        cached = self._get_cached("examples")
        if cached:
            return cached
        
        if examples_dir.exists():
            for example_file in examples_dir.glob("*"):
                if example_file.is_file():
                    try:
                        with open(example_file, 'r') as f:
                            examples[example_file.stem] = f.read()
                    except Exception as e:
                        print(f"Error loading example {example_file}: {e}")
        
        if examples:
            self._set_cached("examples", examples)
        
        return examples if examples else self._get_embedded_examples()
    
    def load_fed_job_advisor_config(self) -> Dict[str, Any]:
        """Load Fed Job Advisor specific configuration"""
        config_file = self.docs_path / "fed_job_advisor" / "configuration.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading FJA config: {e}")
        
        return {}
    
    def check_documentation_currency(self) -> Dict[str, Any]:
        """Check if documentation is up to date"""
        manifest = self.load_manifest()
        last_updated = manifest.get("last_updated", "unknown")
        
        if last_updated != "unknown":
            try:
                last_date = datetime.fromisoformat(last_updated)
                days_old = (datetime.now() - last_date).days
                
                return {
                    "current": days_old < 30,
                    "days_old": days_old,
                    "last_updated": last_updated,
                    "needs_update": days_old > 90
                }
            except:
                pass
        
        return {
            "current": False,
            "days_old": -1,
            "last_updated": "unknown",
            "needs_update": True
        }
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached documentation if still valid"""
        cache_file = self.cache_path / f"{key}.cache"
        
        if not cache_file.exists():
            return None
        
        try:
            # Check cache age
            cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
            ttl_days = self.cache_ttl.get(key.split('_')[0], 7)
            
            if cache_age.days > ttl_days:
                return None
            
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except:
            return None
    
    def _set_cached(self, key: str, data: Any) -> None:
        """Cache documentation data"""
        cache_file = self.cache_path / f"{key}.cache"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Error caching {key}: {e}")
    
    def _create_default_manifest(self) -> Dict[str, Any]:
        """Create default manifest if none exists"""
        return {
            "service": self.service_name,
            "version": "unknown",
            "last_updated": datetime.now().isoformat(),
            "documentation_sources": {},
            "critical_concepts": [],
            "warning": "No manifest found - using defaults"
        }
    
    def _get_embedded_api_reference(self) -> Dict[str, Any]:
        """Get embedded API reference for known services"""
        # This would contain hardcoded API references for critical services
        embedded_refs = {
            "usajobs": {
                "base_url": "https://data.usajobs.gov/api",
                "endpoints": {
                    "search": "/Search/jobs",
                    "codelist": "/codelist"
                },
                "critical": "MUST use Fields=Full"
            },
            "stripe": {
                "base_url": "https://api.stripe.com/v1",
                "endpoints": {
                    "checkout": "/checkout/sessions",
                    "customers": "/customers",
                    "subscriptions": "/subscriptions"
                }
            },
            "render": {
                "base_url": "https://api.render.com/v1",
                "endpoints": {
                    "services": "/services",
                    "deploys": "/deploys"
                }
            }
        }
        
        return embedded_refs.get(self.service_name, {})
    
    def _get_embedded_best_practices(self) -> Dict[str, Any]:
        """Get embedded best practices for known services"""
        practices = {
            "usajobs": {
                "always": ["Use Fields=Full", "Include User-Agent email", "Handle pagination"],
                "never": ["Exceed rate limits", "Ignore Retry-After", "Use Fields=Min"],
                "performance": ["Batch requests", "Cache code lists", "Use date ranges"]
            },
            "stripe": {
                "always": ["Verify webhooks", "Use idempotency keys", "Handle errors gracefully"],
                "never": ["Store card details", "Log sensitive data", "Hardcode API keys"],
                "security": ["Use Stripe Elements", "Implement SCA", "PCI compliance"]
            }
        }
        
        return practices.get(self.service_name, {})
    
    def _get_embedded_troubleshooting(self) -> Dict[str, Any]:
        """Get embedded troubleshooting for known services"""
        troubleshooting = {
            "usajobs": {
                "missing_data": {
                    "cause": "Not using Fields=Full",
                    "solution": "Add Fields=Full to all requests"
                },
                "rate_limit": {
                    "cause": "Too many requests",
                    "solution": "Implement exponential backoff"
                }
            },
            "stripe": {
                "webhook_failure": {
                    "cause": "Invalid signature",
                    "solution": "Check webhook secret and use raw body"
                },
                "payment_declined": {
                    "cause": "Card issue",
                    "solution": "Handle card errors gracefully"
                }
            }
        }
        
        return troubleshooting.get(self.service_name, {})
    
    def _get_embedded_examples(self) -> Dict[str, str]:
        """Get embedded code examples for known services"""
        examples = {
            "usajobs": {
                "basic_search": """
import requests

headers = {
    'Authorization-Key': 'YOUR_KEY',
    'User-Agent': 'your-email@example.com',
    'Host': 'data.usajobs.gov'
}

params = {
    'Fields': 'Full',  # CRITICAL!
    'ResultsPerPage': 250,
    'Page': 1
}

response = requests.get(
    'https://data.usajobs.gov/api/Search/jobs',
    headers=headers,
    params=params
)
"""
            }
        }
        
        return examples.get(self.service_name, {})
    
    def get_all_documentation(self) -> Dict[str, Any]:
        """Load all documentation for a service"""
        return {
            "manifest": self.load_manifest(),
            "api_reference": self.load_api_reference(),
            "best_practices": self.load_best_practices(),
            "troubleshooting": self.load_troubleshooting(),
            "examples": self.load_examples(),
            "fed_job_advisor": self.load_fed_job_advisor_config(),
            "currency": self.check_documentation_currency()
        }


# Mixin for agents to inherit documentation loading
class DocumentedAgent:
    """
    Mixin class for agents to automatically load service documentation
    """
    
    def __init__(self, service_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_name = service_name
        self.doc_loader = DocumentationLoader(service_name)
        self.documentation = None
        self._load_documentation()
    
    def _load_documentation(self):
        """Load all service documentation"""
        self.documentation = self.doc_loader.get_all_documentation()
        
        # Warn if documentation is out of date
        currency = self.documentation.get("currency", {})
        if currency.get("needs_update"):
            print(f"WARNING: {self.service_name} documentation is {currency.get('days_old', 'unknown')} days old")
    
    def refresh_documentation(self):
        """Refresh documentation from disk"""
        self._load_documentation()
    
    def get_critical_info(self) -> Dict[str, Any]:
        """Get critical service information"""
        manifest = self.documentation.get("manifest", {})
        return {
            "service": self.service_name,
            "version": manifest.get("api_version", "unknown"),
            "critical_warning": manifest.get("critical_warning"),
            "critical_concepts": manifest.get("critical_concepts", [])
        }


if __name__ == "__main__":
    # Test documentation loading
    import sys
    
    if len(sys.argv) > 1:
        service = sys.argv[1]
        loader = DocumentationLoader(service)
        
        print(f"Loading documentation for {service}...")
        docs = loader.get_all_documentation()
        
        print(f"\nManifest: {json.dumps(docs['manifest'], indent=2)[:500]}...")
        print(f"\nCurrency: {docs['currency']}")
        print(f"\nCritical concepts: {docs['manifest'].get('critical_concepts', [])}")
    else:
        print("Usage: python documentation_loader.py <service_name>")
        print("Available services: usajobs, stripe, render, postgresql, docker, cron, sentry")
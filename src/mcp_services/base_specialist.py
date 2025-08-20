#!/usr/bin/env python3
"""
Base Specialist Agent with TTL Documentation Management
All service specialist agents inherit from this base class
"""

from pathlib import Path
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
import pickle
from abc import ABC, abstractmethod

class ServiceSpecialistBase(ABC):
    """
    Base class for all service specialist agents with TTL documentation management
    Weekly refresh pattern for all documentation
    """
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.base_path = Path(__file__).parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / service_name
        self.cache_path = self.base_path / ".cache" / "docs" / service_name
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.research_output = self.base_path / "research_outputs" / f"{service_name}_outputs"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Universal TTL pattern - 1 week for everything
        self.cache_ttl_days = 7  # All documentation refreshes weekly
        
        # Load documentation and knowledge base
        self.documentation = self._load_all_documentation()
        self.knowledge_base = self._initialize_knowledge_base()
        
        # Check documentation freshness
        self._check_documentation_freshness()
    
    def _load_all_documentation(self) -> Dict[str, Any]:
        """Load all documentation with TTL caching"""
        docs = {}
        
        # Check if cached documentation exists and is fresh
        cache_file = self.cache_path / "complete_docs.cache"
        
        if self._is_cache_fresh(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    docs = pickle.load(f)
                    print(f"📚 Loaded cached {self.service_name} documentation (TTL: {self.cache_ttl_days} days)")
                    return docs
            except Exception as e:
                print(f"⚠️ Cache load failed: {e}, refreshing documentation...")
        
        # Load fresh documentation
        print(f"🔄 Refreshing {self.service_name} documentation (weekly TTL expired or cache missing)")
        
        docs = {
            "manifest": self._load_manifest(),
            "api_reference": self._load_api_reference(),
            "best_practices": self._load_best_practices(),
            "troubleshooting": self._load_troubleshooting(),
            "examples": self._load_examples(),
            "fed_job_advisor": self._load_fed_job_advisor_config(),
            "last_refreshed": datetime.now().isoformat()
        }
        
        # Cache the complete documentation
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(docs, f)
                print(f"💾 Cached {self.service_name} documentation (expires in 7 days)")
        except Exception as e:
            print(f"⚠️ Failed to cache documentation: {e}")
        
        return docs
    
    def _is_cache_fresh(self, cache_file: Path) -> bool:
        """Check if cache is within TTL period (1 week)"""
        if not cache_file.exists():
            return False
        
        try:
            cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
            is_fresh = cache_age.days < self.cache_ttl_days
            
            if not is_fresh:
                print(f"📅 Cache expired: {cache_age.days} days old (TTL: {self.cache_ttl_days} days)")
            
            return is_fresh
        except:
            return False
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load service manifest"""
        manifest_file = self.docs_path / "manifest.json"
        
        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading manifest: {e}")
        
        # Return default manifest with embedded knowledge
        return self._get_default_manifest()
    
    def _load_api_reference(self) -> Dict[str, Any]:
        """Load API reference documentation"""
        api_file = self.docs_path / "official" / "api_reference.json"
        
        if api_file.exists():
            try:
                with open(api_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Return embedded API reference
        return self._get_embedded_api_reference()
    
    def _load_best_practices(self) -> Dict[str, Any]:
        """Load best practices"""
        practices_file = self.docs_path / "best_practices" / "patterns.json"
        
        if practices_file.exists():
            try:
                with open(practices_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return self._get_embedded_best_practices()
    
    def _load_troubleshooting(self) -> Dict[str, Any]:
        """Load troubleshooting guide"""
        troubleshooting_file = self.docs_path / "troubleshooting" / "common_issues.json"
        
        if troubleshooting_file.exists():
            try:
                with open(troubleshooting_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return self._get_embedded_troubleshooting()
    
    def _load_examples(self) -> Dict[str, str]:
        """Load code examples"""
        examples_dir = self.docs_path / "examples"
        examples = {}
        
        if examples_dir.exists():
            for example_file in examples_dir.glob("*"):
                if example_file.is_file():
                    try:
                        with open(example_file, 'r') as f:
                            examples[example_file.stem] = f.read()
                    except:
                        pass
        
        return examples if examples else self._get_embedded_examples()
    
    def _load_fed_job_advisor_config(self) -> Dict[str, Any]:
        """Load Fed Job Advisor specific configuration"""
        config_file = self.docs_path / "fed_job_advisor" / "configuration.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {}
    
    def _check_documentation_freshness(self):
        """Check if documentation needs updating (weekly check)"""
        last_refreshed = self.documentation.get("last_refreshed")
        
        if last_refreshed:
            try:
                refresh_date = datetime.fromisoformat(last_refreshed)
                days_old = (datetime.now() - refresh_date).days
                
                if days_old >= self.cache_ttl_days:
                    print(f"⚠️ {self.service_name} documentation is {days_old} days old (TTL: {self.cache_ttl_days} days)")
                    print(f"   Run refresh_documentation() to update")
                else:
                    print(f"✅ {self.service_name} documentation is fresh ({days_old}/{self.cache_ttl_days} days)")
            except:
                pass
    
    def refresh_documentation(self):
        """Force refresh of all documentation (clears cache)"""
        print(f"🔄 Force refreshing {self.service_name} documentation...")
        
        # Clear cache
        cache_file = self.cache_path / "complete_docs.cache"
        if cache_file.exists():
            cache_file.unlink()
            print(f"🗑️ Cleared cache for {self.service_name}")
        
        # Reload documentation
        self.documentation = self._load_all_documentation()
        self.knowledge_base = self._initialize_knowledge_base()
        
        print(f"✅ {self.service_name} documentation refreshed")
    
    def get_critical_info(self) -> Dict[str, Any]:
        """Get critical service information"""
        manifest = self.documentation.get("manifest", {})
        return {
            "service": self.service_name,
            "version": manifest.get("api_version", "unknown"),
            "critical_warning": manifest.get("critical_warning"),
            "critical_concepts": manifest.get("critical_concepts", []),
            "last_refreshed": self.documentation.get("last_refreshed"),
            "ttl_days": self.cache_ttl_days
        }
    
    def get_documentation_status(self) -> Dict[str, Any]:
        """Get documentation status and TTL info"""
        last_refreshed = self.documentation.get("last_refreshed")
        
        status = {
            "service": self.service_name,
            "ttl_days": self.cache_ttl_days,
            "last_refreshed": last_refreshed,
            "documentation_loaded": bool(self.documentation),
            "has_manifest": bool(self.documentation.get("manifest")),
            "has_api_reference": bool(self.documentation.get("api_reference")),
            "has_examples": bool(self.documentation.get("examples"))
        }
        
        if last_refreshed:
            try:
                refresh_date = datetime.fromisoformat(last_refreshed)
                days_old = (datetime.now() - refresh_date).days
                days_remaining = self.cache_ttl_days - days_old
                
                status["days_since_refresh"] = days_old
                status["days_until_expiry"] = max(0, days_remaining)
                status["needs_refresh"] = days_old >= self.cache_ttl_days
            except:
                pass
        
        return status
    
    # Abstract methods that each specialist must implement
    @abstractmethod
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize service-specific knowledge base"""
        pass
    
    @abstractmethod
    def _get_default_manifest(self) -> Dict[str, Any]:
        """Get default manifest with embedded critical knowledge"""
        pass
    
    @abstractmethod
    def _get_embedded_api_reference(self) -> Dict[str, Any]:
        """Get embedded API reference"""
        pass
    
    @abstractmethod
    def _get_embedded_best_practices(self) -> Dict[str, Any]:
        """Get embedded best practices"""
        pass
    
    @abstractmethod
    def _get_embedded_troubleshooting(self) -> Dict[str, Any]:
        """Get embedded troubleshooting guide"""
        pass
    
    @abstractmethod
    def _get_embedded_examples(self) -> Dict[str, str]:
        """Get embedded code examples"""
        pass


class DocumentationTTLManager:
    """
    Manages TTL for all service documentation
    Ensures weekly refresh pattern across all agents
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.cache_base = self.base_path / ".cache" / "docs"
        self.ttl_days = 7  # Universal 1-week TTL
        
    def check_all_services(self) -> Dict[str, Dict[str, Any]]:
        """Check TTL status for all services"""
        status = {}
        
        if self.cache_base.exists():
            for service_dir in self.cache_base.iterdir():
                if service_dir.is_dir():
                    service_name = service_dir.name
                    cache_file = service_dir / "complete_docs.cache"
                    
                    if cache_file.exists():
                        try:
                            age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
                            status[service_name] = {
                                "cached": True,
                                "age_days": age.days,
                                "expired": age.days >= self.ttl_days,
                                "expires_in_days": max(0, self.ttl_days - age.days)
                            }
                        except:
                            status[service_name] = {"cached": False}
                    else:
                        status[service_name] = {"cached": False}
        
        return status
    
    def clear_expired_caches(self) -> List[str]:
        """Clear all expired caches (older than 1 week)"""
        cleared = []
        
        if self.cache_base.exists():
            for service_dir in self.cache_base.iterdir():
                if service_dir.is_dir():
                    cache_file = service_dir / "complete_docs.cache"
                    
                    if cache_file.exists():
                        try:
                            age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
                            if age.days >= self.ttl_days:
                                cache_file.unlink()
                                cleared.append(service_dir.name)
                                print(f"🗑️ Cleared expired cache for {service_dir.name} ({age.days} days old)")
                        except:
                            pass
        
        return cleared
    
    def force_refresh_all(self) -> List[str]:
        """Force refresh all service documentation"""
        refreshed = []
        
        if self.cache_base.exists():
            for service_dir in self.cache_base.iterdir():
                if service_dir.is_dir():
                    cache_file = service_dir / "complete_docs.cache"
                    
                    if cache_file.exists():
                        try:
                            cache_file.unlink()
                            refreshed.append(service_dir.name)
                            print(f"🔄 Force refreshed {service_dir.name}")
                        except:
                            pass
        
        return refreshed


if __name__ == "__main__":
    # Test TTL management
    manager = DocumentationTTLManager()
    
    print("📊 Documentation TTL Status (1-week refresh cycle)")
    print("=" * 50)
    
    status = manager.check_all_services()
    
    if not status:
        print("No cached documentation found")
    else:
        for service, info in status.items():
            if info.get("cached"):
                expired = "❌ EXPIRED" if info["expired"] else "✅ FRESH"
                print(f"{service}: {expired} - {info['age_days']} days old (expires in {info['expires_in_days']} days)")
            else:
                print(f"{service}: No cache")
    
    print("\n🔄 Clearing expired caches...")
    cleared = manager.clear_expired_caches()
    if cleared:
        print(f"Cleared: {', '.join(cleared)}")
    else:
        print("No expired caches to clear")
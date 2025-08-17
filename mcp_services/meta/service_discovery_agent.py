#!/usr/bin/env python3
"""
Service Discovery Agent - Scans codebase for unhandled external services
Uses qwen2.5-coder:7b for pattern recognition (94% success rate)
"""

from pathlib import Path
import json
import re
from datetime import datetime
from typing import Dict, Any, List, Set
import asyncio

class ServiceDiscoveryAgent:
    """
    Continuously scans Fed Job Advisor codebase for external service references
    Identifies services that need dedicated researcher agents
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent.parent.parent  # Go to fedJobAdvisor root
        self.research_output = self.base_path / "_Management" / "_PM" / "_Tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Known service patterns to detect
        self.service_patterns = {
            # Environment variable patterns
            "env_vars": [
                r'(\w+)_API_KEY',
                r'(\w+)_SECRET',
                r'(\w+)_CLIENT_ID',
                r'(\w+)_DSN',
                r'(\w+)_WEBHOOK_URL',
                r'(\w+)_ACCESS_TOKEN'
            ],
            # Import patterns
            "imports": [
                r'from\s+(\w+)\s+import',
                r'import\s+(\w+)',
                r'@(\w+)/\w+',  # npm packages
                r'pip\s+install\s+(\w+)'
            ],
            # URL patterns
            "urls": [
                r'https?://api\.(\w+)\.com',
                r'https?://(\w+)\.googleapis\.com',
                r'https?://hooks\.slack\.com',
                r'https?://sentry\.io',
                r'wss?://(\w+)\.com'
            ],
            # Configuration patterns
            "configs": [
                r'(\w+)Config',
                r'(\w+)Client',
                r'(\w+)Service',
                r'init(\w+)',
                r'setup(\w+)'
            ]
        }
        
        # Known services to exclude (already handled)
        self.existing_services = {
            'stripe', 'google', 'oauth', 'render', 'opm', 'usajobs', 
            'sentry', 'slack', 'analytics', 'nextjs', 'fastapi', 'postgresql'
        }
        
        # Service categories
        self.service_categories = {
            'payment': ['stripe', 'paypal', 'square'],
            'auth': ['auth0', 'firebase', 'cognito', 'oauth'],
            'monitoring': ['sentry', 'datadog', 'newrelic', 'rollbar'],
            'communication': ['slack', 'discord', 'twilio', 'sendgrid'],
            'analytics': ['google', 'mixpanel', 'amplitude', 'segment'],
            'cloud': ['aws', 'azure', 'gcp', 'cloudflare'],
            'database': ['mongo', 'redis', 'elasticsearch', 'supabase'],
            'ai': ['openai', 'anthropic', 'huggingface', 'cohere']
        }
        
        self.model = "qwen2.5-coder:7b"
    
    async def scan_codebase(self) -> Dict[str, Any]:
        """Scan entire Fed Job Advisor codebase for service references"""
        
        discovered_services = set()
        scan_results = {
            "env_vars": [],
            "imports": [],
            "urls": [],
            "configs": []
        }
        
        # Scan different parts of codebase
        scan_paths = [
            self.base_path / "frontend",
            self.base_path / "backend", 
            self.base_path / "scripts",
            self.base_path / "_Management"
        ]
        
        for path in scan_paths:
            if path.exists():
                await self._scan_directory(path, discovered_services, scan_results)
        
        # Categorize discovered services
        categorized = self._categorize_services(discovered_services)
        
        # Identify which need agents
        missing_agents = await self._identify_missing_agents(categorized)
        
        return {
            "discovered_services": list(discovered_services),
            "categorized": categorized,
            "missing_agents": missing_agents,
            "scan_results": scan_results,
            "scan_timestamp": datetime.now().isoformat()
        }
    
    async def _scan_directory(self, directory: Path, services: Set[str], results: Dict) -> None:
        """Recursively scan directory for service references"""
        
        # File types to scan
        extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.md', '.env', '.yaml', '.yml'}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                await self._scan_file(file_path, services, results)
    
    async def _scan_file(self, file_path: Path, services: Set[str], results: Dict) -> None:
        """Scan individual file for service references"""
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Scan for each pattern type
            for pattern_type, patterns in self.service_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match[0]  # Extract from tuple
                        
                        service_name = match.lower().strip()
                        
                        # Filter out common false positives
                        if self._is_valid_service(service_name):
                            services.add(service_name)
                            results[pattern_type].append({
                                "service": service_name,
                                "file": str(file_path.relative_to(self.base_path)),
                                "pattern": pattern,
                                "context": self._extract_context(content, match)
                            })
        
        except Exception as e:
            # Skip files that can't be read
            pass
    
    def _is_valid_service(self, service_name: str) -> bool:
        """Check if discovered name is likely a real service"""
        
        # Filter out common false positives
        false_positives = {
            'os', 'sys', 'json', 'path', 'date', 'time', 'user', 'data',
            'config', 'util', 'helper', 'test', 'main', 'app', 'api',
            'db', 'client', 'server', 'local', 'dev', 'prod', 'env'
        }
        
        return (
            len(service_name) > 2 and
            service_name not in false_positives and
            not service_name.isdigit() and
            service_name.isalpha()
        )
    
    def _extract_context(self, content: str, match: str) -> str:
        """Extract context around the match"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if match in line:
                # Return surrounding lines for context
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                return ' | '.join(lines[start:end])
        return ""
    
    def _categorize_services(self, services: Set[str]) -> Dict[str, List[str]]:
        """Categorize discovered services"""
        
        categorized = {category: [] for category in self.service_categories.keys()}
        categorized['unknown'] = []
        
        for service in services:
            categorized_service = False
            
            for category, keywords in self.service_categories.items():
                if any(keyword in service.lower() for keyword in keywords):
                    categorized[category].append(service)
                    categorized_service = True
                    break
            
            if not categorized_service:
                categorized['unknown'].append(service)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    async def _identify_missing_agents(self, categorized: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Identify which services need dedicated agents"""
        
        missing_agents = []
        agents_path = Path(__file__).parent.parent
        
        for category, services in categorized.items():
            for service in services:
                if service not in self.existing_services:
                    # Check if agent already exists
                    potential_paths = [
                        agents_path / "external" / f"{service}_researcher.py",
                        agents_path / "federal" / f"{service}_researcher.py",
                        agents_path / "tech" / f"{service}_researcher.py"
                    ]
                    
                    if not any(path.exists() for path in potential_paths):
                        missing_agents.append({
                            "service": service,
                            "category": category,
                            "priority": self._assess_priority(service, category),
                            "complexity": self._assess_complexity(service),
                            "reason": f"Found {service} references in codebase without dedicated agent"
                        })
        
        return sorted(missing_agents, key=lambda x: self._priority_score(x['priority']), reverse=True)
    
    def _assess_priority(self, service: str, category: str) -> str:
        """Assess priority level for missing agent"""
        
        high_priority_categories = {'payment', 'auth', 'monitoring'}
        critical_services = {'stripe', 'sentry', 'auth0', 'google'}
        
        if service in critical_services:
            return 'critical'
        elif category in high_priority_categories:
            return 'high'
        elif category in {'analytics', 'communication'}:
            return 'medium'
        else:
            return 'low'
    
    def _assess_complexity(self, service: str) -> str:
        """Assess implementation complexity"""
        
        complex_services = {'auth0', 'aws', 'azure', 'openai'}
        simple_services = {'slack', 'webhook', 'sendgrid'}
        
        if service in complex_services:
            return 'complex'
        elif service in simple_services:
            return 'simple'
        else:
            return 'medium'
    
    def _priority_score(self, priority: str) -> int:
        """Convert priority to numeric score for sorting"""
        return {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}.get(priority, 0)
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research service discovery and missing agents"""
        
        scan_results = await self.scan_codebase()
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "scan_summary": {
                "total_services": len(scan_results["discovered_services"]),
                "missing_agents": len(scan_results["missing_agents"]),
                "categories": list(scan_results["categorized"].keys())
            },
            "discovery_results": scan_results,
            "recommendations": self._generate_recommendations(scan_results)
        }
        
        report_path = self._save_discovery_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": f"Discovered {research['scan_summary']['total_services']} services, {research['scan_summary']['missing_agents']} need agents",
            "missing_agents": scan_results["missing_agents"][:3]  # Top 3
        }
    
    def _generate_recommendations(self, scan_results: Dict) -> List[str]:
        """Generate recommendations based on scan results"""
        
        recommendations = []
        
        if scan_results["missing_agents"]:
            critical_missing = [a for a in scan_results["missing_agents"] if a['priority'] == 'critical']
            if critical_missing:
                recommendations.append(f"🚨 Generate {len(critical_missing)} critical missing agents immediately")
            
            high_missing = [a for a in scan_results["missing_agents"] if a['priority'] == 'high']
            if high_missing:
                recommendations.append(f"⚠️ Generate {len(high_missing)} high priority agents for Q1 launch")
        
        if len(scan_results["discovered_services"]) > 20:
            recommendations.append("📊 Large service footprint - consider consolidation")
        
        if 'unknown' in scan_results["categorized"]:
            recommendations.append(f"🔍 Investigate {len(scan_results['categorized']['unknown'])} unknown services")
        
        return recommendations
    
    def _save_discovery_report(self, research: Dict) -> Path:
        """Save service discovery report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"SERVICE_DISCOVERY_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# Service Discovery Report\n\n")
            f.write(f"**Generated**: {research['timestamp']}\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Summary\n")
            summary = research['scan_summary']
            f.write(f"- **Total Services Found**: {summary['total_services']}\n")
            f.write(f"- **Missing Agents**: {summary['missing_agents']}\n")
            f.write(f"- **Categories**: {', '.join(summary['categories'])}\n\n")
            
            f.write("## Missing Agents (Priority Order)\n")
            for agent in research['discovery_results']['missing_agents']:
                f.write(f"- **{agent['service']}** ({agent['priority']} priority)\n")
                f.write(f"  - Category: {agent['category']}\n")
                f.write(f"  - Complexity: {agent['complexity']}\n")
                f.write(f"  - Reason: {agent['reason']}\n\n")
            
            f.write("## Recommendations\n")
            for rec in research['recommendations']:
                f.write(f"- {rec}\n")
        
        return report_path
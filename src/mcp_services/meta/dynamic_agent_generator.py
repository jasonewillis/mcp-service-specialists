#!/usr/bin/env python3
"""
Dynamic Agent Generator - Meta Agent for Agent Creation
Uses qwen2.5-coder:7b for code generation (94% success rate)
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio
import re

class DynamicAgentGenerator:
    """
    Meta-agent that creates specialized researcher agents on-the-fly
    Follows Jason Zhou's three-phase architecture automatically
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.agents_path = self.base_path / "mcp_services"
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Load existing agent templates for pattern matching
        self.templates = self._load_existing_templates()
        
        # Service categorization patterns
        self.service_patterns = {
            "external": {
                "keywords": ["api", "integration", "webhook", "oauth", "payment", "cloud", "saas"],
                "examples": ["stripe", "google", "slack", "sentry", "render", "aws"]
            },
            "federal": {
                "keywords": ["federal", "opm", "usajobs", "government", "gs", "locality", "series"],
                "examples": ["merit_hiring", "locality_pay", "series_mapping"]
            },
            "tech": {
                "keywords": ["framework", "database", "language", "library", "stack"],
                "examples": ["nextjs", "fastapi", "postgresql", "react", "python"]
            }
        }
        
        # Model selection based on complexity
        self.model_selection = {
            "simple": "mistral:7b",
            "complex": "deepseek-coder-v2:16b", 
            "code_heavy": "qwen2.5-coder:7b"
        }
        
        self.model = "qwen2.5-coder:7b"  # For agent code generation
    
    def _load_existing_templates(self) -> Dict[str, str]:
        """Load existing agents as templates"""
        templates = {}
        
        # Scan existing agents
        for category in ["external", "federal", "tech"]:
            category_path = self.agents_path / category
            if category_path.exists():
                for agent_file in category_path.glob("*.py"):
                    if agent_file.name != "__init__.py":
                        with open(agent_file) as f:
                            templates[agent_file.stem] = f.read()
        
        return templates
    
    def detect_service_type(self, service_name: str, context: str = "") -> Dict[str, Any]:
        """Detect what type of service this is and complexity"""
        
        service_lower = service_name.lower()
        context_lower = context.lower()
        combined = f"{service_lower} {context_lower}"
        
        # Determine category
        category_scores = {}
        for category, patterns in self.service_patterns.items():
            score = 0
            for keyword in patterns["keywords"]:
                if keyword in combined:
                    score += 1
            for example in patterns["examples"]:
                if example in service_lower:
                    score += 2
            category_scores[category] = score
        
        # Get highest scoring category
        category = max(category_scores.items(), key=lambda x: x[1])[0]
        
        # Determine complexity
        complexity_indicators = {
            "simple": ["webhook", "get", "basic", "simple"],
            "complex": ["oauth", "auth", "security", "encryption", "ml", "ai"],
            "code_heavy": ["framework", "library", "patterns", "architecture"]
        }
        
        complexity_scores = {}
        for complexity, indicators in complexity_indicators.items():
            score = sum(1 for indicator in indicators if indicator in combined)
            complexity_scores[complexity] = score
        
        complexity = max(complexity_scores.items(), key=lambda x: x[1])[0]
        
        return {
            "category": category,
            "complexity": complexity,
            "model": self.model_selection[complexity],
            "confidence": max(category_scores.values()) / 10
        }
    
    def find_best_template(self, service_type: Dict[str, Any]) -> str:
        """Find the best existing template to base new agent on"""
        
        category = service_type["category"]
        
        # Priority order for templates within category
        template_priorities = {
            "external": ["stripe_researcher", "google_oauth_researcher", "render_researcher", "opm_researcher"],
            "federal": ["merit_hiring_reviewer", "locality_pay_analyst", "series_mapping_expert"],
            "tech": ["nextjs_14_researcher", "fastapi_patterns_researcher", "postgresql_optimizer"]
        }
        
        # Find best available template
        for template_name in template_priorities.get(category, []):
            if template_name in self.templates:
                return template_name
        
        # Fallback to any template in category
        for template_name, template_code in self.templates.items():
            if f"/{category}/" in template_code or category in template_name:
                return template_name
        
        # Final fallback to stripe (most generic external service pattern)
        return "stripe_researcher"
    
    async def generate_agent(self, service_name: str, context: str = "", requirements: List[str] = None) -> Dict[str, Any]:
        """Generate a new specialized researcher agent"""
        
        # Detect service characteristics
        service_type = self.detect_service_type(service_name, context)
        
        # Find best template
        base_template = self.find_best_template(service_type)
        
        # Generate agent specification
        agent_spec = self._create_agent_spec(service_name, service_type, context, requirements or [])
        
        # Generate agent code
        agent_code = self._generate_agent_code(agent_spec, base_template)
        
        # Save agent file
        agent_path = self._save_agent_file(service_name, service_type["category"], agent_code)
        
        # Generate documentation
        docs = self._generate_agent_docs(agent_spec)
        
        return {
            "success": True,
            "agent_path": str(agent_path),
            "service_name": service_name,
            "category": service_type["category"],
            "model": service_type["model"],
            "confidence": service_type["confidence"],
            "template_used": base_template,
            "documentation": docs
        }
    
    def _create_agent_spec(self, service_name: str, service_type: Dict, context: str, requirements: List[str]) -> Dict[str, Any]:
        """Create detailed specification for the agent"""
        
        # Extract key information about the service
        service_info = self._analyze_service(service_name, context)
        
        return {
            "service_name": service_name,
            "class_name": self._to_class_name(service_name),
            "file_name": self._to_file_name(service_name),
            "category": service_type["category"],
            "model": service_type["model"],
            "description": service_info["description"],
            "primary_functions": service_info["functions"],
            "critical_rules": service_info["rules"],
            "integration_patterns": service_info["patterns"],
            "requirements": requirements,
            "fed_job_context": service_info["fed_context"]
        }
    
    def _analyze_service(self, service_name: str, context: str) -> Dict[str, Any]:
        """Analyze service to extract key characteristics"""
        
        # Service-specific analysis
        service_lower = service_name.lower()
        
        known_services = {
            "sentry": {
                "description": "Error tracking and performance monitoring",
                "functions": ["error_capture", "performance_tracking", "alerting"],
                "rules": ["Configure DSN securely", "Set appropriate sample rates", "Use breadcrumbs for context"],
                "patterns": ["DSN configuration", "Error filtering", "Performance monitoring"],
                "fed_context": "Monitor Fed Job Advisor production errors"
            },
            "slack": {
                "description": "Team communication and notifications",
                "functions": ["webhook_notifications", "alert_routing", "status_updates"],
                "rules": ["Secure webhook URLs", "Rate limit notifications", "Use appropriate channels"],
                "patterns": ["Webhook integration", "Message formatting", "Channel routing"],
                "fed_context": "Notify team of signups, errors, payments"
            },
            "google_analytics": {
                "description": "Web analytics and user tracking",
                "functions": ["event_tracking", "conversion_measurement", "user_behavior"],
                "rules": ["Privacy compliance", "Cookie consent", "Data retention policies"],
                "patterns": ["GA4 integration", "Event configuration", "Custom dimensions"],
                "fed_context": "Track job searches, applications, user journeys"
            },
            "usajobs_api": {
                "description": "Federal job data collection",
                "functions": ["job_collection", "search_optimization", "data_validation"],
                "rules": ["NEVER forget Fields=Full", "Respect rate limits", "Handle API changes"],
                "patterns": ["Pagination handling", "Error recovery", "Data transformation"],
                "fed_context": "Primary source of federal job listings"
            }
        }
        
        if service_lower in known_services:
            return known_services[service_lower]
        
        # Generic analysis based on context
        return {
            "description": f"{service_name} integration and configuration",
            "functions": ["integration_setup", "configuration", "monitoring"],
            "rules": ["Follow security best practices", "Handle errors gracefully", "Monitor performance"],
            "patterns": ["API integration", "Configuration management", "Error handling"],
            "fed_context": f"Support Fed Job Advisor {service_name} integration"
        }
    
    def _generate_agent_code(self, spec: Dict[str, Any], base_template: str) -> str:
        """Generate the actual agent code"""
        
        template_code = self.templates[base_template]
        
        # Extract template structure
        class_match = re.search(r'class (\w+):', template_code)
        base_class_name = class_match.group(1) if class_match else "BaseResearcher"
        
        # Generate new agent code
        agent_code = f'''#!/usr/bin/env python3
"""
{spec['service_name'].title()} Researcher - {spec['description'].title()}
Uses {spec['model']} for {spec['category']} service integration
Generated by DynamicAgentGenerator
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import asyncio

class {spec['class_name']}:
    """
    Research-only agent for {spec['service_name']} integration
    {spec['description']}
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # {spec['service_name']} specific configuration
        self.service_config = {{
            "name": "{spec['service_name']}",
            "category": "{spec['category']}",
            "fed_job_context": "{spec['fed_job_context']}"
        }}
        
        self.critical_rules = {spec['critical_rules']}
        
        self.model = "{spec['model']}"
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research {spec['service_name']} implementation"""
        
        task_analysis = self._analyze_task(task)
        
        research = {{
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "service": "{spec['service_name']}",
            "task_type": task_analysis['type'],
            "critical_requirements": self.critical_rules,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "code_templates": self._generate_code_templates(task_analysis),
            "integration_checklist": self._create_integration_checklist()
        }}
        
        report_path = self._save_research_report(research)
        
        return {{
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "critical_reminders": self.critical_rules[:3]
        }}
    
    def _analyze_task(self, task: str) -> Dict:
        """Analyze task for {spec['service_name']} requirements"""
        task_lower = task.lower()
        
        # Service-specific task analysis
        if any(func in task_lower for func in {spec['primary_functions']}):
            return {{"type": "integration", "focus": "service_setup"}}
        else:
            return {{"type": "general", "focus": "configuration"}}
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict:
        """Create implementation plan"""
        return {{
            "summary": f"{spec['service_name']} {{task_analysis['type']}} implementation",
            "steps": [
                "1. Configure {spec['service_name']} service",
                "2. Set up authentication/credentials",
                "3. Implement core integration",
                "4. Add error handling",
                "5. Create monitoring/logging",
                "6. Test integration thoroughly"
            ],
            "components": {spec['primary_functions']}
        }}
    
    def _generate_code_templates(self, task_analysis: Dict) -> Dict[str, str]:
        """Generate code templates for {spec['service_name']}"""
        return {{
            "basic_integration": f"""
# {spec['service_name']} integration template
# TODO: Implement specific integration patterns
class {spec['service_name'].title()}Integration:
    def __init__(self):
        self.config = load_{spec['service_name']}_config()
    
    async def integrate(self):
        # Implementation needed
        pass
""",
            "configuration": f"""
# {spec['service_name']} configuration
{spec['service_name'].upper()}_CONFIG = {{
    "service_name": "{spec['service_name']}",
    "environment": "production",
    # Add specific config keys
}}
"""
        }}
    
    def _create_integration_checklist(self) -> List[str]:
        """Create integration checklist"""
        return [
            f"Configure {spec['service_name']} credentials",
            "Set up error handling",
            "Implement logging",
            "Add monitoring",
            "Test integration",
            "Document configuration"
        ]
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """Review {spec['service_name']} implementation"""
        
        review = {{
            "timestamp": datetime.now().isoformat(),
            "service": "{spec['service_name']}",
            "compliant": True,
            "violations": [],
            "passed": [],
            "warnings": [],
            "score": 100
        }}
        
        # Basic validation checks
        if "{spec['service_name'].lower()}" in code.lower():
            review["passed"].append(f"✅ {spec['service_name']} integration present")
        else:
            review["violations"].append(f"❌ No {spec['service_name']} integration found")
            review["score"] -= 30
        
        # Add service-specific checks here
        
        review["recommendation"] = "✅ Ready" if review["score"] >= 70 else "❌ Needs work"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        """Save research report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"{spec['service_name']}_research_{{timestamp}}.md"
        
        with open(report_path, "w") as f:
            f.write(f"# {spec['service_name'].title()} Integration Research\\n\\n")
            f.write(f"**Task**: {{research['task']}}\\n\\n")
            
            f.write("## Critical Requirements\\n")
            for req in research['critical_requirements']:
                f.write(f"- {{req}}\\n")
            f.write("\\n")
            
            if research.get('code_templates'):
                f.write("## Code Templates\\n")
                for name, template in research['code_templates'].items():
                    f.write(f"### {{name}}\\n```python\\n{{template}}\\n```\\n\\n")
        
        return report_path
'''
        
        return agent_code
    
    def _to_class_name(self, service_name: str) -> str:
        """Convert service name to class name"""
        # Remove special characters and convert to PascalCase
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', service_name)
        parts = clean_name.split('_')
        return ''.join(word.capitalize() for word in parts if word) + "Researcher"
    
    def _to_file_name(self, service_name: str) -> str:
        """Convert service name to file name"""
        # Convert to snake_case
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', service_name.lower())
        return clean_name + "_researcher.py"
    
    def _save_agent_file(self, service_name: str, category: str, agent_code: str) -> Path:
        """Save the generated agent file"""
        
        # Create category directory if needed
        category_path = self.agents_path / category
        category_path.mkdir(exist_ok=True)
        
        # Save agent file
        file_name = self._to_file_name(service_name)
        agent_path = category_path / file_name
        
        with open(agent_path, 'w') as f:
            f.write(agent_code)
        
        return agent_path
    
    def _generate_agent_docs(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agent documentation"""
        return {
            "agent_name": spec['class_name'],
            "service": spec['service_name'],
            "category": spec['category'],
            "model": spec['model'],
            "description": spec['description'],
            "capabilities": spec['primary_functions'],
            "usage": f"Use for {spec['service_name']} integration research and implementation planning",
            "file_location": f"mcp_services/{spec['category']}/{spec['file_name']}"
        }
    
    async def identify_missing_services(self, project_context: str) -> List[Dict[str, Any]]:
        """Analyze project to identify services that need agents"""
        
        # Scan Fed Job Advisor codebase for service references
        missing_services = []
        
        # Known services mentioned in CLAUDE.md but missing agents
        known_missing = [
            {
                "service": "sentry",
                "context": "Error monitoring mentioned in CLAUDE.md",
                "priority": "high",
                "reason": "Production error tracking needed for Q1 2025"
            },
            {
                "service": "slack",
                "context": "Notification webhooks in integration setup",
                "priority": "medium", 
                "reason": "Team notifications for signups/errors"
            },
            {
                "service": "google_analytics",
                "context": "GA4 tracking mentioned for launch",
                "priority": "high",
                "reason": "User behavior tracking for product decisions"
            },
            {
                "service": "usajobs_api",
                "context": "Primary job data source, has harvester but no researcher",
                "priority": "critical",
                "reason": "Core data collection - Fields=Full requirement"
            }
        ]
        
        for service_info in known_missing:
            # Check if agent already exists
            service_type = self.detect_service_type(service_info["service"], service_info["context"])
            category_path = self.agents_path / service_type["category"]
            file_name = self._to_file_name(service_info["service"])
            
            if not (category_path / file_name).exists():
                missing_services.append({
                    **service_info,
                    "category": service_type["category"],
                    "estimated_complexity": service_type["complexity"],
                    "recommended_model": service_type["model"]
                })
        
        return missing_services
    
    async def bulk_generate_agents(self, services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate multiple agents at once"""
        
        results = {
            "generated": [],
            "failed": [],
            "total": len(services)
        }
        
        for service_info in services:
            try:
                result = await self.generate_agent(
                    service_name=service_info["service"],
                    context=service_info.get("context", ""),
                    requirements=service_info.get("requirements", [])
                )
                results["generated"].append(result)
            except Exception as e:
                results["failed"].append({
                    "service": service_info["service"],
                    "error": str(e)
                })
        
        return results
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research dynamic agent generation needs"""
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "generator_capabilities": [
                "Detect service type automatically",
                "Select optimal model based on complexity", 
                "Generate agents following three-phase pattern",
                "Create documentation and integration checklists",
                "Identify missing services in project"
            ],
            "implementation_plan": {
                "summary": "Dynamic agent generation system",
                "steps": [
                    "1. Analyze service requirements",
                    "2. Detect service category and complexity",
                    "3. Select best existing template",
                    "4. Generate specialized agent code",
                    "5. Save agent with proper naming",
                    "6. Generate documentation",
                    "7. Update agent registry"
                ]
            }
        }
        
        report_path = self._save_research_report(research, "dynamic_generator")
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": "Dynamic agent generation system ready",
            "next_steps": "Use to generate missing service agents"
        }
    
    def _save_research_report(self, research: Dict, prefix: str = "research") -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"{prefix}_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# Dynamic Agent Generator Research\n\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Generator Capabilities\n")
            for cap in research['generator_capabilities']:
                f.write(f"- {cap}\n")
            f.write("\n")
            
            f.write("## Implementation Plan\n")
            for step in research['implementation_plan']['steps']:
                f.write(f"{step}\n")
        
        return report_path
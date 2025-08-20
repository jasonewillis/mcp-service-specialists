#!/usr/bin/env python3
"""
MCP Task Router - Intelligent routing of development tasks to appropriate MCP agents

Implements task routing following TASK_APPROACH_BLUEPRINT.md:
- MCP-first methodology (80% research / 20% implementation)
- NO BS data honesty policy
- Agent selection matrix for optimal research coverage
- Quality gates and validation checkpoints
"""

import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TaskType(Enum):
    """Classification of development task types"""
    PAYMENT_INTEGRATION = "payment_integration"
    AUTHENTICATION = "authentication" 
    DATABASE_CHANGES = "database_changes"
    FRONTEND_FEATURES = "frontend_features"
    DATA_COLLECTION = "data_collection"
    FEDERAL_COMPLIANCE = "federal_compliance"
    PERFORMANCE = "performance"
    ANALYTICS = "analytics"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"
    API_DEVELOPMENT = "api_development"
    USER_EXPERIENCE = "user_experience"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    BUG_FIX = "bug_fix"

class Priority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium" 
    LOW = "low"

@dataclass
class TaskAnalysis:
    """Results of task analysis and routing"""
    task_type: TaskType
    priority: Priority
    primary_agents: List[str]
    secondary_agents: List[str]
    complexity_score: int  # 1-10 scale
    estimated_effort: str
    research_requirements: Dict[str, bool]
    compliance_requirements: List[str]
    integration_points: List[str]
    risk_factors: List[str]

class MCPTaskRouter:
    """Intelligent routing system for development tasks to MCP agents"""
    
    def __init__(self):
        # Agent expertise matrix from technical mastery documentation
        self.agent_expertise = {
            "data_scientist": {
                "domains": ["machine_learning", "statistics", "data_analysis", "predictive_modeling"],
                "technologies": ["python", "pandas", "scikit_learn", "tensorflow", "jupyter"],
                "specializations": ["feature_engineering", "model_validation", "data_preprocessing"]
            },
            "statistician": {
                "domains": ["statistical_analysis", "hypothesis_testing", "experimental_design"],
                "technologies": ["r", "python", "statistical_software", "data_visualization"],
                "specializations": ["regression_analysis", "time_series", "bayesian_methods"]
            },
            "database_admin": {
                "domains": ["database_design", "query_optimization", "data_architecture"],
                "technologies": ["postgresql", "mysql", "mongodb", "redis", "sql"],
                "specializations": ["performance_tuning", "backup_recovery", "replication"]
            },
            "devops_engineer": {
                "domains": ["ci_cd", "infrastructure", "containerization", "monitoring"],
                "technologies": ["docker", "kubernetes", "jenkins", "terraform", "prometheus"],
                "specializations": ["deployment_automation", "infrastructure_as_code", "observability"]
            },
            "it_specialist": {
                "domains": ["network_administration", "system_administration", "security"],
                "technologies": ["linux", "windows", "networking", "firewalls", "vpn"],
                "specializations": ["network_troubleshooting", "system_monitoring", "security_hardening"]
            },
            "resume_compression": {
                "domains": ["nlp", "text_processing", "federal_resume_standards"],
                "technologies": ["python", "nltk", "spacy", "text_analytics"],
                "specializations": ["content_optimization", "keyword_extraction", "format_compliance"]
            },
            "executive_orders": {
                "domains": ["legal_research", "policy_analysis", "regulatory_compliance"],
                "technologies": ["legal_databases", "policy_research", "compliance_frameworks"],
                "specializations": ["constitutional_analysis", "regulatory_interpretation", "impact_assessment"]
            },
            "job_market_analytics": {
                "domains": ["market_research", "data_analysis", "economic_analysis"],
                "technologies": ["apis", "web_scraping", "data_visualization", "statistical_analysis"],
                "specializations": ["trend_analysis", "salary_benchmarking", "geographic_analysis"]
            },
            "essay_compliance": {
                "domains": ["nlp", "compliance_analysis", "text_validation"],
                "technologies": ["python", "text_processing", "pattern_matching"],
                "specializations": ["merit_hiring_compliance", "content_validation", "automated_scoring"]
            },
            "collection_orchestrator": {
                "domains": ["etl_pipelines", "data_orchestration", "monitoring"],
                "technologies": ["airflow", "kafka", "python", "data_pipelines"],
                "specializations": ["pipeline_optimization", "data_quality", "error_handling"]
            }
        }
        
        # Task classification patterns
        self.classification_patterns = {
            TaskType.PAYMENT_INTEGRATION: [
                r"\b(stripe|payment|billing|subscription|checkout|credit card)\b",
                r"\b(paypal|square|authorize\.net|merchant)\b",
                r"\b(pci compliance|payment processing)\b"
            ],
            TaskType.AUTHENTICATION: [
                r"\b(auth|login|oauth|sso|jwt|session)\b",
                r"\b(password|2fa|mfa|biometric|webauthn)\b", 
                r"\b(user management|access control|permissions)\b"
            ],
            TaskType.DATABASE_CHANGES: [
                r"\b(database|sql|schema|migration|table)\b",
                r"\b(postgresql|mysql|mongodb|redis|query)\b",
                r"\b(index|optimization|backup|replication)\b"
            ],
            TaskType.FRONTEND_FEATURES: [
                r"\b(ui|frontend|react|nextjs|component)\b",
                r"\b(interface|dashboard|form|modal|responsive)\b",
                r"\b(css|styling|layout|design|user experience)\b"
            ],
            TaskType.DATA_COLLECTION: [
                r"\b(scraping|api|etl|data collection|pipeline)\b",
                r"\b(usajobs|federal data|job postings)\b",
                r"\b(monitoring|orchestration|data quality)\b"
            ],
            TaskType.FEDERAL_COMPLIANCE: [
                r"\b(federal|compliance|regulation|merit hiring)\b",
                r"\b(opm|usajobs|executive order|policy)\b",
                r"\b(accessibility|508|fisma|security clearance)\b"
            ],
            TaskType.PERFORMANCE: [
                r"\b(performance|optimization|slow|speed|latency)\b",
                r"\b(caching|redis|cdn|compression)\b",
                r"\b(monitoring|metrics|profiling|benchmarking)\b"
            ],
            TaskType.ANALYTICS: [
                r"\b(analytics|metrics|tracking|reporting)\b",
                r"\b(dashboard|visualization|statistics|insights)\b",
                r"\b(google analytics|data analysis|trends)\b"
            ]
        }
        
        # Agent routing matrix
        self.routing_matrix = {
            TaskType.PAYMENT_INTEGRATION: {
                "primary": ["data_scientist", "database_admin"],
                "secondary": ["it_specialist", "devops_engineer"]
            },
            TaskType.AUTHENTICATION: {
                "primary": ["it_specialist", "database_admin"], 
                "secondary": ["devops_engineer", "essay_compliance"]
            },
            TaskType.DATABASE_CHANGES: {
                "primary": ["database_admin", "devops_engineer"],
                "secondary": ["data_scientist", "collection_orchestrator"]
            },
            TaskType.FRONTEND_FEATURES: {
                "primary": ["data_scientist", "job_market_analytics"],
                "secondary": ["resume_compression", "essay_compliance"]
            },
            TaskType.DATA_COLLECTION: {
                "primary": ["collection_orchestrator", "database_admin"],
                "secondary": ["data_scientist", "job_market_analytics"]
            },
            TaskType.FEDERAL_COMPLIANCE: {
                "primary": ["essay_compliance", "executive_orders"],
                "secondary": ["resume_compression", "it_specialist"]
            },
            TaskType.PERFORMANCE: {
                "primary": ["devops_engineer", "database_admin"],
                "secondary": ["it_specialist", "collection_orchestrator"]
            },
            TaskType.ANALYTICS: {
                "primary": ["data_scientist", "statistician"],
                "secondary": ["job_market_analytics", "collection_orchestrator"]
            }
        }
        
    def analyze_task(self, task_description: str, context: Dict[str, Any] = None) -> TaskAnalysis:
        """
        Analyze development task and determine optimal MCP agent routing
        
        Args:
            task_description: Natural language description of the task
            context: Additional context about the task (priority, constraints, etc.)
            
        Returns:
            TaskAnalysis with routing recommendations and requirements
        """
        
        logger.info(f"Analyzing task: {task_description}")
        
        # Classify task type
        task_type = self._classify_task_type(task_description)
        
        # Determine priority
        priority = self._determine_priority(task_description, context)
        
        # Select agents
        primary_agents, secondary_agents = self._select_agents(task_type, task_description)
        
        # Assess complexity
        complexity_score = self._assess_complexity(task_description, task_type)
        
        # Estimate effort
        estimated_effort = self._estimate_effort(complexity_score, len(primary_agents))
        
        # Identify research requirements
        research_requirements = self._identify_research_requirements(task_type, task_description)
        
        # Check compliance requirements
        compliance_requirements = self._check_compliance_requirements(task_description)
        
        # Identify integration points
        integration_points = self._identify_integration_points(task_description)
        
        # Assess risk factors
        risk_factors = self._assess_risk_factors(task_description, task_type, complexity_score)
        
        analysis = TaskAnalysis(
            task_type=task_type,
            priority=priority,
            primary_agents=primary_agents,
            secondary_agents=secondary_agents,
            complexity_score=complexity_score,
            estimated_effort=estimated_effort,
            research_requirements=research_requirements,
            compliance_requirements=compliance_requirements,
            integration_points=integration_points,
            risk_factors=risk_factors
        )
        
        logger.info(f"Task analysis complete: {task_type.value}, complexity {complexity_score}/10")
        return analysis
        
    def _classify_task_type(self, task_description: str) -> TaskType:
        """Classify task type using pattern matching"""
        
        task_lower = task_description.lower()
        scores = {}
        
        for task_type, patterns in self.classification_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, task_lower))
                score += matches
            scores[task_type] = score
            
        # Return highest scoring task type, default to API development
        if not scores or max(scores.values()) == 0:
            return TaskType.API_DEVELOPMENT
            
        return max(scores.items(), key=lambda x: x[1])[0]
        
    def _determine_priority(self, task_description: str, context: Dict[str, Any] = None) -> Priority:
        """Determine task priority based on description and context"""
        
        if context and context.get("priority"):
            priority_map = {
                "critical": Priority.CRITICAL,
                "high": Priority.HIGH,
                "medium": Priority.MEDIUM,
                "low": Priority.LOW
            }
            return priority_map.get(context["priority"], Priority.MEDIUM)
            
        # Analyze description for priority indicators
        task_lower = task_description.lower()
        
        critical_indicators = [r"\b(urgent|critical|emergency|production down|security vulnerability)\b"]
        high_indicators = [r"\b(important|asap|needed soon|blocking|user-facing)\b"]
        low_indicators = [r"\b(nice to have|enhancement|future|optimization|refactor)\b"]
        
        for pattern in critical_indicators:
            if re.search(pattern, task_lower):
                return Priority.CRITICAL
                
        for pattern in high_indicators:
            if re.search(pattern, task_lower):
                return Priority.HIGH
                
        for pattern in low_indicators:
            if re.search(pattern, task_lower):
                return Priority.LOW
                
        return Priority.MEDIUM
        
    def _select_agents(self, task_type: TaskType, task_description: str) -> Tuple[List[str], List[str]]:
        """Select optimal agents for the task type"""
        
        routing = self.routing_matrix.get(task_type, {
            "primary": ["data_scientist"],
            "secondary": ["database_admin"]
        })
        
        primary_agents = routing["primary"].copy()
        secondary_agents = routing["secondary"].copy()
        
        # Enhance selection based on specific keywords
        task_lower = task_description.lower()
        
        # Add specialized agents based on specific requirements
        if re.search(r"\b(machine learning|ai|model|prediction)\b", task_lower):
            if "data_scientist" not in primary_agents:
                primary_agents.append("data_scientist")
                
        if re.search(r"\b(statistical|statistics|hypothesis|correlation)\b", task_lower):
            if "statistician" not in primary_agents:
                primary_agents.append("statistician")
                
        if re.search(r"\b(resume|cv|federal format)\b", task_lower):
            if "resume_compression" not in primary_agents:
                primary_agents.append("resume_compression")
                
        if re.search(r"\b(policy|regulation|executive order|legal)\b", task_lower):
            if "executive_orders" not in primary_agents:
                primary_agents.append("executive_orders")
                
        # Remove duplicates while preserving order
        primary_agents = list(dict.fromkeys(primary_agents))
        secondary_agents = list(dict.fromkeys(secondary_agents))
        
        # Ensure we have at least one primary agent
        if not primary_agents:
            primary_agents = ["data_scientist"]
            
        return primary_agents, secondary_agents
        
    def _assess_complexity(self, task_description: str, task_type: TaskType) -> int:
        """Assess task complexity on 1-10 scale"""
        
        base_complexity = {
            TaskType.DOCUMENTATION: 2,
            TaskType.BUG_FIX: 3,
            TaskType.FRONTEND_FEATURES: 4,
            TaskType.API_DEVELOPMENT: 5,
            TaskType.DATABASE_CHANGES: 6,
            TaskType.AUTHENTICATION: 7,
            TaskType.PAYMENT_INTEGRATION: 8,
            TaskType.DATA_COLLECTION: 6,
            TaskType.FEDERAL_COMPLIANCE: 7,
            TaskType.PERFORMANCE: 8,
            TaskType.ANALYTICS: 6
        }.get(task_type, 5)
        
        # Adjust based on complexity indicators
        task_lower = task_description.lower()
        complexity_modifiers = 0
        
        # Increase complexity
        high_complexity_patterns = [
            r"\b(integration|multiple systems|complex|advanced)\b",
            r"\b(real-time|high performance|scalable|distributed)\b",
            r"\b(security|compliance|encryption|authentication)\b",
            r"\b(machine learning|ai|algorithm|optimization)\b"
        ]
        
        for pattern in high_complexity_patterns:
            if re.search(pattern, task_lower):
                complexity_modifiers += 1
                
        # Decrease complexity  
        low_complexity_patterns = [
            r"\b(simple|basic|straightforward|quick)\b",
            r"\b(update|modify|small change|minor)\b",
            r"\b(documentation|readme|comment)\b"
        ]
        
        for pattern in low_complexity_patterns:
            if re.search(pattern, task_lower):
                complexity_modifiers -= 1
                
        # Calculate final complexity (1-10 scale)
        final_complexity = max(1, min(10, base_complexity + complexity_modifiers))
        
        return final_complexity
        
    def _estimate_effort(self, complexity_score: int, num_agents: int) -> str:
        """Estimate development effort based on complexity and agent count"""
        
        base_hours = complexity_score * 2  # Base: 2 hours per complexity point
        
        # Adjust for multiple agents (more research, coordination)
        agent_multiplier = 1 + (num_agents - 1) * 0.3
        
        total_hours = base_hours * agent_multiplier
        
        if total_hours <= 4:
            return "Small (2-4 hours)"
        elif total_hours <= 16:
            return "Medium (1-2 days)"
        elif total_hours <= 40:
            return "Large (1 week)"
        else:
            return "Extra Large (2+ weeks)"
            
    def _identify_research_requirements(self, task_type: TaskType, task_description: str) -> Dict[str, bool]:
        """Identify specific research requirements for the task"""
        
        base_requirements = {
            "technical_analysis": True,
            "implementation_guidance": True,
            "integration_strategy": True,
            "testing_approach": True,
            "security_review": False,
            "compliance_check": False,
            "performance_analysis": False,
            "user_experience_review": False
        }
        
        task_lower = task_description.lower()
        
        # Enable additional requirements based on task content
        if re.search(r"\b(security|auth|encryption|vulnerability)\b", task_lower):
            base_requirements["security_review"] = True
            
        if re.search(r"\b(federal|compliance|regulation|opm)\b", task_lower):
            base_requirements["compliance_check"] = True
            
        if re.search(r"\b(performance|speed|optimization|slow)\b", task_lower):
            base_requirements["performance_analysis"] = True
            
        if re.search(r"\b(ui|ux|interface|user experience|frontend)\b", task_lower):
            base_requirements["user_experience_review"] = True
            
        return base_requirements
        
    def _check_compliance_requirements(self, task_description: str) -> List[str]:
        """Identify federal compliance requirements"""
        
        requirements = []
        task_lower = task_description.lower()
        
        compliance_patterns = {
            "Section 508 Accessibility": r"\b(accessibility|508|ada|screen reader|wcag)\b",
            "FISMA Security": r"\b(security|fisma|cybersecurity|encryption)\b", 
            "Privacy Act": r"\b(privacy|pii|personal information|data protection)\b",
            "Merit Hiring": r"\b(merit|hiring|federal employment|job posting)\b",
            "OPM Standards": r"\b(opm|classification|job series|gs level)\b"
        }
        
        for requirement, pattern in compliance_patterns.items():
            if re.search(pattern, task_lower):
                requirements.append(requirement)
                
        return requirements
        
    def _identify_integration_points(self, task_description: str) -> List[str]:
        """Identify systems that need integration consideration"""
        
        integration_points = []
        task_lower = task_description.lower()
        
        system_patterns = {
            "USAJOBS API": r"\b(usajobs|federal jobs|job postings)\b",
            "Stripe Payment": r"\b(stripe|payment|billing|subscription)\b",
            "Google OAuth": r"\b(google|oauth|authentication|sso)\b",
            "PostgreSQL Database": r"\b(database|postgresql|sql|data storage)\b",
            "Redis Cache": r"\b(cache|redis|session|performance)\b",
            "Sentry Monitoring": r"\b(monitoring|errors|sentry|logging)\b",
            "Google Analytics": r"\b(analytics|tracking|metrics|ga4)\b"
        }
        
        for system, pattern in system_patterns.items():
            if re.search(pattern, task_lower):
                integration_points.append(system)
                
        return integration_points
        
    def _assess_risk_factors(self, task_description: str, task_type: TaskType, complexity_score: int) -> List[str]:
        """Assess potential risk factors for the task"""
        
        risk_factors = []
        task_lower = task_description.lower()
        
        # High complexity risks
        if complexity_score >= 8:
            risk_factors.append("High complexity - requires careful planning and testing")
            
        # Task type specific risks
        type_risks = {
            TaskType.PAYMENT_INTEGRATION: ["PCI compliance requirements", "Financial transaction security", "Webhook reliability"],
            TaskType.AUTHENTICATION: ["Security vulnerabilities", "Session management complexity", "OAuth flow errors"],
            TaskType.DATABASE_CHANGES: ["Data migration risks", "Performance impact", "Backup requirements"],
            TaskType.FEDERAL_COMPLIANCE: ["Regulatory compliance", "Merit hiring requirements", "Accessibility standards"],
            TaskType.PERFORMANCE: ["System stability", "User experience impact", "Monitoring complexity"]
        }
        
        if task_type in type_risks:
            risk_factors.extend(type_risks[task_type])
            
        # Content-based risks
        if re.search(r"\b(production|live|users?|customer)\b", task_lower):
            risk_factors.append("Production system impact")
            
        if re.search(r"\b(breaking|major|significant)\b", task_lower):
            risk_factors.append("Breaking changes potential")
            
        if re.search(r"\b(data|migration|schema)\b", task_lower):
            risk_factors.append("Data integrity considerations")
            
        return list(set(risk_factors))  # Remove duplicates
        
    def generate_research_strategy(self, analysis: TaskAnalysis) -> Dict[str, Any]:
        """Generate comprehensive research strategy based on task analysis"""
        
        return {
            "research_phases": [
                {
                    "phase": "Discovery",
                    "agents": analysis.primary_agents,
                    "focus": "Technical analysis and implementation patterns",
                    "deliverables": ["Technical research", "Implementation recommendations", "Integration strategy"]
                },
                {
                    "phase": "Validation", 
                    "agents": analysis.secondary_agents,
                    "focus": "Reality checking and gap analysis",
                    "deliverables": ["Constraint identification", "Risk assessment", "Alternative approaches"]
                },
                {
                    "phase": "Planning",
                    "agents": ["general_purpose"],
                    "focus": "Implementation planning and coordination",
                    "deliverables": ["Step-by-step plan", "Testing strategy", "Success metrics"]
                }
            ],
            "research_requirements": analysis.research_requirements,
            "quality_gates": [
                "All quantitative claims have supporting data",
                "Limitations and constraints clearly documented",
                "Implementation approach validated against current architecture",
                "Federal compliance requirements addressed",
                "Risk mitigation strategies defined"
            ],
            "success_criteria": [
                f"Research completed by {len(analysis.primary_agents)} primary agents",
                "Validation passed by secondary agents",
                "Implementation plan approved with NO BS compliance",
                "All integration points identified and planned",
                "Risk factors assessed and mitigated"
            ]
        }

# Example usage and testing
if __name__ == "__main__":
    router = MCPTaskRouter()
    
    # Test various task descriptions
    test_tasks = [
        "Add Stripe payment integration with subscription management",
        "Improve user authentication with WebAuthn and 2FA",
        "Optimize database queries for better performance",
        "Create analytics dashboard for job application tracking",
        "Implement federal resume builder with compliance checking",
        "Fix bug in data collection pipeline causing failures"
    ]
    
    for task in test_tasks:
        print(f"\n{'='*60}")
        print(f"TASK: {task}")
        print('='*60)
        
        analysis = router.analyze_task(task)
        strategy = router.generate_research_strategy(analysis)
        
        print(f"Type: {analysis.task_type.value}")
        print(f"Priority: {analysis.priority.value}")
        print(f"Complexity: {analysis.complexity_score}/10")
        print(f"Estimated Effort: {analysis.estimated_effort}")
        print(f"Primary Agents: {', '.join(analysis.primary_agents)}")
        print(f"Secondary Agents: {', '.join(analysis.secondary_agents)}")
        print(f"Compliance Requirements: {', '.join(analysis.compliance_requirements) if analysis.compliance_requirements else 'None'}")
        print(f"Risk Factors: {len(analysis.risk_factors)} identified")
        print(f"Research Phases: {len(strategy['research_phases'])}")
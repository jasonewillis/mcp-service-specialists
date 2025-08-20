"""
Fed Job Advisor Context Master Agent - Integrated with Agent System
The ultimate assistant for Claude - deep knowledge of data, Merit Hiring, and project constraints
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime, timedelta
import json
import re
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import structlog
from langchain.tools import Tool

from agents.app.agents.base import FederalJobAgent, AgentConfig

logger = structlog.get_logger()


class DataFieldImportance(Enum):
    """USAJobs data field importance levels"""
    CRITICAL = "critical"  # Must have for job matching
    HIGH = "high"         # Important for analysis
    MEDIUM = "medium"     # Useful for features
    LOW = "low"          # Optional enhancement


class MeritComplianceLevel(Enum):
    """Merit Hiring compliance requirements"""
    MANDATORY = "mandatory"    # Legal requirement
    RECOMMENDED = "recommended" # Best practice
    OPTIONAL = "optional"      # Nice to have


@dataclass
class USAJobsField:
    """USAJobs API field mapping"""
    ui_element: str
    api_path: str
    db_column: str
    data_type: str
    importance: DataFieldImportance
    purpose: str
    example: str


@dataclass
class MeritHiringRule:
    """Merit Hiring compliance rule"""
    rule_name: str
    description: str
    compliance_level: MeritComplianceLevel
    validation: str
    consequences: str


class AgentRouter(FederalJobAgent):
    """
    Intelligent agent router for Fed Job Advisor project
    Routes tasks to appropriate agents while maintaining project knowledge
    Ensures compliance with data requirements, Merit Hiring rules, and constraints
    """
    
    def __init__(self, config: AgentConfig):
        self.project_root = Path("/Users/jasonewillis/Developer/jwRepos/JLWAI/fedJobAdvisor")
        
        # Initialize all knowledge domains first
        self._load_data_dictionary()
        self._load_merit_hiring_rules()
        self._load_project_constraints()
        self._load_launch_requirements()
        
        # Now initialize parent class (which needs tools)
        super().__init__(config)
        
        logger.info("Agent Router initialized - Ready to coordinate agent tasks")
    
    def _get_prompt_template(self) -> str:
        """Get the prompt template for the agent router"""
        return """You are an intelligent Agent Router for the Fed Job Advisor system.
        
Your role is to:
1. Analyze tasks and route them to the appropriate specialized agents
2. Ensure compliance with project constraints (Merit Hiring, data requirements, protected files)
3. Coordinate parallel execution for efficiency
4. Provide warnings about critical requirements

Project Knowledge:
- CRITICAL: Fields=Full parameter prevents 93% data loss
- NEVER generate essay content (Merit Hiring compliance)
- Protected files must not be modified without careful review
- Solo developer with $0 budget constraint

Available tools:
{tools}

Tool names: {tool_names}

When routing tasks, always consider:
- Which agents can work in parallel
- What constraints apply
- What warnings are needed

{agent_scratchpad}
"""
    
    def _load_tools(self):
        """Load tools for the agent router"""
        # Tools are created in _create_tools method
        pass
    
    def _create_tools(self) -> List[Tool]:
        """Create specialized tools for agent routing and coordination"""
        
        return [
            Tool(
                name="route_task",
                func=self._route_task_tool,
                description="Route a task to the appropriate agents and determine parallel execution strategy"
            ),
            Tool(
                name="check_compliance",
                func=self._check_compliance_tool,
                description="Check if an action complies with project constraints (Merit Hiring, data requirements, protected files)"
            ),
            Tool(
                name="get_agent_recommendations",
                func=self._get_agent_recommendations_tool,
                description="Get specific agent recommendations for a task with priority and coordination strategy"
            ),
            Tool(
                name="validate_approach",
                func=self._validate_approach_tool,
                description="Validate a proposed approach against project requirements and suggest improvements"
            ),
            Tool(
                name="get_project_context",
                func=self._get_project_context_tool,
                description="Get relevant project context for a specific task (data fields, rules, constraints)"
            )
        ]
    
    def _load_data_dictionary(self):
        """Load complete USAJobs data dictionary"""
        
        self.critical_fields = {
            "title": USAJobsField(
                ui_element="Job Title",
                api_path="PositionTitle",
                db_column="title",
                data_type="VARCHAR(500)",
                importance=DataFieldImportance.CRITICAL,
                purpose="Job matching, search",
                example="Software Developer"
            ),
            "agency": USAJobsField(
                ui_element="Agency",
                api_path="OrganizationName",
                db_column="agency",
                data_type="VARCHAR(200)",
                importance=DataFieldImportance.CRITICAL,
                purpose="Agency analysis, filtering",
                example="Department of Defense"
            ),
            "salary": USAJobsField(
                ui_element="Salary Range",
                api_path="PositionRemuneration[].MinimumRange",
                db_column="salary_min",
                data_type="INTEGER",
                importance=DataFieldImportance.CRITICAL,
                purpose="Compensation analysis",
                example="65000"
            ),
            "grade": USAJobsField(
                ui_element="Grade",
                api_path="PositionRemuneration[].Grade",
                db_column="grade",
                data_type="VARCHAR(20)",
                importance=DataFieldImportance.CRITICAL,
                purpose="Career progression",
                example="13"
            ),
            "location": USAJobsField(
                ui_element="Location(s)",
                api_path="PositionLocation[]",
                db_column="location_data",
                data_type="JSONB",
                importance=DataFieldImportance.CRITICAL,
                purpose="Geographic matching, COL analysis",
                example='[{"CityName":"DC","StateCode":"DC"}]'
            ),
            "series": USAJobsField(
                ui_element="Job Series",
                api_path="JobCategory[].Code",
                db_column="series",
                data_type="VARCHAR(10)",
                importance=DataFieldImportance.HIGH,
                purpose="Career pathway analysis",
                example="2210"
            ),
            "clearance": USAJobsField(
                ui_element="Security Clearance",
                api_path="SecurityClearanceRequired",
                db_column="security_clearance",
                data_type="VARCHAR(100)",
                importance=DataFieldImportance.HIGH,
                purpose="Clearance pathway planning",
                example="Secret"
            )
        }
        
        # Federal keywords for matching
        self.federal_keywords = {
            "technical": [
                "Python", "Java", "SQL", "AWS", "Azure", "Kubernetes",
                "Machine Learning", "Data Science", "DevOps", "Cloud"
            ],
            "clearance": [
                "Secret", "Top Secret", "TS/SCI", "Public Trust",
                "Confidential", "Q Clearance", "L Clearance"
            ],
            "agencies": [
                "DOD", "VA", "DHS", "State", "Treasury", "Justice",
                "HHS", "NASA", "NSA", "CIA", "FBI", "EPA"
            ],
            "pay_plans": [
                "GS", "GG", "NH", "NF", "WG", "WS", "SES", "SL", "ST",
                "ES", "EX", "FP", "FO", "AD", "YA", "VN", "VH"
            ],
            "work_arrangements": [
                "Remote", "Telework", "Hybrid", "On-site", "Flexible",
                "Compressed Schedule", "Alternative Work Schedule"
            ]
        }
        
        # Locality pay areas (53 official areas)
        self.locality_areas = {
            "DC": {"name": "Washington-DC-MD-VA-WV-PA", "adjustment": 32.49},
            "SF": {"name": "San Francisco-Oakland-San Jose, CA", "adjustment": 42.74},
            "NY": {"name": "New York-Newark, NY-NJ-CT-PA", "adjustment": 36.16},
            "LA": {"name": "Los Angeles-Long Beach, CA", "adjustment": 32.18},
            "SEA": {"name": "Seattle-Tacoma, WA", "adjustment": 28.30},
            "BOS": {"name": "Boston-Worcester-Providence, MA-RI-NH-ME-CT", "adjustment": 32.79},
            "DEN": {"name": "Denver-Aurora, CO", "adjustment": 29.52},
            "REST": {"name": "Rest of United States", "adjustment": 16.50}
        }
    
    def _load_merit_hiring_rules(self):
        """Load Merit Hiring system rules and compliance requirements"""
        
        self.merit_rules = {
            "no_content_generation": MeritHiringRule(
                rule_name="No AI Content Generation",
                description="System must NEVER write essays or application content for candidates",
                compliance_level=MeritComplianceLevel.MANDATORY,
                validation="Check all outputs for generated content",
                consequences="Immediate disqualification if violated"
            ),
            "word_limit": MeritHiringRule(
                rule_name="200 Word Essay Limit",
                description="Essays must be exactly 200 words or less",
                compliance_level=MeritComplianceLevel.MANDATORY,
                validation="Strict word count enforcement",
                consequences="Application rejected if exceeded"
            ),
            "attestation": MeritHiringRule(
                rule_name="No-AI Attestation",
                description="Candidates must attest they wrote content themselves",
                compliance_level=MeritComplianceLevel.MANDATORY,
                validation="Checkbox required before submission",
                consequences="Legal liability for false attestation"
            ),
            "star_method": MeritHiringRule(
                rule_name="STAR Method Structure",
                description="Essays should follow Situation-Task-Action-Result format",
                compliance_level=MeritComplianceLevel.RECOMMENDED,
                validation="Analyze for STAR components",
                consequences="Lower scoring without structure"
            ),
            "keyword_matching": MeritHiringRule(
                rule_name="Federal Keyword Usage",
                description="Include relevant federal terminology and competencies",
                compliance_level=MeritComplianceLevel.RECOMMENDED,
                validation="Check for job-specific keywords",
                consequences="May not pass initial screening"
            ),
            "competency_based": MeritHiringRule(
                rule_name="Competency-Based Assessment",
                description="Focus on demonstrating specific competencies",
                compliance_level=MeritComplianceLevel.MANDATORY,
                validation="Map to OPM competency framework",
                consequences="Required for federal positions"
            )
        }
        
        # Essay scoring components
        self.essay_components = {
            "situation": {"weight": 0.2, "max_words": 40},
            "task": {"weight": 0.2, "max_words": 40},
            "action": {"weight": 0.4, "max_words": 80},
            "result": {"weight": 0.2, "max_words": 40}
        }
        
        # Common disqualifiers
        self.merit_disqualifiers = [
            "AI-generated content detected",
            "Exceeded word limit",
            "No attestation provided",
            "Plagiarism detected",
            "Generic non-specific content",
            "No quantifiable results"
        ]
    
    def _load_project_constraints(self):
        """Load all project constraints and protected resources"""
        
        self.constraints = {
            "developer": {
                "team_size": 1,
                "hours_per_week": 20,
                "budget": 0,
                "timeline": "evenings/weekends"
            },
            "protected_files": [
                "backend/collect_federal_jobs.py",  # Contains Fields=Full fix
                "backend/collect_current_jobs.py",   # 93% data loss if broken
                "backend/monitor_field_population.py",
                ".github/workflows/test_backend.yml"
            ],
            "critical_parameters": {
                "Fields": "Full",  # MUST be in all USAJobs API calls
                "ResultsPerPage": 500,  # Optimal for collection
                "SortField": "PositionStartDate"
            },
            "environment_variables": {
                "read_only": [".env", ".env.production"],
                "managed_by": "Render dashboard",
                "never_commit": ["API keys", "secrets", "tokens"]
            }
        }
        
        # Revenue reality check
        self.revenue_constraints = {
            "realistic_targets": {
                "year_1": "$50K-100K",
                "customers_year_1": "100-200",
                "growth": "linear not exponential"
            },
            "avoid_assumptions": [
                "Hiring contractors",
                "VC funding",
                "Enterprise infrastructure",
                "Paid marketing",
                "Team expansion"
            ]
        }
    
    def _load_launch_requirements(self):
        """Load launch readiness requirements"""
        
        self.launch_status = {
            "target": "Q1 2025",
            "phase": "PRE-LAUNCH PREPARATION",
            "completed": [
                "Production deployment on Render",
                "SSL certificates",
                "Database backups",
                "Docker containerization",
                "Basic UI/UX"
            ],
            "critical_pending": {
                "stripe": {
                    "status": "NOT STARTED",
                    "priority": "CRITICAL",
                    "tasks": [
                        "Create Stripe account",
                        "Configure webhook endpoints",
                        "Set up subscription plans",
                        "Test payment flows",
                        "Configure tax handling"
                    ]
                },
                "sentry": {
                    "status": "NOT STARTED",
                    "priority": "HIGH",
                    "tasks": [
                        "Create Sentry project",
                        "Install SDKs",
                        "Configure DSNs",
                        "Set up alerts"
                    ]
                },
                "analytics": {
                    "status": "NOT STARTED",
                    "priority": "MEDIUM",
                    "tasks": [
                        "Create GA4 property",
                        "Install tracking",
                        "Define conversions"
                    ]
                }
            },
            "pricing": {
                "local": 29,
                "mobile": 49,
                "annual_discount": "2 months free"
            }
        }
    
    # Tool implementation methods
    def _route_task_tool(self, task: str) -> str:
        """Tool: Route task to appropriate agents"""
        routing = self.route_task(task)
        return json.dumps(routing, indent=2)
    
    def _check_compliance_tool(self, action: str) -> str:
        """Tool: Check compliance with project constraints"""
        compliance = self.check_compliance(action)
        return json.dumps(compliance, indent=2)
    
    def _get_agent_recommendations_tool(self, task: str) -> str:
        """Tool: Get agent recommendations for a task"""
        recommendations = self.get_agent_recommendations(task)
        return json.dumps(recommendations, indent=2)
    
    def _validate_approach_tool(self, approach_json: str) -> str:
        """Tool: Validate a proposed approach"""
        try:
            approach = json.loads(approach_json) if isinstance(approach_json, str) and approach_json.startswith('{') else {"description": approach_json}
        except json.JSONDecodeError:
            approach = {"description": approach_json}
        
        validation = self.validate_approach(approach)
        return json.dumps(validation, indent=2)
    
    def _get_project_context_tool(self, topic: str) -> str:
        """Tool: Get relevant project context"""
        context = self.get_project_context(topic)
        return json.dumps(context, indent=2)
    
    def analyze_data_request(self, request: str) -> Dict[str, Any]:
        """
        Analyze a data-related request with full context
        """
        
        analysis = {
            "data_fields_involved": [],
            "importance_level": None,
            "compliance_requirements": [],
            "warnings": [],
            "recommendations": []
        }
        
        request_lower = request.lower()
        
        # Check for critical data fields
        for field_name, field_info in self.critical_fields.items():
            if field_name in request_lower or field_info.ui_element.lower() in request_lower:
                analysis["data_fields_involved"].append({
                    "field": field_name,
                    "importance": field_info.importance.value,
                    "db_column": field_info.db_column,
                    "purpose": field_info.purpose
                })
        
        # Check for collection parameters
        if "collect" in request_lower or "api" in request_lower:
            analysis["warnings"].append("⚠️ CRITICAL: Must include Fields=Full parameter")
            analysis["warnings"].append("⚠️ Check protected collectors before modifying")
            analysis["recommendations"].append("Use existing collect_federal_jobs.py as entry point")
        
        # Check for locality/COL data
        if "locality" in request_lower or "col" in request_lower or "cost of living" in request_lower:
            analysis["recommendations"].append("Use locality_areas data for 53 official OPM areas")
            analysis["recommendations"].append("Include locality pay adjustments in calculations")
            analysis["data_fields_involved"].append({
                "field": "locality_data",
                "importance": "critical",
                "purpose": "COL analysis with locality pay adjustments"
            })
        
        # Set importance level
        if analysis["data_fields_involved"]:
            critical_count = sum(1 for f in analysis["data_fields_involved"] 
                                if f.get("importance") == "critical")
            analysis["importance_level"] = "CRITICAL" if critical_count > 0 else "HIGH"
        
        return analysis
    
    def check_merit_compliance(self, action: str) -> Dict[str, Any]:
        """
        Check Merit Hiring compliance for an action
        """
        
        compliance = {
            "compliant": True,
            "violations": [],
            "warnings": [],
            "requirements": [],
            "guidance": []
        }
        
        action_lower = action.lower()
        
        # Check for content generation violations
        if any(word in action_lower for word in ["write essay", "generate essay", "create essay"]):
            compliance["compliant"] = False
            compliance["violations"].append("NEVER write essay content for candidates")
            compliance["guidance"].append("Only analyze and provide structural feedback")
        
        # Check for word limit compliance
        if "essay" in action_lower:
            compliance["requirements"].append("Enforce 200-word strict limit")
            compliance["requirements"].append("Require no-AI attestation")
            compliance["guidance"].append("Suggest STAR method structure")
        
        # Check for keyword optimization
        if "keyword" in action_lower or "optimize" in action_lower:
            compliance["guidance"].append("Point to existing experience")
            compliance["guidance"].append("Suggest federal terminology from job posting")
            compliance["warnings"].append("Never provide specific wording")
        
        # Add competency mapping
        if "competency" in action_lower or "qualification" in action_lower:
            compliance["requirements"].append("Map to OPM competency framework")
            compliance["guidance"].append("Focus on demonstrable skills")
        
        return compliance
    
    def get_data_collection_guidance(self) -> Dict[str, Any]:
        """
        Provide comprehensive data collection guidance
        """
        
        return {
            "critical_parameters": {
                "Fields": "Full",  # MANDATORY - prevents 93% data loss
                "ResultsPerPage": 500,
                "SortField": "PositionStartDate",
                "DatePosted": 30  # Last 30 days
            },
            "api_endpoints": {
                "search": "https://data.usajobs.gov/api/search",
                "headers": {
                    "Authorization-Key": "YOUR_API_KEY",
                    "User-Agent": "YOUR_EMAIL"
                }
            },
            "protected_files": self.constraints["protected_files"],
            "data_quality_checks": [
                "Verify job_summary is not NULL",
                "Check qualification_summary populated",
                "Validate salary_min > 0",
                "Ensure location_data is valid JSON"
            ],
            "storage_optimization": {
                "keep": ["title", "agency", "salary", "grade", "location", "job_summary"],
                "index": ["posting_date", "closing_date", "agency", "series"],
                "compress": ["job_summary", "qualifications", "duties"]
            }
        }
    
    def route_task(self, task: str) -> Dict[str, Any]:
        """
        Primary routing method - determines which agents to use for a task
        """
        task_lower = task.lower()
        
        routing = {
            "task": task,
            "primary_agents": [],
            "parallel_agents": [],
            "sequence": [],
            "warnings": [],
            "requirements": []
        }
        
        # Determine task type and route accordingly
        if "col" in task_lower or "locality" in task_lower or "dashboard" in task_lower:
            routing["primary_agents"] = ["statistician-analyst", "data_scientist"]
            routing["parallel_agents"] = ["FrontendEngineeringManager"]
            routing["requirements"].append("Use 53 official OPM locality areas")
            
        elif "data" in task_lower or "collection" in task_lower:
            routing["primary_agents"] = ["data-pipeline-guardian"]
            routing["parallel_agents"] = ["job-data-quality-analyst", "database-performance-tuner"]
            routing["warnings"].append("⚠️ Must include Fields=Full parameter")
            routing["requirements"].append("Check protected collectors before modifying")
            
        elif "merit" in task_lower or "essay" in task_lower:
            routing["primary_agents"] = ["essay_guidance"]
            routing["parallel_agents"] = ["federal-compliance-auditor", "test-coverage-enforcer"]
            routing["warnings"].append("⚠️ NEVER generate essay content")
            routing["requirements"].append("Enforce 200-word limit")
            
        elif "resume" in task_lower:
            routing["primary_agents"] = ["resume_compression"]
            routing["parallel_agents"] = ["test-coverage-enforcer"]
            routing["requirements"].append("Enforce 2-page limit")
            
        elif "job search" in task_lower or "job matching" in task_lower:
            routing["primary_agents"] = ["analytics", "data_scientist"]
            routing["parallel_agents"] = ["job_collector"]
            
        else:
            # General routing based on keywords
            routing["primary_agents"] = ["general-purpose"]
            routing["requirements"].append("Consider using Task tool for complex searches")
        
        # Add execution sequence
        if routing["primary_agents"]:
            routing["sequence"] = [
                {"step": 1, "agents": routing["primary_agents"], "action": "Primary analysis"},
                {"step": 2, "agents": routing["parallel_agents"], "action": "Parallel support"},
                {"step": 3, "agents": ["project-manager"], "action": "Create PR if code changes"}
            ]
        
        return routing
    
    def get_agent_recommendations(self, task: str) -> List[Dict[str, Any]]:
        """
        Get detailed agent recommendations with priorities
        """
        routing = self.route_task(task)
        recommendations = []
        
        # Convert routing to recommendations format
        priority = 1
        for agent in routing["primary_agents"]:
            recommendations.append({
                "agent": agent,
                "priority": priority,
                "role": "Primary",
                "reason": f"Best suited for {task[:50]}..."
            })
            priority += 1
            
        for agent in routing["parallel_agents"]:
            recommendations.append({
                "agent": agent,
                "priority": priority,
                "role": "Support",
                "reason": "Parallel execution for efficiency"
            })
            priority += 1
            
        return recommendations
    
    def check_compliance(self, action: str) -> Dict[str, Any]:
        """
        Check compliance with all project constraints
        """
        compliance = {
            "compliant": True,
            "violations": [],
            "warnings": [],
            "checks": {
                "merit_hiring": True,
                "data_requirements": True,
                "protected_files": True,
                "budget_constraints": True
            }
        }
        
        action_lower = action.lower()
        
        # Merit Hiring checks
        if any(word in action_lower for word in ["write essay", "generate essay", "create essay"]):
            compliance["compliant"] = False
            compliance["checks"]["merit_hiring"] = False
            compliance["violations"].append("Cannot generate essay content - Merit Hiring violation")
            
        # Data collection checks
        if "collect" in action_lower and "fields=full" not in action_lower:
            compliance["warnings"].append("Must include Fields=Full in API calls")
            compliance["checks"]["data_requirements"] = False
            
        # Protected file checks
        for protected in self.constraints["protected_files"]:
            if protected.lower() in action_lower:
                compliance["warnings"].append(f"⚠️ Protected file: {protected} - verify changes carefully")
                
        # Budget checks
        if any(word in action_lower for word in ["hire", "contractor", "consultant", "purchase"]):
            compliance["warnings"].append("Budget constraint: $0 for external development")
            compliance["checks"]["budget_constraints"] = False
            
        return compliance
    
    def validate_approach(self, approach: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a proposed approach against project requirements
        """
        validation = {
            "valid": True,
            "score": 100,
            "issues": [],
            "suggestions": [],
            "optimizations": []
        }
        
        description = approach.get("description", "").lower()
        
        # Check for common issues
        if "mock data" in description:
            validation["issues"].append("Never use mock data in production")
            validation["score"] -= 20
            
        if "hire" in description or "contractor" in description:
            validation["issues"].append("Solo developer constraint - no hiring")
            validation["score"] -= 30
            validation["valid"] = False
            
        # Suggest optimizations
        if "sequential" in description:
            validation["optimizations"].append("Consider parallel agent execution")
            
        if "api" in description and "fields=full" not in description:
            validation["suggestions"].append("Remember Fields=Full parameter for USAJobs API")
            
        if validation["score"] < 70:
            validation["valid"] = False
            
        return validation
    
    def get_project_context(self, topic: str) -> Dict[str, Any]:
        """
        Get relevant project context for a specific topic
        """
        topic_lower = topic.lower()
        context = {
            "topic": topic,
            "relevant_info": {},
            "constraints": [],
            "best_practices": []
        }
        
        if "data" in topic_lower or "api" in topic_lower:
            context["relevant_info"]["critical_fields"] = list(self.critical_fields.keys())
            context["relevant_info"]["api_params"] = self.constraints["critical_parameters"]
            context["constraints"].append("Fields=Full is mandatory")
            context["best_practices"].append("Use existing collectors as entry points")
            
        elif "merit" in topic_lower or "essay" in topic_lower:
            context["relevant_info"]["rules"] = [r.rule_name for r in self.merit_rules.values()]
            context["relevant_info"]["word_limit"] = 200
            context["constraints"].append("Never generate content")
            context["best_practices"].append("Use STAR method guidance")
            
        elif "launch" in topic_lower or "deployment" in topic_lower:
            context["relevant_info"]["status"] = self.launch_status["phase"]
            context["relevant_info"]["target"] = self.launch_status["target"]
            context["relevant_info"]["pending"] = list(self.launch_status["critical_pending"].keys())
            context["constraints"].append("Stripe integration not started")
            
        elif "budget" in topic_lower or "cost" in topic_lower:
            context["relevant_info"] = self.revenue_constraints
            context["constraints"] = self.constraints["developer"]
            context["best_practices"].append("Bootstrap approach - no external costs")
            
        return context
    
    def suggest_agent_coordination(self, task: str) -> List[Dict[str, Any]]:
        """
        Suggest agent coordination for data and Merit tasks
        """
        
        suggestions = []
        task_lower = task.lower()
        
        if "data" in task_lower or "collection" in task_lower:
            suggestions.extend([
                {"agent": "data-pipeline-guardian", "role": "Monitor collection", "priority": 1},
                {"agent": "job-data-quality-analyst", "role": "Validate data quality", "priority": 2},
                {"agent": "database-performance-tuner", "role": "Optimize queries", "priority": 3}
            ])
        
        if "merit" in task_lower or "essay" in task_lower:
            suggestions.extend([
                {"agent": "federal-compliance-auditor", "role": "Ensure Merit compliance", "priority": 1},
                {"agent": "test-coverage-enforcer", "role": "Test word limits", "priority": 2},
                {"agent": "user-experience-guardian", "role": "Verify accessibility", "priority": 3}
            ])
        
        if "locality" in task_lower or "col" in task_lower:
            suggestions.extend([
                {"agent": "statistician-analyst", "role": "Analyze COL data", "priority": 1},
                {"agent": "data-scientist (from Agents)", "role": "Build predictive models", "priority": 2},
                {"agent": "FrontendEngineeringManager", "role": "Create visualizations", "priority": 3}
            ])
        
        return sorted(suggestions, key=lambda x: x["priority"])
    
    def validate_data_integrity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data against Fed Job Advisor requirements
        """
        
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "missing_critical": [],
            "data_quality_score": 100
        }
        
        # Check critical fields
        for field_name, field_info in self.critical_fields.items():
            if field_name not in data or data.get(field_name) is None:
                validation["valid"] = False
                validation["missing_critical"].append(field_name)
                validation["data_quality_score"] -= 20
        
        # Check for Fields=Full indicator
        if data.get("job_summary") is None or len(str(data.get("job_summary", ""))) < 100:
            validation["warnings"].append("job_summary appears truncated - Fields=Full may be missing")
            validation["data_quality_score"] -= 30
        
        # Validate salary data
        if data.get("salary_min", 0) < 15000:
            validation["errors"].append("Salary below federal minimum")
            validation["valid"] = False
        
        # Validate location data
        if data.get("location_data"):
            try:
                if isinstance(data["location_data"], str):
                    json.loads(data["location_data"])
            except:
                validation["errors"].append("Invalid location_data JSON")
                validation["valid"] = False
        
        return validation
    
    def provide_context_summary(self) -> str:
        """
        Provide a comprehensive context summary for Claude
        """
        
        return f"""
🎯 FED JOB ADVISOR CONTEXT SUMMARY

📊 DATA ARCHITECTURE:
- Critical Fields: {len(self.critical_fields)} tracked
- Locality Areas: {len(self.locality_areas)} official OPM zones
- Federal Keywords: {sum(len(v) for v in self.federal_keywords.values())} terms
- MANDATORY: Fields=Full in all API calls (prevents 93% data loss)

⚖️ MERIT HIRING COMPLIANCE:
- Rules: {len(self.merit_rules)} compliance requirements
- Word Limit: 200 words STRICT
- NEVER: Generate essay content
- ALWAYS: Require attestation
- Focus: STAR method structure

🚨 PROTECTED RESOURCES:
- Files: {len(self.constraints['protected_files'])} protected collectors
- Especially: collect_federal_jobs.py (DO NOT MODIFY)
- Environment: .env files are READ-ONLY

💰 LAUNCH STATUS:
- Target: {self.launch_status['target']}
- Phase: {self.launch_status['phase']}
- Critical Missing: Stripe integration
- Pricing: ${self.launch_status['pricing']['local']}/${self.launch_status['pricing']['mobile']}

⚠️ CONSTRAINTS:
- Developer: Solo (20 hrs/week)
- Budget: $0 for development
- Reality: 100 customers = success

📍 CURRENT PRIORITIES:
1. Stripe payment integration (CRITICAL)
2. Merit Hiring essay compliance
3. Data collection integrity
4. COL dashboard implementation
"""
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis method for agent system integration
        """
        
        # Extract the analysis type from data
        analysis_type = data.get("analysis_type", "general")
        
        if analysis_type == "data_request":
            return self.analyze_data_request(data.get("request", ""))
        elif analysis_type == "merit_compliance":
            return self.check_merit_compliance(data.get("action", ""))
        elif analysis_type == "collection_guidance":
            return self.get_data_collection_guidance()
        elif analysis_type == "agent_coordination":
            return {"suggestions": self.suggest_agent_coordination(data.get("task", ""))}
        elif analysis_type == "data_validation":
            return self.validate_data_integrity(data.get("data", {}))
        else:
            # General context summary
            return {
                "summary": self.provide_context_summary(),
                "critical_fields": len(self.critical_fields),
                "merit_rules": len(self.merit_rules),
                "protected_files": self.constraints["protected_files"],
                "launch_status": self.launch_status["phase"]
            }


# Export the agent class
__all__ = ["AgentRouter"]
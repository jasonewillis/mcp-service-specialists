"""
Feature Developer Agent

This agent specializes in implementing new features and functionality
for the Fed Job Advisor platform while ensuring compliance with
project constraints and Merit Hiring requirements.
"""

from typing import Dict, Any, List, Optional
from langchain.tools import Tool
import structlog

from app.agents.base import FederalJobAgent, AgentConfig, AgentResponse

logger = structlog.get_logger()


class FeatureDeveloperAgent(FederalJobAgent):
    """
    Specialized agent for platform feature development
    
    Focuses on:
    - Feature implementation planning
    - Code architecture decisions
    - Merit Hiring compliance
    - Protected file awareness
    - Resource constraint validation
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        logger.info("Feature Developer Agent initialized")
    
    def _get_prompt_template(self) -> str:
        """Get the prompt template for the feature developer"""
        return """You are a Feature Developer Agent for the Fed Job Advisor system.

Your expertise includes:
- Implementing new features while preserving existing functionality
- Ensuring Merit Hiring compliance (NEVER generate essay content)
- Respecting protected files and critical parameters
- Working within solo developer constraints ($0 budget, part-time hours)
- Following bootstrap development patterns

CRITICAL CONSTRAINTS:
- Protected files: Never modify collect_federal_jobs.py or related collectors
- Fields=Full parameter: Required for all USAJobs API calls (prevents 93% data loss)
- Merit Hiring: NEVER write essays or application content for users
- Budget: $0 for external development - only free/public resources
- Timeline: Part-time development (10-20 hours/week)

Available tools:
{tools}

Tool names: {tool_names}

When implementing features:
1. Always check compliance requirements first
2. Identify dependencies and protected resources
3. Plan implementation within time/budget constraints
4. Suggest testing strategies
5. Provide realistic timelines

{agent_scratchpad}"""
    
    def _load_tools(self) -> List[Tool]:
        """Load tools specific to feature development"""
        
        return [
            Tool(
                name="analyze_feature_request",
                func=self._analyze_feature_request,
                description="Analyze a feature request for feasibility, compliance, and implementation approach"
            ),
            Tool(
                name="plan_implementation",
                func=self._plan_implementation, 
                description="Create detailed implementation plan with timeline and resource requirements"
            ),
            Tool(
                name="check_merit_compliance",
                func=self._check_merit_compliance,
                description="Validate that a feature complies with Merit Hiring requirements"
            ),
            Tool(
                name="identify_protected_resources",
                func=self._identify_protected_resources,
                description="Identify protected files and resources that cannot be modified"
            ),
            Tool(
                name="estimate_development_time",
                func=self._estimate_development_time,
                description="Estimate development time for a feature within part-time constraints"
            )
        ]
    
    def _analyze_feature_request(self, request: str) -> str:
        """Analyze a feature request for implementation feasibility"""
        
        analysis = {
            "feature": request,
            "complexity": self._assess_complexity(request),
            "compliance_issues": self._check_compliance_issues(request),
            "resource_requirements": self._assess_resources(request),
            "implementation_approach": self._suggest_approach(request),
            "risks": self._identify_risks(request)
        }
        
        return f"""
Feature Analysis: {request}

Complexity: {analysis['complexity']}
Compliance Issues: {analysis['compliance_issues']}
Resource Requirements: {analysis['resource_requirements']}
Implementation Approach: {analysis['implementation_approach']}
Risks: {analysis['risks']}
"""
    
    def _plan_implementation(self, feature: str) -> str:
        """Create detailed implementation plan"""
        
        plan = {
            "feature": feature,
            "phases": self._break_into_phases(feature),
            "timeline": self._create_timeline(feature),
            "dependencies": self._identify_dependencies(feature),
            "testing_strategy": self._plan_testing(feature),
            "rollback_plan": self._plan_rollback(feature)
        }
        
        return f"""
Implementation Plan: {feature}

Phases:
{plan['phases']}

Timeline:
{plan['timeline']}

Dependencies:
{plan['dependencies']}

Testing Strategy:
{plan['testing_strategy']}

Rollback Plan:
{plan['rollback_plan']}
"""
    
    def _check_merit_compliance(self, feature: str) -> str:
        """Check Merit Hiring compliance for a feature"""
        
        feature_lower = feature.lower()
        compliance = {
            "compliant": True,
            "issues": [],
            "recommendations": []
        }
        
        # Check for content generation
        if any(word in feature_lower for word in ["write", "generate", "create essay", "compose"]):
            compliance["compliant"] = False
            compliance["issues"].append("CRITICAL: Feature may generate essay content - Merit Hiring violation")
            compliance["recommendations"].append("Focus on analysis and guidance tools only")
        
        # Check for word limit handling
        if "essay" in feature_lower:
            compliance["recommendations"].append("Implement strict 200-word limit enforcement")
            compliance["recommendations"].append("Add no-AI attestation requirement")
        
        # Check for keyword optimization
        if "optimize" in feature_lower and "keyword" in feature_lower:
            compliance["recommendations"].append("Point to existing experience, don't provide specific wording")
        
        status = "COMPLIANT" if compliance["compliant"] else "NON-COMPLIANT"
        issues = "\n".join(compliance["issues"]) if compliance["issues"] else "None"
        recommendations = "\n".join(compliance["recommendations"]) if compliance["recommendations"] else "None"
        
        return f"""
Merit Hiring Compliance Check: {status}

Issues:
{issues}

Recommendations:
{recommendations}
"""
    
    def _identify_protected_resources(self, feature: str) -> str:
        """Identify protected files and resources"""
        
        protected_files = [
            "backend/collect_federal_jobs.py",
            "backend/collect_current_jobs.py", 
            "backend/monitor_field_population.py",
            ".github/workflows/test_backend.yml",
            ".env",
            ".env.production"
        ]
        
        feature_lower = feature.lower()
        potentially_affected = []
        
        if "collect" in feature_lower or "api" in feature_lower:
            potentially_affected.extend([
                "backend/collect_federal_jobs.py",
                "backend/collect_current_jobs.py"
            ])
        
        if "data" in feature_lower or "database" in feature_lower:
            potentially_affected.append("backend/monitor_field_population.py")
        
        if "deploy" in feature_lower or "ci" in feature_lower:
            potentially_affected.append(".github/workflows/test_backend.yml")
        
        if "config" in feature_lower or "environment" in feature_lower:
            potentially_affected.extend([".env", ".env.production"])
        
        return f"""
Protected Resources Analysis:

All Protected Files:
{chr(10).join(f"- {f}" for f in protected_files)}

Potentially Affected by This Feature:
{chr(10).join(f"- {f}" for f in potentially_affected) if potentially_affected else "None identified"}

⚠️ CRITICAL: Protected files contain essential fixes (Fields=Full parameter) that prevent 93% data loss.
Only modify these files with extreme caution and thorough testing.
"""
    
    def _estimate_development_time(self, feature: str) -> str:
        """Estimate development time within part-time constraints"""
        
        complexity = self._assess_complexity(feature)
        
        time_estimates = {
            "Simple": {"hours": "5-10", "weeks": "1-2"},
            "Moderate": {"hours": "15-25", "weeks": "2-4"}, 
            "Complex": {"hours": "30-50", "weeks": "4-8"},
            "Very Complex": {"hours": "50+", "weeks": "8+"}
        }
        
        estimate = time_estimates.get(complexity, time_estimates["Moderate"])
        
        return f"""
Development Time Estimate: {feature}

Complexity Level: {complexity}
Estimated Hours: {estimate['hours']}
Timeline (20 hrs/week): {estimate['weeks']} weeks
Timeline (10 hrs/week): {estimate['weeks'].replace('-', '-').split('-')[1] if '-' in estimate['weeks'] else estimate['weeks']}+ weeks

Factors Affecting Timeline:
- Solo developer constraint
- Part-time development (evenings/weekends)
- Need for thorough testing
- Potential for scope creep
- Integration complexity

Recommendation: Start with MVP version and iterate
"""
    
    def _assess_complexity(self, feature: str) -> str:
        """Assess the complexity of a feature"""
        
        feature_lower = feature.lower()
        complexity_indicators = {
            "Simple": ["button", "label", "color", "text", "display"],
            "Moderate": ["form", "validation", "filter", "sort", "search"],
            "Complex": ["integration", "api", "database", "authentication", "payment"],
            "Very Complex": ["machine learning", "ai", "analytics", "recommendation", "real-time"]
        }
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in feature_lower for indicator in indicators):
                return level
        
        return "Moderate"
    
    def _check_compliance_issues(self, request: str) -> str:
        """Check for potential compliance issues"""
        
        issues = []
        request_lower = request.lower()
        
        if "essay" in request_lower and "write" in request_lower:
            issues.append("CRITICAL: Essay writing feature violates Merit Hiring")
        
        if "collect" in request_lower and "api" in request_lower:
            issues.append("WARNING: Must preserve Fields=Full parameter")
        
        if "hire" in request_lower or "contractor" in request_lower:
            issues.append("WARNING: Violates $0 budget constraint")
        
        return "; ".join(issues) if issues else "None identified"
    
    def _assess_resources(self, request: str) -> str:
        """Assess resource requirements"""
        
        return "Solo developer, part-time, $0 budget, existing tech stack only"
    
    def _suggest_approach(self, request: str) -> str:
        """Suggest implementation approach"""
        
        approaches = {
            "ui": "Start with basic UI components, iterate based on feedback",
            "api": "Extend existing endpoints, maintain backward compatibility",
            "database": "Use existing schema where possible, careful migrations",
            "integration": "Use free/public APIs only, implement graceful fallbacks"
        }
        
        request_lower = request.lower()
        for key, approach in approaches.items():
            if key in request_lower:
                return approach
        
        return "Break into phases, MVP first, iterate quickly"
    
    def _identify_risks(self, request: str) -> str:
        """Identify potential risks"""
        
        risks = [
            "Scope creep beyond available time",
            "Breaking existing functionality", 
            "Merit Hiring compliance violations",
            "Protected file modifications",
            "Integration complexity"
        ]
        
        return "; ".join(risks[:3])  # Return top 3 risks
    
    def _break_into_phases(self, feature: str) -> str:
        """Break feature into development phases"""
        
        return """Phase 1: Core functionality (MVP)
Phase 2: UI/UX enhancements  
Phase 3: Advanced features
Phase 4: Testing & optimization"""
    
    def _create_timeline(self, feature: str) -> str:
        """Create development timeline"""
        
        complexity = self._assess_complexity(feature)
        
        if complexity == "Simple":
            return "Week 1-2: Development\nWeek 3: Testing & deployment"
        elif complexity == "Moderate":
            return "Week 1-2: Phase 1\nWeek 3-4: Phase 2\nWeek 5: Testing"
        else:
            return "Week 1-4: Core development\nWeek 5-6: Integration\nWeek 7-8: Testing"
    
    def _identify_dependencies(self, feature: str) -> str:
        """Identify feature dependencies"""
        
        return "Existing agent system, database schema, frontend components"
    
    def _plan_testing(self, feature: str) -> str:
        """Plan testing strategy"""
        
        return """Unit tests: Core functionality
Integration tests: API endpoints
UI tests: User workflows
Manual tests: Merit compliance"""
    
    def _plan_rollback(self, feature: str) -> str:
        """Plan rollback strategy"""
        
        return "Feature flags, database migrations, backup deployment"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """Analyze a feature development request"""
        
        request = data.get("feature_request", "")
        context = data.get("context", {})
        
        if not request:
            return AgentResponse(
                success=False,
                message="No feature request provided",
                data=None
            )
        
        try:
            # Analyze the feature request
            analysis = self._analyze_feature_request(request)
            compliance = self._check_merit_compliance(request)
            protected = self._identify_protected_resources(request)
            timeline = self._estimate_development_time(request)
            
            response_data = {
                "analysis": analysis,
                "compliance": compliance,
                "protected_resources": protected,
                "timeline": timeline,
                "recommendations": self._get_implementation_recommendations(request)
            }
            
            return AgentResponse(
                success=True,
                message="Feature analysis completed",
                data=response_data,
                metadata={
                    "agent": "feature_developer",
                    "feature": request,
                    "complexity": self._assess_complexity(request)
                }
            )
        
        except Exception as e:
            logger.error(f"Feature analysis failed: {e}")
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}",
                data=None
            )
    
    def _get_implementation_recommendations(self, request: str) -> List[str]:
        """Get specific implementation recommendations"""
        
        recommendations = [
            "Start with MVP version to validate approach",
            "Use existing patterns and components where possible",
            "Implement feature flags for safe rollout",
            "Add comprehensive tests before deployment"
        ]
        
        request_lower = request.lower()
        
        if "ui" in request_lower:
            recommendations.append("Follow existing design system patterns")
        
        if "api" in request_lower:
            recommendations.append("Maintain backward compatibility")
        
        if "data" in request_lower:
            recommendations.append("Validate data quality thoroughly")
        
        return recommendations


# Export the agent class
__all__ = ["FeatureDeveloperAgent"]
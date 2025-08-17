"""
Project Context Manager Agent - Claude's Assistant
Helps Claude Code navigate complex project requirements and avoid critical mistakes
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import re
from pathlib import Path
import structlog

logger = structlog.get_logger()


class ProjectContextManagerAgent:
    """
    The agent Claude actually needs - manages project context, 
    prevents critical errors, and suggests optimal workflows
    """
    
    def __init__(self):
        self.project_root = Path("/Users/jasonewillis/Developer/jwRepos/JLWAI/fedJobAdvisor")
        self.protected_files = []
        self.launch_requirements = {}
        self.agent_registry = {}
        self.current_context = {}
        
        # Load critical project information
        self._load_project_context()
        
        logger.info("Project Context Manager initialized - Claude's assistant ready")
    
    def _load_project_context(self):
        """Load all critical project context"""
        
        # Protected files that must not be overwritten
        self.protected_files = [
            "backend/collect_federal_jobs.py",
            "backend/collect_current_jobs.py", 
            "backend/monitor_field_population.py",
            ".github/workflows/test_backend.yml"
        ]
        
        # Launch requirements
        self.launch_requirements = {
            "integrations_pending": [
                "Stripe payment processing",
                "Sentry error monitoring",
                "Slack notifications",
                "Google Analytics"
            ],
            "target_date": "Q1 2025",
            "pricing": {"local": 29, "mobile": 49},
            "status": "PRE-LAUNCH PREPARATION"
        }
        
        # Agent capabilities
        self.agent_registry = {
            "frontend": ["FrontendEngineeringManager", "user-experience-guardian"],
            "backend": ["DevOpsManager", "database-performance-tuner", "api-health-monitor"],
            "data": ["data-pipeline-guardian", "job-data-quality-analyst"],
            "testing": ["test-coverage-enforcer"],
            "project": ["project-manager", "project-historian", "codebase-archaeologist"]
        }
    
    def analyze_request(self, user_request: str) -> Dict[str, Any]:
        """
        Analyze user request and provide Claude with context and warnings
        """
        
        analysis = {
            "request_type": self._classify_request(user_request),
            "risks": [],
            "recommended_agents": [],
            "parallel_tasks": [],
            "warnings": [],
            "context_needed": [],
            "suggested_workflow": []
        }
        
        # Check for protected file risks
        if any(file in user_request.lower() for file in ["collect", "collector", "field"]):
            analysis["warnings"].append("⚠️ CRITICAL: This may affect protected data collectors")
            analysis["risks"].append("93% data loss if collectors are modified incorrectly")
            analysis["context_needed"].append("Check PROTECTED_FILES.md before proceeding")
        
        # Identify request type and recommend agents
        request_lower = user_request.lower()
        
        if "bug" in request_lower or "fix" in request_lower:
            analysis["request_type"] = "bug_fix"
            analysis["recommended_agents"] = [
                "FrontendEngineeringManager",
                "test-coverage-enforcer",
                "log-forensics-analyst"
            ]
            analysis["parallel_tasks"] = [
                "Diagnose issue",
                "Write tests", 
                "Check logs"
            ]
            
        elif "feature" in request_lower or "implement" in request_lower:
            analysis["request_type"] = "feature"
            analysis["recommended_agents"] = [
                "feature-impact-analyzer",
                "test-coverage-enforcer",
                "project-manager"
            ]
            analysis["parallel_tasks"] = [
                "Assess impact",
                "Implement feature",
                "Generate tests"
            ]
            
        elif "deploy" in request_lower or "production" in request_lower:
            analysis["request_type"] = "deployment"
            analysis["warnings"].append("⚠️ Production auto-deploys from main branch")
            analysis["context_needed"].append("Check render.yaml configuration")
            
        elif "payment" in request_lower or "stripe" in request_lower:
            analysis["request_type"] = "integration"
            analysis["warnings"].append("💰 Payment integration is launch-critical")
            analysis["context_needed"].append("Stripe test mode required before live")
            
        # Add workflow suggestions
        analysis["suggested_workflow"] = self._generate_workflow(analysis["request_type"])
        
        # Check current project status
        if self.launch_requirements["status"] == "PRE-LAUNCH PREPARATION":
            analysis["context_needed"].append(f"Launch target: {self.launch_requirements['target_date']}")
            analysis["context_needed"].append(f"Pending: {', '.join(self.launch_requirements['integrations_pending'][:2])}")
        
        return analysis
    
    def check_file_safety(self, file_path: str) -> Tuple[bool, str]:
        """
        Check if a file is safe to modify
        """
        
        for protected in self.protected_files:
            if protected in file_path:
                return False, f"PROTECTED FILE: {protected} - Contains Fields=Full fix for 93% data loss issue"
        
        return True, "Safe to modify"
    
    def suggest_parallel_execution(self, task: str) -> List[Dict[str, str]]:
        """
        Suggest parallel agent execution for a task
        """
        
        suggestions = []
        
        task_lower = task.lower()
        
        # Frontend task
        if any(word in task_lower for word in ["ui", "frontend", "react", "component"]):
            suggestions.append({
                "agent": "FrontendEngineeringManager",
                "task": "Implement UI changes",
                "priority": 1
            })
            suggestions.append({
                "agent": "user-experience-guardian",
                "task": "Verify mobile responsiveness",
                "priority": 2
            })
            suggestions.append({
                "agent": "test-coverage-enforcer",
                "task": "Generate component tests",
                "priority": 2
            })
        
        # Backend task
        if any(word in task_lower for word in ["api", "backend", "database", "endpoint"]):
            suggestions.append({
                "agent": "DevOpsManager",
                "task": "Implement backend changes",
                "priority": 1
            })
            suggestions.append({
                "agent": "database-performance-tuner",
                "task": "Optimize queries",
                "priority": 2
            })
            suggestions.append({
                "agent": "api-health-monitor",
                "task": "Verify API health",
                "priority": 3
            })
        
        # Data task
        if any(word in task_lower for word in ["data", "collection", "pipeline"]):
            suggestions.append({
                "agent": "data-pipeline-guardian",
                "task": "Monitor data flow",
                "priority": 1
            })
            suggestions.append({
                "agent": "job-data-quality-analyst",
                "task": "Validate data quality",
                "priority": 2
            })
        
        # Always add testing
        suggestions.append({
            "agent": "test-coverage-enforcer",
            "task": "Ensure test coverage",
            "priority": 3
        })
        
        # Sort by priority
        suggestions.sort(key=lambda x: x["priority"])
        
        return suggestions
    
    def generate_commit_message(self, changes: List[str]) -> str:
        """
        Generate proper commit message following project standards
        """
        
        # Analyze changes to determine type
        change_type = "feat"  # default
        
        if any("fix" in change.lower() for change in changes):
            change_type = "fix"
        elif any("test" in change.lower() for change in changes):
            change_type = "test"
        elif any("docs" in change.lower() for change in changes):
            change_type = "docs"
        
        # Generate scope
        scope = ""
        if any("frontend" in change.lower() for change in changes):
            scope = "frontend"
        elif any("backend" in change.lower() for change in changes):
            scope = "backend"
        elif any("agent" in change.lower() for change in changes):
            scope = "agents"
        
        # Create message
        summary = changes[0] if changes else "Update project"
        
        if scope:
            message = f"{change_type}({scope}): {summary}"
        else:
            message = f"{change_type}: {summary}"
        
        # Add body if multiple changes
        if len(changes) > 1:
            message += "\n\n"
            for change in changes[1:]:
                message += f"- {change}\n"
        
        return message
    
    def check_launch_readiness(self) -> Dict[str, Any]:
        """
        Check project launch readiness
        """
        
        readiness = {
            "ready": False,
            "completed": [],
            "pending": [],
            "critical": [],
            "progress_percentage": 0
        }
        
        # Check integrations
        for integration in self.launch_requirements["integrations_pending"]:
            if "stripe" in integration.lower():
                readiness["critical"].append(integration)
            else:
                readiness["pending"].append(integration)
        
        # Calculate progress
        total_tasks = 10  # Approximate
        completed_tasks = 6  # Based on current status
        readiness["progress_percentage"] = (completed_tasks / total_tasks) * 100
        
        readiness["ready"] = len(readiness["critical"]) == 0
        
        return readiness
    
    def get_documentation_context(self, topic: str) -> List[str]:
        """
        Get relevant documentation for a topic
        """
        
        docs_map = {
            "business": ["_Management/_PM/BusinessModel.md"],
            "launch": ["_Management/_PM/LAUNCH_READINESS_2025.md"],
            "agents": ["_Management/MASTER_AGENT_REGISTRY.md"],
            "security": ["SECURITY_IMPROVEMENTS.md"],
            "deployment": ["_Management/_PM/Deployment/DEPLOYMENT_GUIDE.md"],
            "protected": ["_Management/_PM/Security/PROTECTED_FILES.md"]
        }
        
        relevant_docs = []
        topic_lower = topic.lower()
        
        for key, docs in docs_map.items():
            if key in topic_lower:
                relevant_docs.extend(docs)
        
        return relevant_docs
    
    def _classify_request(self, request: str) -> str:
        """Classify the type of request"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["bug", "fix", "error", "broken"]):
            return "bug_fix"
        elif any(word in request_lower for word in ["feature", "implement", "add", "create"]):
            return "feature"
        elif any(word in request_lower for word in ["deploy", "production", "release"]):
            return "deployment"
        elif any(word in request_lower for word in ["test", "testing", "coverage"]):
            return "testing"
        elif any(word in request_lower for word in ["document", "docs", "readme"]):
            return "documentation"
        else:
            return "general"
    
    def _generate_workflow(self, request_type: str) -> List[str]:
        """Generate workflow steps based on request type"""
        
        workflows = {
            "bug_fix": [
                "1. Reproduce the issue",
                "2. Run diagnostic agents in parallel",
                "3. Implement fix",
                "4. Write tests",
                "5. Review with codebase-archaeologist",
                "6. Create PR with fix"
            ],
            "feature": [
                "1. Analyze with feature-impact-analyzer",
                "2. Check affected components",
                "3. Implement in parallel (frontend/backend)",
                "4. Generate tests",
                "5. Update documentation",
                "6. Create PR for review"
            ],
            "deployment": [
                "1. Check all tests pass",
                "2. Review DEPLOYMENT_GUIDE.md",
                "3. Verify environment variables",
                "4. Push to main branch",
                "5. Monitor Render dashboard",
                "6. Test production endpoints"
            ],
            "testing": [
                "1. Run test-coverage-enforcer",
                "2. Identify uncovered code",
                "3. Write missing tests",
                "4. Run full test suite",
                "5. Check CI/CD passes"
            ],
            "general": [
                "1. Clarify requirements",
                "2. Select appropriate agents",
                "3. Execute in parallel",
                "4. Review results",
                "5. Document changes"
            ]
        }
        
        return workflows.get(request_type, workflows["general"])
    
    def provide_claude_guidance(self, situation: str) -> str:
        """
        Provide specific guidance to Claude for common situations
        """
        
        guidance_map = {
            "starting_task": """
🎯 Before starting, I should:
1. Check if any protected files are involved
2. Identify which agents to run in parallel
3. Load relevant documentation context
4. Create a todo list for tracking
5. Consider the solo developer constraints
""",
            
            "fixing_bug": """
🐛 For this bug fix:
1. First reproduce the issue
2. Run these agents in parallel:
   - FrontendEngineeringManager (if UI)
   - log-forensics-analyst (check errors)
   - test-coverage-enforcer (prepare tests)
3. After fix, run tests and lint
4. Create PR with clear description
""",
            
            "adding_feature": """
✨ For this feature:
1. Run feature-impact-analyzer first
2. Check if it affects protected files
3. Remember: Solo dev, $0 budget
4. Keep it simple (10-20 hrs max)
5. Test thoroughly before committing
""",
            
            "before_deploy": """
🚀 Before deployment:
1. All tests must pass
2. Check protected files intact
3. Environment variables in Render
4. Remember: Auto-deploys from main
5. Monitor after deployment
"""
        }
        
        return guidance_map.get(situation, "Proceed with caution and check documentation")


def test_context_manager():
    """Test the Project Context Manager Agent"""
    
    print("🤖 Testing Project Context Manager Agent - Claude's Assistant")
    print("=" * 60)
    
    agent = ProjectContextManagerAgent()
    
    # Test 1: Analyze a request
    print("\n1️⃣ Analyzing user request:")
    request = "Fix the bug in job search and add COL dashboard feature"
    analysis = agent.analyze_request(request)
    print(f"Request: {request}")
    print(f"Type: {analysis['request_type']}")
    print(f"Recommended Agents: {', '.join(analysis['recommended_agents'][:3])}")
    print(f"Warnings: {analysis['warnings']}")
    
    # Test 2: Check file safety
    print("\n2️⃣ Checking file safety:")
    safe_file = "frontend/src/components/Dashboard.tsx"
    unsafe_file = "backend/collect_federal_jobs.py"
    
    safe, message = agent.check_file_safety(safe_file)
    print(f"✅ {safe_file}: {message}")
    
    safe, message = agent.check_file_safety(unsafe_file)
    print(f"❌ {unsafe_file}: {message}")
    
    # Test 3: Suggest parallel execution
    print("\n3️⃣ Parallel execution suggestions:")
    task = "Update frontend dashboard and optimize API performance"
    suggestions = agent.suggest_parallel_execution(task)
    for sug in suggestions[:4]:
        print(f"  • {sug['agent']}: {sug['task']}")
    
    # Test 4: Check launch readiness
    print("\n4️⃣ Launch readiness check:")
    readiness = agent.check_launch_readiness()
    print(f"Progress: {readiness['progress_percentage']}%")
    print(f"Critical pending: {', '.join(readiness['critical'])}")
    
    # Test 5: Get Claude guidance
    print("\n5️⃣ Guidance for Claude:")
    guidance = agent.provide_claude_guidance("fixing_bug")
    print(guidance)
    
    print("\n" + "=" * 60)
    print("✅ Project Context Manager Agent Ready to Assist Claude!")
    

if __name__ == "__main__":
    test_context_manager()
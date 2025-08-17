#!/usr/bin/env python3
"""
GitHub Specialist - Version Control and CI/CD Expert
Provides specialized GitHub integration and workflow guidance
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
from ..base_specialist import BaseSpecialist

class GitHubSpecialist(BaseSpecialist):
    """
    Specialist agent for GitHub operations and CI/CD workflows
    Focuses on repository management, Actions, and DevOps integration
    """
    
    def __init__(self):
        super().__init__()
        self.service_name = "github"
        self.specialization = "Version Control & CI/CD"
        
        self.core_expertise = [
            "Repository management and Git workflows",
            "GitHub Actions CI/CD pipelines", 
            "Branch protection and security policies",
            "Issue and PR automation",
            "GitHub API integration",
            "Deployment strategies and environments",
            "Code review workflows",
            "Repository security and secrets management"
        ]
        
        self.critical_practices = [
            "Never commit secrets or credentials",
            "Use branch protection rules for main branches",
            "Implement required status checks",
            "Use least privilege access for Actions",
            "Enable security alerts and dependency scanning",
            "Implement proper secret management",
            "Use environment-specific deployments",
            "Maintain clear branching strategies"
        ]
    
    async def analyze_repository_setup(self, repo_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and recommend GitHub repository configuration"""
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "repository": repo_config.get("name", "unknown"),
            "recommendations": [],
            "security_score": 100,
            "workflow_suggestions": [],
            "branch_strategy": self._analyze_branch_strategy(repo_config),
            "ci_cd_recommendations": self._generate_cicd_recommendations(repo_config)
        }
        
        # Analyze security settings
        if not repo_config.get("branch_protection", False):
            analysis["recommendations"].append("❌ Enable branch protection rules for main/master")
            analysis["security_score"] -= 20
        
        if not repo_config.get("required_reviews", False):
            analysis["recommendations"].append("❌ Require pull request reviews")
            analysis["security_score"] -= 15
        
        if not repo_config.get("security_alerts", False):
            analysis["recommendations"].append("❌ Enable security alerts and dependency scanning")
            analysis["security_score"] -= 25
        
        # Workflow suggestions
        if repo_config.get("project_type") == "web_app":
            analysis["workflow_suggestions"].extend([
                "Implement automated testing on PR",
                "Set up staging environment deployments",
                "Add code quality checks (linting, formatting)",
                "Configure automated dependency updates"
            ])
        
        analysis["overall_rating"] = "Excellent" if analysis["security_score"] >= 80 else "Needs Improvement"
        
        return analysis
    
    async def generate_workflow_template(self, project_type: str, deployment_target: str = "render") -> Dict[str, Any]:
        """Generate GitHub Actions workflow templates"""
        
        workflows = {
            "timestamp": datetime.now().isoformat(),
            "project_type": project_type,
            "deployment_target": deployment_target,
            "workflows": {}
        }
        
        # CI workflow for testing
        workflows["workflows"]["ci"] = self._generate_ci_workflow(project_type)
        
        # CD workflow for deployment
        workflows["workflows"]["cd"] = self._generate_cd_workflow(project_type, deployment_target)
        
        # Security workflow
        workflows["workflows"]["security"] = self._generate_security_workflow()
        
        workflows["setup_instructions"] = [
            "1. Create .github/workflows/ directory in your repository",
            "2. Add the generated workflow files",
            "3. Configure required secrets in repository settings",
            "4. Set up environment protection rules",
            "5. Test workflows with a pull request"
        ]
        
        return workflows
    
    async def review_github_actions(self, workflow_content: str) -> Dict[str, Any]:
        """Review GitHub Actions workflow for best practices"""
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "compliant": True,
            "violations": [],
            "passed": [],
            "score": 100,
            "security_issues": [],
            "optimization_suggestions": []
        }
        
        # Security checks
        if "${{" in workflow_content and "secrets." not in workflow_content:
            review["security_issues"].append("⚠️ Direct variable usage without secrets management")
            review["score"] -= 15
        
        if "actions/checkout@v" not in workflow_content:
            review["violations"].append("❌ Missing or outdated checkout action")
            review["score"] -= 10
        else:
            review["passed"].append("✅ Using checkout action")
        
        if "runs-on: ubuntu-latest" in workflow_content:
            review["passed"].append("✅ Using latest Ubuntu runner")
        
        # Best practices
        if "timeout-minutes" not in workflow_content:
            review["optimization_suggestions"].append("💡 Add timeout-minutes to prevent hanging jobs")
        
        if "if: github.event_name == 'pull_request'" in workflow_content:
            review["passed"].append("✅ Conditional execution on PR events")
        
        review["recommendation"] = "✅ Production Ready" if review["score"] >= 80 else "❌ Needs Improvement"
        
        return review
    
    async def suggest_branch_strategy(self, team_size: int, release_frequency: str) -> Dict[str, Any]:
        """Suggest optimal branching strategy based on team and release patterns"""
        
        strategy = {
            "timestamp": datetime.now().isoformat(),
            "team_size": team_size,
            "release_frequency": release_frequency,
            "recommended_strategy": "",
            "branch_structure": {},
            "protection_rules": {},
            "workflow_overview": []
        }
        
        if team_size <= 3 and release_frequency in ["daily", "continuous"]:
            strategy["recommended_strategy"] = "GitHub Flow (Simple)"
            strategy["branch_structure"] = {
                "main": "Production-ready code",
                "feature/*": "Feature development branches",
                "hotfix/*": "Emergency fixes"
            }
        elif team_size <= 10 and release_frequency in ["weekly", "bi-weekly"]:
            strategy["recommended_strategy"] = "Git Flow (Traditional)"
            strategy["branch_structure"] = {
                "main": "Production releases",
                "develop": "Integration branch",
                "feature/*": "Feature development",
                "release/*": "Release preparation",
                "hotfix/*": "Emergency fixes"
            }
        else:
            strategy["recommended_strategy"] = "GitLab Flow (Environment-based)"
            strategy["branch_structure"] = {
                "main": "Production",
                "staging": "Staging environment",
                "develop": "Development integration",
                "feature/*": "Feature branches"
            }
        
        strategy["protection_rules"] = {
            "main": ["Require PR reviews", "Require status checks", "Dismiss stale reviews"],
            "develop": ["Require status checks", "Allow force pushes by admins"],
            "staging": ["Require status checks"]
        }
        
        return strategy
    
    def _analyze_branch_strategy(self, repo_config: Dict) -> Dict[str, str]:
        """Analyze current branch strategy"""
        branches = repo_config.get("branches", ["main"])
        
        if "develop" in branches and "main" in branches:
            return {"type": "Git Flow", "complexity": "High", "suitable_for": "Large teams"}
        elif len(branches) <= 2:
            return {"type": "GitHub Flow", "complexity": "Low", "suitable_for": "Small teams"}
        else:
            return {"type": "Feature Branch", "complexity": "Medium", "suitable_for": "Medium teams"}
    
    def _generate_ci_workflow(self, project_type: str) -> str:
        """Generate CI workflow YAML"""
        if project_type == "nextjs":
            return """name: CI
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linting
        run: npm run lint
      
      - name: Run tests
        run: npm run test
      
      - name: Build application
        run: npm run build
"""
        elif project_type == "fastapi":
            return """name: CI
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest --cov=./
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
"""
        else:
            return """name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: echo "Add your test commands here"
"""
    
    def _generate_cd_workflow(self, project_type: str, deployment_target: str) -> str:
        """Generate CD workflow YAML"""
        if deployment_target == "render":
            return """name: Deploy to Render
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Render
        uses: bounceapp/render-action@0.6.0
        with:
          render-token: ${{ secrets.RENDER_TOKEN }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
"""
        else:
            return """name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: echo "Add your deployment commands here"
"""
    
    def _generate_security_workflow(self) -> str:
        """Generate security scanning workflow"""
        return """name: Security Scan
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
"""

# MCP Tool definitions
async def analyze_repository_setup(repo_config: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze GitHub repository configuration and provide security recommendations"""
    specialist = GitHubSpecialist()
    return await specialist.analyze_repository_setup(repo_config)

async def generate_workflow_template(project_type: str, deployment_target: str = "render") -> Dict[str, Any]:
    """Generate GitHub Actions workflow templates for CI/CD"""
    specialist = GitHubSpecialist()
    return await specialist.generate_workflow_template(project_type, deployment_target)

async def review_github_actions(workflow_content: str) -> Dict[str, Any]:
    """Review GitHub Actions workflows for best practices and security"""
    specialist = GitHubSpecialist()
    return await specialist.review_github_actions(workflow_content)

async def suggest_branch_strategy(team_size: int, release_frequency: str) -> Dict[str, Any]:
    """Suggest optimal Git branching strategy based on team size and release patterns"""
    specialist = GitHubSpecialist()
    return await specialist.suggest_branch_strategy(team_size, release_frequency)
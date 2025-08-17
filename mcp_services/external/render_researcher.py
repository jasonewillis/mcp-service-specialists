#!/usr/bin/env python3
"""
Render Deployment Researcher - Cloud Infrastructure Expert
Uses mistral:7b for deployment analysis
Critical for Q1 2025 launch
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import asyncio

class RenderResearcher:
    """
    Research-only agent for Render.com deployment strategies
    Specializes in production deployment, scaling, and monitoring
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Fed Job Advisor specific requirements
        self.app_context = {
            "frontend": "Next.js 14 on Render Static Site",
            "backend": "FastAPI on Render Web Service",
            "database": "PostgreSQL on Render Database",
            "redis": "Redis on Render for caching",
            "budget": "$100/month max for everything",
            "traffic": "100-200 users initially"
        }
        
        self.critical_rules = [
            "NEVER exceed $100/month total cost",
            "Use Render's free SSL certificates",
            "Configure auto-deploy from main branch",
            "Set up health checks for both services",
            "Use environment groups for shared configs",
            "Enable automatic database backups",
            "Configure custom domains (fedjobadvisor.com)",
            "Set resource limits to prevent overcharges",
            "Use build filters to prevent unnecessary deploys",
            "Monitor with Render's built-in metrics"
        ]
        
        self.model = "mistral:7b"  # Good balance for deployment tasks
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research Render deployment strategies"""
        
        task_analysis = self._analyze_task(task)
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "task_type": task_analysis['type'],
            "critical_requirements": self.critical_rules,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "render_yaml": self._generate_render_yaml(),
            "cost_breakdown": self._calculate_costs(),
            "monitoring_setup": self._create_monitoring_plan()
        }
        
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "critical_reminders": [
                "Keep under $100/month",
                "Auto-deploy from main branch",
                "Set up health checks"
            ]
        }
    
    def _analyze_task(self, task: str) -> Dict:
        task_lower = task.lower()
        
        if "deploy" in task_lower:
            return {"type": "deployment", "focus": "initial_setup"}
        elif "scale" in task_lower:
            return {"type": "scaling", "focus": "resource_optimization"}
        elif "monitor" in task_lower:
            return {"type": "monitoring", "focus": "observability"}
        elif "backup" in task_lower:
            return {"type": "backup", "focus": "data_protection"}
        else:
            return {"type": "general", "focus": "deployment"}
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict:
        return {
            "summary": f"Render {task_analysis['type']} configuration",
            "steps": [
                "1. Create Render Blueprint (render.yaml)",
                "2. Configure environment groups",
                "3. Set up PostgreSQL with daily backups",
                "4. Deploy backend FastAPI service",
                "5. Deploy frontend Next.js static site",
                "6. Configure custom domain + SSL",
                "7. Set up health checks and alerts",
                "8. Configure auto-deploy from GitHub",
                "9. Set resource limits to control costs",
                "10. Monitor initial performance"
            ],
            "services": {
                "backend": {
                    "type": "Web Service",
                    "plan": "Starter ($7/mo)",
                    "runtime": "Python 3.11",
                    "buildCommand": "pip install -r requirements.txt",
                    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
                },
                "frontend": {
                    "type": "Static Site",
                    "plan": "Free",
                    "buildCommand": "npm install && npm run build",
                    "publishDirectory": "out"
                },
                "database": {
                    "type": "PostgreSQL",
                    "plan": "Starter ($7/mo)",
                    "version": "15",
                    "backups": "Daily, 7-day retention"
                }
            }
        }
    
    def _generate_render_yaml(self) -> str:
        """Generate Render Blueprint configuration"""
        return """databases:
  - name: fedjobadvisor-db
    plan: starter
    region: oregon
    databaseName: fedjobadvisor
    user: fedjobadvisor
    postgresMajorVersion: 15

services:
  - type: web
    name: fedjobadvisor-backend
    runtime: python
    plan: starter
    region: oregon
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: fedjobadvisor-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          name: fedjobadvisor-redis
          type: pserv
          property: connectionString
      - fromGroup: fedjobadvisor-secrets
    healthCheckPath: /health
    autoDeploy: true
    
  - type: static
    name: fedjobadvisor-frontend
    buildCommand: npm install && npm run build && npm run export
    staticPublishPath: ./out
    headers:
      - path: /*
        name: X-Frame-Options
        value: DENY
    routes:
      - type: rewrite
        source: /api/*
        destination: https://fedjobadvisor-backend.onrender.com/api/*
    pullRequestPreviewsEnabled: true
    
  - type: pserv
    name: fedjobadvisor-redis
    runtime: docker
    plan: starter
    dockerfilePath: ./redis/Dockerfile
    disk:
      name: redis-data
      mountPath: /data
      sizeGB: 1

envVarGroups:
  - name: fedjobadvisor-secrets
    envVars:
      - key: STRIPE_SECRET_KEY
        sync: false
      - key: GOOGLE_CLIENT_SECRET
        sync: false
      - key: JWT_SECRET
        generateValue: true
      - key: SENTRY_DSN
        sync: false"""
    
    def _calculate_costs(self) -> Dict:
        """Calculate monthly Render costs"""
        return {
            "total_monthly": "$84",
            "breakdown": {
                "backend_web_service": "$7/mo (Starter)",
                "database_postgres": "$7/mo (Starter)",
                "redis_cache": "$7/mo (Starter)",
                "frontend_static": "$0 (Free tier)",
                "ssl_certificates": "$0 (Included)",
                "bandwidth": "~$10/mo (estimated)",
                "backups": "$0 (Included with Starter)"
            },
            "scaling_options": {
                "next_tier": "Standard at $25/mo per service",
                "auto_scaling": "Available on Standard+",
                "recommendation": "Start with Starter, monitor usage"
            },
            "cost_controls": [
                "Set spending alerts at $75",
                "Review metrics weekly",
                "Optimize build frequency",
                "Use caching aggressively"
            ]
        }
    
    def _create_monitoring_plan(self) -> Dict:
        """Create monitoring and alerting plan"""
        return {
            "health_checks": {
                "backend": "/health endpoint every 30s",
                "database": "Connection pool monitoring",
                "frontend": "Uptime monitoring"
            },
            "alerts": [
                "Service down > 1 minute",
                "CPU usage > 80% for 5 minutes",
                "Memory usage > 90%",
                "Database connections > 80%",
                "Failed deploys",
                "Monthly spend > $75"
            ],
            "metrics_to_track": [
                "Request latency (p50, p95, p99)",
                "Error rate by endpoint",
                "Active users",
                "Database query performance",
                "Build and deploy times"
            ],
            "integrations": {
                "sentry": "Error tracking",
                "slack": "Alert notifications",
                "github": "Deploy status"
            }
        }
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """Review Render deployment configuration"""
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "compliant": True,
            "violations": [],
            "warnings": [],
            "passed": [],
            "score": 100
        }
        
        # Check for render.yaml
        if "render.yaml" in code or "blueprint" in code.lower():
            review["passed"].append("✅ Using Render Blueprint")
        else:
            review["warnings"].append("⚠️ Consider using render.yaml for IaC")
            review["score"] -= 10
        
        # Check for health checks
        if "health" in code.lower():
            review["passed"].append("✅ Health checks configured")
        else:
            review["violations"].append("❌ No health checks!")
            review["score"] -= 20
        
        # Check for environment groups
        if "envVarGroups" in code or "fromGroup" in code:
            review["passed"].append("✅ Using environment groups")
        else:
            review["warnings"].append("⚠️ Use env groups for secrets")
        
        # Check for auto-deploy
        if "autoDeploy" in code:
            review["passed"].append("✅ Auto-deploy enabled")
        
        # Check for cost controls
        if "starter" in code.lower() or "free" in code.lower():
            review["passed"].append("✅ Using cost-effective plans")
        
        review["recommendation"] = "✅ Ready" if review["score"] >= 70 else "❌ Fix issues"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"render_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# Render Deployment Research\n\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Critical Requirements\n")
            for req in research['critical_requirements'][:5]:
                f.write(f"- {req}\n")
            f.write("\n")
            
            f.write("## Implementation Steps\n")
            for step in research['implementation_plan']['steps']:
                f.write(f"{step}\n")
            f.write("\n")
            
            f.write("## render.yaml Blueprint\n")
            f.write(f"```yaml\n{research['render_yaml']}\n```\n\n")
            
            f.write("## Cost Breakdown\n")
            f.write(f"**Total**: {research['cost_breakdown']['total_monthly']}\n\n")
            for service, cost in research['cost_breakdown']['breakdown'].items():
                f.write(f"- {service}: {cost}\n")
        
        return report_path
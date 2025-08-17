#!/usr/bin/env python3
"""
Render Deployment Specialist - Ultra-deep expertise in Render.com platform
Uses qwen2.5-coder:7b for deployment optimization and troubleshooting
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio
from enum import Enum

class RenderServiceType(Enum):
    """Render.com service types"""
    WEB_SERVICE = "web_service"
    PRIVATE_SERVICE = "private_service"
    BACKGROUND_WORKER = "background_worker"
    CRON_JOB = "cron_job"
    STATIC_SITE = "static_site"
    POSTGRESQL = "postgresql"
    REDIS = "redis"

class RenderSpecialist:
    """
    Ultra-specialized agent for Render.com deployment and optimization
    Complete knowledge of Render platform for Fed Job Advisor
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "render"
        self.research_output = self.base_path / "research_outputs" / "render_deployments"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Exhaustive Render.com knowledge base
        self.knowledge_base = {
            "deployment_patterns": {
                "zero_downtime": {
                    "health_checks": "/api/health",
                    "preboot": True,
                    "deploy_strategy": "rolling",
                    "min_instances": 1
                },
                "blue_green": {
                    "preview_environments": True,
                    "traffic_splitting": True,
                    "rollback_strategy": "instant"
                },
                "monorepo": {
                    "build_filters": ["frontend/**", "backend/**"],
                    "root_directory": ".",
                    "dockerfile_path": "./Dockerfile"
                }
            },
            
            "environment_variables": {
                "best_practices": [
                    "Use environment groups for shared configs",
                    "Separate secrets from config",
                    "Use sync environments for staging/prod parity",
                    "Never commit .env files"
                ],
                "secret_management": {
                    "database_url": "Use internal connection string",
                    "api_keys": "Store in secret files",
                    "certificates": "Use Render disk for persistence"
                }
            },
            
            "build_optimization": {
                "docker": {
                    "layer_caching": True,
                    "multi_stage_builds": True,
                    "build_command": "docker build",
                    "ignored_files": [".git", "node_modules", "__pycache__"]
                },
                "native": {
                    "build_command": "npm install && npm run build",
                    "cache_directories": ["node_modules", ".next/cache"]
                },
                "python": {
                    "build_command": "pip install -r requirements.txt",
                    "python_version": "3.11",
                    "poetry_support": True
                }
            },
            
            "scaling_strategies": {
                "autoscaling": {
                    "min_instances": 1,
                    "max_instances": 10,
                    "target_cpu": 70,
                    "target_memory": 80,
                    "scale_up_rate": 1,
                    "scale_down_delay": 300
                },
                "manual_scaling": {
                    "instance_types": ["starter", "standard", "performance", "performance_plus"],
                    "memory_limits": {"starter": "512MB", "standard": "2GB", "performance": "4GB", "performance_plus": "8GB"},
                    "cpu_limits": {"starter": "0.5", "standard": "1", "performance": "2", "performance_plus": "4"}
                }
            },
            
            "database_configuration": {
                "postgresql": {
                    "versions": ["14", "15", "16"],
                    "connection_pooling": True,
                    "max_connections": 97,
                    "backup_schedule": "daily",
                    "point_in_time_recovery": True
                },
                "redis": {
                    "eviction_policy": "allkeys-lru",
                    "maxmemory_policy": "noeviction",
                    "persistence": "RDB + AOF"
                }
            },
            
            "monitoring_alerts": {
                "health_checks": {
                    "endpoint": "/api/health",
                    "interval": 30,
                    "timeout": 10,
                    "failure_threshold": 3
                },
                "metrics": {
                    "cpu_alert": 80,
                    "memory_alert": 90,
                    "disk_alert": 85,
                    "response_time_alert": 2000
                },
                "notifications": {
                    "email": True,
                    "slack": True,
                    "pagerduty": False
                }
            },
            
            "common_errors": {
                "build_failures": {
                    "out_of_memory": "Increase build instance size or optimize build",
                    "timeout": "Extend build timeout or optimize build steps",
                    "missing_dependencies": "Check package.json or requirements.txt",
                    "docker_errors": "Verify Dockerfile syntax and base image"
                },
                "runtime_errors": {
                    "port_binding": "Use PORT environment variable",
                    "health_check_failures": "Verify endpoint returns 200",
                    "memory_exceeded": "Optimize app or upgrade instance",
                    "connection_refused": "Check internal networking and service discovery"
                },
                "deployment_errors": {
                    "rollback_triggered": "Check logs for startup errors",
                    "preview_env_failure": "Verify branch protection rules",
                    "sync_env_mismatch": "Ensure environment variables match"
                }
            },
            
            "cost_optimization": {
                "strategies": [
                    "Use autoscaling instead of fixed high-tier instances",
                    "Implement caching to reduce compute",
                    "Use static sites for frontend when possible",
                    "Consolidate background workers",
                    "Right-size database instances"
                ],
                "pricing_tiers": {
                    "individual": {"free_tier": True, "price": "$0-19/mo"},
                    "team": {"collaboration": True, "price": "$19+/mo"},
                    "organization": {"sso": True, "price": "custom"}
                }
            },
            
            "ci_cd_integration": {
                "github": {
                    "auto_deploy": True,
                    "branch_deploys": True,
                    "pr_previews": True,
                    "deploy_hooks": True
                },
                "gitlab": {
                    "auto_deploy": True,
                    "branch_deploys": True
                },
                "api_deployment": {
                    "deploy_key": "Required for API deploys",
                    "webhook_url": "https://api.render.com/deploy/srv-xxx"
                }
            },
            
            "render_yaml_configuration": {
                "structure": {
                    "version": 1,
                    "services": [],
                    "databases": [],
                    "envVarGroups": []
                },
                "service_config": {
                    "type": "web",
                    "env": "docker",
                    "plan": "standard",
                    "healthCheckPath": "/api/health",
                    "autoDeploy": True,
                    "domains": []
                }
            }
        }
        
        # Fed Job Advisor specific Render configuration
        self.fja_config = {
            "frontend": {
                "service_name": "fedjobadvisor-frontend",
                "type": "static_site",
                "build_command": "npm run build",
                "publish_directory": "out",
                "environment": {
                    "NODE_VERSION": "18",
                    "NEXT_PUBLIC_API_URL": "https://fedjobadvisor-backend.onrender.com"
                }
            },
            "backend": {
                "service_name": "fedjobadvisor-backend",
                "type": "web_service",
                "runtime": "python-3.11",
                "build_command": "pip install -r requirements.txt",
                "start_command": "uvicorn main:app --host 0.0.0.0 --port $PORT",
                "health_check_path": "/api/health"
            },
            "database": {
                "service_name": "fedjobadvisor-db",
                "type": "postgresql",
                "version": "15",
                "plan": "standard",
                "high_availability": False
            }
        }
    
    async def analyze_deployment_issue(self, error_log: str, service_type: str = "web_service") -> Dict[str, Any]:
        """
        Analyze Render deployment errors with deep platform knowledge
        """
        timestamp = datetime.now().isoformat()
        
        # Pattern matching for common Render errors
        error_patterns = {
            "Build failed": self._analyze_build_failure,
            "Health check failed": self._analyze_health_check_failure,
            "Out of memory": self._analyze_memory_issue,
            "Port": self._analyze_port_binding_issue,
            "Environment variable": self._analyze_env_var_issue,
            "Docker": self._analyze_docker_issue,
            "Timeout": self._analyze_timeout_issue,
            "Permission denied": self._analyze_permission_issue
        }
        
        analysis = {
            "timestamp": timestamp,
            "service_type": service_type,
            "error_log": error_log[:500],  # First 500 chars
            "identified_issues": [],
            "solutions": [],
            "render_specific_fixes": []
        }
        
        # Identify issues
        for pattern, analyzer in error_patterns.items():
            if pattern.lower() in error_log.lower():
                issue_analysis = analyzer(error_log)
                analysis["identified_issues"].append(issue_analysis["issue"])
                analysis["solutions"].extend(issue_analysis["solutions"])
                analysis["render_specific_fixes"].extend(issue_analysis["render_fixes"])
        
        # If no specific pattern matched, provide general guidance
        if not analysis["identified_issues"]:
            analysis["identified_issues"] = ["Unidentified deployment issue"]
            analysis["solutions"] = [
                "Check Render dashboard logs for more details",
                "Verify service configuration in render.yaml",
                "Ensure all environment variables are set",
                "Check if the service has sufficient resources"
            ]
        
        # Save analysis
        output_file = self.research_output / f"{timestamp}_deployment_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return analysis
    
    def _analyze_build_failure(self, error_log: str) -> Dict[str, Any]:
        """Analyze build-specific failures"""
        return {
            "issue": "Build failure detected",
            "solutions": [
                "Check if all dependencies are specified in requirements.txt or package.json",
                "Verify Docker base image is available",
                "Ensure build command is correct in render.yaml",
                "Check for syntax errors in Dockerfile"
            ],
            "render_fixes": [
                "Increase build timeout in Render dashboard > Settings > Build & Deploy",
                "Clear build cache in Render dashboard > Settings > Clear build cache",
                "Try using a different build instance type for more memory"
            ]
        }
    
    def _analyze_health_check_failure(self, error_log: str) -> Dict[str, Any]:
        """Analyze health check failures"""
        return {
            "issue": "Health check endpoint not responding",
            "solutions": [
                "Ensure health check endpoint returns HTTP 200",
                "Verify the path matches render.yaml healthCheckPath",
                "Check if service is binding to 0.0.0.0:$PORT",
                "Add logging to health check endpoint"
            ],
            "render_fixes": [
                "Temporarily disable health checks to debug",
                "Increase health check timeout in render.yaml",
                "Use /api/health as standard endpoint",
                "Check 'Logs' tab during deployment for startup errors"
            ]
        }
    
    def _analyze_memory_issue(self, error_log: str) -> Dict[str, Any]:
        """Analyze memory-related issues"""
        return {
            "issue": "Service running out of memory",
            "solutions": [
                "Optimize application memory usage",
                "Implement pagination for large datasets",
                "Add memory limits to prevent crashes",
                "Use streaming for large file operations"
            ],
            "render_fixes": [
                "Upgrade to higher instance type (Standard -> Performance)",
                "Enable autoscaling to distribute load",
                "Set memory limits in Docker container",
                "Monitor memory usage in Metrics tab"
            ]
        }
    
    def _analyze_port_binding_issue(self, error_log: str) -> Dict[str, Any]:
        """Analyze port binding issues"""
        return {
            "issue": "Service not binding to correct port",
            "solutions": [
                "Use PORT environment variable: os.environ.get('PORT', 8000)",
                "Bind to 0.0.0.0 not localhost or 127.0.0.1",
                "For FastAPI: --host 0.0.0.0 --port $PORT",
                "For Next.js: next start -p $PORT"
            ],
            "render_fixes": [
                "PORT is automatically set by Render",
                "Don't hardcode port numbers",
                "Check Start Command in render.yaml",
                "Verify service type matches application"
            ]
        }
    
    def _analyze_env_var_issue(self, error_log: str) -> Dict[str, Any]:
        """Analyze environment variable issues"""
        return {
            "issue": "Missing or incorrect environment variables",
            "solutions": [
                "List all required env vars in documentation",
                "Use environment groups for shared variables",
                "Add defaults for non-critical variables",
                "Validate env vars on startup"
            ],
            "render_fixes": [
                "Check Environment tab in Render dashboard",
                "Use Secret Files for sensitive data",
                "Sync environments between services",
                "Use render.yaml envVarGroups for consistency"
            ]
        }
    
    def _analyze_docker_issue(self, error_log: str) -> Dict[str, Any]:
        """Analyze Docker-related issues"""
        return {
            "issue": "Docker build or runtime error",
            "solutions": [
                "Verify Dockerfile syntax",
                "Use official base images",
                "Implement multi-stage builds",
                "Check file permissions in container"
            ],
            "render_fixes": [
                "Enable Docker layer caching",
                "Use .dockerignore to exclude files",
                "Set dockerfilePath in render.yaml",
                "Check Docker build logs in dashboard"
            ]
        }
    
    def _analyze_timeout_issue(self, error_log: str) -> Dict[str, Any]:
        """Analyze timeout issues"""
        return {
            "issue": "Request or build timeout",
            "solutions": [
                "Optimize slow operations",
                "Implement async processing",
                "Add caching layers",
                "Break up large operations"
            ],
            "render_fixes": [
                "Increase timeout in Settings > Advanced",
                "Use background workers for long tasks",
                "Implement request queuing",
                "Add CDN for static assets"
            ]
        }
    
    def _analyze_permission_issue(self, error_log: str) -> Dict[str, Any]:
        """Analyze permission issues"""
        return {
            "issue": "File or directory permission error",
            "solutions": [
                "Set correct file permissions in Dockerfile",
                "Use non-root user in container",
                "Check write permissions for temp directories",
                "Verify database connection permissions"
            ],
            "render_fixes": [
                "Use Render Disks for persistent storage",
                "Don't write to container filesystem",
                "Use /tmp for temporary files",
                "Check database user permissions"
            ]
        }
    
    async def optimize_render_yaml(self, current_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize render.yaml configuration for Fed Job Advisor
        """
        optimized = current_config.copy()
        
        recommendations = []
        
        # Check services configuration
        for service in optimized.get("services", []):
            # Optimize instance type
            if service.get("plan") == "free":
                recommendations.append(f"Consider upgrading {service['name']} to 'starter' plan for better reliability")
            
            # Add health checks if missing
            if service["type"] == "web" and not service.get("healthCheckPath"):
                service["healthCheckPath"] = "/api/health"
                recommendations.append(f"Added health check to {service['name']}")
            
            # Enable autoscaling for production
            if service.get("plan") in ["standard", "performance"]:
                if not service.get("scaling"):
                    service["scaling"] = {
                        "minInstances": 1,
                        "maxInstances": 3,
                        "targetMemoryPercent": 80,
                        "targetCPUPercent": 70
                    }
                    recommendations.append(f"Enabled autoscaling for {service['name']}")
            
            # Add preview environments
            if not service.get("pullRequestPreviewsEnabled"):
                service["pullRequestPreviewsEnabled"] = "yes"
                recommendations.append(f"Enabled PR previews for {service['name']}")
        
        # Check databases
        for db in optimized.get("databases", []):
            # Ensure backups are enabled
            if not db.get("ipAllowList"):
                recommendations.append(f"Consider adding IP allowlist to {db['name']} for security")
            
            # Check plan
            if db.get("plan") == "free":
                recommendations.append(f"Free database {db['name']} has limitations - consider 'starter' for production")
        
        return {
            "optimized_config": optimized,
            "recommendations": recommendations,
            "estimated_monthly_cost": self._estimate_cost(optimized)
        }
    
    def _estimate_cost(self, config: Dict[str, Any]) -> str:
        """Estimate monthly Render costs"""
        total = 0
        
        # Service costs
        plan_costs = {
            "free": 0,
            "starter": 7,
            "standard": 25,
            "performance": 85,
            "performance_plus": 175
        }
        
        for service in config.get("services", []):
            plan = service.get("plan", "free")
            instances = service.get("scaling", {}).get("minInstances", 1)
            total += plan_costs.get(plan, 0) * instances
        
        # Database costs
        db_costs = {
            "free": 0,
            "starter": 7,
            "standard": 20,
            "pro": 60
        }
        
        for db in config.get("databases", []):
            plan = db.get("plan", "free")
            total += db_costs.get(plan, 0)
        
        return f"${total}/month (estimated)"
    
    async def generate_deployment_guide(self, project_type: str = "fed_job_advisor") -> str:
        """
        Generate comprehensive Render deployment guide
        """
        timestamp = datetime.now().isoformat()
        
        guide = f"""# Render.com Deployment Guide for Fed Job Advisor
Generated: {timestamp}

## Quick Start Deployment

### 1. Initial Setup
```bash
# Install Render CLI (optional but recommended)
brew install render

# Login to Render
render login
```

### 2. Create render.yaml
```yaml
version: 1
services:
  # Frontend Service
  - type: web
    name: fedjobadvisor-frontend
    runtime: node
    repo: https://github.com/yourusername/fedjobadvisor
    buildCommand: cd frontend && npm install && npm run build
    startCommand: cd frontend && npm start
    healthCheckPath: /
    envVars:
      - key: NODE_VERSION
        value: 18
      - key: NEXT_PUBLIC_API_URL
        value: https://fedjobadvisor-backend.onrender.com
    
  # Backend Service  
  - type: web
    name: fedjobadvisor-backend
    runtime: python
    repo: https://github.com/yourusername/fedjobadvisor
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /api/health
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: DATABASE_URL
        fromDatabase:
          name: fedjobadvisor-db
          property: connectionString

databases:
  - name: fedjobadvisor-db
    plan: standard
    postgresMajorVersion: 15
```

### 3. Environment Variables Setup

#### Required Variables (Backend)
- `DATABASE_URL` - Auto-populated from database
- `JWT_SECRET` - Generate with: openssl rand -hex 32
- `STRIPE_SECRET_KEY` - From Stripe dashboard
- `STRIPE_WEBHOOK_SECRET` - From Stripe webhook settings
- `SENTRY_DSN` - From Sentry project settings
- `GOOGLE_CLIENT_ID` - From Google Cloud Console
- `GOOGLE_CLIENT_SECRET` - From Google Cloud Console

#### Required Variables (Frontend)
- `NEXT_PUBLIC_API_URL` - Your backend URL
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - From Stripe
- `NEXT_PUBLIC_GA_MEASUREMENT_ID` - From Google Analytics
- `NEXT_PUBLIC_SENTRY_DSN` - From Sentry

### 4. Deployment Commands

```bash
# Deploy using render.yaml
git add render.yaml
git commit -m "Add Render configuration"
git push origin main

# Or deploy via dashboard
# 1. Go to https://dashboard.render.com
# 2. New > Web Service/Static Site
# 3. Connect GitHub repo
# 4. Configure and deploy
```

## Production Optimizations

### Enable Autoscaling
```yaml
scaling:
  minInstances: 1
  maxInstances: 5
  targetMemoryPercent: 80
  targetCPUPercent: 70
```

### Configure Health Checks
```python
# FastAPI health endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "fedjobadvisor-backend"
    }
```

### Implement Zero-Downtime Deployments
1. Enable preview environments
2. Use health checks
3. Configure preboot
4. Implement graceful shutdown

### Database Optimization
```sql
-- Create indexes for common queries
CREATE INDEX idx_jobs_posted_date ON jobs(date_posted);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_users_email ON users(email);

-- Enable connection pooling
-- Set in Render dashboard > Database > Settings
```

## Monitoring & Alerts

### Set Up Alerts
1. Go to Settings > Notifications
2. Configure alerts for:
   - High CPU usage (>80%)
   - High memory usage (>90%)
   - Failed deploys
   - Health check failures

### Enable Logging
```python
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Cost Optimization Tips

1. **Use Autoscaling** instead of fixed high-tier instances
2. **Implement Caching** with Redis to reduce compute
3. **Optimize Images** and static assets
4. **Use CDN** for static files (Cloudflare)
5. **Schedule Background Jobs** during off-peak hours
6. **Right-size Database** based on actual usage

## Troubleshooting Common Issues

### Build Failures
- Check build logs in dashboard
- Verify all dependencies are listed
- Clear build cache if needed
- Increase build timeout

### Service Won't Start
- Check start command syntax
- Verify PORT binding
- Review environment variables
- Check health endpoint

### Database Connection Issues
- Use internal connection string
- Check IP allowlist
- Verify credentials
- Test with render shell

### High Memory Usage
- Implement pagination
- Add memory limits
- Optimize queries
- Upgrade instance type

## Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Enable IP allowlisting** for databases
3. **Use secret files** for sensitive configs
4. **Implement rate limiting** on APIs
5. **Enable DDoS protection** via Cloudflare
6. **Regular security updates** for dependencies

## Render CLI Commands

```bash
# List services
render services list

# View logs
render logs -s fedjobadvisor-backend

# SSH into service
render shell -s fedjobadvisor-backend

# Trigger manual deploy
render deploy -s fedjobadvisor-backend

# Scale service
render scale -s fedjobadvisor-backend --min 2 --max 5
```

## Support Resources

- [Render Documentation](https://render.com/docs)
- [Render Status Page](https://status.render.com)
- [Community Forum](https://community.render.com)
- Support Email: support@render.com

---
*Generated by Render Deployment Specialist Agent*
"""
        
        # Save guide
        output_file = self.research_output / f"{timestamp}_deployment_guide.md"
        with open(output_file, 'w') as f:
            f.write(guide)
        
        return guide
    
    async def analyze_metrics(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze Render service metrics and provide optimization recommendations
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics_data,
            "recommendations": [],
            "alerts": [],
            "cost_savings": []
        }
        
        # CPU analysis
        if metrics_data.get("cpu_percent", 0) > 80:
            analysis["alerts"].append("High CPU usage detected")
            analysis["recommendations"].append("Consider scaling up or optimizing code")
        elif metrics_data.get("cpu_percent", 0) < 20:
            analysis["cost_savings"].append("CPU underutilized - consider smaller instance")
        
        # Memory analysis
        if metrics_data.get("memory_percent", 0) > 90:
            analysis["alerts"].append("Critical memory usage")
            analysis["recommendations"].append("Upgrade instance or optimize memory usage")
        
        # Response time analysis
        if metrics_data.get("response_time_ms", 0) > 1000:
            analysis["recommendations"].append("Slow response times - add caching or optimize queries")
        
        return analysis

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    specialist = RenderSpecialist()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analyze":
            # Example: python render_specialist.py analyze "error log content"
            if len(sys.argv) > 2:
                error_log = sys.argv[2]
                result = asyncio.run(specialist.analyze_deployment_issue(error_log))
                print(json.dumps(result, indent=2))
        
        elif command == "guide":
            # Generate deployment guide
            guide = asyncio.run(specialist.generate_deployment_guide())
            print(guide)
        
        elif command == "optimize":
            # Example: python render_specialist.py optimize config.yaml
            if len(sys.argv) > 2:
                with open(sys.argv[2], 'r') as f:
                    config = json.load(f)
                result = asyncio.run(specialist.optimize_render_yaml(config))
                print(json.dumps(result, indent=2))
    else:
        print("Render Deployment Specialist")
        print("Commands:")
        print("  analyze <error_log> - Analyze deployment error")
        print("  guide - Generate deployment guide")
        print("  optimize <config.yaml> - Optimize render.yaml")
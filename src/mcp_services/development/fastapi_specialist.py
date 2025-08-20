#!/usr/bin/env python3
"""
FastAPI Specialist - Modern Python API Framework Expert
Provides specialized guidance for FastAPI applications with async patterns
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
from ..base_specialist import BaseSpecialist

class FastAPISpecialist(BaseSpecialist):
    """
    Specialist agent for FastAPI applications and async Python development
    Focuses on API design, performance, security, and deployment
    """
    
    def __init__(self):
        super().__init__()
        self.service_name = "fastapi"
        self.specialization = "Python API Development & Async Programming"
        
        self.core_expertise = [
            "FastAPI application architecture and design patterns",
            "Async/await programming and performance optimization",
            "Pydantic models and data validation",
            "Authentication and authorization (JWT, OAuth2)",
            "Database integration with SQLAlchemy and Alembic",
            "API documentation with OpenAPI/Swagger",
            "Testing with pytest and async test patterns",
            "Production deployment and monitoring"
        ]
        
        self.best_practices = [
            "Use dependency injection for clean architecture",
            "Implement proper error handling and HTTP status codes",
            "Validate all input data with Pydantic models",
            "Use async/await for I/O operations",
            "Implement proper logging and monitoring",
            "Follow RESTful API design principles",
            "Use database sessions properly with context managers",
            "Implement rate limiting and security middleware"
        ]
    
    async def analyze_fastapi_project(self, project_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze FastAPI project structure and provide architectural recommendations"""
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "project_type": project_structure.get("type", "api"),
            "architecture_score": 100,
            "recommendations": [],
            "security_issues": [],
            "performance_optimizations": [],
            "code_quality": {},
            "dependency_analysis": {}
        }
        
        # Architecture analysis
        if "routers" not in project_structure.get("directories", []):
            analysis["recommendations"].append("📁 Organize endpoints using APIRouter for better modularity")
            analysis["architecture_score"] -= 15
        
        if "models" not in project_structure.get("directories", []):
            analysis["recommendations"].append("📁 Create separate models directory for Pydantic schemas")
            analysis["architecture_score"] -= 10
        
        if "dependencies" not in project_structure.get("files", []):
            analysis["recommendations"].append("🔧 Implement dependency injection patterns")
            analysis["architecture_score"] -= 10
        
        # Security analysis
        if not project_structure.get("authentication", False):
            analysis["security_issues"].append("🔒 No authentication system detected")
            analysis["architecture_score"] -= 20
        
        if not project_structure.get("cors_configured", False):
            analysis["security_issues"].append("🔒 CORS not properly configured")
            analysis["architecture_score"] -= 5
        
        # Performance analysis
        analysis["performance_optimizations"] = self._analyze_performance_opportunities(project_structure)
        
        # Code quality assessment
        analysis["code_quality"] = self._assess_code_quality(project_structure)
        
        return analysis
    
    async def design_api_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design optimal FastAPI architecture based on requirements"""
        
        architecture = {
            "timestamp": datetime.now().isoformat(),
            "project_structure": {},
            "routing_strategy": {},
            "database_design": {},
            "authentication_design": {},
            "deployment_strategy": {},
            "configuration_files": {}
        }
        
        # Project structure
        architecture["project_structure"] = self._design_project_structure(requirements)
        
        # Routing strategy
        architecture["routing_strategy"] = self._design_routing_strategy(requirements)
        
        # Database design
        if requirements.get("database", False):
            architecture["database_design"] = self._design_database_architecture(requirements)
        
        # Authentication design
        if requirements.get("authentication", False):
            architecture["authentication_design"] = self._design_auth_architecture(requirements)
        
        # Deployment strategy
        architecture["deployment_strategy"] = self._design_deployment_strategy(requirements)
        
        # Configuration files
        architecture["configuration_files"] = self._generate_config_files(requirements)
        
        return architecture
    
    async def optimize_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze FastAPI performance and provide optimization strategies"""
        
        optimization = {
            "timestamp": datetime.now().isoformat(),
            "current_metrics": performance_data,
            "bottlenecks": [],
            "optimizations": [],
            "database_optimizations": [],
            "caching_strategy": {},
            "async_improvements": []
        }
        
        # Analyze response times
        avg_response_time = performance_data.get("avg_response_time", 0)
        if avg_response_time > 500:  # ms
            optimization["bottlenecks"].append("🐌 High average response time")
            optimization["optimizations"].extend([
                "Implement database connection pooling",
                "Add response caching for expensive operations",
                "Use async database operations",
                "Optimize database queries and add indexes"
            ])
        
        # Memory usage analysis
        memory_usage = performance_data.get("memory_usage", 0)
        if memory_usage > 512:  # MB
            optimization["bottlenecks"].append("💾 High memory usage")
            optimization["optimizations"].extend([
                "Implement pagination for large datasets",
                "Use streaming responses for large files",
                "Optimize Pydantic model serialization",
                "Add memory profiling and monitoring"
            ])
        
        # Database optimization
        optimization["database_optimizations"] = self._generate_db_optimizations(performance_data)
        
        # Caching strategy
        optimization["caching_strategy"] = self._design_caching_strategy(performance_data)
        
        # Async improvements
        optimization["async_improvements"] = self._suggest_async_improvements(performance_data)
        
        return optimization
    
    async def review_api_security(self, api_config: Dict[str, Any]) -> Dict[str, Any]:
        """Review FastAPI security implementation and provide recommendations"""
        
        security_review = {
            "timestamp": datetime.now().isoformat(),
            "security_score": 100,
            "vulnerabilities": [],
            "recommendations": [],
            "authentication_review": {},
            "input_validation_review": {},
            "deployment_security": {}
        }
        
        # Authentication review
        auth_method = api_config.get("authentication", "none")
        if auth_method == "none":
            security_review["vulnerabilities"].append("🚨 No authentication mechanism")
            security_review["security_score"] -= 40
        elif auth_method == "basic":
            security_review["vulnerabilities"].append("⚠️ Basic auth is not secure for production")
            security_review["security_score"] -= 20
        
        # Input validation
        if not api_config.get("pydantic_validation", False):
            security_review["vulnerabilities"].append("🚨 Missing input validation")
            security_review["security_score"] -= 25
        
        # CORS configuration
        cors_config = api_config.get("cors", {})
        if cors_config.get("allow_origins") == ["*"]:
            security_review["vulnerabilities"].append("⚠️ CORS allows all origins")
            security_review["security_score"] -= 15
        
        # HTTPS enforcement
        if not api_config.get("https_only", False):
            security_review["vulnerabilities"].append("🚨 HTTPS not enforced")
            security_review["security_score"] -= 20
        
        # Rate limiting
        if not api_config.get("rate_limiting", False):
            security_review["recommendations"].append("⚡ Implement rate limiting")
        
        # Security headers
        if not api_config.get("security_headers", False):
            security_review["recommendations"].append("🛡️ Add security headers middleware")
        
        security_review["authentication_review"] = self._review_authentication(api_config)
        security_review["input_validation_review"] = self._review_input_validation(api_config)
        security_review["deployment_security"] = self._review_deployment_security(api_config)
        
        return security_review
    
    async def troubleshoot_fastapi_issue(self, issue_details: Dict[str, Any]) -> Dict[str, Any]:
        """Troubleshoot common FastAPI issues and provide solutions"""
        
        troubleshooting = {
            "timestamp": datetime.now().isoformat(),
            "issue_category": self._categorize_issue(issue_details),
            "likely_causes": [],
            "solutions": [],
            "prevention_tips": [],
            "related_resources": []
        }
        
        error_type = issue_details.get("error", "").lower()
        
        if "async" in error_type or "await" in error_type:
            troubleshooting["likely_causes"] = [
                "Mixing async and sync code incorrectly",
                "Using blocking operations in async functions",
                "Incorrect database session handling"
            ]
            troubleshooting["solutions"] = [
                "Ensure all I/O operations use async/await",
                "Use async database drivers (asyncpg, aiomysql)",
                "Implement proper async context managers",
                "Check dependency injection is async-compatible"
            ]
        
        elif "pydantic" in error_type or "validation" in error_type:
            troubleshooting["likely_causes"] = [
                "Invalid data types in request payload",
                "Missing required fields",
                "Pydantic model configuration issues"
            ]
            troubleshooting["solutions"] = [
                "Check request payload matches Pydantic model",
                "Add proper field validation and constraints",
                "Use Pydantic v2 compatibility mode if needed",
                "Implement custom validators for complex logic"
            ]
        
        elif "database" in error_type or "sqlalchemy" in error_type:
            troubleshooting["likely_causes"] = [
                "Database connection issues",
                "Incorrect session management",
                "Migration problems"
            ]
            troubleshooting["solutions"] = [
                "Check database connection string",
                "Ensure proper session cleanup with dependency injection",
                "Run Alembic migrations to sync schema",
                "Check database permissions and access"
            ]
        
        elif "import" in error_type or "module" in error_type:
            troubleshooting["likely_causes"] = [
                "Missing dependencies",
                "Incorrect import paths",
                "Python path issues"
            ]
            troubleshooting["solutions"] = [
                "Install missing packages: pip install -r requirements.txt",
                "Check relative import paths",
                "Verify PYTHONPATH is set correctly",
                "Use absolute imports for better reliability"
            ]
        
        troubleshooting["related_resources"] = [
            "https://fastapi.tiangolo.com/tutorial/",
            "https://fastapi.tiangolo.com/async/",
            "https://pydantic-docs.helpmanual.io/"
        ]
        
        return troubleshooting
    
    def _analyze_performance_opportunities(self, structure: Dict) -> List[str]:
        """Analyze performance optimization opportunities"""
        optimizations = []
        
        if not structure.get("async_endpoints", False):
            optimizations.append("🚀 Convert endpoints to async for better performance")
        
        if not structure.get("connection_pooling", False):
            optimizations.append("🗄️ Implement database connection pooling")
        
        if not structure.get("caching", False):
            optimizations.append("⚡ Add caching layer for expensive operations")
        
        if structure.get("large_responses", False):
            optimizations.append("📦 Implement response pagination and streaming")
        
        return optimizations
    
    def _assess_code_quality(self, structure: Dict) -> Dict[str, Any]:
        """Assess code quality metrics"""
        return {
            "type_hints": structure.get("type_hints", False),
            "docstrings": structure.get("docstrings", False),
            "error_handling": structure.get("error_handling", False),
            "testing": structure.get("tests", False),
            "linting": structure.get("linting", False),
            "score": sum([
                structure.get("type_hints", False),
                structure.get("docstrings", False),
                structure.get("error_handling", False),
                structure.get("tests", False),
                structure.get("linting", False)
            ]) * 20  # Out of 100
        }
    
    def _design_project_structure(self, requirements: Dict) -> Dict[str, Any]:
        """Design optimal project structure"""
        base_structure = {
            "app/": {
                "__init__.py": "Main application package",
                "main.py": "FastAPI application entry point",
                "config.py": "Application configuration",
                "routers/": {
                    "__init__.py": "",
                    "auth.py": "Authentication endpoints",
                    "users.py": "User management endpoints",
                    "health.py": "Health check endpoints"
                },
                "models/": {
                    "__init__.py": "",
                    "user.py": "User Pydantic models",
                    "auth.py": "Authentication models"
                },
                "database/": {
                    "__init__.py": "",
                    "connection.py": "Database connection",
                    "models.py": "SQLAlchemy models",
                    "crud.py": "Database operations"
                },
                "dependencies/": {
                    "__init__.py": "",
                    "auth.py": "Authentication dependencies",
                    "database.py": "Database dependencies"
                },
                "middleware/": {
                    "__init__.py": "",
                    "cors.py": "CORS middleware",
                    "auth.py": "Authentication middleware",
                    "logging.py": "Logging middleware"
                }
            },
            "tests/": {
                "__init__.py": "",
                "test_auth.py": "Authentication tests",
                "test_users.py": "User endpoint tests",
                "conftest.py": "Test configuration"
            },
            "alembic/": "Database migrations",
            "requirements.txt": "Python dependencies",
            "Dockerfile": "Container configuration",
            ".env.example": "Environment variables template"
        }
        
        if requirements.get("features"):
            for feature in requirements["features"]:
                if feature == "file_upload":
                    base_structure["app/"]["routers/"]["files.py"] = "File upload endpoints"
                elif feature == "websockets":
                    base_structure["app/"]["websockets/"] = "WebSocket handlers"
                elif feature == "background_tasks":
                    base_structure["app/"]["tasks/"] = "Background task definitions"
        
        return base_structure
    
    def _design_routing_strategy(self, requirements: Dict) -> Dict[str, Any]:
        """Design API routing strategy"""
        return {
            "api_versioning": {
                "strategy": "URL path versioning",
                "example": "/api/v1/users",
                "deprecation_policy": "Support previous version for 6 months"
            },
            "router_organization": {
                "by_resource": "Group endpoints by resource (users, auth, etc.)",
                "by_feature": "Group endpoints by business feature",
                "prefix_strategy": "Use consistent prefixes (/api/v1/)"
            },
            "response_models": {
                "success_responses": "Use specific Pydantic models",
                "error_responses": "Standardized error response format",
                "pagination": "Consistent pagination for list endpoints"
            }
        }
    
    def _design_database_architecture(self, requirements: Dict) -> Dict[str, Any]:
        """Design database architecture"""
        return {
            "orm": "SQLAlchemy with async support",
            "migration_tool": "Alembic for schema management",
            "connection_strategy": {
                "pool_size": 10,
                "max_overflow": 20,
                "pool_pre_ping": True,
                "pool_recycle": 3600
            },
            "session_management": "Dependency injection with automatic cleanup",
            "query_optimization": [
                "Use select() for better performance",
                "Implement eager loading for relationships",
                "Add database indexes for frequently queried fields",
                "Use database-specific optimizations"
            ]
        }
    
    def _design_auth_architecture(self, requirements: Dict) -> Dict[str, Any]:
        """Design authentication architecture"""
        auth_type = requirements.get("auth_type", "jwt")
        
        if auth_type == "jwt":
            return {
                "token_type": "JWT with refresh tokens",
                "algorithm": "RS256 for production",
                "token_storage": "HttpOnly cookies (recommended)",
                "refresh_strategy": "Automatic token rotation",
                "middleware": "Custom authentication middleware",
                "dependencies": "Authentication dependency injection"
            }
        elif auth_type == "oauth2":
            return {
                "flow": "Authorization Code with PKCE",
                "providers": ["Google", "GitHub", "Microsoft"],
                "session_management": "Server-side sessions",
                "token_validation": "Provider token introspection"
            }
        else:
            return {
                "recommendation": "Implement JWT-based authentication",
                "security_features": ["Token rotation", "Rate limiting", "HTTPS only"]
            }
    
    def _design_deployment_strategy(self, requirements: Dict) -> Dict[str, Any]:
        """Design deployment strategy"""
        return {
            "containerization": {
                "base_image": "python:3.11-slim",
                "multi_stage_build": True,
                "security_scanning": "Trivy or similar tools"
            },
            "production_server": {
                "asgi_server": "Uvicorn with Gunicorn workers",
                "worker_count": "CPU cores * 2 + 1",
                "worker_class": "uvicorn.workers.UvicornWorker"
            },
            "monitoring": {
                "health_checks": "/health endpoint",
                "metrics": "Prometheus integration",
                "logging": "Structured JSON logging",
                "error_tracking": "Sentry integration"
            },
            "scaling": {
                "horizontal": "Multiple container instances",
                "load_balancing": "nginx or cloud load balancer",
                "database": "Connection pooling and read replicas"
            }
        }
    
    def _generate_config_files(self, requirements: Dict) -> Dict[str, str]:
        """Generate configuration files"""
        return {
            "main.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.app.routers import auth, users, health
from agents.app.config import settings

app = FastAPI(
    title="API",
    description="FastAPI application",
    version="1.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
''',
            "config.py": '''from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"

settings = Settings()
''',
            "Dockerfile": '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        }
    
    def _generate_db_optimizations(self, performance_data: Dict) -> List[str]:
        """Generate database optimization suggestions"""
        optimizations = []
        
        query_time = performance_data.get("avg_query_time", 0)
        if query_time > 100:  # ms
            optimizations.extend([
                "Add database indexes for frequently queried fields",
                "Optimize N+1 query problems with eager loading",
                "Use database query analysis tools",
                "Consider query caching for expensive operations"
            ])
        
        connection_issues = performance_data.get("connection_errors", 0)
        if connection_issues > 0:
            optimizations.extend([
                "Increase database connection pool size",
                "Implement connection retry logic",
                "Add connection health checks",
                "Monitor connection pool usage"
            ])
        
        return optimizations
    
    def _design_caching_strategy(self, performance_data: Dict) -> Dict[str, Any]:
        """Design caching strategy"""
        return {
            "application_cache": "Redis for session storage and caching",
            "response_cache": "FastAPI-Cache for endpoint caching",
            "database_cache": "SQLAlchemy query result caching",
            "cdn_cache": "CloudFlare or similar for static assets",
            "cache_invalidation": "Event-based cache invalidation strategy"
        }
    
    def _suggest_async_improvements(self, performance_data: Dict) -> List[str]:
        """Suggest async programming improvements"""
        return [
            "Use async database drivers (asyncpg, aiomysql)",
            "Implement async context managers for resource cleanup",
            "Use asyncio.gather() for concurrent operations",
            "Avoid blocking operations in async functions",
            "Implement proper async error handling",
            "Use async middleware for better performance"
        ]
    
    def _review_authentication(self, config: Dict) -> Dict[str, Any]:
        """Review authentication implementation"""
        return {
            "token_security": "Use strong secret keys and proper algorithms",
            "session_management": "Implement secure session handling",
            "password_security": "Use proper password hashing (bcrypt, argon2)",
            "rate_limiting": "Implement login attempt rate limiting"
        }
    
    def _review_input_validation(self, config: Dict) -> Dict[str, Any]:
        """Review input validation implementation"""
        return {
            "pydantic_models": "Use strict Pydantic models for all inputs",
            "custom_validators": "Implement custom validation for business rules",
            "sanitization": "Sanitize inputs to prevent injection attacks",
            "file_uploads": "Validate file types and sizes for uploads"
        }
    
    def _review_deployment_security(self, config: Dict) -> Dict[str, Any]:
        """Review deployment security"""
        return {
            "environment_variables": "Store secrets in environment variables",
            "https_only": "Enforce HTTPS in production",
            "security_headers": "Add security headers (HSTS, CSP, etc.)",
            "container_security": "Use security-scanned base images"
        }
    
    def _categorize_issue(self, issue_details: Dict) -> str:
        """Categorize the type of issue"""
        error = issue_details.get("error", "").lower()
        
        if any(term in error for term in ["async", "await", "coroutine"]):
            return "Async Programming"
        elif any(term in error for term in ["pydantic", "validation", "field"]):
            return "Data Validation"
        elif any(term in error for term in ["database", "sqlalchemy", "connection"]):
            return "Database"
        elif any(term in error for term in ["import", "module", "dependency"]):
            return "Dependencies"
        elif any(term in error for term in ["auth", "token", "permission"]):
            return "Authentication"
        else:
            return "General"

# MCP Tool definitions
async def analyze_fastapi_project(project_structure: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze FastAPI project structure and provide architectural recommendations"""
    specialist = FastAPISpecialist()
    return await specialist.analyze_fastapi_project(project_structure)

async def design_api_architecture(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Design optimal FastAPI architecture based on project requirements"""
    specialist = FastAPISpecialist()
    return await specialist.design_api_architecture(requirements)

async def optimize_performance(performance_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze FastAPI performance metrics and provide optimization strategies"""
    specialist = FastAPISpecialist()
    return await specialist.optimize_performance(performance_data)

async def review_api_security(api_config: Dict[str, Any]) -> Dict[str, Any]:
    """Review FastAPI security implementation and identify vulnerabilities"""
    specialist = FastAPISpecialist()
    return await specialist.review_api_security(api_config)

async def troubleshoot_fastapi_issue(issue_details: Dict[str, Any]) -> Dict[str, Any]:
    """Troubleshoot common FastAPI issues and provide step-by-step solutions"""
    specialist = FastAPISpecialist()
    return await specialist.troubleshoot_fastapi_issue(issue_details)
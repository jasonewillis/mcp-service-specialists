#!/usr/bin/env python3
"""
Docker Orchestration Master - Ultra-deep expertise in Docker and containerization
Specialized for multi-service applications like Fed Job Advisor
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio
from enum import Enum

class DockerBuildStrategy(Enum):
    """Docker build strategies"""
    SINGLE_STAGE = "single_stage"
    MULTI_STAGE = "multi_stage"
    BUILDKIT = "buildkit"
    BUILDX = "buildx"

class DockerMaster:
    """
    Ultra-specialized agent for Docker containerization and orchestration
    Complete knowledge of Docker, Docker Compose, and container best practices
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "docker"
        self.research_output = self.base_path / "research_outputs" / "docker_optimization"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Exhaustive Docker knowledge base
        self.knowledge_base = {
            "dockerfile_patterns": {
                "multi_stage_build": {
                    "pattern": """
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
""",
                    "benefits": [
                        "Smaller final image size",
                        "No build tools in production",
                        "Improved security",
                        "Layer caching optimization"
                    ]
                },
                "layer_optimization": {
                    "rules": [
                        "Order commands from least to most frequently changing",
                        "Combine RUN commands with &&",
                        "Use .dockerignore to exclude files",
                        "Copy package files before source code",
                        "Use specific base image tags, not latest"
                    ],
                    "example": """
# Good - optimized layers
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Bad - invalidates cache
COPY . .
RUN npm ci --only=production
"""
                },
                "security_hardening": {
                    "non_root_user": """
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs
""",
                    "minimal_base": "Use alpine or distroless images",
                    "no_secrets": "Never include secrets in images",
                    "scan_images": "Use docker scan or trivy"
                }
            },
            
            "docker_compose_patterns": {
                "service_configuration": {
                    "template": """
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    image: myapp-backend:latest
    container_name: myapp-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - app-network
    volumes:
      - ./data:/app/data
      - app-logs:/app/logs

  db:
    image: postgres:15-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

volumes:
  postgres-data:
  app-logs:

networks:
  app-network:
    driver: bridge
"""
                },
                "environment_management": {
                    "env_files": [".env", ".env.local", ".env.production"],
                    "override_files": ["docker-compose.override.yml"],
                    "secrets_management": "Use Docker secrets or external vault"
                }
            },
            
            "performance_optimization": {
                "build_optimization": {
                    "buildkit": {
                        "enable": "DOCKER_BUILDKIT=1 docker build",
                        "cache_mounts": """
# Cache package manager downloads
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production
""",
                        "parallel_builds": "docker buildx build --platform linux/amd64,linux/arm64"
                    },
                    "layer_caching": {
                        "strategies": [
                            "Use Docker layer cache",
                            "Registry caching with --cache-from",
                            "BuildKit inline cache"
                        ],
                        "example": """
docker build \
  --cache-from type=registry,ref=myregistry/myapp:cache \
  --cache-to type=registry,ref=myregistry/myapp:cache,mode=max \
  -t myapp:latest .
"""
                    }
                },
                "runtime_optimization": {
                    "resource_limits": """
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
""",
                    "healthchecks": "Essential for orchestration",
                    "restart_policies": ["no", "always", "on-failure", "unless-stopped"]
                }
            },
            
            "networking": {
                "network_types": {
                    "bridge": "Default, isolated network",
                    "host": "Use host networking (Linux only)",
                    "overlay": "Multi-host networking (Swarm)",
                    "macvlan": "Assign MAC address",
                    "none": "No networking"
                },
                "service_discovery": {
                    "internal_dns": "Services accessible by name",
                    "aliases": "network aliases for multiple names",
                    "external_access": "Use reverse proxy (nginx, traefik)"
                },
                "security": {
                    "network_isolation": "Use custom networks, not default",
                    "encrypted_overlay": "For sensitive data in Swarm",
                    "firewall_rules": "iptables rules for additional security"
                }
            },
            
            "volume_management": {
                "volume_types": {
                    "named_volumes": "Docker managed, persistent",
                    "bind_mounts": "Host directory mapping",
                    "tmpfs": "Memory-only, ephemeral",
                    "nfs_volumes": "Network attached storage"
                },
                "backup_strategies": {
                    "volume_backup": """
docker run --rm \
  -v myvolume:/source \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /source .
""",
                    "database_specific": "Use database tools for consistency"
                },
                "performance": {
                    "volume_drivers": ["local", "nfs", "azure", "aws"],
                    "mount_options": "noatime, nodiratime for performance"
                }
            },
            
            "debugging_troubleshooting": {
                "common_issues": {
                    "container_exits": {
                        "diagnosis": "docker logs <container>",
                        "interactive": "docker run -it --entrypoint /bin/sh image",
                        "debug_mode": "Add command: sleep infinity"
                    },
                    "networking_issues": {
                        "inspect": "docker network inspect <network>",
                        "connectivity": "docker exec container ping other-container",
                        "port_mapping": "docker port <container>"
                    },
                    "permission_errors": {
                        "user_mapping": "Check UID/GID mapping",
                        "volume_permissions": "chown in entrypoint script",
                        "selinux": "Add :Z or :z to volume mounts"
                    }
                },
                "debugging_tools": {
                    "logs": "docker logs -f --tail 100 container",
                    "exec": "docker exec -it container /bin/bash",
                    "inspect": "docker inspect container",
                    "stats": "docker stats",
                    "top": "docker top container",
                    "events": "docker events --since 1h"
                }
            },
            
            "fed_job_advisor_setup": {
                "services": {
                    "frontend": {
                        "base_image": "node:18-alpine",
                        "build_stage": "Next.js build",
                        "runtime": "Node server or nginx",
                        "port": 3000
                    },
                    "backend": {
                        "base_image": "python:3.11-slim",
                        "framework": "FastAPI",
                        "server": "uvicorn",
                        "port": 8000
                    },
                    "database": {
                        "image": "postgres:15-alpine",
                        "volumes": "persistent data",
                        "backup": "pg_dump scheduled"
                    },
                    "redis": {
                        "image": "redis:7-alpine",
                        "purpose": "caching and sessions",
                        "persistence": "optional AOF"
                    }
                },
                "development_setup": {
                    "hot_reload": "Volume mount source code",
                    "debugging": "Expose debug ports",
                    "database_gui": "Include pgAdmin service"
                },
                "production_setup": {
                    "ssl_termination": "Nginx or Traefik",
                    "secrets": "Docker secrets or env vault",
                    "monitoring": "Prometheus + Grafana",
                    "logging": "ELK stack or Loki"
                }
            }
        }
    
    async def generate_dockerfile(self, app_type: str, config: Dict[str, Any]) -> str:
        """
        Generate optimized Dockerfile for specific application type
        """
        timestamp = datetime.now().isoformat()
        
        if app_type == "nodejs":
            dockerfile = self._generate_nodejs_dockerfile(config)
        elif app_type == "python":
            dockerfile = self._generate_python_dockerfile(config)
        elif app_type == "static":
            dockerfile = self._generate_static_dockerfile(config)
        else:
            dockerfile = "# Unsupported application type"
        
        # Save Dockerfile
        output_file = self.research_output / f"{timestamp}_Dockerfile_{app_type}"
        with open(output_file, 'w') as f:
            f.write(dockerfile)
        
        return dockerfile
    
    def _generate_nodejs_dockerfile(self, config: Dict[str, Any]) -> str:
        """Generate Node.js Dockerfile"""
        return f"""# Multi-stage Dockerfile for Node.js application
# Generated: {datetime.now().isoformat()}

# Stage 1: Dependencies
FROM node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .

# Build application
ENV NODE_ENV production
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

# Security: Non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy built application
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD node healthcheck.js || exit 1

EXPOSE 3000
ENV PORT 3000

CMD ["node", "dist/index.js"]
"""
    
    def _generate_python_dockerfile(self, config: Dict[str, Any]) -> str:
        """Generate Python Dockerfile"""
        return f"""# Multi-stage Dockerfile for Python application
# Generated: {datetime.now().isoformat()}

# Stage 1: Builder
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Security: Non-root user
RUN useradd -m -u 1001 python && \
    mkdir -p /app && \
    chown -R python:python /app

WORKDIR /app

# Copy Python wheels and install
COPY --from=builder /app/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application
COPY --chown=python:python . .

USER python

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000

# FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    def _generate_static_dockerfile(self, config: Dict[str, Any]) -> str:
        """Generate static site Dockerfile"""
        return f"""# Multi-stage Dockerfile for static site
# Generated: {datetime.now().isoformat()}

# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built static files
COPY --from=builder /app/dist /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
"""
    
    async def generate_docker_compose(self, project_type: str = "fed_job_advisor") -> str:
        """
        Generate complete Docker Compose configuration
        """
        compose = """# Docker Compose for Fed Job Advisor
# Generated: {timestamp}
version: '3.8'

services:
  # Frontend - Next.js
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        - NODE_ENV=production
    image: fedjobadvisor-frontend:latest
    container_name: fja-frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - fja-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Backend - FastAPI
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    image: fedjobadvisor-backend:latest
    container_name: fja-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://fja_user:${DB_PASSWORD}@db:5432/federal_career_dev
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - fja-network
    volumes:
      - ./backend/logs:/app/logs
      - ./backend/data:/app/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Database - PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: fja-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=federal_career_dev
      - POSTGRES_USER=fja_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./backend/migrations/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fja_user -d federal_career_dev"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - fja-network
    ports:
      - "5432:5432"  # Remove in production

  # Cache - Redis
  redis:
    image: redis:7-alpine
    container_name: fja-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - fja-network
    ports:
      - "6379:6379"  # Remove in production

  # Reverse Proxy - Nginx (Production)
  nginx:
    image: nginx:alpine
    container_name: fja-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx-cache:/var/cache/nginx
    depends_on:
      - frontend
      - backend
    networks:
      - fja-network
    profiles:
      - production

  # Database Admin - pgAdmin (Development)
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: fja-pgadmin
    restart: unless-stopped
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@fedjobadvisor.com
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PASSWORD}
    ports:
      - "5050:80"
    networks:
      - fja-network
    profiles:
      - development

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
  nginx-cache:
    driver: local

networks:
  fja-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
""".format(timestamp=datetime.now().isoformat())
        
        return compose
    
    async def diagnose_container_issue(self, error_log: str, service: str) -> Dict[str, Any]:
        """
        Diagnose Docker container issues
        """
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "issues_detected": [],
            "solutions": [],
            "commands": []
        }
        
        error_lower = error_log.lower()
        
        # Exit code analysis
        if "exit code 1" in error_lower or "exited with code 1" in error_lower:
            diagnosis["issues_detected"].append("Container exited with error")
            diagnosis["solutions"].append("Check application logs for startup errors")
            diagnosis["commands"].append(f"docker logs {service}")
        
        # Permission issues
        if "permission denied" in error_lower:
            diagnosis["issues_detected"].append("Permission denied error")
            diagnosis["solutions"].extend([
                "Check file ownership in container",
                "Verify USER directive in Dockerfile",
                "Add :Z flag to volumes for SELinux"
            ])
            diagnosis["commands"].extend([
                f"docker exec {service} ls -la",
                f"docker exec {service} whoami"
            ])
        
        # Network issues
        if "connection refused" in error_lower or "no route to host" in error_lower:
            diagnosis["issues_detected"].append("Network connectivity issue")
            diagnosis["solutions"].extend([
                "Verify service is on same network",
                "Check if service is actually running",
                "Use service name, not localhost"
            ])
            diagnosis["commands"].extend([
                "docker network ls",
                f"docker inspect {service} | grep NetworkMode",
                f"docker exec {service} ping other-service"
            ])
        
        # Port binding issues
        if "bind: address already in use" in error_lower:
            diagnosis["issues_detected"].append("Port already in use")
            diagnosis["solutions"].extend([
                "Check what's using the port",
                "Change port mapping in docker-compose.yml",
                "Stop conflicting service"
            ])
            diagnosis["commands"].extend([
                "lsof -i :PORT",
                "docker ps --format 'table {{.Names}}\\t{{.Ports}}'"
            ])
        
        # Memory issues
        if "out of memory" in error_lower or "cannot allocate memory" in error_lower:
            diagnosis["issues_detected"].append("Out of memory")
            diagnosis["solutions"].extend([
                "Increase memory limits",
                "Optimize application memory usage",
                "Check Docker daemon memory allocation"
            ])
            diagnosis["commands"].extend([
                "docker stats --no-stream",
                "docker system df"
            ])
        
        return diagnosis
    
    async def optimize_docker_setup(self, current_setup: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and optimize Docker configuration
        """
        optimizations = {
            "dockerfile_improvements": [],
            "compose_improvements": [],
            "security_enhancements": [],
            "performance_gains": [],
            "cost_savings": []
        }
        
        # Analyze Dockerfile
        if "dockerfile" in current_setup:
            dockerfile = current_setup["dockerfile"]
            
            # Check for multi-stage
            if "FROM" in dockerfile and dockerfile.count("FROM") == 1:
                optimizations["dockerfile_improvements"].append(
                    "Use multi-stage build to reduce image size"
                )
            
            # Check for layer optimization
            if "RUN apt-get update && apt-get install" not in dockerfile:
                optimizations["dockerfile_improvements"].append(
                    "Combine RUN commands to reduce layers"
                )
            
            # Check for non-root user
            if "USER" not in dockerfile:
                optimizations["security_enhancements"].append(
                    "Add non-root user for security"
                )
        
        # Analyze Docker Compose
        if "compose" in current_setup:
            # Check for health checks
            optimizations["compose_improvements"].append(
                "Add health checks to all services"
            )
            
            # Check for resource limits
            optimizations["performance_gains"].append(
                "Set resource limits to prevent runaway containers"
            )
        
        return optimizations

# CLI interface
if __name__ == "__main__":
    import sys
    
    master = DockerMaster()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "dockerfile":
            app_type = sys.argv[2] if len(sys.argv) > 2 else "nodejs"
            result = asyncio.run(master.generate_dockerfile(app_type, {}))
            print(result)
        
        elif command == "compose":
            result = asyncio.run(master.generate_docker_compose())
            print(result)
        
        elif command == "diagnose":
            if len(sys.argv) > 3:
                error = sys.argv[2]
                service = sys.argv[3]
                result = asyncio.run(master.diagnose_container_issue(error, service))
                print(json.dumps(result, indent=2))
    else:
        print("Docker Orchestration Master")
        print("Commands:")
        print("  dockerfile <type> - Generate Dockerfile")
        print("  compose - Generate docker-compose.yml")
        print("  diagnose <error> <service> - Diagnose container issue")
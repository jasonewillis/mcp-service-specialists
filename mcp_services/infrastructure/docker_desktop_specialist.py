#!/usr/bin/env python3
"""
Docker Desktop Specialist - Ultra-deep expertise in Docker Desktop application
Specialized for Docker Desktop management, troubleshooting, and optimization
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio
from enum import Enum
import subprocess
import platform

class DockerDesktopPlatform(Enum):
    """Docker Desktop platforms"""
    MACOS = "macos"
    WINDOWS = "windows" 
    LINUX = "linux"

class DockerDesktopIssue(Enum):
    """Common Docker Desktop issues"""
    NOT_RUNNING = "not_running"
    STARTUP_FAILURE = "startup_failure"
    RESOURCE_LIMITS = "resource_limits"
    NETWORKING = "networking"
    VOLUME_MOUNTS = "volume_mounts"
    PERMISSION_DENIED = "permission_denied"
    WSL_INTEGRATION = "wsl_integration"
    KUBERNETES = "kubernetes"

class DockerDesktopSpecialist:
    """
    Ultra-specialized agent for Docker Desktop application management
    Complete knowledge of Docker Desktop across macOS, Windows, and Linux
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "docker"
        self.research_output = self.base_path / "research_outputs" / "docker_desktop"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        self.platform = self._detect_platform()
        
        # Exhaustive Docker Desktop knowledge base
        self.knowledge_base = {
            "installation": {
                "macos": {
                    "requirements": {
                        "os_version": "macOS 10.15 or newer",
                        "chip": "Intel or Apple Silicon",
                        "memory": "4GB RAM minimum, 8GB recommended",
                        "disk": "2.5GB disk space"
                    },
                    "download_url": "https://desktop.docker.com/mac/main/amd64/Docker.dmg",
                    "apple_silicon_url": "https://desktop.docker.com/mac/main/arm64/Docker.dmg",
                    "installation_steps": [
                        "Download Docker.dmg",
                        "Double-click to open installer",
                        "Drag Docker to Applications folder",
                        "Launch Docker from Applications",
                        "Follow setup wizard"
                    ],
                    "post_install": [
                        "Enable 'Use Docker Compose V2'",
                        "Configure resource limits",
                        "Enable experimental features if needed",
                        "Set up file sharing directories"
                    ]
                },
                "windows": {
                    "requirements": {
                        "os_version": "Windows 10 64-bit Pro/Enterprise/Education or Windows 11",
                        "wsl2": "WSL 2 feature enabled",
                        "virtualization": "Hardware virtualization enabled in BIOS",
                        "memory": "4GB RAM minimum, 8GB recommended"
                    },
                    "download_url": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
                    "wsl2_setup": [
                        "Enable WSL 2 feature",
                        "Install WSL 2 Linux kernel update",
                        "Set WSL 2 as default version",
                        "Install Ubuntu or preferred distribution"
                    ],
                    "installation_steps": [
                        "Download Docker Desktop Installer.exe",
                        "Run installer as administrator", 
                        "Follow installation wizard",
                        "Restart computer if prompted",
                        "Launch Docker Desktop"
                    ]
                },
                "linux": {
                    "requirements": {
                        "os": "64-bit Ubuntu, Debian, Fedora, or Arch",
                        "kernel": "Linux kernel 4.0 or newer",
                        "memory": "4GB RAM minimum",
                        "kvm": "KVM virtualization support"
                    },
                    "installation_methods": [
                        "DEB package for Ubuntu/Debian",
                        "RPM package for Fedora/RHEL", 
                        "Generic binary package",
                        "Snap package (experimental)"
                    ]
                }
            },
            
            "startup_troubleshooting": {
                "macos": {
                    "common_issues": {
                        "docker_not_starting": {
                            "symptoms": ["Docker Desktop icon shows error", "Cannot start containers"],
                            "solutions": [
                                "Reset Docker Desktop from Troubleshoot menu",
                                "Check macOS security settings",
                                "Verify disk space availability",
                                "Restart Docker Desktop service",
                                "Delete and reinstall if corrupted"
                            ],
                            "commands": [
                                "killall Docker && open /Applications/Docker.app",
                                "rm -rf ~/Library/Containers/com.docker.docker",
                                "sudo launchctl unload /Library/LaunchDaemons/com.docker.vmnetd.plist",
                                "sudo launchctl load /Library/LaunchDaemons/com.docker.vmnetd.plist"
                            ]
                        },
                        "permission_denied": {
                            "symptoms": ["Cannot connect to Docker daemon", "Permission denied on socket"],
                            "solutions": [
                                "Add user to docker group (if applicable)",
                                "Check Docker Desktop is running",
                                "Verify Docker socket permissions",
                                "Reset Docker Desktop"
                            ],
                            "commands": [
                                "docker context ls",
                                "docker context use desktop-linux",
                                "ls -la /var/run/docker.sock"
                            ]
                        }
                    }
                },
                "windows": {
                    "common_issues": {
                        "wsl2_integration": {
                            "symptoms": ["WSL 2 integration failed", "Cannot access containers from WSL"],
                            "solutions": [
                                "Enable WSL 2 integration in Docker settings",
                                "Update WSL 2 kernel", 
                                "Restart WSL 2 service",
                                "Reinstall WSL 2 distributions"
                            ],
                            "commands": [
                                "wsl --update",
                                "wsl --list --verbose",
                                "wsl --set-default-version 2",
                                "wsl --shutdown && wsl"
                            ]
                        },
                        "hyperv_conflict": {
                            "symptoms": ["Hyper-V conflicts", "Virtualization errors"],
                            "solutions": [
                                "Disable conflicting virtualization software",
                                "Enable Windows features correctly",
                                "Switch between Hyper-V and WSL 2 backends",
                                "Check BIOS virtualization settings"
                            ],
                            "commands": [
                                "bcdedit /set hypervisorlaunchtype auto",
                                "dism /online /enable-feature /featurename:Microsoft-Hyper-V -All"
                            ]
                        }
                    }
                }
            },
            
            "resource_management": {
                "memory_optimization": {
                    "default_limits": {
                        "macos": "50% of available RAM",
                        "windows": "50% of available RAM",
                        "linux": "25% of available RAM"
                    },
                    "recommended_settings": {
                        "development": {
                            "memory": "4-6GB",
                            "cpu": "2-4 cores",
                            "disk": "64GB"
                        },
                        "production_testing": {
                            "memory": "8-12GB", 
                            "cpu": "4-6 cores",
                            "disk": "100GB+"
                        }
                    },
                    "optimization_tips": [
                        "Monitor memory usage in Docker Desktop dashboard",
                        "Use multi-stage builds to reduce image sizes",
                        "Implement proper cleanup of unused containers/images",
                        "Set resource limits on individual containers",
                        "Use .dockerignore to reduce build context"
                    ]
                },
                "disk_management": {
                    "cleanup_strategies": [
                        "docker system prune -a --volumes",
                        "Remove unused images regularly",
                        "Use Docker Desktop cleanup features", 
                        "Monitor disk usage in Settings > Resources",
                        "Move Docker data directory if needed"
                    ],
                    "disk_usage_commands": [
                        "docker system df",
                        "docker images --format 'table {{.Repository}}\\t{{.Tag}}\\t{{.Size}}'",
                        "docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Size}}'"
                    ]
                }
            },
            
            "networking_configuration": {
                "port_forwarding": {
                    "host_networking": {
                        "macos": "Uses VM with port mapping",
                        "windows": "Uses Hyper-V or WSL 2",
                        "linux": "Direct host networking available"
                    },
                    "common_ports": {
                        "web_development": [3000, 3001, 8000, 8080, 8081],
                        "databases": [5432, 3306, 6379, 27017],
                        "monitoring": [9090, 3000, 8080]
                    },
                    "troubleshooting": [
                        "Check port conflicts with 'lsof -i :PORT' or 'netstat -an'",
                        "Verify container is binding to 0.0.0.0 not localhost",
                        "Use 'docker port CONTAINER' to see mappings",
                        "Check firewall rules blocking ports"
                    ]
                },
                "dns_resolution": {
                    "internal_dns": "Automatic service discovery between containers",
                    "external_dns": "Uses host DNS configuration",
                    "custom_dns": "Configure in Docker Desktop settings",
                    "common_issues": [
                        "DNS resolution failures in containers",
                        "Cannot reach external services",
                        "Corporate firewall blocking DNS"
                    ]
                }
            },
            
            "volume_management": {
                "file_sharing": {
                    "macos": {
                        "default_shares": ["/Users", "/Volumes", "/tmp", "/private"],
                        "configuration": "Settings > Resources > File Sharing",
                        "performance_tips": [
                            "Limit shared directories to improve performance",
                            "Use named volumes instead of bind mounts when possible",
                            "Consider using cached or delegated mount options"
                        ]
                    },
                    "windows": {
                        "default_shares": ["C:\\"],
                        "wsl2_integration": "Automatic sharing via WSL 2",
                        "performance_considerations": [
                            "WSL 2 backend offers better performance",
                            "Use Linux containers when possible",
                            "Avoid bind mounting Windows paths when unnecessary"
                        ]
                    }
                },
                "volume_types": {
                    "bind_mounts": {
                        "use_case": "Development with hot reload",
                        "syntax": "-v /host/path:/container/path",
                        "performance": "Slower on macOS/Windows"
                    },
                    "named_volumes": {
                        "use_case": "Persistent data storage",
                        "syntax": "-v volume_name:/container/path", 
                        "performance": "Better performance, Docker managed"
                    },
                    "tmpfs_mounts": {
                        "use_case": "Temporary data in memory",
                        "syntax": "--tmpfs /container/path",
                        "performance": "Fastest, but ephemeral"
                    }
                }
            },
            
            "development_workflow": {
                "hot_reload_setup": {
                    "nodejs": {
                        "docker_command": "docker run -v $(pwd):/app -w /app node:18 npm run dev",
                        "compose_example": """
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
""",
                        "optimization": "Use node_modules volume to avoid copying"
                    },
                    "python": {
                        "docker_command": "docker run -v $(pwd):/app -w /app python:3.11 python app.py",
                        "compose_example": """
services:
  app:
    build: .
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
      - FLASK_ENV=development
""",
                        "optimization": "Use __pycache__ volume exclusion"
                    }
                },
                "debugging": {
                    "remote_debugging": {
                        "vscode": "Use Remote-Containers extension",
                        "pycharm": "Configure Docker interpreter",
                        "general": "Expose debug ports and attach debugger"
                    },
                    "logging": {
                        "container_logs": "docker logs -f container_name",
                        "compose_logs": "docker-compose logs -f service_name",
                        "log_drivers": ["json-file", "syslog", "journald"]
                    }
                }
            },
            
            "kubernetes_integration": {
                "enable_kubernetes": {
                    "steps": [
                        "Go to Settings > Kubernetes",
                        "Check 'Enable Kubernetes'",
                        "Wait for cluster to start",
                        "Verify with 'kubectl cluster-info'"
                    ],
                    "requirements": {
                        "memory": "At least 6GB allocated to Docker",
                        "disk": "Additional 2GB for Kubernetes images"
                    }
                },
                "common_commands": [
                    "kubectl get nodes",
                    "kubectl get pods --all-namespaces",
                    "kubectl create deployment nginx --image=nginx",
                    "kubectl expose deployment nginx --port=80 --type=LoadBalancer"
                ],
                "troubleshooting": [
                    "Reset Kubernetes cluster if stuck",
                    "Check resource allocation",
                    "Verify Docker images are available",
                    "Use kubectl describe for detailed error info"
                ]
            },
            
            "performance_optimization": {
                "build_performance": {
                    "strategies": [
                        "Use BuildKit for faster builds",
                        "Implement proper layer caching",
                        "Use multi-stage builds",
                        "Optimize Dockerfile order",
                        "Use .dockerignore effectively"
                    ],
                    "buildkit_enable": {
                        "environment": "DOCKER_BUILDKIT=1",
                        "docker_cli": "docker buildx use default",
                        "compose": "COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1"
                    }
                },
                "runtime_performance": {
                    "container_optimization": [
                        "Set appropriate resource limits",
                        "Use init process for PID 1",
                        "Implement health checks",
                        "Use read-only root filesystem when possible"
                    ],
                    "host_optimization": [
                        "Allocate sufficient resources to Docker",
                        "Use SSD storage for Docker data",
                        "Close unnecessary applications",
                        "Monitor system resource usage"
                    ]
                }
            },
            
            "fed_job_advisor_integration": {
                "development_setup": {
                    "recommended_resources": {
                        "memory": "8GB",
                        "cpu": "4 cores", 
                        "disk": "100GB"
                    },
                    "required_ports": [3000, 8000, 5432, 6379],
                    "file_sharing": [
                        "Enable sharing for project directory",
                        "Add performance optimization for large codebases"
                    ]
                },
                "compose_optimization": {
                    "services": ["frontend", "backend", "database", "redis"],
                    "networks": "Custom bridge network for isolation",
                    "volumes": "Named volumes for persistent data",
                    "health_checks": "All services should have health checks"
                },
                "common_issues": [
                    "Port conflicts with system services",
                    "Database connection timeouts",
                    "Hot reload not working with volume mounts",
                    "Memory limits causing container crashes"
                ]
            }
        }
    
    def _detect_platform(self) -> DockerDesktopPlatform:
        """Detect the current platform"""
        system = platform.system().lower()
        if system == "darwin":
            return DockerDesktopPlatform.MACOS
        elif system == "windows":
            return DockerDesktopPlatform.WINDOWS
        else:
            return DockerDesktopPlatform.LINUX
    
    async def diagnose_docker_desktop_issue(self, symptoms: List[str], error_log: str = "") -> Dict[str, Any]:
        """
        Comprehensive Docker Desktop issue diagnosis
        """
        timestamp = datetime.now().isoformat()
        
        diagnosis = {
            "timestamp": timestamp,
            "platform": self.platform.value,
            "symptoms": symptoms,
            "identified_issues": [],
            "solutions": [],
            "commands_to_run": [],
            "prevention_tips": []
        }
        
        # Check if Docker Desktop is running
        is_running = await self._check_docker_desktop_status()
        diagnosis["docker_desktop_running"] = is_running
        
        if not is_running:
            diagnosis["identified_issues"].append("Docker Desktop is not running")
            diagnosis["solutions"].extend([
                "Start Docker Desktop application",
                "Check if Docker Desktop is installed",
                "Verify system requirements are met",
                "Check for startup error messages"
            ])
            diagnosis["commands_to_run"].extend([
                f"open /Applications/Docker.app" if self.platform == DockerDesktopPlatform.MACOS else "Start Docker Desktop",
                "docker --version",
                "docker info"
            ])
        
        # Analyze symptoms
        for symptom in symptoms:
            issue_analysis = self._analyze_symptom(symptom, error_log)
            if issue_analysis:
                diagnosis["identified_issues"].extend(issue_analysis["issues"])
                diagnosis["solutions"].extend(issue_analysis["solutions"])
                diagnosis["commands_to_run"].extend(issue_analysis["commands"])
        
        # Platform-specific diagnostics
        platform_analysis = await self._platform_specific_diagnosis()
        diagnosis.update(platform_analysis)
        
        # Save diagnosis
        output_file = self.research_output / f"{timestamp}_diagnosis.json"
        with open(output_file, 'w') as f:
            json.dump(diagnosis, f, indent=2)
        
        return diagnosis
    
    async def _check_docker_desktop_status(self) -> bool:
        """Check if Docker Desktop is running"""
        try:
            result = subprocess.run(
                ["docker", "info"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _analyze_symptom(self, symptom: str, error_log: str) -> Optional[Dict[str, Any]]:
        """Analyze individual symptoms"""
        symptom_lower = symptom.lower()
        
        # Common symptom patterns
        if "permission denied" in symptom_lower:
            return {
                "issues": ["Docker daemon permission error"],
                "solutions": [
                    "Ensure Docker Desktop is running",
                    "Check user permissions for Docker",
                    "Restart Docker Desktop",
                    "Reset Docker Desktop to factory defaults"
                ],
                "commands": [
                    "docker context ls",
                    "docker info",
                    "groups $USER"
                ]
            }
        
        elif "connection refused" in symptom_lower or "cannot connect" in symptom_lower:
            return {
                "issues": ["Cannot connect to Docker daemon"],
                "solutions": [
                    "Start Docker Desktop if not running", 
                    "Check Docker daemon is listening",
                    "Verify Docker socket permissions",
                    "Reset Docker Desktop settings"
                ],
                "commands": [
                    "docker version",
                    "docker context use default",
                    "ps aux | grep docker"
                ]
            }
        
        elif "port" in symptom_lower and ("in use" in symptom_lower or "bind" in symptom_lower):
            return {
                "issues": ["Port binding conflict"],
                "solutions": [
                    "Find process using the port and stop it",
                    "Change port mapping in docker-compose.yml",
                    "Use different port for development",
                    "Check for existing containers using the port"
                ],
                "commands": [
                    "lsof -i :PORT" if self.platform != DockerDesktopPlatform.WINDOWS else "netstat -an | findstr :PORT",
                    "docker ps --format 'table {{.Names}}\\t{{.Ports}}'",
                    "docker port CONTAINER_NAME"
                ]
            }
        
        elif "memory" in symptom_lower or "oom" in symptom_lower:
            return {
                "issues": ["Memory allocation problem"],
                "solutions": [
                    "Increase memory allocation in Docker Desktop settings",
                    "Close unnecessary applications to free memory",
                    "Add memory limits to containers",
                    "Optimize application memory usage"
                ],
                "commands": [
                    "docker stats --no-stream",
                    "docker system df",
                    "free -h" if self.platform == DockerDesktopPlatform.LINUX else "memory_pressure"
                ]
            }
        
        elif "volume" in symptom_lower or "mount" in symptom_lower:
            return {
                "issues": ["Volume mounting issue"],
                "solutions": [
                    "Check file sharing settings in Docker Desktop",
                    "Verify host path exists and is accessible",
                    "Use absolute paths for volume mounts",
                    "Check container user permissions"
                ],
                "commands": [
                    "ls -la /host/path",
                    "docker inspect CONTAINER | grep Mounts",
                    "docker exec CONTAINER ls -la /mounted/path"
                ]
            }
        
        return None
    
    async def _platform_specific_diagnosis(self) -> Dict[str, Any]:
        """Platform-specific diagnostic information"""
        platform_info = {
            "platform_specific_checks": [],
            "platform_recommendations": []
        }
        
        if self.platform == DockerDesktopPlatform.MACOS:
            platform_info["platform_specific_checks"] = [
                "Check macOS version compatibility",
                "Verify Rosetta 2 is installed (Apple Silicon)",
                "Check available disk space",
                "Verify privacy settings allow Docker"
            ]
            platform_info["platform_recommendations"] = [
                "Use latest macOS version for best compatibility",
                "Allocate 4-8GB RAM to Docker Desktop",
                "Enable 'Use Rosetta for x86/amd64 emulation' if needed",
                "Keep Docker Desktop updated"
            ]
        
        elif self.platform == DockerDesktopPlatform.WINDOWS:
            platform_info["platform_specific_checks"] = [
                "Verify WSL 2 is installed and updated",
                "Check Windows version (Windows 10/11 Pro or Enterprise)",
                "Ensure Hyper-V is enabled",
                "Verify virtualization is enabled in BIOS"
            ]
            platform_info["platform_recommendations"] = [
                "Use WSL 2 backend for better performance",
                "Keep WSL 2 kernel updated",
                "Use Linux containers when possible",
                "Ensure Windows is fully updated"
            ]
        
        elif self.platform == DockerDesktopPlatform.LINUX:
            platform_info["platform_specific_checks"] = [
                "Check kernel version (4.0+)",
                "Verify KVM virtualization support",
                "Check available storage space",
                "Verify user groups (docker)"
            ]
            platform_info["platform_recommendations"] = [
                "Add user to docker group",
                "Use systemd for service management",
                "Keep kernel updated",
                "Monitor system resources"
            ]
        
        return platform_info
    
    async def optimize_docker_desktop(self, current_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize Docker Desktop configuration for development workflow
        """
        optimization = {
            "timestamp": datetime.now().isoformat(),
            "platform": self.platform.value,
            "current_config": current_config,
            "optimizations": [],
            "resource_recommendations": {},
            "performance_improvements": []
        }
        
        # Resource optimization
        if current_config.get("memory_gb", 0) < 4:
            optimization["optimizations"].append("Increase memory allocation to at least 4GB")
        elif current_config.get("memory_gb", 0) > 12:
            optimization["optimizations"].append("Consider reducing memory if not fully utilized")
        
        if current_config.get("cpu_cores", 0) < 2:
            optimization["optimizations"].append("Allocate at least 2 CPU cores")
        
        # Disk space optimization
        if current_config.get("disk_gb", 0) < 64:
            optimization["optimizations"].append("Increase disk space allocation to at least 64GB")
        
        # Feature optimizations
        if not current_config.get("buildkit_enabled", False):
            optimization["performance_improvements"].append("Enable BuildKit for faster builds")
        
        if not current_config.get("compose_v2", False):
            optimization["performance_improvements"].append("Enable Docker Compose V2")
        
        # Platform-specific optimizations
        if self.platform == DockerDesktopPlatform.MACOS:
            optimization["performance_improvements"].extend([
                "Use VirtioFS for better file sharing performance",
                "Enable 'Use Rosetta for x86/amd64 emulation' if using Apple Silicon",
                "Limit file sharing to necessary directories only"
            ])
        
        elif self.platform == DockerDesktopPlatform.WINDOWS:
            optimization["performance_improvements"].extend([
                "Use WSL 2 backend instead of Hyper-V",
                "Enable WSL 2 integration for development",
                "Use Linux containers for better performance"
            ])
        
        # Fed Job Advisor specific recommendations
        optimization["fed_job_advisor_optimizations"] = [
            "Allocate 8GB RAM for full-stack development",
            "Enable ports 3000, 8000, 5432, 6379",
            "Use named volumes for database persistence",
            "Configure file sharing for hot reload",
            "Enable health checks for all services"
        ]
        
        return optimization
    
    async def generate_troubleshooting_guide(self) -> str:
        """
        Generate comprehensive Docker Desktop troubleshooting guide
        """
        timestamp = datetime.now().isoformat()
        
        guide = f"""# Docker Desktop Troubleshooting Guide
Generated: {timestamp}
Platform: {self.platform.value}

## Quick Diagnostics

### 1. Check Docker Desktop Status
```bash
# Check if Docker is running
docker info

# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version
```

### 2. Common Quick Fixes
```bash
# Restart Docker Desktop
{self._get_restart_command()}

# Reset Docker Desktop (last resort)
{self._get_reset_command()}

# Clean up Docker resources
docker system prune -a --volumes
```

## Platform-Specific Issues

### {self.platform.value.title()} Specific

{self._get_platform_specific_section()}

## Common Issues and Solutions

### Issue: "Cannot connect to the Docker daemon"
**Symptoms:**
- `docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock`
- Commands fail with connection errors

**Solutions:**
1. Ensure Docker Desktop is running
2. Check Docker context: `docker context use default`
3. Restart Docker Desktop
4. Reset Docker Desktop if persistent

### Issue: "Port already in use"
**Symptoms:**
- `bind: address already in use`
- Cannot start containers on specific ports

**Solutions:**
1. Find conflicting process: `{self._get_port_check_command()}`
2. Change port mapping in docker-compose.yml
3. Stop conflicting service
4. Use different development port

### Issue: "Permission denied"
**Symptoms:**
- Cannot access Docker socket
- Permission errors in containers

**Solutions:**
1. Check Docker Desktop is running
2. {self._get_permission_fix()}
3. Restart Docker Desktop
4. Check file sharing settings

### Issue: "Out of memory"
**Symptoms:**
- Containers killed unexpectedly
- Build failures with memory errors

**Solutions:**
1. Increase Docker memory allocation
2. Close unnecessary applications
3. Optimize container resource usage
4. Use multi-stage builds

### Issue: "Volume mount failures"
**Symptoms:**
- Files not syncing between host and container
- Mount errors in logs

**Solutions:**
1. Check file sharing settings in Docker Desktop
2. Use absolute paths for mounts
3. Verify host directory exists
4. Check container user permissions

## Fed Job Advisor Specific Setup

### Recommended Configuration
```yaml
# Resource Allocation
Memory: 8GB
CPU: 4 cores
Disk: 100GB

# Required Ports
- 3000 (Frontend)
- 8000 (Backend API)
- 5432 (PostgreSQL)
- 6379 (Redis)

# File Sharing
- Enable sharing for project directory
- Add project root to file sharing
```

### Development Setup
```bash
# Check current resource allocation
docker system df
docker stats --no-stream

# Verify all services can start
docker-compose up --dry-run

# Test port accessibility
{self._get_port_test_commands()}
```

## Performance Optimization

### Build Performance
1. Enable BuildKit: `export DOCKER_BUILDKIT=1`
2. Use multi-stage Dockerfiles
3. Optimize layer caching
4. Use .dockerignore effectively

### Runtime Performance
1. Set appropriate resource limits
2. Use named volumes instead of bind mounts where possible
3. Implement health checks
4. Monitor resource usage

### Platform Optimizations
{self._get_platform_optimizations()}

## Monitoring and Maintenance

### Regular Maintenance
```bash
# Weekly cleanup
docker system prune

# Monthly deep clean
docker system prune -a --volumes

# Check disk usage
docker system df

# Monitor running containers
docker stats
```

### Health Monitoring
```bash
# Check container health
docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"

# View container logs
docker logs -f container_name

# Check resource usage
docker stats --no-stream
```

## Emergency Recovery

### If Docker Desktop Won't Start
1. Restart computer
2. Reset Docker Desktop to factory defaults
3. Reinstall Docker Desktop
4. Check system requirements

### If Containers Won't Start
1. Check available resources
2. Verify port conflicts
3. Review container logs
4. Reset Docker networks

### If Performance is Poor
1. Increase resource allocation
2. Close unnecessary applications
3. Check for runaway containers
4. Optimize Dockerfiles

## Getting Help

### Diagnostic Information to Collect
```bash
# System information
{self._get_system_info_command()}

# Docker information
docker version
docker info
docker system df

# Container information
docker ps -a
docker images
docker network ls
docker volume ls
```

### Support Resources
- Docker Desktop Issues: https://github.com/docker/for-mac/issues
- Docker Community: https://forums.docker.com
- Docker Documentation: https://docs.docker.com
- Stack Overflow: docker-desktop tag

---
*Generated by Docker Desktop Specialist Agent*
"""
        
        # Save guide
        output_file = self.research_output / f"{timestamp}_troubleshooting_guide.md"
        with open(output_file, 'w') as f:
            f.write(guide)
        
        return guide
    
    def _get_restart_command(self) -> str:
        """Get platform-specific restart command"""
        if self.platform == DockerDesktopPlatform.MACOS:
            return "killall Docker && open /Applications/Docker.app"
        elif self.platform == DockerDesktopPlatform.WINDOWS:
            return "Restart Docker Desktop from system tray"
        else:
            return "systemctl restart docker"
    
    def _get_reset_command(self) -> str:
        """Get platform-specific reset command"""
        if self.platform == DockerDesktopPlatform.MACOS:
            return "Docker Desktop > Troubleshoot > Reset to factory defaults"
        elif self.platform == DockerDesktopPlatform.WINDOWS:
            return "Docker Desktop > Troubleshoot > Reset to factory defaults"
        else:
            return "docker system prune -a --volumes && systemctl restart docker"
    
    def _get_port_check_command(self) -> str:
        """Get platform-specific port check command"""
        if self.platform == DockerDesktopPlatform.WINDOWS:
            return "netstat -an | findstr :PORT"
        else:
            return "lsof -i :PORT"
    
    def _get_permission_fix(self) -> str:
        """Get platform-specific permission fix"""
        if self.platform == DockerDesktopPlatform.LINUX:
            return "Add user to docker group: sudo usermod -aG docker $USER"
        else:
            return "Check Docker Desktop permissions in system settings"
    
    def _get_port_test_commands(self) -> str:
        """Get port testing commands"""
        return """# Test port accessibility
curl -f http://localhost:3000 || echo "Port 3000 not accessible"
curl -f http://localhost:8000 || echo "Port 8000 not accessible"
nc -zv localhost 5432 || echo "Port 5432 not accessible"
nc -zv localhost 6379 || echo "Port 6379 not accessible\""""
    
    def _get_platform_specific_section(self) -> str:
        """Get platform-specific troubleshooting section"""
        if self.platform == DockerDesktopPlatform.MACOS:
            return """
#### macOS Issues

**Rosetta 2 (Apple Silicon)**
- Install: `softwareupdate --install-rosetta`
- Enable in Docker Desktop for x86 compatibility

**File Sharing Performance**
- Use VirtioFS (experimental)
- Limit shared directories
- Use named volumes when possible

**Memory Pressure**
- Check Activity Monitor
- Close memory-intensive apps
- Increase Docker memory allocation
"""
        
        elif self.platform == DockerDesktopPlatform.WINDOWS:
            return """
#### Windows Issues

**WSL 2 Integration**
- Update WSL: `wsl --update`
- Restart WSL: `wsl --shutdown && wsl`
- Check distribution: `wsl --list --verbose`

**Hyper-V Conflicts**
- Disable conflicting virtualization software
- Check Windows features
- Verify BIOS virtualization settings

**Performance Issues**
- Use WSL 2 backend
- Keep WSL kernel updated
- Use Linux containers
"""
        
        else:
            return """
#### Linux Issues

**Permissions**
- Add user to docker group: `sudo usermod -aG docker $USER`
- Restart session after group change
- Check Docker socket: `ls -la /var/run/docker.sock`

**Systemd Integration**
- Enable Docker service: `sudo systemctl enable docker`
- Start Docker service: `sudo systemctl start docker`
- Check service status: `sudo systemctl status docker`

**Resource Limits**
- Check kernel version: `uname -r`
- Verify KVM support: `kvm-ok`
- Monitor system resources: `htop`
"""
    
    def _get_platform_optimizations(self) -> str:
        """Get platform-specific optimizations"""
        if self.platform == DockerDesktopPlatform.MACOS:
            return """
### macOS Optimizations
- Enable VirtioFS for better file system performance
- Use gRPC FUSE for file sharing if VirtioFS unavailable
- Allocate 50-70% of available RAM to Docker
- Use SSD storage for Docker data directory
"""
        elif self.platform == DockerDesktopPlatform.WINDOWS:
            return """
### Windows Optimizations
- Use WSL 2 backend instead of Hyper-V
- Enable WSL 2 integration for all distributions
- Store code in WSL 2 filesystem for better performance
- Use Windows Terminal for better CLI experience
"""
        else:
            return """
### Linux Optimizations
- Use native Docker Engine for best performance
- Configure systemd for service management
- Use overlay2 storage driver
- Enable cgroup v2 for better resource management
"""
    
    def _get_system_info_command(self) -> str:
        """Get platform-specific system info command"""
        if self.platform == DockerDesktopPlatform.MACOS:
            return "system_profiler SPSoftwareDataType SPHardwareDataType"
        elif self.platform == DockerDesktopPlatform.WINDOWS:
            return "systeminfo"
        else:
            return "uname -a && lscpu && free -h"
    
    async def generate_setup_script(self, project_type: str = "fed_job_advisor") -> str:
        """
        Generate Docker Desktop setup script for Fed Job Advisor
        """
        timestamp = datetime.now().isoformat()
        
        if self.platform == DockerDesktopPlatform.MACOS:
            script = f"""#!/bin/bash
# Docker Desktop Setup Script for Fed Job Advisor (macOS)
# Generated: {timestamp}

set -e

echo "🐳 Setting up Docker Desktop for Fed Job Advisor development..."

# Check if Docker Desktop is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker Desktop is not installed"
    echo "📥 Download from: https://desktop.docker.com/mac/main/amd64/Docker.dmg"
    echo "🍎 For Apple Silicon: https://desktop.docker.com/mac/main/arm64/Docker.dmg"
    exit 1
fi

# Check if Docker Desktop is running
if ! docker info &> /dev/null; then
    echo "🚀 Starting Docker Desktop..."
    open /Applications/Docker.app
    echo "⏳ Waiting for Docker Desktop to start..."
    sleep 30
    
    # Wait for Docker to be ready
    timeout=60
    while ! docker info &> /dev/null && [ $timeout -gt 0 ]; do
        echo "⏳ Waiting for Docker daemon..."
        sleep 5
        timeout=$((timeout-5))
    done
    
    if ! docker info &> /dev/null; then
        echo "❌ Docker Desktop failed to start"
        exit 1
    fi
fi

echo "✅ Docker Desktop is running"

# Check resource allocation
echo "🔍 Checking Docker resource allocation..."
docker system df

# Enable BuildKit
echo "🚀 Enabling BuildKit..."
echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> ~/.bashrc

# Create Fed Job Advisor network
echo "🌐 Creating Fed Job Advisor network..."
docker network create fja-network 2>/dev/null || echo "Network already exists"

# Pull base images
echo "📥 Pulling base images..."
docker pull node:18-alpine
docker pull python:3.11-slim
docker pull postgres:15-alpine
docker pull redis:7-alpine

# Create volumes
echo "💾 Creating persistent volumes..."
docker volume create fja-postgres-data 2>/dev/null || echo "Volume already exists"
docker volume create fja-redis-data 2>/dev/null || echo "Volume already exists"

# Test setup
echo "🧪 Testing Docker setup..."
docker run --rm hello-world

echo "✅ Docker Desktop setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Navigate to your Fed Job Advisor project directory"
echo "2. Run: docker-compose up"
echo "3. Open http://localhost:3000 for frontend"
echo "4. Open http://localhost:8000/docs for API docs"
echo ""
echo "🔧 Recommended Docker Desktop settings:"
echo "  Memory: 8GB"
echo "  CPU: 4 cores"
echo "  Disk: 100GB"
echo "  File Sharing: Enable for project directory"
"""
        
        elif self.platform == DockerDesktopPlatform.WINDOWS:
            script = f"""@echo off
REM Docker Desktop Setup Script for Fed Job Advisor (Windows)
REM Generated: {timestamp}

echo 🐳 Setting up Docker Desktop for Fed Job Advisor development...

REM Check if Docker Desktop is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Desktop is not installed
    echo 📥 Download from: https://desktop.docker.com/win/main/amd64/Docker%%20Desktop%%20Installer.exe
    exit /b 1
)

REM Check if Docker Desktop is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo 🚀 Please start Docker Desktop manually
    echo ⏳ Waiting for Docker Desktop to start...
    timeout /t 30 >nul
    
    docker info >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Docker Desktop is not responding
        echo Please start Docker Desktop and run this script again
        exit /b 1
    )
)

echo ✅ Docker Desktop is running

REM Check WSL 2 integration
echo 🔍 Checking WSL 2 integration...
wsl --list --verbose

REM Enable BuildKit
echo 🚀 Enabling BuildKit...
setx DOCKER_BUILDKIT 1
setx COMPOSE_DOCKER_CLI_BUILD 1

REM Create Fed Job Advisor network
echo 🌐 Creating Fed Job Advisor network...
docker network create fja-network 2>nul || echo Network already exists

REM Pull base images
echo 📥 Pulling base images...
docker pull node:18-alpine
docker pull python:3.11-slim
docker pull postgres:15-alpine
docker pull redis:7-alpine

REM Create volumes
echo 💾 Creating persistent volumes...
docker volume create fja-postgres-data 2>nul || echo Volume already exists
docker volume create fja-redis-data 2>nul || echo Volume already exists

REM Test setup
echo 🧪 Testing Docker setup...
docker run --rm hello-world

echo ✅ Docker Desktop setup complete!
echo.
echo 📋 Next steps:
echo 1. Navigate to your Fed Job Advisor project directory
echo 2. Run: docker-compose up
echo 3. Open http://localhost:3000 for frontend
echo 4. Open http://localhost:8000/docs for API docs
echo.
echo 🔧 Recommended Docker Desktop settings:
echo   Memory: 8GB
echo   CPU: 4 cores
echo   Disk: 100GB
echo   Use WSL 2 backend
echo   Enable WSL 2 integration
"""
        
        else:  # Linux
            script = f"""#!/bin/bash
# Docker Desktop Setup Script for Fed Job Advisor (Linux)
# Generated: {timestamp}

set -e

echo "🐳 Setting up Docker for Fed Job Advisor development..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "📥 Install with: curl -fsSL https://get.docker.com | sh"
    exit 1
fi

# Check if user is in docker group
if ! groups $USER | grep -q docker; then
    echo "👤 Adding user to docker group..."
    sudo usermod -aG docker $USER
    echo "🔄 Please log out and back in, then run this script again"
    exit 1
fi

# Start Docker service
echo "🚀 Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker service failed to start"
    sudo systemctl status docker
    exit 1
fi

echo "✅ Docker is running"

# Enable BuildKit
echo "🚀 Enabling BuildKit..."
echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc
echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> ~/.bashrc

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "📥 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Create Fed Job Advisor network
echo "🌐 Creating Fed Job Advisor network..."
docker network create fja-network 2>/dev/null || echo "Network already exists"

# Pull base images
echo "📥 Pulling base images..."
docker pull node:18-alpine
docker pull python:3.11-slim
docker pull postgres:15-alpine
docker pull redis:7-alpine

# Create volumes
echo "💾 Creating persistent volumes..."
docker volume create fja-postgres-data 2>/dev/null || echo "Volume already exists"
docker volume create fja-redis-data 2>/dev/null || echo "Volume already exists"

# Test setup
echo "🧪 Testing Docker setup..."
docker run --rm hello-world

echo "✅ Docker setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Navigate to your Fed Job Advisor project directory"
echo "2. Run: docker-compose up"
echo "3. Open http://localhost:3000 for frontend"
echo "4. Open http://localhost:8000/docs for API docs"
echo ""
echo "🔧 Recommended system requirements:"
echo "  RAM: 8GB+"
echo "  Storage: 100GB+ available"
echo "  CPU: 4+ cores"
"""
        
        # Save script
        script_name = f"setup_docker_desktop_{self.platform.value}.{'sh' if self.platform != DockerDesktopPlatform.WINDOWS else 'bat'}"
        output_file = self.research_output / f"{timestamp}_{script_name}"
        with open(output_file, 'w') as f:
            f.write(script)
        
        return script

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    specialist = DockerDesktopSpecialist()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "diagnose":
            # Example: python docker_desktop_specialist.py diagnose "cannot connect" "permission denied"
            symptoms = sys.argv[2:] if len(sys.argv) > 2 else ["connection issues"]
            result = asyncio.run(specialist.diagnose_docker_desktop_issue(symptoms))
            print(json.dumps(result, indent=2))
        
        elif command == "guide":
            # Generate troubleshooting guide
            guide = asyncio.run(specialist.generate_troubleshooting_guide())
            print(guide)
        
        elif command == "setup":
            # Generate setup script
            script = asyncio.run(specialist.generate_setup_script())
            print(script)
        
        elif command == "optimize":
            # Example: python docker_desktop_specialist.py optimize
            config = {
                "memory_gb": 4,
                "cpu_cores": 2,
                "disk_gb": 64,
                "buildkit_enabled": True
            }
            result = asyncio.run(specialist.optimize_docker_desktop(config))
            print(json.dumps(result, indent=2))
    else:
        print("Docker Desktop Specialist Agent")
        print(f"Platform: {specialist.platform.value}")
        print("Commands:")
        print("  diagnose <symptoms...> - Diagnose Docker Desktop issues")
        print("  guide - Generate troubleshooting guide")
        print("  setup - Generate setup script")
        print("  optimize - Optimize Docker Desktop configuration")
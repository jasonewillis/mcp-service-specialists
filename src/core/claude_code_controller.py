#!/usr/bin/env python3
"""
Claude Code Controller for Virtual Development Team
Main API interface for controlling the agent system
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

# Import agent components
from agents.app.agents.enhanced_factory import EnhancedAgentFactory
from agents.app.orchestrator.virtual_team_orchestrator import (
    VirtualTeamOrchestrator,
    TaskPriority,
    TaskStatus
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Request/Response Models
class TaskRequest(BaseModel):
    """Request model for task execution"""
    description: str = Field(..., description="Task description")
    priority: str = Field(default="medium", description="Task priority: low, medium, high, critical")
    agents: Optional[List[str]] = Field(default=None, description="Specific agents to use")
    parallel: bool = Field(default=True, description="Execute subtasks in parallel")
    require_approval: bool = Field(default=False, description="Require human approval")
    max_retries: int = Field(default=3, description="Maximum retry attempts")

class AgentExecutionRequest(BaseModel):
    """Request model for direct agent execution"""
    agent: str = Field(..., description="Agent role to execute")
    task: str = Field(..., description="Task for the agent")
    
class SystemConfigRequest(BaseModel):
    """Request model for system configuration"""
    temperature: Optional[float] = Field(default=None, description="LLM temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens")
    timeout: Optional[int] = Field(default=None, description="Execution timeout")

class ClaudeCodeController:
    """Main controller for Claude Code integration with virtual team"""
    
    def __init__(self):
        """Initialize the controller"""
        self.app = FastAPI(
            title="Virtual Development Team Controller",
            description="API for controlling AI agent team with local LLMs",
            version="1.0.0"
        )
        
        # Initialize components
        self.factory = None
        self.orchestrator = None
        self.active_sessions = {}
        self.system_status = "initializing"
        
        # Setup middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Setup routes
        self.setup_routes()
        
        # Initialize system on startup
        self.app.add_event_handler("startup", self.startup_event)
        self.app.add_event_handler("shutdown", self.shutdown_event)
        
        logger.info("Claude Code Controller initialized")
    
    async def startup_event(self):
        """Initialize system on startup"""
        logger.info("Starting Virtual Development Team...")
        
        try:
            # Initialize factory and orchestrator
            self.factory = EnhancedAgentFactory()
            self.orchestrator = VirtualTeamOrchestrator(self.factory)
            
            self.system_status = "operational"
            logger.info("✅ Virtual Development Team is operational")
            
        except Exception as e:
            logger.error(f"Failed to initialize system: {e}")
            self.system_status = "error"
    
    async def shutdown_event(self):
        """Cleanup on shutdown"""
        logger.info("Shutting down Virtual Development Team...")
        self.system_status = "shutdown"
    
    def setup_routes(self):
        """Setup API routes"""
        
        # Health and status endpoints
        @self.app.get("/")
        async def root():
            """Root endpoint"""
            return {
                "name": "Virtual Development Team Controller",
                "status": self.system_status,
                "docs": "/docs",
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": self.system_status,
                "agents_loaded": len(self.factory.agents) if self.factory else 0,
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.get("/status")
        async def get_status():
            """Get detailed system status"""
            if not self.factory:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            return {
                "status": self.system_status,
                "agents": {
                    "total": len(self.factory.agents),
                    "available": self.factory.list_agents()
                },
                "models": {
                    "loaded": len(self.factory.models),
                    "configuration": self.factory.config["models"]
                },
                "orchestrator": {
                    "active_tasks": len(self.orchestrator.active_tasks) if self.orchestrator else 0
                },
                "timestamp": datetime.now().isoformat()
            }
        
        # Agent management endpoints
        @self.app.get("/agents")
        async def list_agents():
            """List all available agents"""
            if not self.factory:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            return {
                "agents": self.factory.get_all_agents_info(),
                "total": len(self.factory.agents)
            }
        
        @self.app.get("/agents/{agent_role}")
        async def get_agent_info(agent_role: str):
            """Get information about a specific agent"""
            if not self.factory:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            info = self.factory.get_agent_info(agent_role)
            if "error" in info:
                raise HTTPException(status_code=404, detail=info["error"])
            
            return info
        
        @self.app.post("/agents/execute")
        async def execute_agent_task(request: AgentExecutionRequest):
            """Execute a task with a specific agent"""
            if not self.factory:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            try:
                result = await self.factory.execute_task(request.agent, request.task)
                return {
                    "status": "success",
                    "agent": request.agent,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.error(f"Error executing agent task: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Task orchestration endpoints
        @self.app.post("/execute")
        async def execute_task(request: TaskRequest, background_tasks: BackgroundTasks):
            """Execute a complex task with the virtual team"""
            if not self.orchestrator:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            # Convert priority string to enum
            priority_map = {
                "critical": TaskPriority.CRITICAL,
                "high": TaskPriority.HIGH,
                "medium": TaskPriority.MEDIUM,
                "low": TaskPriority.LOW
            }
            priority = priority_map.get(request.priority.lower(), TaskPriority.MEDIUM)
            
            try:
                # Execute task
                result = await self.orchestrator.execute_task(
                    task_description=request.description,
                    priority=priority,
                    agents=request.agents,
                    require_human_approval=request.require_approval,
                    max_iterations=request.max_retries
                )
                
                return {
                    "status": "completed",
                    "task_id": result["task_id"],
                    "results": result["results"],
                    "errors": result["errors"],
                    "execution_time": result["execution_time"],
                    "progress": result["progress"]
                }
                
            except Exception as e:
                logger.error(f"Error executing task: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/tasks")
        async def list_tasks():
            """List all active tasks"""
            if not self.orchestrator:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            return {
                "tasks": self.orchestrator.list_active_tasks(),
                "total": len(self.orchestrator.active_tasks)
            }
        
        @self.app.get("/tasks/{task_id}")
        async def get_task_status(task_id: str):
            """Get status of a specific task"""
            if not self.orchestrator:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            status = self.orchestrator.get_task_status(task_id)
            if not status:
                raise HTTPException(status_code=404, detail="Task not found")
            
            return status
        
        # Configuration endpoints
        @self.app.post("/config")
        async def update_configuration(request: SystemConfigRequest):
            """Update system configuration"""
            if not self.factory:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            updates = {}
            
            if request.temperature is not None:
                self.factory.config["agent_settings"]["temperature"] = request.temperature
                updates["temperature"] = request.temperature
            
            if request.max_tokens is not None:
                self.factory.config["agent_settings"]["max_tokens"] = request.max_tokens
                updates["max_tokens"] = request.max_tokens
            
            if request.timeout is not None:
                self.factory.config["agent_settings"]["timeout"] = request.timeout
                updates["timeout"] = request.timeout
            
            # Reinitialize models with new config
            if updates:
                self.factory._initialize_models()
            
            return {
                "status": "updated",
                "updates": updates,
                "current_config": self.factory.config["agent_settings"]
            }
        
        @self.app.get("/config")
        async def get_configuration():
            """Get current system configuration"""
            if not self.factory:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            return {
                "models": self.factory.config["models"],
                "settings": self.factory.config["agent_settings"]
            }
        
        # Fed Job Advisor integration endpoints
        @self.app.post("/fedjob/enhance-matching")
        async def enhance_job_matching(resume: Dict[str, Any]):
            """Enhance job matching using virtual team"""
            if not self.orchestrator:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            task_description = f"""
            Analyze the following resume and provide:
            1. Skills analysis and recommendations
            2. Federal job match scores
            3. Tailored cover letter
            4. Compliance check for federal requirements
            
            Resume: {json.dumps(resume)}
            """
            
            result = await self.orchestrator.execute_task(
                task_description=task_description,
                priority=TaskPriority.HIGH,
                agents=["data_scientist", "content_creator", "compliance_officer"]
            )
            
            return result
        
        @self.app.post("/fedjob/automate-issue/{issue_number}")
        async def automate_github_issue(issue_number: int, background_tasks: BackgroundTasks):
            """Automate development from GitHub issue"""
            if not self.orchestrator:
                raise HTTPException(status_code=503, detail="System not initialized")
            
            task_description = f"""
            Implement GitHub issue #{issue_number}:
            1. Analyze the issue requirements
            2. Create implementation plan
            3. Write the code
            4. Create tests
            5. Generate documentation
            """
            
            # Execute in background
            background_tasks.add_task(
                self._process_github_issue,
                issue_number,
                task_description
            )
            
            return {
                "status": "processing",
                "issue": issue_number,
                "message": "Task queued for processing"
            }
        
        # Utility endpoints
        @self.app.get("/logs")
        async def get_logs(limit: int = 100):
            """Get recent system logs"""
            # In production, would read from actual log file
            return {
                "logs": [],
                "message": "Log retrieval not implemented"
            }
        
        @self.app.post("/reset")
        async def reset_system():
            """Reset the system"""
            try:
                # Reinitialize components
                self.factory = EnhancedAgentFactory()
                self.orchestrator = VirtualTeamOrchestrator(self.factory)
                self.active_sessions = {}
                
                return {
                    "status": "reset",
                    "message": "System reset successfully"
                }
            except Exception as e:
                logger.error(f"Error resetting system: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def _process_github_issue(self, issue_number: int, task_description: str):
        """Process GitHub issue in background"""
        try:
            result = await self.orchestrator.execute_task(
                task_description=task_description,
                priority=TaskPriority.HIGH,
                agents=["project_manager", "backend_engineer", "frontend_developer", "devops_engineer"],
                require_human_approval=True
            )
            
            logger.info(f"GitHub issue #{issue_number} processed: {result['status']}")
            
        except Exception as e:
            logger.error(f"Error processing GitHub issue #{issue_number}: {e}")
    
    def run(self, host: str = "127.0.0.1", port: int = 8002):
        """Run the controller"""
        logger.info(f"Starting Virtual Development Team Controller on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port, log_level="info")

# Main execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Virtual Development Team Controller")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8002, help="Port to bind to")
    
    args = parser.parse_args()
    
    controller = ClaudeCodeController()
    controller.run(host=args.host, port=args.port)
"""
Federal Job Advisory Agent System
Main FastAPI application for agent services
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import os
from dotenv import load_dotenv
import structlog
import json

from ..agents.app.agents.factory import AgentFactory, AgentRoles
from ..agents.app.agents.base import AgentConfig

# Import all agents
from ..agents.app.agents.roles.data_scientist import DataScientistAgent
from ..agents.app.agents.roles.statistician import StatisticianAgent
from ..agents.app.agents.roles.database_admin import DatabaseAdminAgent
from ..agents.app.agents.roles.devops_engineer import DevOpsEngineerAgent
from ..agents.app.agents.roles.it_specialist import ITSpecialistAgent
from ..agents.app.agents.compliance.essay_guidance import EssayGuidanceAgent
from ..agents.app.agents.compliance.resume_compression import ResumeCompressionAgent
from ..agents.app.agents.compliance.executive_order_research import ExecutiveOrderResearchAgent
from ..agents.app.agents.automation.job_collection_orchestrator import JobCollectionOrchestratorAgent
from ..agents.app.agents.automation.analytics_intelligence import AnalyticsIntelligenceAgent
from ..agents.app.agents.roles.agent_router import AgentRouter
from ..agents.app.agents.roles.general_purpose import GeneralPurposeAgent
from ..agents.app.agents.roles.researcher import ResearcherAgent
from ..agents.app.agents.roles.ux_designer import UXDesignerAgent

# Import LangGraph orchestrator and related components - Temporarily disabled
# from ..agents.app.orchestrator.fed_job_orchestrator import get_orchestrator, WorkflowType
# from ..agents.app.orchestrator.debugging.time_travel import DebugLevel
# from ..agents.app.orchestrator.compliance.merit_hiring_gates import get_compliance_gates

# Temporary stubs for disabled orchestrator
class WorkflowType:
    pass

def get_orchestrator():
    return None

class DebugLevel:
    STANDARD = "standard"
    DETAILED = "detailed"

def get_compliance_gates():
    return None

# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="Federal Job Advisory Agent System",
    description="AI-powered agents for federal job application assistance",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class AgentRequest(BaseModel):
    """Request model for agent interactions"""
    role: str
    user_id: str
    query: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    stream: bool = False


class AgentAnalysisRequest(BaseModel):
    """Request model for agent analysis"""
    role: str
    user_id: str
    data: Dict[str, Any]


class EssayAnalysisRequest(BaseModel):
    """Request model for essay analysis"""
    user_id: str
    essay_text: str
    essay_number: int
    experience: Optional[str] = ""


class DataScientistAnalysisRequest(BaseModel):
    """Request model for data scientist analysis"""
    user_id: str
    skills: List[str]
    experience: str
    projects: Optional[List[Dict]] = []
    education: Optional[Dict] = {}
    target_grade: str = "GS-13"


class OrchestratorRequest(BaseModel):
    """Request model for LangGraph orchestrator"""
    user_id: str
    query: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    enable_streaming: bool = True
    debug_mode: bool = False


class StreamingStatusRequest(BaseModel):
    """Request model for streaming status check"""
    session_id: str


class CheckpointReplayRequest(BaseModel):
    """Request model for checkpoint replay"""
    session_id: str
    checkpoint_id: str


class WebscrapingRequest(BaseModel):
    """Request model for webscraping operations"""
    user_id: str
    data: Dict[str, Any]


# Global orchestrator instance
orchestrator = None
compliance_gates = None


# Startup/Shutdown Events
@app.on_event("startup")
async def startup_event():
    """Initialize agents and orchestrator on startup"""
    global orchestrator, compliance_gates
    
    logger.info("Starting Federal Job Advisory Agent System with LangGraph Integration")
    
    # Initialize LangGraph orchestrator
    enable_time_travel = os.getenv("ENABLE_TIME_TRAVEL", "true").lower() == "true"
    debug_level_str = os.getenv("DEBUG_LEVEL", "detailed").lower()
    
    # Fix: Use correct DebugLevel enum values
    debug_level = DebugLevel.DETAILED if debug_level_str == "detailed" else DebugLevel.STANDARD
    
    try:
        # Skip complex orchestrator initialization for now - just basic agent setup
        logger.info("Starting with basic agent setup (orchestrator disabled)")
        orchestrator = None
        compliance_gates = None
        
    except Exception as e:
        logger.error(f"Failed to initialize agent system: {e}")
        # Continue without orchestrator for basic health checks
        orchestrator = None
        compliance_gates = None
    
    # Register ALL 13 Fed Job Advisor agents (10 original + 3 new general-purpose)
    agents_to_register = [
        # Technical Role Agents (5)
        (AgentRoles.DATA_SCIENTIST, DataScientistAgent, {
            "description": "Data science and ML/AI development specialist",
            "tools": ["skill_matcher", "project_analyzer", "technical_depth_checker"]
        }),
        (AgentRoles.STATISTICIAN, StatisticianAgent, {
            "description": "Statistical analysis and hypothesis testing specialist",
            "tools": ["statistical_analyzer", "data_visualizer", "test_designer"]
        }),
        (AgentRoles.DATABASE_ADMIN, DatabaseAdminAgent, {
            "description": "Database administration and optimization specialist",
            "tools": ["query_optimizer", "schema_manager", "performance_monitor"]
        }),
        (AgentRoles.DEVOPS, DevOpsEngineerAgent, {
            "description": "DevOps and infrastructure specialist for deployment, monitoring, and backup systems",
            "tools": ["infrastructure_analyzer", "deployment_manager", "backup_monitor"]
        }),
        (AgentRoles.IT_SPECIALIST, ITSpecialistAgent, {
            "description": "IT systems and technical support specialist",
            "tools": ["system_diagnostics", "technical_troubleshooter", "configuration_manager"]
        }),
        
        # Compliance Agents (3)
        (AgentRoles.ESSAY_GUIDANCE, EssayGuidanceAgent, {
            "description": "Merit hiring compliance and essay writing guidance specialist",
            "tools": ["merit_analyzer", "compliance_checker", "writing_coach"]
        }),
        (AgentRoles.RESUME_COMPRESSION, ResumeCompressionAgent, {
            "description": "Federal resume optimization and compression specialist",
            "tools": ["resume_optimizer", "keyword_analyzer", "format_validator"]
        }),
        (AgentRoles.EXECUTIVE_ORDER, ExecutiveOrderResearchAgent, {
            "description": "Executive order research and policy compliance specialist",
            "tools": ["policy_researcher", "executive_order_tracker", "compliance_validator"]
        }),
        
        # Analytics & Intelligence Agents (2)
        (AgentRoles.JOB_COLLECTOR, JobCollectionOrchestratorAgent, {
            "description": "Job data collection orchestration and monitoring specialist",
            "tools": ["collection_monitor", "pipeline_orchestrator", "data_quality_checker"]
        }),
        (AgentRoles.ANALYTICS, AnalyticsIntelligenceAgent, {
            "description": "Job market analytics and intelligence specialist", 
            "tools": ["market_analyzer", "trend_tracker", "intelligence_aggregator"]
        }),
        
        # General-Purpose Agents (3)
        (AgentRoles.GENERAL_PURPOSE, GeneralPurposeAgent, {
            "description": "General research, analysis, and multi-step task coordination specialist",
            "tools": ["research_analyzer", "problem_solver", "task_coordinator", "requirements_gatherer", "risk_assessor"]
        }),
        (AgentRoles.RESEARCHER, ResearcherAgent, {
            "description": "Deep research, investigation, and information gathering specialist",
            "tools": ["research_planner", "source_evaluator", "information_synthesizer", "fact_checker", "trend_analyzer", "gap_identifier"]
        }),
        (AgentRoles.UX_DESIGNER, UXDesignerAgent, {
            "description": "UX/UI design, web design, and user experience specialist with federal compliance focus",
            "tools": ["accessibility_auditor", "user_flow_analyzer", "design_system_advisor", "shadcn_ui_components", "usability_evaluator", "responsive_design_checker", "federal_compliance_validator"]
        })
    ]
    
    registered_count = 0
    for role, agent_class, metadata in agents_to_register:
        try:
            AgentFactory.register_agent(role, agent_class, metadata=metadata)
            logger.info(f"Registered {agent_class.__name__}")
            registered_count += 1
        except Exception as e:
            logger.warning(f"Failed to register {agent_class.__name__}: {e}")
    
    logger.info(f"Successfully registered {registered_count} agents")
    
    logger.info(f"Registered {len(AgentFactory.list_available_agents())} agents")
    logger.info("Federal Job Advisory Agent System with LangGraph ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global orchestrator, compliance_gates
    
    logger.info("Shutting down agent system and orchestrator")
    await AgentFactory.cleanup_all_agents()
    
    # Cleanup orchestrator resources if needed
    if orchestrator:
        logger.info("Orchestrator cleanup completed")
    
    orchestrator = None
    compliance_gates = None


# Health Check Endpoints
@app.get("/health")
async def health_check():
    """Basic health check including orchestrator status"""
    orchestrator_status = "healthy" if orchestrator else "not_initialized"
    compliance_status = "healthy" if compliance_gates else "not_initialized"
    
    return {
        "status": "healthy", 
        "service": "agent-system",
        "orchestrator": orchestrator_status,
        "compliance_gates": compliance_status,
        "time_travel_enabled": orchestrator.time_travel_enabled if orchestrator else False
    }


@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": AgentFactory.list_available_agents(),
        "total": len(AgentFactory.list_available_agents())
    }


# Agent Interaction Endpoints
@app.post("/agents/process")
async def process_with_agent(request: AgentRequest):
    """Process a query with the specified agent"""
    try:
        # Create or get agent
        agent = AgentFactory.create(
            role=request.role,
            user_id=request.user_id
        )
        
        # Handle streaming response
        if request.stream:
            async def generate():
                async for chunk in agent.stream_response(
                    request.query or "",
                    request.data
                ):
                    yield json.dumps({"chunk": chunk}) + "\n"
            
            return StreamingResponse(generate(), media_type="application/x-ndjson")
        
        # Regular response
        response = await agent.process(
            request.query or "",
            request.data
        )
        
        return response.dict()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Agent processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/agents/analyze")
async def analyze_with_agent(request: AgentAnalysisRequest):
    """Run analysis with the specified agent"""
    try:
        # Create or get agent
        agent = AgentFactory.create(
            role=request.role,
            user_id=request.user_id
        )
        
        # Run analysis
        response = await agent.analyze(request.data)
        
        return response.dict()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Agent analysis error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Specialized Agent Endpoints
@app.post("/agents/data-scientist/analyze")
async def analyze_data_scientist_profile(request: DataScientistAnalysisRequest):
    """Analyze profile for data scientist positions"""
    try:
        # Create agent
        agent = AgentFactory.create(
            role=AgentRoles.DATA_SCIENTIST,
            user_id=request.user_id
        )
        
        # Prepare data
        data = {
            "skills": request.skills,
            "experience": request.experience,
            "projects": request.projects,
            "education": request.education,
            "target_grade": request.target_grade
        }
        
        # Run analysis
        response = await agent.analyze(data)
        
        return response.dict()
        
    except Exception as e:
        logger.error(f"Data scientist analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/essay/analyze")
async def analyze_essay_compliance(request: EssayAnalysisRequest):
    """Analyze essay for Merit Hiring compliance"""
    try:
        # Create agent
        agent = AgentFactory.create(
            role=AgentRoles.ESSAY_GUIDANCE,
            user_id=request.user_id
        )
        
        # Prepare data
        data = {
            "essay_text": request.essay_text,
            "essay_number": request.essay_number,
            "experience": request.experience
        }
        
        # Run analysis
        response = await agent.analyze(data)
        
        return response.dict()
        
    except Exception as e:
        logger.error(f"Essay analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/webscraping/analyze")
async def analyze_webscraping_request(request: WebscrapingRequest):
    """Handle webscraping operations - single page or documentation traversal"""
    try:
        # Import the webscraping specialist
        from ..mcp_services.external.webscraping_specialist import WebscrapingSpecialist
        
        # Create webscraping specialist instance
        scraper = WebscrapingSpecialist()
        
        # Run the analysis/scraping
        response = await scraper.analyze_request(request.user_id, request.data)
        
        return {
            "success": response.get("success", True),
            "message": "Webscraping completed" if response.get("success") else "Webscraping failed",
            "data": response
        }
        
    except Exception as e:
        logger.error(f"Webscraping error: {e}")
        raise HTTPException(status_code=500, detail=f"Webscraping error: {str(e)}")


# Memory Management Endpoints
@app.post("/agents/{role}/{user_id}/reset-memory")
async def reset_agent_memory(role: str, user_id: str):
    """Reset memory for a specific agent"""
    try:
        agent = AgentFactory.create(role, user_id)
        await agent.reset_memory()
        
        return {
            "success": True,
            "message": f"Memory reset for {role} agent (user: {user_id})"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Memory reset error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents/{role}/{user_id}/metrics")
async def get_agent_metrics(role: str, user_id: str):
    """Get performance metrics for a specific agent"""
    try:
        agent = AgentFactory.create(role, user_id)
        metrics = agent.get_metrics()
        
        return {
            "agent": role,
            "user": user_id,
            "metrics": metrics
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Metrics retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# User Management
@app.post("/users/{user_id}/cleanup")
async def cleanup_user_agents(user_id: str, background_tasks: BackgroundTasks):
    """Cleanup all agents for a user"""
    try:
        # Schedule cleanup in background
        background_tasks.add_task(AgentFactory.cleanup_user_agents, user_id)
        
        return {
            "success": True,
            "message": f"Cleanup scheduled for user {user_id}"
        }
        
    except Exception as e:
        logger.error(f"User cleanup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# LangGraph Orchestrator Endpoints
@app.post("/orchestrator/process")
async def process_with_orchestrator(request: OrchestratorRequest):
    """Process a request using the LangGraph orchestrator"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        result = await orchestrator.process_request(
            user_id=request.user_id,
            query=request.query,
            session_id=request.session_id,
            context=request.context,
            enable_streaming=request.enable_streaming,
            debug_mode=request.debug_mode
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Orchestrator processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orchestrator/status/{session_id}")
async def get_real_time_status(session_id: str):
    """Get real-time status of a workflow session"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        status = await orchestrator.get_real_time_status(session_id)
        return status
        
    except Exception as e:
        logger.error(f"Status retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orchestrator/history/{session_id}")
async def get_session_history(session_id: str, include_streaming: bool = True):
    """Get session history and conversation data"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        history = await orchestrator.get_session_history(
            session_id=session_id,
            include_streaming_events=include_streaming
        )
        return history
        
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/orchestrator/replay")
async def replay_from_checkpoint(request: CheckpointReplayRequest):
    """Replay workflow from a specific checkpoint"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    if not orchestrator.time_travel_enabled:
        raise HTTPException(status_code=400, detail="Time travel debugging not enabled")
    
    try:
        result = await orchestrator.replay_from_checkpoint(
            session_id=request.session_id,
            checkpoint_id=request.checkpoint_id
        )
        return result
        
    except Exception as e:
        logger.error(f"Checkpoint replay error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orchestrator/stream/{session_id}")
async def stream_workflow_progress(session_id: str):
    """Stream real-time workflow progress updates"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    async def generate():
        try:
            # Get initial status
            status = await orchestrator.get_real_time_status(session_id)
            yield json.dumps({"type": "status", "data": status}) + "\n"
            
            # Stream updates (simplified implementation)
            # In production, this would connect to actual streaming events
            import asyncio
            while True:
                await asyncio.sleep(1)  # Poll every second
                
                try:
                    status = await orchestrator.get_real_time_status(session_id)
                    if status.get("status") != "not_found":
                        yield json.dumps({"type": "update", "data": status}) + "\n"
                    else:
                        # Session completed or not found
                        yield json.dumps({"type": "completed", "data": status}) + "\n"
                        break
                        
                except Exception as e:
                    yield json.dumps({"type": "error", "error": str(e)}) + "\n"
                    break
                    
        except Exception as e:
            yield json.dumps({"type": "error", "error": str(e)}) + "\n"
    
    return StreamingResponse(generate(), media_type="application/x-ndjson")


# Compliance Gates Endpoints
@app.get("/compliance/status")
async def get_compliance_status():
    """Get real-time compliance system status"""
    if not compliance_gates:
        raise HTTPException(status_code=503, detail="Compliance gates not initialized")
    
    try:
        status = await compliance_gates.get_real_time_status()
        return status
        
    except Exception as e:
        logger.error(f"Compliance status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/compliance/report")
async def get_compliance_report(include_streaming: bool = True):
    """Get comprehensive compliance report"""
    if not compliance_gates:
        raise HTTPException(status_code=503, detail="Compliance gates not initialized")
    
    try:
        report = compliance_gates.export_compliance_report(
            include_streaming_data=include_streaming
        )
        return report
        
    except Exception as e:
        logger.error(f"Compliance report error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/compliance/audit-log")
async def get_compliance_audit_log(limit: Optional[int] = None):
    """Get compliance audit log"""
    if not compliance_gates:
        raise HTTPException(status_code=503, detail="Compliance gates not initialized")
    
    try:
        audit_log = compliance_gates.get_audit_log(limit=limit)
        return {
            "audit_log": audit_log,
            "total_entries": len(compliance_gates.get_audit_log())
        }
        
    except Exception as e:
        logger.error(f"Audit log error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Debug and Development Endpoints
@app.get("/debug/orchestrator")
async def get_orchestrator_debug_info():
    """Get orchestrator debug information"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    return {
        "time_travel_enabled": orchestrator.time_travel_enabled,
        "debug_level": orchestrator.debug_level.value if hasattr(orchestrator, 'debug_level') else "unknown",
        "agents_registered": len(orchestrator.agents),
        "agent_list": list(orchestrator.agents.keys()),
        "checkpointer_type": type(orchestrator.checkpointer).__name__ if orchestrator.checkpointer else None
    }


@app.post("/debug/toggle-streaming")
async def toggle_streaming(enable: bool = True):
    """Toggle streaming for compliance gates (debug only)"""
    if not compliance_gates:
        raise HTTPException(status_code=503, detail="Compliance gates not initialized")
    
    try:
        compliance_gates.streaming_enabled = enable
        return {
            "streaming_enabled": compliance_gates.streaming_enabled,
            "dynamic_interrupts_enabled": compliance_gates.dynamic_interrupts_enabled
        }
        
    except Exception as e:
        logger.error(f"Toggle streaming error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/debug/clear-compliance-events")
async def clear_compliance_streaming_events(keep_recent: int = 100):
    """Clear compliance streaming events (debug only)"""
    if not compliance_gates:
        raise HTTPException(status_code=503, detail="Compliance gates not initialized")
    
    try:
        initial_count = len(compliance_gates.streaming_events)
        compliance_gates.clear_streaming_events(keep_recent=keep_recent)
        final_count = len(compliance_gates.streaming_events)
        
        return {
            "cleared": initial_count - final_count,
            "remaining": final_count,
            "kept_recent": keep_recent
        }
        
    except Exception as e:
        logger.error(f"Clear events error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Test Endpoints (Development only)
if os.getenv("API_RELOAD", "false").lower() == "true":
    @app.post("/test/ollama")
    async def test_ollama_connection():
        """Test Ollama connection"""
        try:
            import ollama
            client = ollama.Client()
            
            # Test with simple prompt
            response = client.generate(
                model=os.getenv("OLLAMA_MODEL", "gpt-oss:latest"),
                prompt="Say 'Connected' if you can read this"
            )
            
            return {
                "connected": True,
                "model": os.getenv("OLLAMA_MODEL", "gpt-oss:latest"),
                "response": response.get("response", "")[:100]
            }
            
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }


def main():
    """Main entry point for the application"""
    import uvicorn
    
    uvicorn.run(
        "src.core.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8001")),
        reload=os.getenv("API_RELOAD", "true").lower() == "true"
    )

if __name__ == "__main__":
    main()
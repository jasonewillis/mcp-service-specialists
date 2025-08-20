"""
User-Facing Subgraph for Fed Job Advisor

Organizes and coordinates the 10 user-facing agents:
- Role analysis agents (Data Scientist, Statistician, DBA, DevOps, IT Specialist)
- Compliance agents (Essay Guidance, Resume Compression, Executive Order Research)
- Analytics agents (Job Market Analytics, Job Collection Orchestrator)

Implements conditional routing based on job series and requirements with parallel execution.
"""

from typing import Dict, Any, List, Optional, TypedDict, Union
from datetime import datetime
import asyncio
import logging
from enum import Enum
import sqlite3
from pathlib import Path

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import Send
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

# Import agent types
from agents.app.agents.base import FederalJobAgent, AgentConfig, AgentResponse
from agents.app.agents.roles.data_scientist import DataScientist
from agents.app.agents.roles.statistician import Statistician
from agents.app.agents.roles.database_admin import DatabaseAdmin
from agents.app.agents.roles.devops_engineer import DevOpsEngineer
from agents.app.agents.roles.it_specialist import ITSpecialist
from agents.app.agents.compliance.essay_guidance import EssayGuidanceAgent
from agents.app.agents.compliance.resume_compression import ResumeCompressionAgent
from agents.app.agents.compliance.executive_order_research import ExecutiveOrderResearchAgent
from agents.app.agents.automation.analytics_intelligence import AnalyticsIntelligence
from agents.app.agents.automation.job_collection_orchestrator import JobCollectionOrchestrator

logger = logging.getLogger(__name__)


class UserQueryType(Enum):
    """Types of user queries this subgraph can handle"""
    JOB_ANALYSIS = "job_analysis"
    CAREER_GUIDANCE = "career_guidance"
    RESUME_HELP = "resume_help"
    ESSAY_GUIDANCE = "essay_guidance"
    COMPLIANCE_CHECK = "compliance_check"
    MARKET_RESEARCH = "market_research"
    DATA_ANALYSIS = "data_analysis"
    TECHNICAL_ROLE = "technical_role"
    GENERAL_INQUIRY = "general_inquiry"


class JobSeries(Enum):
    """Federal job series that require specific expertise"""
    # IT Series
    IT_SPECIALIST = "2210"
    CYBERSECURITY = "2210"
    DEVOPS = "0301"
    
    # Data Series
    DATA_SCIENTIST = "1560"
    STATISTICIAN = "1530"
    DATABASE_ADMIN = "0334"
    
    # General
    MANAGEMENT = "0340"
    ANALYST = "0343"
    OTHER = "other"


class UserFacingState(TypedDict):
    """State for user-facing workflow processing with streaming and checkpoints"""
    # Query Information
    original_query: str
    query_type: UserQueryType
    job_series: Optional[JobSeries]
    user_profile: Dict[str, Any]
    
    # Agent Coordination
    primary_agents: List[str]
    supporting_agents: List[str]
    agent_results: Dict[str, Any]
    agent_errors: Dict[str, str]
    active_parallel_tasks: List[str]
    
    # Processing Control
    parallel_execution: bool
    requires_compliance_check: bool
    needs_human_review: bool
    interrupt_before_essay: bool
    streaming_enabled: bool
    
    # Progress Tracking
    current_phase: str
    completed_phases: List[str]
    progress_percentage: float
    
    # Results
    consolidated_response: str
    actionable_recommendations: List[str]
    next_steps: List[str]
    warnings: List[str]
    
    # Streaming Events
    events: List[Dict[str, Any]]
    
    # Metadata
    processing_time: float
    confidence_score: float
    sources_used: List[str]
    checkpoint_id: Optional[str]


class UserFacingGraph:
    """
    Subgraph for coordinating user-facing agents
    
    Handles job seekers, career guidance, compliance questions,
    and technical role analysis with appropriate agent routing.
    """
    
    def __init__(self, enable_checkpoints: bool = False):
        """Initialize the user-facing agent graph with optional persistent checkpoints"""
        
        # Initialize specialized agents
        self.agents: Dict[str, FederalJobAgent] = {}
        self._initialize_agents()
        
        # Set up checkpointer if enabled
        self.checkpointer = None
        if enable_checkpoints:
            db_path = Path("checkpoints/user_facing.sqlite")
            db_path.parent.mkdir(exist_ok=True)
            conn = sqlite3.connect(str(db_path), check_same_thread=False)
            self.checkpointer = SqliteSaver(conn)
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
        
        logger.info("User-facing subgraph initialized with %d agents", len(self.agents))
    
    def _initialize_agents(self):
        """Initialize all user-facing agents"""
        
        # Role analysis agents
        try:
            self.agents["data_scientist"] = DataScientist(AgentConfig(
                role="data_scientist", 
                user_id="system",
                model="gptFREE"
            ))
            
            self.agents["statistician"] = Statistician(AgentConfig(
                role="statistician",
                user_id="system", 
                model="gptFREE"
            ))
            
            self.agents["database_admin"] = DatabaseAdmin(AgentConfig(
                role="database_admin",
                user_id="system",
                model="gptFREE"
            ))
            
            self.agents["devops_engineer"] = DevOpsEngineer(AgentConfig(
                role="devops_engineer",
                user_id="system",
                model="gptFREE"
            ))
            
            self.agents["it_specialist"] = ITSpecialist(AgentConfig(
                role="it_specialist",
                user_id="system",
                model="gptFREE"
            ))
            
        except Exception as e:
            logger.warning(f"Could not initialize role agents: {e}")
        
        # Compliance agents
        try:
            self.agents["essay_guidance"] = EssayGuidanceAgent(AgentConfig(
                role="essay_guidance",
                user_id="system",
                model="gptFREE"
            ))
            
            self.agents["resume_compression"] = ResumeCompressionAgent(AgentConfig(
                role="resume_compression", 
                user_id="system",
                model="gptFREE"
            ))
            
            self.agents["executive_order_research"] = ExecutiveOrderResearchAgent(AgentConfig(
                role="executive_order_research",
                user_id="system",
                model="gptFREE"
            ))
            
        except Exception as e:
            logger.warning(f"Could not initialize compliance agents: {e}")
        
        # Analytics agents
        try:
            self.agents["analytics_intelligence"] = AnalyticsIntelligence(AgentConfig(
                role="analytics_intelligence",
                user_id="system", 
                model="gptFREE"
            ))
            
            self.agents["job_collection_orchestrator"] = JobCollectionOrchestrator(AgentConfig(
                role="job_collection_orchestrator",
                user_id="system",
                model="gptFREE"
            ))
            
        except Exception as e:
            logger.warning(f"Could not initialize analytics agents: {e}")
            
        logger.info(f"Initialized {len(self.agents)} user-facing agents")
    
    def _create_workflow(self) -> StateGraph:
        """Create the user-facing workflow graph"""
        
        workflow = StateGraph(UserFacingState)
        
        # Add workflow nodes
        workflow.add_node("analyze_query", self._analyze_query)
        workflow.add_node("route_to_specialists", self._route_to_specialists)
        workflow.add_node("pre_essay_interrupt", self._pre_essay_interrupt)
        workflow.add_node("execute_parallel", self._execute_parallel)
        workflow.add_node("execute_sequential", self._execute_sequential)
        workflow.add_node("compliance_validation", self._compliance_validation)
        workflow.add_node("consolidate_results", self._consolidate_results)
        workflow.add_node("generate_recommendations", self._generate_recommendations)
        workflow.add_node("stream_progress", self._stream_progress)
        
        # Add parallel task coordination nodes
        workflow.add_node("parallel_role_analysis", self._parallel_role_analysis)
        workflow.add_node("sequential_compliance", self._sequential_compliance)
        
        # Define workflow edges
        workflow.add_edge(START, "analyze_query")
        workflow.add_edge("analyze_query", "route_to_specialists")
        
        # Conditional routing with essay interrupt
        workflow.add_conditional_edges(
            "route_to_specialists",
            self._determine_routing_path,
            {
                "essay_interrupt": "pre_essay_interrupt",
                "parallel": "execute_parallel", 
                "sequential": "execute_sequential",
                "role_analysis": "parallel_role_analysis",
                "compliance_flow": "sequential_compliance"
            }
        )
        
        # Essay interrupt handling
        workflow.add_edge("pre_essay_interrupt", "execute_sequential")
        workflow.add_edge("parallel_role_analysis", "compliance_validation")
        workflow.add_edge("sequential_compliance", "compliance_validation")
        
        workflow.add_edge("execute_parallel", "stream_progress")
        workflow.add_edge("execute_sequential", "stream_progress")
        workflow.add_edge("stream_progress", "compliance_validation")
        workflow.add_edge("compliance_validation", "consolidate_results")
        workflow.add_edge("consolidate_results", "generate_recommendations")
        workflow.add_edge("generate_recommendations", END)
        
        return workflow
    
    async def _analyze_query(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Analyze the user query to determine type and routing with streaming events"""
        
        # Initialize streaming and progress tracking
        state["current_phase"] = "analyzing_query"
        state["progress_percentage"] = 10.0
        state["events"] = state.get("events", [])
        state["streaming_enabled"] = True
        
        # Stream progress event
        self._add_streaming_event(state, "analysis_started", {
            "message": "Starting query analysis...",
            "progress": 10.0
        })
        
        query = state["original_query"].lower()
        
        # Determine query type
        if any(word in query for word in ["essay", "narrative", "ksa", "writing"]):
            state["query_type"] = UserQueryType.ESSAY_GUIDANCE
            state["requires_compliance_check"] = True
            
        elif any(word in query for word in ["resume", "cv", "experience", "qualifications"]):
            state["query_type"] = UserQueryType.RESUME_HELP
            
        elif any(word in query for word in ["data scientist", "1560", "analytics", "machine learning"]):
            state["query_type"] = UserQueryType.TECHNICAL_ROLE
            state["job_series"] = JobSeries.DATA_SCIENTIST
            
        elif any(word in query for word in ["statistician", "1530", "statistics", "statistical"]):
            state["query_type"] = UserQueryType.TECHNICAL_ROLE  
            state["job_series"] = JobSeries.STATISTICIAN
            
        elif any(word in query for word in ["database", "dba", "0334", "sql"]):
            state["query_type"] = UserQueryType.TECHNICAL_ROLE
            state["job_series"] = JobSeries.DATABASE_ADMIN
            
        elif any(word in query for word in ["devops", "0301", "deployment", "infrastructure"]):
            state["query_type"] = UserQueryType.TECHNICAL_ROLE
            state["job_series"] = JobSeries.DEVOPS
            
        elif any(word in query for word in ["it specialist", "2210", "cybersecurity", "technology"]):
            state["query_type"] = UserQueryType.TECHNICAL_ROLE
            state["job_series"] = JobSeries.IT_SPECIALIST
            
        elif any(word in query for word in ["market", "trends", "analysis", "research"]):
            state["query_type"] = UserQueryType.MARKET_RESEARCH
            
        elif any(word in query for word in ["compliance", "merit hiring", "regulation"]):
            state["query_type"] = UserQueryType.COMPLIANCE_CHECK
            state["requires_compliance_check"] = True
            
        else:
            state["query_type"] = UserQueryType.GENERAL_INQUIRY
        
        # Update progress and stream completion
        state["completed_phases"] = state.get("completed_phases", []) + ["analyze_query"]
        state["progress_percentage"] = 20.0
        
        self._add_streaming_event(state, "analysis_completed", {
            "query_type": state["query_type"].value,
            "job_series": state.get("job_series", {}).value if state.get("job_series") else None,
            "requires_compliance": state.get("requires_compliance_check", False),
            "progress": 20.0
        })
        
        logger.info(f"Query analyzed as {state['query_type'].value}")
        return state
    
    async def _route_to_specialists(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Route query to appropriate specialist agents with streaming"""
        
        state["current_phase"] = "routing_specialists"
        state["progress_percentage"] = 30.0
        
        self._add_streaming_event(state, "routing_started", {
            "message": "Routing to specialist agents...",
            "progress": 30.0
        })
        
        query_type = state["query_type"]
        job_series = state.get("job_series")
        
        # Determine primary and supporting agents
        if query_type == UserQueryType.TECHNICAL_ROLE:
            if job_series == JobSeries.DATA_SCIENTIST:
                state["primary_agents"] = ["data_scientist"]
                state["supporting_agents"] = ["statistician", "analytics_intelligence"]
                
            elif job_series == JobSeries.STATISTICIAN:
                state["primary_agents"] = ["statistician"]
                state["supporting_agents"] = ["data_scientist", "analytics_intelligence"]
                
            elif job_series == JobSeries.DATABASE_ADMIN:
                state["primary_agents"] = ["database_admin"]
                state["supporting_agents"] = ["devops_engineer", "it_specialist"]
                
            elif job_series == JobSeries.DEVOPS:
                state["primary_agents"] = ["devops_engineer"]
                state["supporting_agents"] = ["database_admin", "it_specialist"]
                
            elif job_series == JobSeries.IT_SPECIALIST:
                state["primary_agents"] = ["it_specialist"]
                state["supporting_agents"] = ["devops_engineer", "database_admin"]
                
        elif query_type == UserQueryType.ESSAY_GUIDANCE:
            state["primary_agents"] = ["essay_guidance"]
            state["supporting_agents"] = ["executive_order_research"]
            state["needs_human_review"] = True
            
        elif query_type == UserQueryType.RESUME_HELP:
            state["primary_agents"] = ["resume_compression"]
            state["supporting_agents"] = []
            
        elif query_type == UserQueryType.MARKET_RESEARCH:
            state["primary_agents"] = ["analytics_intelligence", "job_collection_orchestrator"]
            state["supporting_agents"] = []
            state["parallel_execution"] = True
            
        elif query_type == UserQueryType.COMPLIANCE_CHECK:
            state["primary_agents"] = ["executive_order_research", "essay_guidance"]
            state["supporting_agents"] = ["resume_compression"]
            state["needs_human_review"] = True
            
        else:
            # General inquiry - use analytics as default
            state["primary_agents"] = ["analytics_intelligence"]
            state["supporting_agents"] = []
        
        # Set parallel execution for multiple primary agents
        if len(state["primary_agents"]) > 1:
            state["parallel_execution"] = True
        
        # Update progress
        state["progress_percentage"] = 40.0
        state["completed_phases"] = state.get("completed_phases", []) + ["route_to_specialists"]
        
        self._add_streaming_event(state, "routing_completed", {
            "primary_agents": state["primary_agents"],
            "supporting_agents": state["supporting_agents"],
            "parallel_execution": state.get("parallel_execution", False),
            "progress": 40.0
        })
        
        logger.info(f"Routed to primary agents: {state['primary_agents']}")
        return state
    
    def _determine_routing_path(self, state: UserFacingState) -> str:
        """Determine routing path based on query type and job series"""
        
        query_type = state["query_type"]
        job_series = state.get("job_series")
        
        # Essay guidance requires interrupt
        if query_type == UserQueryType.ESSAY_GUIDANCE:
            state["interrupt_before_essay"] = True
            return "essay_interrupt"
        
        # Role analysis agents run in parallel
        if query_type == UserQueryType.TECHNICAL_ROLE and job_series:
            return "role_analysis"
        
        # Compliance checks run sequentially
        if query_type == UserQueryType.COMPLIANCE_CHECK:
            return "compliance_flow"
        
        # Default execution type
        if state.get("parallel_execution", False):
            return "parallel"
        else:
            return "sequential"
    
    async def _pre_essay_interrupt(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Dynamic interrupt before essay guidance to ensure human oversight"""
        
        state["current_phase"] = "essay_guidance_interrupt"
        state["needs_human_review"] = True
        
        # Log the interrupt requirement
        interrupt_message = (
            "ESSAY GUIDANCE REQUEST DETECTED: This query requires human oversight "
            "to ensure Merit Hiring compliance. The system will provide guidance only, "
            "not content generation."
        )
        
        state["warnings"] = state.get("warnings", []) + [interrupt_message]
        
        self._add_streaming_event(state, "essay_interrupt_triggered", {
            "message": interrupt_message,
            "requires_human_approval": True,
            "compliance_level": "critical"
        })
        
        logger.warning(f"Essay guidance interrupt triggered for session: {config.get('configurable', {}).get('thread_id') if config else 'unknown'}")
        return state
    
    async def _parallel_role_analysis(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Execute role analysis agents in parallel for technical positions"""
        
        state["current_phase"] = "parallel_role_analysis"
        state["progress_percentage"] = 50.0
        state["active_parallel_tasks"] = state["primary_agents"] + state["supporting_agents"]
        
        self._add_streaming_event(state, "parallel_analysis_started", {
            "agents": state["active_parallel_tasks"],
            "job_series": state.get("job_series", {}).value if state.get("job_series") else None,
            "progress": 50.0
        })
        
        query = state["original_query"]
        tasks = []
        
        # Create parallel tasks with progress tracking
        for agent_name in state["active_parallel_tasks"]:
            if agent_name in self.agents:
                task = self._execute_agent_with_progress(agent_name, query, {}, state)
                tasks.append((agent_name, task))
        
        # Execute in parallel with progress streaming
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        # Process results
        state["agent_results"] = {}
        state["agent_errors"] = {}
        
        for (agent_name, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                state["agent_errors"][agent_name] = str(result)
                logger.error(f"Agent {agent_name} failed: {result}")
                self._add_streaming_event(state, "agent_failed", {
                    "agent": agent_name,
                    "error": str(result)
                })
            else:
                state["agent_results"][agent_name] = result
                logger.info(f"Agent {agent_name} completed successfully")
                self._add_streaming_event(state, "agent_completed", {
                    "agent": agent_name,
                    "success": True
                })
        
        state["progress_percentage"] = 70.0
        state["completed_phases"] = state.get("completed_phases", []) + ["parallel_role_analysis"]
        
        return state
    
    async def _sequential_compliance(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Execute compliance checks sequentially with checkpoints"""
        
        state["current_phase"] = "sequential_compliance"
        state["progress_percentage"] = 50.0
        
        self._add_streaming_event(state, "compliance_flow_started", {
            "agents": state["primary_agents"],
            "requires_human_review": state.get("needs_human_review", False),
            "progress": 50.0
        })
        
        query = state["original_query"]
        context = {}
        
        state["agent_results"] = {}
        state["agent_errors"] = {}
        
        # Execute compliance agents sequentially with checkpoints
        for i, agent_name in enumerate(state["primary_agents"]):
            checkpoint_progress = 50.0 + (i * 15.0)
            
            try:
                self._add_streaming_event(state, "compliance_agent_starting", {
                    "agent": agent_name,
                    "step": i + 1,
                    "total_steps": len(state["primary_agents"]),
                    "progress": checkpoint_progress
                })
                
                result = await self._execute_agent(agent_name, query, context)
                state["agent_results"][agent_name] = result
                
                # Update context for next agent
                context["previous_result"] = result
                
                self._add_streaming_event(state, "compliance_checkpoint", {
                    "agent": agent_name,
                    "completed": True,
                    "checkpoint_id": f"compliance_{agent_name}_{datetime.utcnow().timestamp()}",
                    "progress": checkpoint_progress + 15.0
                })
                
            except Exception as e:
                state["agent_errors"][agent_name] = str(e)
                logger.error(f"Compliance agent {agent_name} failed: {e}")
                
                self._add_streaming_event(state, "compliance_error", {
                    "agent": agent_name,
                    "error": str(e),
                    "recovery_action": "continue_with_warnings"
                })
        
        state["progress_percentage"] = 70.0
        state["completed_phases"] = state.get("completed_phases", []) + ["sequential_compliance"]
        
        return state
    
    async def _execute_parallel(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Execute primary agents in parallel with streaming progress"""
        
        state["current_phase"] = "parallel_execution"
        state["progress_percentage"] = 50.0
        
        primary_agents = state["primary_agents"]
        supporting_agents = state["supporting_agents"]
        all_agents = primary_agents + supporting_agents
        state["active_parallel_tasks"] = all_agents
        
        query = state["original_query"]
        
        self._add_streaming_event(state, "parallel_execution_started", {
            "agents": all_agents,
            "progress": 50.0
        })
        
        # Execute all agents in parallel
        tasks = []
        for agent_name in all_agents:
            if agent_name in self.agents:
                task = self._execute_agent_with_progress(agent_name, query, {}, state)
                tasks.append((agent_name, task))
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        # Process results
        state["agent_results"] = {}
        state["agent_errors"] = {}
        
        for (agent_name, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                state["agent_errors"][agent_name] = str(result)
                logger.error(f"Agent {agent_name} failed: {result}")
            else:
                state["agent_results"][agent_name] = result
                logger.info(f"Agent {agent_name} completed successfully")
        
        state["progress_percentage"] = 70.0
        state["completed_phases"] = state.get("completed_phases", []) + ["execute_parallel"]
        
        return state
    
    async def _execute_sequential(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Execute agents sequentially with context passing and progress streaming"""
        
        state["current_phase"] = "sequential_execution"
        state["progress_percentage"] = 50.0
        
        primary_agents = state["primary_agents"]
        supporting_agents = state["supporting_agents"]
        
        query = state["original_query"]
        context = {}
        
        state["agent_results"] = {}
        state["agent_errors"] = {}
        
        self._add_streaming_event(state, "sequential_execution_started", {
            "primary_agents": primary_agents,
            "supporting_agents": supporting_agents,
            "progress": 50.0
        })
        
        # Execute primary agents first
        for i, agent_name in enumerate(primary_agents):
            progress = 50.0 + (i * 10.0)
            
            try:
                self._add_streaming_event(state, "agent_starting", {
                    "agent": agent_name,
                    "type": "primary",
                    "progress": progress
                })
                
                result = await self._execute_agent(agent_name, query, context)
                state["agent_results"][agent_name] = result
                
                # Update context for next agent
                context["previous_result"] = result
                
                self._add_streaming_event(state, "agent_completed", {
                    "agent": agent_name,
                    "type": "primary",
                    "success": True,
                    "progress": progress + 10.0
                })
                
            except Exception as e:
                state["agent_errors"][agent_name] = str(e)
                logger.error(f"Primary agent {agent_name} failed: {e}")
                self._add_streaming_event(state, "agent_failed", {
                    "agent": agent_name,
                    "type": "primary",
                    "error": str(e)
                })
        
        # Execute supporting agents with context from primary
        for i, agent_name in enumerate(supporting_agents):
            progress = 60.0 + (i * 5.0)
            
            try:
                self._add_streaming_event(state, "agent_starting", {
                    "agent": agent_name,
                    "type": "supporting",
                    "progress": progress
                })
                
                enriched_query = f"{query}\n\nContext from primary analysis: {context.get('previous_result', {})}"
                result = await self._execute_agent(agent_name, enriched_query, context)
                state["agent_results"][agent_name] = result
                
                self._add_streaming_event(state, "agent_completed", {
                    "agent": agent_name,
                    "type": "supporting",
                    "success": True,
                    "progress": progress + 5.0
                })
                
            except Exception as e:
                state["agent_errors"][agent_name] = str(e)
                logger.error(f"Supporting agent {agent_name} failed: {e}")
                self._add_streaming_event(state, "agent_failed", {
                    "agent": agent_name,
                    "type": "supporting",
                    "error": str(e)
                })
        
        state["progress_percentage"] = 70.0
        state["completed_phases"] = state.get("completed_phases", []) + ["execute_sequential"]
        
        return state
    
    async def _execute_agent(self, agent_name: str, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single agent"""
        
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found")
        
        result = await agent.process(query, context)
        
        return {
            "success": result.success,
            "message": result.message,
            "data": result.data,
            "metadata": result.metadata,
            "timestamp": result.timestamp.isoformat() if result.timestamp else None
        }
    
    async def _execute_agent_with_progress(self, agent_name: str, query: str, context: Dict[str, Any], state: UserFacingState) -> Dict[str, Any]:
        """Execute a single agent with progress streaming"""
        
        self._add_streaming_event(state, "agent_progress", {
            "agent": agent_name,
            "status": "starting",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        try:
            result = await self._execute_agent(agent_name, query, context)
            
            self._add_streaming_event(state, "agent_progress", {
                "agent": agent_name,
                "status": "completed",
                "success": result["success"],
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return result
        except Exception as e:
            self._add_streaming_event(state, "agent_progress", {
                "agent": agent_name,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
            raise
    
    async def _stream_progress(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Stream real-time progress updates"""
        
        state["current_phase"] = "streaming_progress"
        
        # Calculate overall progress
        total_phases = 6  # analyze, route, execute, validate, consolidate, recommend
        completed = len(state.get("completed_phases", []))
        progress = min(80.0, (completed / total_phases) * 80.0)  # Cap at 80% before final steps
        
        state["progress_percentage"] = progress
        
        # Stream comprehensive progress update
        progress_event = {
            "overall_progress": progress,
            "current_phase": state["current_phase"],
            "completed_phases": state.get("completed_phases", []),
            "active_agents": len(state.get("agent_results", {})),
            "failed_agents": len(state.get("agent_errors", {})),
            "warnings_count": len(state.get("warnings", [])),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self._add_streaming_event(state, "progress_update", progress_event)
        
        logger.info(f"Progress update: {progress:.1f}% - {state['current_phase']}")
        
        state["completed_phases"] = state.get("completed_phases", []) + ["stream_progress"]
        return state
    
    def _add_streaming_event(self, state: UserFacingState, event_type: str, event_data: Dict[str, Any]):
        """Add a streaming event to the state"""
        
        if not state.get("streaming_enabled", True):
            return
        
        event = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": event_data
        }
        
        events = state.get("events", [])
        events.append(event)
        state["events"] = events
        
        # Log important events
        if event_type in ["analysis_completed", "routing_completed", "agent_failed", "essay_interrupt_triggered"]:
            logger.info(f"Streaming event: {event_type} - {event_data}")
    
    async def _compliance_validation(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Validate results against compliance requirements with streaming"""
        
        state["current_phase"] = "compliance_validation"
        state["progress_percentage"] = 75.0
        state["warnings"] = state.get("warnings", [])
        
        self._add_streaming_event(state, "compliance_validation_started", {
            "message": "Validating compliance requirements...",
            "progress": 75.0
        })
        
        # Check if compliance validation is required
        if state.get("requires_compliance_check", False):
            
            # Check for essay-related violations
            agent_results = state.get("agent_results", {})
            
            for agent_name, result in agent_results.items():
                if agent_name == "essay_guidance":
                    # Validate essay guidance doesn't include content generation
                    response_text = str(result.get("data", {}).get("response", "")).lower()
                    
                    if any(phrase in response_text for phrase in [
                        "here is your essay", "here's your essay", 
                        "i wrote", "draft essay", "example essay"
                    ]):
                        state["warnings"].append("COMPLIANCE WARNING: Essay content generation detected")
                        state["needs_human_review"] = True
                    
                    # Check for word count violations  
                    if "200" in response_text and "word" in response_text:
                        if not any(phrase in response_text for phrase in [
                            "limit to 200", "maximum 200", "no more than 200"
                        ]):
                            state["warnings"].append("COMPLIANCE WARNING: 200-word limit not enforced")
        
        state["progress_percentage"] = 80.0
        state["completed_phases"] = state.get("completed_phases", []) + ["compliance_validation"]
        
        self._add_streaming_event(state, "compliance_validation_completed", {
            "warnings_count": len(state["warnings"]),
            "violations_found": len([w for w in state["warnings"] if "COMPLIANCE WARNING" in w]),
            "human_review_required": state.get("needs_human_review", False),
            "progress": 80.0
        })
        
        logger.info(f"Compliance validation completed with {len(state['warnings'])} warnings")
        return state
    
    async def _consolidate_results(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Consolidate results from multiple agents into coherent response"""
        
        state["current_phase"] = "consolidating_results"
        state["progress_percentage"] = 85.0
        
        self._add_streaming_event(state, "consolidation_started", {
            "message": "Consolidating agent results...",
            "agent_count": len(state.get("agent_results", {})),
            "progress": 85.0
        })
        
        agent_results = state.get("agent_results", {})
        primary_agents = state["primary_agents"]
        
        # Start with primary agent results
        response_parts = []
        sources = []
        
        for agent_name in primary_agents:
            if agent_name in agent_results:
                result = agent_results[agent_name]
                if result.get("success") and result.get("data"):
                    response_parts.append(f"**{agent_name.replace('_', ' ').title()} Analysis:**\n{result.get('message', '')}")
                    sources.append(agent_name)
        
        # Add supporting agent insights
        supporting_agents = state["supporting_agents"]
        for agent_name in supporting_agents:
            if agent_name in agent_results:
                result = agent_results[agent_name]
                if result.get("success") and result.get("data"):
                    response_parts.append(f"**Additional Insights from {agent_name.replace('_', ' ').title()}:**\n{result.get('message', '')}")
                    sources.append(agent_name)
        
        if not response_parts:
            response_parts = ["No successful agent responses were received for your query."]
        
        state["consolidated_response"] = "\n\n".join(response_parts)
        state["sources_used"] = sources
        
        # Calculate confidence score based on successful agents
        total_agents = len(primary_agents) + len(supporting_agents)
        successful_agents = len([r for r in agent_results.values() if r.get("success")])
        state["confidence_score"] = successful_agents / total_agents if total_agents > 0 else 0.0
        
        state["progress_percentage"] = 90.0
        state["completed_phases"] = state.get("completed_phases", []) + ["consolidate_results"]
        
        self._add_streaming_event(state, "consolidation_completed", {
            "response_length": len(state["consolidated_response"]),
            "sources_count": len(state["sources_used"]),
            "confidence_score": state["confidence_score"],
            "progress": 90.0
        })
        
        return state
    
    async def _generate_recommendations(self, state: UserFacingState, config: RunnableConfig = None) -> UserFacingState:
        """Generate actionable recommendations and next steps with final streaming"""
        
        state["current_phase"] = "generating_recommendations"
        state["progress_percentage"] = 95.0
        
        self._add_streaming_event(state, "recommendations_started", {
            "message": "Generating recommendations and next steps...",
            "query_type": state["query_type"].value,
            "progress": 95.0
        })
        
        query_type = state["query_type"]
        job_series = state.get("job_series")
        
        recommendations = []
        next_steps = []
        
        if query_type == UserQueryType.TECHNICAL_ROLE:
            recommendations.extend([
                "Review the specific qualifications and requirements for your target job series",
                "Align your experience with federal competency frameworks",
                "Consider obtaining relevant certifications or training"
            ])
            
            if job_series:
                next_steps.extend([
                    f"Search USAJobs for {job_series.value} positions",
                    "Review sample job announcements for required skills",
                    "Prepare targeted application materials"
                ])
        
        elif query_type == UserQueryType.ESSAY_GUIDANCE:
            recommendations.extend([
                "Follow STAR method (Situation, Task, Action, Result) for narrative responses",
                "Keep within 200-word limits as specified",
                "Focus on specific examples from your experience"
            ])
            
            next_steps.extend([
                "Draft your narrative responses independently",
                "Review for compliance with Merit Hiring requirements",
                "Have responses reviewed by a qualified federal HR professional"
            ])
            
            # Add compliance reminder
            if state.get("needs_human_review"):
                state["warnings"].append("IMPORTANT: All essay content must be your own work per Merit Hiring regulations")
        
        elif query_type == UserQueryType.MARKET_RESEARCH:
            recommendations.extend([
                "Focus on agencies that align with your career goals",
                "Monitor job announcement patterns and timing",
                "Research agency-specific requirements and culture"
            ])
            
            next_steps.extend([
                "Set up USAJobs saved searches for relevant positions",
                "Research target agencies' mission and values",
                "Network with current federal employees in your field"
            ])
        
        else:
            # General recommendations
            recommendations.extend([
                "Clarify your federal career objectives",
                "Research relevant job series and qualification requirements",
                "Prepare comprehensive application materials"
            ])
            
            next_steps.extend([
                "Explore USAJobs and identify positions of interest",
                "Review qualification requirements for target roles",
                "Consider speaking with a federal career counselor"
            ])
        
        state["actionable_recommendations"] = recommendations
        state["next_steps"] = next_steps
        state["progress_percentage"] = 100.0
        state["completed_phases"] = state.get("completed_phases", []) + ["generate_recommendations"]
        
        # Final streaming event
        self._add_streaming_event(state, "workflow_completed", {
            "total_recommendations": len(recommendations),
            "total_next_steps": len(next_steps),
            "confidence_score": state.get("confidence_score", 0.0),
            "human_review_required": state.get("needs_human_review", False),
            "warnings_count": len(state.get("warnings", [])),
            "progress": 100.0,
            "final_status": "completed"
        })
        
        return state
    
    async def process_user_query(
        self, 
        query: str, 
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user query through the user-facing workflow
        
        Args:
            query: User's question or request
            user_profile: Optional user profile information
            
        Returns:
            Processed response with recommendations
        """
        
        start_time = datetime.utcnow()
        
        initial_state = UserFacingState(
            original_query=query,
            query_type=UserQueryType.GENERAL_INQUIRY,
            job_series=None,
            user_profile=user_profile or {},
            primary_agents=[],
            supporting_agents=[],
            agent_results={},
            agent_errors={},
            parallel_execution=False,
            requires_compliance_check=False,
            needs_human_review=False,
            consolidated_response="",
            actionable_recommendations=[],
            next_steps=[],
            warnings=[],
            processing_time=0.0,
            confidence_score=0.0,
            sources_used=[]
        )
        
        try:
            # Execute the workflow
            compiled_workflow = self.workflow.compile()
            final_state = await compiled_workflow.ainvoke(initial_state)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            final_state["processing_time"] = processing_time
            
            return {
                "success": True,
                "response": final_state["consolidated_response"],
                "recommendations": final_state["actionable_recommendations"],
                "next_steps": final_state["next_steps"],
                "warnings": final_state["warnings"],
                "metadata": {
                    "query_type": final_state["query_type"].value,
                    "job_series": final_state.get("job_series", {}).value if final_state.get("job_series") else None,
                    "agents_used": final_state["sources_used"],
                    "confidence_score": final_state["confidence_score"],
                    "processing_time": processing_time,
                    "needs_human_review": final_state.get("needs_human_review", False)
                }
            }
            
        except Exception as e:
            logger.error(f"User-facing workflow failed: {e}")
            return {
                "success": False,
                "response": f"An error occurred processing your query: {str(e)}",
                "recommendations": [],
                "next_steps": [],
                "warnings": ["System error occurred during processing"],
                "streaming_events": [],
                "metadata": {
                    "error": str(e),
                    "processing_time": (datetime.utcnow() - start_time).total_seconds(),
                    "thread_id": config.configurable.get("thread_id") if config else None,
                    "streaming_enabled": enable_streaming,
                    "final_status": "error"
                }
            }
    
    async def get_streaming_events(self, config: RunnableConfig) -> List[Dict[str, Any]]:
        """Get streaming events for a specific session"""
        
        if not self.checkpointer:
            return []
        
        try:
            state = await self.workflow.compile(checkpointer=self.checkpointer).aget_state(config)
            if state and state.values:
                return state.values.get("events", [])
            return []
        except Exception as e:
            logger.error(f"Error retrieving streaming events: {e}")
            return []
    
    async def resume_from_checkpoint(self, config: RunnableConfig, user_input: Optional[str] = None) -> Dict[str, Any]:
        """Resume execution from a checkpoint (e.g., after human approval)"""
        
        if not self.checkpointer:
            raise ValueError("Checkpointer not enabled")
        
        try:
            compiled_workflow = self.workflow.compile(checkpointer=self.checkpointer)
            
            # Resume with optional user input
            update_data = {"human_input": user_input} if user_input else None
            
            final_state = None
            async for event in compiled_workflow.astream(update_data, config):
                final_state = event
            
            return {
                "success": True,
                "resumed": True,
                "response": final_state["consolidated_response"],
                "recommendations": final_state["actionable_recommendations"],
                "next_steps": final_state["next_steps"],
                "warnings": final_state["warnings"],
                "streaming_events": final_state.get("events", []),
                "metadata": {
                    "thread_id": config.configurable.get("thread_id"),
                    "checkpoint_resumed": True,
                    "human_input_provided": user_input is not None
                }
            }
            
        except Exception as e:
            logger.error(f"Error resuming from checkpoint: {e}")
            return {
                "success": False,
                "error": str(e),
                "streaming_events": []
            }


# Export the main class
__all__ = ["UserFacingGraph", "UserQueryType", "JobSeries", "UserFacingState"]
"""
Federal Job Advisor LangGraph Orchestrator

This module provides the main orchestrator for the Fed Job Advisor system using LangGraph.
It coordinates both user-facing applications and platform development workflows.
"""

from typing import Dict, Any, List, Optional, TypedDict, Union, Annotated
from datetime import datetime
import asyncio
import json
import logging
from enum import Enum
from dataclasses import dataclass

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.base import Checkpoint
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import Tool
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field
import sqlite3
from pathlib import Path

# Import existing agents
from agents.app.agents.base import FederalJobAgent, AgentConfig, AgentResponse
from agents.app.agents.roles.agent_router import AgentRouter

# Import subgraphs
from agents.app.orchestrator.subgraphs import UserFacingGraph, PlatformDevelopmentGraph
from agents.app.orchestrator.subgraphs import UserQueryType, DevelopmentPhase, FeatureType

# Import compliance gates
from agents.app.orchestrator.compliance import get_compliance_gates, ComplianceLevel, ViolationType

# Import debugging tools
from agents.app.orchestrator.debugging import (
    TimeTravel, DebugLevel, CheckpointEvent, 
    create_time_travel_debugger, debug_session
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowType(Enum):
    """Types of workflows the orchestrator can handle"""
    USER_QUERY = "user_query"
    PLATFORM_DEVELOPMENT = "platform_development" 
    DATA_COLLECTION = "data_collection"
    MERIT_COMPLIANCE = "merit_compliance"
    JOB_MATCHING = "job_matching"
    SYSTEM_MAINTENANCE = "system_maintenance"


class Priority(Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TaskDefinition:
    """Definition of a task to be executed"""
    task_id: str
    workflow_type: WorkflowType
    description: str
    priority: Priority
    required_agents: List[str]
    parallel_execution: bool = False
    dependencies: List[str] = None
    context: Dict[str, Any] = None


class ApplicationState(TypedDict):
    """
    Enhanced main state object that flows through the LangGraph workflow
    Contains all information needed for processing tasks with streaming and debugging
    """
    # User/Request Information
    user_id: str
    session_id: str
    request_type: str
    original_query: str
    
    # Workflow Control
    workflow_type: WorkflowType
    current_step: str
    completed_steps: List[str]
    pending_tasks: List[TaskDefinition]
    
    # Agent Coordination
    active_agents: List[str]
    agent_results: Dict[str, Any]
    agent_errors: Dict[str, str]
    
    # Context & Memory
    conversation_history: List[BaseMessage]
    project_context: Dict[str, Any]
    user_preferences: Dict[str, Any]
    
    # Compliance & Validation
    compliance_checks: Dict[str, bool]
    validation_results: Dict[str, Any]
    warnings: List[str]
    compliance_violations: List[Dict[str, Any]]
    human_approvals_needed: List[str]
    dynamic_interrupts_triggered: List[str]
    
    # Subgraph Results
    user_facing_result: Optional[Dict[str, Any]]
    platform_development_result: Optional[Dict[str, Any]]
    
    # Streaming & Progress
    streaming_events: List[Dict[str, Any]]
    progress_percentage: float
    real_time_monitoring: bool
    
    # Debugging & Checkpoints
    debug_mode: bool
    checkpoint_id: Optional[str]
    debug_session_id: Optional[str]
    performance_metrics: Dict[str, Any]
    
    # Results
    final_response: str
    response_data: Dict[str, Any]
    metadata: Dict[str, Any]
    
    # Control Flags
    require_human_review: bool
    parallel_execution: bool
    error_recovery: bool


class FedJobOrchestrator:
    """
    Main LangGraph orchestrator for the Fed Job Advisor system
    
    Coordinates multiple agents to handle:
    - User queries about federal jobs
    - Platform development tasks
    - Data collection and processing
    - Merit hiring compliance
    - System maintenance
    """
    
    def __init__(self, enable_time_travel: bool = False, debug_level: DebugLevel = DebugLevel.STANDARD):
        """Initialize the enhanced orchestrator with all necessary components"""
        
        # Initialize checkpointer (SQLite for persistence if time travel enabled)
        if enable_time_travel:
            db_path = Path("checkpoints/orchestrator.sqlite")
            db_path.parent.mkdir(exist_ok=True)
            conn = sqlite3.connect(str(db_path), check_same_thread=False)
            self.checkpointer = SqliteSaver(conn)
        else:
            self.checkpointer = MemorySaver()
        
        # Initialize time travel debugging
        self.time_travel_enabled = enable_time_travel
        self.debug_level = debug_level
        self.time_travel = None
        if enable_time_travel:
            self.time_travel = create_time_travel_debugger(debug_level=debug_level)
        
        # Initialize the agent registry
        self.agents: Dict[str, FederalJobAgent] = {}
        
        # Initialize enhanced subgraphs
        self.user_facing_graph = UserFacingGraph(enable_checkpoints=enable_time_travel)
        self.platform_development_graph = PlatformDevelopmentGraph(enable_checkpoints=enable_time_travel)
        
        # Initialize enhanced compliance gates with streaming
        self.compliance_gates = get_compliance_gates(
            enable_streaming=True,
            enable_dynamic_interrupts=True
        )
        
        # Load configuration and initialize agents
        self._initialize_agents()
        
        # Create the main workflow graph
        self.workflow = self._create_workflow()
        
        # Compile the graph with checkpoints
        self.app = self.workflow.compile(checkpointer=self.checkpointer)
        
        logger.info(f"Fed Job Orchestrator initialized (time_travel={enable_time_travel}, debug_level={debug_level.value})")
    
    def _initialize_agents(self):
        """Initialize all required agents for the system"""
        
        # Core system agents
        self.agent_router = AgentRouter(AgentConfig(
            role="agent_router",
            user_id="system",
            model="gptFREE"
        ))
        
        # Register the router in our agent registry
        self.agents["router"] = self.agent_router
        
        logger.info(f"Initialized {len(self.agents)} agents")
    
    def _create_workflow(self) -> StateGraph:
        """Create the main LangGraph workflow with subgraphs and compliance gates"""
        
        # Create the state graph
        workflow = StateGraph(ApplicationState)
        
        # Add enhanced workflow nodes
        workflow.add_node("initialize_request", self._initialize_request)
        workflow.add_node("create_debug_checkpoint", self._create_debug_checkpoint)
        workflow.add_node("route_task", self._route_task)
        workflow.add_node("real_time_compliance_check", self._real_time_compliance_check)
        workflow.add_node("compliance_gate_initial", self._compliance_gate_initial)
        workflow.add_node("execute_user_subgraph", self._execute_user_subgraph)
        workflow.add_node("execute_platform_subgraph", self._execute_platform_subgraph)
        workflow.add_node("stream_progress", self._stream_progress)
        workflow.add_node("compliance_gate_results", self._compliance_gate_results)
        workflow.add_node("dynamic_interrupt_handler", self._dynamic_interrupt_handler)
        workflow.add_node("human_review_checkpoint", self._human_review_checkpoint)
        workflow.add_node("finalize_response", self._finalize_response)
        workflow.add_node("handle_error", self._handle_error)
        
        # Define enhanced workflow edges
        workflow.add_edge(START, "initialize_request")
        
        # Debug checkpoint creation if enabled
        workflow.add_conditional_edges(
            "initialize_request",
            self._should_create_debug_checkpoint,
            {
                "create_checkpoint": "create_debug_checkpoint",
                "skip_checkpoint": "route_task"
            }
        )
        
        workflow.add_edge("create_debug_checkpoint", "route_task")
        workflow.add_edge("route_task", "real_time_compliance_check")
        
        # Real-time compliance with dynamic interrupts
        workflow.add_conditional_edges(
            "real_time_compliance_check",
            self._determine_compliance_action,
            {
                "proceed": "compliance_gate_initial",
                "interrupt": "dynamic_interrupt_handler",
                "blocked": "handle_error"
            }
        )
        
        workflow.add_edge("dynamic_interrupt_handler", "compliance_gate_initial")
        
        # Conditional routing after initial compliance check
        workflow.add_conditional_edges(
            "compliance_gate_initial",
            self._determine_workflow_path,
            {
                "user_workflow": "execute_user_subgraph",
                "platform_workflow": "execute_platform_subgraph",
                "blocked": "handle_error"
            }
        )
        
        # Both subgraphs flow to progress streaming
        workflow.add_edge("execute_user_subgraph", "stream_progress")
        workflow.add_edge("execute_platform_subgraph", "stream_progress")
        workflow.add_edge("stream_progress", "compliance_gate_results")
        
        # Conditional routing after results compliance check
        workflow.add_conditional_edges(
            "compliance_gate_results", 
            self._determine_post_results_action,
            {
                "human_review": "human_review_checkpoint",
                "finalize": "finalize_response",
                "blocked": "handle_error"
            }
        )
        
        # Human review can either approve or block
        workflow.add_conditional_edges(
            "human_review_checkpoint",
            self._determine_human_review_result,
            {
                "approved": "finalize_response",
                "blocked": "handle_error"
            }
        )
        
        workflow.add_edge("finalize_response", END)
        workflow.add_edge("handle_error", END)
        
        return workflow
    
    async def _initialize_request(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Initialize the request and set up the enhanced workflow state"""
        
        logger.info(f"Initializing request: {state.get('original_query', 'No query')}")
        
        # Set enhanced initial workflow state
        state["current_step"] = "initializing"
        state["completed_steps"] = []
        state["pending_tasks"] = []
        state["active_agents"] = []
        state["agent_results"] = {}
        state["agent_errors"] = {}
        state["compliance_checks"] = {}
        state["validation_results"] = {}
        state["warnings"] = []
        state["compliance_violations"] = []
        state["human_approvals_needed"] = []
        state["dynamic_interrupts_triggered"] = []
        state["user_facing_result"] = None
        state["platform_development_result"] = None
        state["streaming_events"] = []
        state["progress_percentage"] = 0.0
        state["real_time_monitoring"] = True
        state["debug_mode"] = self.time_travel_enabled
        state["checkpoint_id"] = None
        state["debug_session_id"] = None
        state["performance_metrics"] = {
            "start_time": datetime.utcnow().timestamp(),
            "agent_execution_times": {},
            "phase_durations": {}
        }
        state["require_human_review"] = False
        state["parallel_execution"] = False
        state["error_recovery"] = False
        
        # Initialize conversation history if not present
        if "conversation_history" not in state:
            state["conversation_history"] = []
        
        # Add user message to history
        if state.get("original_query"):
            state["conversation_history"].append(
                HumanMessage(content=state["original_query"])
            )
        
        # Set metadata
        state["metadata"] = {
            "started_at": datetime.utcnow().isoformat(),
            "orchestrator_version": "1.0.0",
            "session_id": state.get("session_id", f"session_{datetime.utcnow().timestamp()}")
        }
        
        # Add streaming event for initialization
        self._add_streaming_event(state, "workflow_initialized", {
            "message": "Workflow initialization completed",
            "user_id": state.get("user_id"),
            "session_id": state.get("session_id"),
            "debug_mode": state["debug_mode"],
            "progress": 5.0
        })
        
        state["progress_percentage"] = 5.0
        state["completed_steps"].append("initialize_request")
        return state
    
    def _should_create_debug_checkpoint(self, state: ApplicationState) -> str:
        """Determine if a debug checkpoint should be created"""
        
        if state.get("debug_mode", False) and self.time_travel_enabled:
            return "create_checkpoint"
        return "skip_checkpoint"
    
    async def _create_debug_checkpoint(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Create a debug checkpoint for time travel debugging"""
        
        if not self.time_travel or not config:
            return state
        
        try:
            thread_id = config.configurable.get("thread_id", state.get("session_id", "unknown"))
            
            checkpoint_id = await self.time_travel.create_checkpoint(
                thread_id=thread_id,
                state=dict(state),
                event_type=CheckpointEvent.WORKFLOW_START,
                workflow_type=state.get("workflow_type", WorkflowType.USER_QUERY).value,
                phase="initialization",
                debug_notes="Initial workflow checkpoint",
                performance_metrics=state.get("performance_metrics", {})
            )
            
            state["checkpoint_id"] = checkpoint_id
            
            self._add_streaming_event(state, "debug_checkpoint_created", {
                "checkpoint_id": checkpoint_id,
                "thread_id": thread_id,
                "message": "Debug checkpoint created for workflow start"
            })
            
            logger.info(f"Created debug checkpoint: {checkpoint_id}")
            
        except Exception as e:
            logger.error(f"Failed to create debug checkpoint: {e}")
            state["warnings"].append(f"Debug checkpoint creation failed: {str(e)}")
        
        return state
    
    async def _real_time_compliance_check(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Real-time compliance check with dynamic interrupts"""
        
        state["current_step"] = "real_time_compliance"
        state["progress_percentage"] = 10.0
        
        self._add_streaming_event(state, "real_time_compliance_started", {
            "message": "Starting real-time compliance monitoring...",
            "progress": 10.0
        })
        
        query = state.get("original_query", "")
        
        try:
            # Run real-time compliance check
            compliance_result = await self.compliance_gates.real_time_compliance_check(
                content=query,
                context={
                    "user_id": state.get("user_id"),
                    "session_id": state.get("session_id"),
                    "workflow_type": state.get("workflow_type", WorkflowType.USER_QUERY).value
                }
            )
            
            # Store results
            state["compliance_checks"]["real_time_passed"] = compliance_result.passed
            state["compliance_checks"]["dynamic_interrupt"] = compliance_result.dynamic_interrupt_triggered
            
            if compliance_result.dynamic_interrupt_triggered:
                state["dynamic_interrupts_triggered"].append("REAL_TIME_COMPLIANCE_VIOLATION")
                
                self._add_streaming_event(state, "dynamic_interrupt_triggered", {
                    "violation_count": len(compliance_result.violations),
                    "critical_violations": len([v for v in compliance_result.violations if v.level.value == "critical"]),
                    "message": "Dynamic interrupt triggered due to compliance violations"
                })
            
            # Add violations to state
            state["compliance_violations"].extend([
                {
                    "type": v.violation_type.value,
                    "level": v.level.value,
                    "message": v.message,
                    "timestamp": v.timestamp.isoformat(),
                    "action_blocked": v.action_blocked
                }
                for v in compliance_result.violations
            ])
            
            # Add streaming events from compliance check
            if compliance_result.streaming_events:
                state["streaming_events"].extend(compliance_result.streaming_events)
            
            logger.info(f"Real-time compliance check completed: violations={len(compliance_result.violations)}")
            
        except Exception as e:
            logger.error(f"Real-time compliance check failed: {e}")
            state["warnings"].append(f"Real-time compliance check error: {str(e)}")
            state["compliance_checks"]["real_time_passed"] = True  # Allow to proceed on error
        
        state["progress_percentage"] = 15.0
        state["completed_steps"].append("real_time_compliance_check")
        return state
    
    def _determine_compliance_action(self, state: ApplicationState) -> str:
        """Determine action based on real-time compliance results"""
        
        compliance_checks = state.get("compliance_checks", {})
        
        # Check for dynamic interrupt
        if compliance_checks.get("dynamic_interrupt", False):
            return "interrupt"
        
        # Check if real-time compliance passed
        if not compliance_checks.get("real_time_passed", True):
            return "blocked"
        
        return "proceed"
    
    async def _dynamic_interrupt_handler(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Handle dynamic interrupts triggered by compliance violations"""
        
        state["current_step"] = "dynamic_interrupt_handler"
        
        interrupts = state.get("dynamic_interrupts_triggered", [])
        violations = state.get("compliance_violations", [])
        
        # Log interrupt details
        interrupt_message = (
            f"DYNAMIC INTERRUPT TRIGGERED: {len(interrupts)} interrupts detected. "
            f"Critical compliance violations require immediate attention. "
            f"Review violations: {[v['type'] for v in violations if v.get('level') == 'critical']}"
        )
        
        state["warnings"].append(interrupt_message)
        state["require_human_review"] = True
        
        self._add_streaming_event(state, "interrupt_handled", {
            "interrupt_count": len(interrupts),
            "violation_count": len(violations),
            "message": "Dynamic interrupts processed, proceeding with human review requirement",
            "human_review_required": True
        })
        
        logger.warning(f"Handled {len(interrupts)} dynamic interrupts")
        
        state["completed_steps"].append("dynamic_interrupt_handler")
        return state
    
    async def _stream_progress(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Stream progress updates for real-time monitoring"""
        
        state["current_step"] = "streaming_progress"
        
        # Calculate progress based on completed steps
        total_expected_steps = 8  # Approximate number of major steps
        completed_steps = len(state.get("completed_steps", []))
        progress = min(80.0, (completed_steps / total_expected_steps) * 80.0)  # Cap at 80%
        
        state["progress_percentage"] = progress
        
        # Stream comprehensive progress update
        progress_event = {
            "overall_progress": progress,
            "current_step": state["current_step"],
            "completed_steps": state.get("completed_steps", []),
            "active_agents": len(state.get("agent_results", {})),
            "failed_agents": len(state.get("agent_errors", {})),
            "warnings_count": len(state.get("warnings", [])),
            "compliance_violations": len(state.get("compliance_violations", [])),
            "human_review_required": state.get("require_human_review", False),
            "debug_mode": state.get("debug_mode", False),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self._add_streaming_event(state, "progress_update", progress_event)
        
        # Create performance checkpoint if in debug mode
        if state.get("debug_mode", False) and self.time_travel_enabled:
            try:
                thread_id = config.configurable.get("thread_id") if config else state.get("session_id")
                if thread_id:
                    await self.time_travel.create_checkpoint(
                        thread_id=thread_id,
                        state=dict(state),
                        event_type=CheckpointEvent.PHASE_COMPLETE,
                        workflow_type=state.get("workflow_type", WorkflowType.USER_QUERY).value,
                        phase="progress_streaming",
                        debug_notes=f"Progress: {progress:.1f}%",
                        performance_metrics=state.get("performance_metrics", {})
                    )
            except Exception as e:
                logger.error(f"Failed to create progress checkpoint: {e}")
        
        logger.info(f"Progress streamed: {progress:.1f}% - {state['current_step']}")
        
        state["completed_steps"].append("stream_progress")
        return state
    
    def _add_streaming_event(self, state: ApplicationState, event_type: str, event_data: Dict[str, Any]):
        """Add a streaming event to the state"""
        
        event = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": event_data,
            "source": "orchestrator"
        }
        
        events = state.get("streaming_events", [])
        events.append(event)
        state["streaming_events"] = events
        
        # Log important events
        if event_type in ["workflow_initialized", "debug_checkpoint_created", "dynamic_interrupt_triggered", "interrupt_handled"]:
            logger.info(f"Orchestrator streaming event: {event_type} - {event_data}")
    
    async def _route_task(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Enhanced route task to determine workflow type and required agents"""
        
        logger.info("Routing task to appropriate workflow")
        
        state["current_step"] = "routing_task"
        state["progress_percentage"] = 20.0
        
        query = state.get("original_query", "")
        
        try:
            # Use agent router to analyze the task
            routing_result = await self.agent_router.process(
                f"Route this task: {query}",
                context={"user_id": state.get("user_id")}
            )
            
            if routing_result.success:
                routing_data = routing_result.data.get("response", "{}")
                
                # Try to parse routing response
                try:
                    if isinstance(routing_data, str) and routing_data.startswith('{'):
                        routing_info = json.loads(routing_data)
                    else:
                        routing_info = {"description": routing_data}
                except json.JSONDecodeError:
                    routing_info = {"description": routing_data}
                
                # Determine workflow type based on content
                workflow_type = self._determine_workflow_type(query)
                state["workflow_type"] = workflow_type
                
                # Store routing information
                state["project_context"] = {
                    "routing_info": routing_info,
                    "workflow_type": workflow_type.value,
                    "query_analysis": query.lower()
                }
                
                logger.info(f"Task routed to workflow: {workflow_type.value}")
                
            else:
                logger.warning(f"Agent router failed: {routing_result.message}")
                state["workflow_type"] = WorkflowType.USER_QUERY
                state["warnings"].append("Routing failed, using default workflow")
        
        except Exception as e:
            logger.error(f"Error in task routing: {str(e)}")
            state["workflow_type"] = WorkflowType.USER_QUERY
            state["warnings"].append(f"Routing error: {str(e)}")
        
        # Add streaming event for routing completion
        self._add_streaming_event(state, "task_routed", {
            "workflow_type": workflow_type.value,
            "routing_success": True,
            "progress": 20.0
        })
        
        state["completed_steps"].append("route_task")
        return state
    
    def _determine_workflow_type(self, query: str) -> WorkflowType:
        """Determine the appropriate workflow type based on the query"""
        
        query_lower = query.lower()
        
        # Platform development keywords
        if any(word in query_lower for word in ["implement", "create", "build", "develop", "code", "feature"]):
            return WorkflowType.PLATFORM_DEVELOPMENT
            
        # Data collection keywords
        elif any(word in query_lower for word in ["collect", "data", "api", "usajobs", "database"]):
            return WorkflowType.DATA_COLLECTION
            
        # Merit hiring keywords
        elif any(word in query_lower for word in ["merit", "essay", "compliance", "hiring"]):
            return WorkflowType.MERIT_COMPLIANCE
            
        # Job matching keywords
        elif any(word in query_lower for word in ["job", "search", "match", "find", "career"]):
            return WorkflowType.JOB_MATCHING
            
        # System maintenance keywords
        elif any(word in query_lower for word in ["fix", "debug", "optimize", "monitor", "maintenance"]):
            return WorkflowType.SYSTEM_MAINTENANCE
            
        # Default to user query
        else:
            return WorkflowType.USER_QUERY
    
    async def _compliance_gate_initial(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Enhanced initial compliance gate check with streaming"""
        
        logger.info("Running initial compliance gate")
        
        state["current_step"] = "compliance_gate_initial"
        state["progress_percentage"] = 25.0
        query = state.get("original_query", "")
        
        try:
            self._add_streaming_event(state, "initial_compliance_started", {
                "message": "Running comprehensive compliance checks...",
                "query_length": len(query),
                "progress": 25.0
            })
            
            # Run enhanced comprehensive compliance check
            compliance_result = await self.compliance_gates.comprehensive_compliance_check(
                query=query,
                response="",  # No response yet
                context={
                    "user_id": state.get("user_id"),
                    "session_id": state.get("session_id"),
                    "workflow_type": state.get("workflow_type", WorkflowType.USER_QUERY).value
                },
                enable_real_time_monitoring=True
            )
            
            # Store compliance results
            state["compliance_checks"] = {
                "initial_gate_passed": compliance_result.passed,
                "action_allowed": compliance_result.action_allowed,
                "human_review_required": compliance_result.human_review_required
            }
            
            # Store violations
            state["compliance_violations"] = [
                {
                    "type": v.violation_type.value,
                    "level": v.level.value,
                    "message": v.message,
                    "timestamp": v.timestamp.isoformat(),
                    "action_blocked": v.action_blocked
                }
                for v in compliance_result.violations
            ]
            
            # Store warnings
            state["warnings"].extend(compliance_result.warnings)
            
            # Check for critical violations
            critical_violations = [v for v in compliance_result.violations if v.level == ComplianceLevel.CRITICAL]
            if critical_violations:
                state["require_human_review"] = True
                state["human_approvals_needed"].extend([
                    f"CRITICAL_VIOLATION_{v.violation_type.value.upper()}" 
                    for v in critical_violations
                ])
            
            # Add streaming events from compliance check
            if hasattr(compliance_result, 'streaming_events') and compliance_result.streaming_events:
                state["streaming_events"].extend(compliance_result.streaming_events)
            
            self._add_streaming_event(state, "initial_compliance_completed", {
                "passed": compliance_result.passed,
                "violations_count": len(compliance_result.violations),
                "warnings_count": len(compliance_result.warnings),
                "action_allowed": compliance_result.action_allowed,
                "progress": 30.0
            })
            
            logger.info(f"Initial compliance gate completed: passed={compliance_result.passed}, violations={len(compliance_result.violations)}")
            
        except Exception as e:
            logger.error(f"Initial compliance gate error: {str(e)}")
            state["warnings"].append(f"Compliance gate error: {str(e)}")
            state["compliance_checks"] = {"initial_gate_passed": False, "action_allowed": False}
        
        state["progress_percentage"] = 30.0
        state["completed_steps"].append("compliance_gate_initial")
        return state
    
    def _determine_workflow_path(self, state: ApplicationState) -> str:
        """Determine which workflow path to take after initial compliance gate"""
        
        # Check compliance gate results
        compliance_checks = state.get("compliance_checks", {})
        
        # Block if action not allowed
        if not compliance_checks.get("action_allowed", False):
            return "blocked"
        
        # Route based on workflow type
        workflow_type = state.get("workflow_type", WorkflowType.USER_QUERY)
        
        if workflow_type == WorkflowType.PLATFORM_DEVELOPMENT:
            return "platform_workflow"
        else:
            return "user_workflow"
    
    async def _execute_user_subgraph(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Execute enhanced user-facing subgraph with streaming"""
        
        logger.info("Executing user-facing subgraph")
        
        state["current_step"] = "executing_user_subgraph"
        state["progress_percentage"] = 40.0
        query = state.get("original_query", "")
        user_profile = state.get("user_preferences", {})
        
        try:
            self._add_streaming_event(state, "user_subgraph_started", {
                "message": "Starting user-facing workflow...",
                "query_length": len(query),
                "progress": 40.0
            })
            
            # Execute enhanced user-facing subgraph with streaming
            result = await self.user_facing_graph.process_user_query(
                query=query,
                user_profile=user_profile,
                config=config,
                enable_streaming=True
            )
            
            state["user_facing_result"] = result
            
            # Add streaming events from subgraph
            if "streaming_events" in result:
                state["streaming_events"].extend(result["streaming_events"])
            
            if result["success"]:
                logger.info("User-facing subgraph completed successfully")
                self._add_streaming_event(state, "user_subgraph_completed", {
                    "success": True,
                    "recommendations_count": len(result.get("recommendations", [])),
                    "confidence_score": result.get("metadata", {}).get("confidence_score", 0.0),
                    "progress": 60.0
                })
            else:
                state["warnings"].append("User-facing subgraph encountered issues")
                self._add_streaming_event(state, "user_subgraph_warning", {
                    "success": False,
                    "warnings": result.get("warnings", [])
                })
                
        except Exception as e:
            logger.error(f"User-facing subgraph failed: {e}")
            state["user_facing_result"] = {
                "success": False,
                "response": f"User workflow error: {str(e)}",
                "warnings": [f"Subgraph execution error: {str(e)}"]
            }
        
        state["completed_steps"].append("execute_user_subgraph")
        return state
    
    async def _execute_platform_subgraph(self, state: ApplicationState, config: RunnableConfig = None) -> ApplicationState:
        """Execute enhanced platform development subgraph with checkpoints"""
        
        logger.info("Executing platform development subgraph")
        
        state["current_step"] = "executing_platform_subgraph"
        state["progress_percentage"] = 40.0
        query = state.get("original_query", "")
        
        try:
            # Extract project info from query or context
            project_name = state.get("project_context", {}).get("project_name", "Fed Job Advisor Feature")
            
            self._add_streaming_event(state, "platform_subgraph_started", {
                "message": "Starting platform development workflow...",
                "project_name": project_name,
                "feature_request": query[:100] + "..." if len(query) > 100 else query,
                "progress": 40.0
            })
            
            # Execute enhanced platform development subgraph
            result = await self.platform_development_graph.develop_feature(
                project_name=project_name,
                feature_request=query,
                config=config,
                enable_streaming=True
            )
            
            state["platform_development_result"] = result
            
            # Add streaming events from subgraph
            if "streaming_events" in result:
                state["streaming_events"].extend(result["streaming_events"])
            
            # Add human approvals if needed
            if result.get("human_approvals_needed"):
                state["human_approvals_needed"].extend(result["human_approvals_needed"])
                state["require_human_review"] = True
            
            # Add cost monitoring alerts
            if "cost_analysis" in result:
                cost_analysis = result["cost_analysis"]
                if cost_analysis.get("budget_exceeded", False):
                    state["warnings"].extend(cost_analysis.get("cost_alerts", []))
                    state["require_human_review"] = True
            
            if result["success"]:
                logger.info("Platform development subgraph completed successfully")
                self._add_streaming_event(state, "platform_subgraph_completed", {
                    "success": True,
                    "completed_phases": result.get("completed_phases", []),
                    "cost_analysis": result.get("cost_analysis", {}),
                    "progress": 60.0
                })
            else:
                state["warnings"].append("Platform development subgraph encountered issues")
                self._add_streaming_event(state, "platform_subgraph_warning", {
                    "success": False,
                    "errors": result.get("errors", []),
                    "status": result.get("status", "unknown")
                })
                
        except Exception as e:
            logger.error(f"Platform development subgraph failed: {e}")
            state["platform_development_result"] = {
                "success": False,
                "status": "error",
                "errors": [f"Subgraph execution error: {str(e)}"],
                "warnings": [],
                "next_actions": ["Review system logs and retry"]
            }
        
        state["completed_steps"].append("execute_platform_subgraph")
        return state
    
    async def _compliance_gate_results(self, state: ApplicationState) -> ApplicationState:
        """Compliance gate check on results before finalization"""
        
        logger.info("Running compliance gate on results")
        
        state["current_step"] = "compliance_gate_results"
        query = state.get("original_query", "")
        
        # Get response from subgraph results
        user_result = state.get("user_facing_result", {})
        platform_result = state.get("platform_development_result", {})
        
        response = ""
        if user_result:
            response += user_result.get("response", "")
        if platform_result:
            response += f"\n{platform_result.get('status', '')}: {platform_result.get('next_actions', [])}"
        
        try:
            # Run compliance check on results
            compliance_result = self.compliance_gates.comprehensive_compliance_check(
                query=query,
                response=response,
                context={
                    "user_id": state.get("user_id"),
                    "session_id": state.get("session_id"),
                    "subgraph_results": {
                        "user_facing": user_result,
                        "platform_development": platform_result
                    }
                }
            )
            
            # Update compliance checks
            state["compliance_checks"].update({
                "results_gate_passed": compliance_result.passed,
                "final_action_allowed": compliance_result.action_allowed,
                "final_human_review_required": compliance_result.human_review_required
            })
            
            # Add any new violations
            new_violations = [
                {
                    "type": v.violation_type.value,
                    "level": v.level.value,
                    "message": v.message,
                    "timestamp": v.timestamp.isoformat(),
                    "action_blocked": v.action_blocked
                }
                for v in compliance_result.violations
            ]
            state["compliance_violations"].extend(new_violations)
            
            # Add warnings
            state["warnings"].extend(compliance_result.warnings)
            
            # Check for human review requirements
            if compliance_result.human_review_required:
                state["require_human_review"] = True
            
            logger.info(f"Results compliance gate completed: passed={compliance_result.passed}, new_violations={len(compliance_result.violations)}")
            
        except Exception as e:
            logger.error(f"Results compliance gate error: {str(e)}")
            state["warnings"].append(f"Results compliance gate error: {str(e)}")
            state["compliance_checks"]["results_gate_passed"] = False
        
        state["completed_steps"].append("compliance_gate_results")
        return state
    
    def _determine_post_results_action(self, state: ApplicationState) -> str:
        """Determine action after results compliance gate"""
        
        compliance_checks = state.get("compliance_checks", {})
        
        # Block if final action not allowed
        if not compliance_checks.get("final_action_allowed", True):
            return "blocked"
        
        # Require human review if needed
        if state.get("require_human_review", False) or compliance_checks.get("final_human_review_required", False):
            return "human_review"
        
        # Otherwise proceed to finalize
        return "finalize"
    
    async def _human_review_checkpoint(self, state: ApplicationState) -> ApplicationState:
        """Human review checkpoint for sensitive operations"""
        
        logger.info("Requiring human review checkpoint")
        
        state["current_step"] = "human_review_checkpoint"
        
        # Prepare review summary
        violations = state.get("compliance_violations", [])
        warnings = state.get("warnings", [])
        approvals_needed = state.get("human_approvals_needed", [])
        
        review_summary = {
            "session_id": state.get("session_id"),
            "original_query": state.get("original_query"),
            "violations_count": len(violations),
            "warnings_count": len(warnings),
            "approvals_needed": approvals_needed,
            "critical_violations": [
                v for v in violations 
                if v.get("level") == "critical"
            ],
            "high_priority_violations": [
                v for v in violations
                if v.get("level") == "high"
            ]
        }
        
        # Log the review requirement
        logger.warning(f"HUMAN REVIEW REQUIRED: {review_summary}")
        
        # In a real implementation, this would pause execution and wait for human approval
        # For now, we'll add a clear indication that human review is needed
        state["metadata"]["human_review_required"] = True
        state["metadata"]["review_summary"] = review_summary
        state["warnings"].append("CRITICAL: This operation requires human review before proceeding")
        
        # For this implementation, we'll assume human review is required but not block
        # In production, this should integrate with a human approval system
        
        state["completed_steps"].append("human_review_checkpoint")
        return state
    
    def _determine_human_review_result(self, state: ApplicationState) -> str:
        """Determine result of human review (placeholder for actual implementation)"""
        
        # In a real implementation, this would check the status of human approval
        # For now, we'll proceed but with clear warnings
        
        critical_violations = [
            v for v in state.get("compliance_violations", [])
            if v.get("level") == "critical"
        ]
        
        # Block if there are critical violations
        if critical_violations:
            logger.error("Critical violations detected - blocking execution")
            return "blocked"
        
        # Otherwise approve with warnings
        logger.warning("Human review checkpoint passed with warnings")
        return "approved"
    
    
    
    async def _finalize_response(self, state: ApplicationState) -> ApplicationState:
        """Finalize the response and prepare for return"""
        
        logger.info("Finalizing response")
        
        state["current_step"] = "finalizing_response"
        
        # Compile results from all agents
        agent_results = state.get("agent_results", {})
        
        # Create comprehensive response
        response_parts = []
        response_data = {}
        
        for agent_name, result in agent_results.items():
            if result.get("success") and result.get("data"):
                response_parts.append(f"[{agent_name}]: {result.get('message', 'Completed successfully')}")
                if result.get("data"):
                    response_data[agent_name] = result["data"]
        
        # Handle case with no successful results
        if not response_parts:
            response_parts = ["No successful agent responses received"]
        
        state["final_response"] = "\n\n".join(response_parts)
        state["response_data"] = response_data
        
        # Add warnings to response
        warnings = state.get("warnings", [])
        if warnings:
            state["final_response"] += f"\n\n⚠️ Warnings:\n" + "\n".join(f"- {w}" for w in warnings)
        
        # Update metadata
        state["metadata"].update({
            "completed_at": datetime.utcnow().isoformat(),
            "total_agents": len(state.get("active_agents", [])),
            "successful_agents": len(agent_results),
            "workflow_type": state.get("workflow_type", WorkflowType.USER_QUERY).value,
            "final_status": "success"
        })
        
        # Add AI message to conversation history
        state["conversation_history"].append(
            AIMessage(content=state["final_response"])
        )
        
        state["completed_steps"].append("finalize_response")
        logger.info("Response finalization completed")
        
        return state
    
    async def _handle_error(self, state: ApplicationState) -> ApplicationState:
        """Handle errors and provide error response"""
        
        logger.error("Handling workflow error")
        
        state["current_step"] = "handling_error"
        
        # Collect error information
        agent_errors = state.get("agent_errors", {})
        warnings = state.get("warnings", [])
        
        error_message = "An error occurred during processing:\n"
        
        if agent_errors:
            error_message += "\nAgent Errors:\n"
            for agent, error in agent_errors.items():
                error_message += f"- {agent}: {error}\n"
        
        if warnings:
            error_message += "\nWarnings:\n"
            for warning in warnings:
                error_message += f"- {warning}\n"
        
        state["final_response"] = error_message
        state["metadata"]["final_status"] = "error"
        
        # Add error message to conversation history
        state["conversation_history"].append(
            AIMessage(content=error_message)
        )
        
        state["completed_steps"].append("handle_error")
        return state
    
    async def process_request(
        self,
        user_id: str,
        query: str,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        enable_streaming: bool = True,
        debug_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Enhanced main entry point for processing requests with streaming and debugging
        
        Args:
            user_id: ID of the user making the request
            query: The user's query or task description
            session_id: Optional session ID for conversation continuity
            context: Additional context for the request
            enable_streaming: Whether to enable real-time streaming events
            debug_mode: Whether to enable debug mode with time travel
        
        Returns:
            Dictionary containing the response, metadata, and streaming events
        """
        
        if not session_id:
            session_id = f"session_{user_id}_{datetime.utcnow().timestamp()}"
        
        # Create enhanced initial state
        initial_state = ApplicationState(
            user_id=user_id,
            session_id=session_id,
            request_type="user_query",
            original_query=query,
            workflow_type=WorkflowType.USER_QUERY,
            current_step="starting",
            completed_steps=[],
            pending_tasks=[],
            active_agents=[],
            agent_results={},
            agent_errors={},
            conversation_history=[],
            project_context=context or {},
            user_preferences={},
            compliance_checks={},
            validation_results={},
            warnings=[],
            compliance_violations=[],
            human_approvals_needed=[],
            dynamic_interrupts_triggered=[],
            user_facing_result=None,
            platform_development_result=None,
            streaming_events=[],
            progress_percentage=0.0,
            real_time_monitoring=True,
            debug_mode=debug_mode or self.time_travel_enabled,
            checkpoint_id=None,
            debug_session_id=None,
            performance_metrics={
                "request_start": datetime.utcnow().timestamp(),
                "agent_execution_times": {},
                "phase_durations": {}
            },
            final_response="",
            response_data={},
            metadata={},
            require_human_review=False,
            parallel_execution=False,
            error_recovery=False
        )
        
        try:
            # Create debug session if in debug mode
            config = RunnableConfig(
                configurable={"thread_id": session_id}
            )
            
            if debug_mode and self.time_travel_enabled:
                debug_session_id = await self.time_travel.create_debug_session(
                    thread_id=session_id,
                    breakpoints=["compliance_violations", "human_review", "errors"],
                    session_notes=f"Debug session for query: {query[:100]}"
                )
                initial_state["debug_session_id"] = debug_session_id
            
            # Execute the enhanced workflow
            if enable_streaming:
                final_state = None
                async for event in self.app.astream(initial_state, config):
                    final_state = event
                    # In production, these events could be yielded for real-time UI updates
                    if "streaming_events" in event and event["streaming_events"]:
                        logger.debug(f"Streaming event: {event['streaming_events'][-1]}")
            else:
                final_state = await self.app.ainvoke(initial_state, config)
            
            # Calculate final performance metrics
            if final_state and "performance_metrics" in final_state:
                final_state["performance_metrics"]["request_end"] = datetime.utcnow().timestamp()
                final_state["performance_metrics"]["total_duration"] = (
                    final_state["performance_metrics"]["request_end"] - 
                    final_state["performance_metrics"]["request_start"]
                )
            
            # Return the enhanced results
            return {
                "success": final_state["metadata"].get("final_status") == "success",
                "response": final_state["final_response"],
                "data": final_state["response_data"],
                "metadata": final_state["metadata"],
                "warnings": final_state["warnings"],
                "compliance_violations": final_state.get("compliance_violations", []),
                "streaming_events": final_state.get("streaming_events", []) if enable_streaming else [],
                "human_approvals_needed": final_state.get("human_approvals_needed", []),
                "dynamic_interrupts": final_state.get("dynamic_interrupts_triggered", []),
                "progress_percentage": final_state.get("progress_percentage", 100.0),
                "debug_info": {
                    "debug_mode": debug_mode,
                    "checkpoint_id": final_state.get("checkpoint_id"),
                    "debug_session_id": final_state.get("debug_session_id"),
                    "performance_metrics": final_state.get("performance_metrics", {})
                } if debug_mode else None,
                "session_id": session_id
            }
        
        except Exception as e:
            logger.error(f"Enhanced orchestrator execution failed: {e}")
            
            # Create error checkpoint if in debug mode
            if debug_mode and self.time_travel_enabled:
                try:
                    await self.time_travel.create_checkpoint(
                        thread_id=session_id,
                        state=dict(initial_state),
                        event_type=CheckpointEvent.ERROR_OCCURRED,
                        workflow_type=initial_state.get("workflow_type", WorkflowType.USER_QUERY).value,
                        phase="error_occurred",
                        debug_notes=f"System error: {str(e)}",
                        performance_metrics={"error_timestamp": datetime.utcnow().timestamp()}
                    )
                except Exception as checkpoint_error:
                    logger.error(f"Failed to create error checkpoint: {checkpoint_error}")
            
            return {
                "success": False,
                "response": f"System error: {str(e)}",
                "data": {},
                "metadata": {"error": str(e), "final_status": "system_error"},
                "warnings": ["System error occurred"],
                "compliance_violations": [],
                "streaming_events": [],
                "human_approvals_needed": [],
                "dynamic_interrupts": [],
                "progress_percentage": 0.0,
                "debug_info": {
                    "debug_mode": debug_mode,
                    "error_occurred": True,
                    "error_message": str(e)
                } if debug_mode else None,
                "session_id": session_id
            }
    
    async def get_session_history(self, session_id: str, include_streaming_events: bool = True) -> Dict[str, Any]:
        """Get enhanced conversation history and streaming events for a session"""
        
        try:
            # Get state from checkpointer
            config = RunnableConfig(
                configurable={"thread_id": session_id}
            )
            state = await self.app.aget_state(config)
            
            if state and state.values:
                history = state.values.get("conversation_history", [])
                conversation_history = [
                    {
                        "type": msg.type,
                        "content": msg.content,
                        "timestamp": getattr(msg, "timestamp", None)
                    }
                    for msg in history
                ]
                
                result = {
                    "session_id": session_id,
                    "conversation_history": conversation_history,
                    "current_progress": state.values.get("progress_percentage", 0.0),
                    "current_step": state.values.get("current_step", "unknown"),
                    "warnings": state.values.get("warnings", []),
                    "human_approvals_needed": state.values.get("human_approvals_needed", [])
                }
                
                if include_streaming_events:
                    result["streaming_events"] = state.values.get("streaming_events", [])
                    result["compliance_violations"] = state.values.get("compliance_violations", [])
                    result["dynamic_interrupts"] = state.values.get("dynamic_interrupts_triggered", [])
                
                return result
            
            return {
                "session_id": session_id,
                "conversation_history": [],
                "streaming_events": [],
                "message": "No session data found"
            }
        
        except Exception as e:
            logger.error(f"Error retrieving enhanced session history: {e}")
            return {
                "session_id": session_id,
                "error": str(e),
                "conversation_history": [],
                "streaming_events": []
            }
    
    async def get_real_time_status(self, session_id: str) -> Dict[str, Any]:
        """Get real-time status of a workflow session"""
        
        try:
            config = RunnableConfig(
                configurable={"thread_id": session_id}
            )
            state = await self.app.aget_state(config)
            
            if state and state.values:
                return {
                    "session_id": session_id,
                    "current_step": state.values.get("current_step", "unknown"),
                    "progress_percentage": state.values.get("progress_percentage", 0.0),
                    "completed_steps": state.values.get("completed_steps", []),
                    "active_agents": len(state.values.get("agent_results", {})),
                    "warnings_count": len(state.values.get("warnings", [])),
                    "compliance_violations_count": len(state.values.get("compliance_violations", [])),
                    "human_review_required": state.values.get("require_human_review", False),
                    "debug_mode": state.values.get("debug_mode", False),
                    "last_update": datetime.utcnow().isoformat(),
                    "streaming_events_count": len(state.values.get("streaming_events", []))
                }
            
            return {
                "session_id": session_id,
                "status": "not_found",
                "message": "No active session found"
            }
            
        except Exception as e:
            logger.error(f"Error getting real-time status: {e}")
            return {
                "session_id": session_id,
                "status": "error",
                "error": str(e)
            }
    
    async def replay_from_checkpoint(self, session_id: str, checkpoint_id: str) -> Dict[str, Any]:
        """Replay workflow from a specific checkpoint using time travel debugging"""
        
        if not self.time_travel_enabled or not self.time_travel:
            return {
                "success": False,
                "error": "Time travel debugging not enabled",
                "session_id": session_id
            }
        
        try:
            result = await self.time_travel.replay_from_checkpoint(
                checkpoint_id=checkpoint_id,
                debug_mode=True
            )
            
            return {
                "success": result["replay_successful"],
                "session_id": session_id,
                "checkpoint_id": checkpoint_id,
                "replay_data": result,
                "message": "Checkpoint replay completed"
            }
            
        except Exception as e:
            logger.error(f"Checkpoint replay failed: {e}")
            return {
                "success": False,
                "session_id": session_id,
                "checkpoint_id": checkpoint_id,
                "error": str(e)
            }


# Create singleton instance with enhanced features
_orchestrator_instance = None

def get_orchestrator(enable_time_travel: bool = False, debug_level: DebugLevel = DebugLevel.STANDARD) -> FedJobOrchestrator:
    """Get or create the global orchestrator instance with enhanced capabilities"""
    global _orchestrator_instance
    
    if _orchestrator_instance is None:
        _orchestrator_instance = FedJobOrchestrator(
            enable_time_travel=enable_time_travel,
            debug_level=debug_level
        )
    
    return _orchestrator_instance


# Export main classes and functions
__all__ = [
    "FedJobOrchestrator",
    "ApplicationState", 
    "WorkflowType",
    "Priority",
    "TaskDefinition",
    "get_orchestrator"
]
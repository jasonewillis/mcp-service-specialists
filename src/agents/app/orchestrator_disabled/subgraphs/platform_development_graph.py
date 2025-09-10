"""
Platform Development Subgraph for Fed Job Advisor

Organizes platform development agents:
- Feature Developer Agent
- Payment Integration Agent  
- Security & Authentication Agent
- Monitoring & Analytics Agent

Implements sequential workflows for feature implementation with testing and deployment steps.
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
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

# Import platform agents
from ...agents.base import FederalJobAgent, AgentConfig, AgentResponse
from ...agents.platform.feature_developer import FeatureDeveloperAgent
from ...agents.platform.payment_integration_agent import PaymentIntegrationAgent  
from ...agents.platform.security_authentication_agent import SecurityAuthenticationAgent
from ...agents.platform.monitoring_analytics_agent import MonitoringAnalyticsAgent

logger = logging.getLogger(__name__)


class DevelopmentPhase(Enum):
    """Phases of platform development"""
    PLANNING = "planning"
    DESIGN = "design" 
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    MAINTENANCE = "maintenance"


class FeatureType(Enum):
    """Types of features that can be developed"""
    CORE_FUNCTIONALITY = "core_functionality"
    USER_INTERFACE = "user_interface"
    DATA_PROCESSING = "data_processing"
    INTEGRATION = "integration"
    SECURITY = "security"
    PAYMENT = "payment"
    ANALYTICS = "analytics"
    PERFORMANCE = "performance"


class DeploymentEnvironment(Enum):
    """Target deployment environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class PlatformDevelopmentState(TypedDict):
    """State for platform development workflow with checkpoints and cost monitoring"""
    # Project Information
    project_name: str
    feature_request: str
    feature_type: FeatureType
    current_phase: DevelopmentPhase
    target_environment: DeploymentEnvironment
    
    # Requirements & Planning
    requirements: Dict[str, Any]
    technical_specifications: Dict[str, Any]
    architecture_design: Dict[str, Any]
    security_requirements: Dict[str, Any]
    
    # Development Control
    assigned_agents: List[str]
    completed_phases: List[DevelopmentPhase]
    current_deliverables: Dict[str, Any]
    phase_results: Dict[str, Any]
    phase_checkpoints: Dict[str, str]  # phase -> checkpoint_id
    
    # Quality & Testing
    test_results: Dict[str, Any]
    security_audit_results: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    
    # Deployment & Operations
    deployment_plan: Dict[str, Any]
    monitoring_setup: Dict[str, Any]
    rollback_plan: Dict[str, Any]
    
    # Compliance & Budget
    budget_constraints: Dict[str, Any]
    current_costs: Dict[str, float]
    cost_alerts: List[str]
    budget_exceeded: bool
    compliance_checkpoints: Dict[str, bool]
    human_approvals_needed: List[str]
    human_approval_status: Dict[str, str]  # approval_id -> status
    
    # Progress & Events
    progress_percentage: float
    streaming_events: List[Dict[str, Any]]
    
    # Results
    implementation_status: str
    next_actions: List[str]
    warnings: List[str]
    errors: List[str]
    
    # Metadata
    started_at: datetime
    estimated_completion: Optional[datetime]
    actual_completion: Optional[datetime]
    checkpoint_id: Optional[str]


class PlatformDevelopmentGraph:
    """
    Subgraph for coordinating platform development agents
    
    Handles feature implementation, payment integration, security,
    and monitoring with sequential workflows and proper checkpoints.
    """
    
    def __init__(self, enable_checkpoints: bool = True):
        """Initialize the platform development graph with checkpoints and cost monitoring"""
        
        # Initialize platform agents
        self.agents: Dict[str, FederalJobAgent] = {}
        self._initialize_agents()
        
        # Set up checkpointer for recovery
        self.checkpointer = None
        if enable_checkpoints:
            db_path = Path("checkpoints/platform_development.sqlite")
            db_path.parent.mkdir(exist_ok=True)
            conn = sqlite3.connect(str(db_path), check_same_thread=False)
            self.checkpointer = SqliteSaver(conn)
        
        # Budget monitoring thresholds
        self.cost_thresholds = {
            "tool_subscriptions": 100.0,  # $100/month
            "infrastructure": 50.0,       # $50/month
            "apis": 25.0,                 # $25/month
            "total_monthly": 175.0        # Total monthly limit
        }
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
        
        logger.info("Platform development subgraph initialized with %d agents", len(self.agents))
    
    def _initialize_agents(self):
        """Initialize all platform development agents"""
        
        try:
            self.agents["feature_developer"] = FeatureDeveloperAgent(AgentConfig(
                role="feature_developer",
                user_id="system", 
                model="gptFREE"
            ))
            
            self.agents["payment_integration"] = PaymentIntegrationAgent(AgentConfig(
                role="payment_integration",
                user_id="system",
                model="gptFREE"
            ))
            
            self.agents["security_authentication"] = SecurityAuthenticationAgent(AgentConfig(
                role="security_authentication", 
                user_id="system",
                model="gptFREE"
            ))
            
            self.agents["monitoring_analytics"] = MonitoringAnalyticsAgent(AgentConfig(
                role="monitoring_analytics",
                user_id="system",
                model="gptFREE"
            ))
            
        except Exception as e:
            logger.warning(f"Could not initialize platform agents: {e}")
            
        logger.info(f"Initialized {len(self.agents)} platform development agents")
    
    def _create_workflow(self) -> StateGraph:
        """Create the platform development workflow graph"""
        
        workflow = StateGraph(PlatformDevelopmentState)
        
        # Add workflow nodes for each development phase
        workflow.add_node("validate_request", self._validate_request)
        workflow.add_node("cost_monitoring_check", self._cost_monitoring_check)
        workflow.add_node("planning_phase", self._planning_phase)
        workflow.add_node("planning_checkpoint", self._create_phase_checkpoint)
        workflow.add_node("design_phase", self._design_phase)
        workflow.add_node("design_checkpoint", self._create_phase_checkpoint)
        workflow.add_node("implementation_phase", self._implementation_phase)
        workflow.add_node("implementation_checkpoint", self._create_phase_checkpoint)
        workflow.add_node("testing_phase", self._testing_phase)
        workflow.add_node("testing_checkpoint", self._create_phase_checkpoint)
        workflow.add_node("security_review", self._security_review)
        workflow.add_node("deployment_phase", self._deployment_phase)
        workflow.add_node("deployment_checkpoint", self._create_phase_checkpoint)
        workflow.add_node("monitoring_setup", self._monitoring_setup)
        workflow.add_node("human_approval_gate", self._human_approval_gate)
        workflow.add_node("final_validation", self._final_validation)
        workflow.add_node("handle_errors", self._handle_errors)
        workflow.add_node("handle_budget_exceeded", self._handle_budget_exceeded)
        
        # Define sequential workflow edges with checkpoints and cost monitoring
        workflow.add_edge(START, "validate_request")
        
        # Conditional routing after validation
        workflow.add_conditional_edges(
            "validate_request",
            self._check_validation_result,
            {
                "proceed": "cost_monitoring_check",
                "error": "handle_errors"
            }
        )
        
        # Cost monitoring before each major phase
        workflow.add_conditional_edges(
            "cost_monitoring_check",
            self._check_budget_status,
            {
                "proceed": "planning_phase",
                "budget_exceeded": "handle_budget_exceeded",
                "needs_approval": "human_approval_gate"
            }
        )
        
        # Sequential phases with checkpoints
        workflow.add_edge("planning_phase", "planning_checkpoint")
        workflow.add_edge("planning_checkpoint", "design_phase")
        workflow.add_edge("design_phase", "design_checkpoint")
        workflow.add_edge("design_checkpoint", "implementation_phase")
        workflow.add_edge("implementation_phase", "implementation_checkpoint")
        workflow.add_edge("implementation_checkpoint", "testing_phase")
        workflow.add_edge("testing_phase", "testing_checkpoint")
        workflow.add_edge("testing_checkpoint", "security_review")
        
        # Conditional routing after security review
        workflow.add_conditional_edges(
            "security_review",
            self._check_security_results,
            {
                "approved": "deployment_phase",
                "needs_fixes": "implementation_phase",
                "rejected": "handle_errors",
                "needs_human_approval": "human_approval_gate"
            }
        )
        
        workflow.add_edge("deployment_phase", "deployment_checkpoint")
        workflow.add_edge("deployment_checkpoint", "monitoring_setup")
        workflow.add_edge("monitoring_setup", "human_approval_gate")
        workflow.add_edge("human_approval_gate", "final_validation")
        workflow.add_edge("final_validation", END)
        workflow.add_edge("handle_errors", END)
        workflow.add_edge("handle_budget_exceeded", END)
        
        return workflow
    
    async def _validate_request(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Validate the development request and check constraints"""
        
        logger.info("Validating development request")
        
        state["current_phase"] = DevelopmentPhase.PLANNING
        state["progress_percentage"] = 5.0
        state["warnings"] = []
        state["errors"] = []
        state["human_approvals_needed"] = []
        state["human_approval_status"] = {}
        state["streaming_events"] = []
        state["phase_checkpoints"] = {}
        state["current_costs"] = {"tools": 0.0, "infrastructure": 0.0, "apis": 0.0}
        state["cost_alerts"] = []
        state["budget_exceeded"] = False
        
        self._add_streaming_event(state, "validation_started", {
            "message": "Validating development request...",
            "progress": 5.0
        })
        
        # Validate budget constraints (should be $0 for external development)
        budget_constraints = {
            "external_development_budget": 0,
            "tool_subscriptions_budget": 100,  # Max $100/month
            "infrastructure_budget": 50,      # Max $50/month  
            "api_costs_budget": 25            # Max $25/month
        }
        state["budget_constraints"] = budget_constraints
        
        # Check feature type for complexity warnings
        feature_request = state["feature_request"].lower()
        
        if any(word in feature_request for word in ["ai", "machine learning", "ml", "chatbot"]):
            state["warnings"].append("AI features require careful compliance review")
            state["human_approvals_needed"].append("AI_FEATURE_APPROVAL")
        
        if any(word in feature_request for word in ["payment", "billing", "subscription", "money"]):
            state["feature_type"] = FeatureType.PAYMENT
            state["human_approvals_needed"].append("PAYMENT_FEATURE_APPROVAL")
        
        if any(word in feature_request for word in ["security", "authentication", "auth", "login"]):
            state["feature_type"] = FeatureType.SECURITY
            state["human_approvals_needed"].append("SECURITY_FEATURE_APPROVAL")
        
        # Validate solo developer constraints
        complexity_keywords = ["microservices", "distributed", "kubernetes", "enterprise"]
        if any(word in feature_request for word in complexity_keywords):
            state["warnings"].append("Complex architecture may exceed solo developer capacity")
            state["warnings"].append("Consider simpler implementation approach")
        
        # Set realistic timeline expectations (solo part-time development)
        state["estimated_completion"] = datetime.utcnow().replace(
            month=datetime.utcnow().month + 3  # 3-month estimate for features
        )
        
        state["progress_percentage"] = 10.0
        
        self._add_streaming_event(state, "validation_completed", {
            "warnings_count": len(state["warnings"]),
            "approvals_needed": len(state["human_approvals_needed"]),
            "feature_type": state.get("feature_type", FeatureType.CORE_FUNCTIONALITY).value,
            "progress": 10.0
        })
        
        logger.info(f"Request validation completed with {len(state['warnings'])} warnings")
        return state
    
    def _check_validation_result(self, state: PlatformDevelopmentState) -> str:
        """Check if validation passed or failed"""
        
        errors = state.get("errors", [])
        if errors:
            return "error"
        
        # Always proceed but with warnings
        return "proceed"
    
    async def _cost_monitoring_check(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Monitor costs and check budget constraints before proceeding"""
        
        state["progress_percentage"] = 12.0
        
        self._add_streaming_event(state, "cost_monitoring_started", {
            "message": "Checking budget constraints and cost projections...",
            "progress": 12.0
        })
        
        # Analyze feature request for cost implications
        feature_request = state["feature_request"].lower()
        current_costs = state["current_costs"]
        
        # Estimate costs based on feature type
        if "payment" in feature_request or "stripe" in feature_request:
            current_costs["tools"] += 29.0  # Stripe fees estimated
            state["human_approvals_needed"].append("PAYMENT_FEATURE_COST_APPROVAL")
            
        if "ai" in feature_request or "llm" in feature_request or "gpt" in feature_request:
            current_costs["apis"] += 50.0  # AI API costs
            state["human_approvals_needed"].append("AI_API_COST_APPROVAL")
            
        if "database" in feature_request or "postgres" in feature_request:
            current_costs["infrastructure"] += 20.0  # Database scaling
            
        if "monitoring" in feature_request or "analytics" in feature_request:
            current_costs["tools"] += 15.0  # Monitoring tools
        
        # Calculate total projected monthly cost
        total_cost = sum(current_costs.values())
        
        # Check against thresholds
        for category, cost in current_costs.items():
            if category in self.cost_thresholds and cost > self.cost_thresholds[category]:
                state["cost_alerts"].append(f"{category.title()} cost ${cost:.2f} exceeds threshold ${self.cost_thresholds[category]:.2f}")
        
        # Check total budget
        if total_cost > self.cost_thresholds["total_monthly"]:
            state["budget_exceeded"] = True
            state["cost_alerts"].append(f"Total projected cost ${total_cost:.2f} exceeds monthly budget ${self.cost_thresholds['total_monthly']:.2f}")
        
        state["current_costs"] = current_costs
        
        self._add_streaming_event(state, "cost_analysis_completed", {
            "projected_monthly_cost": total_cost,
            "budget_limit": self.cost_thresholds["total_monthly"],
            "budget_exceeded": state["budget_exceeded"],
            "cost_alerts": len(state["cost_alerts"]),
            "progress": 15.0
        })
        
        state["progress_percentage"] = 15.0
        logger.info(f"Cost monitoring: ${total_cost:.2f} projected monthly cost")
        
        return state
    
    def _check_budget_status(self, state: PlatformDevelopmentState) -> str:
        """Check budget status and determine next action"""
        
        if state.get("budget_exceeded", False):
            return "budget_exceeded"
        
        # Require approval for high-cost features
        total_cost = sum(state["current_costs"].values())
        if total_cost > 100.0 or state.get("human_approvals_needed"):
            return "needs_approval"
        
        return "proceed"
    
    async def _create_phase_checkpoint(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Create a checkpoint after completing each phase for recovery"""
        
        current_phase = state["current_phase"]
        checkpoint_id = f"{current_phase.value}_{datetime.utcnow().timestamp()}"
        
        state["phase_checkpoints"][current_phase.value] = checkpoint_id
        state["checkpoint_id"] = checkpoint_id
        
        self._add_streaming_event(state, "checkpoint_created", {
            "phase": current_phase.value,
            "checkpoint_id": checkpoint_id,
            "message": f"Checkpoint created for {current_phase.value} phase",
            "recoverable": True
        })
        
        logger.info(f"Created checkpoint {checkpoint_id} for phase {current_phase.value}")
        return state
    
    async def _human_approval_gate(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Human approval gate for production changes and cost overruns"""
        
        approvals_needed = state.get("human_approvals_needed", [])
        
        if not approvals_needed:
            # No approvals needed, proceed
            return state
        
        self._add_streaming_event(state, "human_approval_required", {
            "approvals_needed": approvals_needed,
            "cost_alerts": state.get("cost_alerts", []),
            "budget_exceeded": state.get("budget_exceeded", False),
            "message": "Human approval required before proceeding to production",
            "pause_execution": True
        })
        
        # Initialize approval status for tracking
        for approval in approvals_needed:
            if approval not in state["human_approval_status"]:
                state["human_approval_status"][approval] = "pending"
        
        # Log detailed approval requirements
        logger.warning(f"HUMAN APPROVAL REQUIRED: {approvals_needed}")
        
        # In production, this would pause execution and wait for human input
        # For now, we add warnings and continue with restrictions
        state["warnings"].extend([
            f"CRITICAL: Human approval required for {approval}" 
            for approval in approvals_needed
        ])
        
        return state
    
    async def _handle_budget_exceeded(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Handle budget exceeded scenario with recovery options"""
        
        state["implementation_status"] = "budget_exceeded"
        
        total_cost = sum(state["current_costs"].values())
        budget_limit = self.cost_thresholds["total_monthly"]
        
        recovery_options = [
            f"Reduce feature scope to stay within ${budget_limit:.2f} monthly budget",
            "Break feature into smaller incremental releases",
            "Find free alternatives to paid tools and services", 
            "Defer feature implementation until budget allows",
            "Seek budget approval for ${:.2f} monthly cost".format(total_cost)
        ]
        
        state["next_actions"] = recovery_options
        
        self._add_streaming_event(state, "budget_exceeded_handled", {
            "projected_cost": total_cost,
            "budget_limit": budget_limit,
            "overage": total_cost - budget_limit,
            "recovery_options": len(recovery_options),
            "message": "Feature development paused due to budget constraints"
        })
        
        logger.error(f"Budget exceeded: ${total_cost:.2f} > ${budget_limit:.2f}")
        return state
    
    def _add_streaming_event(self, state: PlatformDevelopmentState, event_type: str, event_data: Dict[str, Any]):
        """Add a streaming event to the state"""
        
        event = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": event_data
        }
        
        events = state.get("streaming_events", [])
        events.append(event)
        state["streaming_events"] = events
        
        # Log important events
        if event_type in ["cost_analysis_completed", "checkpoint_created", "human_approval_required", "budget_exceeded_handled"]:
            logger.info(f"Platform development event: {event_type} - {event_data}")
    
    async def _planning_phase(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Planning phase with feature developer agent and checkpoint"""
        
        logger.info("Starting planning phase")
        
        state["current_phase"] = DevelopmentPhase.PLANNING
        state["progress_percentage"] = 20.0
        
        self._add_streaming_event(state, "planning_phase_started", {
            "message": "Starting feature planning and requirements analysis...",
            "feature_request": state["feature_request"],
            "progress": 20.0
        })
        
        # Use feature developer for planning
        try:
            planning_query = f"""
            Plan the implementation of: {state['feature_request']}
            
            Constraints:
            - Solo developer (part-time, 10-20 hours/week)
            - $0 budget for external development
            - Bootstrap/self-funded approach
            - Must be built incrementally
            
            Provide:
            1. Technical requirements
            2. Implementation phases
            3. Resource requirements
            4. Risk assessment
            """
            
            result = await self._execute_agent("feature_developer", planning_query, {
                "feature_type": state.get("feature_type", FeatureType.CORE_FUNCTIONALITY).value,
                "budget_constraints": state["budget_constraints"]
            })
            
            if result["success"]:
                state["requirements"] = result.get("data", {})
                state["phase_results"]["planning"] = result
                
                # Extract key planning information
                planning_data = result.get("data", {})
                state["technical_specifications"] = planning_data.get("technical_specs", {})
                state["architecture_design"] = planning_data.get("architecture", {})
                
            else:
                state["errors"].append(f"Planning failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            state["errors"].append(f"Planning phase error: {str(e)}")
            logger.error(f"Planning phase failed: {e}")
        
        if DevelopmentPhase.PLANNING not in state.get("completed_phases", []):
            state.setdefault("completed_phases", []).append(DevelopmentPhase.PLANNING)
        
        state["progress_percentage"] = 30.0
        
        self._add_streaming_event(state, "planning_phase_completed", {
            "success": len(state.get("errors", [])) == 0,
            "requirements_defined": bool(state.get("requirements")),
            "progress": 30.0
        })
        
        return state
    
    async def _design_phase(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Design phase with architecture and UI considerations"""
        
        logger.info("Starting design phase")
        
        state["current_phase"] = DevelopmentPhase.DESIGN
        state["progress_percentage"] = 40.0
        
        self._add_streaming_event(state, "design_phase_started", {
            "message": "Starting architecture design and technical specifications...",
            "progress": 40.0
        })
        
        # Use feature developer for design
        try:
            design_query = f"""
            Design the architecture for: {state['feature_request']}
            
            Requirements: {state.get('requirements', {})}
            
            Focus on:
            1. Simple, maintainable architecture 
            2. Minimal external dependencies
            3. Easy deployment and monitoring
            4. Scalability considerations for 100-500 users
            """
            
            result = await self._execute_agent("feature_developer", design_query, {
                "phase": "design",
                "requirements": state.get("requirements", {})
            })
            
            if result["success"]:
                state["phase_results"]["design"] = result
                
                # Update architecture design
                design_data = result.get("data", {})
                state["architecture_design"].update(design_data.get("architecture", {}))
                
            else:
                state["errors"].append(f"Design failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            state["errors"].append(f"Design phase error: {str(e)}")
            logger.error(f"Design phase failed: {e}")
        
        state.setdefault("completed_phases", []).append(DevelopmentPhase.DESIGN)
        state["progress_percentage"] = 50.0
        
        self._add_streaming_event(state, "design_phase_completed", {
            "success": len(state.get("errors", [])) == 0,
            "architecture_defined": bool(state.get("architecture_design")),
            "progress": 50.0
        })
        
        return state
    
    async def _implementation_phase(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Implementation phase with appropriate specialist agents"""
        
        logger.info("Starting implementation phase")
        
        state["current_phase"] = DevelopmentPhase.IMPLEMENTATION
        state["progress_percentage"] = 60.0
        
        self._add_streaming_event(state, "implementation_phase_started", {
            "message": "Starting feature implementation...",
            "feature_type": state.get("feature_type", FeatureType.CORE_FUNCTIONALITY).value,
            "progress": 60.0
        })
        
        feature_type = state.get("feature_type", FeatureType.CORE_FUNCTIONALITY)
        
        # Route to appropriate specialist based on feature type
        if feature_type == FeatureType.PAYMENT:
            agent_name = "payment_integration"
        elif feature_type == FeatureType.SECURITY:
            agent_name = "security_authentication"
        elif feature_type == FeatureType.ANALYTICS:
            agent_name = "monitoring_analytics"
        else:
            agent_name = "feature_developer"
        
        try:
            implementation_query = f"""
            Implement: {state['feature_request']}
            
            Architecture: {state.get('architecture_design', {})}
            Requirements: {state.get('requirements', {})}
            
            Implementation approach:
            1. Start with MVP (Minimum Viable Product)
            2. Use existing tools and libraries where possible
            3. Focus on core functionality first
            4. Plan for iterative improvements
            """
            
            result = await self._execute_agent(agent_name, implementation_query, {
                "phase": "implementation", 
                "architecture": state.get("architecture_design", {}),
                "budget_constraints": state["budget_constraints"]
            })
            
            if result["success"]:
                state["phase_results"]["implementation"] = result
                state["current_deliverables"] = result.get("data", {})
                
            else:
                state["errors"].append(f"Implementation failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            state["errors"].append(f"Implementation phase error: {str(e)}")
            logger.error(f"Implementation phase failed: {e}")
        
        state.setdefault("completed_phases", []).append(DevelopmentPhase.IMPLEMENTATION)
        state["progress_percentage"] = 70.0
        
        self._add_streaming_event(state, "implementation_phase_completed", {
            "success": len(state.get("errors", [])) == 0,
            "deliverables_ready": bool(state.get("current_deliverables")),
            "progress": 70.0
        })
        
        return state
    
    async def _testing_phase(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Testing phase with quality assurance"""
        
        logger.info("Starting testing phase")
        
        state["current_phase"] = DevelopmentPhase.TESTING
        state["progress_percentage"] = 75.0
        
        self._add_streaming_event(state, "testing_phase_started", {
            "message": "Starting comprehensive testing and quality assurance...",
            "progress": 75.0
        })
        
        try:
            testing_query = f"""
            Create testing strategy for: {state['feature_request']}
            
            Implementation: {state.get('current_deliverables', {})}
            
            Testing requirements:
            1. Unit tests for core functionality
            2. Integration tests for key workflows
            3. Basic performance testing
            4. Security testing for sensitive features
            5. User acceptance testing plan
            """
            
            result = await self._execute_agent("feature_developer", testing_query, {
                "phase": "testing",
                "deliverables": state.get("current_deliverables", {})
            })
            
            if result["success"]:
                state["phase_results"]["testing"] = result
                state["test_results"] = result.get("data", {})
                
            else:
                state["warnings"].append(f"Testing setup incomplete: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            state["warnings"].append(f"Testing phase error: {str(e)}")
            logger.error(f"Testing phase failed: {e}")
        
        state.setdefault("completed_phases", []).append(DevelopmentPhase.TESTING)
        state["progress_percentage"] = 80.0
        
        self._add_streaming_event(state, "testing_phase_completed", {
            "success": len(state.get("errors", [])) == 0,
            "tests_defined": bool(state.get("test_results")),
            "progress": 80.0
        })
        
        return state
    
    async def _security_review(self, state: PlatformDevelopmentState) -> PlatformDevelopmentState:
        """Security review phase"""
        
        logger.info("Starting security review")
        
        try:
            security_query = f"""
            Security review for: {state['feature_request']}
            
            Implementation details: {state.get('current_deliverables', {})}
            
            Review areas:
            1. Authentication and authorization
            2. Data protection and privacy
            3. Input validation and sanitization
            4. Secure communication
            5. Compliance with federal standards
            """
            
            result = await self._execute_agent("security_authentication", security_query, {
                "phase": "security_review",
                "implementation": state.get("current_deliverables", {})
            })
            
            if result["success"]:
                state["phase_results"]["security_review"] = result
                state["security_audit_results"] = result.get("data", {})
                
                # Check for security issues
                security_data = result.get("data", {})
                issues = security_data.get("security_issues", [])
                if issues:
                    state["warnings"].extend([f"Security issue: {issue}" for issue in issues])
                
            else:
                state["warnings"].append(f"Security review incomplete: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            state["warnings"].append(f"Security review error: {str(e)}")
            logger.error(f"Security review failed: {e}")
        
        return state
    
    def _check_security_results(self, state: PlatformDevelopmentState) -> str:
        """Check security review results and determine approval path"""
        
        security_results = state.get("security_audit_results", {})
        critical_issues = security_results.get("critical_issues", [])
        high_priority_issues = security_results.get("high_priority_issues", [])
        
        if critical_issues:
            return "needs_fixes"
        
        if high_priority_issues:
            state["warnings"].append("High priority security issues detected - proceed with caution")
            # Require human approval for production deployment with security issues
            state["human_approvals_needed"].append("SECURITY_ISSUES_APPROVAL")
            return "needs_human_approval"
        
        # Check if this is production deployment
        if state.get("target_environment") == DeploymentEnvironment.PRODUCTION:
            state["human_approvals_needed"].append("PRODUCTION_DEPLOYMENT_APPROVAL")
            return "needs_human_approval"
        
        return "approved"
    
    async def _deployment_phase(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Deployment phase with environment setup"""
        
        logger.info("Starting deployment phase")
        
        state["current_phase"] = DevelopmentPhase.DEPLOYMENT
        state["progress_percentage"] = 85.0
        
        self._add_streaming_event(state, "deployment_phase_started", {
            "message": "Starting deployment to target environment...",
            "target_environment": state.get("target_environment", DeploymentEnvironment.STAGING).value,
            "progress": 85.0
        })
        
        try:
            deployment_query = f"""
            Create deployment plan for: {state['feature_request']}
            
            Target environment: {state.get('target_environment', DeploymentEnvironment.STAGING).value}
            Implementation: {state.get('current_deliverables', {})}
            
            Deployment requirements:
            1. Environment setup and configuration
            2. Database migrations if needed
            3. Service dependencies
            4. Rollback plan
            5. Health checks and monitoring
            """
            
            result = await self._execute_agent("feature_developer", deployment_query, {
                "phase": "deployment",
                "environment": state.get("target_environment", DeploymentEnvironment.STAGING).value,
                "budget_constraints": state["budget_constraints"]
            })
            
            if result["success"]:
                state["phase_results"]["deployment"] = result
                state["deployment_plan"] = result.get("data", {})
                
            else:
                state["errors"].append(f"Deployment planning failed: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            state["errors"].append(f"Deployment phase error: {str(e)}")
            logger.error(f"Deployment phase failed: {e}")
        
        state.setdefault("completed_phases", []).append(DevelopmentPhase.DEPLOYMENT)
        state["progress_percentage"] = 90.0
        
        self._add_streaming_event(state, "deployment_phase_completed", {
            "success": len(state.get("errors", [])) == 0,
            "deployment_plan_ready": bool(state.get("deployment_plan")),
            "progress": 90.0
        })
        
        return state
    
    async def _monitoring_setup(self, state: PlatformDevelopmentState, config: RunnableConfig = None) -> PlatformDevelopmentState:
        """Set up monitoring and analytics"""
        
        logger.info("Setting up monitoring")
        
        state["progress_percentage"] = 95.0
        
        self._add_streaming_event(state, "monitoring_setup_started", {
            "message": "Setting up monitoring and analytics...",
            "progress": 95.0
        })
        
        try:
            monitoring_query = f"""
            Set up monitoring for: {state['feature_request']}
            
            Deployment: {state.get('deployment_plan', {})}
            
            Monitoring requirements:
            1. Basic application health checks
            2. Performance metrics
            3. Error tracking and logging
            4. User analytics (privacy-compliant)
            5. Resource utilization monitoring
            """
            
            result = await self._execute_agent("monitoring_analytics", monitoring_query, {
                "phase": "monitoring",
                "deployment": state.get("deployment_plan", {}),
                "budget_constraints": state["budget_constraints"]
            })
            
            if result["success"]:
                state["phase_results"]["monitoring"] = result
                state["monitoring_setup"] = result.get("data", {})
                
            else:
                state["warnings"].append(f"Monitoring setup incomplete: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            state["warnings"].append(f"Monitoring setup error: {str(e)}")
            logger.error(f"Monitoring setup failed: {e}")
        
        state.setdefault("completed_phases", []).append(DevelopmentPhase.MONITORING)
        state["progress_percentage"] = 98.0
        
        self._add_streaming_event(state, "monitoring_setup_completed", {
            "success": len(state.get("warnings", [])) < 3,  # Allow some warnings
            "monitoring_ready": bool(state.get("monitoring_setup")),
            "progress": 98.0
        })
        
        return state
    
    async def _final_validation(self, state: PlatformDevelopmentState) -> PlatformDevelopmentState:
        """Final validation and status update"""
        
        logger.info("Performing final validation")
        
        completed_phases = state.get("completed_phases", [])
        errors = state.get("errors", [])
        
        if errors:
            state["implementation_status"] = "failed"
            state["next_actions"] = [
                "Review and fix identified errors",
                "Re-run failed phases",
                "Consider simplifying implementation approach"
            ]
        elif len(completed_phases) >= 5:  # Most phases completed
            state["implementation_status"] = "completed"
            state["actual_completion"] = datetime.utcnow()
            state["next_actions"] = [
                "Monitor deployment in production",
                "Gather user feedback",
                "Plan iterative improvements",
                "Document lessons learned"
            ]
        else:
            state["implementation_status"] = "partial"
            remaining_phases = [p for p in DevelopmentPhase if p not in completed_phases]
            state["next_actions"] = [f"Complete {phase.value} phase" for phase in remaining_phases[:3]]
        
        # Add human review requirements
        if state.get("human_approvals_needed"):
            state["next_actions"].insert(0, "Obtain required human approvals before deployment")
        
        return state
    
    async def _handle_errors(self, state: PlatformDevelopmentState) -> PlatformDevelopmentState:
        """Handle errors and provide recovery options"""
        
        logger.error("Handling development errors")
        
        state["implementation_status"] = "error"
        errors = state.get("errors", [])
        
        # Provide recovery suggestions based on error types
        recovery_actions = []
        
        if any("budget" in error.lower() for error in errors):
            recovery_actions.extend([
                "Review budget constraints and find free alternatives",
                "Consider phased implementation within budget limits",
                "Explore open-source solutions"
            ])
        
        if any("complexity" in error.lower() for error in errors):
            recovery_actions.extend([
                "Simplify feature requirements",
                "Break down into smaller incremental releases",
                "Focus on MVP (Minimum Viable Product) first"
            ])
        
        if any("security" in error.lower() for error in errors):
            recovery_actions.extend([
                "Conduct thorough security review",
                "Implement security best practices",
                "Consider security-focused implementation approach"
            ])
        
        if not recovery_actions:
            recovery_actions = [
                "Review error logs and identify root causes",
                "Consult documentation and best practices",
                "Consider alternative implementation approaches",
                "Seek expert review if needed"
            ]
        
        state["next_actions"] = recovery_actions
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
    
    async def develop_feature(
        self,
        project_name: str,
        feature_request: str,
        target_environment: DeploymentEnvironment = DeploymentEnvironment.DEVELOPMENT
    ) -> Dict[str, Any]:
        """
        Process a feature development request through the platform workflow
        
        Args:
            project_name: Name of the project 
            feature_request: Description of feature to implement
            target_environment: Target deployment environment
            
        Returns:
            Development results with status and next actions
        """
        
        initial_state = PlatformDevelopmentState(
            project_name=project_name,
            feature_request=feature_request,
            feature_type=FeatureType.CORE_FUNCTIONALITY,
            current_phase=DevelopmentPhase.PLANNING,
            target_environment=target_environment,
            requirements={},
            technical_specifications={},
            architecture_design={},
            security_requirements={},
            assigned_agents=[],
            completed_phases=[],
            current_deliverables={},
            phase_results={},
            test_results={},
            security_audit_results={},
            performance_metrics={},
            deployment_plan={},
            monitoring_setup={},
            rollback_plan={},
            budget_constraints={},
            compliance_checkpoints={},
            human_approvals_needed=[],
            implementation_status="in_progress",
            next_actions=[],
            warnings=[],
            errors=[],
            started_at=datetime.utcnow(),
            estimated_completion=None,
            actual_completion=None
        )
        
        try:
            # Execute the workflow
            compiled_workflow = self.workflow.compile()
            final_state = await compiled_workflow.ainvoke(initial_state)
            
            return {
                "success": final_state["implementation_status"] in ["completed", "partial"],
                "status": final_state["implementation_status"],
                "completed_phases": [phase.value for phase in final_state.get("completed_phases", [])],
                "next_actions": final_state["next_actions"],
                "warnings": final_state["warnings"],
                "errors": final_state["errors"],
                "human_approvals_needed": final_state.get("human_approvals_needed", []),
                "metadata": {
                    "project_name": project_name,
                    "feature_type": final_state.get("feature_type", FeatureType.CORE_FUNCTIONALITY).value,
                    "target_environment": target_environment.value,
                    "started_at": final_state["started_at"].isoformat(),
                    "estimated_completion": final_state.get("estimated_completion", {}).isoformat() if final_state.get("estimated_completion") else None,
                    "actual_completion": final_state.get("actual_completion", {}).isoformat() if final_state.get("actual_completion") else None,
                    "phases_completed": len(final_state.get("completed_phases", [])),
                    "total_phases": len(list(DevelopmentPhase))
                }
            }
            
        except Exception as e:
            logger.error(f"Platform development workflow failed: {e}")
            return {
                "success": False,
                "status": "error",
                "completed_phases": [],
                "next_actions": ["Review system logs and retry with simpler approach"],
                "warnings": [],
                "errors": [f"System error: {str(e)}"],
                "human_approvals_needed": [],
                "streaming_events": [],
                "cost_analysis": {
                    "projected_monthly_cost": 0.0,
                    "budget_limit": self.cost_thresholds["total_monthly"],
                    "budget_exceeded": False,
                    "cost_alerts": []
                },
                "metadata": {
                    "error": str(e),
                    "started_at": datetime.utcnow().isoformat(),
                    "thread_id": config.configurable.get("thread_id") if config else None,
                    "streaming_enabled": enable_streaming,
                    "final_status": "error"
                }
            }
    
    async def resume_from_checkpoint(self, config: RunnableConfig, phase: str = None) -> Dict[str, Any]:
        """Resume development from a specific checkpoint"""
        
        if not self.checkpointer:
            raise ValueError("Checkpointer not enabled")
        
        try:
            compiled_workflow = self.workflow.compile(checkpointer=self.checkpointer)
            
            # Resume from checkpoint
            final_state = None
            async for event in compiled_workflow.astream(None, config):
                final_state = event
            
            return {
                "success": True,
                "resumed": True,
                "status": final_state["implementation_status"],
                "completed_phases": [p.value for p in final_state.get("completed_phases", [])],
                "next_actions": final_state["next_actions"],
                "warnings": final_state["warnings"],
                "streaming_events": final_state.get("streaming_events", []),
                "metadata": {
                    "thread_id": config.configurable.get("thread_id"),
                    "checkpoint_resumed": True,
                    "resumed_from_phase": phase
                }
            }
            
        except Exception as e:
            logger.error(f"Error resuming from checkpoint: {e}")
            return {
                "success": False,
                "error": str(e),
                "streaming_events": []
            }
    
    async def get_cost_analysis(self, config: RunnableConfig) -> Dict[str, Any]:
        """Get current cost analysis for a development session"""
        
        if not self.checkpointer:
            return {"error": "Checkpointer not enabled"}
        
        try:
            state = await self.workflow.compile(checkpointer=self.checkpointer).aget_state(config)
            if state and state.values:
                current_costs = state.values.get("current_costs", {})
                return {
                    "current_costs": current_costs,
                    "total_cost": sum(current_costs.values()),
                    "budget_limit": self.cost_thresholds["total_monthly"],
                    "budget_exceeded": state.values.get("budget_exceeded", False),
                    "cost_alerts": state.values.get("cost_alerts", [])
                }
            return {"error": "No state found"}
        except Exception as e:
            logger.error(f"Error retrieving cost analysis: {e}")
            return {"error": str(e)}


# Export the main class
__all__ = [
    "PlatformDevelopmentGraph", 
    "DevelopmentPhase", 
    "FeatureType", 
    "DeploymentEnvironment",
    "PlatformDevelopmentState"
]
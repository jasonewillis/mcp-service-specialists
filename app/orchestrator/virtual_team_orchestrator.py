"""
Virtual Team Orchestrator with LangGraph
Coordinates multiple agents for complex task execution
"""

from typing import TypedDict, List, Dict, Any, Optional, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
import asyncio
import json
import logging
from datetime import datetime
from enum import Enum

# Import the enhanced factory
from ..agents.enhanced_factory import EnhancedAgentFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED = "failed"

class TeamState(TypedDict):
    """State for team coordination"""
    # Task information
    task_id: str
    task_description: str
    task_priority: int
    
    # Subtask breakdown
    subtasks: List[Dict[str, Any]]
    dependencies: Dict[str, List[str]]
    
    # Agent assignments
    assigned_agents: Dict[str, str]
    agent_availability: Dict[str, bool]
    
    # Execution tracking
    results: Dict[str, Any]
    errors: List[Dict[str, str]]
    status: str
    progress: float
    
    # Workflow control
    current_step: int
    max_iterations: int
    require_human_approval: bool
    human_feedback: Optional[str]
    
    # Metadata
    start_time: str
    end_time: Optional[str]
    execution_log: List[Dict[str, Any]]

class VirtualTeamOrchestrator:
    """Orchestrates virtual development team using LangGraph"""
    
    def __init__(self, factory: Optional[EnhancedAgentFactory] = None):
        """Initialize the orchestrator"""
        self.factory = factory or EnhancedAgentFactory()
        self.checkpointer = MemorySaver()
        self.workflow = self._build_workflow()
        self.active_tasks: Dict[str, TeamState] = {}
        logger.info("Virtual Team Orchestrator initialized")
    
    def _build_workflow(self) -> StateGraph:
        """Build team coordination workflow with LangGraph"""
        workflow = StateGraph(TeamState)
        
        # Define workflow nodes
        workflow.add_node("initialize", self.initialize_task)
        workflow.add_node("analyze_task", self.analyze_task)
        workflow.add_node("assign_agents", self.assign_agents)
        workflow.add_node("check_dependencies", self.check_dependencies)
        workflow.add_node("execute_parallel", self.execute_parallel)
        workflow.add_node("execute_sequential", self.execute_sequential)
        workflow.add_node("review_results", self.review_results)
        workflow.add_node("human_review", self.human_review)
        workflow.add_node("integrate_work", self.integrate_work)
        workflow.add_node("handle_errors", self.handle_errors)
        workflow.add_node("finalize", self.finalize_task)
        
        # Define workflow edges
        workflow.add_edge("initialize", "analyze_task")
        workflow.add_edge("analyze_task", "assign_agents")
        workflow.add_edge("assign_agents", "check_dependencies")
        
        # Conditional routing based on dependencies
        workflow.add_conditional_edges(
            "check_dependencies",
            self.execution_strategy,
            {
                "parallel": "execute_parallel",
                "sequential": "execute_sequential",
                "error": "handle_errors"
            }
        )
        
        # Both execution paths lead to review
        workflow.add_edge("execute_parallel", "review_results")
        workflow.add_edge("execute_sequential", "review_results")
        
        # Conditional routing after review
        workflow.add_conditional_edges(
            "review_results",
            self.review_decision,
            {
                "approve": "integrate_work",
                "retry": "check_dependencies",
                "human": "human_review",
                "error": "handle_errors"
            }
        )
        
        # Human review outcomes
        workflow.add_conditional_edges(
            "human_review",
            self.human_decision,
            {
                "approve": "integrate_work",
                "retry": "check_dependencies",
                "reject": "finalize"
            }
        )
        
        # Error handling
        workflow.add_conditional_edges(
            "handle_errors",
            self.error_recovery,
            {
                "retry": "check_dependencies",
                "fail": "finalize"
            }
        )
        
        # Final steps
        workflow.add_edge("integrate_work", "finalize")
        workflow.add_edge("finalize", END)
        
        # Set entry point
        workflow.set_entry_point("initialize")
        
        return workflow.compile(checkpointer=self.checkpointer)
    
    async def initialize_task(self, state: TeamState) -> TeamState:
        """Initialize a new task"""
        state["task_id"] = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        state["status"] = TaskStatus.ANALYZING.value
        state["start_time"] = datetime.now().isoformat()
        state["execution_log"] = []
        state["progress"] = 0.0
        
        # Initialize empty collections if not present
        state.setdefault("subtasks", [])
        state.setdefault("dependencies", {})
        state.setdefault("assigned_agents", {})
        state.setdefault("results", {})
        state.setdefault("errors", [])
        
        # Log initialization
        self._log_event(state, "task_initialized", {
            "task_id": state["task_id"],
            "description": state["task_description"]
        })
        
        logger.info(f"Task {state['task_id']} initialized")
        return state
    
    async def analyze_task(self, state: TeamState) -> TeamState:
        """Analyze task and break into subtasks"""
        logger.info(f"Analyzing task: {state['task_description']}")
        
        # Use project manager agent to analyze the task
        pm_agent = self.factory.get_agent("project_manager")
        if not pm_agent:
            state["errors"].append({
                "step": "analyze_task",
                "error": "Project manager agent not available"
            })
            return state
        
        analysis_prompt = f"""
        Analyze this task and break it into subtasks:
        {state['task_description']}
        
        Provide a JSON response with:
        {{
            "subtasks": [
                {{
                    "id": "subtask_1",
                    "description": "...",
                    "agent_role": "backend_engineer",
                    "priority": 1,
                    "estimated_time": 30,
                    "dependencies": []
                }}
            ],
            "execution_strategy": "parallel or sequential",
            "total_estimated_time": 120
        }}
        """
        
        try:
            result = await pm_agent.ainvoke({"input": analysis_prompt})
            # Parse the result (in real implementation, would use proper JSON parsing)
            subtasks = self._parse_analysis(result.get("output", ""))
            
            state["subtasks"] = subtasks
            state["progress"] = 10.0
            
            self._log_event(state, "task_analyzed", {
                "subtask_count": len(subtasks)
            })
            
        except Exception as e:
            logger.error(f"Error analyzing task: {e}")
            state["errors"].append({
                "step": "analyze_task",
                "error": str(e)
            })
        
        return state
    
    async def assign_agents(self, state: TeamState) -> TeamState:
        """Assign agents to subtasks"""
        logger.info(f"Assigning agents for {len(state['subtasks'])} subtasks")
        
        # Check agent availability
        available_agents = self.factory.list_agents()
        state["agent_availability"] = {agent: True for agent in available_agents}
        
        # Assign agents to subtasks
        for subtask in state["subtasks"]:
            agent_role = subtask.get("agent_role")
            
            if agent_role in available_agents:
                subtask_id = subtask["id"]
                state["assigned_agents"][subtask_id] = agent_role
                subtask["status"] = "assigned"
                
                logger.info(f"Assigned {agent_role} to {subtask_id}")
            else:
                # Find alternative agent
                alternative = self._find_alternative_agent(agent_role, available_agents)
                if alternative:
                    subtask_id = subtask["id"]
                    state["assigned_agents"][subtask_id] = alternative
                    subtask["status"] = "assigned"
                    subtask["agent_role"] = alternative
                    
                    logger.info(f"Assigned alternative {alternative} to {subtask_id}")
                else:
                    subtask["status"] = "unassigned"
                    state["errors"].append({
                        "step": "assign_agents",
                        "error": f"No agent available for {agent_role}"
                    })
        
        state["progress"] = 20.0
        self._log_event(state, "agents_assigned", state["assigned_agents"])
        
        return state
    
    async def check_dependencies(self, state: TeamState) -> TeamState:
        """Check task dependencies and determine execution order"""
        logger.info("Checking task dependencies")
        
        # Build dependency graph
        for subtask in state["subtasks"]:
            subtask_id = subtask["id"]
            deps = subtask.get("dependencies", [])
            state["dependencies"][subtask_id] = deps
        
        # Validate dependencies
        if self._has_circular_dependencies(state["dependencies"]):
            state["errors"].append({
                "step": "check_dependencies",
                "error": "Circular dependencies detected"
            })
        
        state["progress"] = 25.0
        return state
    
    def execution_strategy(self, state: TeamState) -> Literal["parallel", "sequential", "error"]:
        """Determine execution strategy based on dependencies"""
        if state["errors"]:
            return "error"
        
        # Check if tasks can be executed in parallel
        has_dependencies = any(
            len(deps) > 0 
            for deps in state["dependencies"].values()
        )
        
        if has_dependencies:
            logger.info("Sequential execution required due to dependencies")
            return "sequential"
        else:
            logger.info("Parallel execution possible")
            return "parallel"
    
    async def execute_parallel(self, state: TeamState) -> TeamState:
        """Execute subtasks in parallel"""
        logger.info(f"Executing {len(state['subtasks'])} subtasks in parallel")
        
        tasks = []
        for subtask in state["subtasks"]:
            if subtask.get("status") != "completed":
                subtask_id = subtask["id"]
                agent_role = state["assigned_agents"].get(subtask_id)
                
                if agent_role:
                    task_desc = subtask["description"]
                    task = self._execute_subtask(agent_role, task_desc, subtask_id)
                    tasks.append(task)
        
        # Execute all tasks in parallel
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for result in results:
                if isinstance(result, Exception):
                    state["errors"].append({
                        "step": "execute_parallel",
                        "error": str(result)
                    })
                elif isinstance(result, dict):
                    subtask_id = result.get("subtask_id")
                    state["results"][subtask_id] = result.get("output")
                    
                    # Update subtask status
                    for subtask in state["subtasks"]:
                        if subtask["id"] == subtask_id:
                            subtask["status"] = "completed"
                            break
        
        state["progress"] = 70.0
        state["current_step"] += 1
        
        self._log_event(state, "parallel_execution_complete", {
            "completed_tasks": len([s for s in state["subtasks"] if s.get("status") == "completed"])
        })
        
        return state
    
    async def execute_sequential(self, state: TeamState) -> TeamState:
        """Execute subtasks sequentially based on dependencies"""
        logger.info("Executing subtasks sequentially")
        
        # Sort subtasks by dependencies
        execution_order = self._topological_sort(state["dependencies"])
        
        for subtask_id in execution_order:
            # Find subtask
            subtask = next(
                (s for s in state["subtasks"] if s["id"] == subtask_id),
                None
            )
            
            if subtask and subtask.get("status") != "completed":
                agent_role = state["assigned_agents"].get(subtask_id)
                
                if agent_role:
                    task_desc = subtask["description"]
                    
                    try:
                        result = await self._execute_subtask(
                            agent_role, 
                            task_desc, 
                            subtask_id
                        )
                        
                        state["results"][subtask_id] = result.get("output")
                        subtask["status"] = "completed"
                        
                        # Update progress
                        completed = len([s for s in state["subtasks"] if s.get("status") == "completed"])
                        total = len(state["subtasks"])
                        state["progress"] = 25.0 + (45.0 * completed / total)
                        
                    except Exception as e:
                        logger.error(f"Error executing {subtask_id}: {e}")
                        state["errors"].append({
                            "step": "execute_sequential",
                            "subtask": subtask_id,
                            "error": str(e)
                        })
        
        state["current_step"] += 1
        self._log_event(state, "sequential_execution_complete", {
            "execution_order": execution_order
        })
        
        return state
    
    async def review_results(self, state: TeamState) -> TeamState:
        """Review execution results"""
        logger.info("Reviewing execution results")
        
        # Calculate completion rate
        total_subtasks = len(state["subtasks"])
        completed_subtasks = len([
            s for s in state["subtasks"] 
            if s.get("status") == "completed"
        ])
        
        completion_rate = completed_subtasks / total_subtasks if total_subtasks > 0 else 0
        
        state["progress"] = 80.0
        
        # Log review
        self._log_event(state, "results_reviewed", {
            "completion_rate": completion_rate,
            "errors_count": len(state["errors"])
        })
        
        # Update status based on completion
        if completion_rate == 1.0 and not state["errors"]:
            state["status"] = TaskStatus.REVIEWING.value
        elif state["errors"]:
            state["status"] = TaskStatus.FAILED.value
        
        return state
    
    def review_decision(self, state: TeamState) -> Literal["approve", "retry", "human", "error"]:
        """Decide next step after review"""
        completion_rate = len([s for s in state["subtasks"] if s.get("status") == "completed"]) / len(state["subtasks"])
        
        if state["errors"] and state["current_step"] >= state["max_iterations"]:
            return "error"
        elif state["errors"] and state["current_step"] < state["max_iterations"]:
            return "retry"
        elif state.get("require_human_approval", False):
            return "human"
        elif completion_rate == 1.0:
            return "approve"
        else:
            return "retry"
    
    async def human_review(self, state: TeamState) -> TeamState:
        """Handle human review checkpoint"""
        logger.info("Awaiting human review")
        
        state["status"] = "awaiting_human_review"
        
        # In real implementation, this would wait for human input
        # For now, simulate approval
        await asyncio.sleep(1)
        state["human_feedback"] = "approved"
        
        self._log_event(state, "human_review_complete", {
            "feedback": state["human_feedback"]
        })
        
        return state
    
    def human_decision(self, state: TeamState) -> Literal["approve", "retry", "reject"]:
        """Process human decision"""
        feedback = state.get("human_feedback", "").lower()
        
        if "approve" in feedback:
            return "approve"
        elif "retry" in feedback:
            return "retry"
        else:
            return "reject"
    
    async def integrate_work(self, state: TeamState) -> TeamState:
        """Integrate results from all agents"""
        logger.info("Integrating work from all agents")
        
        # Combine all results
        integrated_result = {
            "task_id": state["task_id"],
            "description": state["task_description"],
            "subtasks_completed": len([s for s in state["subtasks"] if s.get("status") == "completed"]),
            "results": state["results"],
            "execution_time": self._calculate_execution_time(state),
            "status": "success"
        }
        
        state["results"]["integrated"] = integrated_result
        state["progress"] = 90.0
        state["status"] = TaskStatus.COMPLETED.value
        
        self._log_event(state, "work_integrated", integrated_result)
        
        return state
    
    async def handle_errors(self, state: TeamState) -> TeamState:
        """Handle errors in execution"""
        logger.error(f"Handling {len(state['errors'])} errors")
        
        for error in state["errors"]:
            logger.error(f"Error in {error['step']}: {error['error']}")
        
        # Attempt recovery strategies
        if state["current_step"] < state["max_iterations"]:
            # Reset failed subtasks for retry
            for subtask in state["subtasks"]:
                if subtask.get("status") == "failed":
                    subtask["status"] = "pending"
        
        self._log_event(state, "errors_handled", {
            "error_count": len(state["errors"]),
            "retry_attempt": state["current_step"]
        })
        
        return state
    
    def error_recovery(self, state: TeamState) -> Literal["retry", "fail"]:
        """Determine error recovery strategy"""
        if state["current_step"] < state["max_iterations"]:
            logger.info("Retrying after error recovery")
            return "retry"
        else:
            logger.error("Max retries exceeded, failing task")
            return "fail"
    
    async def finalize_task(self, state: TeamState) -> TeamState:
        """Finalize task execution"""
        state["end_time"] = datetime.now().isoformat()
        state["progress"] = 100.0
        
        if state["status"] != TaskStatus.COMPLETED.value:
            state["status"] = TaskStatus.FAILED.value
        
        # Calculate final metrics
        execution_time = self._calculate_execution_time(state)
        
        self._log_event(state, "task_finalized", {
            "status": state["status"],
            "execution_time": execution_time,
            "total_errors": len(state["errors"])
        })
        
        logger.info(f"Task {state['task_id']} finalized with status: {state['status']}")
        
        # Store completed task
        self.active_tasks[state["task_id"]] = state
        
        return state
    
    # Helper methods
    
    async def _execute_subtask(self, agent_role: str, task_desc: str, subtask_id: str) -> Dict[str, Any]:
        """Execute a single subtask with an agent"""
        try:
            output = await self.factory.execute_task(agent_role, task_desc)
            return {
                "subtask_id": subtask_id,
                "agent": agent_role,
                "output": output,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error executing subtask {subtask_id}: {e}")
            return {
                "subtask_id": subtask_id,
                "agent": agent_role,
                "output": None,
                "error": str(e),
                "status": "failed"
            }
    
    def _parse_analysis(self, analysis_output: str) -> List[Dict[str, Any]]:
        """Parse task analysis output into subtasks"""
        # In real implementation, would use proper JSON parsing
        # For now, create sample subtasks
        return [
            {
                "id": "subtask_1",
                "description": "Implement backend API",
                "agent_role": "backend_engineer",
                "priority": 1,
                "estimated_time": 30,
                "dependencies": [],
                "status": "pending"
            },
            {
                "id": "subtask_2",
                "description": "Create frontend components",
                "agent_role": "frontend_developer",
                "priority": 2,
                "estimated_time": 45,
                "dependencies": ["subtask_1"],
                "status": "pending"
            },
            {
                "id": "subtask_3",
                "description": "Write tests",
                "agent_role": "backend_engineer",
                "priority": 3,
                "estimated_time": 20,
                "dependencies": ["subtask_1"],
                "status": "pending"
            }
        ]
    
    def _find_alternative_agent(self, preferred_role: str, available_agents: List[str]) -> Optional[str]:
        """Find alternative agent for a role"""
        # Define role compatibility matrix
        alternatives = {
            "backend_engineer": ["devops_engineer", "database_admin"],
            "frontend_developer": ["ux_designer", "content_creator"],
            "data_scientist": ["statistician", "market_analyst"],
            "devops_engineer": ["backend_engineer", "security_analyst"]
        }
        
        for alt in alternatives.get(preferred_role, []):
            if alt in available_agents:
                return alt
        
        return None
    
    def _has_circular_dependencies(self, dependencies: Dict[str, List[str]]) -> bool:
        """Check for circular dependencies"""
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in dependencies.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in dependencies:
            if node not in visited:
                if has_cycle(node):
                    return True
        
        return False
    
    def _topological_sort(self, dependencies: Dict[str, List[str]]) -> List[str]:
        """Perform topological sort on dependencies"""
        # Simple implementation - in production would use more robust algorithm
        result = []
        visited = set()
        
        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for dep in dependencies.get(node, []):
                visit(dep)
            result.append(node)
        
        for node in dependencies:
            visit(node)
        
        return result[::-1]
    
    def _calculate_execution_time(self, state: TeamState) -> float:
        """Calculate total execution time"""
        if state.get("start_time") and state.get("end_time"):
            start = datetime.fromisoformat(state["start_time"])
            end = datetime.fromisoformat(state["end_time"])
            return (end - start).total_seconds()
        return 0.0
    
    def _log_event(self, state: TeamState, event: str, data: Dict[str, Any]):
        """Log event to execution log"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "data": data
        }
        state["execution_log"].append(log_entry)
        logger.debug(f"Event logged: {event}")
    
    # Public API methods
    
    async def execute_task(
        self,
        task_description: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        agents: Optional[List[str]] = None,
        require_human_approval: bool = False,
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """Execute a task with the virtual team"""
        
        # Create initial state
        state = TeamState(
            task_description=task_description,
            task_priority=priority.value,
            subtasks=[],
            dependencies={},
            assigned_agents={},
            agent_availability={},
            results={},
            errors=[],
            status=TaskStatus.PENDING.value,
            progress=0.0,
            current_step=0,
            max_iterations=max_iterations,
            require_human_approval=require_human_approval,
            human_feedback=None,
            start_time=datetime.now().isoformat(),
            end_time=None,
            execution_log=[]
        )
        
        # If specific agents requested, set them
        if agents:
            state["assigned_agents"] = {f"agent_{i}": agent for i, agent in enumerate(agents)}
        
        # Execute workflow
        result = await self.workflow.ainvoke(state)
        
        return {
            "task_id": result["task_id"],
            "status": result["status"],
            "results": result["results"],
            "errors": result["errors"],
            "execution_time": self._calculate_execution_time(result),
            "progress": result["progress"]
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            return {
                "task_id": task_id,
                "status": task["status"],
                "progress": task["progress"],
                "errors": len(task["errors"]),
                "subtasks_completed": len([s for s in task["subtasks"] if s.get("status") == "completed"]),
                "subtasks_total": len(task["subtasks"])
            }
        return None
    
    def list_active_tasks(self) -> List[Dict[str, Any]]:
        """List all active tasks"""
        return [
            self.get_task_status(task_id)
            for task_id in self.active_tasks
        ]
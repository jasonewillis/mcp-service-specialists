"""
Agent Factory for creating specialized agents
"""

from typing import Dict, Type, Optional
import structlog

from agents.app.agents.base import FederalJobAgent, AgentConfig

# Import role-based agents (to be created)
# from agents.app.agents.roles.data_scientist import DataScientistAgent
# from agents.app.agents.roles.statistician import StatisticianAgent
# from agents.app.agents.roles.database_admin import DatabaseAdminAgent
# from agents.app.agents.roles.devops import DevOpsAgent
# from agents.app.agents.roles.it_specialist import ITSpecialistAgent

# Import compliance agents (to be created)
# from agents.app.agents.compliance.essay_guidance import EssayGuidanceAgent
# from agents.app.agents.compliance.resume_compression import ResumeCompressionAgent
# from agents.app.agents.compliance.executive_order import ExecutiveOrderAgent

# Import backend agents (to be created)
# from agents.app.agents.backend.job_collector import JobCollectionAgent
# from agents.app.agents.backend.analytics import AnalyticsAgent

logger = structlog.get_logger()


class AgentRegistry:
    """Registry of available agent types"""
    
    def __init__(self):
        self._agents: Dict[str, Type[FederalJobAgent]] = {}
        self._metadata: Dict[str, Dict] = {}
        
    def register(
        self, 
        role: str, 
        agent_class: Type[FederalJobAgent],
        metadata: Optional[Dict] = None
    ):
        """Register an agent type"""
        self._agents[role] = agent_class
        self._metadata[role] = metadata or {}
        logger.info(f"Registered agent: {role}")
        
    def get(self, role: str) -> Optional[Type[FederalJobAgent]]:
        """Get an agent class by role"""
        return self._agents.get(role)
        
    def list_agents(self) -> Dict[str, Dict]:
        """List all available agents with metadata"""
        return {
            role: {
                "class": agent_class.__name__,
                "metadata": self._metadata.get(role, {})
            }
            for role, agent_class in self._agents.items()
        }
        
    def is_registered(self, role: str) -> bool:
        """Check if an agent role is registered"""
        return role in self._agents


class AgentFactory:
    """Factory for creating agent instances"""
    
    # Class-level registry
    _registry = AgentRegistry()
    _instances: Dict[str, FederalJobAgent] = {}
    
    @classmethod
    def register_agent(
        cls,
        role: str,
        agent_class: Type[FederalJobAgent],
        metadata: Optional[Dict] = None
    ):
        """Register a new agent type"""
        cls._registry.register(role, agent_class, metadata)
        
    @classmethod
    def create(
        cls,
        role: str,
        user_id: str,
        **kwargs
    ) -> FederalJobAgent:
        """
        Create or retrieve an agent instance
        Uses singleton pattern per role-user combination
        """
        
        # Create unique instance key
        instance_key = f"{role}:{user_id}"
        
        # Check for existing instance
        if instance_key in cls._instances:
            logger.debug(f"Returning existing agent: {instance_key}")
            return cls._instances[instance_key]
            
        # Get agent class
        agent_class = cls._registry.get(role)
        if not agent_class:
            raise ValueError(f"Unknown agent role: {role}")
            
        # Create configuration
        config = AgentConfig(
            role=role,
            user_id=user_id,
            **kwargs
        )
        
        # Create new instance
        agent = agent_class(config)
        cls._instances[instance_key] = agent
        
        logger.info(f"Created new agent: {instance_key}")
        return agent
        
    @classmethod
    def list_available_agents(cls) -> Dict[str, Dict]:
        """List all available agent types"""
        return cls._registry.list_agents()
        
    @classmethod
    async def cleanup_user_agents(cls, user_id: str):
        """Cleanup all agents for a specific user"""
        keys_to_remove = []
        
        for key, agent in cls._instances.items():
            if key.endswith(f":{user_id}"):
                await agent.cleanup()
                keys_to_remove.append(key)
                
        for key in keys_to_remove:
            del cls._instances[key]
            
        logger.info(f"Cleaned up {len(keys_to_remove)} agents for user {user_id}")
        
    @classmethod
    async def cleanup_all_agents(cls):
        """Cleanup all agent instances"""
        for agent in cls._instances.values():
            await agent.cleanup()
            
        cls._instances.clear()
        logger.info("Cleaned up all agent instances")


# Agent role constants
class AgentRoles:
    """Constants for agent roles"""
    
    # Role-based agents
    DATA_SCIENTIST = "data_scientist"
    STATISTICIAN = "statistician"
    DATABASE_ADMIN = "database_admin"
    DEVOPS = "devops"
    IT_SPECIALIST = "it_specialist"
    
    # Compliance agents
    ESSAY_GUIDANCE = "essay_guidance"
    RESUME_COMPRESSION = "resume_compression"
    EXECUTIVE_ORDER = "executive_order"
    
    # Backend agents
    JOB_COLLECTOR = "job_collector"
    ANALYTICS = "analytics"
    
    # Composite agents
    CAREER_ADVISOR = "career_advisor"
    APPLICATION_ASSISTANT = "application_assistant"


def initialize_agents():
    """Initialize and register all available agents"""
    
    # This will be called when agents are implemented
    # Example:
    # AgentFactory.register_agent(
    #     AgentRoles.DATA_SCIENTIST,
    #     DataScientistAgent,
    #     metadata={
    #         "series": ["1560"],
    #         "description": "Specialized for data science federal positions",
    #         "tools": ["skill_matcher", "project_analyzer", "technical_depth_checker"]
    #     }
    # )
    
    logger.info("Agent initialization complete")
"""
Enhanced Agent Factory with Local LLM Support
Virtual Development Team Implementation
"""

from typing import Dict, List, Any, Optional
from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
import asyncio
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model assignments for different agent roles
# Based on comprehensive testing (Jan 2025)
MODEL_ASSIGNMENTS = {
    # Technical Agents - Use qwen3:30b for quality
    "backend_engineer": "qwen3:30b",
    "devops_engineer": "qwen3:30b",
    "database_admin": "qwen3:30b",
    
    # Analytical Agents - Use qwen3:30b for complex analysis
    "data_scientist": "qwen3:30b",
    "statistician": "qwen3:30b",
    "market_analyst": "llama3.1:8b",  # Faster for market insights
    
    # Creative Agents - Use llama3.1:8b for speed
    "frontend_developer": "llama3.1:8b",
    "content_creator": "gptFREE:latest",
    "ux_designer": "llama3.1:8b",  # Fast UI/UX iterations
    
    # Administrative Agents - Use llama3.1:8b for quick responses
    "project_manager": "llama3.1:8b",
    "email_handler": "llama3.1:8b",
    "documentation_specialist": "gptFREE:latest",
    
    # Specialized Agents - Balance based on criticality
    "compliance_officer": "qwen3:30b",  # Quality for compliance
    "security_analyst": "qwen3:30b",    # Quality for security
    "customer_support": "llama3.1:8b"   # Speed for support
}

class EnhancedAgentFactory:
    """Factory for creating specialized agents with local LLMs"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the agent factory"""
        self.agents: Dict[str, AgentExecutor] = {}
        self.models: Dict[str, Ollama] = {}
        self.config = self._load_config(config_path)
        self._initialize_models()
        self._create_all_agents()
        logger.info(f"Initialized {len(self.agents)} agents with local LLMs")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            "models": MODEL_ASSIGNMENTS,
            "agent_settings": {
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 30,
                "retry_attempts": 3
            }
        }
    
    def _initialize_models(self):
        """Initialize all Ollama models"""
        logger.info("Initializing Ollama models...")
        
        for role, model_name in self.config["models"].items():
            try:
                self.models[role] = Ollama(
                    model=model_name,
                    temperature=self.config["agent_settings"]["temperature"],
                    num_ctx=8192,  # Extended context window
                    num_gpu=1,     # GPU acceleration if available
                    repeat_penalty=1.1,
                    timeout=self.config["agent_settings"]["timeout"]
                )
                logger.info(f"✓ Initialized {model_name} for {role}")
            except Exception as e:
                logger.error(f"✗ Failed to initialize {model_name} for {role}: {e}")
    
    def _create_all_agents(self):
        """Create all specialized agents"""
        agent_creators = {
            "backend_engineer": self._create_backend_agent,
            "frontend_developer": self._create_frontend_agent,
            "data_scientist": self._create_data_agent,
            "devops_engineer": self._create_devops_agent,
            "security_analyst": self._create_security_agent,
            "content_creator": self._create_content_agent,
            "project_manager": self._create_pm_agent,
            "compliance_officer": self._create_compliance_agent,
            "database_admin": self._create_database_agent,
            "email_handler": self._create_email_agent
        }
        
        for name, creator_func in agent_creators.items():
            if name in self.models:
                try:
                    self.agents[name] = creator_func()
                    logger.info(f"✓ Created {name} agent")
                except Exception as e:
                    logger.error(f"✗ Failed to create {name} agent: {e}")
    
    def _create_agent(self, role: str, tools: List[Tool], prompt: str, description: str) -> AgentExecutor:
        """Generic agent creation method"""
        if role not in self.models:
            raise ValueError(f"No model configured for role: {role}")
        
        # Create memory
        memory = ConversationSummaryBufferMemory(
            llm=self.models[role],
            max_token_limit=2000,
            return_messages=True
        )
        
        # Create prompt template
        prompt_template = PromptTemplate(
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
            template=prompt
        )
        
        # Create agent
        agent = create_react_agent(
            llm=self.models[role],
            tools=tools,
            prompt=prompt_template
        )
        
        # Create executor
        executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True,
            description=description
        )
        
        return executor
    
    def _create_backend_agent(self) -> AgentExecutor:
        """Create backend development agent"""
        tools = [
            Tool(
                name="create_api_endpoint",
                func=lambda x: f"Created API endpoint: {x}",
                description="Create a new API endpoint"
            ),
            Tool(
                name="debug_code",
                func=lambda x: f"Debugging: {x}",
                description="Debug Python code"
            ),
            Tool(
                name="write_tests",
                func=lambda x: f"Writing tests for: {x}",
                description="Write unit tests"
            ),
            Tool(
                name="optimize_database",
                func=lambda x: f"Optimizing query: {x}",
                description="Optimize database queries"
            ),
            Tool(
                name="implement_feature",
                func=lambda x: f"Implementing feature: {x}",
                description="Implement new feature"
            )
        ]
        
        prompt = """You are a senior backend engineer specializing in FastAPI and Python.
        Your responsibilities include:
        - Creating robust API endpoints
        - Writing comprehensive tests
        - Optimizing database queries
        - Implementing new features
        - Debugging and fixing issues
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "backend_engineer",
            tools,
            prompt,
            "Backend development and API tasks"
        )
    
    def _create_frontend_agent(self) -> AgentExecutor:
        """Create frontend development agent"""
        tools = [
            Tool(
                name="create_component",
                func=lambda x: f"Created React component: {x}",
                description="Create a new React component"
            ),
            Tool(
                name="style_component",
                func=lambda x: f"Styling with Tailwind: {x}",
                description="Add Tailwind CSS styles"
            ),
            Tool(
                name="implement_ui",
                func=lambda x: f"Implementing UI: {x}",
                description="Implement user interface"
            ),
            Tool(
                name="add_interactivity",
                func=lambda x: f"Adding interactivity: {x}",
                description="Add JavaScript interactivity"
            ),
            Tool(
                name="optimize_performance",
                func=lambda x: f"Optimizing frontend: {x}",
                description="Optimize frontend performance"
            )
        ]
        
        prompt = """You are a senior frontend developer specializing in React and Next.js.
        Your responsibilities include:
        - Creating responsive React components
        - Implementing modern UI/UX designs
        - Optimizing frontend performance
        - Adding interactivity and animations
        - Ensuring accessibility standards
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "frontend_developer",
            tools,
            prompt,
            "Frontend development and UI/UX tasks"
        )
    
    def _create_data_agent(self) -> AgentExecutor:
        """Create data science agent"""
        tools = [
            Tool(
                name="analyze_data",
                func=lambda x: f"Analyzing data: {x}",
                description="Perform data analysis"
            ),
            Tool(
                name="create_visualization",
                func=lambda x: f"Creating visualization: {x}",
                description="Create data visualization"
            ),
            Tool(
                name="build_model",
                func=lambda x: f"Building ML model: {x}",
                description="Build machine learning model"
            ),
            Tool(
                name="generate_insights",
                func=lambda x: f"Generating insights: {x}",
                description="Generate data insights"
            ),
            Tool(
                name="create_dashboard",
                func=lambda x: f"Creating dashboard: {x}",
                description="Create analytics dashboard"
            )
        ]
        
        prompt = """You are a senior data scientist specializing in analytics and machine learning.
        Your responsibilities include:
        - Analyzing complex datasets
        - Building predictive models
        - Creating insightful visualizations
        - Generating actionable insights
        - Developing analytics dashboards
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "data_scientist",
            tools,
            prompt,
            "Data analysis and machine learning tasks"
        )
    
    def _create_devops_agent(self) -> AgentExecutor:
        """Create DevOps agent"""
        tools = [
            Tool(
                name="setup_ci_cd",
                func=lambda x: f"Setting up CI/CD: {x}",
                description="Setup CI/CD pipeline"
            ),
            Tool(
                name="configure_docker",
                func=lambda x: f"Configuring Docker: {x}",
                description="Configure Docker containers"
            ),
            Tool(
                name="deploy_application",
                func=lambda x: f"Deploying: {x}",
                description="Deploy application"
            ),
            Tool(
                name="monitor_performance",
                func=lambda x: f"Monitoring: {x}",
                description="Monitor system performance"
            ),
            Tool(
                name="manage_infrastructure",
                func=lambda x: f"Managing infrastructure: {x}",
                description="Manage cloud infrastructure"
            )
        ]
        
        prompt = """You are a senior DevOps engineer specializing in cloud infrastructure and automation.
        Your responsibilities include:
        - Setting up CI/CD pipelines
        - Managing Docker containers
        - Deploying applications
        - Monitoring system performance
        - Managing cloud infrastructure
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "devops_engineer",
            tools,
            prompt,
            "DevOps and infrastructure tasks"
        )
    
    def _create_security_agent(self) -> AgentExecutor:
        """Create security analyst agent"""
        tools = [
            Tool(
                name="security_audit",
                func=lambda x: f"Performing security audit: {x}",
                description="Perform security audit"
            ),
            Tool(
                name="vulnerability_scan",
                func=lambda x: f"Scanning for vulnerabilities: {x}",
                description="Scan for vulnerabilities"
            ),
            Tool(
                name="implement_security",
                func=lambda x: f"Implementing security: {x}",
                description="Implement security measures"
            ),
            Tool(
                name="review_code",
                func=lambda x: f"Reviewing code security: {x}",
                description="Review code for security issues"
            ),
            Tool(
                name="create_security_policy",
                func=lambda x: f"Creating security policy: {x}",
                description="Create security policies"
            )
        ]
        
        prompt = """You are a senior security analyst specializing in application security.
        Your responsibilities include:
        - Performing security audits
        - Identifying vulnerabilities
        - Implementing security measures
        - Reviewing code for security issues
        - Creating security policies
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "security_analyst",
            tools,
            prompt,
            "Security analysis and implementation"
        )
    
    def _create_content_agent(self) -> AgentExecutor:
        """Create content creator agent"""
        tools = [
            Tool(
                name="write_documentation",
                func=lambda x: f"Writing documentation: {x}",
                description="Write technical documentation"
            ),
            Tool(
                name="create_blog_post",
                func=lambda x: f"Creating blog post: {x}",
                description="Create blog post"
            ),
            Tool(
                name="generate_marketing",
                func=lambda x: f"Generating marketing content: {x}",
                description="Generate marketing content"
            ),
            Tool(
                name="write_user_guide",
                func=lambda x: f"Writing user guide: {x}",
                description="Write user guides"
            ),
            Tool(
                name="create_social_media",
                func=lambda x: f"Creating social media content: {x}",
                description="Create social media content"
            )
        ]
        
        prompt = """You are a senior content creator specializing in technical writing and marketing.
        Your responsibilities include:
        - Writing technical documentation
        - Creating blog posts
        - Generating marketing content
        - Writing user guides
        - Creating social media content
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "content_creator",
            tools,
            prompt,
            "Content creation and documentation"
        )
    
    def _create_pm_agent(self) -> AgentExecutor:
        """Create project manager agent"""
        tools = [
            Tool(
                name="plan_project",
                func=lambda x: f"Planning project: {x}",
                description="Create project plan"
            ),
            Tool(
                name="assign_tasks",
                func=lambda x: f"Assigning tasks: {x}",
                description="Assign tasks to team"
            ),
            Tool(
                name="track_progress",
                func=lambda x: f"Tracking progress: {x}",
                description="Track project progress"
            ),
            Tool(
                name="manage_timeline",
                func=lambda x: f"Managing timeline: {x}",
                description="Manage project timeline"
            ),
            Tool(
                name="coordinate_team",
                func=lambda x: f"Coordinating team: {x}",
                description="Coordinate team activities"
            )
        ]
        
        prompt = """You are a senior project manager specializing in agile development.
        Your responsibilities include:
        - Planning and organizing projects
        - Assigning tasks to team members
        - Tracking project progress
        - Managing timelines and deadlines
        - Coordinating team activities
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "project_manager",
            tools,
            prompt,
            "Project management and coordination"
        )
    
    def _create_compliance_agent(self) -> AgentExecutor:
        """Create compliance officer agent"""
        tools = [
            Tool(
                name="check_compliance",
                func=lambda x: f"Checking compliance: {x}",
                description="Check regulatory compliance"
            ),
            Tool(
                name="review_policies",
                func=lambda x: f"Reviewing policies: {x}",
                description="Review compliance policies"
            ),
            Tool(
                name="create_audit_report",
                func=lambda x: f"Creating audit report: {x}",
                description="Create compliance audit report"
            ),
            Tool(
                name="implement_controls",
                func=lambda x: f"Implementing controls: {x}",
                description="Implement compliance controls"
            ),
            Tool(
                name="federal_requirements",
                func=lambda x: f"Checking federal requirements: {x}",
                description="Check federal compliance requirements"
            )
        ]
        
        prompt = """You are a senior compliance officer specializing in federal regulations.
        Your responsibilities include:
        - Ensuring regulatory compliance
        - Reviewing compliance policies
        - Creating audit reports
        - Implementing compliance controls
        - Checking federal requirements
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "compliance_officer",
            tools,
            prompt,
            "Compliance and regulatory tasks"
        )
    
    def _create_database_agent(self) -> AgentExecutor:
        """Create database administrator agent"""
        tools = [
            Tool(
                name="design_schema",
                func=lambda x: f"Designing database schema: {x}",
                description="Design database schema"
            ),
            Tool(
                name="optimize_queries",
                func=lambda x: f"Optimizing queries: {x}",
                description="Optimize SQL queries"
            ),
            Tool(
                name="manage_indexes",
                func=lambda x: f"Managing indexes: {x}",
                description="Manage database indexes"
            ),
            Tool(
                name="backup_database",
                func=lambda x: f"Creating backup: {x}",
                description="Create database backup"
            ),
            Tool(
                name="migrate_data",
                func=lambda x: f"Migrating data: {x}",
                description="Migrate database data"
            )
        ]
        
        prompt = """You are a senior database administrator specializing in PostgreSQL.
        Your responsibilities include:
        - Designing database schemas
        - Optimizing SQL queries
        - Managing database indexes
        - Creating backups
        - Migrating data
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "database_admin",
            tools,
            prompt,
            "Database administration and optimization"
        )
    
    def _create_email_agent(self) -> AgentExecutor:
        """Create email handler agent"""
        tools = [
            Tool(
                name="draft_email",
                func=lambda x: f"Drafting email: {x}",
                description="Draft professional email"
            ),
            Tool(
                name="schedule_meeting",
                func=lambda x: f"Scheduling meeting: {x}",
                description="Schedule meetings"
            ),
            Tool(
                name="manage_calendar",
                func=lambda x: f"Managing calendar: {x}",
                description="Manage calendar events"
            ),
            Tool(
                name="create_report",
                func=lambda x: f"Creating report: {x}",
                description="Create status reports"
            ),
            Tool(
                name="handle_inquiries",
                func=lambda x: f"Handling inquiry: {x}",
                description="Handle customer inquiries"
            )
        ]
        
        prompt = """You are an administrative assistant specializing in communication and organization.
        Your responsibilities include:
        - Drafting professional emails
        - Scheduling meetings
        - Managing calendars
        - Creating status reports
        - Handling inquiries
        
        Current task: {input}
        
        Available tools: {tools}
        Tool names: {tool_names}
        
        Think step by step and use the appropriate tools to complete the task.
        
        {agent_scratchpad}
        """
        
        return self._create_agent(
            "email_handler",
            tools,
            prompt,
            "Email and administrative tasks"
        )
    
    def get_agent(self, role: str) -> Optional[AgentExecutor]:
        """Get agent by role"""
        return self.agents.get(role)
    
    async def execute_task(self, role: str, task: str) -> str:
        """Execute task with specified agent"""
        agent = self.get_agent(role)
        if not agent:
            raise ValueError(f"No agent found for role: {role}")
        
        try:
            result = await agent.ainvoke({"input": task})
            return result.get("output", "Task completed")
        except Exception as e:
            logger.error(f"Error executing task for {role}: {e}")
            raise
    
    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())
    
    def get_agent_info(self, role: str) -> Dict[str, Any]:
        """Get information about a specific agent"""
        if role not in self.agents:
            return {"error": f"Agent {role} not found"}
        
        return {
            "role": role,
            "model": self.config["models"].get(role, "unknown"),
            "description": self.agents[role].description if hasattr(self.agents[role], 'description') else "No description",
            "tools": [tool.name for tool in self.agents[role].tools] if hasattr(self.agents[role], 'tools') else []
        }
    
    def get_all_agents_info(self) -> Dict[str, Any]:
        """Get information about all agents"""
        return {
            role: self.get_agent_info(role)
            for role in self.list_agents()
        }
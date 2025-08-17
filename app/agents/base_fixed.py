"""
Improved Base Agent with Better Error Handling and ReAct Prompt
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncGenerator
import asyncio
from datetime import datetime
import json

from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger()


class AgentConfig(BaseModel):
    """Enhanced configuration for agent instances"""
    role: str = Field(..., description="Agent role identifier")
    user_id: str = Field(..., description="User ID for session tracking")
    model: str = Field(default="gptFREE", description="Ollama model to use")
    temperature: float = Field(default=0.1, description="Lower temperature for consistency")
    max_tokens: int = Field(default=1500, description="Reduced max tokens")
    timeout: int = Field(default=45, description="Increased timeout")
    max_iterations: int = Field(default=2, description="Reduced iterations")
    enable_memory: bool = Field(default=False, description="Disable memory for stability")


class AgentResponse(BaseModel):
    """Standardized agent response format"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ImprovedFederalJobAgent(ABC):
    """
    Improved base class with better error handling and simpler prompts
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.role = config.role
        self.user_id = config.user_id
        
        # Initialize Ollama with conservative settings
        self.llm = Ollama(
            model=config.model,
            temperature=config.temperature,
            num_ctx=2048,  # Reduced context
            num_predict=config.max_tokens,
            top_k=10,  # More focused responses
            top_p=0.9,
            repeat_penalty=1.1
        )
        
        # Simplified memory handling
        self.memory = None
        if config.enable_memory:
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        
        # Load tools and create agent
        self.tools = self._load_tools()
        self.agent = self._create_improved_agent()
        
        # Simple metrics
        self.metrics = {
            "requests": 0,
            "successes": 0,
            "failures": 0
        }
        
        logger.info(f"Initialized improved {self.role} agent")
    
    def _create_improved_agent(self) -> AgentExecutor:
        """Create agent with improved prompt and error handling"""
        
        # Simplified, more reliable ReAct prompt
        template = self._get_improved_prompt_template()
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": self._format_tools_simple(),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )
        
        # Create agent with strict settings
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Executor with conservative settings
        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=self.config.max_iterations,
            handle_parsing_errors=True,
            return_intermediate_steps=False,
            early_stopping_method="force"  # Stop early if needed
        )
        
        return executor
    
    def _format_tools_simple(self) -> str:
        """Format tools in a simple, consistent way"""
        tool_descriptions = []
        for tool in self.tools:
            tool_descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(tool_descriptions)
    
    def _get_improved_prompt_template(self) -> str:
        """Improved ReAct template with better formatting"""
        role_desc = self._get_role_description()
        return f"""You are a Federal Job Advisory Agent. Your role is: {role_desc}

AVAILABLE TOOLS:
{{tools}}

IMPORTANT INSTRUCTIONS:
1. Always use this EXACT format
2. Keep responses focused and concise
3. Use tools to gather information before providing final answer
4. Never write content for candidates - only analyze and guide

FORMAT TO FOLLOW:
Question: [the input question]
Thought: [what you need to do]
Action: [tool name from: {{tool_names}}]
Action Input: [input for the tool]
Observation: [tool result]
Thought: [analyze the result]
Final Answer: [your complete response]

CRITICAL: Follow the format exactly. Always end with "Final Answer:"

Question: {{input}}
Thought:{{agent_scratchpad}}"""
    
    @abstractmethod
    def _load_tools(self) -> List[Tool]:
        """Load role-specific tools"""
        pass
    
    @abstractmethod
    def _get_role_description(self) -> str:
        """Get role-specific description"""
        pass
    
    async def process_simple(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """Simplified processing with better error handling"""
        start_time = datetime.utcnow()
        self.metrics["requests"] += 1
        
        try:
            # Simple input preparation
            agent_input = {"input": query}
            if context:
                agent_input["context"] = json.dumps(context)
            
            # Run with timeout and error catching
            result = await asyncio.wait_for(
                asyncio.to_thread(self._safe_agent_invoke, agent_input),
                timeout=self.config.timeout
            )
            
            self.metrics["successes"] += 1
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AgentResponse(
                success=True,
                message="Analysis completed successfully",
                data={"response": result.get("output", ""), "analysis": result.get("analysis", {})},
                metadata={
                    "agent": self.role,
                    "response_time": response_time,
                    "model": self.config.model
                }
            )
            
        except asyncio.TimeoutError:
            self.metrics["failures"] += 1
            return AgentResponse(
                success=False,
                message=f"Agent response timed out after {self.config.timeout} seconds",
                metadata={"agent": self.role, "timeout": self.config.timeout}
            )
            
        except Exception as e:
            self.metrics["failures"] += 1
            logger.error(f"Agent processing error: {e}")
            
            # Fallback to simple analysis if agent fails
            fallback_response = self._fallback_analysis(query, context)
            
            return AgentResponse(
                success=True,  # Mark as success since we provided fallback
                message="Used fallback analysis due to agent error",
                data={"response": fallback_response, "fallback": True},
                metadata={"agent": self.role, "error": str(e), "mode": "fallback"}
            )
    
    def _safe_agent_invoke(self, agent_input: Dict) -> Dict:
        """Safely invoke agent with error handling"""
        try:
            return self.agent.invoke(agent_input)
        except Exception as e:
            logger.error(f"Agent invoke error: {e}")
            # Return a structured error that can be handled
            return {
                "output": "Agent processing encountered an error. Using fallback analysis.",
                "error": str(e)
            }
    
    @abstractmethod
    def _fallback_analysis(self, query: str, context: Optional[Dict] = None) -> str:
        """Provide fallback analysis when agent fails"""
        pass
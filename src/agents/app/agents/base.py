"""
Base Agent Infrastructure for Federal Job Advisory System
Provides foundation for all specialized agents
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
import redis.asyncio as redis
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger()


class AgentConfig(BaseModel):
    """Configuration for agent instances"""
    role: str = Field(..., description="Agent role identifier")
    user_id: str = Field(..., description="User ID for session tracking")
    model: str = Field(default="gptFREE", description="Ollama model to use")
    temperature: float = Field(default=0.3, description="Model temperature")
    max_tokens: int = Field(default=2000, description="Maximum response tokens")
    timeout: int = Field(default=30, description="Response timeout in seconds")
    enable_memory: bool = Field(default=True, description="Enable conversation memory")
    

class AgentResponse(BaseModel):
    """Standardized agent response format"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FederalJobAgent(ABC):
    """
    Base class for all federal job advisory agents
    Provides common functionality and enforces agent patterns
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.role = config.role
        self.user_id = config.user_id
        
        # Initialize Ollama LLM
        self.llm = Ollama(
            model=config.model,
            temperature=config.temperature,
            num_ctx=4096,
            num_predict=config.max_tokens
        )
        
        # Initialize memory if enabled
        self.memory = None
        self.redis_client = None
        if config.enable_memory:
            self._initialize_memory()
        
        # Load role-specific tools
        self.tools = self._load_tools()
        
        # Create agent executor
        self.agent = self._create_agent()
        
        # Track metrics
        self.metrics = {
            "requests": 0,
            "successes": 0,
            "failures": 0,
            "total_tokens": 0,
            "avg_response_time": 0
        }
        
        logger.info(f"Initialized {self.role} agent for user {self.user_id}")
    
    def _initialize_memory(self):
        """Initialize Redis-backed conversation memory"""
        try:
            # Connect to Redis
            self.redis_client = redis.from_url(
                "redis://localhost:6379",
                decode_responses=True
            )
            
            # Create conversation memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Load existing conversation if available
            asyncio.create_task(self._load_conversation_history())
            
        except Exception as e:
            logger.warning(f"Failed to initialize memory: {e}")
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
    
    async def _load_conversation_history(self):
        """Load conversation history from Redis"""
        if not self.redis_client:
            return
            
        try:
            key = f"conversation:{self.role}:{self.user_id}"
            history = await self.redis_client.get(key)
            
            if history:
                messages = json.loads(history)
                for msg in messages:
                    if msg["type"] == "human":
                        self.memory.chat_memory.add_user_message(msg["content"])
                    else:
                        self.memory.chat_memory.add_ai_message(msg["content"])
                        
        except Exception as e:
            logger.error(f"Failed to load conversation history: {e}")
    
    async def _save_conversation_history(self):
        """Save conversation history to Redis"""
        if not self.redis_client or not self.memory:
            return
            
        try:
            key = f"conversation:{self.role}:{self.user_id}"
            messages = []
            
            for msg in self.memory.chat_memory.messages:
                messages.append({
                    "type": "human" if msg.type == "human" else "ai",
                    "content": msg.content
                })
            
            await self.redis_client.setex(
                key,
                3600,  # 1 hour TTL
                json.dumps(messages)
            )
            
        except Exception as e:
            logger.error(f"Failed to save conversation history: {e}")
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor with tools and memory"""
        
        # Create the prompt template with tool information
        template = self._get_prompt_template()
        
        # Create prompt with partial variables for tools
        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools]),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )
        
        # Create the ReAct agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create the executor
        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True
        )
        
        return executor
    
    @abstractmethod
    def _load_tools(self) -> List[Tool]:
        """
        Load role-specific tools
        Must be implemented by each specialized agent
        """
        pass
    
    @abstractmethod
    def _get_prompt_template(self) -> str:
        """
        Get role-specific prompt template
        Must be implemented by each specialized agent
        """
        pass
    
    @abstractmethod
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Perform role-specific analysis
        Must be implemented by each specialized agent
        """
        pass
    
    async def process(self, query: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process a user query with the agent
        """
        start_time = datetime.utcnow()
        self.metrics["requests"] += 1
        
        try:
            # Prepare input
            agent_input = {
                "input": query,
                "context": json.dumps(context) if context else "{}"
            }
            
            # Run the agent
            result = await asyncio.wait_for(
                asyncio.to_thread(self.agent.invoke, agent_input),
                timeout=self.config.timeout
            )
            
            # Save conversation history
            await self._save_conversation_history()
            
            # Update metrics
            self.metrics["successes"] += 1
            response_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_avg_response_time(response_time)
            
            return AgentResponse(
                success=True,
                message="Query processed successfully",
                data={"response": result.get("output", "")},
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
                message="Agent response timed out",
                metadata={"agent": self.role, "timeout": self.config.timeout}
            )
            
        except Exception as e:
            self.metrics["failures"] += 1
            logger.error(f"Agent processing error: {e}")
            return AgentResponse(
                success=False,
                message=f"Agent processing failed: {str(e)}",
                metadata={"agent": self.role, "error": str(e)}
            )
    
    async def stream_response(
        self, 
        query: str, 
        context: Optional[Dict] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream agent response for real-time UI updates
        """
        try:
            # For now, we'll chunk the response
            # In future, integrate with Ollama streaming
            response = await self.process(query, context)
            
            if response.success and response.data:
                text = response.data.get("response", "")
                
                # Chunk the response
                chunk_size = 50
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i + chunk_size]
                    yield chunk
                    await asyncio.sleep(0.05)  # Small delay for streaming effect
                    
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"Error: {str(e)}"
    
    def _update_avg_response_time(self, new_time: float):
        """Update average response time metric"""
        current_avg = self.metrics["avg_response_time"]
        total_requests = self.metrics["successes"]
        
        if total_requests == 1:
            self.metrics["avg_response_time"] = new_time
        else:
            # Calculate new average
            total_time = current_avg * (total_requests - 1) + new_time
            self.metrics["avg_response_time"] = total_time / total_requests
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        return {
            **self.metrics,
            "success_rate": (
                self.metrics["successes"] / self.metrics["requests"] 
                if self.metrics["requests"] > 0 else 0
            )
        }
    
    async def reset_memory(self):
        """Reset conversation memory"""
        if self.memory:
            self.memory.clear()
            
        if self.redis_client:
            key = f"conversation:{self.role}:{self.user_id}"
            await self.redis_client.delete(key)
            
        logger.info(f"Reset memory for {self.role} agent (user: {self.user_id})")
    
    async def cleanup(self):
        """Cleanup agent resources"""
        try:
            # Save final conversation state
            await self._save_conversation_history()
            
            # Close Redis connection
            if self.redis_client:
                await self.redis_client.close()
                
            logger.info(f"Cleaned up {self.role} agent for user {self.user_id}")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
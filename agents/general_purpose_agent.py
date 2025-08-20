#!/usr/bin/env python3
"""
General Purpose MCP Agent
Handles complex research, analysis, and implementation tasks using local LLM.
Designed for token conservation and cost-effective operation.
"""

import os
import sys
import json
import yaml
import asyncio
import requests
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class AgentRequest:
    """Structure for agent requests"""
    task_description: str
    context: Dict[str, Any]
    output_format: str = "markdown"
    priority: str = "medium"
    max_tokens: int = 4096

@dataclass 
class AgentResponse:
    """Structure for agent responses"""
    success: bool
    content: str
    metadata: Dict[str, Any]
    cost_estimate: float
    tokens_used: int

class GeneralPurposeAgent:
    """
    General Purpose MCP Agent using local Ollama for cost-effective operation
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self.load_config(config_path)
        self.ollama_url = self.config.get("ollama_url", "http://localhost:11434")
        self.model = self.config.get("model", "llama3.1:8b")
        self.fallback_model = self.config.get("fallback_model", "mistral:7b")
        
        # Verify Ollama is running
        self.setup_ollama()
    
    def load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load agent configuration"""
        default_config = {
            "ollama_url": "http://localhost:11434",
            "model": "llama3.1:8b",
            "fallback_model": "mistral:7b",
            "temperature": 0.1,
            "max_tokens": 4096,
            "cost_per_token": 0.0,  # Free local inference
            "timeout": 300  # 5 minutes
        }
        
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)
        
        return default_config
    
    def setup_ollama(self) -> bool:
        """Ensure Ollama is running and models are available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise Exception("Ollama not responding")
            
            # Check if primary model is available
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            
            if self.model not in model_names:
                print(f"📥 Pulling model {self.model}...")
                self.pull_model(self.model)
            
            return True
            
        except Exception as e:
            print(f"❌ Ollama setup failed: {e}")
            print("To fix: brew install ollama && ollama pull llama3.1:8b")
            return False
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model via Ollama"""
        try:
            result = subprocess.run([
                "ollama", "pull", model_name
            ], capture_output=True, text=True, timeout=600)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Failed to pull model {model_name}: {e}")
            return False
    
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a general-purpose agent request"""
        start_time = datetime.now()
        
        try:
            # Build prompt based on task type
            prompt = self.build_prompt(request)
            
            # Get response from Ollama
            response_content = await self.query_ollama(prompt, request.max_tokens)
            
            # Calculate metadata
            processing_time = (datetime.now() - start_time).total_seconds()
            estimated_tokens = len(response_content.split()) * 1.3  # Rough estimate
            
            return AgentResponse(
                success=True,
                content=response_content,
                metadata={
                    "processing_time": processing_time,
                    "model_used": self.model,
                    "task_type": request.task_description,
                    "timestamp": start_time.isoformat()
                },
                cost_estimate=0.0,  # Free local inference
                tokens_used=int(estimated_tokens)
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                content=f"Agent processing failed: {str(e)}",
                metadata={"error": str(e)},
                cost_estimate=0.0,
                tokens_used=0
            )
    
    def build_prompt(self, request: AgentRequest) -> str:
        """Build optimized prompt for the request"""
        
        system_prompt = """You are a general-purpose AI assistant specialized in software development, technical analysis, and project management for the Fed Job Advisor platform.

Key Constraints:
- Follow NO BS Data Honesty Policy - only make quantitative claims with supporting data
- Focus on practical, implementable solutions for a solo developer
- Consider part-time development constraints (10-20 hours/week)
- Prioritize simple, effective solutions over complex architectures
- Always provide actionable next steps

Context: Fed Job Advisor is a federal job search platform with:
- Next.js frontend, FastAPI backend, PostgreSQL database
- Production deployment on Render.com
- Target launch Q1 2025 with $29/$49 monthly tiers
- Current focus on pre-launch feature completion"""

        user_prompt = f"""Task: {request.task_description}

Context: {json.dumps(request.context, indent=2)}

Please provide a comprehensive response in {request.output_format} format with:
1. Clear analysis of the situation
2. Specific, actionable recommendations  
3. Implementation guidance if applicable
4. Honest assessment of time/complexity requirements
5. Risk factors and mitigation strategies

Focus on practical solutions that can be implemented by a solo developer working part-time."""

        return f"{system_prompt}\n\n{user_prompt}"
    
    async def query_ollama(self, prompt: str, max_tokens: int) -> str:
        """Query Ollama API for response"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config["temperature"],
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.config["timeout"]
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code}")
            
            result = response.json()
            return result.get("response", "")
            
        except Exception as e:
            # Try fallback model
            if hasattr(self, 'fallback_attempted'):
                raise e
            
            self.fallback_attempted = True
            try:
                payload["model"] = self.fallback_model
                response = requests.post(
                    f"{self.ollama_url}/api/generate", 
                    json=payload,
                    timeout=self.config["timeout"]
                )
                result = response.json()
                return result.get("response", "")
            except:
                raise e
    
    def save_response(self, request: AgentRequest, response: AgentResponse, output_path: str):
        """Save agent response to file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create comprehensive response document
        document = f"""# General Purpose Agent Response
**Task**: {request.task_description}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Model**: {response.metadata.get('model_used', 'unknown')}
**Processing Time**: {response.metadata.get('processing_time', 0):.2f}s
**Tokens Used**: {response.tokens_used}
**Cost**: ${response.cost_estimate:.4f}

---

{response.content}

---

## Request Metadata
```json
{json.dumps(request.__dict__, indent=2)}
```

## Response Metadata  
```json
{json.dumps(response.metadata, indent=2)}
```
"""
        
        with open(output_file, 'w') as f:
            f.write(document)
        
        print(f"📄 Response saved: {output_file}")

def main():
    """CLI interface for the general-purpose agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="General Purpose MCP Agent")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--context", help="Context JSON string", default="{}")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", default="markdown", help="Output format")
    parser.add_argument("--priority", default="medium", help="Task priority")
    parser.add_argument("--max-tokens", type=int, default=4096, help="Max response tokens")
    
    args = parser.parse_args()
    
    # Create agent
    agent = GeneralPurposeAgent()
    
    # Create request
    request = AgentRequest(
        task_description=args.task,
        context=json.loads(args.context),
        output_format=args.format,
        priority=args.priority,
        max_tokens=args.max_tokens
    )
    
    # Process request
    print(f"🚀 Processing: {args.task}")
    response = asyncio.run(agent.process_request(request))
    
    if response.success:
        print(f"✅ Task completed in {response.metadata.get('processing_time', 0):.2f}s")
        print(f"💰 Cost: ${response.cost_estimate:.4f} | Tokens: {response.tokens_used}")
        
        if args.output:
            agent.save_response(request, response, args.output)
        else:
            print("\n" + "="*50)
            print(response.content)
    else:
        print(f"❌ Task failed: {response.content}")
        sys.exit(1)

if __name__ == "__main__":
    main()
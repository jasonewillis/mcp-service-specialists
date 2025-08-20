#!/usr/bin/env python3
"""
Simple controller startup for the virtual team
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
from ollama import Client

app = FastAPI(title="Virtual Team Controller (Simple)")

# Global client
ollama_client = Client()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Virtual Team Controller",
        "status": "operational",
        "models": ["llama3.1:8b", "gptFREE:latest", "gpt-oss:20b"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/models")
async def list_models():
    """List available Ollama models"""
    try:
        models = ollama_client.list()
        return {
            "models": [
                {
                    "name": m['name'],
                    "size_gb": m['size'] / 1e9,
                    "modified": m['modified']
                }
                for m in models['models']
            ]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/test/{agent_role}")
async def test_agent(agent_role: str, task: str = "Hello, introduce yourself"):
    """Test an agent with a simple task"""
    
    agent_prompts = {
        "backend": "You are a senior backend engineer specializing in FastAPI and Python.",
        "frontend": "You are a senior frontend developer specializing in React and Next.js.",
        "data": "You are a senior data scientist specializing in analytics and ML.",
        "devops": "You are a senior DevOps engineer specializing in Docker and CI/CD.",
        "security": "You are a senior security analyst specializing in application security.",
        "pm": "You are a senior project manager specializing in agile development."
    }
    
    prompt = agent_prompts.get(agent_role, "You are a helpful assistant.")
    
    try:
        response = ollama_client.generate(
            model='llama3.1:8b',
            prompt=f"{prompt}\n\nTask: {task}\n\nResponse:",
            options={'temperature': 0.7, 'num_ctx': 4096}
        )
        
        return {
            "agent": agent_role,
            "task": task,
            "response": response['response'],
            "model": "llama3.1:8b",
            "eval_count": response.get('eval_count', 0)
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/compare")
async def compare_models(task: str = "Write a Python function to reverse a string"):
    """Compare models on same task"""
    models = ['llama3.1:8b', 'qwen3:30b', 'gptFREE:latest']
    results = {}
    
    for model in models:
        try:
            import time
            start = time.time()
            
            response = ollama_client.generate(
                model=model,
                prompt=f"Task: {task}\n\nProvide only code:",
                options={'temperature': 0.7}
            )
            
            results[model] = {
                "response": response['response'][:500],
                "time": time.time() - start,
                "tokens": response.get('eval_count', 0)
            }
        except Exception as e:
            results[model] = {"error": str(e)}
    
    # Determine winner based on speed
    valid_results = {k: v for k, v in results.items() if 'error' not in v}
    if valid_results:
        winner = min(valid_results.keys(), key=lambda k: valid_results[k]['time'])
        results['winner'] = winner
    
    return results

if __name__ == "__main__":
    print("🚀 Starting Virtual Team Controller (Simple)")
    print("📍 API will be available at: http://localhost:8003")
    print("📚 API Docs: http://localhost:8003/docs")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(app, host="127.0.0.1", port=8003)
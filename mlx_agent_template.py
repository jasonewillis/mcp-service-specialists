#!/usr/bin/env python3
"""
MLX-Accelerated MCP Agent Template
Universal template for creating Apple Silicon optimized agents
All agents inherit from this base for automatic MLX acceleration
"""

import mlx.core as mx
import numpy as np
from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
import json
import logging
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)


def mlx_accelerate(func: Callable) -> Callable:
    """Decorator to automatically accelerate functions with MLX"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Convert numpy arrays to MLX arrays for acceleration
            mlx_args = []
            for arg in args:
                if isinstance(arg, np.ndarray):
                    mlx_args.append(mx.array(arg.tolist()))  # Convert via list to avoid type issues
                elif isinstance(arg, (list, tuple)) and arg and isinstance(arg[0], (int, float)):
                    mlx_args.append(mx.array(arg))
                else:
                    mlx_args.append(arg)
            
            # Convert kwargs
            mlx_kwargs = {}
            for key, val in kwargs.items():
                if isinstance(val, np.ndarray):
                    mlx_kwargs[key] = mx.array(val.tolist())
                elif isinstance(val, (list, tuple)) and val and isinstance(val[0], (int, float)):
                    mlx_kwargs[key] = mx.array(val)
                else:
                    mlx_kwargs[key] = val
            
            # Execute on Apple Silicon GPU
            result = func(*mlx_args, **mlx_kwargs)
            
            # Convert MLX arrays back to standard types
            def convert_result(r):
                if hasattr(r, 'tolist'):  # MLX array
                    return r.tolist()  # Return as Python list/number
                return r
                
            if isinstance(result, (list, tuple)):
                return type(result)(convert_result(r) for r in result)
            else:
                return convert_result(result)
            
        except Exception as e:
            logger.warning(f"MLX acceleration failed, falling back to CPU: {e}")
            # Fallback to original function without acceleration
            return func(*args, **kwargs)
    
    return wrapper


class MLXAgent(ABC):
    """
    Base class for all MLX-accelerated MCP agents
    Provides automatic Apple Silicon GPU acceleration for all agents
    """
    
    def __init__(self, agent_name: str, agent_type: str = "specialist"):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.mlx_enabled = self._check_mlx_availability()
        self.performance_metrics = {
            "tasks_processed": 0,
            "mlx_accelerated": 0,
            "cpu_fallback": 0,
            "total_time_saved": 0.0
        }
        
        if self.mlx_enabled:
            logger.info(f"✅ MLX acceleration enabled for {agent_name} on Apple Silicon")
        else:
            logger.warning(f"⚠️ MLX not available for {agent_name}, using CPU")
    
    def _check_mlx_availability(self) -> bool:
        """Check if MLX is available on this system"""
        try:
            # Test MLX with a simple operation
            test_array = mx.array([1, 2, 3])
            result = mx.sum(test_array)
            mx.eval(result)  # Force evaluation
            return True
        except Exception as e:
            logger.debug(f"MLX availability check failed: {e}")
            return False
    
    def preprocess_data(self, data: Any) -> Any:
        """
        Preprocess data - no MLX acceleration to avoid conversion issues
        Override in child classes for specific preprocessing
        """
        if isinstance(data, (list, np.ndarray)):
            # Simple passthrough - let individual methods handle MLX conversion
            if isinstance(data, np.ndarray):
                return data.tolist()
            return data
        return data
    
    @mlx_accelerate
    def compute_embeddings(self, text_or_tokens: Any, fixed_dim: int = 10) -> mx.array:
        """
        Compute embeddings using MLX acceleration with fixed dimensions
        Override for specific embedding models
        """
        # Placeholder for embedding computation with consistent dimensions
        if isinstance(text_or_tokens, str):
            # Simple hash-based embedding for demo with fixed dimensions
            tokens = text_or_tokens.split()
            embeddings = []
            for i in range(fixed_dim):
                # Create a deterministic embedding based on text content
                hash_val = hash(text_or_tokens + str(i)) % 1000
                embeddings.append(hash_val / 1000.0)
            return mx.array(embeddings)
        else:
            # Ensure array has fixed dimensions
            arr = mx.array(text_or_tokens) if not isinstance(text_or_tokens, mx.array) else text_or_tokens
            if len(arr) > fixed_dim:
                return arr[:fixed_dim]
            elif len(arr) < fixed_dim:
                # Pad with zeros
                padding = mx.zeros(fixed_dim - len(arr))
                return mx.concatenate([arr, padding])
            return arr
    
    @mlx_accelerate
    def similarity_search(self, query_embedding: mx.array, 
                         database_embeddings: mx.array,
                         top_k: int = 5) -> List[int]:
        """
        Fast similarity search using MLX
        """
        # Compute cosine similarity
        query_norm = mx.sqrt(mx.sum(query_embedding ** 2))
        db_norms = mx.sqrt(mx.sum(database_embeddings ** 2, axis=1))
        
        # Dot product
        similarities = mx.matmul(database_embeddings, query_embedding)
        
        # Normalize
        similarities = similarities / (db_norms * query_norm + 1e-8)
        
        # Get top-k indices
        top_indices = mx.argsort(similarities)[-top_k:][::-1]
        
        return top_indices.tolist()
    
    @abstractmethod
    def analyze(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis method - must be implemented by each agent
        Automatically benefits from MLX acceleration through helper methods
        """
        pass
    
    @abstractmethod
    def generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on analysis
        Must be implemented by each agent
        """
        pass
    
    def execute_task(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a task with automatic MLX acceleration where applicable
        """
        start_time = datetime.now()
        context = context or {}
        
        try:
            # Log task execution
            logger.info(f"🚀 {self.agent_name} executing task: {task[:100]}...")
            
            # Skip preprocessing for now - let individual methods handle conversion
            # if "data" in context:
            #     context["data"] = self.preprocess_data(context["data"])
            #     self.performance_metrics["mlx_accelerated"] += 1
            
            # Perform analysis
            analysis_results = self.analyze(task, context)
            
            # Generate recommendations
            recommendations = self.generate_recommendations(analysis_results)
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update metrics
            self.performance_metrics["tasks_processed"] += 1
            
            # Create response
            response = {
                "agent": self.agent_name,
                "task": task,
                "analysis": analysis_results,
                "recommendations": recommendations,
                "execution_time": execution_time,
                "mlx_enabled": self.mlx_enabled,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
            logger.info(f"✅ {self.agent_name} completed task in {execution_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ {self.agent_name} failed: {e}")
            self.performance_metrics["cpu_fallback"] += 1
            
            return {
                "agent": self.agent_name,
                "task": task,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance metrics for this agent"""
        return {
            "agent": self.agent_name,
            "mlx_enabled": self.mlx_enabled,
            "metrics": self.performance_metrics,
            "acceleration_rate": (
                self.performance_metrics["mlx_accelerated"] / 
                max(self.performance_metrics["tasks_processed"], 1) * 100
            )
        }


class DataScienceAgent(MLXAgent):
    """Example: Data Science Agent with MLX acceleration"""
    
    def __init__(self):
        super().__init__("data_scientist", "technical_specialist")
    
    @mlx_accelerate
    def analyze(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data science tasks with MLX acceleration"""
        analysis = {
            "task_type": "data_science_analysis",
            "mlx_accelerated": self.mlx_enabled
        }
        
        # Example: Statistical analysis with MLX
        if "data" in context:
            data = context["data"]
            if isinstance(data, (list, np.ndarray)):
                arr = mx.array(data)
                analysis["statistics"] = {
                    "mean": float(mx.mean(arr)),
                    "std": float(mx.std(arr)),
                    "min": float(mx.min(arr)),
                    "max": float(mx.max(arr))
                }
        
        analysis["findings"] = [
            "Data patterns analyzed using MLX acceleration",
            "Statistical insights computed on Apple Silicon GPU",
            "Optimized performance for large-scale data processing"
        ]
        
        return analysis
    
    def generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate data science recommendations"""
        return [
            "Leverage MLX for faster model training",
            "Use Apple Silicon GPU for data preprocessing",
            "Implement batch processing with MLX arrays",
            "Optimize memory usage with lazy evaluation"
        ]


class DevOpsAgent(MLXAgent):
    """Example: DevOps Agent with MLX acceleration for metrics analysis"""
    
    def __init__(self):
        super().__init__("devops_engineer", "infrastructure_specialist")
    
    def analyze(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze DevOps tasks"""
        analysis = {
            "task_type": "infrastructure_analysis",
            "mlx_accelerated": self.mlx_enabled
        }
        
        # Example: Analyze performance metrics with MLX
        if "metrics" in context:
            metrics = context["metrics"]
            if isinstance(metrics, (list, dict)):
                # Process metrics with MLX acceleration
                analysis["performance_analysis"] = self._analyze_metrics(metrics)
        
        analysis["findings"] = [
            "Infrastructure optimized for MLX workloads",
            "Container configurations validated",
            "CI/CD pipeline enhanced with GPU acceleration"
        ]
        
        return analysis
    
    @mlx_accelerate
    def _analyze_metrics(self, metrics: Any) -> Dict[str, float]:
        """Analyze performance metrics using MLX"""
        if isinstance(metrics, list):
            arr = mx.array(metrics)
            return {
                "p50": float(mx.quantile(arr, 0.5)),
                "p95": float(mx.quantile(arr, 0.95)),
                "p99": float(mx.quantile(arr, 0.99))
            }
        return {}
    
    def generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate DevOps recommendations"""
        return [
            "Deploy MLX-enabled containers for agent workloads",
            "Monitor GPU utilization with Metal Performance Shaders",
            "Set up MLX model caching for faster cold starts",
            "Configure memory limits for unified memory architecture"
        ]


# Factory function to create agents
def create_mlx_agent(agent_type: str) -> MLXAgent:
    """Factory function to create MLX-accelerated agents"""
    agents = {
        "data_scientist": DataScienceAgent,
        "devops": DevOpsAgent,
        # Add more agents here as they're created
    }
    
    agent_class = agents.get(agent_type)
    if agent_class:
        return agent_class()
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


if __name__ == "__main__":
    # Test MLX acceleration
    print("🧪 Testing MLX Agent Template")
    
    # Create a data science agent
    ds_agent = DataScienceAgent()
    
    # Test task
    result = ds_agent.execute_task(
        task="Analyze performance data",
        context={
            "data": np.random.randn(1000).tolist()
        }
    )
    
    print(f"\n📊 Results: {json.dumps(result, indent=2)}")
    print(f"\n⚡ Performance: {json.dumps(ds_agent.get_performance_report(), indent=2)}")
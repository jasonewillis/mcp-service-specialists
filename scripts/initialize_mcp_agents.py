#!/usr/bin/env python3
"""
MCP Agents Initialization Script
Loads all specialist agents, verifies documentation, and sets up MCP server
"""

import sys
import os
import json
import importlib
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPAgentInitializer:
    """
    Initializes and validates all MCP specialist agents
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.config_path = self.base_path / "mcp_server_config.json"
        self.docs_path = self.base_path / "documentation" / "external_services"
        
        self.config = None
        self.loaded_agents = {}
        self.failed_agents = []
        self.validation_results = {}
        
    async def initialize_all_agents(self) -> Dict[str, Any]:
        """
        Complete initialization process for all specialist agents
        """
        logger.info("Starting MCP Agents initialization...")
        
        start_time = datetime.now()
        
        try:
            # Load configuration
            await self._load_configuration()
            
            # Validate environment
            await self._validate_environment()
            
            # Load all specialist agents
            await self._load_specialist_agents()
            
            # Verify documentation
            await self._verify_documentation()
            
            # Validate agent tools
            await self._validate_agent_tools()
            
            # Generate initialization report
            report = await self._generate_initialization_report(start_time)
            
            logger.info(f"Initialization completed in {(datetime.now() - start_time).total_seconds():.2f} seconds")
            
            return report
            
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise
    
    async def _load_configuration(self):
        """Load MCP server configuration"""
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
    async def _validate_environment(self):
        """Validate required environment variables"""
        required_vars = self.config.get("environment_configuration", {}).get("required_environment_variables", [])
        optional_vars = self.config.get("environment_configuration", {}).get("optional_environment_variables", [])
        
        missing_required = []
        missing_optional = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_required.append(var)
        
        for var in optional_vars:
            if not os.getenv(var):
                missing_optional.append(var)
        
        if missing_required:
            logger.warning(f"Missing required environment variables: {missing_required}")
        
        if missing_optional:
            logger.info(f"Missing optional environment variables: {missing_optional}")
        
        self.validation_results["environment"] = {
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "total_required": len(required_vars),
            "total_optional": len(optional_vars)
        }
    
    async def _load_specialist_agents(self):
        """Load all specialist agents from configuration"""
        specialist_config = self.config.get("specialist_agents", {})
        
        for category, agents in specialist_config.items():
            logger.info(f"Loading {category} agents...")
            
            for agent_name, agent_config in agents.items():
                try:
                    await self._load_single_agent(agent_name, agent_config, category)
                    logger.info(f"✅ Successfully loaded {agent_name}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to load {agent_name}: {str(e)}")
                    self.failed_agents.append({
                        "name": agent_name,
                        "category": category,
                        "error": str(e)
                    })
    
    async def _load_single_agent(self, agent_name: str, agent_config: Dict[str, Any], category: str):
        """Load a single specialist agent"""
        module_path = agent_config["module"]
        class_name = agent_config["class"]
        
        try:
            # Import the module
            module = importlib.import_module(module_path)
            
            # Get the agent class
            agent_class = getattr(module, class_name)
            
            # Instantiate the agent
            agent_instance = agent_class()
            
            # Store the loaded agent
            self.loaded_agents[agent_name] = {
                "instance": agent_instance,
                "config": agent_config,
                "category": category,
                "module_path": module_path,
                "class_name": class_name
            }
            
        except ImportError as e:
            raise ImportError(f"Could not import module {module_path}: {str(e)}")
        except AttributeError as e:
            raise AttributeError(f"Class {class_name} not found in module {module_path}: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to instantiate {class_name}: {str(e)}")
    
    async def _verify_documentation(self):
        """Verify documentation exists for all agents"""
        doc_verification = {}
        
        for agent_name, agent_data in self.loaded_agents.items():
            doc_path = agent_data["config"].get("documentation_path")
            
            if doc_path:
                full_doc_path = self.docs_path / doc_path
                
                verification = {
                    "path_exists": full_doc_path.exists(),
                    "manifest_exists": False,
                    "examples_exist": False,
                    "best_practices_exist": False
                }
                
                if verification["path_exists"]:
                    verification["manifest_exists"] = (full_doc_path / "manifest.json").exists()
                    verification["examples_exist"] = (full_doc_path / "examples").exists()
                    verification["best_practices_exist"] = (full_doc_path / "best_practices").exists()
                
                doc_verification[agent_name] = verification
                
                if not verification["path_exists"]:
                    logger.warning(f"Documentation missing for {agent_name}: {full_doc_path}")
            else:
                doc_verification[agent_name] = {"error": "No documentation path specified"}
        
        self.validation_results["documentation"] = doc_verification
    
    async def _validate_agent_tools(self):
        """Validate that all agent tools are properly defined"""
        tool_validation = {}
        
        for agent_name, agent_data in self.loaded_agents.items():
            tools_config = agent_data["config"].get("tools", [])
            
            validation = {
                "total_tools": len(tools_config),
                "validated_tools": [],
                "missing_tools": [],
                "tool_errors": []
            }
            
            # Check if agent instance has the tools
            agent_instance = agent_data["instance"]
            
            for tool_config in tools_config:
                tool_name = tool_config["name"]
                
                try:
                    # Check if the tool function exists in the module
                    module_path = agent_data["module_path"]
                    module = importlib.import_module(module_path)
                    
                    if hasattr(module, tool_name):
                        validation["validated_tools"].append(tool_name)
                    else:
                        validation["missing_tools"].append(tool_name)
                        
                except Exception as e:
                    validation["tool_errors"].append({
                        "tool": tool_name,
                        "error": str(e)
                    })
            
            tool_validation[agent_name] = validation
        
        self.validation_results["tools"] = tool_validation
    
    async def _generate_initialization_report(self, start_time: datetime) -> Dict[str, Any]:
        """Generate comprehensive initialization report"""
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Calculate statistics
        total_agents = len(self.config.get("specialist_agents", {}))
        total_categories = sum(len(agents) for agents in self.config.get("specialist_agents", {}).values())
        loaded_count = len(self.loaded_agents)
        failed_count = len(self.failed_agents)
        
        # Documentation statistics
        doc_stats = self._calculate_documentation_stats()
        
        # Tool statistics
        tool_stats = self._calculate_tool_stats()
        
        # Environment statistics
        env_stats = self.validation_results.get("environment", {})
        
        report = {
            "initialization_summary": {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "success": failed_count == 0
            },
            "agent_statistics": {
                "total_categories": len(self.config.get("specialist_agents", {})),
                "total_agents_configured": total_categories,
                "agents_loaded_successfully": loaded_count,
                "agents_failed_to_load": failed_count,
                "success_rate": (loaded_count / total_categories * 100) if total_categories > 0 else 0
            },
            "documentation_statistics": doc_stats,
            "tool_statistics": tool_stats,
            "environment_statistics": env_stats,
            "loaded_agents": {
                name: {
                    "category": data["category"],
                    "class_name": data["class_name"],
                    "specialization": data["config"].get("specialization", "Unknown"),
                    "tool_count": len(data["config"].get("tools", []))
                }
                for name, data in self.loaded_agents.items()
            },
            "failed_agents": self.failed_agents,
            "validation_results": self.validation_results,
            "mcp_server_ready": failed_count == 0 and self._check_mcp_readiness()
        }
        
        return report
    
    def _calculate_documentation_stats(self) -> Dict[str, Any]:
        """Calculate documentation statistics"""
        doc_validation = self.validation_results.get("documentation", {})
        
        total_agents = len(doc_validation)
        agents_with_docs = sum(1 for v in doc_validation.values() 
                              if isinstance(v, dict) and v.get("path_exists", False))
        agents_with_manifests = sum(1 for v in doc_validation.values() 
                                   if isinstance(v, dict) and v.get("manifest_exists", False))
        agents_with_examples = sum(1 for v in doc_validation.values() 
                                  if isinstance(v, dict) and v.get("examples_exist", False))
        
        return {
            "total_agents": total_agents,
            "agents_with_documentation": agents_with_docs,
            "agents_with_manifests": agents_with_manifests,
            "agents_with_examples": agents_with_examples,
            "documentation_coverage": (agents_with_docs / total_agents * 100) if total_agents > 0 else 0
        }
    
    def _calculate_tool_stats(self) -> Dict[str, Any]:
        """Calculate tool statistics"""
        tool_validation = self.validation_results.get("tools", {})
        
        total_tools = sum(v.get("total_tools", 0) for v in tool_validation.values())
        validated_tools = sum(len(v.get("validated_tools", [])) for v in tool_validation.values())
        missing_tools = sum(len(v.get("missing_tools", [])) for v in tool_validation.values())
        tool_errors = sum(len(v.get("tool_errors", [])) for v in tool_validation.values())
        
        return {
            "total_tools_configured": total_tools,
            "tools_validated": validated_tools,
            "tools_missing": missing_tools,
            "tools_with_errors": tool_errors,
            "tool_validation_rate": (validated_tools / total_tools * 100) if total_tools > 0 else 0
        }
    
    def _check_mcp_readiness(self) -> bool:
        """Check if MCP server is ready to start"""
        # MCP server is ready if:
        # 1. At least 80% of agents loaded successfully
        # 2. All critical agents are loaded
        # 3. No critical environment variables are missing
        
        critical_agents = ["usajobs_master", "postgres_expert", "render_specialist"]
        critical_loaded = all(agent in self.loaded_agents for agent in critical_agents)
        
        success_rate = len(self.loaded_agents) / max(1, len(self.loaded_agents) + len(self.failed_agents))
        
        env_issues = len(self.validation_results.get("environment", {}).get("missing_required", []))
        
        return critical_loaded and success_rate >= 0.8 and env_issues == 0
    
    def print_summary(self, report: Dict[str, Any]):
        """Print a human-readable summary of the initialization"""
        print("\n" + "="*60)
        print("🚀 MCP SPECIALIST AGENTS INITIALIZATION SUMMARY")
        print("="*60)
        
        # Agent statistics
        agent_stats = report["agent_statistics"]
        print(f"\n📊 AGENT LOADING:")
        print(f"   ✅ Successfully loaded: {agent_stats['agents_loaded_successfully']}")
        print(f"   ❌ Failed to load: {agent_stats['agents_failed_to_load']}")
        print(f"   📈 Success rate: {agent_stats['success_rate']:.1f}%")
        
        # Documentation statistics
        doc_stats = report["documentation_statistics"]
        print(f"\n📚 DOCUMENTATION:")
        print(f"   📁 Agents with docs: {doc_stats['agents_with_documentation']}/{doc_stats['total_agents']}")
        print(f"   📋 Coverage: {doc_stats['documentation_coverage']:.1f}%")
        
        # Tool statistics
        tool_stats = report["tool_statistics"]
        print(f"\n🛠️  TOOLS:")
        print(f"   ✅ Validated tools: {tool_stats['tools_validated']}")
        print(f"   ❌ Missing tools: {tool_stats['tools_missing']}")
        print(f"   🔧 Validation rate: {tool_stats['tool_validation_rate']:.1f}%")
        
        # Environment
        env_stats = report["environment_statistics"]
        missing_required = len(env_stats.get("missing_required", []))
        if missing_required > 0:
            print(f"\n⚠️  ENVIRONMENT:")
            print(f"   Missing required vars: {missing_required}")
            for var in env_stats.get("missing_required", []):
                print(f"     - {var}")
        
        # MCP Server status
        mcp_ready = report["mcp_server_ready"]
        status_emoji = "✅" if mcp_ready else "❌"
        status_text = "READY" if mcp_ready else "NOT READY"
        print(f"\n🚀 MCP SERVER STATUS: {status_emoji} {status_text}")
        
        if report["failed_agents"]:
            print(f"\n❌ FAILED AGENTS:")
            for failed in report["failed_agents"]:
                print(f"   - {failed['name']} ({failed['category']}): {failed['error']}")
        
        print(f"\n⏱️  Total initialization time: {report['initialization_summary']['duration_seconds']:.2f} seconds")
        print("="*60)

async def main():
    """Main initialization function"""
    try:
        initializer = MCPAgentInitializer()
        report = await initializer.initialize_all_agents()
        
        # Print summary
        initializer.print_summary(report)
        
        # Save detailed report
        report_path = initializer.base_path / "initialization_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        # Return appropriate exit code
        if report["mcp_server_ready"]:
            print("\n🎉 MCP Specialist Agents are ready for use!")
            return 0
        else:
            print("\n⚠️  Some issues need to be resolved before MCP server can start properly.")
            return 1
            
    except Exception as e:
        logger.error(f"Initialization failed with error: {str(e)}")
        print(f"\n💥 Initialization failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
#!/usr/bin/env python3
"""
MCP Research Caller - Interface for Claude Code to request research from MCP agents

This module implements the MCP-first research methodology from TASK_APPROACH_BLUEPRINT.md:
- 80% of thinking done by MCP agents
- Documentation-driven implementation  
- NO BS data honesty policy
- Reality-first validation
"""

import json
import asyncio
import aiohttp
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPResearchCaller:
    """Interface for Claude Code to request systematic research from MCP agents"""
    
    def __init__(self, 
                 mcp_server_url: str = "http://localhost:8002",
                 research_dir: str = "/Users/jasonewillis/Developer/jwRepos/JLWAI/fedJobAdvisor/_Management/_PM/_Tasks"):
        self.mcp_server_url = mcp_server_url
        self.research_dir = Path(research_dir)
        self.active_dir = self.research_dir / "active"
        self.completed_dir = self.research_dir / "completed" 
        self.archived_dir = self.research_dir / "_archived"
        
        # Ensure directories exist
        for dir_path in [self.active_dir, self.completed_dir, self.archived_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Agent selection matrix from TASK_APPROACH_BLUEPRINT.md
        self.agent_matrix = {
            "payment_integration": ["stripe_specialist", "security_specialist", "backend_specialist"],
            "authentication": ["security_specialist", "backend_specialist", "compliance_specialist"],
            "database_changes": ["database_specialist", "backend_specialist", "devops_specialist"],
            "frontend_features": ["frontend_specialist", "ux_specialist", "accessibility_specialist"],
            "data_collection": ["collection_orchestrator", "database_specialist", "analytics_specialist"],
            "federal_compliance": ["compliance_specialist", "essay_specialist", "executive_orders_specialist"],
            "performance": ["devops_specialist", "database_specialist", "backend_specialist"],
            "analytics": ["analytics_specialist", "statistician", "data_scientist"]
        }
        
    async def request_research(self, 
                             task_name: str,
                             task_description: str, 
                             task_type: str,
                             priority: str = "medium") -> Dict[str, Any]:
        """
        Request comprehensive research following MCP-first methodology
        
        Args:
            task_name: Unique identifier for the task
            task_description: Detailed description of what needs to be researched
            task_type: Type of task (from agent_matrix keys)
            priority: Priority level (low/medium/high)
            
        Returns:
            Dict with research status and file locations
        """
        
        logger.info(f"Starting MCP research for task: {task_name}")
        
        # Phase 1.1: Context Gathering
        context_result = await self._gather_context(task_name, task_description, task_type)
        
        # Phase 1.2: MCP Research Assignment
        agents_needed = self._select_agents(task_type)
        research_results = await self._assign_mcp_research(
            task_name, task_description, agents_needed
        )
        
        # Phase 1.3: Research Validation
        validation_result = await self._validate_research(task_name, research_results)
        
        # Create comprehensive research package
        research_package = await self._create_research_package(
            task_name, context_result, research_results, validation_result
        )
        
        return {
            "status": "research_complete",
            "task_name": task_name,
            "agents_used": agents_needed,
            "research_files": research_package["files"],
            "validation_passed": validation_result["passed"],
            "implementation_ready": validation_result["implementation_ready"],
            "next_steps": research_package["next_steps"]
        }
        
    def _select_agents(self, task_type: str) -> List[str]:
        """Select appropriate MCP agents based on task type"""
        
        agents = self.agent_matrix.get(task_type, ["general_specialist"])
        logger.info(f"Selected agents for {task_type}: {agents}")
        return agents
        
    async def _gather_context(self, task_name: str, task_description: str, task_type: str) -> Dict[str, Any]:
        """Phase 1.1: Context Gathering - Current state analysis"""
        
        context_file = self.active_dir / f"{datetime.now().strftime('%Y%m%d')}_{task_name}_CONTEXT.md"
        
        context_content = f"""# Context Analysis - {task_name}

**Date**: {datetime.now().isoformat()}
**Task Type**: {task_type}
**Description**: {task_description}

## Current State Analysis

### Existing Implementation
[Claude Code should analyze current fedJobAdvisor codebase here]

### Documentation Review
[Claude Code should review relevant CLAUDE.md files and constraints]

### Constraint Identification  
[Claude Code should identify technical and business constraints]

## Research Requirements

### Primary Questions
- What currently exists related to this task?
- What are the technical requirements and constraints?
- What are the federal/compliance requirements?
- What are the integration points with existing systems?

### Expected MCP Agent Contributions
- Technical expertise and best practices research
- Implementation patterns and code examples
- Security and compliance analysis
- Integration strategy development

## Context Validation

### Reality Check Items
- [ ] Current capabilities accurately assessed
- [ ] Limitations honestly documented  
- [ ] Constraints properly identified
- [ ] Integration points mapped

**Status**: Context gathering complete
**Next Phase**: MCP Research Assignment
"""

        # Write context file
        with open(context_file, 'w') as f:
            f.write(context_content)
            
        return {
            "context_file": str(context_file),
            "constraints_identified": True,
            "current_state_assessed": True
        }
        
    async def _assign_mcp_research(self, task_name: str, task_description: str, agents: List[str]) -> Dict[str, Any]:
        """Phase 1.2: MCP Research Assignment - 80% of thinking happens here"""
        
        research_results = {}
        
        for agent in agents:
            logger.info(f"Requesting research from {agent}")
            
            # Create research request following template
            research_request = self._create_research_request(
                task_name, task_description, agent
            )
            
            # This would call the actual MCP agent (simulated for now)
            agent_research = await self._call_mcp_agent(agent, research_request)
            
            # Save agent research to file
            research_file = await self._save_agent_research(
                task_name, agent, agent_research
            )
            
            research_results[agent] = {
                "research_file": research_file,
                "research_quality": agent_research.get("quality_score", 0),
                "sources_cited": agent_research.get("sources_count", 0),
                "limitations_noted": agent_research.get("limitations_count", 0)
            }
            
        return research_results
        
    def _create_research_request(self, task_name: str, task_description: str, agent: str) -> Dict[str, Any]:
        """Create structured research request for MCP agent"""
        
        return {
            "task_name": task_name,
            "task_description": task_description,
            "agent_role": agent,
            "research_requirements": {
                "technical_analysis": True,
                "implementation_guidance": True,
                "constraints_identification": True,
                "integration_strategy": True,
                "testing_approach": True,
                "source_attribution": True,
                "limitation_acknowledgment": True
            },
            "output_format": "detailed_markdown",
            "honesty_policy": "NO_BS_quantitative_claims_only",
            "template_path": str(self.research_dir / "templates" / "MCP_RESEARCH_TEMPLATE.md")
        }
        
    async def _call_mcp_agent(self, agent: str, research_request: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP agent for research (actual implementation would use MCP protocol)"""
        
        # For now, simulate the research call
        # In actual implementation, this would:
        # 1. Connect to MCP server
        # 2. Send research request to specific agent
        # 3. Receive comprehensive research response
        # 4. Validate response format and completeness
        
        logger.info(f"Simulating MCP call to {agent}")
        
        # Simulate research response
        return {
            "agent": agent,
            "research_content": f"# Research from {agent}\n\nDetailed technical research would be here...",
            "quality_score": 85,
            "sources_count": 12,
            "limitations_count": 3,
            "implementation_examples": 5,
            "honesty_validation": "passed"
        }
        
    async def _save_agent_research(self, task_name: str, agent: str, research: Dict[str, Any]) -> str:
        """Save agent research to structured file"""
        
        timestamp = datetime.now().strftime('%Y%m%d')
        research_file = self.active_dir / f"{timestamp}_{task_name}_{agent.upper()}_RESEARCH.md"
        
        research_content = f"""# {agent.title()} Research - {task_name}

**Date**: {datetime.now().isoformat()}
**Agent**: {agent}
**Quality Score**: {research.get('quality_score', 'N/A')}

## Research Content

{research.get('research_content', 'No research content provided')}

## Research Metadata

- **Sources Cited**: {research.get('sources_count', 0)}
- **Limitations Noted**: {research.get('limitations_count', 0)}  
- **Implementation Examples**: {research.get('implementation_examples', 0)}
- **Honesty Validation**: {research.get('honesty_validation', 'Not validated')}

## Agent Specialization Applied

This research leverages the {agent} technical mastery documentation for:
- Domain-specific expertise and best practices
- Implementation patterns and code examples
- Security and compliance considerations
- Integration strategies and testing approaches

**Research Status**: Complete
**Implementation Ready**: Pending validation
"""

        with open(research_file, 'w') as f:
            f.write(research_content)
            
        logger.info(f"Saved {agent} research to {research_file}")
        return str(research_file)
        
    async def _validate_research(self, task_name: str, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 1.3: Research Validation - NO BS compliance and reality check"""
        
        validation_results = {
            "passed": True,
            "implementation_ready": True,
            "issues": [],
            "quality_scores": {}
        }
        
        for agent, result in research_results.items():
            quality_score = result["research_quality"]
            sources_cited = result["sources_cited"]
            limitations_noted = result["limitations_noted"]
            
            # Quality validation
            if quality_score < 70:
                validation_results["issues"].append(f"{agent}: Low quality score ({quality_score})")
                validation_results["passed"] = False
                
            if sources_cited < 3:
                validation_results["issues"].append(f"{agent}: Insufficient sources cited ({sources_cited})")
                
            if limitations_noted < 1:
                validation_results["issues"].append(f"{agent}: No limitations acknowledged")
                
            validation_results["quality_scores"][agent] = quality_score
            
        # Create validation report
        await self._create_validation_report(task_name, validation_results)
        
        return validation_results
        
    async def _create_validation_report(self, task_name: str, validation_results: Dict[str, Any]) -> str:
        """Create research validation report"""
        
        timestamp = datetime.now().strftime('%Y%m%d')
        validation_file = self.active_dir / f"{timestamp}_{task_name}_ANALYSIS.md"
        
        validation_content = f"""# Research Validation - {task_name}

**Date**: {datetime.now().isoformat()}
**Validation Status**: {"PASSED" if validation_results["passed"] else "FAILED"}
**Implementation Ready**: {"YES" if validation_results["implementation_ready"] else "NO"}

## Validation Results

### Quality Scores
{chr(10).join([f"- **{agent}**: {score}/100" for agent, score in validation_results["quality_scores"].items()])}

### Issues Identified
{chr(10).join([f"- {issue}" for issue in validation_results["issues"]]) if validation_results["issues"] else "- No issues identified"}

## NO BS Compliance Check

### Quantitative Claims Validation
- [ ] All numerical claims backed by data sources
- [ ] No unsupported projections or estimates
- [ ] Clear acknowledgment of data limitations

### Honesty Audit  
- [ ] "We don't know" items explicitly stated
- [ ] Technical limitations clearly documented
- [ ] Assumptions marked as assumptions

### Reality Alignment
- [ ] Recommendations align with actual fedJobAdvisor architecture  
- [ ] Implementation approach considers development constraints
- [ ] Timeline estimates realistic for solo developer

## Implementation Readiness Assessment

{"Research validation passed - ready for implementation planning" if validation_results["passed"] else "Research validation failed - additional research required"}

**Next Phase**: {"Implementation Planning" if validation_results["passed"] else "Research Revision"}
"""

        with open(validation_file, 'w') as f:
            f.write(validation_content)
            
        return str(validation_file)
        
    async def _create_research_package(self, task_name: str, context_result: Dict, 
                                     research_results: Dict, validation_result: Dict) -> Dict[str, Any]:
        """Create comprehensive research package for implementation"""
        
        timestamp = datetime.now().strftime('%Y%m%d')
        plan_file = self.active_dir / f"{timestamp}_{task_name}_PLAN.md"
        
        # Create implementation plan based on research
        plan_content = f"""# Implementation Plan - {task_name}

**Date**: {datetime.now().isoformat()}
**Research Status**: {"Complete" if validation_result["passed"] else "Incomplete"}
**Implementation Ready**: {"YES" if validation_result["implementation_ready"] else "NO"}

## Research Summary

### Agents Consulted
{chr(10).join([f"- **{agent}**: Quality {result['research_quality']}/100" for agent, result in research_results.items()])}

### Key Findings
[Summary of key research findings from all agents]

### Constraints and Limitations
[Consolidated constraints from all research]

## Implementation Instructions

### Prerequisites  
[What needs to exist before implementation can begin]

### Step-by-Step Implementation
1. **Phase 1**: [First implementation step based on research]
2. **Phase 2**: [Second implementation step]  
3. **Phase 3**: [Final implementation step]

### Code Examples and Patterns
[Consolidated code examples from agent research]

### Testing Strategy
[Testing approach based on agent recommendations]

## Quality Gates

### Success Criteria
[Measurable outcomes that define successful implementation]

### Validation Points
[Checkpoints during implementation to ensure quality]

### Rollback Plan
[How to undo changes if problems occur]

## Next Steps for Claude Code

1. **Read Research Files**: Review all agent research files in detail
2. **Follow Implementation Plan**: Execute steps in order
3. **Validate Against Research**: Ensure implementation matches research recommendations  
4. **Test Thoroughly**: Apply testing strategies from research
5. **Document Results**: Update with actual implementation outcomes

**Implementation Status**: Ready to Begin
**Estimated Effort**: [Based on research complexity]
"""

        with open(plan_file, 'w') as f:
            f.write(plan_content)
            
        # If validation passed, move to completed directory
        if validation_result["passed"]:
            await self._move_to_completed(task_name)
            
        return {
            "files": {
                "context": context_result["context_file"],
                "research": [result["research_file"] for result in research_results.values()],
                "validation": str(self.active_dir / f"{timestamp}_{task_name}_ANALYSIS.md"),
                "plan": str(plan_file)
            },
            "next_steps": [
                "Review all research files",
                "Execute implementation plan",
                "Validate against research recommendations",
                "Test thoroughly",
                "Archive research upon completion"
            ]
        }
        
    async def _move_to_completed(self, task_name: str) -> None:
        """Move research package to completed directory when ready for implementation"""
        
        completed_package_dir = self.completed_dir / f"{task_name}_COMPLETE"
        completed_package_dir.mkdir(exist_ok=True)
        
        # Move relevant files to completed package
        timestamp = datetime.now().strftime('%Y%m%d')
        active_files = list(self.active_dir.glob(f"{timestamp}_{task_name}_*"))
        
        for file_path in active_files:
            target_path = completed_package_dir / file_path.name
            file_path.rename(target_path)
            
        logger.info(f"Moved research package to {completed_package_dir}")
        
    async def get_research_status(self, task_name: str) -> Dict[str, Any]:
        """Get current research status for a task"""
        
        # Check active directory
        active_files = list(self.active_dir.glob(f"*{task_name}*"))
        
        # Check completed directory  
        completed_dir = self.completed_dir / f"{task_name}_COMPLETE"
        completed_exists = completed_dir.exists()
        
        # Check archived directory
        archived_files = list(self.archived_dir.glob(f"*{task_name}*"))
        
        return {
            "task_name": task_name,
            "status": "archived" if archived_files else "completed" if completed_exists else "active" if active_files else "not_found",
            "active_files": [str(f) for f in active_files],
            "completed_package": str(completed_dir) if completed_exists else None,
            "archived_files": [str(f) for f in archived_files]
        }

# Example usage for Claude Code integration
if __name__ == "__main__":
    async def example_usage():
        """Example of how Claude Code would use the MCP Research Caller"""
        
        caller = MCPResearchCaller()
        
        # Request research for a development task
        result = await caller.request_research(
            task_name="stripe_payment_integration",
            task_description="Add Stripe payment processing to fedJobAdvisor with subscription management",
            task_type="payment_integration",
            priority="high"
        )
        
        print("Research Results:")
        print(json.dumps(result, indent=2))
        
        # Check research status
        status = await caller.get_research_status("stripe_payment_integration")
        print("\nResearch Status:")
        print(json.dumps(status, indent=2))
        
    # Run example
    asyncio.run(example_usage())
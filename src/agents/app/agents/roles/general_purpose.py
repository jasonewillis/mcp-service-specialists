"""
General Purpose Agent - Multi-domain Research and Analysis Specialist
Handles complex research, analysis, and multi-step task coordination using local LLM.
Designed for token conservation and cost-effective operation.

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Clearly define the task scope and objectives
2. Gather all relevant background information
3. Identify key stakeholders and constraints
4. Specify output format and success criteria

**Effective Prompting Patterns:**
```
"Research and analyze [specific topic] for [project]:
- Context: [relevant background]
- Scope: [what to include/exclude]  
- Output: [format and depth needed]
- Timeline: [urgency and deadlines]"
```

**Best Workflow:**
1. **Problem Definition** → Use analyze() method with complete context
2. **Research Phase** → Gather information from multiple sources
3. **Analysis Phase** → Synthesize findings and identify patterns
4. **Recommendation Phase** → Provide actionable next steps

### Integration with Other Agents

**Workflow Chains:**
- Start with General Purpose Agent → Specialized domain agents
- Use for initial research → Hand off to technical specialists
- Coordinate multi-agent workflows and consolidate results

**Handoff Points:**
- Pass technical requirements to specialized agents
- Share research findings with domain experts
- Provide coordination for complex implementations

### Common Use Cases

1. **Research Tasks** - Market analysis, competitive intelligence, technical research
2. **Problem-Solving** - Root cause analysis, solution evaluation, risk assessment
3. **Project Planning** - Requirements gathering, timeline estimation, resource planning
4. **Documentation** - Process documentation, technical writing, knowledge synthesis

### Test-Driven Usage Examples

**Example 1: Market Research**
```python
test_data = {
    "topic": "Federal job board competitive landscape",
    "scope": "Direct competitors and feature comparison",
    "output_format": "markdown report",
    "timeline": "urgent - needed within 48 hours"
}
```

**Example 2: Technical Analysis**
```python
test_data = {
    "problem": "Database performance issues",
    "context": "PostgreSQL on Render, 10K+ records",
    "constraints": "Limited budget, part-time development",
    "goals": "Identify bottlenecks and solutions"
}
```

### Integration with CLAUDE.md Principles

- **No assumptions:** Ask for specific requirements and constraints
- **Solo developer focus:** Provide solutions manageable by one person
- **Bootstrap approach:** Prioritize free/low-cost solutions
- **Practical focus:** Emphasize actionable, implementable recommendations
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from ..base import FederalJobAgent, AgentResponse


class GeneralPurposeAgent(FederalJobAgent):
    """
    General-purpose agent for research, analysis, and multi-step coordination
    Provides comprehensive analysis and guidance for complex tasks
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load general-purpose tools"""
        
        tools = [
            Tool(
                name="research_analyzer",
                func=self._analyze_research_topic,
                description="Analyze research topics and provide structured approach"
            ),
            Tool(
                name="problem_solver",
                func=self._solve_problem,
                description="Break down complex problems into manageable components"
            ),
            Tool(
                name="task_coordinator",
                func=self._coordinate_tasks,
                description="Coordinate multi-step tasks and workflows"
            ),
            Tool(
                name="requirements_gatherer",
                func=self._gather_requirements,
                description="Gather and organize project requirements"
            ),
            Tool(
                name="risk_assessor",
                func=self._assess_risks,
                description="Identify and assess project risks and mitigation strategies"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get general-purpose prompt template"""
        
        return """You are a General Purpose AI Assistant specializing in research, analysis, and project coordination for the Fed Job Advisor platform.
        Your role is to provide comprehensive analysis and actionable guidance across multiple domains.
        
        Key Responsibilities:
        1. Conduct thorough research and analysis
        2. Break down complex problems into manageable components
        3. Coordinate multi-step workflows and tasks
        4. Provide evidence-based recommendations
        5. Synthesize information from multiple sources
        
        Focus Areas:
        - Market research and competitive analysis
        - Technical problem-solving and architecture
        - Project planning and resource allocation
        - Risk assessment and mitigation strategies
        - Requirements gathering and documentation
        - Process optimization and workflow design
        
        Constraints:
        - Follow NO BS Data Honesty Policy - only make quantitative claims with supporting data
        - Focus on practical, implementable solutions for a solo developer
        - Consider part-time development constraints (10-20 hours/week)
        - Prioritize simple, effective solutions over complex architectures
        - Always provide actionable next steps
        
        You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Remember: Provide comprehensive analysis with specific, actionable recommendations.
        Focus on practical solutions that can be implemented by a solo developer working part-time.

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""
    
    def _analyze_research_topic(self, input_data: str) -> str:
        """Analyze research topics and provide structured approach"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            topic = data.get("topic", "")
            scope = data.get("scope", "broad")
            timeline = data.get("timeline", "flexible")
            
            # Research methodology framework
            research_methods = {
                "desk_research": ["literature review", "online sources", "documentation"],
                "competitive_analysis": ["feature comparison", "pricing analysis", "market positioning"],
                "technical_analysis": ["architecture review", "performance analysis", "scalability assessment"],
                "user_research": ["surveys", "interviews", "usage analytics"],
                "market_analysis": ["size estimation", "growth trends", "opportunity assessment"]
            }
            
            # Determine appropriate research methods
            recommended_methods = []
            if any(keyword in topic.lower() for keyword in ["competitor", "market", "landscape"]):
                recommended_methods.extend(research_methods["competitive_analysis"])
                recommended_methods.extend(research_methods["market_analysis"])
            
            if any(keyword in topic.lower() for keyword in ["technical", "architecture", "performance"]):
                recommended_methods.extend(research_methods["technical_analysis"])
            
            if any(keyword in topic.lower() for keyword in ["user", "customer", "behavior"]):
                recommended_methods.extend(research_methods["user_research"])
            
            # Default to desk research if no specific methods identified
            if not recommended_methods:
                recommended_methods = research_methods["desk_research"]
            
            return json.dumps({
                "research_approach": {
                    "recommended_methods": recommended_methods,
                    "estimated_timeline": self._estimate_research_timeline(scope, timeline),
                    "deliverables": self._identify_deliverables(topic),
                    "success_metrics": self._define_success_metrics(topic)
                },
                "next_steps": [
                    "Define specific research questions",
                    "Identify information sources",
                    "Set up data collection framework",
                    "Create analysis and reporting structure"
                ]
            })
            
        except Exception as e:
            return f"Error analyzing research topic: {str(e)}"
    
    def _solve_problem(self, input_data: str) -> str:
        """Break down complex problems into manageable components"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            problem = data.get("problem", "")
            context = data.get("context", "")
            constraints = data.get("constraints", [])
            
            # Problem decomposition framework
            problem_components = {
                "root_causes": self._identify_root_causes(problem, context),
                "impact_areas": self._assess_impact_areas(problem),
                "stakeholders": self._identify_stakeholders(problem, context),
                "dependencies": self._map_dependencies(problem),
                "success_criteria": self._define_success_criteria(problem)
            }
            
            # Solution framework
            solution_approach = {
                "immediate_actions": self._suggest_immediate_actions(problem),
                "short_term_solutions": self._develop_short_term_solutions(problem, constraints),
                "long_term_strategy": self._outline_long_term_strategy(problem),
                "resource_requirements": self._estimate_resources(problem, constraints)
            }
            
            return json.dumps({
                "problem_analysis": problem_components,
                "solution_framework": solution_approach,
                "implementation_roadmap": self._create_implementation_roadmap(problem, constraints)
            })
            
        except Exception as e:
            return f"Error solving problem: {str(e)}"
    
    def _coordinate_tasks(self, input_data: str) -> str:
        """Coordinate multi-step tasks and workflows"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            tasks = data.get("tasks", [])
            timeline = data.get("timeline", "flexible")
            resources = data.get("resources", {})
            
            # Task analysis
            task_analysis = []
            for task in tasks:
                analysis = {
                    "task": task,
                    "complexity": self._assess_task_complexity(task),
                    "estimated_effort": self._estimate_effort(task),
                    "dependencies": self._identify_task_dependencies(task, tasks),
                    "priority": self._determine_priority(task)
                }
                task_analysis.append(analysis)
            
            # Workflow optimization
            optimized_workflow = {
                "execution_order": self._optimize_task_order(task_analysis),
                "parallel_opportunities": self._identify_parallel_tasks(task_analysis),
                "critical_path": self._identify_critical_path(task_analysis),
                "milestone_schedule": self._create_milestone_schedule(task_analysis, timeline)
            }
            
            return json.dumps({
                "task_analysis": task_analysis,
                "workflow_optimization": optimized_workflow,
                "coordination_recommendations": self._provide_coordination_tips(task_analysis)
            })
            
        except Exception as e:
            return f"Error coordinating tasks: {str(e)}"
    
    def _gather_requirements(self, input_data: str) -> str:
        """Gather and organize project requirements"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            project_type = data.get("project_type", "general")
            stakeholders = data.get("stakeholders", [])
            goals = data.get("goals", [])
            
            requirements_framework = {
                "functional_requirements": self._identify_functional_requirements(project_type, goals),
                "non_functional_requirements": self._identify_non_functional_requirements(project_type),
                "technical_requirements": self._identify_technical_requirements(project_type),
                "business_requirements": self._identify_business_requirements(goals),
                "user_requirements": self._identify_user_requirements(stakeholders)
            }
            
            return json.dumps({
                "requirements_framework": requirements_framework,
                "requirements_gathering_process": self._design_gathering_process(stakeholders),
                "validation_criteria": self._define_validation_criteria(requirements_framework)
            })
            
        except Exception as e:
            return f"Error gathering requirements: {str(e)}"
    
    def _assess_risks(self, input_data: str) -> str:
        """Identify and assess project risks and mitigation strategies"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            project_scope = data.get("project_scope", "")
            timeline = data.get("timeline", "")
            resources = data.get("resources", {})
            
            # Risk categories
            risk_categories = {
                "technical": ["scalability", "security", "integration", "performance"],
                "resource": ["time constraints", "skill gaps", "budget limitations"],
                "business": ["market changes", "competition", "regulatory"],
                "operational": ["process", "quality", "delivery", "maintenance"]
            }
            
            identified_risks = []
            for category, risk_types in risk_categories.items():
                for risk_type in risk_types:
                    risk_assessment = self._assess_individual_risk(risk_type, project_scope, timeline, resources)
                    if risk_assessment["probability"] > 0:
                        identified_risks.append({
                            "category": category,
                            "risk": risk_type,
                            "probability": risk_assessment["probability"],
                            "impact": risk_assessment["impact"],
                            "mitigation_strategies": risk_assessment["mitigation"]
                        })
            
            return json.dumps({
                "risk_assessment": identified_risks,
                "risk_matrix": self._create_risk_matrix(identified_risks),
                "mitigation_plan": self._create_mitigation_plan(identified_risks)
            })
            
        except Exception as e:
            return f"Error assessing risks: {str(e)}"
    
    # Helper methods for tool implementations
    def _estimate_research_timeline(self, scope: str, timeline: str) -> str:
        """Estimate research timeline based on scope"""
        if "urgent" in timeline.lower():
            return "1-2 days"
        elif "broad" in scope.lower():
            return "1-2 weeks"
        else:
            return "3-5 days"
    
    def _identify_deliverables(self, topic: str) -> List[str]:
        """Identify research deliverables"""
        base_deliverables = ["Research report", "Key findings summary", "Recommendations"]
        
        if "competitive" in topic.lower():
            base_deliverables.extend(["Competitive matrix", "Feature comparison"])
        if "technical" in topic.lower():
            base_deliverables.extend(["Technical analysis", "Architecture recommendations"])
        
        return base_deliverables
    
    def _define_success_metrics(self, topic: str) -> List[str]:
        """Define success metrics for research"""
        return [
            "Comprehensive coverage of topic",
            "Actionable recommendations provided",
            "Evidence-based conclusions",
            "Clear next steps identified"
        ]
    
    def _identify_root_causes(self, problem: str, context: str) -> List[str]:
        """Identify potential root causes"""
        # Simplified root cause analysis
        return ["To be determined through deeper analysis", "Requires stakeholder input", "Needs data investigation"]
    
    def _assess_impact_areas(self, problem: str) -> List[str]:
        """Assess areas impacted by the problem"""
        return ["Users", "System performance", "Business operations", "Development workflow"]
    
    def _identify_stakeholders(self, problem: str, context: str) -> List[str]:
        """Identify relevant stakeholders"""
        return ["End users", "Development team", "Product owner", "System administrators"]
    
    def _map_dependencies(self, problem: str) -> List[str]:
        """Map problem dependencies"""
        return ["External services", "System components", "Data sources", "User workflows"]
    
    def _define_success_criteria(self, problem: str) -> List[str]:
        """Define success criteria for problem resolution"""
        return ["Problem eliminated", "Performance improved", "User satisfaction increased", "System stability maintained"]
    
    def _suggest_immediate_actions(self, problem: str) -> List[str]:
        """Suggest immediate actions"""
        return ["Gather more data", "Assess current state", "Identify quick wins", "Communicate with stakeholders"]
    
    def _develop_short_term_solutions(self, problem: str, constraints: List[str]) -> List[str]:
        """Develop short-term solutions"""
        return ["Implement temporary fixes", "Monitor key metrics", "Document workarounds", "Plan permanent solution"]
    
    def _outline_long_term_strategy(self, problem: str) -> List[str]:
        """Outline long-term strategy"""
        return ["Root cause elimination", "Process improvement", "System enhancement", "Prevention measures"]
    
    def _estimate_resources(self, problem: str, constraints: List[str]) -> Dict[str, str]:
        """Estimate resource requirements"""
        return {
            "time": "To be determined based on scope",
            "skills": "Problem-specific expertise",
            "budget": "Minimal for solo developer",
            "tools": "Standard development tools"
        }
    
    def _create_implementation_roadmap(self, problem: str, constraints: List[str]) -> List[Dict[str, str]]:
        """Create implementation roadmap"""
        return [
            {"phase": "Analysis", "duration": "1-2 days", "activities": ["Problem investigation", "Data gathering"]},
            {"phase": "Solution Design", "duration": "2-3 days", "activities": ["Solution architecture", "Resource planning"]},
            {"phase": "Implementation", "duration": "Variable", "activities": ["Code changes", "Testing", "Deployment"]},
            {"phase": "Validation", "duration": "1-2 days", "activities": ["Testing", "Monitoring", "Documentation"]}
        ]
    
    def _assess_task_complexity(self, task: str) -> str:
        """Assess task complexity"""
        if any(keyword in task.lower() for keyword in ["integrate", "architect", "optimize"]):
            return "High"
        elif any(keyword in task.lower() for keyword in ["implement", "create", "develop"]):
            return "Medium"
        else:
            return "Low"
    
    def _estimate_effort(self, task: str) -> str:
        """Estimate effort required"""
        complexity = self._assess_task_complexity(task)
        if complexity == "High":
            return "8-16 hours"
        elif complexity == "Medium":
            return "4-8 hours"
        else:
            return "1-4 hours"
    
    def _identify_task_dependencies(self, task: str, all_tasks: List[str]) -> List[str]:
        """Identify task dependencies"""
        # Simplified dependency analysis
        return ["Review task relationships for dependencies"]
    
    def _determine_priority(self, task: str) -> str:
        """Determine task priority"""
        if any(keyword in task.lower() for keyword in ["critical", "urgent", "blocker"]):
            return "High"
        elif any(keyword in task.lower() for keyword in ["important", "required"]):
            return "Medium"
        else:
            return "Low"
    
    def _optimize_task_order(self, task_analysis: List[Dict]) -> List[str]:
        """Optimize task execution order"""
        # Sort by priority and dependencies
        sorted_tasks = sorted(task_analysis, key=lambda x: (
            {"High": 3, "Medium": 2, "Low": 1}[x["priority"]], 
            x["complexity"]
        ), reverse=True)
        return [task["task"] for task in sorted_tasks]
    
    def _identify_parallel_tasks(self, task_analysis: List[Dict]) -> List[str]:
        """Identify tasks that can be done in parallel"""
        return ["Review tasks for parallel execution opportunities"]
    
    def _identify_critical_path(self, task_analysis: List[Dict]) -> List[str]:
        """Identify critical path"""
        return ["Determine critical path based on dependencies"]
    
    def _create_milestone_schedule(self, task_analysis: List[Dict], timeline: str) -> List[Dict[str, str]]:
        """Create milestone schedule"""
        return [
            {"milestone": "Planning Complete", "target": "Week 1"},
            {"milestone": "Development 50%", "target": "Week 2-3"},
            {"milestone": "Testing Complete", "target": "Week 4"},
            {"milestone": "Deployment Ready", "target": "Week 4-5"}
        ]
    
    def _provide_coordination_tips(self, task_analysis: List[Dict]) -> List[str]:
        """Provide coordination tips"""
        return [
            "Focus on high-priority tasks first",
            "Look for opportunities to batch similar work",
            "Plan for regular check-ins and reviews",
            "Document progress and blockers"
        ]
    
    def _identify_functional_requirements(self, project_type: str, goals: List[str]) -> List[str]:
        """Identify functional requirements"""
        return ["Core features and capabilities", "User workflows and interactions", "System behaviors and responses"]
    
    def _identify_non_functional_requirements(self, project_type: str) -> List[str]:
        """Identify non-functional requirements"""
        return ["Performance targets", "Security requirements", "Scalability needs", "Usability standards"]
    
    def _identify_technical_requirements(self, project_type: str) -> List[str]:
        """Identify technical requirements"""
        return ["Technology stack", "Integration requirements", "Data requirements", "Infrastructure needs"]
    
    def _identify_business_requirements(self, goals: List[str]) -> List[str]:
        """Identify business requirements"""
        return ["Business objectives", "Success metrics", "Constraints and assumptions", "Compliance requirements"]
    
    def _identify_user_requirements(self, stakeholders: List[str]) -> List[str]:
        """Identify user requirements"""
        return ["User needs and expectations", "User experience goals", "Accessibility requirements", "User support needs"]
    
    def _design_gathering_process(self, stakeholders: List[str]) -> List[str]:
        """Design requirements gathering process"""
        return ["Stakeholder interviews", "Requirements workshops", "Document analysis", "Prototyping sessions"]
    
    def _define_validation_criteria(self, requirements_framework: Dict) -> List[str]:
        """Define validation criteria"""
        return ["Requirements completeness", "Stakeholder approval", "Technical feasibility", "Business alignment"]
    
    def _assess_individual_risk(self, risk_type: str, project_scope: str, timeline: str, resources: Dict) -> Dict:
        """Assess individual risk"""
        # Simplified risk assessment
        return {
            "probability": 0.3,  # Default moderate probability
            "impact": "Medium",
            "mitigation": [f"Monitor {risk_type} closely", f"Develop contingency plan for {risk_type}"]
        }
    
    def _create_risk_matrix(self, risks: List[Dict]) -> Dict[str, List[str]]:
        """Create risk matrix"""
        return {
            "high_priority": [risk["risk"] for risk in risks if risk["probability"] > 0.5 and risk["impact"] == "High"],
            "medium_priority": [risk["risk"] for risk in risks if risk["probability"] > 0.3 or risk["impact"] == "Medium"],
            "low_priority": [risk["risk"] for risk in risks if risk["probability"] <= 0.3 and risk["impact"] == "Low"]
        }
    
    def _create_mitigation_plan(self, risks: List[Dict]) -> List[Dict[str, Any]]:
        """Create mitigation plan"""
        return [
            {
                "risk": risk["risk"],
                "mitigation_actions": risk["mitigation_strategies"],
                "owner": "Project team",
                "timeline": "Ongoing"
            }
            for risk in risks if risk["probability"] > 0.3
        ]
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze general-purpose requests and provide comprehensive guidance
        """
        
        try:
            # Extract request information
            task_type = data.get("task_type", "general")
            context = data.get("context", {})
            requirements = data.get("requirements", [])
            constraints = data.get("constraints", [])
            timeline = data.get("timeline", "flexible")
            
            # Build analysis query
            query = f"""
            Analyze this {task_type} request:
            
            Context: {json.dumps(context, indent=2)}
            
            Requirements: {', '.join(requirements) if requirements else 'To be determined'}
            
            Constraints: {', '.join(constraints) if constraints else 'None specified'}
            
            Timeline: {timeline}
            
            Provide:
            1. Comprehensive analysis of the request
            2. Recommended approach and methodology
            3. Resource requirements and timeline estimate
            4. Risk assessment and mitigation strategies
            5. Specific next steps and action items
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add general recommendations
                response.data["recommendations"] = {
                    "immediate_actions": [
                        "Define clear objectives and success criteria",
                        "Gather all necessary background information",
                        "Identify key stakeholders and constraints",
                        "Create detailed project plan"
                    ],
                    "best_practices": [
                        "Break down complex tasks into manageable components",
                        "Document assumptions and decisions",
                        "Plan for regular progress reviews",
                        "Prepare contingency plans for high-risk areas"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
"""
Data Scientist Agent - Series 1560 Specialist
Analyzes candidates for federal data science positions

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Read candidate's resume/profile first using Read tool
2. Gather job description(s) for target positions 
3. Collect any relevant projects or portfolio information
4. Identify target grade level (GS-11 through GS-15 typical)

**Effective Prompting Patterns:**
```
"Analyze this data scientist candidate for GS-13 positions:
- Skills: [paste skill list]
- Experience: [paste relevant experience]
- Target agency: NASA/NOAA/Census
- Projects: [list 2-3 key projects]"
```

**Best Workflow:**
1. **Profile Analysis** → Use analyze() method with complete candidate data
2. **Gap Identification** → Review recommendations for missing skills
3. **Project Evaluation** → Focus on quantifiable impacts and federal relevance
4. **Merit Hiring Prep** → Use guidance for essay topics (never write content)

### Integration with Other Agents

**Workflow Chains:**
- Start with Data Scientist Agent → Essay Guidance Agent (structure only)
- Use with Analytics Intelligence Agent for market insights
- Combine with Executive Order Research for policy context

**Handoff Points:**
- Pass skill gaps to relevant training resources
- Share project recommendations with Resume Compression Agent
- Provide federal context to Essay Guidance Agent

### Common Pitfalls to Avoid

1. **Don't write content** - Only analyze and point to existing experience
2. **Avoid generic advice** - Use federal-specific context always
3. **Don't ignore quantifiable results** - Federal hiring values metrics
4. **Don't overlook clearance requirements** - Critical for many positions

### Test-Driven Usage Examples

**Example 1: Entry-level PhD**
```python
test_data = {
    "education": {"degree": "PhD", "field": "Statistics"},
    "experience": "2 years academic research",
    "skills": ["Python", "R", "SQL", "scikit-learn"],
    "target_grade": "GS-11"
}
# Expected: Focus on research experience, highlight federal applications
```

**Example 2: Industry Professional**
```python
test_data = {
    "experience": "5 years private sector ML engineer",
    "skills": ["Python", "TensorFlow", "AWS", "Docker"],
    "projects": [{"name": "Fraud Detection", "impact": "Reduced fraud 40%"}],
    "target_grade": "GS-13"
}
# Expected: Emphasize quantifiable business impact, relate to federal use cases
```

### Optimization Tips

1. **Preparation:** Have complete candidate profile before analysis
2. **Context:** Always specify target agency and grade level
3. **Iteration:** Use feedback to refine skill mapping
4. **Documentation:** Track which recommendations work best

### Integration with CLAUDE.md Principles

- **No assumptions:** Ask for specific grade targets and agencies
- **Solo developer focus:** Emphasize skills that one person can demonstrate
- **Bootstrap approach:** Highlight free/open-source technology experience
- **Practical focus:** Point to actual experience, not theoretical knowledge
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from app.agents.base import FederalJobAgent, AgentResponse


class DataScientistAgent(FederalJobAgent):
    """
    Specialized agent for federal data scientist positions (Series 1560)
    Provides guidance without writing content for candidates
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load data science specific tools"""
        
        tools = [
            Tool(
                name="skill_matcher",
                func=self._match_skills,
                description="Match candidate skills to position requirements"
            ),
            Tool(
                name="project_analyzer",
                func=self._analyze_projects,
                description="Analyze data science projects for relevance"
            ),
            Tool(
                name="technical_depth_checker",
                func=self._check_technical_depth,
                description="Evaluate technical depth in key areas"
            ),
            Tool(
                name="publication_finder",
                func=self._find_publications,
                description="Identify relevant publications and research"
            ),
            Tool(
                name="certification_validator",
                func=self._validate_certifications,
                description="Check relevant certifications and training"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get data scientist specific prompt template"""
        
        return """You are a Federal Data Scientist Career Advisor specializing in Series 1560 positions.
        Your role is to ANALYZE and GUIDE candidates, but NEVER write content for them.
        
        Key Responsibilities:
        1. Analyze candidate's data science background
        2. Match skills to federal requirements
        3. Identify gaps in qualifications
        4. Suggest areas to highlight (without writing)
        5. Point to relevant experience they already have
        
        Federal Data Science Focus Areas:
        - Statistical analysis and modeling
        - Machine learning and AI
        - Big data technologies
        - Data visualization
        - Programming (Python, R, SQL)
        - Research and publication
        - Federal data governance
        
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

        Remember: You must NEVER write essays, resumes, or application content. 
        Only analyze, guide, and point to the candidate's existing experience.

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""
    
    def _match_skills(self, input_data: str) -> str:
        """Match candidate skills to position requirements"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            # Core data science skills for federal positions
            required_skills = {
                "programming": ["Python", "R", "SQL", "SAS", "MATLAB"],
                "ml_frameworks": ["scikit-learn", "TensorFlow", "PyTorch", "Keras"],
                "big_data": ["Spark", "Hadoop", "Hive", "HBase"],
                "visualization": ["Tableau", "Power BI", "D3.js", "Plotly"],
                "statistics": ["regression", "hypothesis testing", "time series", "Bayesian"],
                "databases": ["PostgreSQL", "MongoDB", "Oracle", "Redshift"],
                "cloud": ["AWS", "Azure", "GCP", "Databricks"]
            }
            
            candidate_skills = data.get("skills", [])
            matched = {}
            gaps = {}
            
            for category, skills in required_skills.items():
                matched[category] = [s for s in skills if any(s.lower() in c.lower() for c in candidate_skills)]
                gaps[category] = [s for s in skills if s not in matched[category]][:3]  # Top 3 gaps
            
            return json.dumps({
                "matched_skills": matched,
                "skill_gaps": gaps,
                "match_percentage": len([s for m in matched.values() for s in m]) / len([s for r in required_skills.values() for s in r]) * 100
            })
            
        except Exception as e:
            return f"Error analyzing skills: {str(e)}"
    
    def _analyze_projects(self, input_data: str) -> str:
        """Analyze data science projects for federal relevance"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            projects = data.get("projects", [])
            
            federal_relevance_keywords = [
                "classification", "prediction", "forecasting", "optimization",
                "fraud detection", "risk assessment", "resource allocation",
                "policy analysis", "program evaluation", "performance metrics",
                "survey analysis", "census", "demographic", "economic modeling",
                "healthcare analytics", "security", "compliance"
            ]
            
            analyzed_projects = []
            
            for project in projects:
                project_text = project.get("description", "").lower()
                
                # Check for federal relevance
                relevance_score = sum(1 for kw in federal_relevance_keywords if kw in project_text)
                
                # Check for quantifiable results
                has_metrics = bool(re.search(r'\d+%|\$\d+|\d+x|improved|reduced|increased', project_text))
                
                # Check for technical depth
                technical_terms = ["model", "algorithm", "pipeline", "api", "database", "deployment"]
                technical_score = sum(1 for term in technical_terms if term in project_text)
                
                analyzed_projects.append({
                    "project": project.get("name", "Unknown"),
                    "federal_relevance": relevance_score,
                    "has_metrics": has_metrics,
                    "technical_depth": technical_score,
                    "recommendation": self._get_project_recommendation(relevance_score, has_metrics, technical_score)
                })
            
            return json.dumps(analyzed_projects)
            
        except Exception as e:
            return f"Error analyzing projects: {str(e)}"
    
    def _get_project_recommendation(self, relevance: int, has_metrics: bool, technical: int) -> str:
        """Get recommendation for project presentation"""
        
        if relevance >= 3 and has_metrics and technical >= 2:
            return "Highly relevant - emphasize this project"
        elif relevance >= 2 or (has_metrics and technical >= 2):
            return "Relevant - include with federal context"
        else:
            return "Consider relating to federal use cases"
    
    def _check_technical_depth(self, input_data: str) -> str:
        """Evaluate technical depth in key areas"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "")
            
            depth_areas = {
                "statistics": ["regression", "hypothesis", "anova", "time series", "bayesian"],
                "machine_learning": ["supervised", "unsupervised", "deep learning", "neural", "ensemble"],
                "data_engineering": ["etl", "pipeline", "streaming", "batch", "workflow"],
                "experimentation": ["a/b test", "experiment", "causal", "randomized"],
                "domain_knowledge": ["federal", "government", "policy", "regulation", "compliance"]
            }
            
            depth_assessment = {}
            
            for area, keywords in depth_areas.items():
                count = sum(1 for kw in keywords if kw in experience.lower())
                depth_assessment[area] = {
                    "depth": "Strong" if count >= 3 else "Moderate" if count >= 1 else "Limited",
                    "evidence_count": count
                }
            
            return json.dumps(depth_assessment)
            
        except Exception as e:
            return f"Error checking technical depth: {str(e)}"
    
    def _find_publications(self, input_data: str) -> str:
        """Identify relevant publications and research"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            publications = data.get("publications", [])
            
            federal_value_indicators = [
                "peer-reviewed", "journal", "conference", "white paper",
                "technical report", "github", "open source", "methodology"
            ]
            
            valuable_pubs = []
            
            for pub in publications:
                pub_text = pub.get("title", "") + " " + pub.get("venue", "")
                value_score = sum(1 for ind in federal_value_indicators if ind in pub_text.lower())
                
                if value_score > 0:
                    valuable_pubs.append({
                        "publication": pub.get("title"),
                        "value_score": value_score,
                        "recommendation": "Include - demonstrates research capability"
                    })
            
            return json.dumps({
                "valuable_publications": valuable_pubs,
                "total_identified": len(valuable_pubs)
            })
            
        except Exception as e:
            return f"Error analyzing publications: {str(e)}"
    
    def _validate_certifications(self, input_data: str) -> str:
        """Check relevant certifications and training"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            certifications = data.get("certifications", [])
            
            valuable_certs = {
                "cloud": ["AWS Certified", "Azure", "GCP", "Solutions Architect"],
                "data": ["Certified Analytics Professional", "SAS Certified", "Databricks"],
                "project": ["PMP", "Agile", "Scrum Master"],
                "security": ["Security+", "CISSP", "Certified Ethical Hacker"]
            }
            
            cert_assessment = []
            
            for cert in certifications:
                cert_name = cert.get("name", "").lower()
                
                for category, keywords in valuable_certs.items():
                    if any(kw.lower() in cert_name for kw in keywords):
                        cert_assessment.append({
                            "certification": cert.get("name"),
                            "category": category,
                            "federal_value": "High" if category in ["security", "cloud"] else "Medium"
                        })
                        break
            
            return json.dumps({
                "valuable_certifications": cert_assessment,
                "recommendation": "Highlight security and cloud certifications for federal positions"
            })
            
        except Exception as e:
            return f"Error validating certifications: {str(e)}"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze candidate profile for data scientist positions
        """
        
        try:
            # Extract candidate information
            skills = data.get("skills", [])
            experience = data.get("experience", "")
            projects = data.get("projects", [])
            education = data.get("education", {})
            target_grade = data.get("target_grade", "GS-13")
            
            # Build analysis query
            query = f"""
            Analyze this candidate for a {target_grade} Data Scientist (1560) position:
            
            Skills: {', '.join(skills)}
            
            Experience Summary: {experience[:500]}
            
            Education: {education.get('degree', 'Unknown')} in {education.get('field', 'Unknown')}
            
            Projects: {len(projects)} data science projects
            
            Provide:
            1. Skill match assessment
            2. Experience gaps to address
            3. Projects to emphasize
            4. Areas needing more evidence
            5. Recommendations for Merit Hiring essays (without writing them)
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add specific recommendations
                response.data["recommendations"] = {
                    "immediate_actions": [
                        "Review your data science projects for federal relevance",
                        "Identify quantifiable results from your work",
                        "Map your skills to the position requirements"
                    ],
                    "merit_hiring_tips": [
                        "Use STAR method to structure your experiences",
                        "Focus on projects with measurable impact",
                        "Highlight any government or public sector work"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
"""
Fixed Data Scientist Agent with Better Error Handling
"""

from typing import Dict, Any, List, Optional
from langchain.tools import Tool
import json

from app.agents.base_fixed import ImprovedFederalJobAgent, AgentResponse, AgentConfig


class FixedDataScientistAgent(ImprovedFederalJobAgent):
    """
    Fixed data scientist agent with improved reliability
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load simplified, reliable tools"""
        
        tools = [
            Tool(
                name="skill_analyzer",
                func=self._analyze_skills,
                description="Analyze candidate skills against federal requirements"
            ),
            Tool(
                name="experience_checker",
                func=self._check_experience,
                description="Check experience relevance and depth"
            ),
            Tool(
                name="gap_identifier",
                func=self._identify_gaps,
                description="Identify qualification gaps and recommendations"
            )
        ]
        
        return tools
    
    def _get_role_description(self) -> str:
        """Get data scientist role description"""
        return "Federal Data Scientist Career Advisor (Series 1560) - Analyze candidates and provide guidance without writing content"
    
    def _analyze_skills(self, input_data: str) -> str:
        """Simplified skill analysis"""
        try:
            # Handle both string and dict input
            if isinstance(input_data, str):
                try:
                    data = json.loads(input_data)
                except:
                    # If not JSON, treat as simple skill list
                    skills = [s.strip() for s in input_data.split(',')]
                    data = {"skills": skills}
            else:
                data = input_data
            
            candidate_skills = data.get("skills", [])
            
            # Core federal data science skills
            critical_skills = {
                "Python": any("python" in s.lower() for s in candidate_skills),
                "R": any("r" in s.lower() for s in candidate_skills),
                "SQL": any("sql" in s.lower() for s in candidate_skills),
                "Statistics": any(stat in s.lower() for s in candidate_skills for stat in ["stat", "regression", "analysis"]),
                "Machine Learning": any(ml in s.lower() for s in candidate_skills for ml in ["machine", "ml", "model"]),
                "Visualization": any(viz in s.lower() for s in candidate_skills for viz in ["visual", "chart", "plot", "dashboard"])
            }
            
            matched_skills = [skill for skill, present in critical_skills.items() if present]
            missing_skills = [skill for skill, present in critical_skills.items() if not present]
            
            match_percentage = (len(matched_skills) / len(critical_skills)) * 100
            
            return f"Skill Match: {match_percentage:.1f}% | Matched: {', '.join(matched_skills)} | Missing: {', '.join(missing_skills)}"
            
        except Exception as e:
            return f"Skills analysis error: {str(e)}"
    
    def _check_experience(self, input_data: str) -> str:
        """Check experience relevance"""
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            federal_keywords = ["government", "federal", "public", "policy", "compliance", "security"]
            data_keywords = ["data", "analysis", "model", "research", "study", "report"]
            
            federal_relevance = sum(1 for kw in federal_keywords if kw in experience)
            data_relevance = sum(1 for kw in data_keywords if kw in experience)
            
            return f"Federal Relevance: {federal_relevance}/6 | Data Science Relevance: {data_relevance}/6"
            
        except Exception as e:
            return f"Experience check error: {str(e)}"
    
    def _identify_gaps(self, input_data: str) -> str:
        """Identify key gaps and provide recommendations"""
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            gaps = []
            recommendations = []
            
            skills = data.get("skills", [])
            experience = data.get("experience", "")
            
            # Check for common gaps
            if not any("python" in s.lower() for s in skills):
                gaps.append("Python programming")
                recommendations.append("Complete Python for Data Science certification")
            
            if not any("federal" in experience.lower() or "government" in experience.lower()):
                gaps.append("Federal experience")
                recommendations.append("Highlight any government contracting or public sector work")
            
            if not any("security" in experience.lower() or "compliance" in experience.lower()):
                gaps.append("Data governance knowledge")
                recommendations.append("Study federal data governance requirements")
            
            return f"Key Gaps: {', '.join(gaps)} | Recommendations: {'; '.join(recommendations)}"
            
        except Exception as e:
            return f"Gap analysis error: {str(e)}"
    
    def _fallback_analysis(self, query: str, context: Optional[Dict] = None) -> str:
        """Provide fallback analysis when agent fails"""
        
        # Extract basic information from context
        skills = context.get("skills", []) if context else []
        experience = context.get("experience", "") if context else ""
        target_grade = context.get("target_grade", "GS-13") if context else "GS-13"
        
        # Simple analysis without agent
        analysis = f"""
**Data Scientist Position Analysis ({target_grade})**

**Skills Assessment:**
- Listed Skills: {len(skills)} skills provided
- Key Federal Requirements: Python, R, SQL, Statistics, Machine Learning
- Recommendation: Review federal data science job postings for specific requirements

**Experience Review:**
- Experience Length: {len(experience.split())} words of experience described
- Federal Relevance: Look for government, policy, or public sector connections
- Technical Depth: Highlight quantifiable results and methodologies used

**Next Steps:**
1. Map your technical skills to federal requirements
2. Identify projects with measurable impact
3. Research the specific agency's data science needs
4. Prepare examples using STAR method for essays

**Merit Hiring Guidance:**
- Focus on analytical thinking and problem-solving
- Emphasize collaborative work and communication skills
- Highlight any work with sensitive or regulated data
- Show continuous learning and adaptation to new technologies

Note: This is a simplified analysis. For detailed guidance, ensure the agent service is properly configured.
"""
        
        return analysis.strip()
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Main analysis method for data scientist candidates
        """
        
        # Build analysis query
        skills = data.get("skills", [])
        experience = data.get("experience", "")
        target_grade = data.get("target_grade", "GS-13")
        
        query = f"""
        Analyze this candidate for a {target_grade} Data Scientist position:
        
        Skills: {', '.join(skills) if skills else 'None provided'}
        Experience: {experience[:200] if experience else 'None provided'}
        
        Provide skill match assessment, experience evaluation, and gap analysis.
        """
        
        # Use the improved processing method
        response = await self.process_simple(query, data)
        
        # Add structured recommendations
        if response.success and response.data:
            response.data["structured_guidance"] = {
                "immediate_actions": [
                    "Review federal data science job announcements",
                    "Map your skills to position requirements",
                    "Identify quantifiable project results"
                ],
                "skill_development": [
                    "Python for federal data analysis",
                    "Statistical modeling and validation",
                    "Federal data governance principles"
                ],
                "application_tips": [
                    "Use STAR method in essay responses",
                    "Highlight measurable project impacts",
                    "Connect experience to federal mission"
                ]
            }
        
        return response


# Factory function for easy creation
def create_fixed_data_scientist_agent(user_id: str) -> FixedDataScientistAgent:
    """Create a fixed data scientist agent with optimal configuration"""
    
    config = AgentConfig(
        role="data_scientist",
        user_id=user_id,
        model="gptFREE",
        temperature=0.1,  # Low temperature for consistency
        max_tokens=1000,  # Reasonable limit
        timeout=30,       # Reasonable timeout
        max_iterations=2, # Prevent infinite loops
        enable_memory=False  # Disable for stability
    )
    
    return FixedDataScientistAgent(config)
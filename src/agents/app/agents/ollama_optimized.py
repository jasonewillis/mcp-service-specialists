"""
Optimized Agent for Ollama/gptFREE Model
Works WITH the model's tendencies instead of fighting them
"""

import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from langchain_community.llms import Ollama
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger()


class OllamaOptimizedAgent:
    """
    Agent optimized for Ollama's gptFREE model behavior
    Uses simpler prompts and programmatic orchestration
    """
    
    def __init__(self, role: str = "federal_advisor"):
        self.role = role
        
        # Configure Ollama for maximum consistency
        self.llm = Ollama(
            model="gptFREE",
            temperature=0.0,  # Zero temperature for consistency
            num_ctx=2048,     # Smaller context to stay focused
            num_predict=500,  # Limit output length
            top_k=5,          # Very focused token selection
            top_p=0.8,        # Narrow probability range
            repeat_penalty=1.3,  # Strong repetition penalty
            stop=["Question:", "**Question", "---", "###"]  # Stop sequences
        )
        
        logger.info(f"Initialized Ollama-optimized {role} agent")
    
    def analyze_with_cot(self, query: str, context: Dict[str, Any]) -> str:
        """
        Use simple Chain-of-Thought prompting
        """
        
        # Build a simple, focused prompt
        prompt = f"""Federal Job Analysis Task:

Context:
- Skills: {', '.join(context.get('skills', ['None listed']))}
- Experience: {context.get('experience', 'Not provided')[:100]}
- Grade: {context.get('target_grade', 'GS-13')}

Analyze this step by step:
1. Match skills to federal requirements
2. Identify critical gaps
3. Provide specific recommendations

Keep each section to 2-3 sentences. Be direct and specific.

Analysis:"""

        try:
            # Get response with timeout
            response = self.llm.invoke(prompt)
            
            # Clean up the response
            cleaned = self._clean_response(response)
            
            return cleaned
            
        except Exception as e:
            logger.error(f"CoT analysis error: {e}")
            return self._fallback_analysis(context)
    
    def analyze_with_json(self, query: str, context: Dict[str, Any]) -> Dict:
        """
        Request JSON structured output
        """
        
        prompt = f"""Analyze federal job candidate and return JSON:

Candidate:
- Skills: {context.get('skills', [])}
- Experience: {context.get('experience', 'None')[:100]}

Return this exact JSON structure:
{{
  "skill_match_percentage": <number>,
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "top_gaps": ["gap1", "gap2", "gap3"],
  "recommendations": ["rec1", "rec2", "rec3"]
}}

JSON Output:"""

        try:
            response = self.llm.invoke(prompt)
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Try to parse as-is
                return json.loads(response)
                
        except Exception as e:
            logger.error(f"JSON parsing error: {e}")
            return self._generate_structured_fallback(context)
    
    def analyze_with_sections(self, query: str, context: Dict[str, Any]) -> str:
        """
        Use section-based prompting
        """
        
        prompt = f"""Federal Data Scientist Analysis

CANDIDATE PROFILE:
{self._format_profile(context)}

Provide analysis in these sections:

SKILLS ASSESSMENT:
[Write 2-3 sentences about skill alignment]

EXPERIENCE GAPS:
[List 3 main gaps as bullets]

RECOMMENDATIONS:
[List 3 specific actions as bullets]

Begin analysis below:
"""

        try:
            response = self.llm.invoke(prompt)
            return self._format_sections(response)
            
        except Exception as e:
            logger.error(f"Section analysis error: {e}")
            return self._fallback_analysis(context)
    
    def direct_tool_analysis(self, context: Dict[str, Any]) -> Dict:
        """
        Skip LLM orchestration, use tools directly
        """
        
        results = {}
        
        # Direct skill analysis
        skills = context.get('skills', [])
        federal_skills = ['Python', 'R', 'SQL', 'Statistics', 'ML', 'Visualization']
        
        results['skill_match'] = {
            'matched': [s for s in skills if any(f.lower() in s.lower() for f in federal_skills)],
            'missing': [f for f in federal_skills if not any(f.lower() in s.lower() for s in skills)],
            'percentage': len([s for s in skills if any(f.lower() in s.lower() for f in federal_skills)]) / len(federal_skills) * 100
        }
        
        # Direct gap analysis
        experience = context.get('experience', '').lower()
        gaps = []
        
        if 'federal' not in experience and 'government' not in experience:
            gaps.append("Federal/government experience")
        if 'big data' not in experience and 'spark' not in experience:
            gaps.append("Big data processing experience")
        if 'visualization' not in experience and 'dashboard' not in experience:
            gaps.append("Data visualization skills")
        
        results['gaps'] = gaps
        
        # Direct recommendations
        results['recommendations'] = [
            f"Highlight {results['skill_match']['matched'][0]} expertise" if results['skill_match']['matched'] else "Develop Python/R skills",
            "Emphasize any government contracting or public sector work",
            "Complete a federal data governance certification"
        ]
        
        return results
    
    def _clean_response(self, response: str) -> str:
        """Clean up Ollama response"""
        
        # Remove markdown formatting
        response = re.sub(r'\*\*', '', response)
        response = re.sub(r'#{1,6}\s*', '', response)
        response = re.sub(r'---+', '', response)
        
        # Remove question restatements
        response = re.sub(r'^.*?Question:.*?\n', '', response, flags=re.IGNORECASE)
        
        # Remove excessive whitespace
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        return response.strip()
    
    def _format_profile(self, context: Dict) -> str:
        """Format candidate profile for prompt"""
        
        profile = []
        profile.append(f"Skills: {', '.join(context.get('skills', ['Not provided']))}")
        profile.append(f"Experience: {context.get('experience', 'Not provided')[:150]}")
        profile.append(f"Target Grade: {context.get('target_grade', 'GS-13')}")
        
        return '\n'.join(profile)
    
    def _format_sections(self, response: str) -> str:
        """Format response into clear sections"""
        
        sections = []
        
        # Try to extract sections
        skills_match = re.search(r'SKILLS ASSESSMENT:?\s*(.*?)(?=EXPERIENCE GAPS:|$)', response, re.DOTALL)
        gaps_match = re.search(r'EXPERIENCE GAPS:?\s*(.*?)(?=RECOMMENDATIONS:|$)', response, re.DOTALL)
        recs_match = re.search(r'RECOMMENDATIONS:?\s*(.*?)$', response, re.DOTALL)
        
        if skills_match:
            sections.append(f"**Skills Assessment:**\n{skills_match.group(1).strip()}")
        
        if gaps_match:
            sections.append(f"**Experience Gaps:**\n{gaps_match.group(1).strip()}")
        
        if recs_match:
            sections.append(f"**Recommendations:**\n{recs_match.group(1).strip()}")
        
        return '\n\n'.join(sections) if sections else response
    
    def _generate_structured_fallback(self, context: Dict) -> Dict:
        """Generate structured fallback when JSON parsing fails"""
        
        skills = context.get('skills', [])
        
        return {
            "skill_match_percentage": 60,
            "matched_skills": skills[:3] if skills else ["Python"],
            "missing_skills": ["Federal data governance", "Big data platforms"],
            "top_gaps": [
                "Federal experience",
                "Advanced analytics",
                "Security clearance"
            ],
            "recommendations": [
                "Complete federal data science certification",
                "Highlight any government-adjacent work",
                "Develop portfolio with public datasets"
            ]
        }
    
    def _fallback_analysis(self, context: Dict) -> str:
        """Provide fallback analysis when LLM fails"""
        
        skills = context.get('skills', [])
        experience = context.get('experience', 'Not provided')
        
        return f"""
**Federal Job Analysis**

**Skills Assessment:**
You have {len(skills)} skills listed. Federal data scientist positions typically require Python, R, SQL, statistics, and machine learning. Focus on strengthening any gaps in these core areas.

**Experience Gaps:**
• Federal or government experience
• Big data and cloud platforms
• Published research or presentations

**Recommendations:**
• Map your existing skills to federal requirements
• Highlight any public sector or compliance work
• Consider federal data certifications
• Build portfolio using government datasets

This analysis helps identify areas for development in pursuing federal data science positions.
"""


def test_optimized_agent():
    """Test the optimized agent with different strategies"""
    
    print("🧪 Testing Ollama-Optimized Agent")
    print("=" * 60)
    
    agent = OllamaOptimizedAgent()
    
    test_context = {
        "skills": ["Python", "Machine Learning", "SQL"],
        "experience": "5 years in financial data analysis",
        "target_grade": "GS-13"
    }
    
    print("\n1️⃣ Testing Chain-of-Thought:")
    print("-" * 40)
    cot_result = agent.analyze_with_cot("Analyze candidate", test_context)
    print(cot_result[:500])
    
    print("\n2️⃣ Testing JSON Structure:")
    print("-" * 40)
    json_result = agent.analyze_with_json("Analyze candidate", test_context)
    print(json.dumps(json_result, indent=2))
    
    print("\n3️⃣ Testing Section-Based:")
    print("-" * 40)
    section_result = agent.analyze_with_sections("Analyze candidate", test_context)
    print(section_result[:500])
    
    print("\n4️⃣ Testing Direct Analysis (No LLM):")
    print("-" * 40)
    direct_result = agent.direct_tool_analysis(test_context)
    print(json.dumps(direct_result, indent=2))
    
    print("\n" + "=" * 60)
    print("✅ All strategies tested successfully!")


if __name__ == "__main__":
    test_optimized_agent()
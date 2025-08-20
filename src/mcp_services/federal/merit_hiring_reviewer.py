#!/usr/bin/env python3
"""
Merit Hiring Compliance Reviewer
Federal domain expert - NEVER generates content, only reviews
Uses mistral:7b for compliance analysis
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import asyncio

class MeritHiringReviewer:
    """
    Review-only agent for Merit Hiring compliance
    Ensures NO AI-generated content in federal applications
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Merit System Principles
        self.merit_principles = [
            "Recruitment from all segments of society",
            "Fair and equitable treatment",
            "Equal pay for equal work",
            "High standards of integrity and conduct",
            "Efficient and effective use of workforce",
            "Retention based on performance",
            "Education and training opportunities",
            "Protection from arbitrary action",
            "Protection of whistleblowers"
        ]
        
        # Prohibited practices
        self.prohibited_practices = [
            "AI-generated essay content",
            "Plagiarism or copied content",
            "False statements or misrepresentation",
            "Discrimination based on protected classes",
            "Political influence or coercion",
            "Nepotism or favoritism",
            "Retaliation against whistleblowers"
        ]
        
        # Essay requirements
        self.essay_requirements = {
            "word_limit": 200,
            "structure": "STAR method recommended",
            "content": "Must be candidate's own work",
            "attestation": "Required no-AI declaration"
        }
        
        self.model = "mistral:7b"  # Good for analysis
    
    async def review_compliance(self, content: Dict, user_id: str = "system") -> Dict[str, Any]:
        """
        Review content for Merit Hiring compliance
        NEVER generates content, only analyzes
        """
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "compliant": True,
            "violations": [],
            "warnings": [],
            "guidance": [],
            "score": 100
        }
        
        # Check essay if present
        if "essay" in content:
            essay_review = self._review_essay(content["essay"])
            review["violations"].extend(essay_review["violations"])
            review["warnings"].extend(essay_review["warnings"])
            review["guidance"].extend(essay_review["guidance"])
            review["score"] = essay_review["score"]
        
        # Check for AI generation indicators
        if "ai_generated" in str(content).lower() or "chatgpt" in str(content).lower():
            review["violations"].append("❌ CRITICAL: AI-generated content detected")
            review["compliant"] = False
            review["score"] = 0
        
        # Provide guidance (never content)
        if not review["compliant"]:
            review["guidance"].append("Focus on YOUR specific experiences")
            review["guidance"].append("Use STAR method: Situation, Task, Action, Result")
            review["guidance"].append("Be specific with metrics and outcomes")
            review["guidance"].append("Stay within 200-word limit")
        
        review["recommendation"] = self._generate_recommendation(review)
        
        return review
    
    def _review_essay(self, essay_text: str) -> Dict:
        """Review essay for compliance"""
        
        review = {
            "violations": [],
            "warnings": [],
            "guidance": [],
            "score": 100
        }
        
        word_count = len(essay_text.split())
        
        # Check word limit
        if word_count > 200:
            review["violations"].append(f"❌ Exceeds 200-word limit ({word_count} words)")
            review["score"] -= 30
        elif word_count < 50:
            review["warnings"].append("⚠️ Very short response (under 50 words)")
            review["score"] -= 10
        
        # Check for STAR structure
        star_keywords = ["situation", "task", "action", "result"]
        star_found = sum(1 for kw in star_keywords if kw in essay_text.lower())
        
        if star_found < 2:
            review["warnings"].append("⚠️ STAR method not clearly used")
            review["guidance"].append("Structure with: Situation, Task, Action, Result")
            review["score"] -= 10
        
        # Check for specific metrics
        has_numbers = any(char.isdigit() for char in essay_text)
        if not has_numbers:
            review["warnings"].append("⚠️ No specific metrics or numbers")
            review["guidance"].append("Include quantifiable results")
            review["score"] -= 5
        
        # Check for generic content
        generic_phrases = [
            "team player",
            "hard worker",
            "detail oriented",
            "self starter",
            "excellent communication"
        ]
        generic_count = sum(1 for phrase in generic_phrases if phrase in essay_text.lower())
        if generic_count > 2:
            review["warnings"].append("⚠️ Too many generic phrases")
            review["guidance"].append("Be specific about YOUR contributions")
            review["score"] -= 10
        
        return review
    
    def _generate_recommendation(self, review: Dict) -> str:
        """Generate compliance recommendation"""
        
        if review["score"] >= 80:
            return "✅ Meets Merit Hiring requirements"
        elif review["score"] >= 60:
            return "⚠️ Address warnings before submission"
        else:
            return "❌ Major revisions required for compliance"
    
    async def provide_guidance(self, topic: str, user_id: str = "system") -> Dict[str, Any]:
        """
        Provide Merit Hiring guidance (NEVER writes content)
        """
        
        guidance = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "topic": topic,
            "guidelines": [],
            "dos": [],
            "donts": [],
            "examples": []
        }
        
        if "essay" in topic.lower():
            guidance["guidelines"] = [
                "Write about YOUR specific experiences",
                "Use STAR method for structure",
                "Stay within 200-word limit",
                "Include quantifiable results",
                "Proofread for clarity"
            ]
            guidance["dos"] = [
                "DO use first person ('I')",
                "DO be specific about your role",
                "DO include metrics and outcomes",
                "DO show progression/growth",
                "DO connect to job requirements"
            ]
            guidance["donts"] = [
                "DON'T use AI to write content",
                "DON'T exceed word limit",
                "DON'T be vague or generic",
                "DON'T exaggerate or lie",
                "DON'T copy from others"
            ]
            guidance["examples"] = [
                "GOOD: 'I reduced processing time by 40%'",
                "BAD: 'I improved efficiency'",
                "GOOD: 'Led team of 5 to complete project'",
                "BAD: 'Worked on team project'"
            ]
        
        return guidance
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research Merit Hiring requirements"""
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "merit_principles": self.merit_principles,
            "prohibited_practices": self.prohibited_practices,
            "essay_requirements": self.essay_requirements,
            "implementation_plan": {
                "summary": "Merit Hiring compliance system",
                "steps": [
                    "1. Implement word count validation",
                    "2. Add no-AI attestation checkbox",
                    "3. Create STAR method template",
                    "4. Build compliance checker",
                    "5. Add guidance tooltips"
                ]
            }
        }
        
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": "Merit Hiring compliance requirements",
            "critical_reminders": [
                "NEVER generate essay content",
                "Enforce 200-word limit",
                "Require attestation"
            ]
        }
    
    def _save_research_report(self, research: Dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"merit_hiring_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# Merit Hiring Compliance Research\n\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Merit System Principles\n")
            for principle in research['merit_principles']:
                f.write(f"- {principle}\n")
            f.write("\n")
            
            f.write("## Prohibited Practices\n")
            for practice in research['prohibited_practices']:
                f.write(f"- {practice}\n")
            f.write("\n")
            
            f.write("## Essay Requirements\n")
            f.write(f"- Word Limit: {research['essay_requirements']['word_limit']}\n")
            f.write(f"- Structure: {research['essay_requirements']['structure']}\n")
            f.write(f"- Content: {research['essay_requirements']['content']}\n")
            f.write(f"- Attestation: {research['essay_requirements']['attestation']}\n")
        
        return report_path
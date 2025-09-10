"""
Essay Guidance Agent - Merit Hiring Compliance
Provides guidance without writing content - fully compliant with Merit Hiring rules

## Claude Code Best Practices

### How to Use This Agent Effectively

**CRITICAL COMPLIANCE WARNING:**
This agent NEVER writes content. It only analyzes structure and points to existing experience.
Any attempt to have it write, draft, or suggest specific wording violates federal regulations.

**Initial Context Setup:**
1. Use Read tool to examine candidate's full background first
2. Identify which of the 4 Merit Hiring essays is being worked on
3. Have candidate's actual draft ready for structural analysis only
4. Gather candidate's relevant experience for each essay topic

**Effective Prompting Patterns:**
```
"Analyze structural compliance for Merit Hiring Essay #2:
- Topic: Government Efficiency 
- Draft: [paste their written draft]
- Experience: [list relevant efficiency/improvement projects]
- Word count check needed
- STAR structure validation required"
```

**Best Workflow (STRUCTURE ONLY):**
1. **Word Count** → Check 200-word limit compliance
2. **STAR Analysis** → Verify Situation/Task/Action/Result structure
3. **Topic Coverage** → Ensure focus areas are addressed
4. **Experience Mapping** → Point to relevant background (never write)
5. **Compliance Check** → Verify originality indicators

### Integration with Other Agents

**Workflow Chains:**
- Data Scientist/IT/etc. Agent → Essay Guidance Agent (experience identification)
- Essay Guidance Agent → Resume Compression Agent (consistent messaging)
- NEVER chains that involve content creation

**Handoff Points:**
- Receive experience analysis from technical agents
- Point to specific experiences for essay topics
- Validate technical examples are properly structured

### Federal Merit Hiring Essays

**Essay #1: Constitutional Principles**
- Focus: Constitution, limited government principles
- Experience to highlight: Government work, civic involvement, constitutional awareness
- Structure: Personal commitment → Understanding → Application

**Essay #2: Government Efficiency**
- Focus: Efficiency, effectiveness, improvement, innovation  
- Experience to highlight: Process improvement, cost savings, innovation projects
- Structure: Problem identification → Solution implementation → Results

**Essay #3: Presidential Priorities**
- Focus: Policy priorities, implementation, advancement
- Experience to highlight: Policy work, current administration priorities
- Structure: Understanding → Alignment → Contribution

**Essay #4: Work Ethic**
- Focus: Work ethic, excellence, commitment to service
- Experience to highlight: Dedication examples, quality work, service orientation
- Structure: Personal values → Demonstration → Government application

### CRITICAL Compliance Requirements

**NEVER DO:**
- Write any portion of essays
- Suggest specific wording or phrases
- Provide example sentences
- Edit or revise content
- Generate ideas for content

**ONLY DO:**
- Count words (200 max)
- Check STAR structure presence
- Identify missing focus areas
- Point to candidate's existing experience
- Verify originality indicators

### Test-Driven Usage Examples

**Example 1: Structure Analysis**
```python
test_data = {
    "essay_number": 2,
    "essay_text": "[candidate's draft - 185 words]",
    "experience": "Led efficiency project saving 30% processing time"
}
# Expected: Word count OK, check STAR elements, point to efficiency experience
```

**Example 2: Experience Mapping**
```python
test_data = {
    "essay_number": 1,
    "essay_text": "",  # No draft yet
    "experience": "Veteran, oath of office, government service"
}
# Expected: Point to military/government experience for constitutional topic
```

### Checklist-Based Compliance Workflow

**Pre-Analysis Safety Check:**
- [ ] Candidate has written their own draft
- [ ] Analysis will be structural only
- [ ] No content suggestions will be made
- [ ] Experience pointing only (not writing)

**Analysis Checklist:**
- [ ] Word count verified (≤200 words)
- [ ] STAR structure elements present
- [ ] Essay topic focus areas covered
- [ ] Relevant experience identified from background
- [ ] Originality indicators checked

**Post-Analysis Compliance:**
- [ ] No content was written or suggested
- [ ] Only structural feedback provided
- [ ] Experience mapping completed
- [ ] Candidate must do all writing

### Common Pitfalls to Avoid

1. **NEVER write content** - Federal violation, agent must refuse
2. **Don't suggest specific wording** - Point to experience only
3. **Avoid example phrases** - No language suggestions allowed
4. **Don't edit drafts** - Analysis only, no revisions
5. **No idea generation** - Work with existing experience only

### Visual Iteration Methods

**Structural Analysis Dashboard:**
- Word count tracker (visual meter to 200)
- STAR element presence indicators
- Topic coverage checklist
- Experience relevance mapping

### Integration with CLAUDE.md Principles

- **No assumptions:** Always verify essay number and topic
- **Solo developer focus:** Candidate writes alone, agent analyzes only
- **Bootstrap approach:** Use candidate's actual experience, not hypotheticals
- **Practical focus:** Point to real examples from their background
- **Compliance first:** Federal regulations override all other considerations

### Emergency Compliance Procedures

**If asked to write content:**
1. Immediately refuse and explain violation
2. Redirect to structural analysis only
3. Emphasize candidate must write everything
4. Document refusal for compliance

**If content accidentally suggested:**
1. Immediately retract and apologize
2. Clarify violation of federal rules
3. Emphasize need for original work
4. Reset to compliance mode

### Optimization Tips

1. **Preparation:** Have complete candidate background before analysis
2. **Focus:** Stick to structure, word count, and experience mapping
3. **Boundaries:** Never cross from analysis to content creation
4. **Documentation:** Always emphasize compliance requirements

### Success Metrics

- **Compliance:** 100% content-writing refusal rate
- **Structure:** Effective STAR and word count analysis  
- **Mapping:** Accurate experience-to-topic alignment
- **Boundaries:** Clear separation of analysis vs. creation
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from ..base import FederalJobAgent, AgentResponse


class EssayGuidanceAgent(FederalJobAgent):
    """
    Guides candidates through Merit Hiring essays WITHOUT writing content
    Ensures 100% compliance with federal Merit Hiring requirements
    """
    
    # Official Merit Hiring essay questions
    ESSAY_QUESTIONS = {
        1: {
            "title": "Constitutional Principles",
            "question": "Describe your understanding of and commitment to the Constitution and the principles of limited government.",
            "focus": ["Constitution", "limited government", "federal principles"]
        },
        2: {
            "title": "Government Efficiency",
            "question": "Describe your understanding of how to make government more efficient and effective.",
            "focus": ["efficiency", "effectiveness", "improvement", "innovation"]
        },
        3: {
            "title": "Presidential Priorities",
            "question": "Describe your understanding of the President's policy priorities and how you would advance them in this role.",
            "focus": ["policy priorities", "implementation", "advancement", "alignment"]
        },
        4: {
            "title": "Work Ethic",
            "question": "Describe your work ethic and commitment to excellence in federal service.",
            "focus": ["work ethic", "excellence", "commitment", "service"]
        }
    }
    
    def _load_tools(self) -> List[Tool]:
        """Load essay guidance tools"""
        
        tools = [
            Tool(
                name="star_validator",
                func=self._validate_star_structure,
                description="Check if text follows STAR method (structure only)"
            ),
            Tool(
                name="word_counter",
                func=self._count_words,
                description="Count words and check against 200-word limit"
            ),
            Tool(
                name="experience_identifier",
                func=self._identify_relevant_experience,
                description="Point to relevant experiences from candidate's background"
            ),
            Tool(
                name="compliance_checker",
                func=self._check_compliance,
                description="Ensure guidance stays compliant with Merit Hiring rules"
            ),
            Tool(
                name="focus_analyzer",
                func=self._analyze_focus,
                description="Check if response addresses the question focus areas"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get essay guidance specific prompt template"""
        
        return """You are a Merit Hiring Essay Guidance Counselor.
        
        CRITICAL COMPLIANCE REQUIREMENTS:
        - You must NEVER write, draft, or compose essay content
        - You must NEVER provide example sentences or paragraphs
        - You must NEVER suggest specific wording or phrasing
        - You can ONLY analyze structure and point to user's experiences
        
        Your Role:
        1. Analyze essay structure (not content)
        2. Count words and warn about limits
        3. Check if STAR method is being used
        4. Point to relevant experiences from their background
        5. Identify if key focus areas are addressed
        
        Merit Hiring Requirements:
        - 200 words maximum per essay (strict limit)
        - Must use STAR method (Situation, Task, Action, Result)
        - Must be original work by candidate
        - Must directly answer the question
        
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

        REMEMBER: Any attempt to write content violates federal regulations.
        Only provide structural guidance and point to their experiences.

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""
    
    def _validate_star_structure(self, text: str) -> str:
        """Validate STAR structure without reading content"""
        
        try:
            if not text:
                return json.dumps({
                    "has_structure": False,
                    "feedback": "No text provided to analyze"
                })
            
            text_lower = text.lower()
            word_count = len(text.split())
            
            # Look for structural indicators only
            structure_indicators = {
                "situation": ["situation", "context", "background", "when", "where"],
                "task": ["task", "objective", "goal", "responsibility", "charged with"],
                "action": ["action", "did", "implemented", "developed", "led", "created"],
                "result": ["result", "outcome", "achieved", "success", "impact", "improved"]
            }
            
            found_elements = {}
            for element, keywords in structure_indicators.items():
                found_elements[element] = any(kw in text_lower for kw in keywords)
            
            # Rough distribution check (each element should be ~25% of text)
            expected_words_per_element = word_count / 4
            
            feedback = {
                "has_structure": all(found_elements.values()),
                "elements_found": found_elements,
                "structural_balance": "balanced" if 40 <= word_count <= 60 else "check distribution",
                "recommendation": self._get_structure_recommendation(found_elements)
            }
            
            return json.dumps(feedback)
            
        except Exception as e:
            return f"Error validating structure: {str(e)}"
    
    def _get_structure_recommendation(self, elements: Dict[str, bool]) -> str:
        """Provide structural recommendations"""
        
        missing = [k for k, v in elements.items() if not v]
        
        if not missing:
            return "All STAR elements appear present"
        elif len(missing) == 1:
            return f"Consider adding {missing[0]} element"
        else:
            return f"Missing elements: {', '.join(missing)}"
    
    def _count_words(self, text: str) -> str:
        """Count words and check limit"""
        
        try:
            if not text:
                return json.dumps({
                    "word_count": 0,
                    "remaining": 200,
                    "status": "empty"
                })
            
            word_count = len(text.split())
            remaining = 200 - word_count
            
            if word_count > 200:
                status = "over_limit"
                message = f"OVER LIMIT by {word_count - 200} words"
            elif word_count > 195:
                status = "near_limit"
                message = "Very close to limit - be careful"
            elif word_count > 180:
                status = "approaching_limit"
                message = "Approaching limit"
            elif word_count < 100:
                status = "too_short"
                message = "May be too brief to fully answer"
            else:
                status = "good"
                message = "Good length"
            
            return json.dumps({
                "word_count": word_count,
                "remaining": remaining,
                "status": status,
                "message": message
            })
            
        except Exception as e:
            return f"Error counting words: {str(e)}"
    
    def _identify_relevant_experience(self, input_data: str) -> str:
        """Identify relevant experiences from candidate's background"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            essay_number = data.get("essay_number", 1)
            candidate_experience = data.get("experience", "")
            
            # Get focus areas for this essay
            essay_info = self.ESSAY_QUESTIONS.get(essay_number, self.ESSAY_QUESTIONS[1])
            focus_areas = essay_info["focus"]
            
            # Find relevant experiences (without writing about them)
            relevant_experiences = []
            
            for focus in focus_areas:
                # Check if candidate has related experience
                if focus.lower() in candidate_experience.lower():
                    relevant_experiences.append({
                        "focus_area": focus,
                        "found": True,
                        "guidance": f"You have experience related to {focus} - consider using it"
                    })
                else:
                    relevant_experiences.append({
                        "focus_area": focus,
                        "found": False,
                        "guidance": f"Think about any experience that relates to {focus}"
                    })
            
            return json.dumps({
                "essay_topic": essay_info["title"],
                "relevant_experiences": relevant_experiences,
                "general_guidance": "Draw from your actual experiences, not hypotheticals"
            })
            
        except Exception as e:
            return f"Error identifying experiences: {str(e)}"
    
    def _check_compliance(self, text: str) -> str:
        """Ensure the text appears to be original work"""
        
        try:
            if not text:
                return json.dumps({
                    "compliant": True,
                    "notes": "No text to check"
                })
            
            # Check for signs of AI generation (patterns to avoid)
            ai_patterns = [
                "as an ai", "language model", "i cannot", "i don't have personal",
                "however, i can", "it's important to note", "in conclusion"
            ]
            
            text_lower = text.lower()
            found_patterns = [p for p in ai_patterns if p in text_lower]
            
            # Check for overly formal or generic language
            generic_phrases = [
                "commitment to excellence", "dedicated professional",
                "proven track record", "results-driven", "team player"
            ]
            
            generic_count = sum(1 for phrase in generic_phrases if phrase in text_lower)
            
            compliance_assessment = {
                "appears_original": len(found_patterns) == 0,
                "ai_patterns_found": found_patterns,
                "generic_phrase_count": generic_count,
                "recommendation": self._get_compliance_recommendation(found_patterns, generic_count)
            }
            
            return json.dumps(compliance_assessment)
            
        except Exception as e:
            return f"Error checking compliance: {str(e)}"
    
    def _get_compliance_recommendation(self, patterns: List[str], generic_count: int) -> str:
        """Provide compliance recommendations"""
        
        if patterns:
            return "Text contains patterns suggesting non-original work"
        elif generic_count > 3:
            return "Consider using more specific, personal examples"
        else:
            return "Appears to be original work"
    
    def _analyze_focus(self, input_data: str) -> str:
        """Analyze if response addresses question focus areas"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            text = data.get("text", "")
            essay_number = data.get("essay_number", 1)
            
            essay_info = self.ESSAY_QUESTIONS.get(essay_number, self.ESSAY_QUESTIONS[1])
            focus_areas = essay_info["focus"]
            
            text_lower = text.lower()
            
            addressed_areas = []
            missing_areas = []
            
            for focus in focus_areas:
                if focus.lower() in text_lower:
                    addressed_areas.append(focus)
                else:
                    # Check for synonyms/related terms
                    related_found = False
                    if focus == "Constitution" and any(term in text_lower for term in ["constitutional", "founding"]):
                        related_found = True
                    elif focus == "efficiency" and any(term in text_lower for term in ["efficient", "streamline", "optimize"]):
                        related_found = True
                    
                    if related_found:
                        addressed_areas.append(f"{focus} (related)")
                    else:
                        missing_areas.append(focus)
            
            return json.dumps({
                "question": essay_info["title"],
                "addressed": addressed_areas,
                "missing": missing_areas,
                "coverage": len(addressed_areas) / len(focus_areas) * 100
            })
            
        except Exception as e:
            return f"Error analyzing focus: {str(e)}"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze essay draft for Merit Hiring compliance
        """
        
        try:
            essay_text = data.get("essay_text", "")
            essay_number = data.get("essay_number", 1)
            candidate_experience = data.get("experience", "")
            
            if not essay_text:
                return AgentResponse(
                    success=True,
                    message="Ready to provide guidance",
                    data={
                        "guidance": {
                            "essay_question": self.ESSAY_QUESTIONS[essay_number]["question"],
                            "requirements": {
                                "word_limit": "200 words maximum",
                                "structure": "Use STAR method",
                                "content": "Must be your original work"
                            },
                            "focus_areas": self.ESSAY_QUESTIONS[essay_number]["focus"]
                        }
                    }
                )
            
            # Build analysis query
            query = f"""
            Analyze this Merit Hiring essay draft for structural compliance only:
            
            Essay #{essay_number}: {self.ESSAY_QUESTIONS[essay_number]['title']}
            
            Check:
            1. Word count (200 max)
            2. STAR structure presence
            3. Focus area coverage
            4. Originality indicators
            
            DO NOT write or suggest content. Only analyze structure.
            """
            
            # Process with agent
            context = {
                "essay_text": essay_text,
                "essay_number": essay_number,
                "experience": candidate_experience
            }
            
            response = await self.process(query, context)
            
            if response.success:
                # Add compliance reminder
                response.data["compliance_reminder"] = {
                    "critical": "You must write this essay yourself",
                    "prohibited": [
                        "AI cannot write any portion",
                        "AI cannot suggest sentences",
                        "AI cannot edit your content"
                    ],
                    "allowed": [
                        "Structure analysis",
                        "Word counting",
                        "Pointing to your experiences"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
"""
Resume Compression Agent - Federal Resume Optimization
Helps compress resumes to meet federal 2-page requirements

## Claude Code Best Practices

### How to Use This Agent Effectively

**CRITICAL LIMITATION:**
This agent NEVER writes or rewrites resume content. It only analyzes and suggests compression strategies.

**Initial Context Setup:**
1. Use Read tool to examine current resume (PDF/text conversion needed)
2. Get accurate page count and formatting details
3. Identify target position/series for relevance assessment
4. Gather information about must-keep federal requirements
5. Calculate percentage compression needed

**Effective Prompting Patterns:**
```
"Analyze 4-page federal resume for compression to 2 pages:
- Current: 4 pages, ~2,400 words
- Target: GS-13 IT Specialist (2210)
- Must keep: All federal job details, grades, hours/week
- Focus: Remove redundancy, optimize format, prioritize content
- Timeline: Need compressed version in 2 weeks"
```

**Best Workflow:**
1. **Length Analysis** → Calculate compression percentage needed
2. **Redundancy Check** → Identify repetitive content
3. **Impact Evaluation** → Rank accomplishments by relevance
4. **Format Optimization** → Suggest space-saving formatting
5. **Priority Ranking** → Identify what to keep vs. remove

### Integration with Other Agents

**Workflow Chains:**
- Technical Agent → Resume Compression Agent (content priority guidance)
- Resume Compression Agent → Essay Guidance Agent (consistent messaging)
- Analytics Intelligence → Resume Compression Agent (market priorities)

**Handoff Points:**
- Receive experience prioritization from technical agents
- Share format recommendations with application preparation
- Coordinate federal requirements across all documents

### Federal Resume Requirements (MUST KEEP)

**For Federal Positions:**
- Job title, series, grade for all federal jobs
- Complete dates (month/year start and end)
- Hours per week for each position
- Supervisor name and contact info (or "contact upon request")
- Salary information (for current federal employees)

**For Private Sector:**
- Company name and general location
- Job title and key responsibilities
- Employment dates and duration
- Major accomplishments with metrics

### Test-Driven Usage Examples

**Example 1: Severe Compression (5→2 pages)**
```python
test_data = {
    "current_pages": 5,
    "word_count": 3000,
    "target_position": "GS-12 Data Scientist",
    "federal_jobs": 2,
    "private_jobs": 6,
    "target_compression": "60%"
}
# Expected: Major restructuring needed, focus on recent/relevant experience
```

**Example 2: Moderate Compression (3→2 pages)**
```python
test_data = {
    "current_pages": 3,
    "word_count": 1800,
    "target_position": "GS-13 DBA",
    "redundancy_issues": ["repeated action verbs", "similar job descriptions"],
    "target_compression": "33%"
}
# Expected: Format optimization and redundancy removal sufficient
```

### Visual Iteration Methods

**Compression Analysis Dashboard:**
- Page-by-page content breakdown
- Word count reduction targets
- Content priority matrix (keep/condense/remove)
- Format optimization impact visualization

### Checklist-Based Workflows

**Pre-Compression Analysis:**
- [ ] Current page count and word count documented
- [ ] Federal requirements identified and marked as must-keep
- [ ] Target position relevance criteria established
- [ ] Redundancy patterns identified
- [ ] Format optimization opportunities noted

**Compression Strategy Checklist:**
- [ ] Federal compliance maintained (grades, dates, hours)
- [ ] Most relevant experience prioritized
- [ ] Redundant language eliminated
- [ ] Format optimized for space efficiency
- [ ] 2-page limit achieved without losing critical information

### Common Compression Strategies

**Content Strategies:**
1. **Time-based filtering:** Keep last 10-15 years detailed, summarize older
2. **Relevance ranking:** Prioritize target-position-relevant experience
3. **Accomplishment focus:** Remove generic duties, keep specific achievements
4. **Federal priority:** Detail federal experience, summarize private sector

**Format Strategies:**
1. **Margin optimization:** 0.5" margins (minimum allowable)
2. **Font efficiency:** 10-11pt font, single spacing
3. **Bullet efficiency:** Use bullets vs. paragraphs
4. **Section consolidation:** Combine related sections

### Integration with CLAUDE.md Principles

- **No assumptions:** Always ask for target position and current length
- **Solo developer focus:** Emphasize individual accomplishments over team results
- **Bootstrap approach:** Highlight cost-effective improvements and efficiencies
- **Practical focus:** Keep only demonstrable experience, remove theoretical
- **Part-time consideration:** Acknowledge time constraints for resume revision

### Common Pitfalls to Avoid

1. **NEVER rewrite content** - Only suggest what to compress/remove
2. **Don't remove federal requirements** - Grades, dates, hours are mandatory
3. **Avoid generic advice** - Be specific about what to cut
4. **Don't sacrifice readability** - 2 pages must still be professional

### Advanced Compression Techniques

**For 50%+ Compression Needed:**
- Remove positions older than 15 years
- Consolidate similar roles at same organization
- Focus on most recent grade level experience
- Convert education to one-line format
- Remove references section entirely

**For 25-35% Compression Needed:**
- Eliminate redundant action verbs
- Combine bullet points where logical
- Optimize white space usage
- Condense education and training sections
- Remove outdated technical skills

### Federal Resume Format Optimization

**Space-Saving Formatting:**
```
WORK EXPERIENCE
IT Specialist (SYSADMIN), GS-2210-12 | Agency Name | 01/2020-Present | 40 hrs/week
Supervisor: John Smith (contact upon request) | Salary: $85,000
• Managed 500+ user Windows environment with 99.9% uptime
• Automated patch deployment saving 15 hours/week manual effort
```

**Inefficient Formatting (avoid):**
```
WORK EXPERIENCE

Position: Information Technology Specialist (Systems Administration)
Series and Grade: GS-2210-12
Agency: Department of Example Agency  
Dates: January 2020 to Present
Hours per week: 40
Supervisor: John Smith (phone: xxx-xxx-xxxx, email: john.smith@agency.gov)
Starting Salary: $75,000
Ending Salary: $85,000

Duties and Accomplishments:
I was responsible for managing a Windows server environment that supported over 500 users across multiple locations...
```

### Success Metrics

- **Length:** 2 pages maximum achieved
- **Compliance:** All federal requirements maintained
- **Relevance:** Target position alignment optimized
- **Readability:** Professional appearance preserved
- **Impact:** Key accomplishments retained

### Emergency Compression (Last Resort)

**If still over 2 pages after optimization:**
1. Remove all positions older than 10 years
2. Convert accomplishments to single-line bullets
3. Use smallest acceptable font (10pt)
4. Remove all optional sections (awards, associations)
5. Consider supplemental documents for detailed technical skills
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from agents.app.agents.base import FederalJobAgent, AgentResponse


class ResumeCompressionAgent(FederalJobAgent):
    """
    Specialized agent for compressing federal resumes to 2-page limit
    NEVER writes content, only analyzes and suggests compression strategies
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load resume compression specific tools"""
        
        tools = [
            Tool(
                name="length_analyzer",
                func=self._analyze_resume_length,
                description="Analyze resume length and sections"
            ),
            Tool(
                name="redundancy_checker",
                func=self._check_redundancy,
                description="Identify redundant or repetitive content"
            ),
            Tool(
                name="impact_evaluator",
                func=self._evaluate_impact_statements,
                description="Assess strength and necessity of accomplishments"
            ),
            Tool(
                name="format_optimizer",
                func=self._optimize_formatting,
                description="Suggest formatting improvements for space"
            ),
            Tool(
                name="priority_ranker",
                func=self._rank_content_priority,
                description="Rank content by relevance to target position"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get resume compression specific prompt template"""
        
        return """You are a Federal Resume Compression Advisor helping candidates meet the 2-page limit.
        Your role is to ANALYZE and GUIDE compression, but NEVER write or rewrite content.
        
        Key Responsibilities:
        1. Identify content that can be condensed
        2. Point out redundancies and repetition
        3. Suggest which experiences to prioritize
        4. Recommend formatting changes for space
        5. Ensure critical federal elements remain
        
        Federal Resume Requirements (MUST KEEP):
        - Job title, series, grade for federal positions
        - Complete employment dates (month/year)
        - Hours per week
        - Supervisor name and contact (can say "contact upon request")
        - Detailed accomplishments with metrics
        
        Compression Strategies:
        - Combine similar roles at same agency
        - Remove outdated technical skills
        - Condense education to essential details
        - Use bullet points instead of paragraphs
        - Eliminate generic duties, keep accomplishments
        - Remove references section (provided separately)
        
        Format Guidelines:
        - 0.5" margins minimum
        - 10-11 point font
        - Single spacing with space between sections
        - No headers/footers except page numbers
        - Consistent formatting throughout
        
        Available tools:
        {tools}
        
        Current conversation:
        {chat_history}
        
        User Input: {input}
        Context: {context}
        
        CRITICAL: You must NEVER write or rewrite resume content. 
        Only analyze and provide specific guidance on what to compress.
        
        {agent_scratchpad}
        """
    
    def _analyze_resume_length(self, input_data: str) -> str:
        """Analyze resume length and sections"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            resume_text = data.get("resume_text", "")
            current_pages = data.get("current_pages", 3)
            
            # Estimate content breakdown
            sections = {
                "contact": len(re.findall(r'(email|phone|address|linkedin)', resume_text.lower())),
                "summary": len(re.findall(r'(summary|objective|profile)', resume_text.lower())),
                "experience": len(re.findall(r'(experience|employment|work history)', resume_text.lower())),
                "education": len(re.findall(r'(education|degree|university|college)', resume_text.lower())),
                "skills": len(re.findall(r'(skills|technical|software|tools)', resume_text.lower())),
                "certifications": len(re.findall(r'(certification|certified|license)', resume_text.lower())),
                "awards": len(re.findall(r'(award|recognition|honor)', resume_text.lower()))
            }
            
            # Estimate word and line count
            word_count = len(resume_text.split())
            line_count = resume_text.count('\n')
            char_count = len(resume_text)
            
            # Calculate compression needed
            if current_pages > 2:
                compression_needed = round(((current_pages - 2) / current_pages) * 100)
            else:
                compression_needed = 0
            
            # Identify potential areas for compression
            compression_targets = []
            
            if word_count > 1200:  # Typical 2-page max
                compression_targets.append("Overall word count exceeds typical 2-page limit")
            
            if sections["skills"] > 20:
                compression_targets.append("Skills section may be too detailed")
            
            if sections["education"] > 10 and "experience" in resume_text.lower():
                compression_targets.append("Education section could be condensed if you have experience")
            
            # Check for date ranges
            date_patterns = re.findall(r'\d{4}\s*[-–]\s*\d{4}|\d{1,2}/\d{4}\s*[-–]\s*\d{1,2}/\d{4}', resume_text)
            job_count = len(date_patterns)
            
            if job_count > 6:
                compression_targets.append(f"Consider combining or removing older positions ({job_count} jobs listed)")
            
            return json.dumps({
                "current_pages": current_pages,
                "word_count": word_count,
                "line_count": line_count,
                "compression_needed": f"{compression_needed}%",
                "sections_detected": sections,
                "job_count": job_count,
                "compression_targets": compression_targets,
                "recommendation": self._get_length_recommendation(current_pages, compression_needed)
            })
            
        except Exception as e:
            return f"Error analyzing length: {str(e)}"
    
    def _get_length_recommendation(self, pages: int, compression: int) -> str:
        """Provide length recommendations"""
        
        if pages <= 2:
            return "Resume meets 2-page requirement"
        elif pages == 3:
            return f"Need to cut approximately {compression}% - focus on older or less relevant experience"
        elif pages == 4:
            return f"Significant compression needed ({compression}%) - keep only most recent 10-15 years"
        else:
            return f"Major compression required ({compression}%) - consider complete restructuring"
    
    def _check_redundancy(self, input_data: str) -> str:
        """Identify redundant or repetitive content"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            resume_text = data.get("resume_text", "").lower()
            
            # Common redundant phrases in federal resumes
            redundant_phrases = {
                "responsible for": "Action verb instead",
                "duties included": "Jump straight to accomplishments",
                "assisted with": "Specify your actual contribution",
                "helped to": "Use direct action verbs",
                "various tasks": "Be specific or remove",
                "etc.": "Remove and be specific",
                "references available": "Not needed on resume",
                "upon request": "Assumed, can remove"
            }
            
            redundancies_found = {}
            for phrase, suggestion in redundant_phrases.items():
                count = resume_text.count(phrase)
                if count > 0:
                    redundancies_found[phrase] = {
                        "count": count,
                        "suggestion": suggestion
                    }
            
            # Check for repeated action verbs
            action_verbs = ["managed", "developed", "implemented", "created", "led", "coordinated"]
            repeated_verbs = {}
            for verb in action_verbs:
                count = resume_text.count(verb)
                if count > 3:
                    repeated_verbs[verb] = count
            
            # Check for duplicate information
            sentences = resume_text.split('.')
            similar_content = []
            
            for i, sent1 in enumerate(sentences[:-1]):
                for sent2 in sentences[i+1:]:
                    # Simple similarity check
                    words1 = set(sent1.split())
                    words2 = set(sent2.split())
                    if len(words1) > 5 and len(words2) > 5:
                        overlap = len(words1.intersection(words2))
                        if overlap / min(len(words1), len(words2)) > 0.7:
                            similar_content.append("Potential duplicate content detected")
                            break
            
            total_redundancies = len(redundancies_found) + len(repeated_verbs)
            
            return json.dumps({
                "redundant_phrases": redundancies_found,
                "repeated_verbs": repeated_verbs,
                "similar_content_warnings": len(similar_content),
                "total_redundancies": total_redundancies,
                "space_savings": f"Could save {total_redundancies * 2} lines approximately",
                "recommendation": self._get_redundancy_recommendation(total_redundancies)
            })
            
        except Exception as e:
            return f"Error checking redundancy: {str(e)}"
    
    def _get_redundancy_recommendation(self, count: int) -> str:
        """Provide redundancy recommendations"""
        
        if count == 0:
            return "No significant redundancies detected"
        elif count < 5:
            return "Minor redundancies - easy quick wins for space"
        elif count < 10:
            return "Moderate redundancies - addressing these will help significantly"
        else:
            return "High redundancy - major opportunity for compression"
    
    def _evaluate_impact_statements(self, input_data: str) -> str:
        """Assess strength and necessity of accomplishments"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            accomplishments = data.get("accomplishments", [])
            target_series = data.get("target_series", "")
            
            evaluated_accomplishments = []
            
            for accomplishment in accomplishments:
                score = 0
                feedback = []
                
                # Check for metrics
                if re.search(r'\d+%|\$\d+|#\d+|\d+\s*(hours|days|months)', accomplishment):
                    score += 3
                    feedback.append("Has metrics")
                
                # Check for action verbs
                strong_verbs = ["achieved", "exceeded", "transformed", "pioneered", "spearheaded"]
                if any(verb in accomplishment.lower() for verb in strong_verbs):
                    score += 2
                    feedback.append("Strong action verb")
                
                # Check for relevance keywords
                if target_series and any(keyword in accomplishment.lower() 
                                       for keyword in target_series.lower().split()):
                    score += 2
                    feedback.append("Relevant to target")
                
                # Check length
                word_count = len(accomplishment.split())
                if word_count > 30:
                    score -= 1
                    feedback.append("Too long - compress")
                elif word_count < 10:
                    score -= 1
                    feedback.append("Too brief - may lack impact")
                
                # Categorize
                if score >= 5:
                    priority = "HIGH - Keep as is"
                elif score >= 3:
                    priority = "MEDIUM - Keep but consider condensing"
                else:
                    priority = "LOW - Consider removing or combining"
                
                evaluated_accomplishments.append({
                    "text": accomplishment[:50] + "...",
                    "score": score,
                    "priority": priority,
                    "feedback": feedback
                })
            
            # Sort by score
            evaluated_accomplishments.sort(key=lambda x: x["score"], reverse=True)
            
            high_priority = sum(1 for a in evaluated_accomplishments if "HIGH" in a["priority"])
            low_priority = sum(1 for a in evaluated_accomplishments if "LOW" in a["priority"])
            
            return json.dumps({
                "total_evaluated": len(evaluated_accomplishments),
                "high_priority_count": high_priority,
                "low_priority_count": low_priority,
                "top_accomplishments": evaluated_accomplishments[:5],
                "compression_opportunity": f"Consider removing {low_priority} low-priority items",
                "recommendation": self._get_impact_recommendation(high_priority, low_priority)
            })
            
        except Exception as e:
            return f"Error evaluating impact: {str(e)}"
    
    def _get_impact_recommendation(self, high: int, low: int) -> str:
        """Provide impact statement recommendations"""
        
        if low > 5:
            return f"Remove {low} low-impact items for significant space savings"
        elif low > 0:
            return f"Consider removing {low} low-priority accomplishments"
        elif high > 10:
            return "Strong accomplishments but too many - keep only best 8-10 per position"
        else:
            return "Accomplishments are well-prioritized"
    
    def _optimize_formatting(self, input_data: str) -> str:
        """Suggest formatting improvements for space"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            current_format = data.get("format_info", {})
            
            formatting_suggestions = []
            estimated_savings = 0
            
            # Check margins
            margins = current_format.get("margins", 1.0)
            if margins > 0.5:
                formatting_suggestions.append(f"Reduce margins from {margins}\" to 0.5\"")
                estimated_savings += 10
            
            # Check font size
            font_size = current_format.get("font_size", 12)
            if font_size > 11:
                formatting_suggestions.append(f"Reduce font from {font_size}pt to 10-11pt")
                estimated_savings += 15
            
            # Check line spacing
            line_spacing = current_format.get("line_spacing", 1.5)
            if line_spacing > 1.0:
                formatting_suggestions.append("Use single spacing (1.0)")
                estimated_savings += 20
            
            # Check bullet style
            if current_format.get("paragraph_style", False):
                formatting_suggestions.append("Convert paragraphs to bullet points")
                estimated_savings += 25
            
            # Check section spacing
            if current_format.get("section_spacing", 12) > 6:
                formatting_suggestions.append("Reduce spacing between sections")
                estimated_savings += 10
            
            # Date format
            if current_format.get("date_format") == "long":
                formatting_suggestions.append("Use MM/YYYY format instead of full month names")
                estimated_savings += 5
            
            # Headers and footers
            if current_format.get("headers", False):
                formatting_suggestions.append("Remove headers/footers except page numbers")
                estimated_savings += 5
            
            return json.dumps({
                "current_format": current_format,
                "formatting_suggestions": formatting_suggestions,
                "estimated_space_savings": f"{estimated_savings}%",
                "priority_changes": formatting_suggestions[:3] if formatting_suggestions else [],
                "recommendation": self._get_format_recommendation(estimated_savings)
            })
            
        except Exception as e:
            return f"Error optimizing format: {str(e)}"
    
    def _get_format_recommendation(self, savings: int) -> str:
        """Provide formatting recommendations"""
        
        if savings >= 50:
            return "Major formatting improvements possible - could save half a page or more"
        elif savings >= 30:
            return "Significant space available through formatting changes"
        elif savings >= 15:
            return "Moderate formatting improvements recommended"
        else:
            return "Formatting is already optimized"
    
    def _rank_content_priority(self, input_data: str) -> str:
        """Rank content by relevance to target position"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            positions = data.get("positions", [])
            target_keywords = data.get("target_keywords", [])
            target_series = data.get("target_series", "")
            
            ranked_positions = []
            
            for position in positions:
                relevance_score = 0
                relevance_factors = []
                
                # Check recency
                if "current" in position.lower() or "present" in position.lower():
                    relevance_score += 5
                    relevance_factors.append("Current position")
                elif "2024" in position or "2023" in position:
                    relevance_score += 4
                    relevance_factors.append("Recent experience")
                elif "2022" in position or "2021" in position:
                    relevance_score += 3
                    relevance_factors.append("Relevant timeframe")
                elif any(year in position for year in ["2020", "2019", "2018"]):
                    relevance_score += 2
                    relevance_factors.append("Within 5 years")
                else:
                    relevance_score += 1
                    relevance_factors.append("Older experience")
                
                # Check keyword relevance
                position_lower = position.lower()
                matched_keywords = [kw for kw in target_keywords if kw.lower() in position_lower]
                relevance_score += len(matched_keywords) * 2
                if matched_keywords:
                    relevance_factors.append(f"Matches: {', '.join(matched_keywords[:3])}")
                
                # Check federal experience
                if any(term in position_lower for term in ["federal", "government", "gs-", "usajobs"]):
                    relevance_score += 3
                    relevance_factors.append("Federal experience")
                
                # Check series match
                if target_series and target_series.lower() in position_lower:
                    relevance_score += 4
                    relevance_factors.append("Series match")
                
                # Determine priority
                if relevance_score >= 10:
                    priority = "CRITICAL - Must keep"
                elif relevance_score >= 7:
                    priority = "HIGH - Keep if possible"
                elif relevance_score >= 4:
                    priority = "MEDIUM - Condense"
                else:
                    priority = "LOW - Consider removing"
                
                ranked_positions.append({
                    "position": position[:100] + "...",
                    "relevance_score": relevance_score,
                    "priority": priority,
                    "factors": relevance_factors
                })
            
            # Sort by relevance
            ranked_positions.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            critical_count = sum(1 for p in ranked_positions if "CRITICAL" in p["priority"])
            low_count = sum(1 for p in ranked_positions if "LOW" in p["priority"])
            
            return json.dumps({
                "total_positions": len(ranked_positions),
                "critical_positions": critical_count,
                "low_priority_positions": low_count,
                "top_positions": ranked_positions[:5],
                "removal_candidates": [p for p in ranked_positions if "LOW" in p["priority"]][:3],
                "recommendation": self._get_priority_recommendation(critical_count, low_count)
            })
            
        except Exception as e:
            return f"Error ranking content: {str(e)}"
    
    def _get_priority_recommendation(self, critical: int, low: int) -> str:
        """Provide content priority recommendations"""
        
        if low >= 3:
            return f"Remove or significantly condense {low} low-priority positions"
        elif low > 0:
            return f"Consider removing {low} less relevant position(s)"
        elif critical > 5:
            return "Too many critical positions - be more selective"
        else:
            return "Content is well-prioritized for target position"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze resume for compression opportunities
        NEVER writes content, only provides guidance
        """
        
        try:
            # Extract resume information
            resume_text = data.get("resume_text", "")
            current_pages = data.get("current_pages", 3)
            target_position = data.get("target_position", "")
            target_series = data.get("target_series", "")
            
            # Build analysis query
            query = f"""
            Analyze this resume for compression to 2 pages:
            
            Current Length: {current_pages} pages
            Word Count: {len(resume_text.split())} words
            
            Target Position: {target_position}
            Target Series: {target_series}
            
            Provide:
            1. Length analysis and compression targets
            2. Redundancy identification
            3. Impact statement evaluation
            4. Formatting optimization suggestions
            5. Content prioritization by relevance
            
            Remember: NEVER write or rewrite content. Only analyze and guide.
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add compression strategy
                response.data["compression_strategy"] = {
                    "immediate_actions": [
                        "Remove positions older than 10-15 years",
                        "Convert paragraphs to bullet points",
                        "Eliminate 'responsible for' phrases"
                    ],
                    "formatting_quick_wins": [
                        "Reduce margins to 0.5 inches",
                        "Use 10-11 point font",
                        "Single space with breaks between sections"
                    ],
                    "content_priorities": [
                        "Keep all federal positions with full details",
                        "Condense private sector roles",
                        "Remove references section"
                    ],
                    "compliance_reminder": "NEVER remove: grades, dates, hours/week, supervisor info"
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
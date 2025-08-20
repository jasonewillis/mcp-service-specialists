"""
Executive Order Research Agent - Federal Policy Analysis
Researches executive orders and federal policies relevant to job applications

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Use WebFetch or WebSearch tools to gather recent executive orders
2. Identify target position/agency for relevance filtering
3. Collect policy text using Read tool if documents are available locally
4. Focus on orders from last 2-3 years for current relevance
5. Gather candidate background to match policy areas

**Effective Prompting Patterns:**
```
"Research executive orders relevant to cybersecurity positions:
- Target: GS-13 IT Specialist (INFOSEC) at DHS
- Focus: EO 14028 (Cybersecurity), EO 14110 (AI)
- Analysis needed: Impact on hiring, required skills, implementation
- Timeline: Orders from 2021-present
- Deliverable: Policy keywords and career implications"
```

**Best Workflow:**
1. **Policy Discovery** → Search for relevant executive orders
2. **Impact Analysis** → Assess hiring and operational impacts
3. **Agency Mapping** → Match policies to specific agencies
4. **Timeline Tracking** → Monitor implementation deadlines
5. **Keyword Extraction** → Identify application-relevant terms

### Integration with Other Agents

**Workflow Chains:**
- Executive Order Research → Technical Agents (skill prioritization)
- Use with Analytics Intelligence for hiring trend context
- Combine with Essay Guidance for policy awareness demonstration

**Handoff Points:**
- Share policy priorities with skill development planning
- Provide agency implementation insights to targeting strategy
- Pass keyword analysis to resume optimization

### Key Executive Orders for Federal Job Seekers

**EO 14028 - Improving Nation's Cybersecurity (May 2021):**
- Relevant for: IT Specialists, Security Analysts, DevOps Engineers
- Keywords: Zero Trust, incident response, supply chain security
- Agencies: DHS/CISA, DoD, all federal agencies
- Impact: Massive cybersecurity hiring across government

**EO 14110 - Safe, Secure AI Development (October 2023):**
- Relevant for: Data Scientists, AI/ML Engineers, Policy Analysts
- Keywords: AI governance, risk management, algorithmic bias
- Agencies: NIST, Commerce, OMB, all agencies using AI
- Impact: New AI governance roles, compliance positions

**EO 14058 - Transforming Federal Customer Experience (December 2021):**
- Relevant for: UX Designers, Customer Experience, Program Analysts
- Keywords: Digital services, user experience, service delivery
- Agencies: GSA, OMB, high-impact service providers
- Impact: Focus on citizen-facing service improvements

### Test-Driven Usage Examples

**Example 1: Cybersecurity Professional**
```python
test_data = {
    "target_position": "IT Specialist (INFOSEC)",
    "agency": "DHS",
    "policy_focus": "cybersecurity",
    "orders": ["EO 14028", "EO 14086"],
    "research_depth": "implementation requirements"
}
# Expected: Zero Trust requirements, timeline pressures, skills needed
```

**Example 2: Data Scientist**
```python
test_data = {
    "target_position": "Data Scientist GS-1560",
    "agency": "Commerce/NIST",
    "policy_focus": "AI governance",
    "orders": ["EO 14110"],
    "research_depth": "career opportunities"
}
# Expected: AI safety roles, risk assessment positions, compliance needs
```

### Visual Iteration Methods

**Policy Research Dashboard:**
- Executive order timeline and implementation phases
- Agency-specific implementation status
- Keyword frequency analysis across orders
- Career opportunity mapping from policy requirements

### Checklist-Based Workflows

**Pre-Research Setup:**
- [ ] Target position and agency identified
- [ ] Relevant policy areas determined
- [ ] Time frame for orders established (2021-present)
- [ ] Research objectives clarified
- [ ] Access to policy sources confirmed

**Research Analysis Checklist:**
- [ ] Order text reviewed and categorized
- [ ] Implementation impact assessed
- [ ] Agency-specific requirements identified
- [ ] Career-relevant keywords extracted
- [ ] Timeline implications understood

### Policy Research Strategies

**Current Administration Priorities (2021-Present):**
1. **Cybersecurity** - EO 14028, 14086 (CISA authorities)
2. **Climate** - EO 14008 (climate crisis), 14057 (federal sustainability)
3. **Equity** - EO 13985 (racial equity), 14035 (DEIA in federal workforce)
4. **AI/Technology** - EO 14110 (AI safety), M-24-10 (AI governance)
5. **Customer Experience** - EO 14058 (CX transformation)

**Research Sources:**
- Federal Register (federalregister.gov)
- White House (whitehouse.gov/briefing-room)
- Agency implementation plans
- OMB memoranda
- Congressional oversight reports

### Integration with CLAUDE.md Principles

- **No assumptions:** Always verify order numbers and effective dates
- **Solo developer focus:** Emphasize individual skill development from policy insights
- **Bootstrap approach:** Use free government sources and public information
- **Practical focus:** Connect policy research to actual job opportunities
- **Part-time consideration:** Acknowledge time limits for policy research

### Common Policy Research Pitfalls

1. **Focusing on outdated orders** - Prioritize current administration
2. **Missing implementation timelines** - Deadlines create hiring urgency
3. **Ignoring agency-specific impacts** - Implementation varies by agency
4. **Overlooking keyword value** - Policy language appears in job descriptions

### Advanced Research Techniques

**Implementation Tracking:**
- Monitor agency strategic plans
- Track budget requests for policy implementation
- Follow Congressional hearing transcripts
- Review GAO reports on implementation progress

**Career Intelligence:**
- Identify new position types created by policies
- Track hiring surge patterns after major orders
- Monitor skill requirement evolution
- Assess long-term career trajectory implications

### Policy-to-Career Translation

**From Executive Orders to Job Opportunities:**
1. **Policy Requirement** → **Job Creation** → **Skill Development**
2. **Implementation Deadline** → **Hiring Urgency** → **Application Timing**
3. **Agency Mandate** → **Budget Allocation** → **Position Availability**
4. **Compliance Need** → **Oversight Roles** → **Career Specialization**

### Recent High-Impact Areas

**Zero Trust Architecture (EO 14028):**
- New cybersecurity architect positions
- Cloud security specialist roles
- Identity management experts needed

**AI Governance (EO 14110):**
- AI ethics officers
- Algorithmic bias analysts
- AI risk management specialists

**Federal Workforce Transformation (EO 14035):**
- DEIA program managers
- Workforce analytics specialists
- Barrier analysis experts

### Success Metrics for Policy Research

- **Relevance:** Orders directly impact target position/agency
- **Timeliness:** Implementation creates current hiring needs
- **Actionability:** Research translates to specific career moves
- **Keyword Value:** Policy terms enhance application materials
- **Strategic Insight:** Understanding agency priorities and directions

### Emergency Policy Updates

**When Major Orders Drop:**
1. Immediate impact assessment for target positions
2. Implementation timeline analysis
3. Agency-specific guidance review
4. Skills gap identification
5. Application strategy adjustment
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re
from datetime import datetime, timedelta

from agents.app.agents.base import FederalJobAgent, AgentResponse


class ExecutiveOrderResearchAgent(FederalJobAgent):
    """
    Specialized agent for researching executive orders and federal policies
    Helps candidates understand policy contexts relevant to their applications
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load executive order research specific tools"""
        
        tools = [
            Tool(
                name="order_classifier",
                func=self._classify_executive_order,
                description="Classify and categorize executive orders"
            ),
            Tool(
                name="impact_analyzer",
                func=self._analyze_policy_impact,
                description="Analyze policy impact on hiring and operations"
            ),
            Tool(
                name="agency_matcher",
                func=self._match_agency_policies,
                description="Match policies to specific agencies"
            ),
            Tool(
                name="timeline_tracker",
                func=self._track_implementation_timeline,
                description="Track policy implementation timelines"
            ),
            Tool(
                name="keyword_extractor",
                func=self._extract_relevant_keywords,
                description="Extract job-relevant keywords from policies"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get executive order research specific prompt template"""
        
        return """You are a Federal Executive Order Research Advisor helping candidates understand policy contexts.
        Your role is to RESEARCH and ANALYZE policies, but NEVER write application content.
        
        Key Responsibilities:
        1. Research executive orders relevant to positions
        2. Analyze policy impacts on hiring
        3. Identify agency-specific implementations
        4. Track policy timelines and deadlines
        5. Extract career-relevant keywords
        
        Recent Federal Policy Focus Areas:
        - Cybersecurity (EO 14028 - Improving Nation's Cybersecurity)
        - AI/Technology (EO 14110 - Safe, Secure AI Development)
        - Climate Change (EO 14008 - Climate Crisis Response)
        - Equity (EO 13985 - Advancing Racial Equity)
        - Customer Experience (EO 14058 - Customer Experience)
        - Supply Chain (EO 14017 - Supply Chains)
        - Federal Workforce (EO 14035 - Diversity, Equity, Inclusion)
        - Digital Services (21st Century IDEA Act)
        
        Research Sources:
        - Federal Register
        - WhiteHouse.gov
        - Agency implementation plans
        - OPM guidance
        - GAO reports
        - Congressional oversight
        
        Available tools:
        {tools}
        
        Current conversation:
        {chat_history}
        
        User Input: {input}
        Context: {context}
        
        Remember: You provide research and analysis ONLY. 
        Never write application content or suggest specific language.
        
        {agent_scratchpad}
        """
    
    def _classify_executive_order(self, input_data: str) -> str:
        """Classify and categorize executive orders"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            order_text = data.get("order_text", "").lower()
            order_number = data.get("order_number", "")
            target_position = data.get("target_position", "").lower()
            
            # Known executive order categories
            policy_categories = {
                "cybersecurity": {
                    "keywords": ["cybersecurity", "cyber", "zero trust", "incident response", "nist", "security"],
                    "relevant_orders": ["14028", "14086"],
                    "job_relevance": ["2210", "0854", "1550"]
                },
                "artificial_intelligence": {
                    "keywords": ["artificial intelligence", "ai", "machine learning", "automation", "algorithms"],
                    "relevant_orders": ["14110"],
                    "job_relevance": ["1560", "0343", "2210"]
                },
                "climate_environment": {
                    "keywords": ["climate", "environment", "sustainability", "clean energy", "emissions"],
                    "relevant_orders": ["14008", "14057"],
                    "job_relevance": ["0401", "1301", "0819"]
                },
                "equity_diversity": {
                    "keywords": ["equity", "diversity", "inclusion", "underserved", "barriers", "accessibility"],
                    "relevant_orders": ["13985", "14035"],
                    "job_relevance": ["all_series"]
                },
                "customer_experience": {
                    "keywords": ["customer", "experience", "service", "digital", "user", "public"],
                    "relevant_orders": ["14058"],
                    "job_relevance": ["0301", "2210", "0343"]
                },
                "supply_chain": {
                    "keywords": ["supply chain", "procurement", "sourcing", "manufacturing", "logistics"],
                    "relevant_orders": ["14017"],
                    "job_relevance": ["1102", "0346", "1560"]
                },
                "workforce_development": {
                    "keywords": ["workforce", "skills", "training", "development", "hiring", "retention"],
                    "relevant_orders": ["14035", "14025"],
                    "job_relevance": ["all_series"]
                }
            }
            
            # Classify the order
            matched_categories = []
            relevance_score = 0
            
            for category, info in policy_categories.items():
                keyword_matches = sum(1 for kw in info["keywords"] if kw in order_text)
                if keyword_matches > 0:
                    matched_categories.append({
                        "category": category,
                        "keyword_matches": keyword_matches,
                        "relevant_orders": info["relevant_orders"],
                        "job_relevance": info["job_relevance"]
                    })
                    relevance_score += keyword_matches
            
            # Sort by relevance
            matched_categories.sort(key=lambda x: x["keyword_matches"], reverse=True)
            
            # Determine primary category
            primary_category = matched_categories[0]["category"] if matched_categories else "general_administration"
            
            # Check job relevance
            job_relevant = False
            for category in matched_categories:
                if ("all_series" in category["job_relevance"] or 
                    any(series in target_position for series in category["job_relevance"])):
                    job_relevant = True
                    break
            
            return json.dumps({
                "order_number": order_number,
                "primary_category": primary_category,
                "matched_categories": matched_categories,
                "relevance_score": relevance_score,
                "job_relevant": job_relevant,
                "recommendation": self._get_classification_recommendation(primary_category, job_relevant)
            })
            
        except Exception as e:
            return f"Error classifying order: {str(e)}"
    
    def _get_classification_recommendation(self, category: str, relevant: bool) -> str:
        """Provide classification recommendations"""
        
        if relevant:
            if category == "cybersecurity":
                return "Highly relevant for IT positions - understand zero trust implementation"
            elif category == "artificial_intelligence":
                return "Critical for data science roles - know AI governance requirements"
            elif category == "equity_diversity":
                return "Applies to all positions - understand barrier removal initiatives"
            else:
                return f"Relevant to your field - study {category} implementation requirements"
        else:
            return "Lower direct relevance but may affect agency operations"
    
    def _analyze_policy_impact(self, input_data: str) -> str:
        """Analyze policy impact on hiring and operations"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            policy_text = data.get("policy_text", "").lower()
            target_agency = data.get("target_agency", "").lower()
            
            # Impact indicators
            impact_areas = {
                "hiring_practices": {
                    "indicators": ["hiring", "recruitment", "talent", "workforce", "diversity", "skills gap"],
                    "impact_level": 0
                },
                "technology_modernization": {
                    "indicators": ["modernization", "digital", "technology", "systems", "infrastructure"],
                    "impact_level": 0
                },
                "security_requirements": {
                    "indicators": ["security", "risk", "compliance", "standards", "framework", "controls"],
                    "impact_level": 0
                },
                "operational_changes": {
                    "indicators": ["procedures", "processes", "implementation", "requirements", "mandates"],
                    "impact_level": 0
                },
                "budget_implications": {
                    "indicators": ["funding", "budget", "resources", "investment", "appropriations"],
                    "impact_level": 0
                }
            }
            
            # Calculate impact levels
            for area, info in impact_areas.items():
                info["impact_level"] = sum(1 for indicator in info["indicators"] if indicator in policy_text)
            
            # Determine overall impact
            total_impact = sum(area["impact_level"] for area in impact_areas.values())
            
            if total_impact >= 15:
                impact_magnitude = "High - Major organizational changes expected"
            elif total_impact >= 10:
                impact_magnitude = "Medium - Significant process changes"
            elif total_impact >= 5:
                impact_magnitude = "Low - Limited operational impact"
            else:
                impact_magnitude = "Minimal - Administrative changes only"
            
            # Check for implementation timelines
            timeline_indicators = re.findall(r'(\d+)\s*(days?|months?|years?)', policy_text)
            has_deadlines = len(timeline_indicators) > 0
            
            # Agency-specific considerations
            agency_considerations = []
            if "defense" in target_agency or "dod" in target_agency:
                agency_considerations.append("DoD typically has accelerated implementation")
            elif "homeland" in target_agency or "dhs" in target_agency:
                agency_considerations.append("DHS focuses on security implementation")
            elif "veterans" in target_agency or "va" in target_agency:
                agency_considerations.append("VA emphasizes customer experience aspects")
            
            return json.dumps({
                "impact_areas": impact_areas,
                "total_impact_score": total_impact,
                "impact_magnitude": impact_magnitude,
                "has_implementation_deadlines": has_deadlines,
                "timeline_indicators": timeline_indicators,
                "agency_considerations": agency_considerations,
                "recommendation": self._get_impact_recommendation(impact_magnitude, has_deadlines)
            })
            
        except Exception as e:
            return f"Error analyzing impact: {str(e)}"
    
    def _get_impact_recommendation(self, magnitude: str, deadlines: bool) -> str:
        """Provide impact analysis recommendations"""
        
        if "High" in magnitude and deadlines:
            return "Major policy shift with deadlines - understand implementation requirements"
        elif "High" in magnitude:
            return "Significant changes expected - research agency implementation plans"
        elif deadlines:
            return "Monitor implementation deadlines for potential opportunities"
        else:
            return "Lower immediate impact but track for future relevance"
    
    def _match_agency_policies(self, input_data: str) -> str:
        """Match policies to specific agencies"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            target_agencies = data.get("target_agencies", [])
            policy_area = data.get("policy_area", "")
            
            # Agency policy leadership patterns
            agency_specializations = {
                "dod": {
                    "leads_on": ["cybersecurity", "supply_chain", "ai_security"],
                    "implementation_speed": "fast",
                    "focus_areas": ["zero trust", "cyber workforce", "defense innovation"]
                },
                "dhs": {
                    "leads_on": ["cybersecurity", "critical_infrastructure", "supply_chain"],
                    "implementation_speed": "fast",
                    "focus_areas": ["CISA guidance", "federal security", "incident response"]
                },
                "gsa": {
                    "leads_on": ["customer_experience", "technology_modernization", "procurement"],
                    "implementation_speed": "medium",
                    "focus_areas": ["18F", "TTS", "government-wide services"]
                },
                "omb": {
                    "leads_on": ["all_policies", "government_wide", "implementation"],
                    "implementation_speed": "varies",
                    "focus_areas": ["policy guidance", "memoranda", "oversight"]
                },
                "va": {
                    "leads_on": ["customer_experience", "healthcare_it", "veteran_services"],
                    "implementation_speed": "medium",
                    "focus_areas": ["patient experience", "digital transformation", "benefits"]
                },
                "treasury": {
                    "leads_on": ["cybersecurity", "financial_systems", "risk_management"],
                    "implementation_speed": "medium",
                    "focus_areas": ["financial infrastructure", "payments", "cyber threats"]
                }
            }
            
            # Match agencies to policy area
            agency_matches = []
            
            for agency in target_agencies:
                agency_key = agency.lower()
                if agency_key in agency_specializations:
                    spec = agency_specializations[agency_key]
                    
                    relevance = "high" if (policy_area.lower() in spec["leads_on"] or 
                                        "all_policies" in spec["leads_on"]) else "medium"
                    
                    agency_matches.append({
                        "agency": agency,
                        "relevance": relevance,
                        "implementation_speed": spec["implementation_speed"],
                        "focus_areas": spec["focus_areas"],
                        "leadership_role": policy_area.lower() in spec["leads_on"]
                    })
            
            # Sort by relevance
            agency_matches.sort(key=lambda x: x["relevance"], reverse=True)
            
            return json.dumps({
                "policy_area": policy_area,
                "agency_matches": agency_matches,
                "top_implementers": [a for a in agency_matches if a["relevance"] == "high"],
                "recommendation": self._get_agency_recommendation(agency_matches)
            })
            
        except Exception as e:
            return f"Error matching agencies: {str(e)}"
    
    def _get_agency_recommendation(self, matches: List) -> str:
        """Provide agency matching recommendations"""
        
        high_relevance = [m for m in matches if m["relevance"] == "high"]
        
        if len(high_relevance) > 1:
            return "Multiple agencies lead on this - opportunities across government"
        elif len(high_relevance) == 1:
            return f"Focus on {high_relevance[0]['agency']} - they lead implementation"
        else:
            return "Broad implementation across agencies - good general knowledge"
    
    def _track_implementation_timeline(self, input_data: str) -> str:
        """Track policy implementation timelines"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            policy_text = data.get("policy_text", "")
            order_date = data.get("order_date", "")
            
            # Extract timeline elements
            timeline_patterns = {
                "days": r'(\d+)\s*days?',
                "months": r'(\d+)\s*months?',
                "years": r'(\d+)\s*years?',
                "specific_dates": r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
            }
            
            timeline_elements = {}
            
            for unit, pattern in timeline_patterns.items():
                matches = re.findall(pattern, policy_text, re.IGNORECASE)
                if matches:
                    timeline_elements[unit] = matches
            
            # Identify implementation phases
            phase_indicators = {
                "immediate": ["immediately", "within 30 days", "within 60 days"],
                "short_term": ["within 6 months", "within 180 days", "within 1 year"],
                "long_term": ["within 2 years", "within 3 years", "ongoing"],
                "reporting": ["report", "update", "status", "progress"]
            }
            
            identified_phases = {}
            for phase, indicators in phase_indicators.items():
                found = [ind for ind in indicators if ind.lower() in policy_text.lower()]
                if found:
                    identified_phases[phase] = found
            
            # Calculate urgency score
            urgency_score = 0
            if "immediate" in identified_phases:
                urgency_score += 5
            if "short_term" in identified_phases:
                urgency_score += 3
            if timeline_elements.get("days"):
                urgency_score += 4
            if timeline_elements.get("months"):
                urgency_score += 2
            
            urgency_level = "High" if urgency_score >= 7 else "Medium" if urgency_score >= 3 else "Low"
            
            return json.dumps({
                "timeline_elements": timeline_elements,
                "implementation_phases": identified_phases,
                "urgency_score": urgency_score,
                "urgency_level": urgency_level,
                "hiring_implications": self._assess_hiring_implications(urgency_level, identified_phases),
                "recommendation": self._get_timeline_recommendation(urgency_level)
            })
            
        except Exception as e:
            return f"Error tracking timeline: {str(e)}"
    
    def _assess_hiring_implications(self, urgency: str, phases: Dict) -> str:
        """Assess implications for hiring"""
        
        if urgency == "High" and "immediate" in phases:
            return "Urgent implementation may accelerate hiring for specialized roles"
        elif urgency == "High":
            return "Fast timeline suggests agencies need experienced implementers"
        elif "reporting" in phases:
            return "Ongoing reporting requirements may create analyst positions"
        else:
            return "Standard implementation timeline"
    
    def _get_timeline_recommendation(self, urgency: str) -> str:
        """Provide timeline recommendations"""
        
        if urgency == "High":
            return "Urgent implementation - agencies likely hiring specialists now"
        elif urgency == "Medium":
            return "Moderate timeline - good opportunity to build relevant experience"
        else:
            return "Long-term implementation - time to develop needed skills"
    
    def _extract_relevant_keywords(self, input_data: str) -> str:
        """Extract job-relevant keywords from policies"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            policy_text = data.get("policy_text", "").lower()
            target_series = data.get("target_series", "")
            
            # Keyword categories by job series
            series_keywords = {
                "2210": ["information technology", "cybersecurity", "systems", "network", "security"],
                "1560": ["data science", "analytics", "machine learning", "artificial intelligence", "statistics"],
                "1530": ["statistics", "statistical", "data analysis", "survey", "research methodology"],
                "0343": ["management analysis", "process improvement", "efficiency", "operations"],
                "1102": ["contracting", "procurement", "acquisition", "sourcing", "vendor management"]
            }
            
            # General federal keywords
            federal_keywords = [
                "implementation", "compliance", "framework", "standards", "requirements",
                "oversight", "governance", "risk management", "performance", "metrics",
                "coordination", "collaboration", "stakeholder", "interagency", "cross-functional"
            ]
            
            # Extract keywords
            found_keywords = []
            
            # Series-specific keywords
            if target_series in series_keywords:
                for keyword in series_keywords[target_series]:
                    if keyword in policy_text:
                        found_keywords.append({"keyword": keyword, "category": "series_specific"})
            
            # Federal keywords
            for keyword in federal_keywords:
                if keyword in policy_text:
                    found_keywords.append({"keyword": keyword, "category": "federal_general"})
            
            # Technology keywords (always relevant)
            tech_keywords = ["digital", "automation", "cloud", "api", "platform", "integration"]
            for keyword in tech_keywords:
                if keyword in policy_text:
                    found_keywords.append({"keyword": keyword, "category": "technology"})
            
            # Leadership keywords
            leadership_keywords = ["coordination", "leadership", "oversight", "management", "strategy"]
            for keyword in leadership_keywords:
                if keyword in policy_text:
                    found_keywords.append({"keyword": keyword, "category": "leadership"})
            
            # Remove duplicates and sort
            unique_keywords = []
            seen = set()
            for kw in found_keywords:
                if kw["keyword"] not in seen:
                    unique_keywords.append(kw)
                    seen.add(kw["keyword"])
            
            # Categorize by frequency (if we had frequency data)
            priority_keywords = [kw for kw in unique_keywords if kw["category"] == "series_specific"]
            supporting_keywords = [kw for kw in unique_keywords if kw["category"] != "series_specific"]
            
            return json.dumps({
                "total_keywords": len(unique_keywords),
                "priority_keywords": priority_keywords,
                "supporting_keywords": supporting_keywords,
                "keyword_categories": {
                    "series_specific": len([k for k in unique_keywords if k["category"] == "series_specific"]),
                    "federal_general": len([k for k in unique_keywords if k["category"] == "federal_general"]),
                    "technology": len([k for k in unique_keywords if k["category"] == "technology"]),
                    "leadership": len([k for k in unique_keywords if k["category"] == "leadership"])
                },
                "recommendation": self._get_keyword_recommendation(len(priority_keywords), len(supporting_keywords))
            })
            
        except Exception as e:
            return f"Error extracting keywords: {str(e)}"
    
    def _get_keyword_recommendation(self, priority_count: int, supporting_count: int) -> str:
        """Provide keyword extraction recommendations"""
        
        if priority_count >= 3:
            return "Rich source of series-specific keywords for your applications"
        elif priority_count >= 1:
            return "Some relevant keywords - useful for understanding context"
        elif supporting_count >= 5:
            return "Good federal context keywords but not series-specific"
        else:
            return "Limited keyword relevance for direct application use"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze executive orders and policies for job relevance
        """
        
        try:
            # Extract research parameters
            order_number = data.get("order_number", "")
            policy_text = data.get("policy_text", "")
            target_position = data.get("target_position", "")
            target_agency = data.get("target_agency", "")
            research_focus = data.get("research_focus", "job_relevance")
            
            # Build research query
            query = f"""
            Research this executive order/policy for job application relevance:
            
            Order/Policy: {order_number}
            Target Position: {target_position}
            Target Agency: {target_agency}
            Research Focus: {research_focus}
            
            Policy Content: {policy_text[:500]}...
            
            Provide:
            1. Policy classification and categorization
            2. Impact analysis on hiring and operations
            3. Agency-specific implementation considerations
            4. Implementation timeline tracking
            5. Relevant keyword extraction for applications
            
            Focus on practical insights for job seekers.
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add research insights
                response.data["research_insights"] = {
                    "application_relevance": [
                        "Understand policy context for interview discussions",
                        "Identify skills and experience priorities",
                        "Research agency implementation approaches"
                    ],
                    "career_implications": [
                        "New roles may be created for implementation",
                        "Existing positions may gain new responsibilities",
                        "Skills gaps may create hiring opportunities"
                    ],
                    "monitoring_tips": [
                        "Track agency implementation plans",
                        "Monitor budget requests for clues",
                        "Follow Congressional oversight hearings"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Research failed: {str(e)}"
            )
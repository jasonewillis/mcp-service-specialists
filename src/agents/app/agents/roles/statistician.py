"""
Statistician Agent - Series 1530 Specialist
Analyzes candidates for federal statistician positions

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Use Read tool to examine candidate's statistical background
2. Gather information about target agency (BLS, Census, NCHS, BEA, USDA)
3. Identify methodology experience and software proficiency
4. Collect publication and research portfolio

**Effective Prompting Patterns:**
```
"Analyze this statistician candidate for GS-12 BLS position:
- Education: MS Statistics, University
- Software: SAS (5 years), R (3 years), SPSS (2 years)
- Experience: Survey design at [organization]
- Publications: [list relevant papers]
- Target: Labor statistics focus"
```

**Best Workflow:**
1. **Methodology Assessment** → Evaluate statistical technique depth
2. **Software Validation** → Check federal agency preferences (SAS priority)
3. **Survey Experience** → Assess design and sampling knowledge
4. **Research Portfolio** → Review publications for federal relevance
5. **Agency Matching** → Align experience with specific agency needs

### Integration with Other Agents

**Workflow Chains:**
- Statistician Agent → Executive Order Research (for policy context)
- Use with Analytics Intelligence for federal hiring trends
- Combine with Essay Guidance for Merit Hiring essays

**Handoff Points:**
- Share methodology gaps with training recommendations
- Provide agency-specific insights to application strategy
- Pass federal survey experience to Resume Compression Agent

### Common Pitfalls to Avoid

1. **Undervaluing SAS experience** - Federal agencies heavily use SAS
2. **Ignoring survey methodology** - Critical for federal statistics
3. **Missing federal data context** - ACS, CPS, NHIS experience valuable
4. **Overlooking policy relevance** - Statistical work supports policy decisions

### Test-Driven Usage Examples

**Example 1: Academic Researcher**
```python
test_data = {
    "education": {"degree": "PhD", "field": "Statistics"},
    "experience": "University research, regression modeling",
    "software": ["R", "Stata", "Python"],
    "publications": ["Bayesian methods paper", "Time series analysis"],
    "target_agency": "Census Bureau"
}
# Expected: Emphasize survey methodology, recommend SAS training
```

**Example 2: Government Contractor**
```python
test_data = {
    "experience": "3 years federal contractor, NCHS projects",
    "software": ["SAS", "R", "SQL"],
    "surveys": ["NHIS data analysis", "BRFSS work"],
    "target_grade": "GS-13"
}
# Expected: Strong federal alignment, highlight direct agency experience
```

### Visual Iteration Methods

**Statistical Portfolio Review:**
- Create methodology matrix showing depth vs. breadth
- Map software skills to agency preferences
- Timeline analysis of statistical experience progression
- Research impact visualization (citations, applications)

### Checklist-Based Workflows

**Pre-Analysis Checklist:**
- [ ] Statistical methodology background documented
- [ ] Software proficiency levels assessed
- [ ] Survey/sampling experience identified
- [ ] Research publications reviewed
- [ ] Target agency requirements understood

**Post-Analysis Checklist:**
- [ ] SAS proficiency addressed
- [ ] Federal survey experience highlighted
- [ ] Methodology depth evaluated
- [ ] Agency alignment confirmed
- [ ] Research relevance established

### Optimization Tips

1. **Agency Research:** Understand specific statistical focuses (BLS=labor, Census=demographics)
2. **Software Strategy:** Prioritize SAS experience for federal readiness
3. **Methodology Mapping:** Connect academic/private methods to federal applications
4. **Publication Strategy:** Emphasize policy-relevant research

### Integration with CLAUDE.md Principles

- **No assumptions:** Always ask for target agency and grade level
- **Solo developer focus:** Emphasize individual statistical accomplishments
- **Bootstrap approach:** Highlight work with public datasets (federal data)
- **Practical focus:** Demonstrate actual statistical analyses, not just theory
- **Part-time consideration:** Acknowledge that statistical skills take time to develop

### Common Federal Scenarios

**Bureau of Labor Statistics:** Emphasize economic data, employment statistics, CPI work
**Census Bureau:** Focus on demographic analysis, survey methodology, ACS experience  
**NCHS:** Highlight health statistics, vital records, epidemiological methods
**BEA:** Economic accounts, GDP methodology, input-output analysis
**USDA/ERS:** Agricultural statistics, rural demographics, food security analysis
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from agents.app.agents.base import FederalJobAgent, AgentResponse


class StatisticianAgent(FederalJobAgent):
    """
    Specialized agent for federal statistician positions (Series 1530)
    Focuses on statistical methodology, survey design, and research experience
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load statistician specific tools"""
        
        tools = [
            Tool(
                name="methodology_checker",
                func=self._check_statistical_methodology,
                description="Evaluate statistical methodology experience"
            ),
            Tool(
                name="survey_analyzer",
                func=self._analyze_survey_design,
                description="Assess survey design and sampling experience"
            ),
            Tool(
                name="software_validator",
                func=self._validate_statistical_software,
                description="Check proficiency in statistical software"
            ),
            Tool(
                name="research_scanner",
                func=self._scan_research_experience,
                description="Evaluate research and publication record"
            ),
            Tool(
                name="agency_matcher",
                func=self._match_agency_requirements,
                description="Match experience to specific agency needs"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get statistician specific prompt template"""
        
        return """You are a Federal Statistician Career Advisor specializing in Series 1530 positions.
        Your role is to ANALYZE and GUIDE candidates, but NEVER write content for them.
        
        Key Responsibilities:
        1. Analyze candidate's statistical background
        2. Evaluate methodology expertise
        3. Assess survey and sampling experience
        4. Identify relevant research work
        5. Point to qualifying experience
        
        Federal Statistician Focus Areas:
        - Statistical methodology and theory
        - Survey design and sampling
        - Data collection and quality control
        - Statistical software (SAS, R, SPSS, Stata)
        - Federal statistical systems
        - Research and publication
        - Policy analysis support
        
        Key Federal Agencies:
        - Bureau of Labor Statistics (BLS)
        - Census Bureau
        - National Center for Health Statistics (NCHS)
        - Bureau of Economic Analysis (BEA)
        - USDA Economic Research Service
        
        Available tools:
        {tools}
        
        Current conversation:
        {chat_history}
        
        User Input: {input}
        Context: {context}
        
        Remember: You must NEVER write application content. 
        Only analyze, guide, and point to the candidate's existing experience.
        
        {agent_scratchpad}
        """
    
    def _check_statistical_methodology(self, input_data: str) -> str:
        """Evaluate statistical methodology experience"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            methodologies = {
                "regression": ["linear regression", "logistic", "glm", "mixed models", "hierarchical"],
                "hypothesis_testing": ["t-test", "anova", "chi-square", "fisher", "bonferroni"],
                "time_series": ["arima", "arma", "forecasting", "seasonal", "trend analysis"],
                "sampling": ["stratified", "cluster", "systematic", "probability", "weighting"],
                "bayesian": ["bayesian", "mcmc", "prior", "posterior", "gibbs"],
                "multivariate": ["pca", "factor analysis", "discriminant", "manova", "canonical"],
                "nonparametric": ["mann-whitney", "wilcoxon", "kruskal", "spearman", "kendall"],
                "experimental": ["design of experiments", "randomized", "factorial", "blocking"]
            }
            
            found_methods = {}
            expertise_score = 0
            
            for category, methods in methodologies.items():
                found = [m for m in methods if m in experience]
                if found:
                    found_methods[category] = found
                    expertise_score += len(found)
            
            # Determine expertise level
            if expertise_score >= 15:
                level = "Expert"
            elif expertise_score >= 10:
                level = "Advanced"
            elif expertise_score >= 5:
                level = "Intermediate"
            else:
                level = "Entry"
            
            return json.dumps({
                "methodologies_found": found_methods,
                "expertise_score": expertise_score,
                "expertise_level": level,
                "recommendation": self._get_methodology_recommendation(level, found_methods)
            })
            
        except Exception as e:
            return f"Error checking methodology: {str(e)}"
    
    def _get_methodology_recommendation(self, level: str, methods: Dict) -> str:
        """Provide methodology recommendations"""
        
        if level == "Expert":
            return "Strong methodology background - emphasize advanced techniques"
        elif level == "Advanced":
            return "Good foundation - highlight specialized methods you've used"
        elif level == "Intermediate":
            return "Solid basics - focus on practical applications"
        else:
            return "Consider emphasizing any statistical work you've done"
    
    def _analyze_survey_design(self, input_data: str) -> str:
        """Assess survey design and sampling experience"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            survey_keywords = {
                "design": ["questionnaire", "survey design", "instrument", "validation", "pilot"],
                "sampling": ["sample size", "sampling frame", "response rate", "non-response", "weights"],
                "collection": ["cati", "capi", "web survey", "mail survey", "field work"],
                "quality": ["data quality", "editing", "imputation", "disclosure", "confidentiality"],
                "federal": ["census", "acs", "cps", "nhis", "nhanes", "brfss"]
            }
            
            survey_experience = {}
            total_keywords = 0
            
            for category, keywords in survey_keywords.items():
                found = [k for k in keywords if k in experience]
                if found:
                    survey_experience[category] = found
                    total_keywords += len(found)
            
            # Check for specific federal survey experience
            federal_surveys = ["census", "american community survey", "current population survey",
                             "national health interview survey", "nhanes", "brfss"]
            
            federal_exp = [s for s in federal_surveys if s in experience]
            
            return json.dumps({
                "survey_experience": survey_experience,
                "federal_surveys": federal_exp,
                "experience_depth": "Strong" if total_keywords >= 8 else "Moderate" if total_keywords >= 4 else "Limited",
                "federal_alignment": len(federal_exp) > 0,
                "recommendation": "Emphasize federal survey experience" if federal_exp else "Relate experience to federal survey methods"
            })
            
        except Exception as e:
            return f"Error analyzing survey experience: {str(e)}"
    
    def _validate_statistical_software(self, input_data: str) -> str:
        """Check proficiency in statistical software"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            skills = [s.lower() for s in data.get("skills", [])]
            experience = data.get("experience", "").lower()
            
            # Federal agencies' preferred software
            software_tiers = {
                "critical": {
                    "SAS": ["sas", "proc sql", "sas macro", "sas/stat"],
                    "R": ["r programming", "rstudio", "tidyverse", "ggplot"],
                    "Python": ["python", "pandas", "scipy", "statsmodels"]
                },
                "important": {
                    "SPSS": ["spss", "spss syntax"],
                    "Stata": ["stata", "stata programming"],
                    "SQL": ["sql", "postgresql", "mysql", "oracle"]
                },
                "valuable": {
                    "Tableau": ["tableau", "data visualization"],
                    "Excel": ["excel", "vba", "pivot tables"],
                    "MATLAB": ["matlab", "statistical toolbox"]
                }
            }
            
            proficiency = {}
            software_score = 0
            
            combined_text = " ".join(skills) + " " + experience
            
            for tier, software_list in software_tiers.items():
                for software, keywords in software_list.items():
                    if any(kw in combined_text for kw in keywords):
                        proficiency[software] = tier
                        software_score += 3 if tier == "critical" else 2 if tier == "important" else 1
            
            # Federal preference assessment
            has_sas = "SAS" in proficiency
            has_r = "R" in proficiency
            
            federal_readiness = "High" if has_sas else "Medium" if has_r else "Low"
            
            return json.dumps({
                "software_proficiency": proficiency,
                "software_score": software_score,
                "federal_readiness": federal_readiness,
                "sas_proficient": has_sas,
                "recommendation": self._get_software_recommendation(has_sas, has_r, proficiency)
            })
            
        except Exception as e:
            return f"Error validating software: {str(e)}"
    
    def _get_software_recommendation(self, has_sas: bool, has_r: bool, proficiency: Dict) -> str:
        """Provide software recommendations"""
        
        if has_sas:
            return "Excellent - SAS is heavily used in federal statistics"
        elif has_r:
            return "Good - R is increasingly adopted, but consider learning SAS"
        elif proficiency:
            return "Consider highlighting transferable skills to SAS/R"
        else:
            return "Federal positions strongly prefer SAS or R experience"
    
    def _scan_research_experience(self, input_data: str) -> str:
        """Evaluate research and publication record"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            publications = data.get("publications", [])
            experience = data.get("experience", "")
            
            research_indicators = {
                "peer_reviewed": ["journal", "peer-reviewed", "published", "forthcoming"],
                "government": ["technical report", "statistical brief", "working paper", "bulletin"],
                "conference": ["conference", "proceedings", "presentation", "poster"],
                "methodology": ["methodology", "methods", "technique", "algorithm"],
                "policy": ["policy", "evaluation", "assessment", "impact"]
            }
            
            research_profile = {
                "total_publications": len(publications),
                "research_types": [],
                "methodology_focus": False,
                "policy_relevance": False
            }
            
            # Analyze publications
            for pub in publications:
                pub_text = (pub.get("title", "") + " " + pub.get("venue", "")).lower()
                
                for category, keywords in research_indicators.items():
                    if any(kw in pub_text for kw in keywords):
                        if category not in research_profile["research_types"]:
                            research_profile["research_types"].append(category)
                        
                        if category == "methodology":
                            research_profile["methodology_focus"] = True
                        elif category == "policy":
                            research_profile["policy_relevance"] = True
            
            # Assess research strength
            if research_profile["total_publications"] >= 5:
                strength = "Strong"
            elif research_profile["total_publications"] >= 2:
                strength = "Moderate"
            else:
                strength = "Limited"
            
            return json.dumps({
                "research_profile": research_profile,
                "research_strength": strength,
                "federal_alignment": research_profile["policy_relevance"] or "government" in research_profile["research_types"],
                "recommendation": self._get_research_recommendation(strength, research_profile)
            })
            
        except Exception as e:
            return f"Error scanning research: {str(e)}"
    
    def _get_research_recommendation(self, strength: str, profile: Dict) -> str:
        """Provide research recommendations"""
        
        if strength == "Strong" and profile["policy_relevance"]:
            return "Excellent research background for federal statistics"
        elif strength == "Strong":
            return "Strong research - emphasize policy applications"
        elif strength == "Moderate":
            return "Highlight any government or policy-relevant research"
        else:
            return "Focus on analytical projects if limited publications"
    
    def _match_agency_requirements(self, input_data: str) -> str:
        """Match experience to specific agency needs"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            target_agency = data.get("target_agency", "").lower()
            
            agency_profiles = {
                "census": {
                    "keywords": ["population", "demographic", "survey", "acs", "decennial", "geography"],
                    "focus": "Population statistics and survey methodology"
                },
                "bls": {
                    "keywords": ["employment", "labor", "wages", "cpi", "inflation", "productivity"],
                    "focus": "Labor economics and price statistics"
                },
                "nchs": {
                    "keywords": ["health", "vital", "mortality", "disease", "surveillance", "epidemiology"],
                    "focus": "Health statistics and vital records"
                },
                "bea": {
                    "keywords": ["gdp", "economic", "accounts", "trade", "regional", "input-output"],
                    "focus": "Economic accounts and regional analysis"
                },
                "usda": {
                    "keywords": ["agriculture", "farm", "rural", "food", "nutrition", "crop"],
                    "focus": "Agricultural economics and rural statistics"
                }
            }
            
            matches = {}
            
            for agency, profile in agency_profiles.items():
                keyword_matches = sum(1 for kw in profile["keywords"] if kw in experience)
                if keyword_matches > 0:
                    matches[agency] = {
                        "match_count": keyword_matches,
                        "focus": profile["focus"],
                        "strength": "Strong" if keyword_matches >= 3 else "Moderate" if keyword_matches >= 1 else "Weak"
                    }
            
            # Best match
            if matches:
                best_match = max(matches.items(), key=lambda x: x[1]["match_count"])
                best_agency = best_match[0].upper()
            else:
                best_agency = "General federal statistics"
            
            return json.dumps({
                "agency_matches": matches,
                "best_match": best_agency,
                "targeted_match": matches.get(target_agency, {}) if target_agency else None,
                "recommendation": f"Strong alignment with {best_agency}" if matches else "Focus on general federal statistical experience"
            })
            
        except Exception as e:
            return f"Error matching agencies: {str(e)}"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze candidate profile for statistician positions
        """
        
        try:
            # Extract candidate information
            skills = data.get("skills", [])
            experience = data.get("experience", "")
            publications = data.get("publications", [])
            education = data.get("education", {})
            target_grade = data.get("target_grade", "GS-12")
            target_agency = data.get("target_agency", "")
            
            # Build analysis query
            query = f"""
            Analyze this candidate for a {target_grade} Statistician (1530) position:
            
            Skills: {', '.join(skills)}
            
            Experience Summary: {experience[:500]}
            
            Education: {education.get('degree', 'Unknown')} in {education.get('field', 'Unknown')}
            
            Publications: {len(publications)} research items
            
            Target Agency: {target_agency if target_agency else 'Any federal statistical agency'}
            
            Provide:
            1. Statistical methodology assessment
            2. Survey experience evaluation
            3. Software proficiency check
            4. Research strength analysis
            5. Agency alignment recommendations
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add specific recommendations
                response.data["recommendations"] = {
                    "immediate_actions": [
                        "Review your statistical methodology experience",
                        "Document any survey or sampling work",
                        "Highlight SAS or R proficiency prominently"
                    ],
                    "federal_tips": [
                        "Emphasize any government data work",
                        "Mention experience with large datasets",
                        "Include quality control and documentation experience"
                    ],
                    "merit_hiring_tips": [
                        "Use examples from survey or research projects",
                        "Quantify impact of statistical analyses",
                        "Show experience with federal data standards"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
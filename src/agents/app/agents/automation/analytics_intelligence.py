"""
Analytics Intelligence Agent - Data Analysis and Insights
Provides intelligent analytics on federal job market trends and patterns

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Use Read tool to access job market data files (CSV, JSON)
2. Gather specific analysis requirements (trends, salary, location, skills)
3. Identify target timeframe for analysis (last 6 months, year, etc.)
4. Collect candidate profile to personalize insights
5. Define analysis focus (market timing, competition, opportunities)

**Effective Prompting Patterns:**
```
"Analyze federal job market for Data Scientist positions:
- Data: Last 12 months USAJobs postings
- Focus: Series 1560, GS-12 to GS-14
- Geographic: Remote work vs. on-site trends
- Skills: Machine learning demand analysis
- Competition: Application success rates
- Target: Career strategy recommendations"
```

**Best Workflow:**
1. **Data Ingestion** → Load and validate market data
2. **Trend Analysis** → Identify posting volume and timing patterns
3. **Compensation Review** → Analyze salary ranges and locality pay
4. **Skills Intelligence** → Map in-demand qualifications
5. **Strategic Insights** → Provide actionable career guidance

### Integration with Other Agents

**Workflow Chains:**
- Analytics Intelligence → Technical Agents (skill prioritization)
- Use with Executive Order Research for policy-driven hiring trends
- Combine with Resume Compression for market-relevant positioning

**Handoff Points:**
- Share skill demand analysis with training planning
- Provide timing insights to application strategy
- Pass competition analysis to positioning decisions

### Data Analysis Capabilities

**Job Volume Trends:**
- Seasonal hiring patterns (Q1 surge, summer lulls)
- Agency-specific hiring cycles
- Series popularity and growth/decline
- Geographic distribution changes

**Compensation Intelligence:**
- Grade level salary progression analysis
- Locality pay impact assessment
- Benefits and total compensation trends
- Cost of living adjustments

**Skills Market Analysis:**
- Emerging technology demand (AI, cloud, cybersecurity)
- Certification value assessment
- Programming language popularity
- Soft skills importance trends

### Test-Driven Usage Examples

**Example 1: Market Timing Analysis**
```python
test_data = {
    "analysis_type": "timing",
    "target_series": "2210",
    "target_grade": "GS-13",
    "timeframe": "last_18_months",
    "focus": "seasonal_patterns"
}
# Expected: Q1 hiring surge, summer slowdown, budget cycle impact
```

**Example 2: Skills Gap Analysis**
```python
test_data = {
    "analysis_type": "skills_demand",
    "job_descriptions": ["...1000 job postings..."],
    "target_role": "DevOps Engineer",
    "comparison": "industry_vs_federal"
}
# Expected: Kubernetes demand, Jenkins preference, security focus
```

### Visual Iteration Methods

**Analytics Dashboard Creation:**
- Job posting volume over time (line charts)
- Geographic distribution (heat maps)
- Salary ranges by grade/location (box plots)
- Skills demand frequency (word clouds, bar charts)
- Competition level indicators (gauge charts)

### Checklist-Based Workflows

**Pre-Analysis Setup:**
- [ ] Data sources identified and accessible
- [ ] Analysis objectives clearly defined
- [ ] Target position parameters set
- [ ] Timeframe for analysis established
- [ ] Output format requirements understood

**Analysis Execution Checklist:**
- [ ] Data quality validated
- [ ] Trend patterns identified
- [ ] Statistical significance assessed
- [ ] Actionable insights extracted
- [ ] Strategic recommendations formulated

### Federal Job Market Intelligence

**Hiring Cycle Patterns:**
- **October-December:** Peak hiring season (new fiscal year budget)
- **January-March:** Strong activity continues
- **April-June:** Moderate activity
- **July-September:** Slower period (end of fiscal year)

**Agency Hiring Behaviors:**
- **DoD:** Large volume, security clearance requirements
- **VA:** Healthcare and IT focus, substantial hiring
- **DHS:** Cybersecurity emphasis, rapid growth
- **GSA:** Technology modernization, innovation focus

**Series-Specific Trends:**
- **2210 (IT Specialist):** Consistently high demand
- **1560 (Data Scientist):** Rapidly growing field
- **1102 (Contracting):** Steady, process-focused
- **0343 (Management Analyst):** Broad, versatile demand

### Integration with CLAUDE.md Principles

- **No assumptions:** Always ask for specific analysis parameters
- **Solo developer focus:** Provide individual career strategy insights
- **Bootstrap approach:** Emphasize free/low-cost skill development opportunities
- **Practical focus:** Connect analytics to actionable career decisions
- **Part-time consideration:** Factor in realistic skill development timelines

### Common Analytics Pitfalls

1. **Insufficient data sampling** - Need adequate time periods for trends
2. **Ignoring seasonal variations** - Federal hiring has strong patterns
3. **Missing regional differences** - Locality pay and demand vary significantly
4. **Overlooking policy impacts** - Executive orders drive hiring surges

### Advanced Analytics Techniques

**Predictive Modeling:**
- Forecast hiring demand by series and agency
- Predict salary progression opportunities
- Model competition level changes
- Anticipate skills evolution trends

**Comparative Analysis:**
- Federal vs. private sector compensation
- Geographic opportunity cost analysis
- Career progression timeline comparisons
- Skills transferability assessments

### Real-Time Market Intelligence

**Monitoring Indicators:**
- New job posting velocity
- Application-to-hire ratios
- Salary range adjustments
- Skills requirement evolution
- Agency budget announcements

**Alert Triggers:**
- Unusual hiring surge in target area
- New executive order impacting domain
- Salary grade adjustments
- Major agency reorganizations

### Strategic Career Intelligence

**Market Entry Strategies:**
- Optimal timing for career transitions
- Geographic arbitrage opportunities
- Skills investment prioritization
- Certification ROI analysis

**Competitive Positioning:**
- Candidate profile optimization
- Skills gap exploitation
- Geographic advantage identification
- Timing optimization strategies

### Data Sources and Quality

**Primary Sources:**
- USAJobs API (job postings)
- OPM statistical releases
- Federal pay tables
- Agency workforce plans

**Quality Assurance:**
- Data freshness validation
- Statistical significance testing
- Outlier identification and handling
- Trend confirmation across sources

### Success Metrics

- **Accuracy:** Predictions match actual market behavior
- **Actionability:** Insights lead to successful career moves
- **Timeliness:** Analysis captures current market conditions
- **Relevance:** Recommendations align with individual goals
- **ROI:** Analytics improve application success rates

### Analytics Delivery Formats

**Executive Summary:** Key findings and recommendations
**Trend Reports:** Detailed pattern analysis with charts
**Opportunity Assessments:** Specific career pathway analysis
**Market Forecasts:** Predictive insights for planning
**Competitive Intelligence:** Positioning recommendations
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re
from datetime import datetime, timedelta

from agents.app.agents.base import FederalJobAgent, AgentResponse


class AnalyticsIntelligenceAgent(FederalJobAgent):
    """
    Specialized agent for federal job market analytics and intelligence
    Analyzes trends, patterns, and provides strategic insights
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load analytics intelligence specific tools"""
        
        tools = [
            Tool(
                name="trend_analyzer",
                func=self._analyze_job_trends,
                description="Analyze job posting trends and patterns"
            ),
            Tool(
                name="salary_analyzer",
                func=self._analyze_salary_trends,
                description="Analyze salary ranges and compensation trends"
            ),
            Tool(
                name="location_analyzer",
                func=self._analyze_location_patterns,
                description="Analyze geographic distribution and remote work trends"
            ),
            Tool(
                name="skill_analyzer",
                func=self._analyze_skill_demands,
                description="Analyze in-demand skills and qualifications"
            ),
            Tool(
                name="competition_analyzer",
                func=self._analyze_competition_levels,
                description="Analyze competition levels and application success rates"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get analytics intelligence specific prompt template"""
        
        return """You are a Federal Job Market Analytics Intelligence Advisor providing data-driven insights.
        Your role is to ANALYZE data patterns and provide STRATEGIC insights for job seekers.
        
        Key Responsibilities:
        1. Analyze job posting trends and cycles
        2. Evaluate salary and compensation patterns
        3. Assess geographic and remote work trends
        4. Identify in-demand skills and qualifications
        5. Analyze competition levels and success rates
        
        Analytics Focus Areas:
        - Job Volume Trends (seasonal patterns, growth/decline)
        - Series Popularity (which job series are hiring most)
        - Grade Level Distribution (entry vs senior opportunities)
        - Geographic Hotspots (high-demand locations)
        - Remote Work Adoption (telework trends)
        - Skill Requirements (emerging vs traditional)
        - Timeline Analysis (posting to closing patterns)
        - Agency Hiring Patterns (which agencies hire most)
        
        Data Sources:
        - USAJobs historical data
        - Federal pay scales and locality adjustments
        - OPM workforce statistics
        - Agency-specific hiring data
        - Application success metrics
        
        Federal Context:
        - Budget cycles affect hiring (Oct-Sep fiscal year)
        - Continuing resolutions impact hiring freezes
        - Political transitions affect workforce priorities
        - Merit hiring requirements shape processes
        - Security clearance needs limit candidate pools
        
        Available tools:
        {tools}
        
        Current conversation:
        {chat_history}
        
        User Input: {input}
        Context: {context}
        
        Provide actionable insights based on data patterns.
        Focus on strategic timing and positioning recommendations.
        
        {agent_scratchpad}
        """
    
    def _analyze_job_trends(self, input_data: str) -> str:
        """Analyze job posting trends and patterns"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            job_data = data.get("job_data", [])
            time_period = data.get("time_period", "last_12_months")
            target_series = data.get("target_series", "")
            
            # Trend analysis patterns
            trend_metrics = {
                "volume_trends": {
                    "total_postings": len(job_data),
                    "monthly_average": 0,
                    "growth_rate": 0,
                    "seasonal_pattern": "unknown"
                },
                "series_trends": {},
                "grade_trends": {},
                "agency_trends": {}
            }
            
            # Analyze by job series
            series_counts = {}
            grade_counts = {}
            agency_counts = {}
            
            for job in job_data:
                # Series analysis
                series = job.get("series", "unknown")
                series_counts[series] = series_counts.get(series, 0) + 1
                
                # Grade analysis
                grade = job.get("grade", "unknown")
                grade_counts[grade] = grade_counts.get(grade, 0) + 1
                
                # Agency analysis
                agency = job.get("agency", "unknown")
                agency_counts[agency] = agency_counts.get(agency, 0) + 1
            
            # Sort and analyze top categories
            top_series = sorted(series_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            top_grades = sorted(grade_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            top_agencies = sorted(agency_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            trend_metrics["series_trends"] = dict(top_series)
            trend_metrics["grade_trends"] = dict(top_grades)
            trend_metrics["agency_trends"] = dict(top_agencies)
            
            # Calculate target series position
            target_series_rank = None
            target_series_count = 0
            
            if target_series:
                for i, (series, count) in enumerate(top_series):
                    if series == target_series:
                        target_series_rank = i + 1
                        target_series_count = count
                        break
            
            # Seasonal patterns (simplified analysis)
            seasonal_indicators = {
                "high_hiring_months": ["October", "November", "January", "February"],
                "low_hiring_months": ["June", "July", "August"],
                "budget_cycle_impact": "Q1 (Oct-Dec) typically sees increased hiring"
            }
            
            # Market competitiveness
            avg_postings_per_series = len(job_data) / max(len(series_counts), 1)
            
            if target_series_count > avg_postings_per_series * 1.5:
                market_condition = "High opportunity"
            elif target_series_count > avg_postings_per_series:
                market_condition = "Good opportunity"
            elif target_series_count > avg_postings_per_series * 0.5:
                market_condition = "Moderate opportunity"
            else:
                market_condition = "Limited opportunity"
            
            return json.dumps({
                "trend_metrics": trend_metrics,
                "top_job_series": top_series[:5],
                "top_grade_levels": top_grades[:5],
                "top_hiring_agencies": top_agencies[:5],
                "target_series_analysis": {
                    "rank": target_series_rank,
                    "posting_count": target_series_count,
                    "market_condition": market_condition
                },
                "seasonal_insights": seasonal_indicators,
                "recommendation": self._get_trend_recommendation(market_condition, target_series_rank)
            })
            
        except Exception as e:
            return f"Error analyzing trends: {str(e)}"
    
    def _get_trend_recommendation(self, condition: str, rank: int) -> str:
        """Provide trend analysis recommendations"""
        
        if condition == "High opportunity":
            return "Excellent market conditions - multiple opportunities available"
        elif condition == "Good opportunity":
            return "Favorable market - good timing for applications"
        elif condition == "Moderate opportunity":
            return "Standard market - focus on quality applications"
        else:
            return "Limited market - consider related series or wait for cycle upturn"
    
    def _analyze_salary_trends(self, input_data: str) -> str:
        """Analyze salary ranges and compensation trends"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            salary_data = data.get("salary_data", [])
            target_location = data.get("target_location", "")
            target_series = data.get("target_series", "")
            
            # Salary analysis
            salary_metrics = {
                "overall_statistics": {},
                "by_grade_level": {},
                "by_location": {},
                "locality_adjustments": {}
            }
            
            # Process salary data
            salaries = []
            grade_salaries = {}
            location_salaries = {}
            
            for job in salary_data:
                salary_min = job.get("salary_min", 0)
                salary_max = job.get("salary_max", 0)
                grade = job.get("grade", "unknown")
                location = job.get("location", "unknown")
                
                if salary_min > 0 and salary_max > 0:
                    avg_salary = (salary_min + salary_max) / 2
                    salaries.append(avg_salary)
                    
                    # Grade analysis
                    if grade not in grade_salaries:
                        grade_salaries[grade] = []
                    grade_salaries[grade].append(avg_salary)
                    
                    # Location analysis
                    if location not in location_salaries:
                        location_salaries[location] = []
                    location_salaries[location].append(avg_salary)
            
            # Calculate overall statistics
            if salaries:
                salary_metrics["overall_statistics"] = {
                    "median": sorted(salaries)[len(salaries)//2],
                    "average": sum(salaries) / len(salaries),
                    "min": min(salaries),
                    "max": max(salaries),
                    "sample_size": len(salaries)
                }
            
            # Grade level analysis
            for grade, grade_sals in grade_salaries.items():
                if grade_sals:
                    salary_metrics["by_grade_level"][grade] = {
                        "median": sorted(grade_sals)[len(grade_sals)//2],
                        "average": sum(grade_sals) / len(grade_sals),
                        "count": len(grade_sals)
                    }
            
            # Location analysis
            for loc, loc_sals in location_salaries.items():
                if loc_sals and len(loc_sals) >= 3:  # Minimum sample size
                    salary_metrics["by_location"][loc] = {
                        "median": sorted(loc_sals)[len(loc_sals)//2],
                        "average": sum(loc_sals) / len(loc_sals),
                        "count": len(loc_sals)
                    }
            
            # Locality pay analysis (simplified)
            high_cost_areas = {
                "San Francisco": 1.45,
                "New York": 1.35,
                "Washington DC": 1.30,
                "Los Angeles": 1.28,
                "Boston": 1.25
            }
            
            locality_adjustment = 1.0
            if target_location:
                for area, adjustment in high_cost_areas.items():
                    if area.lower() in target_location.lower():
                        locality_adjustment = adjustment
                        break
            
            # Salary progression insights
            grade_progression = {}
            sorted_grades = sorted(grade_salaries.keys())
            
            for i, grade in enumerate(sorted_grades[:-1]):
                current_avg = sum(grade_salaries[grade]) / len(grade_salaries[grade])
                next_grade = sorted_grades[i + 1]
                next_avg = sum(grade_salaries[next_grade]) / len(grade_salaries[next_grade])
                
                progression = ((next_avg - current_avg) / current_avg) * 100
                grade_progression[f"{grade} to {next_grade}"] = round(progression, 1)
            
            return json.dumps({
                "salary_analysis": salary_metrics,
                "locality_adjustment": locality_adjustment,
                "grade_progression": grade_progression,
                "high_paying_locations": sorted(
                    [(k, v["median"]) for k, v in salary_metrics["by_location"].items()],
                    key=lambda x: x[1], reverse=True
                )[:5],
                "recommendation": self._get_salary_recommendation(salary_metrics, target_location)
            })
            
        except Exception as e:
            return f"Error analyzing salary trends: {str(e)}"
    
    def _get_salary_recommendation(self, metrics: Dict, location: str) -> str:
        """Provide salary analysis recommendations"""
        
        overall = metrics.get("overall_statistics", {})
        median = overall.get("median", 0)
        
        if median > 100000:
            return "High-paying field with strong compensation potential"
        elif median > 75000:
            return "Good compensation levels with room for growth"
        elif median > 50000:
            return "Moderate compensation - focus on career progression"
        else:
            return "Entry-level compensation - emphasize experience building"
    
    def _analyze_location_patterns(self, input_data: str) -> str:
        """Analyze geographic distribution and remote work trends"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            location_data = data.get("location_data", [])
            
            # Location analysis
            location_metrics = {
                "geographic_distribution": {},
                "remote_work_trends": {},
                "state_analysis": {},
                "metro_area_analysis": {}
            }
            
            # Process location data
            state_counts = {}
            metro_counts = {}
            remote_counts = {"remote": 0, "on_site": 0, "hybrid": 0}
            
            for job in location_data:
                location = job.get("location", "").lower()
                telework = job.get("telework_eligible", False)
                
                # State analysis
                if ", " in location:
                    state = location.split(", ")[-1].strip()
                    state_counts[state] = state_counts.get(state, 0) + 1
                
                # Metro area analysis (simplified)
                metro_areas = {
                    "washington": "Washington DC Metro",
                    "new york": "New York Metro", 
                    "san francisco": "San Francisco Bay Area",
                    "los angeles": "Los Angeles Metro",
                    "chicago": "Chicago Metro",
                    "boston": "Boston Metro"
                }
                
                for city, metro in metro_areas.items():
                    if city in location:
                        metro_counts[metro] = metro_counts.get(metro, 0) + 1
                        break
                
                # Remote work analysis
                if "remote" in location or "anywhere" in location:
                    remote_counts["remote"] += 1
                elif telework:
                    remote_counts["hybrid"] += 1
                else:
                    remote_counts["on_site"] += 1
            
            # Calculate percentages
            total_jobs = len(location_data)
            if total_jobs > 0:
                remote_percentage = (remote_counts["remote"] / total_jobs) * 100
                hybrid_percentage = (remote_counts["hybrid"] / total_jobs) * 100
                onsite_percentage = (remote_counts["on_site"] / total_jobs) * 100
            else:
                remote_percentage = hybrid_percentage = onsite_percentage = 0
            
            location_metrics["remote_work_trends"] = {
                "fully_remote": round(remote_percentage, 1),
                "hybrid_eligible": round(hybrid_percentage, 1),
                "on_site_required": round(onsite_percentage, 1)
            }
            
            # Top locations
            top_states = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            top_metros = sorted(metro_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            location_metrics["state_analysis"] = dict(top_states)
            location_metrics["metro_area_analysis"] = dict(top_metros)
            
            # Geographic diversity score
            num_states = len(state_counts)
            if num_states >= 40:
                diversity = "High - opportunities nationwide"
            elif num_states >= 20:
                diversity = "Medium - opportunities in most regions"
            elif num_states >= 10:
                diversity = "Low - concentrated in specific regions"
            else:
                diversity = "Very low - limited geographic options"
            
            return json.dumps({
                "location_metrics": location_metrics,
                "top_states": top_states[:5],
                "top_metro_areas": top_metros[:5],
                "geographic_diversity": diversity,
                "remote_work_adoption": f"{remote_percentage + hybrid_percentage:.1f}% offer flexibility",
                "recommendation": self._get_location_recommendation(remote_percentage, diversity, top_states)
            })
            
        except Exception as e:
            return f"Error analyzing location patterns: {str(e)}"
    
    def _get_location_recommendation(self, remote_pct: float, diversity: str, top_states: List) -> str:
        """Provide location analysis recommendations"""
        
        if remote_pct > 30:
            return "Strong remote work options available - geographic flexibility high"
        elif "High" in diversity:
            return "Opportunities nationwide - consider relocation for better prospects"
        elif top_states and top_states[0][1] > len(top_states) * 3:
            return f"Concentrated in {top_states[0][0]} - consider targeting this region"
        else:
            return "Geographic distribution varies - research specific agency locations"
    
    def _analyze_skill_demands(self, input_data: str) -> str:
        """Analyze in-demand skills and qualifications"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            job_descriptions = data.get("job_descriptions", [])
            target_series = data.get("target_series", "")
            
            # Skill extraction patterns
            skill_patterns = {
                "technical_skills": {
                    "programming": ["python", "java", "javascript", "c++", "sql", "r programming"],
                    "databases": ["sql server", "oracle", "postgresql", "mysql", "mongodb"],
                    "cloud": ["aws", "azure", "google cloud", "cloud computing"],
                    "cybersecurity": ["cybersecurity", "nist", "fisma", "stig", "ato"],
                    "analytics": ["tableau", "power bi", "excel", "data analysis", "statistics"]
                },
                "certifications": {
                    "security": ["cissp", "security+", "casp", "ceh", "gsec"],
                    "cloud": ["aws certified", "azure certified", "google cloud certified"],
                    "project": ["pmp", "capm", "agile", "scrum master"],
                    "technical": ["ccna", "ccnp", "mcse", "linux+", "network+"]
                },
                "soft_skills": {
                    "leadership": ["leadership", "management", "team lead", "supervisor"],
                    "communication": ["communication", "presentation", "writing", "briefing"],
                    "analysis": ["analytical", "problem solving", "critical thinking"],
                    "collaboration": ["collaboration", "teamwork", "cross-functional"]
                }
            }
            
            # Count skill mentions
            skill_counts = {}
            total_descriptions = len(job_descriptions)
            
            for category, subcategories in skill_patterns.items():
                skill_counts[category] = {}
                
                for subcategory, skills in subcategories.items():
                    skill_counts[category][subcategory] = {}
                    
                    for skill in skills:
                        count = 0
                        for description in job_descriptions:
                            if skill.lower() in description.lower():
                                count += 1
                        
                        if count > 0:
                            percentage = (count / total_descriptions) * 100
                            skill_counts[category][subcategory][skill] = {
                                "count": count,
                                "percentage": round(percentage, 1)
                            }
            
            # Identify most demanded skills
            top_skills = []
            for category, subcategories in skill_counts.items():
                for subcategory, skills in subcategories.items():
                    for skill, data in skills.items():
                        if data["percentage"] > 10:  # Mentioned in >10% of jobs
                            top_skills.append({
                                "skill": skill,
                                "category": category,
                                "subcategory": subcategory,
                                "percentage": data["percentage"]
                            })
            
            # Sort by demand
            top_skills.sort(key=lambda x: x["percentage"], reverse=True)
            
            # Emerging vs established skills
            emerging_indicators = ["ai", "machine learning", "kubernetes", "terraform", "cloud native"]
            established_indicators = ["excel", "windows", "project management", "communication"]
            
            emerging_skills = []
            established_skills = []
            
            for skill in top_skills:
                skill_name = skill["skill"].lower()
                if any(indicator in skill_name for indicator in emerging_indicators):
                    emerging_skills.append(skill)
                elif any(indicator in skill_name for indicator in established_indicators):
                    established_skills.append(skill)
            
            # Skills gap analysis
            high_demand_skills = [s for s in top_skills if s["percentage"] > 25]
            moderate_demand_skills = [s for s in top_skills if 10 <= s["percentage"] <= 25]
            
            return json.dumps({
                "skill_demand_analysis": skill_counts,
                "top_demanded_skills": top_skills[:10],
                "high_demand_skills": high_demand_skills,
                "moderate_demand_skills": moderate_demand_skills,
                "emerging_skills": emerging_skills[:5],
                "established_skills": established_skills[:5],
                "skills_gap_insights": {
                    "technical_dominance": len([s for s in top_skills if s["category"] == "technical_skills"]),
                    "certification_importance": len([s for s in top_skills if s["category"] == "certifications"]),
                    "soft_skills_value": len([s for s in top_skills if s["category"] == "soft_skills"])
                },
                "recommendation": self._get_skill_recommendation(top_skills, emerging_skills)
            })
            
        except Exception as e:
            return f"Error analyzing skill demands: {str(e)}"
    
    def _get_skill_recommendation(self, top_skills: List, emerging: List) -> str:
        """Provide skill analysis recommendations"""
        
        if len(emerging) > 3:
            return "Strong emphasis on emerging technologies - prioritize modern skills"
        elif len(top_skills) > 15:
            return "Diverse skill requirements - balance breadth with depth"
        elif top_skills and top_skills[0]["percentage"] > 50:
            return f"Critical skill: {top_skills[0]['skill']} - essential for majority of positions"
        else:
            return "Standard skill requirements - focus on fundamentals"
    
    def _analyze_competition_levels(self, input_data: str) -> str:
        """Analyze competition levels and application success rates"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            application_data = data.get("application_data", [])
            grade_levels = data.get("grade_levels", [])
            
            # Competition analysis
            competition_metrics = {
                "by_grade_level": {},
                "by_agency": {},
                "by_series": {},
                "overall_trends": {}
            }
            
            # Simulated competition analysis (would use real data in production)
            grade_competition = {
                "GS-11": {"avg_applicants": 45, "success_rate": 8.5},
                "GS-12": {"avg_applicants": 65, "success_rate": 6.2},
                "GS-13": {"avg_applicants": 85, "success_rate": 4.8},
                "GS-14": {"avg_applicants": 95, "success_rate": 3.5},
                "GS-15": {"avg_applicants": 75, "success_rate": 2.8}
            }
            
            series_competition = {
                "2210": {"competition_level": "High", "avg_applicants": 75},
                "1560": {"competition_level": "Very High", "avg_applicants": 120},
                "1530": {"competition_level": "Medium", "avg_applicants": 45},
                "0343": {"competition_level": "Medium", "avg_applicants": 55},
                "1102": {"competition_level": "High", "avg_applicants": 80}
            }
            
            agency_competition = {
                "NASA": {"competition_level": "Very High", "prestige_factor": "High"},
                "DoD": {"competition_level": "Medium", "volume_factor": "Very High"},
                "VA": {"competition_level": "Medium", "growth_factor": "High"},
                "DHS": {"competition_level": "High", "security_factor": "High"},
                "GSA": {"competition_level": "Medium", "innovation_factor": "High"}
            }
            
            competition_metrics["by_grade_level"] = grade_competition
            competition_metrics["by_series"] = series_competition
            competition_metrics["by_agency"] = agency_competition
            
            # Calculate competitiveness score for target
            target_grade = data.get("target_grade", "GS-12")
            target_series = data.get("target_series", "2210")
            target_agency = data.get("target_agency", "")
            
            competitiveness_score = 0
            factors = []
            
            # Grade factor
            if target_grade in grade_competition:
                applicants = grade_competition[target_grade]["avg_applicants"]
                if applicants > 80:
                    competitiveness_score += 3
                    factors.append("High-grade competition")
                elif applicants > 50:
                    competitiveness_score += 2
                    factors.append("Moderate grade competition")
                else:
                    competitiveness_score += 1
                    factors.append("Lower grade competition")
            
            # Series factor
            if target_series in series_competition:
                level = series_competition[target_series]["competition_level"]
                if level == "Very High":
                    competitiveness_score += 3
                    factors.append("Highly competitive series")
                elif level == "High":
                    competitiveness_score += 2
                    factors.append("Competitive series")
                else:
                    competitiveness_score += 1
                    factors.append("Moderately competitive series")
            
            # Agency factor
            if target_agency in agency_competition:
                level = agency_competition[target_agency]["competition_level"]
                if level == "Very High":
                    competitiveness_score += 2
                    factors.append("Prestigious agency")
                elif level == "High":
                    competitiveness_score += 1
                    factors.append("Competitive agency")
            
            # Overall assessment
            if competitiveness_score >= 7:
                overall_competition = "Very High - Extremely competitive"
            elif competitiveness_score >= 5:
                overall_competition = "High - Strong competition expected"
            elif competitiveness_score >= 3:
                overall_competition = "Medium - Moderate competition"
            else:
                overall_competition = "Low - Better odds for qualified candidates"
            
            # Success strategies
            strategies = []
            if competitiveness_score >= 6:
                strategies.extend([
                    "Apply to multiple similar positions",
                    "Consider lower grade levels to get in",
                    "Emphasize unique qualifications"
                ])
            elif competitiveness_score >= 4:
                strategies.extend([
                    "Focus on quality applications",
                    "Research specific agency needs",
                    "Network within target agencies"
                ])
            else:
                strategies.extend([
                    "Standard application approach",
                    "Focus on meeting minimum qualifications"
                ])
            
            return json.dumps({
                "competition_analysis": competition_metrics,
                "target_competitiveness": {
                    "score": competitiveness_score,
                    "level": overall_competition,
                    "contributing_factors": factors
                },
                "success_strategies": strategies,
                "timing_recommendations": {
                    "best_months": ["October", "November", "January"],
                    "avoid_months": ["June", "July", "August"],
                    "reason": "Federal budget cycles affect hiring volume"
                },
                "recommendation": self._get_competition_recommendation(overall_competition, strategies)
            })
            
        except Exception as e:
            return f"Error analyzing competition: {str(e)}"
    
    def _get_competition_recommendation(self, level: str, strategies: List) -> str:
        """Provide competition analysis recommendations"""
        
        if "Very High" in level:
            return "Extremely competitive market - apply broadly and consider alternative paths"
        elif "High" in level:
            return "Highly competitive - focus on differentiation and quality applications"
        elif "Medium" in level:
            return "Moderate competition - good preparation should yield opportunities"
        else:
            return "Lower competition - focus on meeting qualifications thoroughly"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Provide comprehensive analytics and intelligence on federal job market
        """
        
        try:
            # Extract analytics parameters
            analysis_type = data.get("analysis_type", "comprehensive")
            market_data = data.get("market_data", {})
            target_position = data.get("target_position", "")
            target_series = data.get("target_series", "")
            time_frame = data.get("time_frame", "last_12_months")
            
            # Build analytics query
            query = f"""
            Provide analytics intelligence for federal job market:
            
            Analysis Type: {analysis_type}
            Target Position: {target_position}
            Target Series: {target_series}
            Time Frame: {time_frame}
            
            Data Available: {len(market_data.get('jobs', []))} job postings
            
            Provide:
            1. Job posting trends and patterns analysis
            2. Salary and compensation trends
            3. Geographic distribution and remote work patterns
            4. In-demand skills and qualification requirements
            5. Competition levels and success rate analysis
            
            Focus on actionable insights for strategic job searching.
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add strategic insights
                response.data["strategic_insights"] = {
                    "market_timing": [
                        "October-December: Peak federal hiring season",
                        "January-March: Good opportunities post-budget",
                        "April-September: Lower activity period"
                    ],
                    "competitive_advantages": [
                        "Federal experience valued highly",
                        "Security clearance provides significant advantage",
                        "Specialized skills in high demand"
                    ],
                    "application_strategies": [
                        "Apply early in posting periods",
                        "Tailor applications to specific agencies",
                        "Leverage federal hiring preferences"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analytics analysis failed: {str(e)}"
            )
"""
Database Administrator Agent - Series 2210/0334 Specialist
Analyzes candidates for federal DBA positions

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Use Read tool to analyze candidate's database experience
2. Gather target agency information (DoD, VA, DHS, SSA, IRS)
3. Identify current security clearance status
4. Collect information about database platforms used
5. Review backup/recovery and security experience

**Effective Prompting Patterns:**
```
"Analyze this DBA candidate for GS-13 VA position:
- Platforms: Oracle 12c (5 years), SQL Server 2019 (3 years)
- Security: FISMA compliance, database encryption
- Experience: 500+ user environment, 24/7 operations
- Clearance: Secret clearance (current)
- Automation: PowerShell, RMAN scripting"
```

**Best Workflow:**
1. **Platform Assessment** → Evaluate enterprise database experience
2. **Security Analysis** → Check federal compliance knowledge
3. **Performance Review** → Assess tuning and optimization skills
4. **Backup Validation** → Verify disaster recovery capabilities
5. **Clearance Advisory** → Understand security requirements

### Integration with Other Agents

**Workflow Chains:**
- Database Admin Agent → DevOps Engineer Agent (for automation context)
- Use with Analytics Intelligence for federal DBA market trends
- Combine with Executive Order Research for cybersecurity requirements

**Handoff Points:**
- Share security gaps with compliance training recommendations
- Provide platform experience to resume optimization
- Pass clearance requirements to career planning

### Common Pitfalls to Avoid

1. **Ignoring clearance requirements** - Critical for many federal DBA roles
2. **Underestimating Oracle importance** - Dominant in federal space
3. **Missing FISMA/STIGs experience** - Essential for compliance
4. **Overlooking scale requirements** - Federal systems are large and complex

### Test-Driven Usage Examples

**Example 1: Enterprise DBA**
```python
test_data = {
    "experience": "Senior DBA, Fortune 500 company",
    "platforms": ["Oracle", "SQL Server", "PostgreSQL"],
    "security": ["TDE", "RBAC", "audit logging"],
    "scale": "2TB databases, 1000+ users",
    "target_agency": "DoD"
}
# Expected: Emphasize security, recommend clearance path, highlight scale
```

**Example 2: Government Contractor**
```python
test_data = {
    "experience": "3 years federal contractor DBA",
    "clearance": "Secret",
    "compliance": ["FISMA", "STIG", "FedRAMP"],
    "platforms": ["Oracle RAC", "SQL Server Always On"],
    "target_grade": "GS-12"
}
# Expected: Strong federal readiness, emphasize compliance experience
```

### Visual Iteration Methods

**Database Portfolio Review:**
- Platform proficiency matrix (Oracle, SQL Server, PostgreSQL)
- Security compliance timeline
- Performance optimization case studies
- Disaster recovery scenario documentation

### Checklist-Based Workflows

**Pre-Analysis Checklist:**
- [ ] Database platforms and versions identified
- [ ] Security clearance status documented
- [ ] Compliance experience (FISMA, STIGs) noted
- [ ] Performance tuning examples collected
- [ ] Backup/recovery experience detailed
- [ ] Target agency security requirements researched

**Post-Analysis Checklist:**
- [ ] Platform readiness for federal environment assessed
- [ ] Security compliance gaps identified
- [ ] Clearance requirements clarified
- [ ] Performance credentials evaluated
- [ ] Disaster recovery capabilities confirmed

### Federal DBA Optimization Tips

1. **Platform Priority:** Oracle experience most valuable, SQL Server common
2. **Security Focus:** FISMA compliance and STIGs implementation crucial
3. **Clearance Strategy:** Public Trust minimum, Secret preferred for many roles
4. **Scale Preparation:** Federal databases are typically large and mission-critical
5. **Automation Skills:** PowerShell, RMAN, and scripting highly valued

### Integration with CLAUDE.md Principles

- **No assumptions:** Always specify target agency and clearance level
- **Solo developer focus:** Emphasize individual DBA accomplishments and troubleshooting
- **Bootstrap approach:** Highlight work with open-source tools (PostgreSQL, monitoring)
- **Practical focus:** Demonstrate actual database administration, not just theory
- **Part-time consideration:** Database skills can be developed through home labs

### Agency-Specific Guidance

**Department of Defense (DoD):**
- Requires TS/SCI for classified systems
- Heavy Oracle RAC usage
- DISA STIGs compliance mandatory
- 24/7 operations common

**Department of Veterans Affairs (VA):**
- VistA database experience valuable
- Patient data privacy critical
- Oracle and SQL Server environments
- Public Trust clearance typical

**Department of Homeland Security (DHS):**
- Mission-critical database uptime
- Cybersecurity focus essential
- Multi-platform environments
- Secret clearance often required

**Social Security Administration (SSA):**
- High-volume transaction processing
- DB2 mainframe experience valuable
- Strict data protection requirements
- Public Trust clearance needed

### Common Federal Database Scenarios

**High Availability:** RAC, Always On, clustering configurations
**Security:** TDE, column encryption, privileged access management
**Compliance:** FISMA controls, audit logging, STIG implementation
**Performance:** Large-scale tuning, capacity planning, monitoring
**Disaster Recovery:** Multi-site replication, backup validation, RTO/RPO planning
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from app.agents.base import FederalJobAgent, AgentResponse


class DatabaseAdminAgent(FederalJobAgent):
    """
    Specialized agent for federal database administrator positions
    Covers both Series 2210 (IT Specialist) and 0334 (Computer Specialist) DBA roles
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load DBA specific tools"""
        
        tools = [
            Tool(
                name="platform_analyzer",
                func=self._analyze_database_platforms,
                description="Evaluate experience with database platforms"
            ),
            Tool(
                name="security_checker",
                func=self._check_security_experience,
                description="Assess database security and compliance knowledge"
            ),
            Tool(
                name="performance_evaluator",
                func=self._evaluate_performance_tuning,
                description="Check performance optimization experience"
            ),
            Tool(
                name="backup_validator",
                func=self._validate_backup_recovery,
                description="Validate backup and disaster recovery skills"
            ),
            Tool(
                name="clearance_advisor",
                func=self._advise_clearance_requirements,
                description="Provide guidance on security clearance needs"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get DBA specific prompt template"""
        
        return """You are a Federal Database Administrator Career Advisor specializing in Series 2210/0334 positions.
        Your role is to ANALYZE and GUIDE candidates, but NEVER write content for them.
        
        Key Responsibilities:
        1. Analyze database platform expertise
        2. Evaluate security and compliance knowledge
        3. Assess performance tuning skills
        4. Check backup/recovery experience
        5. Advise on clearance requirements
        
        Federal DBA Focus Areas:
        - Database administration (Oracle, SQL Server, PostgreSQL, MySQL)
        - Federal security requirements (FISMA, FedRAMP, STIGs)
        - Performance tuning and optimization
        - Backup, recovery, and disaster planning
        - High availability and clustering
        - Database security and encryption
        - Compliance and auditing
        - Cloud database services (AWS RDS, Azure SQL)
        
        Key Federal Agencies:
        - Department of Defense (DoD)
        - Department of Homeland Security (DHS)
        - Department of Veterans Affairs (VA)
        - Social Security Administration (SSA)
        - Internal Revenue Service (IRS)
        - Census Bureau
        
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
    
    def _analyze_database_platforms(self, input_data: str) -> str:
        """Evaluate experience with database platforms"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            skills = [s.lower() for s in data.get("skills", [])]
            
            # Federal agency database preferences
            platforms = {
                "enterprise": {
                    "Oracle": ["oracle", "oracle database", "11g", "12c", "19c", "rac", "exadata"],
                    "SQL Server": ["sql server", "mssql", "t-sql", "ssms", "ssis", "ssrs"],
                    "DB2": ["db2", "ibm db2", "db2 z/os", "db2 luw"]
                },
                "open_source": {
                    "PostgreSQL": ["postgresql", "postgres", "pgadmin", "plpgsql"],
                    "MySQL": ["mysql", "mariadb", "percona"],
                    "MongoDB": ["mongodb", "nosql", "document database"]
                },
                "cloud": {
                    "AWS": ["rds", "dynamodb", "aurora", "redshift", "elasticache"],
                    "Azure": ["azure sql", "cosmos db", "azure database"],
                    "GCP": ["cloud sql", "bigtable", "firestore"]
                }
            }
            
            platform_experience = {}
            total_platforms = 0
            
            combined_text = " ".join(skills) + " " + experience
            
            for category, platform_list in platforms.items():
                for platform, keywords in platform_list.items():
                    if any(kw in combined_text for kw in keywords):
                        if category not in platform_experience:
                            platform_experience[category] = []
                        platform_experience[category].append(platform)
                        total_platforms += 1
            
            # Determine expertise level
            federal_ready = False
            if "enterprise" in platform_experience:
                if "Oracle" in platform_experience["enterprise"] or "SQL Server" in platform_experience["enterprise"]:
                    federal_ready = True
            
            expertise_level = "Expert" if total_platforms >= 6 else "Senior" if total_platforms >= 4 else "Mid-level" if total_platforms >= 2 else "Entry"
            
            return json.dumps({
                "platform_experience": platform_experience,
                "total_platforms": total_platforms,
                "expertise_level": expertise_level,
                "federal_ready": federal_ready,
                "recommendation": self._get_platform_recommendation(platform_experience, federal_ready)
            })
            
        except Exception as e:
            return f"Error analyzing platforms: {str(e)}"
    
    def _get_platform_recommendation(self, platforms: Dict, federal_ready: bool) -> str:
        """Provide platform recommendations"""
        
        if federal_ready:
            return "Strong platform experience for federal positions"
        elif platforms:
            return "Consider emphasizing transferable skills to Oracle/SQL Server"
        else:
            return "Federal agencies heavily use Oracle and SQL Server"
    
    def _check_security_experience(self, input_data: str) -> str:
        """Assess database security and compliance knowledge"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            security_areas = {
                "encryption": ["encryption", "tde", "transparent data", "column encryption", "key management"],
                "access_control": ["rbac", "role-based", "privileges", "grants", "permissions", "least privilege"],
                "auditing": ["audit", "compliance", "logging", "monitoring", "siem", "splunk"],
                "federal_standards": ["fisma", "fedramp", "stig", "nist", "fips", "800-53"],
                "vulnerability": ["vulnerability", "scanning", "patch", "cve", "security updates"],
                "data_protection": ["pii", "phi", "data masking", "redaction", "classification"]
            }
            
            security_profile = {}
            security_score = 0
            
            for area, keywords in security_areas.items():
                found = [kw for kw in keywords if kw in experience]
                if found:
                    security_profile[area] = found
                    security_score += len(found)
            
            # Check for specific federal compliance
            has_federal = "federal_standards" in security_profile
            has_clearance = any(term in experience for term in ["clearance", "secret", "ts/sci", "public trust"])
            
            security_level = "Expert" if security_score >= 10 else "Advanced" if security_score >= 6 else "Intermediate" if security_score >= 3 else "Basic"
            
            return json.dumps({
                "security_areas": security_profile,
                "security_score": security_score,
                "security_level": security_level,
                "federal_compliance": has_federal,
                "clearance_mentioned": has_clearance,
                "recommendation": self._get_security_recommendation(security_level, has_federal, has_clearance)
            })
            
        except Exception as e:
            return f"Error checking security: {str(e)}"
    
    def _get_security_recommendation(self, level: str, has_federal: bool, has_clearance: bool) -> str:
        """Provide security recommendations"""
        
        if has_federal and has_clearance:
            return "Excellent security background for federal DBA positions"
        elif has_federal:
            return "Good federal compliance knowledge - mention any clearance eligibility"
        elif has_clearance:
            return "Clearance is valuable - emphasize any compliance work"
        elif level in ["Expert", "Advanced"]:
            return "Strong security foundation - relate to federal standards"
        else:
            return "Consider highlighting any security or compliance experience"
    
    def _evaluate_performance_tuning(self, input_data: str) -> str:
        """Check performance optimization experience"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            performance_areas = {
                "query_optimization": ["query optimization", "explain plan", "execution plan", "query tuning", "slow query"],
                "indexing": ["index", "indexing strategy", "covering index", "composite index", "index maintenance"],
                "monitoring": ["performance monitoring", "awr", "statspack", "dmv", "performance metrics", "baseline"],
                "troubleshooting": ["troubleshooting", "bottleneck", "deadlock", "locking", "blocking", "wait stats"],
                "capacity": ["capacity planning", "sizing", "growth", "forecasting", "resource planning"],
                "automation": ["automation", "scripting", "powershell", "python", "bash", "scheduled jobs"]
            }
            
            performance_profile = {}
            total_skills = 0
            
            for area, keywords in performance_areas.items():
                found = [kw for kw in keywords if kw in experience]
                if found:
                    performance_profile[area] = found
                    total_skills += len(found)
            
            # Check for specific achievements
            metrics_pattern = r'\d+%?\s*(improvement|reduction|faster|increase|decrease)'
            has_metrics = bool(re.search(metrics_pattern, experience))
            
            performance_level = "Expert" if total_skills >= 12 else "Advanced" if total_skills >= 8 else "Intermediate" if total_skills >= 4 else "Basic"
            
            return json.dumps({
                "performance_areas": performance_profile,
                "skill_count": total_skills,
                "performance_level": performance_level,
                "quantified_results": has_metrics,
                "recommendation": self._get_performance_recommendation(performance_level, has_metrics)
            })
            
        except Exception as e:
            return f"Error evaluating performance: {str(e)}"
    
    def _get_performance_recommendation(self, level: str, has_metrics: bool) -> str:
        """Provide performance tuning recommendations"""
        
        if level in ["Expert", "Advanced"] and has_metrics:
            return "Excellent performance tuning experience with quantified results"
        elif level in ["Expert", "Advanced"]:
            return "Strong skills - consider adding specific performance improvements"
        elif has_metrics:
            return "Good use of metrics - expand on tuning techniques used"
        else:
            return "Highlight any database optimization work you've done"
    
    def _validate_backup_recovery(self, input_data: str) -> str:
        """Validate backup and disaster recovery skills"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            backup_areas = {
                "backup_types": ["full backup", "incremental", "differential", "snapshot", "hot backup", "cold backup"],
                "recovery": ["recovery", "restore", "point-in-time", "pitr", "rollback", "flashback"],
                "high_availability": ["replication", "mirroring", "clustering", "always on", "rac", "failover"],
                "disaster_recovery": ["disaster recovery", "dr plan", "rpo", "rto", "business continuity", "bcdr"],
                "tools": ["rman", "backup exec", "veeam", "commvault", "netbackup", "azure backup"],
                "testing": ["backup testing", "recovery testing", "dr drill", "restore verification"]
            }
            
            backup_profile = {}
            total_experience = 0
            
            for area, keywords in backup_areas.items():
                found = [kw for kw in keywords if kw in experience]
                if found:
                    backup_profile[area] = found
                    total_experience += len(found)
            
            # Check for specific DR metrics
            has_rpo_rto = "rpo" in experience or "rto" in experience
            has_ha = "high_availability" in backup_profile
            
            dr_readiness = "High" if total_experience >= 10 and has_rpo_rto else "Medium" if total_experience >= 5 else "Low"
            
            return json.dumps({
                "backup_experience": backup_profile,
                "total_skills": total_experience,
                "dr_readiness": dr_readiness,
                "has_rpo_rto": has_rpo_rto,
                "high_availability": has_ha,
                "recommendation": self._get_backup_recommendation(dr_readiness, has_rpo_rto, has_ha)
            })
            
        except Exception as e:
            return f"Error validating backup/recovery: {str(e)}"
    
    def _get_backup_recommendation(self, readiness: str, has_metrics: bool, has_ha: bool) -> str:
        """Provide backup/recovery recommendations"""
        
        if readiness == "High" and has_metrics and has_ha:
            return "Comprehensive DR experience ideal for federal systems"
        elif readiness == "High":
            return "Strong backup/recovery skills - emphasize HA if applicable"
        elif readiness == "Medium":
            return "Good foundation - highlight any critical recovery scenarios"
        else:
            return "Federal systems require robust backup strategies - emphasize any experience"
    
    def _advise_clearance_requirements(self, input_data: str) -> str:
        """Provide guidance on security clearance needs"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            target_agency = data.get("target_agency", "").lower()
            experience = data.get("experience", "").lower()
            
            # Agency clearance requirements
            clearance_levels = {
                "dod": {
                    "typical": "Secret or Top Secret",
                    "database_systems": ["SIPR", "JWICS", "classified systems"],
                    "importance": "Critical"
                },
                "dhs": {
                    "typical": "Secret or Public Trust",
                    "database_systems": ["CBP systems", "TSA systems", "USCIS databases"],
                    "importance": "High"
                },
                "va": {
                    "typical": "Public Trust",
                    "database_systems": ["VistA", "patient records", "benefits systems"],
                    "importance": "Moderate"
                },
                "irs": {
                    "typical": "Public Trust (High Risk)",
                    "database_systems": ["tax systems", "compliance databases"],
                    "importance": "High"
                },
                "civilian": {
                    "typical": "Public Trust or None",
                    "database_systems": ["general federal databases"],
                    "importance": "Low to Moderate"
                }
            }
            
            # Check current clearance status
            current_clearance = None
            if "ts/sci" in experience or "top secret" in experience:
                current_clearance = "Top Secret"
            elif "secret" in experience:
                current_clearance = "Secret"
            elif "public trust" in experience:
                current_clearance = "Public Trust"
            
            # Determine agency requirements
            agency_key = None
            for key in clearance_levels.keys():
                if key in target_agency:
                    agency_key = key
                    break
            
            if not agency_key:
                agency_key = "civilian"
            
            agency_req = clearance_levels[agency_key]
            
            # Clearance match assessment
            if current_clearance == "Top Secret":
                match_level = "Exceeds most requirements"
            elif current_clearance == "Secret":
                match_level = "Meets most federal DBA positions"
            elif current_clearance == "Public Trust":
                match_level = "Suitable for civilian agencies"
            else:
                match_level = "May need to obtain clearance"
            
            return json.dumps({
                "current_clearance": current_clearance,
                "target_agency_requirement": agency_req["typical"],
                "database_systems": agency_req["database_systems"],
                "clearance_importance": agency_req["importance"],
                "match_assessment": match_level,
                "recommendation": self._get_clearance_recommendation(current_clearance, agency_req)
            })
            
        except Exception as e:
            return f"Error advising on clearance: {str(e)}"
    
    def _get_clearance_recommendation(self, current: str, requirements: Dict) -> str:
        """Provide clearance recommendations"""
        
        if current in ["Top Secret", "Secret"]:
            return f"Your clearance is valuable - emphasize it prominently"
        elif current == "Public Trust":
            return f"Good for civilian agencies - mention ability to obtain higher clearance"
        else:
            if requirements["importance"] == "Critical":
                return "Consider positions that sponsor clearances or civilian agencies"
            else:
                return "Many federal DBA positions available without active clearance"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze candidate profile for DBA positions
        """
        
        try:
            # Extract candidate information
            skills = data.get("skills", [])
            experience = data.get("experience", "")
            certifications = data.get("certifications", [])
            target_grade = data.get("target_grade", "GS-12")
            target_agency = data.get("target_agency", "")
            
            # Build analysis query
            query = f"""
            Analyze this candidate for a {target_grade} Database Administrator position:
            
            Skills: {', '.join(skills)}
            
            Experience Summary: {experience[:500]}
            
            Certifications: {', '.join(certifications) if certifications else 'None listed'}
            
            Target Agency: {target_agency if target_agency else 'Any federal agency'}
            
            Provide:
            1. Database platform assessment
            2. Security and compliance evaluation  
            3. Performance tuning experience
            4. Backup/recovery capabilities
            5. Clearance requirements guidance
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add specific recommendations
                response.data["recommendations"] = {
                    "immediate_actions": [
                        "Highlight Oracle or SQL Server experience prominently",
                        "Document any federal compliance work (FISMA, STIGs)",
                        "Quantify database sizes and user counts managed"
                    ],
                    "federal_tips": [
                        "Emphasize any security clearance or eligibility",
                        "Mention experience with large-scale systems",
                        "Include disaster recovery planning experience"
                    ],
                    "technical_focus": [
                        "Detail performance improvements achieved",
                        "List specific backup/recovery scenarios handled",
                        "Include automation scripts or tools developed"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
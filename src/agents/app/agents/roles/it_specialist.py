"""
IT Specialist Agent - Series 2210 General Specialist
Analyzes candidates for general federal IT positions

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Use Read tool to examine candidate's broad IT experience
2. Identify target IT specialty (INFOSEC, SYSADMIN, NETWORK, CUSTSPT, etc.)
3. Gather information about target agency and grade level
4. Review certification portfolio and training
5. Assess both technical depth and breadth

**Effective Prompting Patterns:**
```
"Analyze this IT Specialist candidate for GS-12 INFOSEC position:
- Background: 7 years mixed IT experience
- Specialties: Network security, incident response, help desk
- Certifications: Security+, Network+, working on CISSP
- Systems: Windows/Linux, Cisco, firewalls
- Target: DHS cybersecurity role
- Clearance: Public Trust eligible"
```

**Best Workflow:**
1. **Specialty Matching** → Identify primary and secondary IT areas
2. **Systems Analysis** → Evaluate technical platform experience
3. **Network Assessment** → Check networking and security skills
4. **Security Evaluation** → Review cybersecurity knowledge
5. **Support Review** → Assess customer service capabilities

### Integration with Other Agents

**Workflow Chains:**
- IT Specialist Agent → Database Admin Agent (for database-focused roles)
- Use with DevOps Engineer Agent for automation-heavy positions
- Combine with Analytics Intelligence for IT job market trends

**Handoff Points:**
- Share specialty focus areas with targeted training plans
- Provide technical gaps to certification roadmap
- Pass customer service experience to federal service orientation

### Common Pitfalls to Avoid

1. **Forcing single specialty** - IT Specialists often need breadth
2. **Ignoring customer service** - Federal IT requires strong people skills
3. **Missing ITIL/service management** - Process knowledge is crucial
4. **Overlooking compliance awareness** - Federal IT has unique requirements

### Test-Driven Usage Examples

**Example 1: Help Desk Professional**
```python
test_data = {
    "experience": "5 years help desk and desktop support",
    "specialties": ["customer support", "troubleshooting", "Windows/Mac"],
    "certifications": ["A+", "Network+"],
    "soft_skills": ["communication", "patience", "documentation"],
    "target_specialty": "CUSTSPT"
}
# Expected: Strong customer focus, recommend ITIL training
```

**Example 2: Network Administrator**
```python
test_data = {
    "experience": "Network admin at regional ISP",
    "specialties": ["Cisco networking", "firewall management", "VPN"],
    "certifications": ["CCNA", "Security+"],
    "scale": "500+ users, multi-site WAN",
    "target_specialty": "NETWORK"
}
# Expected: Good technical foundation, federal network experience valuable
```

### Visual Iteration Methods

**IT Portfolio Review:**
- Technical skill matrix across specialties
- Certification progression timeline
- Experience breadth vs. depth analysis
- Customer service metrics and feedback

### Checklist-Based Workflows

**Pre-Analysis Checklist:**
- [ ] Primary IT specialty area identified
- [ ] Secondary skills and cross-training noted
- [ ] Certification portfolio documented
- [ ] Customer service experience assessed
- [ ] Technical troubleshooting examples collected
- [ ] Target agency IT environment researched

**Post-Analysis Checklist:**
- [ ] Best-fit specialty area confirmed
- [ ] Technical competency gaps identified
- [ ] Certification roadmap suggested
- [ ] Customer service alignment verified
- [ ] Federal IT readiness assessed

### Federal IT Specialist Optimization Tips

1. **Specialty Strategy:** Choose primary focus but maintain breadth
2. **Certification Path:** Security+ baseline, then specialty certifications
3. **Customer Focus:** Emphasize service delivery and stakeholder communication
4. **Process Knowledge:** ITIL and federal IT service management
5. **Security Awareness:** All IT roles require security consciousness

### Integration with CLAUDE.md Principles

- **No assumptions:** Always ask for target specialty and grade level
- **Solo developer focus:** Emphasize individual troubleshooting and problem-solving
- **Bootstrap approach:** Highlight work with diverse technologies and platforms
- **Practical focus:** Demonstrate actual IT support and system administration
- **Part-time consideration:** IT skills can be developed through home labs and certifications

### IT Specialty Deep Dives

**INFOSEC (Information Security):**
- Security+ certification mandatory
- Incident response experience
- Vulnerability management
- FISMA/NIST framework knowledge

**SYSADMIN (Systems Administration):**
- Windows and/or Linux expertise
- Virtualization and cloud experience
- Automation and scripting
- Performance monitoring and tuning

**NETWORK (Network Services):**
- Cisco networking equipment
- TCP/IP and routing protocols
- Network security implementation
- WAN and VPN technologies

**CUSTSPT (Customer Support):**
- Help desk and ticket management
- End-user training and support
- Service level agreement (SLA) management
- Communication and documentation skills

**DATAMGT (Data Management):**
- Database administration basics
- Data backup and recovery
- Report generation and analysis
- Data quality and governance

### Common Federal IT Scenarios

**Desktop Support:** End-user computing, software deployment, troubleshooting
**Network Operations:** Infrastructure monitoring, incident response, maintenance
**Security Operations:** SOC activities, vulnerability scanning, compliance
**System Administration:** Server management, patch deployment, performance monitoring
**Project Support:** IT implementation, user training, change management

### Career Progression Paths

**Entry Level (GS-7/9):** Help desk, desktop support, junior admin roles
**Mid Level (GS-11/12):** Specialized technical roles, team lead positions
**Senior Level (GS-13/14):** Subject matter expert, project lead, supervisor
**Executive Level (GS-15+):** IT management, program oversight, strategic planning

### Versatility Advantages

**Broad Skills:** Federal IT often requires multi-disciplinary knowledge
**Adaptability:** Government systems are diverse and changing
**Problem Solving:** Complex environments need creative troubleshooting
**Communication:** Technical-to-business translation is crucial
**Service Orientation:** Government serves citizens and mission needs
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from agents.app.agents.base import FederalJobAgent, AgentResponse


class ITSpecialistAgent(FederalJobAgent):
    """
    Specialized agent for federal IT Specialist positions (Series 2210)
    Covers general IT roles including systems, network, cybersecurity, and customer support
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load IT Specialist specific tools"""
        
        tools = [
            Tool(
                name="specialty_matcher",
                func=self._match_it_specialty,
                description="Match experience to IT specialty areas"
            ),
            Tool(
                name="systems_analyzer",
                func=self._analyze_systems_experience,
                description="Evaluate systems administration experience"
            ),
            Tool(
                name="network_checker",
                func=self._check_network_skills,
                description="Assess network administration capabilities"
            ),
            Tool(
                name="security_evaluator",
                func=self._evaluate_cybersecurity,
                description="Check cybersecurity knowledge and practices"
            ),
            Tool(
                name="customer_assessor",
                func=self._assess_customer_support,
                description="Evaluate customer service and support experience"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get IT Specialist specific prompt template"""
        
        return """You are a Federal IT Specialist Career Advisor specializing in Series 2210 positions.
        Your role is to ANALYZE and GUIDE candidates, but NEVER write content for them.
        
        Key Responsibilities:
        1. Match experience to IT specialty areas
        2. Analyze systems administration skills
        3. Evaluate network capabilities
        4. Assess cybersecurity knowledge
        5. Check customer support experience
        
        Federal IT Specialist Focus Areas:
        - Systems Administration (Windows, Linux, VMware)
        - Network Administration (Cisco, routing, switching)
        - Cybersecurity (incident response, vulnerability management)
        - Customer Support (help desk, ticketing, SLAs)
        - Enterprise Applications (Active Directory, Exchange, SharePoint)
        - Cloud Services (M365, AWS, Azure)
        - IT Project Management (ITIL, agile, waterfall)
        - Policy and Compliance (FISMA, Section 508, records management)
        
        IT Specialty Areas (Parentheticals):
        - INFOSEC - Information Security
        - SYSADMIN - Systems Administration  
        - NETWORK - Network Services
        - CUSTSPT - Customer Support
        - DATAMGT - Data Management
        - INTERNET - Internet/Web Services
        - SYSANALYSIS - Systems Analysis
        - APPSW - Applications Software
        
        Key Federal Agencies:
        - All federal agencies employ IT Specialists
        - Large employers: DoD, VA, DHS, Treasury, HHS
        - Tech-focused: NASA, NIST, Patent Office
        
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
    
    def _match_it_specialty(self, input_data: str) -> str:
        """Match experience to IT specialty areas"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            skills = [s.lower() for s in data.get("skills", [])]
            
            # IT Specialty area indicators
            specialties = {
                "INFOSEC": {
                    "keywords": ["security", "vulnerability", "incident response", "siem", "firewall", "ids", "ips", "forensics"],
                    "weight": 0
                },
                "SYSADMIN": {
                    "keywords": ["server", "windows server", "linux", "vmware", "active directory", "group policy", "backup"],
                    "weight": 0
                },
                "NETWORK": {
                    "keywords": ["network", "cisco", "routing", "switching", "tcp/ip", "vlan", "vpn", "wan", "lan"],
                    "weight": 0
                },
                "CUSTSPT": {
                    "keywords": ["help desk", "ticket", "customer service", "troubleshoot", "support", "sla", "end user"],
                    "weight": 0
                },
                "DATAMGT": {
                    "keywords": ["database", "data management", "sql", "etl", "data warehouse", "reporting", "analytics"],
                    "weight": 0
                },
                "INTERNET": {
                    "keywords": ["web", "website", "html", "css", "javascript", "api", "rest", "content management"],
                    "weight": 0
                },
                "SYSANALYSIS": {
                    "keywords": ["requirements", "analysis", "design", "documentation", "process improvement", "workflow"],
                    "weight": 0
                },
                "APPSW": {
                    "keywords": ["application", "software development", "programming", "code", "testing", "deployment"],
                    "weight": 0
                }
            }
            
            combined_text = " ".join(skills) + " " + experience
            
            # Calculate weights for each specialty
            for specialty, info in specialties.items():
                for keyword in info["keywords"]:
                    if keyword in combined_text:
                        info["weight"] += 1
            
            # Sort specialties by weight
            ranked_specialties = sorted(
                [(s, info["weight"]) for s, info in specialties.items() if info["weight"] > 0],
                key=lambda x: x[1],
                reverse=True
            )
            
            # Determine primary and secondary specialties
            primary = ranked_specialties[0][0] if ranked_specialties else None
            secondary = ranked_specialties[1][0] if len(ranked_specialties) > 1 else None
            
            # Calculate breadth of experience
            active_specialties = len([s for s, w in ranked_specialties if w > 0])
            
            if active_specialties >= 5:
                experience_type = "Generalist - broad IT experience"
            elif active_specialties >= 3:
                experience_type = "Multi-disciplinary"
            elif active_specialties >= 1:
                experience_type = "Specialist"
            else:
                experience_type = "Entry-level"
            
            return json.dumps({
                "primary_specialty": primary,
                "secondary_specialty": secondary,
                "all_specialties": dict(ranked_specialties),
                "experience_type": experience_type,
                "specialty_count": active_specialties,
                "recommendation": self._get_specialty_recommendation(primary, experience_type)
            })
            
        except Exception as e:
            return f"Error matching specialty: {str(e)}"
    
    def _get_specialty_recommendation(self, primary: str, exp_type: str) -> str:
        """Provide specialty recommendations"""
        
        if primary == "INFOSEC":
            return "Security focus is highly valued - emphasize compliance and incident response"
        elif primary == "SYSADMIN":
            return "Systems administration is core IT - highlight automation and scale"
        elif primary == "NETWORK":
            return "Network skills essential - emphasize architecture and security"
        elif exp_type == "Generalist - broad IT experience":
            return "Excellent breadth - position as versatile IT professional"
        elif exp_type == "Multi-disciplinary":
            return "Good range - emphasize how specialties complement each other"
        else:
            return "Focus on demonstrating practical IT problem-solving"
    
    def _analyze_systems_experience(self, input_data: str) -> str:
        """Evaluate systems administration experience"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            systems_areas = {
                "windows": ["windows server", "active directory", "group policy", "exchange", "sharepoint", "iis", "wsus"],
                "linux": ["linux", "rhel", "centos", "ubuntu", "debian", "bash", "shell scripting", "apache"],
                "virtualization": ["vmware", "vsphere", "esxi", "hyper-v", "kvm", "virtual machine", "vdi"],
                "cloud_systems": ["aws ec2", "azure vm", "iaas", "cloud migration", "hybrid cloud"],
                "storage": ["san", "nas", "iscsi", "raid", "backup", "disaster recovery", "netapp", "emc"],
                "monitoring": ["monitoring", "nagios", "zabbix", "scom", "performance", "capacity planning"],
                "automation": ["powershell", "ansible", "puppet", "scripting", "automation", "gpo", "sccm"]
            }
            
            systems_profile = {}
            total_skills = 0
            
            for area, keywords in systems_areas.items():
                found = [kw for kw in keywords if kw in experience]
                if found:
                    systems_profile[area] = found
                    total_skills += len(found)
            
            # Check for scale indicators
            scale_pattern = r'\d+\+?\s*(servers?|systems?|users|vms?|machines)'
            scale_matches = re.findall(scale_pattern, experience)
            has_scale = len(scale_matches) > 0
            
            # Determine expertise level
            if total_skills >= 15:
                expertise = "Senior Systems Administrator"
            elif total_skills >= 10:
                expertise = "Systems Administrator"
            elif total_skills >= 5:
                expertise = "Junior Systems Administrator"
            else:
                expertise = "Entry Level"
            
            # Check for federal preferences
            has_windows = bool(systems_profile.get("windows"))
            has_linux = bool(systems_profile.get("linux"))
            has_vmware = "vmware" in experience
            
            return json.dumps({
                "systems_experience": systems_profile,
                "skill_count": total_skills,
                "expertise_level": expertise,
                "manages_scale": has_scale,
                "windows_admin": has_windows,
                "linux_admin": has_linux,
                "virtualization": has_vmware,
                "recommendation": self._get_systems_recommendation(expertise, has_windows, has_linux)
            })
            
        except Exception as e:
            return f"Error analyzing systems: {str(e)}"
    
    def _get_systems_recommendation(self, expertise: str, windows: bool, linux: bool) -> str:
        """Provide systems recommendations"""
        
        if expertise.startswith("Senior") and windows and linux:
            return "Excellent mixed environment experience for federal IT"
        elif windows and linux:
            return "Strong dual-platform skills valued in government"
        elif windows:
            return "Windows dominates federal desktop/server environment"
        elif linux:
            return "Linux skills valuable - also emphasize any Windows experience"
        else:
            return "Consider highlighting any server or system management experience"
    
    def _check_network_skills(self, input_data: str) -> str:
        """Assess network administration capabilities"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            certifications = [c.lower() for c in data.get("certifications", [])]
            
            network_areas = {
                "routing_switching": ["routing", "switching", "ospf", "bgp", "eigrp", "vlan", "stp", "vpc"],
                "network_security": ["firewall", "vpn", "ipsec", "ssl vpn", "nat", "acl", "ids", "ips"],
                "wireless": ["wireless", "wifi", "802.11", "wlan", "access point", "controller"],
                "wan_tech": ["mpls", "sd-wan", "wan optimization", "qos", "voip", "sip"],
                "vendors": ["cisco", "juniper", "palo alto", "fortinet", "aruba", "f5"],
                "protocols": ["tcp/ip", "dns", "dhcp", "snmp", "ipv6", "multicast"]
            }
            
            network_profile = {}
            skill_count = 0
            
            combined_text = experience + " " + " ".join(certifications)
            
            for area, keywords in network_areas.items():
                found = [kw for kw in keywords if kw in combined_text]
                if found:
                    network_profile[area] = found
                    skill_count += len(found)
            
            # Check for certifications
            network_certs = {
                "ccna": "CCNA",
                "ccnp": "CCNP",
                "ccie": "CCIE",
                "network+": "Network+",
                "jncia": "JNCIA",
                "jncis": "JNCIS"
            }
            
            found_certs = []
            for cert_key, cert_name in network_certs.items():
                if cert_key in combined_text:
                    found_certs.append(cert_name)
            
            # Determine network expertise
            if skill_count >= 12 or "ccie" in combined_text:
                network_level = "Network Architect"
            elif skill_count >= 8 or "ccnp" in combined_text:
                network_level = "Senior Network Engineer"
            elif skill_count >= 4 or "ccna" in combined_text:
                network_level = "Network Engineer"
            else:
                network_level = "Basic Networking"
            
            has_cisco = "cisco" in combined_text
            
            return json.dumps({
                "network_skills": network_profile,
                "skill_count": skill_count,
                "network_level": network_level,
                "certifications": found_certs,
                "cisco_experience": has_cisco,
                "recommendation": self._get_network_recommendation(network_level, has_cisco, found_certs)
            })
            
        except Exception as e:
            return f"Error checking network skills: {str(e)}"
    
    def _get_network_recommendation(self, level: str, cisco: bool, certs: List) -> str:
        """Provide network recommendations"""
        
        if level in ["Network Architect", "Senior Network Engineer"] and cisco:
            return "Excellent network expertise for federal infrastructure"
        elif certs:
            return f"Certifications ({', '.join(certs)}) demonstrate expertise"
        elif cisco:
            return "Cisco experience aligns with federal network infrastructure"
        elif level != "Basic Networking":
            return "Good network foundation - Cisco experience is valuable"
        else:
            return "Consider highlighting any network troubleshooting experience"
    
    def _evaluate_cybersecurity(self, input_data: str) -> str:
        """Check cybersecurity knowledge and practices"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            certifications = [c.lower() for c in data.get("certifications", [])]
            
            security_domains = {
                "incident_response": ["incident response", "soc", "csirt", "forensics", "malware analysis", "threat hunting"],
                "vulnerability_mgmt": ["vulnerability", "scanning", "nessus", "qualys", "patch management", "remediation"],
                "compliance": ["fisma", "nist", "800-53", "800-171", "fedramp", "stig", "hipaa", "pci"],
                "identity_mgmt": ["identity", "iam", "sso", "mfa", "privileged access", "pam", "okta", "ping"],
                "security_tools": ["siem", "splunk", "qradar", "edr", "crowdstrike", "carbon black", "firewall"],
                "frameworks": ["zero trust", "defense in depth", "risk management", "rmf", "cybersecurity framework"]
            }
            
            security_profile = {}
            security_score = 0
            
            combined_text = experience + " " + " ".join(certifications)
            
            for domain, keywords in security_domains.items():
                found = [kw for kw in keywords if kw in combined_text]
                if found:
                    security_profile[domain] = found
                    security_score += len(found)
            
            # Check for security certifications
            security_certs = {
                "cissp": "CISSP",
                "security+": "Security+",
                "cysa+": "CySA+",
                "ceh": "CEH",
                "gcih": "GCIH",
                "gsec": "GSEC",
                "casp": "CASP+"
            }
            
            found_certs = []
            for cert_key, cert_name in security_certs.items():
                if cert_key in combined_text:
                    found_certs.append(cert_name)
            
            # Check for federal compliance
            has_federal_compliance = bool(security_profile.get("compliance"))
            
            # Determine security level
            if security_score >= 12 or "cissp" in combined_text:
                security_level = "Senior Security Professional"
            elif security_score >= 8 or found_certs:
                security_level = "Security Analyst"
            elif security_score >= 4:
                security_level = "Security Aware"
            else:
                security_level = "Basic Security"
            
            return json.dumps({
                "security_domains": security_profile,
                "security_score": security_score,
                "security_level": security_level,
                "certifications": found_certs,
                "federal_compliance": has_federal_compliance,
                "recommendation": self._get_security_recommendation(security_level, has_federal_compliance, found_certs)
            })
            
        except Exception as e:
            return f"Error evaluating cybersecurity: {str(e)}"
    
    def _get_security_recommendation(self, level: str, federal: bool, certs: List) -> str:
        """Provide cybersecurity recommendations"""
        
        if level == "Senior Security Professional" and federal:
            return "Outstanding security profile with federal compliance expertise"
        elif federal:
            return "Federal compliance knowledge is highly valuable"
        elif certs:
            return f"Security certifications ({', '.join(certs)}) enhance credibility"
        elif level in ["Security Analyst", "Security Aware"]:
            return "Good security foundation - emphasize any compliance work"
        else:
            return "Security awareness is essential for all federal IT roles"
    
    def _assess_customer_support(self, input_data: str) -> str:
        """Evaluate customer service and support experience"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            support_areas = {
                "help_desk": ["help desk", "service desk", "tier 1", "tier 2", "tier 3", "desktop support"],
                "ticketing": ["ticket", "servicenow", "remedy", "jira", "incident", "request", "change management"],
                "customer_service": ["customer service", "customer satisfaction", "sla", "kpi", "metrics", "survey"],
                "troubleshooting": ["troubleshoot", "diagnose", "resolve", "root cause", "problem solving"],
                "documentation": ["documentation", "knowledge base", "kb article", "sop", "runbook", "training"],
                "communication": ["communicate", "explain", "non-technical", "stakeholder", "briefing", "presentation"]
            }
            
            support_profile = {}
            support_score = 0
            
            for area, keywords in support_areas.items():
                found = [kw for kw in keywords if kw in experience]
                if found:
                    support_profile[area] = found
                    support_score += len(found)
            
            # Check for metrics
            metrics_pattern = r'\d+%?\s*(satisfaction|resolution|tickets?|calls?|users?)'
            has_metrics = bool(re.search(metrics_pattern, experience))
            
            # Check for ITIL
            has_itil = any(term in experience for term in ["itil", "it service management", "itsm"])
            
            # Determine support level
            if support_score >= 10 and has_itil:
                support_level = "Senior IT Support Professional"
            elif support_score >= 7:
                support_level = "Experienced Support Specialist"
            elif support_score >= 4:
                support_level = "Support Technician"
            else:
                support_level = "Entry Support"
            
            return json.dumps({
                "support_experience": support_profile,
                "support_score": support_score,
                "support_level": support_level,
                "uses_metrics": has_metrics,
                "itil_knowledge": has_itil,
                "recommendation": self._get_support_recommendation(support_level, has_metrics, has_itil)
            })
            
        except Exception as e:
            return f"Error assessing support: {str(e)}"
    
    def _get_support_recommendation(self, level: str, metrics: bool, itil: bool) -> str:
        """Provide customer support recommendations"""
        
        if level == "Senior IT Support Professional" and metrics:
            return "Excellent support background with measurable results"
        elif itil:
            return "ITIL knowledge aligns with federal IT service management"
        elif metrics:
            return "Good use of metrics - federal agencies value data-driven support"
        elif level in ["Experienced Support Specialist", "Support Technician"]:
            return "Solid support experience - emphasize problem resolution skills"
        else:
            return "Customer service is critical in federal IT roles"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze candidate profile for IT Specialist positions
        """
        
        try:
            # Extract candidate information
            skills = data.get("skills", [])
            experience = data.get("experience", "")
            certifications = data.get("certifications", [])
            target_grade = data.get("target_grade", "GS-11")
            target_specialty = data.get("target_specialty", "")
            
            # Build analysis query
            query = f"""
            Analyze this candidate for a {target_grade} IT Specialist (2210) position:
            
            Skills: {', '.join(skills)}
            
            Experience Summary: {experience[:500]}
            
            Certifications: {', '.join(certifications) if certifications else 'None listed'}
            
            Target Specialty: {target_specialty if target_specialty else 'Best match based on experience'}
            
            Provide:
            1. IT specialty area matching
            2. Systems administration assessment
            3. Network capabilities evaluation
            4. Cybersecurity knowledge check
            5. Customer support experience review
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add specific recommendations
                response.data["recommendations"] = {
                    "immediate_actions": [
                        "Identify your primary IT specialty area (parenthetical)",
                        "Highlight relevant certifications prominently",
                        "Quantify systems/users/tickets managed"
                    ],
                    "federal_tips": [
                        "Emphasize any federal compliance experience",
                        "Include experience with government systems",
                        "Mention security clearance or ability to obtain"
                    ],
                    "skill_focus": [
                        "Balance technical depth with breadth",
                        "Show progression in responsibility",
                        "Include soft skills and customer service"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
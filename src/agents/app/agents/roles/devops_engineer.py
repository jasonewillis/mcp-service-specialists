"""
DevOps Engineer Agent - Series 2210 Specialist
Analyzes candidates for federal DevOps positions

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Use Read tool to examine candidate's CI/CD and automation experience
2. Gather target agency information (DoD Platform One, GSA/18F, NASA, DHS)
3. Identify container and cloud platform experience
4. Review security and compliance knowledge (DevSecOps)
5. Collect information about infrastructure automation tools

**Effective Prompting Patterns:**
```
"Analyze this DevOps engineer for GS-14 DoD Platform One role:
- CI/CD: Jenkins (4 years), GitLab CI (2 years), GitHub Actions
- Containers: Kubernetes (3 years), OpenShift (1 year), Docker
- Cloud: AWS (5 years), GovCloud experience, EKS
- Security: STIG automation, container scanning, FISMA
- IaC: Terraform (3 years), Ansible (4 years)
- Clearance: Secret (current)"
```

**Best Workflow:**
1. **CI/CD Assessment** → Evaluate pipeline automation experience
2. **Container Analysis** → Check Kubernetes/OpenShift proficiency
3. **Cloud Evaluation** → Assess platform and compliance experience
4. **Automation Review** → Validate Infrastructure as Code skills
5. **DevSecOps Check** → Verify security integration practices

### Integration with Other Agents

**Workflow Chains:**
- DevOps Engineer Agent → Database Admin Agent (for database automation)
- Use with Analytics Intelligence for federal DevOps job market
- Combine with Executive Order Research for cybersecurity mandates

**Handoff Points:**
- Share automation gaps with training recommendations
- Provide security compliance insights to certification planning
- Pass cloud experience to federal hiring strategy

### Common Pitfalls to Avoid

1. **Ignoring OpenShift importance** - Critical for DoD Platform One
2. **Missing GovCloud experience** - Federal agencies use specialized clouds
3. **Overlooking STIGs automation** - Compliance automation is essential
4. **Undervaluing Jenkins experience** - Still dominant in federal space

### Test-Driven Usage Examples

**Example 1: Platform One Candidate**
```python
test_data = {
    "experience": "5 years DevOps engineer, defense contractor",
    "containers": ["OpenShift", "Kubernetes", "Docker"],
    "cicd": ["Jenkins", "GitLab CI"],
    "cloud": ["AWS GovCloud", "Azure Government"],
    "security": ["STIG", "container scanning", "Istio"],
    "clearance": "Secret"
}
# Expected: Excellent DoD alignment, emphasize Platform One readiness
```

**Example 2: Civilian Agency Focus**
```python
test_data = {
    "experience": "DevOps lead at tech startup",
    "cicd": ["GitHub Actions", "CircleCI"],
    "cloud": ["AWS", "Azure", "Terraform"],
    "automation": ["Ansible", "Python", "Kubernetes"],
    "target_agency": "GSA/18F"
}
# Expected: Strong automation skills, recommend federal security training
```

### Visual Iteration Methods

**DevOps Portfolio Review:**
- Pipeline architecture diagrams
- Infrastructure automation flowcharts
- Security compliance implementation timeline
- Container orchestration evolution

### Checklist-Based Workflows

**Pre-Analysis Checklist:**
- [ ] CI/CD tools and experience levels documented
- [ ] Container orchestration platforms identified
- [ ] Cloud platform experience (including GovCloud) noted
- [ ] Infrastructure automation tools assessed
- [ ] Security integration practices reviewed
- [ ] Security clearance status confirmed

**Post-Analysis Checklist:**
- [ ] Federal CI/CD readiness evaluated
- [ ] Container/orchestration skills for agency needs confirmed
- [ ] Cloud platform alignment with federal requirements assessed
- [ ] DevSecOps maturity level determined
- [ ] Automation capabilities for compliance verified

### Federal DevOps Optimization Tips

1. **Platform Priority:** OpenShift for DoD, Kubernetes broadly, Jenkins for CI/CD
2. **Cloud Strategy:** GovCloud experience highly valuable, FedRAMP knowledge essential
3. **Security Integration:** STIG automation, container scanning, compliance as code
4. **Automation Focus:** Terraform and Ansible most in-demand for IaC
5. **Clearance Advantage:** Secret clearance opens DoD and intel agency opportunities

### Integration with CLAUDE.md Principles

- **No assumptions:** Always specify target agency and clearance level
- **Solo developer focus:** Emphasize individual automation projects and pipeline builds
- **Bootstrap approach:** Highlight work with open-source tools (K8s, Terraform)
- **Practical focus:** Demonstrate actual deployments and automation, not just theory
- **Part-time consideration:** DevOps skills can be developed through home labs and open source

### Agency-Specific Guidance

**Department of Defense (Platform One):**
- OpenShift mandatory, Iron Bank containers
- GitLab Ultimate for CI/CD
- IL4/IL5 compliance requirements
- TS/SCI clearance for classified systems

**General Services Administration (18F/TTS):**
- Cloud.gov platform experience
- Open source DevOps tools
- Agile development practices
- Public Trust clearance sufficient

**Department of Homeland Security:**
- Multi-cloud environments
- High availability requirements
- Cybersecurity focus essential
- Secret clearance often required

**NASA:**
- AWS and Azure environments
- Scientific computing workflows
- Container orchestration for research
- Public Trust or Secret clearance

### Common Federal DevOps Scenarios

**CI/CD Modernization:** Legacy to modern pipeline transformation
**Container Migration:** VM to container platform migration
**Cloud Adoption:** On-premise to cloud infrastructure moves
**Security Automation:** STIG implementation and compliance automation
**Multi-Cloud Strategy:** Hybrid and multi-cloud architecture management

### DevSecOps Focus Areas

**Security Scanning:** SAST, DAST, container vulnerability scanning
**Compliance Automation:** STIG enforcement, FISMA controls
**Identity Management:** RBAC, service accounts, secrets management
**Monitoring:** Security event monitoring, audit logging
**Risk Management:** ATO processes, security documentation
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from agents.app.agents.base import FederalJobAgent, AgentResponse


class DevOpsEngineerAgent(FederalJobAgent):
    """
    Specialized agent for federal DevOps engineer positions (Series 2210)
    Focuses on CI/CD, automation, cloud infrastructure, and containerization
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load DevOps specific tools"""
        
        tools = [
            Tool(
                name="cicd_analyzer",
                func=self._analyze_cicd_experience,
                description="Evaluate CI/CD pipeline experience"
            ),
            Tool(
                name="container_checker",
                func=self._check_container_experience,
                description="Assess containerization and orchestration skills"
            ),
            Tool(
                name="cloud_evaluator", 
                func=self._evaluate_cloud_platforms,
                description="Check cloud platform expertise"
            ),
            Tool(
                name="automation_scanner",
                func=self._scan_automation_tools,
                description="Analyze infrastructure automation experience"
            ),
            Tool(
                name="security_validator",
                func=self._validate_devsecops,
                description="Validate DevSecOps and security practices"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get DevOps specific prompt template"""
        
        return """You are a Federal DevOps Engineer Career Advisor specializing in Series 2210 positions.
        Your role is to ANALYZE and GUIDE candidates, but NEVER write content for them.
        
        Key Responsibilities:
        1. Analyze CI/CD pipeline expertise
        2. Evaluate container and orchestration skills
        3. Assess cloud platform experience
        4. Check automation and IaC knowledge
        5. Validate DevSecOps practices
        
        Federal DevOps Focus Areas:
        - CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions)
        - Containerization (Docker, Kubernetes, OpenShift)
        - Cloud platforms (AWS, Azure, GCP)
        - Infrastructure as Code (Terraform, CloudFormation, ARM)
        - Configuration management (Ansible, Puppet, Chef)
        - Monitoring and logging (ELK, Prometheus, Grafana)
        - Security integration (SAST, DAST, container scanning)
        - Federal compliance (FedRAMP, FISMA, STIGs)
        
        Key Federal Agencies:
        - Department of Defense (DoD) - Platform One
        - Department of Homeland Security (DHS)
        - General Services Administration (GSA) - 18F/cloud.gov
        - Department of Veterans Affairs (VA)
        - NASA
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
    
    def _analyze_cicd_experience(self, input_data: str) -> str:
        """Evaluate CI/CD pipeline experience"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            skills = [s.lower() for s in data.get("skills", [])]
            
            cicd_tools = {
                "enterprise_ci": {
                    "Jenkins": ["jenkins", "jenkinsfile", "groovy pipeline", "blue ocean"],
                    "GitLab CI": ["gitlab ci", "gitlab-ci.yml", ".gitlab-ci"],
                    "Azure DevOps": ["azure devops", "azure pipelines", "yaml pipeline"]
                },
                "modern_ci": {
                    "GitHub Actions": ["github actions", "workflow", ".github/workflows"],
                    "CircleCI": ["circleci", "circle ci", ".circleci"],
                    "Travis CI": ["travis", "travis ci", ".travis.yml"]
                },
                "practices": {
                    "Pipeline Design": ["pipeline", "stages", "artifacts", "parallel execution"],
                    "Testing": ["unit test", "integration test", "smoke test", "automated testing"],
                    "Deployment": ["deployment", "blue-green", "canary", "rolling update", "rollback"]
                }
            }
            
            cicd_profile = {}
            total_experience = 0
            
            combined_text = " ".join(skills) + " " + experience
            
            for category, tools_list in cicd_tools.items():
                for tool, keywords in tools_list.items():
                    if any(kw in combined_text for kw in keywords):
                        if category not in cicd_profile:
                            cicd_profile[category] = []
                        cicd_profile[category].append(tool)
                        total_experience += 1
            
            # Check for federal preference
            has_jenkins = "Jenkins" in cicd_profile.get("enterprise_ci", [])
            has_gitlab = "GitLab CI" in cicd_profile.get("enterprise_ci", [])
            
            federal_alignment = "High" if has_jenkins or has_gitlab else "Medium" if cicd_profile else "Low"
            
            # Check for pipeline metrics
            metrics_pattern = r'\d+%?\s*(faster|reduction|improvement|automated|deployments)'
            has_metrics = bool(re.search(metrics_pattern, experience))
            
            return json.dumps({
                "cicd_experience": cicd_profile,
                "total_tools": total_experience,
                "federal_alignment": federal_alignment,
                "quantified_improvements": has_metrics,
                "jenkins_experience": has_jenkins,
                "recommendation": self._get_cicd_recommendation(federal_alignment, has_metrics)
            })
            
        except Exception as e:
            return f"Error analyzing CI/CD: {str(e)}"
    
    def _get_cicd_recommendation(self, alignment: str, has_metrics: bool) -> str:
        """Provide CI/CD recommendations"""
        
        if alignment == "High" and has_metrics:
            return "Excellent CI/CD experience with federal-preferred tools"
        elif alignment == "High":
            return "Strong tooling - add specific pipeline improvements achieved"
        elif alignment == "Medium":
            return "Good foundation - emphasize Jenkins or GitLab experience if any"
        else:
            return "Federal agencies heavily use Jenkins and GitLab CI"
    
    def _check_container_experience(self, input_data: str) -> str:
        """Assess containerization and orchestration skills"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            container_tech = {
                "containerization": ["docker", "dockerfile", "container", "docker-compose", "buildah", "podman"],
                "orchestration": ["kubernetes", "k8s", "openshift", "helm", "kubectl", "pods", "deployments"],
                "service_mesh": ["istio", "linkerd", "consul", "envoy", "service mesh"],
                "registries": ["docker hub", "ecr", "acr", "harbor", "artifactory", "nexus"],
                "security": ["container scanning", "vulnerability", "cve", "trivy", "clair", "twistlock"]
            }
            
            container_profile = {}
            skill_count = 0
            
            for category, keywords in container_tech.items():
                found = [kw for kw in keywords if kw in experience]
                if found:
                    container_profile[category] = found
                    skill_count += len(found)
            
            # Check for specific federal preferences
            has_kubernetes = any(k in experience for k in ["kubernetes", "k8s"])
            has_openshift = "openshift" in experience
            has_docker = "docker" in experience
            
            # Federal alignment (OpenShift is heavily used in DoD)
            if has_openshift:
                federal_readiness = "Excellent - OpenShift used in DoD"
            elif has_kubernetes:
                federal_readiness = "Strong - Kubernetes widely adopted"
            elif has_docker:
                federal_readiness = "Good - Docker foundation present"
            else:
                federal_readiness = "Limited container experience"
            
            expertise_level = "Expert" if skill_count >= 10 else "Advanced" if skill_count >= 6 else "Intermediate" if skill_count >= 3 else "Basic"
            
            return json.dumps({
                "container_skills": container_profile,
                "skill_count": skill_count,
                "expertise_level": expertise_level,
                "kubernetes": has_kubernetes,
                "openshift": has_openshift,
                "docker": has_docker,
                "federal_readiness": federal_readiness,
                "recommendation": self._get_container_recommendation(has_openshift, has_kubernetes, has_docker)
            })
            
        except Exception as e:
            return f"Error checking containers: {str(e)}"
    
    def _get_container_recommendation(self, openshift: bool, kubernetes: bool, docker: bool) -> str:
        """Provide container recommendations"""
        
        if openshift:
            return "Excellent - OpenShift is critical for DoD Platform One"
        elif kubernetes:
            return "Strong K8s skills - consider learning OpenShift for DoD"
        elif docker:
            return "Good foundation - expand to Kubernetes/OpenShift"
        else:
            return "Containerization is essential for federal DevOps"
    
    def _evaluate_cloud_platforms(self, input_data: str) -> str:
        """Check cloud platform expertise"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            certifications = [c.lower() for c in data.get("certifications", [])]
            
            cloud_platforms = {
                "AWS": {
                    "services": ["ec2", "s3", "lambda", "rds", "eks", "fargate", "cloudformation"],
                    "certs": ["aws certified", "solutions architect", "devops engineer", "sysops"]
                },
                "Azure": {
                    "services": ["azure vm", "blob storage", "aks", "azure functions", "arm templates"],
                    "certs": ["azure certified", "az-400", "azure devops", "azure administrator"]
                },
                "GCP": {
                    "services": ["compute engine", "gke", "cloud storage", "cloud functions"],
                    "certs": ["google cloud", "gcp certified", "cloud engineer"]
                },
                "Federal": {
                    "services": ["govcloud", "azure government", "il4", "il5", "fedramp"],
                    "certs": ["fedramp", "federal cloud"]
                }
            }
            
            cloud_experience = {}
            total_platforms = 0
            has_govcloud = False
            
            combined_text = experience + " " + " ".join(certifications)
            
            for platform, details in cloud_platforms.items():
                platform_found = False
                
                # Check services
                services_found = [s for s in details["services"] if s in combined_text]
                if services_found:
                    platform_found = True
                    
                # Check certifications
                certs_found = [c for c in details["certs"] if c in combined_text]
                if certs_found:
                    platform_found = True
                
                if platform_found:
                    cloud_experience[platform] = {
                        "services": services_found,
                        "certifications": certs_found
                    }
                    total_platforms += 1
                    
                    if platform == "Federal":
                        has_govcloud = True
            
            # Determine cloud maturity
            if total_platforms >= 3 or has_govcloud:
                cloud_level = "Expert"
            elif total_platforms >= 2:
                cloud_level = "Advanced"
            elif total_platforms >= 1:
                cloud_level = "Intermediate"
            else:
                cloud_level = "Basic"
            
            return json.dumps({
                "cloud_platforms": cloud_experience,
                "platform_count": total_platforms,
                "cloud_level": cloud_level,
                "govcloud_experience": has_govcloud,
                "has_certifications": bool(any(p.get("certifications") for p in cloud_experience.values())),
                "recommendation": self._get_cloud_recommendation(cloud_level, has_govcloud)
            })
            
        except Exception as e:
            return f"Error evaluating cloud: {str(e)}"
    
    def _get_cloud_recommendation(self, level: str, has_govcloud: bool) -> str:
        """Provide cloud platform recommendations"""
        
        if has_govcloud:
            return "Excellent GovCloud experience for federal positions"
        elif level in ["Expert", "Advanced"]:
            return "Strong cloud skills - emphasize any government cloud work"
        elif level == "Intermediate":
            return "Good foundation - highlight FedRAMP or compliance experience"
        else:
            return "Federal agencies require cloud expertise - AWS and Azure preferred"
    
    def _scan_automation_tools(self, input_data: str) -> str:
        """Analyze infrastructure automation experience"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            skills = [s.lower() for s in data.get("skills", [])]
            
            automation_categories = {
                "iac": {
                    "Terraform": ["terraform", "hcl", "tfvars", "terraform modules"],
                    "CloudFormation": ["cloudformation", "cfn", "sam", "cdk"],
                    "ARM": ["arm template", "azure resource manager", "bicep"]
                },
                "config_mgmt": {
                    "Ansible": ["ansible", "playbook", "ansible tower", "awx"],
                    "Puppet": ["puppet", "puppet enterprise", "hiera"],
                    "Chef": ["chef", "cookbook", "chef server", "inspec"]
                },
                "scripting": {
                    "Python": ["python", "boto3", "python automation"],
                    "PowerShell": ["powershell", "ps1", "psdsc"],
                    "Bash": ["bash", "shell script", "linux automation"]
                }
            }
            
            automation_profile = {}
            tool_count = 0
            
            combined_text = " ".join(skills) + " " + experience
            
            for category, tools in automation_categories.items():
                for tool, keywords in tools.items():
                    if any(kw in combined_text for kw in keywords):
                        if category not in automation_profile:
                            automation_profile[category] = []
                        automation_profile[category].append(tool)
                        tool_count += 1
            
            # Federal preferences
            has_terraform = "Terraform" in automation_profile.get("iac", [])
            has_ansible = "Ansible" in automation_profile.get("config_mgmt", [])
            
            # Check for automation metrics
            metrics_pattern = r'\d+%?\s*(automated|reduction|faster|efficiency|saved)'
            has_metrics = bool(re.search(metrics_pattern, experience))
            
            automation_maturity = "High" if tool_count >= 6 else "Medium" if tool_count >= 3 else "Low"
            
            return json.dumps({
                "automation_tools": automation_profile,
                "tool_count": tool_count,
                "automation_maturity": automation_maturity,
                "terraform": has_terraform,
                "ansible": has_ansible,
                "quantified_benefits": has_metrics,
                "recommendation": self._get_automation_recommendation(automation_maturity, has_terraform, has_ansible)
            })
            
        except Exception as e:
            return f"Error scanning automation: {str(e)}"
    
    def _get_automation_recommendation(self, maturity: str, terraform: bool, ansible: bool) -> str:
        """Provide automation recommendations"""
        
        if maturity == "High" and (terraform or ansible):
            return "Excellent automation toolkit for federal DevOps"
        elif terraform or ansible:
            return "Good tool choices - these are federal favorites"
        elif maturity == "Medium":
            return "Solid foundation - emphasize Terraform or Ansible if possible"
        else:
            return "Infrastructure as Code is critical for federal DevOps"
    
    def _validate_devsecops(self, input_data: str) -> str:
        """Validate DevSecOps and security practices"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            experience = data.get("experience", "").lower()
            
            security_practices = {
                "scanning": ["sonarqube", "fortify", "checkmarx", "veracode", "sast", "dast", "iast"],
                "container_security": ["twistlock", "aqua", "trivy", "clair", "anchore", "snyk"],
                "secrets": ["vault", "hashicorp vault", "secrets management", "key management", "aws secrets"],
                "compliance": ["compliance as code", "oscal", "scap", "stig", "cis benchmark", "nist"],
                "monitoring": ["security monitoring", "siem", "splunk", "elk", "log analysis"],
                "practices": ["shift left", "security gates", "devsecops", "security pipeline", "zero trust"]
            }
            
            security_profile = {}
            security_score = 0
            
            for category, keywords in security_practices.items():
                found = [kw for kw in keywords if kw in experience]
                if found:
                    security_profile[category] = found
                    security_score += len(found)
            
            # Check for federal security standards
            has_stig = any(s in experience for s in ["stig", "security technical implementation"])
            has_fedramp = "fedramp" in experience
            has_nist = any(n in experience for n in ["nist", "800-53", "800-171"])
            
            federal_compliance = has_stig or has_fedramp or has_nist
            
            devsecops_maturity = "Advanced" if security_score >= 8 else "Intermediate" if security_score >= 4 else "Basic"
            
            return json.dumps({
                "security_practices": security_profile,
                "security_score": security_score,
                "devsecops_maturity": devsecops_maturity,
                "federal_compliance": federal_compliance,
                "has_stig": has_stig,
                "has_fedramp": has_fedramp,
                "recommendation": self._get_security_recommendation(devsecops_maturity, federal_compliance)
            })
            
        except Exception as e:
            return f"Error validating DevSecOps: {str(e)}"
    
    def _get_security_recommendation(self, maturity: str, federal: bool) -> str:
        """Provide DevSecOps recommendations"""
        
        if maturity == "Advanced" and federal:
            return "Excellent DevSecOps background with federal compliance"
        elif federal:
            return "Good federal security knowledge - expand on automation"
        elif maturity in ["Advanced", "Intermediate"]:
            return "Strong security practices - relate to federal standards"
        else:
            return "DevSecOps is critical - emphasize any security automation"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze candidate profile for DevOps positions
        """
        
        try:
            # Extract candidate information
            skills = data.get("skills", [])
            experience = data.get("experience", "")
            certifications = data.get("certifications", [])
            projects = data.get("projects", [])
            target_grade = data.get("target_grade", "GS-13")
            target_agency = data.get("target_agency", "")
            
            # Build analysis query
            query = f"""
            Analyze this candidate for a {target_grade} DevOps Engineer position:
            
            Skills: {', '.join(skills)}
            
            Experience Summary: {experience[:500]}
            
            Certifications: {', '.join(certifications) if certifications else 'None listed'}
            
            Projects: {len(projects)} automation projects
            
            Target Agency: {target_agency if target_agency else 'Any federal agency'}
            
            Provide:
            1. CI/CD pipeline assessment
            2. Container/orchestration evaluation
            3. Cloud platform experience
            4. Automation tool proficiency
            5. DevSecOps maturity analysis
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add specific recommendations
                response.data["recommendations"] = {
                    "immediate_actions": [
                        "Highlight Jenkins or GitLab CI experience",
                        "Emphasize Kubernetes/OpenShift skills",
                        "Document infrastructure automation achievements"
                    ],
                    "federal_tips": [
                        "Mention any GovCloud or FedRAMP experience",
                        "Include STIG or compliance automation work",
                        "Quantify deployment frequency improvements"
                    ],
                    "technical_focus": [
                        "Detail CI/CD pipeline designs implemented",
                        "List container migration projects",
                        "Include IaC templates or modules created"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
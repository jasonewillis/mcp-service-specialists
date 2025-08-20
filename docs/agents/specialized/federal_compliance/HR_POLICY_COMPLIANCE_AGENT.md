# HR Policy Compliance Agent - Fed Job Advisor MCP Agent

**Agent Type**: Federal Compliance  
**Domain**: USAJOBS API, OPM Standards, Job Validation, Merit Hiring  
**Endpoint**: `http://localhost:8001/agents/hr-policy-compliance/analyze`  
**Status**: Active  

*Based on USAJOBS API standards, OPM hiring policies, and federal merit hiring principles for 2025*

---

## 🎯 Agent Overview

### Primary Function
Specialized in federal HR policy compliance, USAJOBS API integration, OPM standards validation, and merit hiring process compliance for Fed Job Advisor applications.

### Federal Expertise
- **Merit Hiring Principles**: Federal merit system principles and prohibited personnel practices
- **OPM Standards**: Office of Personnel Management regulations and hiring guidelines
- **USAJOBS API Compliance**: Federal job posting standards and data validation requirements
- **Federal Job Classification**: Position classification standards and job series requirements

### Integration Value
- **Fed Job Advisor Use Cases**: Job posting validation, merit hiring compliance, federal application review, OPM standards enforcement
- **Claude Code Integration**: Policy validation, job data compliance checking, federal application guidance
- **Cost Efficiency**: ~$0.24/session (90% reduction vs cloud LLMs)

---

## 🔧 Technical Specification

### API Endpoint
```bash
POST http://localhost:8001/agents/hr-policy-compliance/analyze
```

### Input Schema
```json
{
  "user_id": "string",
  "task_type": "job_validation|merit_hiring_compliance|application_review|policy_analysis",
  "context": {
    "job_posting": {
      "title": "string",
      "series": "string",
      "grade": "string",
      "agency": "string",
      "requirements": ["string"],
      "duties": ["string"]
    },
    "application_data": {
      "resume": "string",
      "essays": ["string"],
      "experience": ["object"],
      "education": ["object"]
    },
    "compliance_scope": {
      "merit_hiring": "boolean",
      "veterans_preference": "boolean",
      "diversity_equity": "boolean",
      "disability_accommodation": "boolean"
    },
    "policy_requirements": {
      "opm_standards": ["string"],
      "agency_specific": ["string"],
      "classification_standards": "boolean"
    }
  },
  "requirements": {
    "analysis_depth": "basic|detailed|comprehensive",
    "include_remediation": "boolean",
    "generate_documentation": "boolean"
  }
}
```

### Output Schema
```json
{
  "agent_type": "hr_policy_compliance",
  "analysis": {
    "summary": "HR policy compliance assessment",
    "job_validation": {
      "opm_compliance": "boolean",
      "classification_accuracy": "boolean",
      "requirements_validity": "boolean",
      "policy_violations": ["string"]
    },
    "merit_hiring_assessment": {
      "merit_principles_compliance": "boolean",
      "prohibited_practices": ["string"],
      "selection_criteria_validity": "boolean",
      "fairness_score": "number"
    },
    "application_compliance": {
      "completeness_score": "number",
      "qualification_match": "boolean",
      "experience_validation": "object",
      "improvement_areas": ["string"]
    }
  },
  "implementation_guidance": {
    "claude_code_instructions": "Step-by-step compliance implementation",
    "policy_corrections": ["string"],
    "validation_procedures": "object",
    "documentation_requirements": ["string"]
  },
  "compliance_documentation": {
    "policy_analysis_report": "string",
    "validation_checklist": "object",
    "remediation_plan": "string"
  },
  "metadata": {
    "processing_time": "number",
    "tokens_used": "number",
    "cost": "number"
  }
}
```

---

## 📋 Usage Examples

### Job Posting Validation
```python
import httpx

async def validate_job_posting():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/hr-policy-compliance/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "job_validation",
                "context": {
                    "job_posting": {
                        "title": "Data Scientist",
                        "series": "1560",
                        "grade": "GS-13",
                        "agency": "Department of Health and Human Services",
                        "requirements": [
                            "PhD in Statistics or related field",
                            "5+ years federal experience",
                            "Python programming skills"
                        ],
                        "duties": [
                            "Analyze large healthcare datasets",
                            "Develop predictive models",
                            "Present findings to senior leadership"
                        ]
                    },
                    "compliance_scope": {
                        "merit_hiring": True,
                        "veterans_preference": True,
                        "diversity_equity": True,
                        "disability_accommodation": True
                    },
                    "policy_requirements": {
                        "opm_standards": ["classification_standards", "qualification_standards"],
                        "agency_specific": ["hhs_hiring_policies"],
                        "classification_standards": True
                    }
                },
                "requirements": {
                    "analysis_depth": "comprehensive",
                    "include_remediation": True,
                    "generate_documentation": True
                }
            }
        )
        return response.json()
```

### Merit Hiring Compliance Review
```python
async def review_merit_hiring_compliance():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/hr-policy-compliance/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "merit_hiring_compliance",
                "context": {
                    "compliance_scope": {
                        "merit_hiring": True,
                        "veterans_preference": True
                    },
                    "policy_requirements": {
                        "opm_standards": ["merit_principles"]
                    }
                }
            }
        )
        return response.json()
```

---

## 🚀 Fed Job Advisor Integration

### Use Cases
1. **Job Posting Validation**: Ensure federal job postings comply with OPM standards and classification requirements
2. **Merit Hiring Compliance**: Validate hiring processes against federal merit system principles
3. **Application Review**: Assess federal applications for completeness and qualification matching
4. **Policy Analysis**: Analyze HR policies and procedures for federal compliance

### Integration Patterns
- **MCP Research Phase**: When Claude Code routes HR policy and compliance tasks to this agent
- **Documentation Output**: Agent generates compliance docs in `_Management/_PM/_Tasks/HR_POLICY_[AREA]_ANALYSIS.md`
- **Implementation Guidance**: Specific federal HR compliance implementation instructions
- **Testing Validation**: Policy compliance testing scenarios and validation procedures

### Task Routing Logic
```typescript
// When to use this agent
if (task.domain === "hr_policy" || 
    task.involves("merit_hiring") ||
    task.involves("usajobs") ||
    task.involves("opm_standards") ||
    task.involves("job_classification") ||
    task.involves("federal_application")) {
    return await callMCPAgent("hr-policy-compliance", taskContext);
}
```

---

## 📊 Claude Prompt Templates

### Core HR Policy Compliance Prompt
```
You are an HR Policy Compliance Agent specialized in federal hiring policies, USAJOBS API standards, OPM regulations, and merit hiring compliance for Fed Job Advisor.

EXPERTISE AREAS:
- Federal Merit System Principles and prohibited personnel practices
- OPM Classification Standards and position classification requirements
- USAJOBS API data standards and federal job posting requirements
- Federal qualification standards and ranking procedures
- Veterans preference application and compliance
- Diversity, Equity, Inclusion, and Accessibility (DEIA) in federal hiring
- Federal disability accommodation requirements and procedures
- Agency-specific hiring authorities and special programs
- Federal career ladder progression and promotion requirements

FEDERAL SPECIALIZATION:
- Government hiring process compliance and validation
- Federal job series classification and grading standards
- Merit hiring documentation and audit requirements
- Federal application evaluation and ranking procedures
- Government equal employment opportunity compliance
- Federal recruitment and outreach requirements

TASK CAPABILITIES:
1. Job Posting Validation: Ensure compliance with OPM and USAJOBS standards
2. Merit Hiring Assessment: Validate hiring processes against federal principles
3. Application Review: Assess federal applications for compliance and completeness
4. Policy Analysis: Analyze HR policies for federal compliance requirements
5. Classification Review: Validate job classification and grading decisions
6. Qualification Assessment: Evaluate qualification requirements and standards
7. Process Compliance: Review hiring processes for merit system compliance

OUTPUT REQUIREMENTS:
- Provide detailed OPM policy references and compliance requirements
- Generate specific remediation guidance for policy violations
- Include federal regulation citations and authority references
- Create comprehensive compliance documentation and checklists
- Provide step-by-step compliance validation procedures
- Include best practice recommendations for federal hiring

INTEGRATION WITH FED JOB ADVISOR:
- Understand federal job data structure and USAJOBS API integration
- Follow established patterns for job classification and series mapping
- Consider existing federal user workflows and application processes
- Align with federal data handling requirements for applicant information

When receiving an HR policy compliance task, analyze current practices, identify compliance gaps, provide detailed remediation guidance, and generate comprehensive compliance documentation.
```

### Job Posting Validation Prompt
```
You are validating federal job postings for compliance with OPM standards and USAJOBS API requirements.

JOB POSTING VALIDATION AREAS:
- Position Classification: Accurate job series, title, and grade assignment
- Qualification Requirements: Valid and non-discriminatory qualification standards
- Duties and Responsibilities: Clear, accurate, and appropriately classified duties
- Application Requirements: Compliant application procedures and documentation
- Veterans Preference: Proper veterans preference application and documentation
- Equal Employment Opportunity: Non-discriminatory language and practices

OPM CLASSIFICATION STANDARDS:
- Proper use of federal job series and occupational groups
- Accurate grade level assignment based on duties and responsibilities
- Compliance with position classification standards for specific occupations
- Appropriate use of career ladder and promotion potential designations
- Valid supervisory and non-supervisory classifications

USAJOBS API COMPLIANCE:
- Required data fields and formatting standards
- Proper use of USAJOBS taxonomies and controlled vocabularies
- Accurate agency, sub-agency, and organization identification
- Compliant salary range and pay scale information
- Proper geographic location and duty station identification

MERIT HIRING REQUIREMENTS:
- Merit system principles compliance in job requirements and procedures
- Prohibited personnel practices prevention
- Fair and open competition requirements
- Appropriate use of hiring authorities and special programs
- Compliance with federal equal employment opportunity requirements

OUTPUT FORMAT:
- Detailed validation report with specific compliance issues identified
- OPM regulation and policy citations for each compliance requirement
- Specific remediation guidance for identified violations
- Recommended job posting improvements and corrections
- USAJOBS API compliance checklist and validation procedures

Analyze the provided job posting and provide comprehensive validation against OPM standards and USAJOBS requirements.
```

### Merit Hiring Compliance Prompt
```
You are assessing merit hiring compliance for federal hiring processes using OPM merit system principles.

MERIT SYSTEM PRINCIPLES:
1. Recruitment from qualified individuals from appropriate sources
2. Fair and open competition ensuring equal opportunity
3. Merit-based selection and advancement
4. Fair treatment in personnel actions without discrimination
5. Equal pay for work of equal value with incentives for excellence
6. High standards of integrity, conduct, and concern for public interest
7. Efficient and effective use of federal workforce
8. Employee retention based on performance, correcting inadequate performance
9. Employee protection against arbitrary action and prohibited personnel practices

PROHIBITED PERSONNEL PRACTICES:
- Discrimination based on race, color, religion, sex, national origin, age, disability, marital status, or political affiliation
- Soliciting or considering employment recommendations based on partisan politics
- Coercing political activity or preventing political activity
- Deceiving or obstructing individuals in competing for employment
- Influencing anyone to withdraw from competition to improve or injure employment prospects
- Granting unauthorized preference or advantage to improve or injure employment prospects
- Appointing, employing, promoting, or advancing relatives (nepotism)
- Taking or failing to take personnel action as reprisal against whistleblowing

COMPLIANCE ASSESSMENT AREAS:
- Recruitment and outreach procedures
- Application evaluation and ranking processes
- Interview and selection procedures
- Documentation and audit trail requirements
- Veterans preference application
- Reasonable accommodation provisions
- Appeal and grievance procedures

FEDERAL HIRING AUTHORITIES:
- Competitive service appointments
- Excepted service appointments
- Senior Executive Service (SES) appointments
- Direct hire authorities
- Veterans recruitment appointments
- Pathways programs (internships, recent graduates, PMF)

OUTPUT FORMAT:
- Comprehensive merit hiring compliance assessment
- Specific merit principle violations or compliance gaps
- Prohibited personnel practice risk analysis
- Detailed remediation recommendations with policy citations
- Process improvement guidance for merit hiring compliance

Analyze the provided hiring process and assess compliance with federal merit system principles and OPM requirements.
```

---

## 🧪 Testing & Validation

### Test Scenarios
```python
# HR policy compliance testing scenarios
test_cases = [
    {
        "input": {
            "job_posting": {"series": "1560", "grade": "GS-13", "title": "Data Scientist"},
            "compliance_scope": {"merit_hiring": True, "veterans_preference": True}
        },
        "expected_output": {
            "omp_compliance": True,
            "merit_principles_compliance": True,
            "policy_violations": []
        },
        "success_criteria": [
            "All OPM standards met",
            "Merit hiring principles followed",
            "No policy violations identified"
        ]
    }
]
```

### NO BS Validation
- **Data Honesty**: Compliance assessments based on actual OPM regulations and federal law
- **Capability Limits**: Cannot access live USAJOBS data, provides policy-level analysis only
- **Accuracy Claims**: Policy recommendations validated against current OPM guidance and CFR

---

## 🔗 Related Resources

### OPM Resources
- [OPM Classification Standards](https://www.opm.gov/policy-data-oversight/classification-qualifications/classifying-general-schedule-positions/)
- [Merit System Principles](https://www.opm.gov/policy-data-oversight/hiring-information/merit-system-principles/)
- [Federal Hiring Process](https://www.opm.gov/policy-data-oversight/hiring-information/)

### USAJOBS Resources
- [USAJOBS API Documentation](https://developer.usajobs.gov/)
- [Federal Job Search Help](https://www.usajobs.gov/help/)
- [Application Process Guide](https://www.usajobs.gov/help/how-to/application/)

### Federal HR Law Resources
- [5 CFR Personnel Management](https://www.ecfr.gov/current/title-5)
- [5 USC Government Organization and Employees](https://www.govinfo.gov/content/pkg/USCODE-2011-title5/pdf/USCODE-2011-title5.pdf)
- [Federal Equal Employment Opportunity](https://www.eeoc.gov/federal-sector)

### Fed Job Advisor Resources
- [USAJOBS Integration](../../../backend/app/services/usajobs_service.py)
- [Job Classification System](../../../backend/app/models/job_series.py)
- [Federal HR Policy Documentation](../../../docs/federal-hr-policies.md)

---

*This agent specializes in federal HR policy compliance and merit hiring standards, ensuring Fed Job Advisor meets government requirements for fair and lawful federal hiring practices.*

**© 2025 Fed Job Advisor Agent System**
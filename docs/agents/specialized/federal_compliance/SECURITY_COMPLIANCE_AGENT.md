# Security & Compliance Agent - Fed Job Advisor MCP Agent

**Agent Type**: Federal Compliance  
**Domain**: OpenControl, NIST 800-53, USWDS Accessibility Security  
**Endpoint**: `http://localhost:8001/agents/security-compliance/analyze`  
**Status**: Active  

*Based on OpenControl framework, NIST 800-53 controls, and USWDS accessibility standards for 2025*

---

## 🎯 Agent Overview

### Primary Function
Specialized in federal security compliance, OpenControl documentation, NIST 800-53 control implementation, and USWDS accessibility compliance for Fed Job Advisor applications.

### Federal Expertise
- **NIST 800-53**: Security and Privacy Controls for Federal Information Systems
- **OpenControl Framework**: Automated compliance documentation and control mapping
- **USWDS Accessibility**: Section 508 compliance and accessibility testing standards
- **Federal Security Standards**: Government cybersecurity requirements and best practices

### Integration Value
- **Fed Job Advisor Use Cases**: Security audits, compliance documentation, accessibility validation, federal certification support
- **Claude Code Integration**: Security implementation guidance, compliance checking, accessibility fixes
- **Cost Efficiency**: ~$0.24/session (90% reduction vs cloud LLMs)

---

## 🔧 Technical Specification

### API Endpoint
```bash
POST http://localhost:8001/agents/security-compliance/analyze
```

### Input Schema
```json
{
  "user_id": "string",
  "task_type": "security_audit|compliance_documentation|accessibility_validation|control_implementation",
  "context": {
    "application_type": "web_application|api|mobile_app",
    "security_scope": {
      "authentication": "boolean",
      "authorization": "boolean",
      "data_encryption": "boolean",
      "network_security": "boolean",
      "audit_logging": "boolean"
    },
    "compliance_requirements": {
      "nist_800_53": ["control_family"],
      "section_508": "boolean",
      "fisma": "low|moderate|high",
      "fedramp": "boolean"
    },
    "current_implementation": {
      "security_controls": ["string"],
      "accessibility_features": ["string"],
      "documentation_status": "none|partial|complete"
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
  "agent_type": "security_compliance",
  "analysis": {
    "summary": "Security and compliance assessment",
    "security_assessment": {
      "nist_controls": {
        "implemented": ["string"],
        "missing": ["string"],
        "partially_implemented": ["string"]
      },
      "vulnerability_analysis": {
        "critical": ["string"],
        "high": ["string"],
        "medium": ["string"],
        "low": ["string"]
      },
      "compliance_score": "number"
    },
    "accessibility_assessment": {
      "wcag_compliance": {
        "level_a": "boolean",
        "level_aa": "boolean",
        "level_aaa": "boolean"
      },
      "section_508_compliance": "boolean",
      "accessibility_violations": ["string"],
      "accessibility_score": "number"
    }
  },
  "implementation_guidance": {
    "claude_code_instructions": "Step-by-step security implementation",
    "control_implementations": ["string"],
    "accessibility_fixes": ["string"],
    "documentation_templates": "object"
  },
  "compliance_documentation": {
    "opencontrol_yaml": "string",
    "nist_control_mapping": "object",
    "accessibility_report": "string"
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

### Security Audit and NIST Control Assessment
```python
import httpx

async def conduct_security_audit():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/security-compliance/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "security_audit",
                "context": {
                    "application_type": "web_application",
                    "security_scope": {
                        "authentication": True,
                        "authorization": True,
                        "data_encryption": True,
                        "network_security": True,
                        "audit_logging": True
                    },
                    "compliance_requirements": {
                        "nist_800_53": ["AC", "AU", "SC", "SI"],
                        "section_508": True,
                        "fisma": "moderate",
                        "fedramp": False
                    },
                    "current_implementation": {
                        "security_controls": ["JWT_auth", "HTTPS", "input_validation"],
                        "accessibility_features": ["alt_text", "keyboard_nav"],
                        "documentation_status": "partial"
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

### Accessibility Validation
```python
async def validate_accessibility():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/security-compliance/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "accessibility_validation",
                "context": {
                    "application_type": "web_application",
                    "compliance_requirements": {
                        "section_508": True
                    },
                    "current_implementation": {
                        "accessibility_features": ["semantic_html", "aria_labels"]
                    }
                }
            }
        )
        return response.json()
```

---

## 🚀 Fed Job Advisor Integration

### Use Cases
1. **Security Audits**: Comprehensive NIST 800-53 control assessment and gap analysis
2. **Compliance Documentation**: OpenControl framework implementation and automated documentation
3. **Accessibility Validation**: Section 508 and WCAG compliance testing and remediation
4. **Control Implementation**: Specific security control implementation guidance

### Integration Patterns
- **MCP Research Phase**: When Claude Code routes security and compliance tasks to this agent
- **Documentation Output**: Agent generates compliance docs in `_Management/_PM/_Tasks/COMPLIANCE_[AREA]_ASSESSMENT.md`
- **Implementation Guidance**: Specific security and accessibility implementation instructions
- **Testing Validation**: Compliance testing scenarios and validation procedures

### Task Routing Logic
```typescript
// When to use this agent
if (task.domain === "security" || 
    task.domain === "compliance" ||
    task.involves("nist") ||
    task.involves("accessibility") ||
    task.involves("section_508") ||
    task.involves("opencontrol")) {
    return await callMCPAgent("security-compliance", taskContext);
}
```

---

## 📊 Claude Prompt Templates

### Core Security & Compliance Prompt
```
You are a Security & Compliance Agent specialized in federal security standards, OpenControl framework, NIST 800-53 controls, and USWDS accessibility compliance for Fed Job Advisor.

EXPERTISE AREAS:
- NIST 800-53 Security and Privacy Controls (Rev 5)
- OpenControl framework for automated compliance documentation
- FISMA compliance requirements and risk assessment
- FedRAMP security requirements and controls
- Section 508 accessibility compliance and WCAG 2.1 guidelines
- USWDS accessibility patterns and testing procedures
- Federal cybersecurity frameworks and best practices
- Government data classification and handling requirements
- Federal authentication and authorization standards

FEDERAL SPECIALIZATION:
- Government security control implementation patterns
- Federal accessibility requirements and testing methodologies
- OpenControl YAML configuration and control mapping
- Government risk assessment and compliance documentation
- Federal certification and accreditation processes (C&A)
- Government-specific threat modeling and vulnerability assessment

TASK CAPABILITIES:
1. Security Audits: Comprehensive NIST 800-53 control assessment
2. Compliance Documentation: OpenControl framework implementation
3. Accessibility Validation: Section 508 and WCAG compliance testing
4. Control Implementation: Security control design and implementation guidance
5. Risk Assessment: Federal risk management and threat analysis
6. Documentation Generation: Automated compliance documentation creation
7. Remediation Planning: Gap analysis and remediation roadmaps

OUTPUT REQUIREMENTS:
- Provide detailed NIST 800-53 control mappings and implementation guidance
- Generate OpenControl YAML configurations for automated compliance
- Include comprehensive accessibility testing and remediation procedures
- Create federal-standard security documentation and reports
- Provide specific code examples for security control implementation
- Include compliance validation and testing procedures
- Generate risk assessment and mitigation strategies

INTEGRATION WITH FED JOB ADVISOR:
- Understand current security implementation in backend and frontend
- Follow established patterns for JWT authentication and authorization
- Consider existing accessibility features and improvement opportunities
- Align with federal data handling requirements for job application data

When receiving a security or compliance task, analyze current implementation, identify gaps against federal standards, provide detailed remediation guidance, and generate comprehensive compliance documentation.
```

### NIST 800-53 Control Implementation Prompt
```
You are implementing NIST 800-53 security controls for Fed Job Advisor's federal compliance requirements.

NIST 800-53 CONTROL FAMILIES:
- AC (Access Control): User authentication, authorization, and access management
- AU (Audit and Accountability): Security event logging and monitoring
- CA (Security Assessment and Authorization): Continuous monitoring and assessment
- CM (Configuration Management): System configuration and change control
- CP (Contingency Planning): Backup, recovery, and business continuity
- IA (Identification and Authentication): User and device authentication
- IR (Incident Response): Security incident handling and response
- MA (Maintenance): System maintenance and remote access controls
- MP (Media Protection): Removable media and data handling
- PE (Physical and Environmental Protection): Physical security controls
- PL (Planning): Security planning and documentation
- PS (Personnel Security): Personnel screening and access controls
- RA (Risk Assessment): Risk management and vulnerability assessment
- SA (System and Services Acquisition): Supply chain risk management
- SC (System and Communications Protection): Network and system security
- SI (System and Information Integrity): Malware protection and information integrity

FEDERAL IMPLEMENTATION REQUIREMENTS:
- Control implementation appropriate for FISMA impact level (Low/Moderate/High)
- Integration with existing Fed Job Advisor security architecture
- Consideration of government user workflows and federal data handling
- Documentation requirements for federal certification and accreditation
- Continuous monitoring and compliance validation procedures

CONTROL IMPLEMENTATION PATTERNS:
- Authentication: JWT-based with multi-factor authentication support
- Authorization: Role-based access control (RBAC) with federal job series mapping
- Audit Logging: Comprehensive security event logging with federal retention requirements
- Data Protection: Encryption at rest and in transit for federal job application data
- Network Security: HTTPS enforcement and secure API communications

OUTPUT FORMAT:
- Specific control implementation recommendations with code examples
- OpenControl YAML configuration for automated compliance documentation
- Implementation timelines and resource requirements
- Testing and validation procedures for each control
- Integration guidance with existing Fed Job Advisor components

Analyze the specified NIST controls and provide detailed implementation guidance for Fed Job Advisor's federal compliance requirements.
```

### Accessibility Compliance Prompt
```
You are conducting accessibility compliance validation for Fed Job Advisor using Section 508 and WCAG 2.1 standards.

ACCESSIBILITY STANDARDS:
- Section 508 (29 USC 794d): Federal accessibility requirements
- WCAG 2.1 Level AA: Web Content Accessibility Guidelines
- USWDS Accessibility Guidelines: US Web Design System standards
- Federal Plain Language Requirements: Clear communication standards

ACCESSIBILITY TESTING AREAS:
1. Semantic HTML: Proper use of heading hierarchy, landmarks, and form labels
2. Keyboard Navigation: Full keyboard accessibility and focus management
3. Screen Reader Compatibility: ARIA attributes and assistive technology support
4. Color and Contrast: Sufficient color contrast ratios and color-independent design
5. Alternative Text: Comprehensive alt text for images and media
6. Form Accessibility: Label associations, error messages, and help text
7. Dynamic Content: Accessible updates and live region announcements
8. Mobile Accessibility: Touch target sizes and mobile screen reader support

FEDERAL REQUIREMENTS:
- Must meet Section 508 standards for government applications
- USWDS component accessibility patterns and implementations
- Federal user accommodation requirements
- Government employee accessibility needs assessment
- Multi-device accessibility for federal workers

TESTING METHODOLOGY:
- Automated testing with axe-core or similar tools
- Manual keyboard navigation testing
- Screen reader testing with NVDA/JAWS/VoiceOver
- Color contrast analysis and color blindness simulation
- Mobile accessibility testing on government-approved devices

OUTPUT FORMAT:
- Comprehensive accessibility audit report with WCAG success criteria mapping
- Specific accessibility violations with remediation guidance
- Code examples for accessibility improvements
- Testing procedures and validation steps
- Section 508 compliance certification documentation

Analyze the provided application components and provide detailed accessibility compliance assessment with specific remediation guidance.
```

---

## 🧪 Testing & Validation

### Test Scenarios
```python
# Security and compliance testing scenarios
test_cases = [
    {
        "input": {
            "application_type": "web_application",
            "compliance_requirements": {"nist_800_53": ["AC", "AU"], "section_508": True}
        },
        "expected_output": {
            "compliance_score": ">= 85",
            "nist_controls_implemented": ">= 80%",
            "accessibility_score": ">= 95%"
        },
        "success_criteria": [
            "All critical security controls implemented",
            "Section 508 compliance achieved",
            "OpenControl documentation generated"
        ]
    }
]
```

### NO BS Validation
- **Data Honesty**: Compliance scores based on actual NIST and WCAG validation criteria
- **Capability Limits**: Cannot perform penetration testing, provides code-level security analysis
- **Accuracy Claims**: Security recommendations validated against federal standards and best practices

---

## 🔗 Related Resources

### NIST Security Resources
- [NIST 800-53 Security Controls](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [FISMA Implementation Project](https://csrc.nist.gov/projects/risk-management/fisma-background)
- [FedRAMP Security Controls](https://www.fedramp.gov/assets/resources/documents/FedRAMP_Security_Controls_Baseline.xlsx)

### OpenControl Resources
- [OpenControl Framework](https://opencontrol.xyz/)
- [Compliance Masonry](https://github.com/opencontrol/compliance-masonry)
- [OpenControl Components](https://github.com/opencontrol/compliance-masonry/tree/master/fixtures/opencontrol)

### Accessibility Resources
- [Section 508 Guidelines](https://www.section508.gov/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [USWDS Accessibility Guide](https://designsystem.digital.gov/documentation/accessibility/)

### Fed Job Advisor Resources
- [Security Implementation](../../../backend/app/core/security.py)
- [Accessibility Features](../../../frontend/src/components/accessibility/)
- [Compliance Documentation](../../../docs/compliance/)

---

*This agent specializes in federal security compliance and accessibility standards, ensuring Fed Job Advisor meets government requirements for security and accessibility.*

**© 2025 Fed Job Advisor Agent System**
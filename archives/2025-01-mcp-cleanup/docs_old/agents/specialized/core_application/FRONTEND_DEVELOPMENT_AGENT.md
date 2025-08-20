# Frontend Development Agent - Fed Job Advisor MCP Agent

**Agent Type**: Core Application  
**Domain**: React + Next.js 14 + shadcn/ui Frontend Development  
**Endpoint**: `http://localhost:8001/agents/frontend-development/analyze`  
**Status**: Active  

*Based on shadcn/ui, React+Tailwind, and accessibility best practices for 2025*

---

## 🎯 Agent Overview

### Primary Function
Specialized in React + Next.js 14 + shadcn/ui frontend development for Fed Job Advisor, focusing on accessibility, responsive design, and federal compliance standards.

### Federal Expertise
- **USWDS Integration**: US Web Design System compliance for federal applications
- **Accessibility Standards**: WCAG 2.1 AA compliance for federal accessibility requirements
- **Federal UI Patterns**: Government interface design patterns and user experience standards

### Integration Value
- **Fed Job Advisor Use Cases**: Frontend component development, UI/UX optimization, accessibility compliance
- **Claude Code Integration**: Component generation, responsive design fixes, accessibility audits
- **Cost Efficiency**: ~$0.24/session (90% reduction vs cloud LLMs)

---

## 🔧 Technical Specification

### API Endpoint
```bash
POST http://localhost:8001/agents/frontend-development/analyze
```

### Input Schema
```json
{
  "user_id": "string",
  "task_type": "component_development|ui_fix|accessibility_audit|responsive_design",
  "context": {
    "component_type": "string",
    "existing_code": "string",
    "requirements": {
      "accessibility": "boolean",
      "responsive": "boolean", 
      "federal_compliance": "boolean"
    },
    "design_system": "shadcn|uswds|custom",
    "target_pages": ["string"]
  },
  "requirements": {
    "analysis_depth": "basic|detailed|comprehensive",
    "include_tests": "boolean",
    "include_storybook": "boolean"
  }
}
```

### Output Schema
```json
{
  "agent_type": "frontend_development",
  "analysis": {
    "summary": "Component analysis and recommendations",
    "component_structure": "Recommended component architecture",
    "accessibility_compliance": {
      "wcag_level": "A|AA|AAA",
      "compliance_score": "number",
      "violations": ["string"],
      "fixes": ["string"]
    },
    "performance_metrics": {
      "bundle_size_impact": "string",
      "render_performance": "string", 
      "lighthouse_score_estimate": "number"
    }
  },
  "implementation_guidance": {
    "claude_code_instructions": "Step-by-step component implementation",
    "files_to_create": ["string"],
    "files_to_modify": ["string"],
    "dependencies_to_add": ["string"],
    "testing_approach": "Jest + Testing Library test structure"
  },
  "code_templates": {
    "component_code": "string",
    "styles_code": "string", 
    "test_code": "string",
    "storybook_code": "string"
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

### Frontend Component Development
```python
import httpx

async def develop_component():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/frontend-development/analyze",
            json={
                "user_id": "dev_session_123",
                "task_type": "component_development",
                "context": {
                    "component_type": "JobSearchCard",
                    "requirements": {
                        "accessibility": True,
                        "responsive": True,
                        "federal_compliance": True
                    },
                    "design_system": "shadcn",
                    "target_pages": ["dashboard", "job-search"]
                },
                "requirements": {
                    "analysis_depth": "comprehensive",
                    "include_tests": True,
                    "include_storybook": True
                }
            }
        )
        return response.json()
```

### Accessibility Audit
```python
async def audit_accessibility():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/agents/frontend-development/analyze",
            json={
                "user_id": "dev_session_123", 
                "task_type": "accessibility_audit",
                "context": {
                    "existing_code": "...",
                    "requirements": {
                        "accessibility": True,
                        "federal_compliance": True
                    }
                }
            }
        )
        return response.json()
```

---

## 🚀 Fed Job Advisor Integration

### Use Cases
1. **Component Development**: Create new React components using shadcn/ui patterns
2. **Accessibility Compliance**: Ensure WCAG 2.1 AA compliance for federal requirements  
3. **Responsive Design**: Optimize components for mobile-first federal users
4. **Performance Optimization**: Bundle size analysis and rendering performance

### Integration Patterns
- **MCP Research Phase**: When Claude Code routes frontend development tasks to this agent
- **Documentation Output**: Agent generates component specs in `_Management/_PM/_Tasks/FRONTEND_[COMPONENT]_SPEC.md`
- **Implementation Guidance**: Specific React/Next.js implementation instructions
- **Testing Validation**: Jest + Testing Library test scenarios

### Task Routing Logic
```typescript
// When to use this agent
if (task.domain === "frontend" || 
    task.type === "component_development" ||
    task.involves("react") || 
    task.involves("nextjs") ||
    task.involves("accessibility")) {
    return await callMCPAgent("frontend-development", taskContext);
}
```

---

## 📊 Claude Prompt Templates

### Core Frontend Development Prompt
```
You are a Frontend Development Agent specialized in React + Next.js 14 + shadcn/ui development for Fed Job Advisor.

EXPERTISE AREAS:
- shadcn/ui component library patterns and customization
- Next.js 14 App Router architecture and server components  
- Tailwind CSS responsive design and component styling
- React Hook patterns and state management
- WCAG 2.1 AA accessibility compliance
- US Web Design System (USWDS) integration for federal compliance
- Jest + Testing Library component testing
- Storybook component documentation

FEDERAL SPECIALIZATION:
- Government interface design patterns
- Federal accessibility requirements (Section 508 compliance)
- USWDS design tokens and component patterns
- Government user experience standards
- Mobile-first design for federal employees

TASK CAPABILITIES:
1. Component Development: Create new React components following shadcn/ui patterns
2. Accessibility Audits: Analyze and fix WCAG compliance issues
3. Responsive Design: Optimize layouts for all device sizes  
4. Performance Analysis: Bundle size and rendering optimization
5. Federal Compliance: Ensure USWDS and Section 508 compliance
6. Testing Strategy: Component testing with Jest + Testing Library
7. Code Reviews: Frontend architecture and best practice validation

OUTPUT REQUIREMENTS:
- Provide complete, production-ready component code
- Include comprehensive accessibility features (ARIA labels, keyboard navigation, screen reader support)
- Follow shadcn/ui conventions and patterns exactly
- Include responsive Tailwind classes for mobile-first design
- Generate complete test suites with Jest + Testing Library
- Provide Storybook stories for component documentation
- Ensure federal design system compliance

INTEGRATION WITH FED JOB ADVISOR:
- Understand existing component architecture in frontend/src/components/
- Follow established patterns for API integration with backend
- Maintain consistency with existing design system implementation
- Consider federal user workflows and government employee needs

When receiving a frontend development task, analyze the requirements, provide architectural recommendations, generate production-ready code, and include comprehensive testing and documentation.
```

### Accessibility Audit Prompt
```
You are conducting an accessibility audit for Fed Job Advisor frontend components.

ACCESSIBILITY STANDARDS:
- WCAG 2.1 AA compliance (federal requirement)
- Section 508 compliance for federal applications
- ARIA best practices for screen readers
- Keyboard navigation support
- Color contrast requirements (4.5:1 minimum)
- Focus management and visual indicators

AUDIT CHECKLIST:
1. Semantic HTML structure
2. Proper ARIA labels and roles
3. Keyboard navigation flow
4. Screen reader compatibility
5. Color contrast ratios
6. Focus trap management
7. Alternative text for images
8. Form label associations
9. Error message accessibility
10. Mobile accessibility

FEDERAL REQUIREMENTS:
- Must meet Section 508 standards
- Government employee accessibility needs
- USWDS accessibility patterns
- Multi-device accessibility for federal workers

OUTPUT FORMAT:
- Compliance score (0-100)
- Specific violations with line numbers
- Detailed fix recommendations
- Code examples for corrections
- Testing instructions for validation

Analyze the provided component code and identify all accessibility issues, providing specific remediation guidance.
```

---

## 🧪 Testing & Validation

### Test Scenarios
```python
# Frontend component testing scenarios
test_cases = [
    {
        "input": {
            "component_type": "JobCard",
            "requirements": {"accessibility": True, "responsive": True}
        },
        "expected_output": {
            "compliance_score": ">= 95",
            "includes_aria_labels": True,
            "responsive_breakpoints": ["sm", "md", "lg", "xl"]
        },
        "success_criteria": [
            "WCAG 2.1 AA compliance",
            "Mobile-first responsive design",
            "shadcn/ui pattern compliance"
        ]
    }
]
```

### NO BS Validation
- **Data Honesty**: Accessibility scores based on actual WCAG validation tools
- **Capability Limits**: Cannot test in real browsers, provides code-level analysis only
- **Accuracy Claims**: Component recommendations tested against shadcn/ui documentation

---

## 🔗 Related Resources

### shadcn/ui Resources
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [shadcn/ui GitHub](https://github.com/shadcn-ui/ui)
- [Radix UI Primitives](https://www.radix-ui.com/primitives)

### Federal Compliance Resources  
- [US Web Design System](https://designsystem.digital.gov/)
- [Section 508 Guidelines](https://www.section508.gov/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### Fed Job Advisor Resources
- [Frontend Component Library](../../../frontend/src/components/)
- [Design System Implementation](../../../frontend/src/lib/design-system/)
- [Accessibility Testing Guide](../../../docs/accessibility-testing.md)

---

*This agent specializes in modern React development with federal compliance standards, optimized for Fed Job Advisor's government user base.*

**© 2025 Fed Job Advisor Agent System**
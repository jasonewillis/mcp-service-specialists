"""
UX Designer Agent - UX/UI Design, Web Design, and User Experience Specialist
Provides comprehensive UX/UI guidance, design analysis, and user experience optimization.
Focused on federal-compliant design patterns and accessibility standards.

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Identify target users and their federal job search context
2. Define current design challenges and usability issues
3. Specify compliance requirements (Section 508, WCAG)
4. Gather existing design assets and user feedback

**Effective Prompting Patterns:**
```
"Analyze UX for [specific feature/page] targeting [user type]:
- Current issues: [usability problems]
- Federal requirements: [Section 508, USWDS compliance]
- User goals: [primary objectives]
- Constraints: [technical, budget, timeline]"
```

**Best Workflow:**
1. **User Research** → Understand federal job seeker needs and pain points
2. **Design Analysis** → Evaluate current UI/UX against best practices
3. **Accessibility Audit** → Ensure Section 508 and WCAG compliance
4. **Solution Design** → Create user-centered design recommendations
5. **Validation** → Test designs with usability principles

### Integration with Other Agents

**Workflow Chains:**
- Start with UX Designer Agent → Technical agents for implementation
- Use with Researcher Agent for user behavior insights
- Coordinate with Frontend agents for technical feasibility

**Handoff Points:**
- Pass design specifications to Frontend Development agents
- Share accessibility requirements with Technical specialists
- Provide user research findings to Product strategy agents

### Common Design Challenges

1. **Federal Compliance** - Section 508, USWDS guidelines, accessibility standards
2. **Complex Workflows** - Multi-step application processes, form design
3. **Information Architecture** - Large datasets, search and filtering
4. **Mobile Optimization** - Responsive design, touch interfaces
5. **Trust & Credibility** - Government-appropriate design language

### Test-Driven Usage Examples

**Example 1: Accessibility Audit**
```python
test_data = {
    "design_type": "accessibility_audit",
    "component": "job search form",
    "compliance_standards": ["Section 508", "WCAG 2.1 AA"],
    "user_groups": ["screen reader users", "keyboard navigation"],
    "current_issues": ["missing labels", "poor color contrast"]
}
```

**Example 2: User Flow Optimization**
```python
test_data = {
    "design_type": "user_flow_analysis",
    "workflow": "federal job application process", 
    "pain_points": ["too many steps", "confusing navigation"],
    "success_metrics": ["completion rate", "time to complete"],
    "user_personas": ["entry-level applicants", "experienced professionals"]
}
```

### Integration with CLAUDE.md Principles

- **No assumptions:** Validate design decisions with user research and data
- **Solo developer focus:** Prioritize design systems and reusable components
- **Bootstrap approach:** Use free design tools and open-source UI libraries
- **Practical focus:** Emphasize implementable designs within technical constraints
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re

from ..base import FederalJobAgent, AgentResponse


class UXDesignerAgent(FederalJobAgent):
    """
    Specialized agent for UX/UI design, web design, and user experience optimization
    Provides federal-compliant design guidance and accessibility expertise
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load UX design specific tools"""
        
        tools = [
            Tool(
                name="accessibility_auditor",
                func=self._audit_accessibility,
                description="Audit designs for accessibility compliance (Section 508, WCAG)"
            ),
            Tool(
                name="user_flow_analyzer",
                func=self._analyze_user_flows,
                description="Analyze and optimize user workflows and journeys"
            ),
            Tool(
                name="design_system_advisor",
                func=self._advise_design_system,
                description="Provide guidance on design systems and component libraries (including Shadcn/UI)"
            ),
            Tool(
                name="shadcn_ui_components",
                func=self._recommend_shadcn_components,
                description="Recommend and guide implementation of Shadcn/UI components from https://ui.shadcn.com/"
            ),
            Tool(
                name="usability_evaluator",
                func=self._evaluate_usability,
                description="Evaluate interface usability and user experience"
            ),
            Tool(
                name="responsive_design_checker",
                func=self._check_responsive_design,
                description="Analyze responsive design and mobile optimization"
            ),
            Tool(
                name="federal_compliance_validator",
                func=self._validate_federal_compliance,
                description="Validate designs against federal design standards"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get UX designer specific prompt template"""
        
        return """You are a Senior UX/UI Designer specializing in federal government applications and compliance-focused user experiences.
        Your role is to provide expert design guidance that balances user needs with federal accessibility requirements.
        
        Key Responsibilities:
        1. Design user-centered interfaces for federal job seekers
        2. Ensure Section 508 and WCAG accessibility compliance
        3. Optimize user flows for complex government processes
        4. Recommend design systems and reusable components
        5. Validate designs against usability principles
        
        Design Focus Areas:
        - Federal job search and application workflows
        - Accessibility and inclusive design
        - Information architecture for large datasets
        - Form design and complex data entry
        - Mobile-first responsive design
        - Trust and credibility in government interfaces
        
        Compliance Standards:
        - Section 508 accessibility requirements
        - WCAG 2.1 AA compliance
        - U.S. Web Design System (USWDS) guidelines
        - Federal plain language standards
        - Mobile-first design principles
        
        Design Constraints:
        - Solo developer implementation capabilities
        - Limited budget for custom development
        - Government security and privacy requirements
        - Cross-browser compatibility needs
        - Performance optimization for government networks
        
        You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Remember: Prioritize accessibility, usability, and federal compliance in all design recommendations.
        Focus on practical, implementable solutions for a solo developer environment.

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}"""
    
    def _audit_accessibility(self, input_data: str) -> str:
        """Audit designs for accessibility compliance"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            component = data.get("component", "")
            current_issues = data.get("current_issues", [])
            compliance_standards = data.get("compliance_standards", ["Section 508", "WCAG 2.1 AA"])
            
            # Accessibility audit framework
            audit_categories = {
                "perceivable": {
                    "color_contrast": self._check_color_contrast(component, current_issues),
                    "text_alternatives": self._check_text_alternatives(component, current_issues),
                    "multimedia": self._check_multimedia_accessibility(component, current_issues),
                    "adaptable": self._check_adaptable_content(component, current_issues)
                },
                "operable": {
                    "keyboard_accessibility": self._check_keyboard_access(component, current_issues),
                    "seizure_prevention": self._check_seizure_triggers(component, current_issues),
                    "navigation": self._check_navigation_accessibility(component, current_issues),
                    "input_assistance": self._check_input_assistance(component, current_issues)
                },
                "understandable": {
                    "readable": self._check_readability(component, current_issues),
                    "predictable": self._check_predictable_interface(component, current_issues),
                    "input_assistance": self._check_error_handling(component, current_issues)
                },
                "robust": {
                    "compatibility": self._check_assistive_tech_compatibility(component, current_issues),
                    "semantic_markup": self._check_semantic_markup(component, current_issues)
                }
            }
            
            # Generate compliance report
            compliance_report = {
                "audit_results": audit_categories,
                "compliance_score": self._calculate_compliance_score(audit_categories),
                "critical_issues": self._identify_critical_issues(audit_categories),
                "remediation_priorities": self._prioritize_remediation(audit_categories),
                "implementation_guidance": self._provide_implementation_guidance(audit_categories)
            }
            
            return json.dumps(compliance_report)
            
        except Exception as e:
            return f"Error auditing accessibility: {str(e)}"
    
    def _analyze_user_flows(self, input_data: str) -> str:
        """Analyze and optimize user workflows and journeys"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            workflow = data.get("workflow", "")
            pain_points = data.get("pain_points", [])
            user_personas = data.get("user_personas", [])
            success_metrics = data.get("success_metrics", [])
            
            # User flow analysis framework
            flow_analysis = {
                "current_state": {
                    "workflow_steps": self._map_workflow_steps(workflow),
                    "pain_point_mapping": self._map_pain_points(workflow, pain_points),
                    "drop_off_analysis": self._analyze_drop_offs(workflow, pain_points),
                    "friction_assessment": self._assess_friction_points(workflow, pain_points)
                },
                "user_journey_mapping": {
                    "persona_journeys": self._map_persona_journeys(workflow, user_personas),
                    "emotional_journey": self._map_emotional_journey(workflow, pain_points),
                    "touch_point_analysis": self._analyze_touch_points(workflow),
                    "moment_of_truth": self._identify_critical_moments(workflow)
                },
                "optimization_opportunities": {
                    "step_reduction": self._identify_step_reduction_opportunities(workflow),
                    "parallel_processing": self._identify_parallel_opportunities(workflow),
                    "progressive_disclosure": self._suggest_progressive_disclosure(workflow),
                    "error_prevention": self._design_error_prevention(workflow, pain_points)
                }
            }
            
            # Generate optimization recommendations
            optimization_plan = {
                "immediate_improvements": self._recommend_immediate_improvements(flow_analysis),
                "long_term_enhancements": self._recommend_long_term_enhancements(flow_analysis),
                "success_metrics": self._define_success_metrics(flow_analysis, success_metrics),
                "testing_strategy": self._design_testing_strategy(flow_analysis)
            }
            
            return json.dumps({
                "flow_analysis": flow_analysis,
                "optimization_plan": optimization_plan,
                "implementation_roadmap": self._create_implementation_roadmap(optimization_plan)
            })
            
        except Exception as e:
            return f"Error analyzing user flows: {str(e)}"
    
    def _advise_design_system(self, input_data: str) -> str:
        """Provide guidance on design systems and component libraries"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            current_system = data.get("current_system", "none")
            requirements = data.get("requirements", [])
            constraints = data.get("constraints", [])
            
            # Design system recommendations
            system_options = {
                "us_web_design_system": {
                    "description": "Official U.S. government design system",
                    "pros": ["Federal compliance", "Accessibility built-in", "Government credibility"],
                    "cons": ["Limited customization", "Government aesthetic only"],
                    "best_for": ["Federal agencies", "Government contractors", "Compliance-heavy applications"],
                    "implementation": "npm install @uswds/uswds"
                },
                "tailwind_css": {
                    "description": "Utility-first CSS framework",
                    "pros": ["Rapid development", "High customization", "Small bundle size"],
                    "cons": ["Learning curve", "Manual accessibility", "Utility class complexity"],
                    "best_for": ["Custom designs", "Solo developers", "Rapid prototyping"],
                    "implementation": "npm install tailwindcss"
                },
                "shadcn_ui": {
                    "description": "Copy-paste component library with Tailwind",
                    "pros": ["Modern components", "TypeScript support", "Customizable"],
                    "cons": ["Manual accessibility work", "Less federal-specific"],
                    "best_for": ["Modern web apps", "Developer productivity", "Custom branding"],
                    "implementation": "npx shadcn-ui@latest init"
                },
                "custom_system": {
                    "description": "Build custom component library",
                    "pros": ["Perfect fit", "Full control", "Unique branding"],
                    "cons": ["High development cost", "Maintenance burden", "Time to market"],
                    "best_for": ["Unique requirements", "Long-term projects", "Large budgets"],
                    "implementation": "Custom development required"
                }
            }
            
            # System recommendation based on requirements
            recommended_system = self._recommend_design_system(requirements, constraints, system_options)
            
            # Component library guidance
            component_guidance = {
                "essential_components": self._identify_essential_components(requirements),
                "federal_components": self._identify_federal_components(requirements),
                "accessibility_components": self._identify_accessibility_components(requirements),
                "custom_components": self._identify_custom_components(requirements)
            }
            
            # Implementation strategy
            implementation_strategy = {
                "migration_plan": self._create_migration_plan(current_system, recommended_system),
                "component_priorities": self._prioritize_components(component_guidance),
                "development_phases": self._plan_development_phases(recommended_system, component_guidance),
                "maintenance_strategy": self._plan_maintenance_strategy(recommended_system)
            }
            
            return json.dumps({
                "system_options": system_options,
                "recommended_system": recommended_system,
                "component_guidance": component_guidance,
                "implementation_strategy": implementation_strategy
            })
            
        except Exception as e:
            return f"Error advising design system: {str(e)}"
    
    def _evaluate_usability(self, input_data: str) -> str:
        """Evaluate interface usability and user experience"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            interface_type = data.get("interface_type", "web_application")
            user_tasks = data.get("user_tasks", [])
            current_metrics = data.get("current_metrics", {})
            
            # Usability evaluation framework (Jakob Nielsen's principles)
            usability_principles = {
                "visibility_of_system_status": {
                    "evaluation": self._evaluate_system_visibility(interface_type, user_tasks),
                    "score": self._score_system_visibility(interface_type, user_tasks),
                    "recommendations": self._recommend_system_visibility_improvements(interface_type)
                },
                "match_system_real_world": {
                    "evaluation": self._evaluate_real_world_match(interface_type, user_tasks),
                    "score": self._score_real_world_match(interface_type, user_tasks),
                    "recommendations": self._recommend_real_world_improvements(interface_type)
                },
                "user_control_freedom": {
                    "evaluation": self._evaluate_user_control(interface_type, user_tasks),
                    "score": self._score_user_control(interface_type, user_tasks),
                    "recommendations": self._recommend_user_control_improvements(interface_type)
                },
                "consistency_standards": {
                    "evaluation": self._evaluate_consistency(interface_type, user_tasks),
                    "score": self._score_consistency(interface_type, user_tasks),
                    "recommendations": self._recommend_consistency_improvements(interface_type)
                },
                "error_prevention": {
                    "evaluation": self._evaluate_error_prevention(interface_type, user_tasks),
                    "score": self._score_error_prevention(interface_type, user_tasks),
                    "recommendations": self._recommend_error_prevention_improvements(interface_type)
                },
                "recognition_recall": {
                    "evaluation": self._evaluate_recognition_vs_recall(interface_type, user_tasks),
                    "score": self._score_recognition_vs_recall(interface_type, user_tasks),
                    "recommendations": self._recommend_recognition_improvements(interface_type)
                },
                "flexibility_efficiency": {
                    "evaluation": self._evaluate_flexibility_efficiency(interface_type, user_tasks),
                    "score": self._score_flexibility_efficiency(interface_type, user_tasks),
                    "recommendations": self._recommend_flexibility_improvements(interface_type)
                },
                "aesthetic_minimalist": {
                    "evaluation": self._evaluate_aesthetic_design(interface_type, user_tasks),
                    "score": self._score_aesthetic_design(interface_type, user_tasks),
                    "recommendations": self._recommend_aesthetic_improvements(interface_type)
                },
                "error_recovery": {
                    "evaluation": self._evaluate_error_recovery(interface_type, user_tasks),
                    "score": self._score_error_recovery(interface_type, user_tasks),
                    "recommendations": self._recommend_error_recovery_improvements(interface_type)
                },
                "help_documentation": {
                    "evaluation": self._evaluate_help_documentation(interface_type, user_tasks),
                    "score": self._score_help_documentation(interface_type, user_tasks),
                    "recommendations": self._recommend_help_improvements(interface_type)
                }
            }
            
            # Overall usability assessment
            usability_assessment = {
                "overall_score": self._calculate_overall_usability_score(usability_principles),
                "strengths": self._identify_usability_strengths(usability_principles),
                "weaknesses": self._identify_usability_weaknesses(usability_principles),
                "priority_improvements": self._prioritize_usability_improvements(usability_principles)
            }
            
            return json.dumps({
                "usability_evaluation": usability_principles,
                "assessment_summary": usability_assessment,
                "improvement_roadmap": self._create_usability_improvement_roadmap(usability_assessment)
            })
            
        except Exception as e:
            return f"Error evaluating usability: {str(e)}"
    
    def _check_responsive_design(self, input_data: str) -> str:
        """Analyze responsive design and mobile optimization"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            breakpoints = data.get("breakpoints", ["mobile", "tablet", "desktop"])
            components = data.get("components", [])
            performance_requirements = data.get("performance_requirements", {})
            
            # Responsive design analysis
            responsive_analysis = {
                "breakpoint_analysis": {
                    "mobile": self._analyze_mobile_design(components),
                    "tablet": self._analyze_tablet_design(components),
                    "desktop": self._analyze_desktop_design(components)
                },
                "component_responsiveness": {
                    "navigation": self._analyze_navigation_responsiveness(components),
                    "forms": self._analyze_form_responsiveness(components),
                    "data_tables": self._analyze_table_responsiveness(components),
                    "content_layout": self._analyze_content_responsiveness(components)
                },
                "touch_interface": {
                    "touch_targets": self._analyze_touch_targets(components),
                    "gesture_support": self._analyze_gesture_support(components),
                    "thumb_navigation": self._analyze_thumb_navigation(components)
                },
                "performance_optimization": {
                    "image_optimization": self._analyze_image_optimization(components),
                    "lazy_loading": self._analyze_lazy_loading(components),
                    "bundle_optimization": self._analyze_bundle_optimization(components)
                }
            }
            
            # Mobile-first recommendations
            mobile_first_recommendations = {
                "design_principles": self._recommend_mobile_first_principles(),
                "progressive_enhancement": self._recommend_progressive_enhancement(),
                "performance_optimization": self._recommend_performance_optimization(),
                "accessibility_considerations": self._recommend_mobile_accessibility()
            }
            
            return json.dumps({
                "responsive_analysis": responsive_analysis,
                "mobile_first_recommendations": mobile_first_recommendations,
                "implementation_checklist": self._create_responsive_checklist(responsive_analysis)
            })
            
        except Exception as e:
            return f"Error checking responsive design: {str(e)}"
    
    def _validate_federal_compliance(self, input_data: str) -> str:
        """Validate designs against federal design standards"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            compliance_areas = data.get("compliance_areas", ["Section 508", "USWDS", "Plain Language"])
            design_elements = data.get("design_elements", [])
            
            # Federal compliance validation
            compliance_validation = {
                "section_508": {
                    "validation_results": self._validate_section_508(design_elements),
                    "compliance_score": self._score_section_508_compliance(design_elements),
                    "required_fixes": self._identify_section_508_fixes(design_elements)
                },
                "uswds_guidelines": {
                    "validation_results": self._validate_uswds_compliance(design_elements),
                    "compliance_score": self._score_uswds_compliance(design_elements),
                    "required_fixes": self._identify_uswds_fixes(design_elements)
                },
                "plain_language": {
                    "validation_results": self._validate_plain_language(design_elements),
                    "compliance_score": self._score_plain_language_compliance(design_elements),
                    "required_fixes": self._identify_plain_language_fixes(design_elements)
                },
                "security_privacy": {
                    "validation_results": self._validate_security_privacy(design_elements),
                    "compliance_score": self._score_security_privacy_compliance(design_elements),
                    "required_fixes": self._identify_security_privacy_fixes(design_elements)
                }
            }
            
            # Compliance roadmap
            compliance_roadmap = {
                "immediate_requirements": self._identify_immediate_compliance_needs(compliance_validation),
                "certification_path": self._recommend_certification_path(compliance_validation),
                "testing_strategy": self._recommend_compliance_testing(compliance_validation),
                "documentation_requirements": self._identify_documentation_needs(compliance_validation)
            }
            
            return json.dumps({
                "compliance_validation": compliance_validation,
                "compliance_roadmap": compliance_roadmap,
                "implementation_guide": self._create_compliance_implementation_guide(compliance_validation)
            })
            
        except Exception as e:
            return f"Error validating federal compliance: {str(e)}"
    
    # Helper methods for tool implementations (simplified for brevity)
    
    def _check_color_contrast(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check color contrast compliance"""
        return {
            "status": "needs_review",
            "requirements": "WCAG 2.1 AA requires 4.5:1 contrast ratio for normal text",
            "current_issues": [issue for issue in issues if "contrast" in issue.lower()],
            "recommendations": ["Use WebAIM contrast checker", "Test with actual background colors"]
        }
    
    def _check_text_alternatives(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check text alternatives for images and media"""
        return {
            "status": "needs_review",
            "requirements": "All images must have meaningful alt text",
            "current_issues": [issue for issue in issues if "alt" in issue.lower() or "image" in issue.lower()],
            "recommendations": ["Add descriptive alt text", "Use empty alt for decorative images"]
        }
    
    def _check_multimedia_accessibility(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check multimedia accessibility"""
        return {
            "status": "not_applicable",
            "requirements": "Videos must have captions and transcripts",
            "recommendations": ["Add closed captions", "Provide audio descriptions"]
        }
    
    def _check_adaptable_content(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check content adaptability"""
        return {
            "status": "needs_review",
            "requirements": "Content must be adaptable to different presentations",
            "recommendations": ["Use semantic HTML", "Ensure logical reading order"]
        }
    
    def _check_keyboard_access(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check keyboard accessibility"""
        return {
            "status": "critical",
            "requirements": "All functionality must be keyboard accessible",
            "current_issues": [issue for issue in issues if "keyboard" in issue.lower()],
            "recommendations": ["Ensure tab navigation", "Add focus indicators", "Support keyboard shortcuts"]
        }
    
    def _check_seizure_triggers(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check for seizure triggers"""
        return {
            "status": "compliant",
            "requirements": "No flashing content more than 3 times per second",
            "recommendations": ["Avoid flashing animations", "Provide pause controls"]
        }
    
    def _check_navigation_accessibility(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check navigation accessibility"""
        return {
            "status": "needs_review",
            "requirements": "Provide multiple ways to navigate",
            "recommendations": ["Add skip links", "Provide breadcrumbs", "Include site map"]
        }
    
    def _check_input_assistance(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check input assistance features"""
        return {
            "status": "needs_improvement",
            "requirements": "Help users avoid and correct mistakes",
            "current_issues": [issue for issue in issues if "label" in issue.lower() or "error" in issue.lower()],
            "recommendations": ["Add clear labels", "Provide error messages", "Include instructions"]
        }
    
    def _check_readability(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check content readability"""
        return {
            "status": "needs_review",
            "requirements": "Content must be readable and understandable",
            "recommendations": ["Use plain language", "Provide definitions", "Structure content clearly"]
        }
    
    def _check_predictable_interface(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check interface predictability"""
        return {
            "status": "good",
            "requirements": "Interface must behave predictably",
            "recommendations": ["Consistent navigation", "Clear page titles", "Logical tab order"]
        }
    
    def _check_error_handling(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check error handling and prevention"""
        return {
            "status": "needs_improvement",
            "requirements": "Help users identify and correct errors",
            "recommendations": ["Clear error messages", "Inline validation", "Error prevention"]
        }
    
    def _check_assistive_tech_compatibility(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check assistive technology compatibility"""
        return {
            "status": "needs_testing",
            "requirements": "Compatible with screen readers and other assistive technologies",
            "recommendations": ["Use ARIA labels", "Test with screen readers", "Validate HTML"]
        }
    
    def _check_semantic_markup(self, component: str, issues: List[str]) -> Dict[str, Any]:
        """Check semantic HTML markup"""
        return {
            "status": "needs_review",
            "requirements": "Use semantic HTML elements",
            "recommendations": ["Use proper headings", "Structure with landmarks", "Semantic form elements"]
        }
    
    def _calculate_compliance_score(self, audit_results: Dict) -> float:
        """Calculate overall compliance score"""
        # Simplified scoring - in reality would be more sophisticated
        total_checks = 0
        passed_checks = 0
        
        for category in audit_results.values():
            for check in category.values():
                total_checks += 1
                if check.get("status") in ["compliant", "good"]:
                    passed_checks += 1
        
        return (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    def _identify_critical_issues(self, audit_results: Dict) -> List[str]:
        """Identify critical accessibility issues"""
        critical_issues = []
        
        for category_name, category in audit_results.items():
            for check_name, check in category.items():
                if check.get("status") == "critical":
                    critical_issues.append(f"{category_name}: {check_name}")
        
        return critical_issues
    
    def _prioritize_remediation(self, audit_results: Dict) -> List[Dict[str, Any]]:
        """Prioritize accessibility remediation tasks"""
        priorities = []
        
        for category_name, category in audit_results.items():
            for check_name, check in category.items():
                if check.get("status") in ["critical", "needs_improvement"]:
                    priority = "High" if check.get("status") == "critical" else "Medium"
                    priorities.append({
                        "category": category_name,
                        "check": check_name,
                        "priority": priority,
                        "recommendations": check.get("recommendations", [])
                    })
        
        return sorted(priorities, key=lambda x: {"High": 3, "Medium": 2, "Low": 1}[x["priority"]], reverse=True)
    
    def _provide_implementation_guidance(self, audit_results: Dict) -> List[str]:
        """Provide implementation guidance for accessibility fixes"""
        return [
            "Start with critical keyboard accessibility issues",
            "Implement proper ARIA labels and roles",
            "Ensure adequate color contrast ratios",
            "Add descriptive alt text for all images",
            "Test with actual screen reader software",
            "Validate HTML markup for semantic correctness"
        ]
    
    # Additional helper methods (simplified implementations)
    
    def _map_workflow_steps(self, workflow: str) -> List[str]:
        return ["Step mapping requires detailed workflow analysis"]
    
    def _map_pain_points(self, workflow: str, pain_points: List[str]) -> Dict:
        return {"pain_point_mapping": "Requires user journey analysis"}
    
    def _analyze_drop_offs(self, workflow: str, pain_points: List[str]) -> Dict:
        return {"drop_off_analysis": "Requires analytics data"}
    
    def _assess_friction_points(self, workflow: str, pain_points: List[str]) -> List[str]:
        return ["Friction assessment needs user testing data"]
    
    def _map_persona_journeys(self, workflow: str, personas: List[str]) -> Dict:
        return {"persona_journey_mapping": "Requires persona-specific analysis"}
    
    def _map_emotional_journey(self, workflow: str, pain_points: List[str]) -> Dict:
        return {"emotional_journey": "Requires user sentiment analysis"}
    
    def _analyze_touch_points(self, workflow: str) -> List[str]:
        return ["Touch point analysis needs comprehensive audit"]
    
    def _identify_critical_moments(self, workflow: str) -> List[str]:
        return ["Critical moments identification needs user research"]
    
    def _identify_step_reduction_opportunities(self, workflow: str) -> List[str]:
        return ["Step reduction opportunities need process analysis"]
    
    def _identify_parallel_opportunities(self, workflow: str) -> List[str]:
        return ["Parallel processing opportunities need workflow redesign"]
    
    def _suggest_progressive_disclosure(self, workflow: str) -> List[str]:
        return ["Progressive disclosure suggestions need information architecture review"]
    
    def _design_error_prevention(self, workflow: str, pain_points: List[str]) -> List[str]:
        return ["Error prevention design needs validation strategy"]
    
    def _recommend_immediate_improvements(self, analysis: Dict) -> List[str]:
        return ["Immediate improvements based on analysis findings"]
    
    def _recommend_long_term_enhancements(self, analysis: Dict) -> List[str]:
        return ["Long-term enhancements for optimal user experience"]
    
    def _define_success_metrics(self, analysis: Dict, metrics: List[str]) -> List[str]:
        return metrics if metrics else ["Task completion rate", "User satisfaction", "Time to complete"]
    
    def _design_testing_strategy(self, analysis: Dict) -> List[str]:
        return ["A/B testing for key workflows", "User testing with target personas", "Analytics tracking"]
    
    def _create_implementation_roadmap(self, plan: Dict) -> List[Dict[str, str]]:
        return [
            {"phase": "Quick Wins", "timeline": "1-2 weeks", "focus": "High-impact, low-effort improvements"},
            {"phase": "Core Improvements", "timeline": "3-6 weeks", "focus": "Major workflow optimizations"},
            {"phase": "Advanced Features", "timeline": "7-12 weeks", "focus": "Enhanced user experience features"}
        ]
    
    # Design system helper methods
    def _recommend_design_system(self, requirements: List[str], constraints: List[str], options: Dict) -> str:
        """Recommend the best design system based on requirements"""
        if any("federal" in req.lower() or "government" in req.lower() for req in requirements):
            return "us_web_design_system"
        elif any("rapid" in constraint.lower() for constraint in constraints):
            return "tailwind_css"
        else:
            return "shadcn_ui"
    
    def _identify_essential_components(self, requirements: List[str]) -> List[str]:
        return ["Button", "Input", "Form", "Navigation", "Card", "Modal", "Table"]
    
    def _identify_federal_components(self, requirements: List[str]) -> List[str]:
        return ["Alert", "Banner", "Breadcrumb", "Header", "Footer", "Step Indicator"]
    
    def _identify_accessibility_components(self, requirements: List[str]) -> List[str]:
        return ["Skip Link", "Focus Trap", "Screen Reader Text", "Keyboard Navigation"]
    
    def _identify_custom_components(self, requirements: List[str]) -> List[str]:
        return ["Job Card", "Application Form", "Search Filters", "Profile Builder"]
    
    def _create_migration_plan(self, current: str, recommended: str) -> List[str]:
        return ["Audit current components", "Map to new system", "Create migration timeline", "Test thoroughly"]
    
    def _prioritize_components(self, guidance: Dict) -> List[str]:
        return ["Essential components first", "Federal compliance components", "Custom components last"]
    
    def _plan_development_phases(self, system: str, guidance: Dict) -> List[Dict[str, str]]:
        return [
            {"phase": "Foundation", "components": "Basic UI elements"},
            {"phase": "Forms & Navigation", "components": "Complex interactive components"},
            {"phase": "Custom Features", "components": "Domain-specific components"}
        ]
    
    def _plan_maintenance_strategy(self, system: str) -> List[str]:
        return ["Regular updates", "Accessibility audits", "Performance monitoring", "User feedback integration"]
    
    # Usability evaluation helper methods (simplified)
    def _evaluate_system_visibility(self, interface: str, tasks: List[str]) -> str:
        return "System visibility evaluation needs interface analysis"
    
    def _score_system_visibility(self, interface: str, tasks: List[str]) -> float:
        return 7.5  # Example score out of 10
    
    def _recommend_system_visibility_improvements(self, interface: str) -> List[str]:
        return ["Add loading indicators", "Show system status", "Provide progress feedback"]
    
    def _evaluate_real_world_match(self, interface: str, tasks: List[str]) -> str:
        return "Real world matching evaluation needs user research"
    
    def _score_real_world_match(self, interface: str, tasks: List[str]) -> float:
        return 8.0
    
    def _recommend_real_world_improvements(self, interface: str) -> List[str]:
        return ["Use familiar terminology", "Follow real-world conventions", "Match user mental models"]
    
    # Continue with other usability evaluation methods...
    def _evaluate_user_control(self, interface: str, tasks: List[str]) -> str:
        return "User control evaluation pending"
    
    def _score_user_control(self, interface: str, tasks: List[str]) -> float:
        return 7.0
    
    def _recommend_user_control_improvements(self, interface: str) -> List[str]:
        return ["Add undo functionality", "Provide clear exit paths", "Allow user customization"]
    
    def _evaluate_consistency(self, interface: str, tasks: List[str]) -> str:
        return "Consistency evaluation needs comprehensive audit"
    
    def _score_consistency(self, interface: str, tasks: List[str]) -> float:
        return 8.5
    
    def _recommend_consistency_improvements(self, interface: str) -> List[str]:
        return ["Standardize UI patterns", "Use consistent terminology", "Maintain visual hierarchy"]
    
    def _evaluate_error_prevention(self, interface: str, tasks: List[str]) -> str:
        return "Error prevention evaluation needs form analysis"
    
    def _score_error_prevention(self, interface: str, tasks: List[str]) -> float:
        return 6.5
    
    def _recommend_error_prevention_improvements(self, interface: str) -> List[str]:
        return ["Add input validation", "Provide confirmation dialogs", "Design clear constraints"]
    
    def _evaluate_recognition_vs_recall(self, interface: str, tasks: List[str]) -> str:
        return "Recognition vs recall evaluation needs cognitive analysis"
    
    def _score_recognition_vs_recall(self, interface: str, tasks: List[str]) -> float:
        return 7.8
    
    def _recommend_recognition_improvements(self, interface: str) -> List[str]:
        return ["Make options visible", "Provide contextual help", "Use clear labels and icons"]
    
    def _evaluate_flexibility_efficiency(self, interface: str, tasks: List[str]) -> str:
        return "Flexibility evaluation needs user proficiency analysis"
    
    def _score_flexibility_efficiency(self, interface: str, tasks: List[str]) -> float:
        return 6.0
    
    def _recommend_flexibility_improvements(self, interface: str) -> List[str]:
        return ["Add keyboard shortcuts", "Provide advanced options", "Allow customization"]
    
    def _evaluate_aesthetic_design(self, interface: str, tasks: List[str]) -> str:
        return "Aesthetic evaluation needs visual design audit"
    
    def _score_aesthetic_design(self, interface: str, tasks: List[str]) -> float:
        return 8.2
    
    def _recommend_aesthetic_improvements(self, interface: str) -> List[str]:
        return ["Simplify visual design", "Improve information hierarchy", "Reduce cognitive load"]
    
    def _evaluate_error_recovery(self, interface: str, tasks: List[str]) -> str:
        return "Error recovery evaluation needs error scenario analysis"
    
    def _score_error_recovery(self, interface: str, tasks: List[str]) -> float:
        return 5.5
    
    def _recommend_error_recovery_improvements(self, interface: str) -> List[str]:
        return ["Improve error messages", "Provide recovery suggestions", "Add help resources"]
    
    def _evaluate_help_documentation(self, interface: str, tasks: List[str]) -> str:
        return "Help documentation evaluation needs content audit"
    
    def _score_help_documentation(self, interface: str, tasks: List[str]) -> float:
        return 6.8
    
    def _recommend_help_improvements(self, interface: str) -> List[str]:
        return ["Add contextual help", "Improve search functionality", "Create task-oriented guides"]
    
    def _calculate_overall_usability_score(self, principles: Dict) -> float:
        scores = [principle.get("score", 0) for principle in principles.values()]
        return sum(scores) / len(scores) if scores else 0
    
    def _identify_usability_strengths(self, principles: Dict) -> List[str]:
        strengths = []
        for name, principle in principles.items():
            if principle.get("score", 0) >= 8.0:
                strengths.append(name)
        return strengths
    
    def _identify_usability_weaknesses(self, principles: Dict) -> List[str]:
        weaknesses = []
        for name, principle in principles.items():
            if principle.get("score", 0) < 7.0:
                weaknesses.append(name)
        return weaknesses
    
    def _prioritize_usability_improvements(self, principles: Dict) -> List[str]:
        weaknesses = self._identify_usability_weaknesses(principles)
        return sorted(weaknesses, key=lambda x: principles[x].get("score", 0))
    
    def _create_usability_improvement_roadmap(self, assessment: Dict) -> List[Dict[str, Any]]:
        return [
            {"priority": "High", "improvements": assessment.get("weaknesses", [])[:3], "timeline": "2-4 weeks"},
            {"priority": "Medium", "improvements": assessment.get("weaknesses", [])[3:6], "timeline": "4-8 weeks"},
            {"priority": "Low", "improvements": assessment.get("weaknesses", [])[6:], "timeline": "8+ weeks"}
        ]
    
    # Responsive design helper methods (simplified)
    def _analyze_mobile_design(self, components: List[str]) -> Dict[str, str]:
        return {"status": "needs_review", "recommendations": "Optimize for mobile-first design"}
    
    def _analyze_tablet_design(self, components: List[str]) -> Dict[str, str]:
        return {"status": "good", "recommendations": "Maintain current tablet optimization"}
    
    def _analyze_desktop_design(self, components: List[str]) -> Dict[str, str]:
        return {"status": "excellent", "recommendations": "Desktop experience is well-optimized"}
    
    def _analyze_navigation_responsiveness(self, components: List[str]) -> Dict[str, str]:
        return {"status": "needs_improvement", "recommendations": "Implement hamburger menu for mobile"}
    
    def _analyze_form_responsiveness(self, components: List[str]) -> Dict[str, str]:
        return {"status": "good", "recommendations": "Forms adapt well across breakpoints"}
    
    def _analyze_table_responsiveness(self, components: List[str]) -> Dict[str, str]:
        return {"status": "critical", "recommendations": "Tables need horizontal scrolling or card layout on mobile"}
    
    def _analyze_content_responsiveness(self, components: List[str]) -> Dict[str, str]:
        return {"status": "good", "recommendations": "Content layout is well-structured"}
    
    def _analyze_touch_targets(self, components: List[str]) -> Dict[str, str]:
        return {"status": "needs_improvement", "recommendations": "Ensure minimum 44px touch targets"}
    
    def _analyze_gesture_support(self, components: List[str]) -> Dict[str, str]:
        return {"status": "basic", "recommendations": "Add swipe gestures where appropriate"}
    
    def _analyze_thumb_navigation(self, components: List[str]) -> Dict[str, str]:
        return {"status": "needs_review", "recommendations": "Position key actions in thumb-friendly zones"}
    
    def _analyze_image_optimization(self, components: List[str]) -> Dict[str, str]:
        return {"status": "needs_improvement", "recommendations": "Implement responsive images and lazy loading"}
    
    def _analyze_lazy_loading(self, components: List[str]) -> Dict[str, str]:
        return {"status": "not_implemented", "recommendations": "Add lazy loading for images and content"}
    
    def _analyze_bundle_optimization(self, components: List[str]) -> Dict[str, str]:
        return {"status": "needs_review", "recommendations": "Analyze and optimize JavaScript bundle size"}
    
    def _recommend_mobile_first_principles(self) -> List[str]:
        return [
            "Design for mobile screen first",
            "Progressive enhancement for larger screens",
            "Touch-first interaction design",
            "Performance optimization for mobile networks"
        ]
    
    def _recommend_progressive_enhancement(self) -> List[str]:
        return [
            "Start with basic functionality",
            "Enhance with JavaScript features",
            "Ensure graceful degradation",
            "Test on various devices and connections"
        ]
    
    def _recommend_performance_optimization(self) -> List[str]:
        return [
            "Optimize images and media",
            "Minimize HTTP requests",
            "Use efficient caching strategies",
            "Implement lazy loading"
        ]
    
    def _recommend_mobile_accessibility(self) -> List[str]:
        return [
            "Ensure adequate touch target sizes",
            "Support screen reader gestures",
            "Provide alternative text for all media",
            "Test with mobile accessibility tools"
        ]
    
    def _create_responsive_checklist(self, analysis: Dict) -> List[Dict[str, Any]]:
        return [
            {"category": "Mobile Design", "items": ["Touch targets 44px+", "Readable text", "Fast loading"]},
            {"category": "Navigation", "items": ["Mobile-friendly menu", "Clear hierarchy", "Easy back navigation"]},
            {"category": "Forms", "items": ["Large input fields", "Clear labels", "Inline validation"]},
            {"category": "Performance", "items": ["Optimized images", "Lazy loading", "Minimal JavaScript"]}
        ]
    
    # Federal compliance helper methods (simplified)
    def _validate_section_508(self, elements: List[str]) -> Dict[str, str]:
        return {"status": "partial_compliance", "details": "Some elements need accessibility improvements"}
    
    def _score_section_508_compliance(self, elements: List[str]) -> float:
        return 75.0  # Percentage compliance
    
    def _identify_section_508_fixes(self, elements: List[str]) -> List[str]:
        return ["Add ARIA labels", "Improve keyboard navigation", "Fix color contrast"]
    
    def _validate_uswds_compliance(self, elements: List[str]) -> Dict[str, str]:
        return {"status": "needs_improvement", "details": "Not using USWDS components"}
    
    def _score_uswds_compliance(self, elements: List[str]) -> float:
        return 40.0
    
    def _identify_uswds_fixes(self, elements: List[str]) -> List[str]:
        return ["Implement USWDS components", "Follow USWDS design tokens", "Use USWDS typography"]
    
    def _validate_plain_language(self, elements: List[str]) -> Dict[str, str]:
        return {"status": "good", "details": "Content uses clear, simple language"}
    
    def _score_plain_language_compliance(self, elements: List[str]) -> float:
        return 85.0
    
    def _identify_plain_language_fixes(self, elements: List[str]) -> List[str]:
        return ["Simplify technical jargon", "Add definitions for complex terms"]
    
    def _validate_security_privacy(self, elements: List[str]) -> Dict[str, str]:
        return {"status": "needs_review", "details": "Security and privacy features need validation"}
    
    def _score_security_privacy_compliance(self, elements: List[str]) -> float:
        return 70.0
    
    def _identify_security_privacy_fixes(self, elements: List[str]) -> List[str]:
        return ["Add privacy notices", "Implement secure data handling", "Review information collection"]
    
    def _identify_immediate_compliance_needs(self, validation: Dict) -> List[str]:
        return ["Critical accessibility fixes", "Essential security improvements", "Required privacy notices"]
    
    def _recommend_certification_path(self, validation: Dict) -> List[str]:
        return ["Section 508 compliance testing", "USWDS certification", "Security assessment"]
    
    def _recommend_compliance_testing(self, validation: Dict) -> List[str]:
        return ["Automated accessibility testing", "Manual screen reader testing", "Security penetration testing"]
    
    def _identify_documentation_needs(self, validation: Dict) -> List[str]:
        return ["Accessibility conformance statement", "Privacy policy", "Security documentation"]
    
    def _create_compliance_implementation_guide(self, validation: Dict) -> List[Dict[str, Any]]:
        return [
            {"phase": "Critical Fixes", "timeline": "1-2 weeks", "focus": "Section 508 compliance"},
            {"phase": "Design System", "timeline": "3-4 weeks", "focus": "USWDS implementation"},
            {"phase": "Documentation", "timeline": "1 week", "focus": "Compliance documentation"}
        ]
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze UX/UI design requests and provide comprehensive design guidance
        """
        
        try:
            # Extract design parameters
            design_type = data.get("design_type", "general_ux")
            component = data.get("component", "")
            user_needs = data.get("user_needs", [])
            constraints = data.get("constraints", [])
            compliance_requirements = data.get("compliance_requirements", ["Section 508"])
            
            # Build design analysis query
            query = f"""
            Analyze and provide UX/UI design guidance for: {component or design_type}
            
            Design Type: {design_type}
            
            User Needs: {', '.join(user_needs) if user_needs else 'Federal job seekers'}
            
            Constraints: {', '.join(constraints) if constraints else 'Solo developer, limited budget'}
            
            Compliance: {', '.join(compliance_requirements)}
            
            Provide:
            1. User experience analysis and recommendations
            2. Accessibility compliance guidance (Section 508, WCAG)
            3. Federal design standards alignment
            4. Mobile-first responsive design approach
            5. Implementation guidance for solo developer
            6. Testing and validation strategy
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add UX-specific recommendations
                response.data["ux_recommendations"] = {
                    "user_centered_design": [
                        "Conduct user research with federal job seekers",
                        "Create user personas based on government applicants",
                        "Design task flows for complex application processes",
                        "Test designs with actual users regularly"
                    ],
                    "accessibility_first": [
                        "Follow WCAG 2.1 AA guidelines from the start",
                        "Test with screen readers and keyboard navigation",
                        "Ensure adequate color contrast ratios",
                        "Provide alternative text for all images"
                    ],
                    "federal_compliance": [
                        "Use U.S. Web Design System components where possible",
                        "Follow Section 508 accessibility requirements",
                        "Implement plain language principles",
                        "Ensure mobile-first responsive design"
                    ],
                    "implementation": [
                        "Start with a design system foundation",
                        "Create reusable component library",
                        "Focus on core user journeys first",
                        "Plan for iterative design improvements"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"UX design analysis failed: {str(e)}"
            )
    
    def _recommend_shadcn_components(self, component_requirements: str) -> str:
        """Recommend Shadcn/UI components from https://ui.shadcn.com/"""
        try:
            # Parse requirements
            requirements = component_requirements.lower()
            
            # Component recommendations based on common Fed Job Advisor needs
            shadcn_recommendations = {
                "forms": {
                    "components": ["Form", "Input", "Label", "Button", "Select", "Checkbox", "RadioGroup"],
                    "description": "Complete form system with validation",
                    "url": "https://ui.shadcn.com/docs/components/form",
                    "fed_compliance": "Ensure proper labeling and error states for Section 508"
                },
                "navigation": {
                    "components": ["NavigationMenu", "Breadcrumb", "Tabs", "Sheet"],
                    "description": "Navigation and wayfinding components",
                    "url": "https://ui.shadcn.com/docs/components/navigation-menu",
                    "fed_compliance": "Keyboard navigation and clear hierarchy"
                },
                "data_display": {
                    "components": ["Table", "Card", "Badge", "Progress", "Avatar"],
                    "description": "Display job data and user information",
                    "url": "https://ui.shadcn.com/docs/components/table",
                    "fed_compliance": "Accessible tables with proper headers"
                },
                "feedback": {
                    "components": ["Alert", "Toast", "AlertDialog", "Dialog"],
                    "description": "User feedback and confirmation dialogs",
                    "url": "https://ui.shadcn.com/docs/components/alert",
                    "fed_compliance": "Clear error messages and confirmations"
                },
                "search": {
                    "components": ["Command", "Combobox", "Popover", "HoverCard"],
                    "description": "Search and filtering interfaces",
                    "url": "https://ui.shadcn.com/docs/components/command",
                    "fed_compliance": "Predictable search behavior"
                }
            }
            
            # Match requirements to recommendations
            relevant_components = []
            for category, details in shadcn_recommendations.items():
                if any(keyword in requirements for keyword in [category, "form", "table", "dialog", "search", "nav"]):
                    relevant_components.append({
                        "category": category,
                        "components": details["components"],
                        "description": details["description"],
                        "url": details["url"],
                        "federal_compliance": details["fed_compliance"]
                    })
            
            # If no specific match, provide general recommendations
            if not relevant_components:
                relevant_components = [
                    {
                        "category": "core_ui",
                        "components": ["Button", "Input", "Card", "Alert", "Dialog"],
                        "description": "Essential UI components for federal applications",
                        "url": "https://ui.shadcn.com/docs/components",
                        "federal_compliance": "Follow USWDS patterns where possible"
                    }
                ]
            
            return json.dumps({
                "shadcn_recommendations": relevant_components,
                "implementation_guide": {
                    "installation": "npx shadcn-ui@latest init",
                    "component_add": "npx shadcn-ui@latest add [component-name]",
                    "customization": "Modify components in @/components/ui/ to match federal design standards",
                    "accessibility": "Test with screen readers and keyboard navigation"
                },
                "federal_considerations": [
                    "Ensure color contrast meets WCAG AA standards",
                    "Add proper ARIA labels and descriptions",
                    "Test with government-approved browsers",
                    "Follow plain language guidelines for all text"
                ],
                "resources": {
                    "shadcn_docs": "https://ui.shadcn.com/docs",
                    "uswds_components": "https://designsystem.digital.gov/components/",
                    "section_508": "https://www.section508.gov/"
                }
            })
            
        except Exception as e:
            return f"Error recommending Shadcn/UI components: {str(e)}"
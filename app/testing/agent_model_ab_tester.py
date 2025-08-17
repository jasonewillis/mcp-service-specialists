"""
Agent Model A/B Testing Framework
Systematically test different LLM models for each agent role
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestCategory(Enum):
    """Categories of tests for agents"""
    ACCURACY = "accuracy"
    SPEED = "speed"
    CREATIVITY = "creativity"
    REASONING = "reasoning"
    CODE_QUALITY = "code_quality"
    COMPLIANCE = "compliance"
    COMMUNICATION = "communication"

@dataclass
class TestResult:
    """Individual test result"""
    test_id: str
    agent_role: str
    model: str
    test_category: TestCategory
    test_name: str
    input_prompt: str
    expected_output: Optional[str]
    actual_output: str
    execution_time: float
    tokens_used: int
    score: float
    passed: bool
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ModelPerformance:
    """Aggregate performance metrics for a model"""
    model: str
    agent_role: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    average_score: float
    average_time: float
    average_tokens: float
    success_rate: float
    test_categories: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]

class AgentTestSuite:
    """Test suite for specific agent roles"""
    
    def __init__(self, agent_role: str):
        self.agent_role = agent_role
        self.tests = self._load_tests_for_role()
    
    def _load_tests_for_role(self) -> List[Dict[str, Any]]:
        """Load role-specific tests"""
        test_definitions = {
            "backend_engineer": [
                {
                    "id": "be_001",
                    "name": "API Endpoint Creation",
                    "category": TestCategory.CODE_QUALITY,
                    "prompt": "Create a FastAPI endpoint for user registration with email validation",
                    "expected_patterns": ["@app.post", "async def", "email", "validation", "pydantic"],
                    "scoring": {"keywords": 0.4, "structure": 0.3, "completeness": 0.3}
                },
                {
                    "id": "be_002",
                    "name": "Database Query Optimization",
                    "category": TestCategory.REASONING,
                    "prompt": "Optimize this SQL query: SELECT * FROM users WHERE status='active' AND created_at > '2024-01-01'",
                    "expected_patterns": ["INDEX", "SELECT specific columns", "EXPLAIN"],
                    "scoring": {"optimization": 0.5, "explanation": 0.3, "alternatives": 0.2}
                },
                {
                    "id": "be_003",
                    "name": "Error Handling",
                    "category": TestCategory.CODE_QUALITY,
                    "prompt": "Add comprehensive error handling to a file upload function",
                    "expected_patterns": ["try", "except", "logging", "specific exceptions", "cleanup"],
                    "scoring": {"coverage": 0.4, "specificity": 0.3, "recovery": 0.3}
                },
                {
                    "id": "be_004",
                    "name": "Unit Test Writing",
                    "category": TestCategory.CODE_QUALITY,
                    "prompt": "Write unit tests for a user authentication service",
                    "expected_patterns": ["pytest", "mock", "assert", "edge cases", "fixtures"],
                    "scoring": {"coverage": 0.4, "assertions": 0.3, "mocking": 0.3}
                },
                {
                    "id": "be_005",
                    "name": "Microservice Design",
                    "category": TestCategory.REASONING,
                    "prompt": "Design a microservice architecture for an e-commerce platform",
                    "expected_patterns": ["services", "API gateway", "database per service", "communication"],
                    "scoring": {"architecture": 0.5, "scalability": 0.3, "patterns": 0.2}
                }
            ],
            
            "frontend_developer": [
                {
                    "id": "fe_001",
                    "name": "React Component Creation",
                    "category": TestCategory.CODE_QUALITY,
                    "prompt": "Create a React component for a searchable dropdown with TypeScript",
                    "expected_patterns": ["useState", "useEffect", "interface", "onChange", "filter"],
                    "scoring": {"functionality": 0.4, "typescript": 0.3, "hooks": 0.3}
                },
                {
                    "id": "fe_002",
                    "name": "Responsive Design",
                    "category": TestCategory.CREATIVITY,
                    "prompt": "Create CSS for a responsive navigation menu using Tailwind",
                    "expected_patterns": ["flex", "md:", "lg:", "hover:", "mobile-first"],
                    "scoring": {"responsiveness": 0.5, "tailwind": 0.3, "accessibility": 0.2}
                },
                {
                    "id": "fe_003",
                    "name": "State Management",
                    "category": TestCategory.REASONING,
                    "prompt": "Implement global state management for a shopping cart",
                    "expected_patterns": ["context", "reducer", "actions", "localStorage", "persist"],
                    "scoring": {"pattern": 0.4, "persistence": 0.3, "optimization": 0.3}
                },
                {
                    "id": "fe_004",
                    "name": "Performance Optimization",
                    "category": TestCategory.CODE_QUALITY,
                    "prompt": "Optimize a React component that renders 10,000 items",
                    "expected_patterns": ["memo", "virtualization", "useMemo", "useCallback", "lazy"],
                    "scoring": {"techniques": 0.5, "explanation": 0.3, "trade-offs": 0.2}
                },
                {
                    "id": "fe_005",
                    "name": "Accessibility Implementation",
                    "category": TestCategory.COMPLIANCE,
                    "prompt": "Make a form component WCAG 2.1 AA compliant",
                    "expected_patterns": ["aria-", "role", "label", "keyboard", "screen reader"],
                    "scoring": {"aria": 0.4, "semantics": 0.3, "keyboard": 0.3}
                }
            ],
            
            "data_scientist": [
                {
                    "id": "ds_001",
                    "name": "Data Analysis",
                    "category": TestCategory.REASONING,
                    "prompt": "Analyze a dataset of user behavior and identify key patterns",
                    "expected_patterns": ["pandas", "correlation", "visualization", "statistics", "insights"],
                    "scoring": {"analysis": 0.4, "visualization": 0.3, "insights": 0.3}
                },
                {
                    "id": "ds_002",
                    "name": "ML Model Selection",
                    "category": TestCategory.REASONING,
                    "prompt": "Choose and justify an ML model for customer churn prediction",
                    "expected_patterns": ["classification", "features", "validation", "metrics", "ensemble"],
                    "scoring": {"justification": 0.5, "alternatives": 0.3, "metrics": 0.2}
                },
                {
                    "id": "ds_003",
                    "name": "Feature Engineering",
                    "category": TestCategory.CREATIVITY,
                    "prompt": "Create features from raw e-commerce transaction data",
                    "expected_patterns": ["aggregation", "time-based", "categorical", "scaling", "selection"],
                    "scoring": {"creativity": 0.4, "relevance": 0.3, "implementation": 0.3}
                },
                {
                    "id": "ds_004",
                    "name": "Statistical Testing",
                    "category": TestCategory.ACCURACY,
                    "prompt": "Perform A/B test analysis with statistical significance",
                    "expected_patterns": ["hypothesis", "p-value", "confidence", "sample size", "power"],
                    "scoring": {"methodology": 0.5, "interpretation": 0.3, "recommendations": 0.2}
                },
                {
                    "id": "ds_005",
                    "name": "Dashboard Design",
                    "category": TestCategory.COMMUNICATION,
                    "prompt": "Design KPI dashboard for executive leadership",
                    "expected_patterns": ["metrics", "visualization", "real-time", "drill-down", "alerts"],
                    "scoring": {"clarity": 0.4, "relevance": 0.3, "actionability": 0.3}
                }
            ],
            
            "devops_engineer": [
                {
                    "id": "do_001",
                    "name": "CI/CD Pipeline",
                    "category": TestCategory.CODE_QUALITY,
                    "prompt": "Create a GitHub Actions workflow for Python application deployment",
                    "expected_patterns": ["workflow", "jobs", "steps", "secrets", "deployment"],
                    "scoring": {"completeness": 0.4, "security": 0.3, "efficiency": 0.3}
                },
                {
                    "id": "do_002",
                    "name": "Docker Configuration",
                    "category": TestCategory.CODE_QUALITY,
                    "prompt": "Create multi-stage Dockerfile for Node.js application",
                    "expected_patterns": ["FROM", "multi-stage", "COPY", "optimization", "security"],
                    "scoring": {"optimization": 0.4, "security": 0.3, "best practices": 0.3}
                },
                {
                    "id": "do_003",
                    "name": "Infrastructure as Code",
                    "category": TestCategory.REASONING,
                    "prompt": "Design Terraform configuration for AWS web application",
                    "expected_patterns": ["resource", "variables", "modules", "state", "security group"],
                    "scoring": {"architecture": 0.5, "modularity": 0.3, "security": 0.2}
                },
                {
                    "id": "do_004",
                    "name": "Monitoring Setup",
                    "category": TestCategory.REASONING,
                    "prompt": "Implement comprehensive monitoring for microservices",
                    "expected_patterns": ["metrics", "logs", "traces", "alerts", "dashboards"],
                    "scoring": {"coverage": 0.4, "alerting": 0.3, "visualization": 0.3}
                },
                {
                    "id": "do_005",
                    "name": "Incident Response",
                    "category": TestCategory.COMMUNICATION,
                    "prompt": "Create incident response runbook for database outage",
                    "expected_patterns": ["detection", "escalation", "mitigation", "recovery", "post-mortem"],
                    "scoring": {"clarity": 0.4, "completeness": 0.3, "actionability": 0.3}
                }
            ],
            
            "security_analyst": [
                {
                    "id": "sa_001",
                    "name": "Security Audit",
                    "category": TestCategory.COMPLIANCE,
                    "prompt": "Perform security audit on REST API implementation",
                    "expected_patterns": ["OWASP", "authentication", "authorization", "injection", "encryption"],
                    "scoring": {"coverage": 0.5, "severity": 0.3, "recommendations": 0.2}
                },
                {
                    "id": "sa_002",
                    "name": "Vulnerability Assessment",
                    "category": TestCategory.ACCURACY,
                    "prompt": "Identify vulnerabilities in this code snippet: [SQL query with user input]",
                    "expected_patterns": ["SQL injection", "parameterized", "sanitization", "validation"],
                    "scoring": {"identification": 0.5, "explanation": 0.3, "fix": 0.2}
                },
                {
                    "id": "sa_003",
                    "name": "Security Policy",
                    "category": TestCategory.COMMUNICATION,
                    "prompt": "Create password policy for federal application",
                    "expected_patterns": ["complexity", "length", "rotation", "history", "NIST"],
                    "scoring": {"compliance": 0.5, "completeness": 0.3, "clarity": 0.2}
                },
                {
                    "id": "sa_004",
                    "name": "Threat Modeling",
                    "category": TestCategory.REASONING,
                    "prompt": "Create threat model for e-commerce platform",
                    "expected_patterns": ["STRIDE", "attack vectors", "mitigations", "risk assessment"],
                    "scoring": {"methodology": 0.4, "comprehensiveness": 0.3, "prioritization": 0.3}
                },
                {
                    "id": "sa_005",
                    "name": "Incident Analysis",
                    "category": TestCategory.REASONING,
                    "prompt": "Analyze logs for potential security breach indicators",
                    "expected_patterns": ["anomalies", "patterns", "timeline", "IOCs", "recommendations"],
                    "scoring": {"detection": 0.4, "analysis": 0.3, "recommendations": 0.3}
                }
            ],
            
            "project_manager": [
                {
                    "id": "pm_001",
                    "name": "Task Breakdown",
                    "category": TestCategory.REASONING,
                    "prompt": "Break down 'implement user authentication' into subtasks with estimates",
                    "expected_patterns": ["subtasks", "dependencies", "estimates", "priorities", "milestones"],
                    "scoring": {"decomposition": 0.4, "estimates": 0.3, "dependencies": 0.3}
                },
                {
                    "id": "pm_002",
                    "name": "Risk Assessment",
                    "category": TestCategory.REASONING,
                    "prompt": "Identify and mitigate risks for cloud migration project",
                    "expected_patterns": ["risks", "probability", "impact", "mitigation", "contingency"],
                    "scoring": {"identification": 0.4, "assessment": 0.3, "mitigation": 0.3}
                },
                {
                    "id": "pm_003",
                    "name": "Sprint Planning",
                    "category": TestCategory.COMMUNICATION,
                    "prompt": "Plan 2-week sprint for 5-person development team",
                    "expected_patterns": ["velocity", "capacity", "stories", "goals", "ceremonies"],
                    "scoring": {"realistic": 0.4, "clarity": 0.3, "balance": 0.3}
                },
                {
                    "id": "pm_004",
                    "name": "Stakeholder Communication",
                    "category": TestCategory.COMMUNICATION,
                    "prompt": "Write project status update for executive stakeholders",
                    "expected_patterns": ["progress", "risks", "decisions", "metrics", "next steps"],
                    "scoring": {"clarity": 0.4, "completeness": 0.3, "actionability": 0.3}
                },
                {
                    "id": "pm_005",
                    "name": "Resource Planning",
                    "category": TestCategory.REASONING,
                    "prompt": "Allocate team resources for parallel feature development",
                    "expected_patterns": ["skills", "availability", "dependencies", "optimization", "timeline"],
                    "scoring": {"efficiency": 0.4, "feasibility": 0.3, "flexibility": 0.3}
                }
            ],
            
            "compliance_officer": [
                {
                    "id": "co_001",
                    "name": "Federal Compliance Check",
                    "category": TestCategory.COMPLIANCE,
                    "prompt": "Review application for Section 508 accessibility compliance",
                    "expected_patterns": ["WCAG", "screen readers", "keyboard", "color contrast", "alt text"],
                    "scoring": {"accuracy": 0.5, "completeness": 0.3, "recommendations": 0.2}
                },
                {
                    "id": "co_002",
                    "name": "Data Privacy Assessment",
                    "category": TestCategory.COMPLIANCE,
                    "prompt": "Assess GDPR compliance for user data handling",
                    "expected_patterns": ["consent", "rights", "processing", "retention", "breach"],
                    "scoring": {"coverage": 0.5, "accuracy": 0.3, "actionability": 0.2}
                },
                {
                    "id": "co_003",
                    "name": "Audit Report",
                    "category": TestCategory.COMMUNICATION,
                    "prompt": "Create compliance audit report for federal agency",
                    "expected_patterns": ["findings", "severity", "evidence", "recommendations", "timeline"],
                    "scoring": {"structure": 0.4, "clarity": 0.3, "actionability": 0.3}
                },
                {
                    "id": "co_004",
                    "name": "Policy Creation",
                    "category": TestCategory.COMMUNICATION,
                    "prompt": "Draft data retention policy for healthcare application",
                    "expected_patterns": ["HIPAA", "retention periods", "disposal", "access controls", "audit"],
                    "scoring": {"compliance": 0.5, "completeness": 0.3, "clarity": 0.2}
                },
                {
                    "id": "co_005",
                    "name": "Risk Mitigation",
                    "category": TestCategory.REASONING,
                    "prompt": "Develop compliance risk mitigation strategy",
                    "expected_patterns": ["controls", "monitoring", "training", "documentation", "review"],
                    "scoring": {"comprehensiveness": 0.4, "practicality": 0.3, "effectiveness": 0.3}
                }
            ]
        }
        
        return test_definitions.get(self.agent_role, [])
    
    def score_response(self, test: Dict[str, Any], response: str) -> Tuple[float, bool]:
        """Score a response based on test criteria"""
        score = 0.0
        expected_patterns = test.get("expected_patterns", [])
        scoring_weights = test.get("scoring", {})
        
        # Check for expected patterns
        patterns_found = sum(1 for pattern in expected_patterns if pattern.lower() in response.lower())
        pattern_score = patterns_found / len(expected_patterns) if expected_patterns else 0
        
        # Apply weighted scoring if available
        if scoring_weights:
            # This is simplified - in production would have more sophisticated scoring
            score = pattern_score
        else:
            score = pattern_score
        
        # Determine pass/fail (threshold of 0.7)
        passed = score >= 0.7
        
        return score, passed

class AgentModelABTester:
    """Main A/B testing framework for agent models"""
    
    def __init__(self, results_dir: str = "test_results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        self.test_suites = {}
        self.results = []
        self._initialize_test_suites()
    
    def _initialize_test_suites(self):
        """Initialize test suites for all agent roles"""
        agent_roles = [
            "backend_engineer",
            "frontend_developer",
            "data_scientist",
            "devops_engineer",
            "security_analyst",
            "project_manager",
            "compliance_officer"
        ]
        
        for role in agent_roles:
            self.test_suites[role] = AgentTestSuite(role)
            logger.info(f"Initialized test suite for {role}")
    
    async def test_model_on_role(
        self,
        model_name: str,
        agent_role: str,
        agent_executor,
        test_subset: Optional[List[str]] = None
    ) -> List[TestResult]:
        """Test a specific model on an agent role"""
        
        if agent_role not in self.test_suites:
            logger.error(f"No test suite for role: {agent_role}")
            return []
        
        suite = self.test_suites[agent_role]
        results = []
        
        # Filter tests if subset specified
        tests = suite.tests
        if test_subset:
            tests = [t for t in tests if t["id"] in test_subset]
        
        for test in tests:
            logger.info(f"Running test {test['id']}: {test['name']}")
            
            start_time = time.time()
            try:
                # Execute test
                response = await agent_executor.ainvoke({"input": test["prompt"]})
                actual_output = response.get("output", "")
                
                execution_time = time.time() - start_time
                
                # Score the response
                score, passed = suite.score_response(test, actual_output)
                
                # Estimate tokens (simplified)
                tokens_used = len(test["prompt"].split()) + len(actual_output.split())
                
                result = TestResult(
                    test_id=test["id"],
                    agent_role=agent_role,
                    model=model_name,
                    test_category=test["category"],
                    test_name=test["name"],
                    input_prompt=test["prompt"],
                    expected_output=str(test.get("expected_patterns", [])),
                    actual_output=actual_output[:500],  # Truncate for storage
                    execution_time=execution_time,
                    tokens_used=tokens_used,
                    score=score,
                    passed=passed,
                    metadata={"scoring": test.get("scoring", {})}
                )
                
            except Exception as e:
                logger.error(f"Error in test {test['id']}: {e}")
                result = TestResult(
                    test_id=test["id"],
                    agent_role=agent_role,
                    model=model_name,
                    test_category=test["category"],
                    test_name=test["name"],
                    input_prompt=test["prompt"],
                    expected_output=str(test.get("expected_patterns", [])),
                    actual_output="",
                    execution_time=time.time() - start_time,
                    tokens_used=0,
                    score=0.0,
                    passed=False,
                    error=str(e)
                )
            
            results.append(result)
            self.results.append(result)
            
            # Small delay between tests
            await asyncio.sleep(1)
        
        return results
    
    async def compare_models(
        self,
        models: List[str],
        agent_role: str,
        agent_factory,
        test_subset: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Compare multiple models for a specific agent role"""
        
        comparison_results = {
            "agent_role": agent_role,
            "models_tested": models,
            "test_time": datetime.now().isoformat(),
            "model_results": {},
            "winner": None,
            "analysis": {}
        }
        
        all_scores = {}
        
        for model in models:
            logger.info(f"Testing model {model} for role {agent_role}")
            
            # Create agent with specific model
            agent = agent_factory.create_agent_with_model(agent_role, model)
            
            # Run tests
            results = await self.test_model_on_role(
                model,
                agent_role,
                agent,
                test_subset
            )
            
            # Calculate performance metrics
            performance = self._calculate_performance(results)
            comparison_results["model_results"][model] = performance
            all_scores[model] = performance.average_score
        
        # Determine winner
        if all_scores:
            winner = max(all_scores, key=all_scores.get)
            comparison_results["winner"] = winner
            comparison_results["analysis"] = self._analyze_comparison(comparison_results["model_results"])
        
        # Save results
        self._save_comparison_results(comparison_results)
        
        return comparison_results
    
    def _calculate_performance(self, results: List[TestResult]) -> ModelPerformance:
        """Calculate aggregate performance metrics"""
        if not results:
            return ModelPerformance(
                model="unknown",
                agent_role="unknown",
                total_tests=0,
                passed_tests=0,
                failed_tests=0,
                average_score=0.0,
                average_time=0.0,
                average_tokens=0.0,
                success_rate=0.0,
                test_categories={},
                strengths=[],
                weaknesses=[]
            )
        
        model = results[0].model
        agent_role = results[0].agent_role
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.passed)
        failed_tests = total_tests - passed_tests
        
        average_score = np.mean([r.score for r in results])
        average_time = np.mean([r.execution_time for r in results])
        average_tokens = np.mean([r.tokens_used for r in results])
        success_rate = passed_tests / total_tests if total_tests > 0 else 0
        
        # Category breakdown
        categories = {}
        for category in TestCategory:
            category_results = [r for r in results if r.test_category == category]
            if category_results:
                categories[category.value] = np.mean([r.score for r in category_results])
        
        # Identify strengths and weaknesses
        strengths = [cat for cat, score in categories.items() if score >= 0.8]
        weaknesses = [cat for cat, score in categories.items() if score < 0.6]
        
        return ModelPerformance(
            model=model,
            agent_role=agent_role,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            average_score=average_score,
            average_time=average_time,
            average_tokens=average_tokens,
            success_rate=success_rate,
            test_categories=categories,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _analyze_comparison(self, model_results: Dict[str, ModelPerformance]) -> Dict[str, Any]:
        """Analyze comparison results"""
        analysis = {
            "best_overall": None,
            "fastest": None,
            "most_accurate": None,
            "most_efficient": None,
            "recommendations": []
        }
        
        if not model_results:
            return analysis
        
        # Find best performers
        scores = {m: p.average_score for m, p in model_results.items()}
        times = {m: p.average_time for m, p in model_results.items()}
        tokens = {m: p.average_tokens for m, p in model_results.items()}
        
        analysis["best_overall"] = max(scores, key=scores.get)
        analysis["fastest"] = min(times, key=times.get)
        analysis["most_accurate"] = max(scores, key=scores.get)
        analysis["most_efficient"] = min(tokens, key=tokens.get)
        
        # Generate recommendations
        for model, perf in model_results.items():
            if perf.success_rate >= 0.8:
                analysis["recommendations"].append(
                    f"{model} is production-ready with {perf.success_rate:.1%} success rate"
                )
            elif perf.success_rate >= 0.6:
                analysis["recommendations"].append(
                    f"{model} needs improvement in: {', '.join(perf.weaknesses)}"
                )
            else:
                analysis["recommendations"].append(
                    f"{model} is not recommended (only {perf.success_rate:.1%} success rate)"
                )
        
        return analysis
    
    def _save_comparison_results(self, results: Dict[str, Any]):
        """Save comparison results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.results_dir / f"comparison_{results['agent_role']}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Saved comparison results to {filename}")
    
    def generate_report(self) -> str:
        """Generate comprehensive testing report"""
        if not self.results:
            return "No test results available"
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([asdict(r) for r in self.results])
        
        report = []
        report.append("=" * 80)
        report.append("AGENT MODEL A/B TESTING REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append(f"Total Tests Run: {len(self.results)}")
        report.append("")
        
        # Overall summary
        report.append("OVERALL SUMMARY")
        report.append("-" * 40)
        overall_pass_rate = df['passed'].mean()
        report.append(f"Overall Pass Rate: {overall_pass_rate:.1%}")
        report.append(f"Average Score: {df['score'].mean():.2f}")
        report.append(f"Average Execution Time: {df['execution_time'].mean():.2f}s")
        report.append("")
        
        # By Model
        report.append("PERFORMANCE BY MODEL")
        report.append("-" * 40)
        for model in df['model'].unique():
            model_df = df[df['model'] == model]
            report.append(f"\n{model}:")
            report.append(f"  Tests: {len(model_df)}")
            report.append(f"  Pass Rate: {model_df['passed'].mean():.1%}")
            report.append(f"  Avg Score: {model_df['score'].mean():.2f}")
            report.append(f"  Avg Time: {model_df['execution_time'].mean():.2f}s")
        
        # By Agent Role
        report.append("\n\nPERFORMANCE BY AGENT ROLE")
        report.append("-" * 40)
        for role in df['agent_role'].unique():
            role_df = df[df['agent_role'] == role]
            report.append(f"\n{role}:")
            report.append(f"  Tests: {len(role_df)}")
            report.append(f"  Pass Rate: {role_df['passed'].mean():.1%}")
            report.append(f"  Best Model: {role_df.groupby('model')['score'].mean().idxmax()}")
        
        # By Test Category
        report.append("\n\nPERFORMANCE BY TEST CATEGORY")
        report.append("-" * 40)
        for category in TestCategory:
            cat_df = df[df['test_category'] == category.value]
            if not cat_df.empty:
                report.append(f"\n{category.value}:")
                report.append(f"  Pass Rate: {cat_df['passed'].mean():.1%}")
                report.append(f"  Avg Score: {cat_df['score'].mean():.2f}")
        
        # Failed Tests
        failed_df = df[df['passed'] == False]
        if not failed_df.empty:
            report.append("\n\nFAILED TESTS")
            report.append("-" * 40)
            for _, row in failed_df.iterrows():
                report.append(f"- {row['test_name']} ({row['agent_role']}/{row['model']})")
                if row['error']:
                    report.append(f"  Error: {row['error'][:100]}")
        
        return "\n".join(report)
    
    def export_to_csv(self, filename: Optional[str] = None):
        """Export results to CSV for further analysis"""
        if not self.results:
            logger.warning("No results to export")
            return
        
        df = pd.DataFrame([asdict(r) for r in self.results])
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.results_dir / f"test_results_{timestamp}.csv"
        
        df.to_csv(filename, index=False)
        logger.info(f"Exported results to {filename}")
        
        return filename


# Example usage
async def main():
    """Example of running A/B tests"""
    
    # Initialize tester
    tester = AgentModelABTester()
    
    # Example: Compare models for backend engineer role
    models_to_test = ["codellama:7b", "llama3.1:70b", "mistral:7b"]
    
    # This would integrate with your agent factory
    # results = await tester.compare_models(
    #     models=models_to_test,
    #     agent_role="backend_engineer",
    #     agent_factory=your_factory
    # )
    
    # Generate report
    report = tester.generate_report()
    print(report)
    
    # Export for analysis
    tester.export_to_csv()

if __name__ == "__main__":
    asyncio.run(main())
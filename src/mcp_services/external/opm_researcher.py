#!/usr/bin/env python3
"""
OPM Salary Data Researcher
Uses mistral:7b for analysis tasks (good balance of speed/quality)
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple
import asyncio

class OPMResearcher:
    """
    Research-only agent for OPM salary data and locality pay calculations
    Expert in federal compensation structures
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "opm"
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Load OPM data
        self.gs_base = self.load_gs_base_pay()
        self.locality_areas = self.load_locality_data()
        self.critical_rules = self.load_critical_rules()
        
        self.model = "mistral:7b"  # Good for analysis tasks
    
    def load_gs_base_pay(self) -> Dict:
        """Load GS base pay tables"""
        path = self.docs_path / "gs_base_pay_2025.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {}
    
    def load_locality_data(self) -> Dict:
        """Load locality pay adjustments"""
        path = self.docs_path / "locality_pay_2025.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {}
    
    def load_critical_rules(self) -> List[str]:
        """Critical OPM salary calculation rules"""
        return [
            "Always use current year salary tables (2025)",
            "Apply locality pay adjustment to base salary",
            "53 official locality areas + Rest of US",
            "10 steps within each grade (1-10)",
            "15 GS grades total (GS-1 through GS-15)",
            "Within-grade increases: 1-3 yearly, 4-6 biennial, 7-9 triennial",
            "Special rates may apply for IT (2210) and medical positions",
            "Formula: Total = Base × (1 + Locality%/100)"
        ]
    
    def calculate_salary(self, grade: int, step: int, locality: str) -> float:
        """Calculate federal salary with locality pay"""
        try:
            # Get base pay
            base_pay = self.gs_base['base_rates'][f'GS-{grade}'][step - 1]
            
            # Get locality adjustment
            locality_data = self.locality_areas.get(locality, 
                                                   self.locality_areas.get('rest-of-us'))
            adjustment = locality_data.get('adjustment', 16.50)
            
            # Calculate total
            total = base_pay * (1 + adjustment / 100)
            return round(total, 2)
        except:
            return 0
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """
        Phase 1: Research OPM salary calculations
        """
        
        task_analysis = self._analyze_task(task)
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "task_type": task_analysis['type'],
            "critical_requirements": self.critical_rules,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "salary_examples": self._generate_salary_examples(task_analysis),
            "code_templates": self._generate_code_templates(task_analysis),
            "data_requirements": self._identify_data_requirements(task_analysis)
        }
        
        # Save research report
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "critical_reminders": research["critical_requirements"][:3]
        }
    
    def _analyze_task(self, task: str) -> Dict[str, Any]:
        """Analyze OPM-related task"""
        task_lower = task.lower()
        
        analysis = {
            "type": "unknown",
            "operations": [],
            "data_needed": []
        }
        
        if "salary" in task_lower or "pay" in task_lower:
            analysis["type"] = "salary_calculation"
            analysis["operations"].append("calculate_salary")
            analysis["data_needed"].extend(["gs_base", "locality_pay"])
        
        if "locality" in task_lower or "col" in task_lower:
            analysis["type"] = "locality_analysis"
            analysis["operations"].append("compare_localities")
            analysis["data_needed"].append("locality_adjustments")
        
        if "promotion" in task_lower or "grade" in task_lower:
            analysis["type"] = "grade_progression"
            analysis["operations"].append("analyze_progression")
            analysis["data_needed"].append("grade_ranges")
        
        return analysis
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict[str, Any]:
        """Create OPM implementation plan"""
        
        plan = {
            "summary": f"OPM {task_analysis['type']} implementation",
            "steps": [],
            "functions": [],
            "ui_components": []
        }
        
        if task_analysis["type"] == "salary_calculation":
            plan["steps"] = [
                "1. Load 2025 GS base pay tables",
                "2. Load locality pay adjustments",
                "3. Create salary calculation function",
                "4. Handle grade/step validation",
                "5. Format salary for display",
                "6. Cache calculations for performance"
            ]
            plan["functions"] = [
                "calculate_federal_salary(grade, step, locality)",
                "get_salary_range(grade, locality)",
                "get_promotion_increase(current_grade, next_grade, locality)",
                "format_salary(amount)"
            ]
            plan["ui_components"] = [
                "Salary calculator widget",
                "Grade/step selector",
                "Locality dropdown (53 areas)",
                "Salary comparison chart"
            ]
        
        elif task_analysis["type"] == "locality_analysis":
            plan["steps"] = [
                "1. Load all 53 locality areas",
                "2. Calculate salary differences",
                "3. Factor in cost of living",
                "4. Create comparison visualizations",
                "5. Generate relocation recommendations"
            ]
            plan["functions"] = [
                "compare_localities(grade, step, localities[])",
                "calculate_col_adjusted_salary(salary, locality)",
                "rank_localities_by_value(grade, step)"
            ]
        
        return plan
    
    def _generate_salary_examples(self, task_analysis: Dict) -> List[Dict]:
        """Generate example salary calculations"""
        examples = []
        
        # Common federal grades
        test_cases = [
            (7, 1, "rest-of-us", "Entry-level"),
            (11, 1, "washington-dc", "Journey-level DC"),
            (13, 5, "san-francisco", "Senior SF"),
            (14, 10, "new-york", "Supervisory NYC")
        ]
        
        for grade, step, locality, description in test_cases:
            salary = self.calculate_salary(grade, step, locality)
            locality_data = self.locality_areas.get(locality, {})
            
            examples.append({
                "description": description,
                "grade": f"GS-{grade}",
                "step": step,
                "locality": locality_data.get('name', locality),
                "adjustment": locality_data.get('adjustment', 16.50),
                "total_salary": f"${salary:,.2f}"
            })
        
        return examples
    
    def _generate_code_templates(self, task_analysis: Dict) -> Dict[str, str]:
        """Generate code templates for OPM calculations"""
        templates = {}
        
        templates["salary_calculator"] = """
class FederalSalaryCalculator:
    def __init__(self):
        self.gs_base = self.load_gs_base_pay()
        self.locality_areas = self.load_locality_pay()
    
    def calculate_salary(self, grade: int, step: int, locality: str) -> float:
        '''Calculate total federal salary with locality pay'''
        
        # Validate inputs
        if not (1 <= grade <= 15):
            raise ValueError(f"Invalid grade: {grade}")
        if not (1 <= step <= 10):
            raise ValueError(f"Invalid step: {step}")
        
        # Get base pay
        base_pay = self.gs_base['base_rates'][f'GS-{grade}'][step - 1]
        
        # Get locality adjustment (default to Rest of US)
        locality_data = self.locality_areas.get(
            locality, 
            self.locality_areas.get('rest-of-us')
        )
        adjustment = locality_data.get('adjustment', 16.50)
        
        # Calculate total
        total = base_pay * (1 + adjustment / 100)
        
        return round(total, 2)
    
    def get_salary_range(self, grade: int, locality: str) -> Dict:
        '''Get min/max salary for a grade'''
        min_salary = self.calculate_salary(grade, 1, locality)
        max_salary = self.calculate_salary(grade, 10, locality)
        
        return {
            'grade': f'GS-{grade}',
            'locality': locality,
            'min': min_salary,
            'max': max_salary,
            'range': f'${min_salary:,.0f} - ${max_salary:,.0f}'
        }
"""
        
        templates["locality_comparison"] = """
def compare_localities(grade: int, step: int) -> List[Dict]:
    '''Compare salary across all localities'''
    
    comparisons = []
    for locality_key, locality_data in LOCALITY_AREAS.items():
        salary = calculate_salary(grade, step, locality_key)
        comparisons.append({
            'locality': locality_data['name'],
            'adjustment': locality_data['adjustment'],
            'salary': salary,
            'difference_from_base': salary - base_salary
        })
    
    # Sort by salary descending
    return sorted(comparisons, key=lambda x: x['salary'], reverse=True)
"""
        
        return templates
    
    def _identify_data_requirements(self, task_analysis: Dict) -> Dict:
        """Identify required OPM data"""
        return {
            "required_tables": [
                "GS base pay table (current year)",
                "Locality pay adjustments (53 areas)",
                "Special rate tables (if applicable)"
            ],
            "update_frequency": "Annually in January",
            "data_format": "JSON for easy parsing",
            "storage": "Cache in database for performance"
        }
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """
        Phase 3: Review OPM salary implementation
        """
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "compliant": True,
            "violations": [],
            "warnings": [],
            "passed": [],
            "score": 100
        }
        
        # Check for current year data
        if "2025" not in code and "current_year" not in code.lower():
            review["warnings"].append("⚠️ Ensure using 2025 salary tables")
            review["score"] -= 10
        
        # Check for locality adjustment
        if "locality" not in code.lower():
            review["violations"].append("❌ No locality pay adjustment!")
            review["compliant"] = False
            review["score"] -= 30
        else:
            review["passed"].append("✅ Locality pay handled")
        
        # Check for grade/step validation
        if "1 <= grade <= 15" in code or "validate" in code.lower():
            review["passed"].append("✅ Input validation present")
        else:
            review["warnings"].append("⚠️ Add grade/step validation")
            review["score"] -= 10
        
        # Check for all 53 localities
        if "53" in code or "rest-of-us" in code.lower():
            review["passed"].append("✅ Handles all locality areas")
        
        # Check calculation formula
        if "* (1 +" in code or "× (1 +" in code:
            review["passed"].append("✅ Correct salary formula")
        else:
            review["warnings"].append("⚠️ Verify formula: Total = Base × (1 + Locality%/100)")
        
        review["recommendation"] = "✅ Ready for use" if review["score"] >= 70 else "❌ Address issues first"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        """Save research report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"opm_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write(f"# OPM Salary Data Research\n\n")
            f.write(f"**Generated**: {research['timestamp']}\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Critical Rules\n")
            for rule in research['critical_requirements'][:5]:
                f.write(f"- {rule}\n")
            f.write("\n")
            
            if research.get('salary_examples'):
                f.write("## Example Calculations\n")
                for ex in research['salary_examples']:
                    f.write(f"- **{ex['description']}**: {ex['grade']} Step {ex['step']}")
                    f.write(f" in {ex['locality'][:30]}... = **{ex['total_salary']}**\n")
                f.write("\n")
            
            if research.get('code_templates'):
                f.write("## Implementation Templates\n")
                for name, template in research['code_templates'].items():
                    f.write(f"### {name}\n")
                    f.write(f"```python\n{template}\n```\n\n")
        
        return report_path
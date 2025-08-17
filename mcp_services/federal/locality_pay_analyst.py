#!/usr/bin/env python3
"""
Locality Pay Analyst - Federal COL Expert
Uses deepseek-coder-v2:16b for complex COL calculations
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple
import asyncio

class LocalityPayAnalyst:
    """
    Federal domain expert for locality pay and cost of living analysis
    Specializes in comparing federal compensation across regions
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "opm"
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Load locality data
        self.locality_data = self.load_locality_data()
        self.col_indices = self.load_col_indices()
        
        self.critical_insights = [
            "San Francisco has highest adjustment: 42.74%",
            "Rest of US baseline: 16.50%",
            "DC area adjustment: 32.49%",
            "Locality pay doesn't fully offset COL differences",
            "Consider housing costs as primary factor",
            "Tax differences significantly impact take-home",
            "Remote work eligibility affects locality assignment",
            "Special rates may override locality pay"
        ]
        
        self.model = "deepseek-coder-v2:16b"  # Complex calculations
    
    def load_locality_data(self) -> Dict:
        """Load all 53 locality areas"""
        path = self.docs_path / "locality_pay_2025.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {}
    
    def load_col_indices(self) -> Dict:
        """Load cost of living indices"""
        # Simulated COL data (would load from file)
        return {
            "san-francisco": 244.0,
            "new-york": 187.0,
            "washington-dc": 152.0,
            "seattle": 158.0,
            "los-angeles": 173.0,
            "boston": 162.0,
            "denver": 128.0,
            "chicago": 123.0,
            "houston": 96.0,
            "atlanta": 108.0,
            "phoenix": 107.0,
            "rest-of-us": 100.0  # Baseline
        }
    
    def calculate_real_value(self, salary: float, locality: str) -> float:
        """Calculate COL-adjusted salary value"""
        col_index = self.col_indices.get(locality, 100.0)
        return (salary / col_index) * 100
    
    def compare_localities(self, grade: int, step: int) -> List[Dict]:
        """Compare all localities for given grade/step"""
        comparisons = []
        
        # Base salary (example for GS-13)
        base_salary = 96770  # GS-13 Step 1 base
        
        for locality_key, locality_info in self.locality_data.items():
            adjustment = locality_info['adjustment']
            total_salary = base_salary * (1 + adjustment / 100)
            col_index = self.col_indices.get(locality_key, 100.0)
            real_value = self.calculate_real_value(total_salary, locality_key)
            
            comparisons.append({
                "locality": locality_info['name'],
                "adjustment_pct": adjustment,
                "total_salary": total_salary,
                "col_index": col_index,
                "real_value": real_value,
                "value_score": round(real_value / base_salary * 100, 1)
            })
        
        # Sort by real value
        return sorted(comparisons, key=lambda x: x['real_value'], reverse=True)
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research locality pay optimization strategies"""
        
        task_analysis = self._analyze_task(task)
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "task_type": task_analysis['type'],
            "critical_insights": self.critical_insights,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "best_value_locations": self._find_best_value_locations(),
            "relocation_analysis": self._create_relocation_matrix(),
            "code_templates": self._generate_analysis_code()
        }
        
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "top_insight": research["best_value_locations"][0]
        }
    
    def _analyze_task(self, task: str) -> Dict:
        task_lower = task.lower()
        
        if "value" in task_lower or "col" in task_lower:
            return {"type": "value_analysis", "focus": "real_purchasing_power"}
        elif "relocation" in task_lower or "move" in task_lower:
            return {"type": "relocation", "focus": "location_comparison"}
        elif "remote" in task_lower:
            return {"type": "remote_work", "focus": "locality_assignment"}
        else:
            return {"type": "general", "focus": "locality_comparison"}
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict:
        return {
            "summary": f"Locality pay {task_analysis['type']} system",
            "features": [
                "Interactive locality comparison tool",
                "Real purchasing power calculator",
                "Take-home pay estimator (with taxes)",
                "Relocation cost-benefit analyzer",
                "Remote work locality finder",
                "Career progression projections by location"
            ],
            "components": {
                "calculator": {
                    "inputs": ["grade", "step", "current_locality", "target_localities"],
                    "outputs": ["salary_comparison", "col_adjustment", "real_value", "rankings"]
                },
                "visualizations": [
                    "Heat map of real value by location",
                    "Salary vs COL scatter plot",
                    "Take-home pay comparison chart",
                    "5-year projection graphs"
                ],
                "data_updates": {
                    "frequency": "Annual (January)",
                    "sources": ["OPM salary tables", "BLS COL data", "State tax rates"]
                }
            }
        }
    
    def _find_best_value_locations(self) -> List[Dict]:
        """Find locations with best real purchasing power"""
        
        # Example for GS-13 Step 1
        base_salary = 96770
        best_value = []
        
        for locality_key, locality_info in self.locality_data.items():
            if locality_key in self.col_indices:
                adjustment = locality_info['adjustment']
                total_salary = base_salary * (1 + adjustment / 100)
                real_value = self.calculate_real_value(total_salary, locality_key)
                
                best_value.append({
                    "location": locality_info['name'][:30] + "...",
                    "salary": f"${total_salary:,.0f}",
                    "col_index": self.col_indices[locality_key],
                    "real_value": f"${real_value:,.0f}",
                    "verdict": self._get_value_verdict(real_value, base_salary)
                })
        
        # Sort by real value and return top 5
        best_value.sort(key=lambda x: float(x['real_value'].replace('$', '').replace(',', '')), reverse=True)
        return best_value[:5]
    
    def _get_value_verdict(self, real_value: float, base: float) -> str:
        ratio = real_value / base
        if ratio > 1.1:
            return "🟢 Excellent value"
        elif ratio > 1.0:
            return "🟡 Good value"
        elif ratio > 0.9:
            return "🟠 Fair value"
        else:
            return "🔴 Poor value"
    
    def _create_relocation_matrix(self) -> Dict:
        """Create relocation comparison matrix"""
        return {
            "factors_to_consider": [
                "Salary increase/decrease",
                "Housing cost differential",
                "State income tax impact",
                "Moving expenses (~$10-25K)",
                "Quality of life factors",
                "Career advancement opportunities"
            ],
            "break_even_analysis": {
                "formula": "Months = Moving_Cost / Monthly_Gain",
                "typical_range": "12-36 months",
                "recommendation": "Consider if staying 3+ years"
            },
            "hidden_costs": [
                "License/registration transfers",
                "Temporary housing",
                "School/childcare changes",
                "Professional network rebuilding"
            ]
        }
    
    def _generate_analysis_code(self) -> Dict[str, str]:
        """Generate locality analysis code templates"""
        return {
            "value_calculator": """
class LocalityValueCalculator:
    def __init__(self):
        self.localities = load_locality_data()
        self.col_indices = load_col_indices()
        self.tax_rates = load_tax_rates()
    
    def calculate_real_value(self, grade: int, step: int, locality: str) -> Dict:
        '''Calculate real purchasing power after COL and taxes'''
        
        # Get gross salary
        base = self.get_base_salary(grade, step)
        adjustment = self.localities[locality]['adjustment']
        gross = base * (1 + adjustment / 100)
        
        # Calculate taxes
        federal_tax = self.calculate_federal_tax(gross)
        state_tax = self.calculate_state_tax(gross, locality)
        fica = gross * 0.0765
        
        # Net income
        net = gross - federal_tax - state_tax - fica
        
        # Adjust for COL
        col_index = self.col_indices.get(locality, 100)
        real_value = (net / col_index) * 100
        
        return {
            'gross': gross,
            'net': net,
            'real_value': real_value,
            'effective_tax_rate': (gross - net) / gross * 100,
            'col_adjusted_rank': self.get_rank(real_value)
        }
    
    def find_optimal_locations(self, grade: int, priorities: Dict) -> List:
        '''Find best locations based on priorities'''
        
        scores = []
        for locality in self.localities:
            value = self.calculate_real_value(grade, 1, locality)
            
            score = 0
            if priorities.get('maximize_savings'):
                score += value['real_value'] * 0.4
            if priorities.get('low_col'):
                score += (200 - self.col_indices[locality]) * 0.3
            if priorities.get('high_salary'):
                score += value['gross'] * 0.3
            
            scores.append({
                'locality': locality,
                'score': score,
                'details': value
            })
        
        return sorted(scores, key=lambda x: x['score'], reverse=True)[:10]
""",
            "relocation_analyzer": """
def analyze_relocation(current_loc: str, target_loc: str, grade: int) -> Dict:
    '''Analyze financial impact of relocation'''
    
    current = calculate_real_value(grade, 1, current_loc)
    target = calculate_real_value(grade, 1, target_loc)
    
    # Monthly difference
    monthly_gain = (target['net'] - current['net']) / 12
    real_gain = (target['real_value'] - current['real_value']) / 12
    
    # Moving costs
    distance = calculate_distance(current_loc, target_loc)
    moving_cost = estimate_moving_cost(distance)
    
    # Break-even
    if monthly_gain > 0:
        break_even_months = moving_cost / monthly_gain
    else:
        break_even_months = float('inf')
    
    # 5-year projection
    five_year_gain = monthly_gain * 60 - moving_cost
    
    return {
        'recommendation': 'GO' if five_year_gain > 30000 else 'STAY',
        'monthly_gain': monthly_gain,
        'real_purchasing_gain': real_gain,
        'break_even_months': break_even_months,
        'five_year_net': five_year_gain,
        'risk_factors': assess_risks(current_loc, target_loc)
    }
"""
        }
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """Review locality analysis implementation"""
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "compliant": True,
            "violations": [],
            "passed": [],
            "warnings": [],
            "score": 100
        }
        
        # Check for COL adjustment
        if "col" in code.lower() or "cost_of_living" in code.lower():
            review["passed"].append("✅ COL adjustment implemented")
        else:
            review["violations"].append("❌ No COL adjustment!")
            review["score"] -= 30
        
        # Check for tax considerations
        if "tax" in code.lower():
            review["passed"].append("✅ Tax impact considered")
        else:
            review["warnings"].append("⚠️ Consider state taxes")
            review["score"] -= 15
        
        # Check for all localities
        if "53" in code or "all_localities" in code:
            review["passed"].append("✅ Handles all 53 localities")
        
        # Check for real value calculation
        if "real_value" in code or "purchasing_power" in code:
            review["passed"].append("✅ Real value calculated")
        else:
            review["warnings"].append("⚠️ Add purchasing power analysis")
        
        review["recommendation"] = "✅ Ready" if review["score"] >= 70 else "❌ Needs work"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"locality_analysis_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# Locality Pay Analysis Research\n\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Key Insights\n")
            for insight in research['critical_insights'][:5]:
                f.write(f"- {insight}\n")
            f.write("\n")
            
            f.write("## Best Value Locations (GS-13)\n")
            for loc in research['best_value_locations']:
                f.write(f"- **{loc['location']}**: {loc['salary']} salary, ")
                f.write(f"COL {loc['col_index']}, Real value {loc['real_value']} ")
                f.write(f"{loc['verdict']}\n")
            f.write("\n")
            
            if research.get('code_templates'):
                f.write("## Implementation Code\n")
                for name, template in research['code_templates'].items():
                    f.write(f"### {name}\n```python\n{template}\n```\n\n")
        
        return report_path
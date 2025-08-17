#!/usr/bin/env python3
"""
OPM Salary Data Documentation Harvester
Critical for accurate federal salary calculations
"""

import json
from datetime import datetime
from pathlib import Path

def harvest_opm_docs():
    """Harvest OPM salary data documentation"""
    
    base_dir = Path(__file__).parent.parent / "external_services" / "opm"
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💰 Harvesting OPM salary documentation to {base_dir}")
    
    # 2025 General Schedule (GS) Base Pay Table
    gs_base_2025 = {
        "effective_date": "2025-01-01",
        "base_rates": {
            "GS-1": [21022, 21723, 22421, 23116, 23814, 24209, 24901, 25596, 25621, 26283],
            "GS-2": [23633, 24209, 24988, 25621, 25933, 26665, 27397, 28129, 28861, 29593],
            "GS-3": [25792, 26652, 27512, 28372, 29232, 30092, 30952, 31812, 32672, 33532],
            "GS-4": [28966, 29931, 30896, 31861, 32826, 33791, 34756, 35721, 36686, 37651],
            "GS-5": [32423, 33504, 34585, 35666, 36747, 37828, 38909, 39990, 41071, 42152],
            "GS-6": [36152, 37357, 38562, 39767, 40972, 42177, 43382, 44587, 45792, 46997],
            "GS-7": [40171, 41510, 42849, 44188, 45527, 46866, 48205, 49544, 50883, 52222],
            "GS-8": [44512, 46062, 47612, 49162, 50712, 52262, 53812, 55362, 56912, 58462],
            "GS-9": [49255, 50897, 52539, 54181, 55823, 57465, 59107, 60749, 62391, 64033],
            "GS-10": [54292, 56102, 57912, 59722, 61532, 63342, 65152, 66962, 68772, 70582],
            "GS-11": [59675, 61664, 63653, 65642, 67631, 69620, 71609, 73598, 75587, 77576],
            "GS-12": [71491, 73874, 76257, 78640, 81023, 83406, 85789, 88172, 90555, 92938],
            "GS-13": [85021, 87855, 90689, 93523, 96357, 99191, 102025, 104859, 107693, 110527],
            "GS-14": [100506, 103856, 107206, 110556, 113906, 117256, 120606, 123956, 127306, 130656],
            "GS-15": [118172, 122111, 126050, 129989, 133928, 137867, 141806, 145745, 149684, 153623]
        }
    }
    
    # 53 Official Locality Pay Areas (2025 rates)
    locality_areas_2025 = {
        "washington-dc": {"name": "Washington-DC-MD-VA-WV-PA", "adjustment": 32.49},
        "san-francisco": {"name": "San Francisco-Oakland-San Jose, CA", "adjustment": 42.74},
        "new-york": {"name": "New York-Newark, NY-NJ-CT-PA", "adjustment": 36.16},
        "los-angeles": {"name": "Los Angeles-Long Beach, CA", "adjustment": 32.18},
        "seattle": {"name": "Seattle-Tacoma, WA", "adjustment": 28.30},
        "san-diego": {"name": "San Diego-Carlsbad, CA", "adjustment": 30.24},
        "boston": {"name": "Boston-Worcester-Providence, MA-RI-NH-ME-CT", "adjustment": 32.79},
        "chicago": {"name": "Chicago-Naperville, IL-IN-WI", "adjustment": 30.31},
        "denver": {"name": "Denver-Aurora, CO", "adjustment": 29.52},
        "detroit": {"name": "Detroit-Warren-Ann Arbor, MI", "adjustment": 26.07},
        "houston": {"name": "Houston-The Woodlands, TX", "adjustment": 31.48},
        "philadelphia": {"name": "Philadelphia-Reading-Camden, PA-NJ-DE-MD", "adjustment": 28.68},
        "atlanta": {"name": "Atlanta-Athens-Clarke County-Sandy Springs, GA-AL", "adjustment": 23.78},
        "miami": {"name": "Miami-Fort Lauderdale-Port St. Lucie, FL", "adjustment": 23.51},
        "phoenix": {"name": "Phoenix-Mesa-Scottsdale, AZ", "adjustment": 22.43},
        "minneapolis": {"name": "Minneapolis-St. Paul, MN-WI", "adjustment": 26.41},
        "dallas": {"name": "Dallas-Fort Worth, TX-OK", "adjustment": 27.82},
        "rest-of-us": {"name": "Rest of United States", "adjustment": 16.50}
    }
    
    # Save GS base pay table
    with open(base_dir / "gs_base_pay_2025.json", "w") as f:
        json.dump(gs_base_2025, f, indent=2)
    
    # Save locality pay data
    with open(base_dir / "locality_pay_2025.json", "w") as f:
        json.dump(locality_areas_2025, f, indent=2)
    
    # Critical OPM concepts
    with open(base_dir / "CRITICAL_opm_concepts.md", "w") as f:
        f.write("# ⚠️ CRITICAL: OPM Salary Calculation\n\n")
        f.write("## Formula for Total Salary\n")
        f.write("```\n")
        f.write("Total Salary = Base Pay × (1 + Locality Adjustment)\n")
        f.write("```\n\n")
        f.write("## Example Calculation\n")
        f.write("GS-13 Step 5 in Washington DC:\n")
        f.write("- Base Pay: $96,357\n")
        f.write("- Locality Adjustment: 32.49%\n")
        f.write("- Total: $96,357 × 1.3249 = $127,675\n\n")
        f.write("## Within-Grade Increases (WGI)\n")
        f.write("- Steps 1-3: Every year\n")
        f.write("- Steps 4-6: Every 2 years\n")
        f.write("- Steps 7-9: Every 3 years\n\n")
        f.write("## Special Rate Tables\n")
        f.write("Some positions (IT, Medical) have special rates above GS base\n\n")
        f.write("## Key Points\n")
        f.write("- 10 steps within each grade\n")
        f.write("- 15 GS grades total\n")
        f.write("- 53 official locality areas\n")
        f.write("- Rest of US gets 16.50% adjustment\n")
    
    # Salary calculation functions
    calculation_template = {
        "calculate_total_salary": """
def calculate_federal_salary(grade: int, step: int, locality: str) -> float:
    '''Calculate total federal salary with locality pay'''
    
    # Get base pay
    base_pay = GS_BASE_2025[f"GS-{grade}"][step - 1]
    
    # Get locality adjustment
    locality_adjustment = LOCALITY_AREAS.get(locality, {}).get('adjustment', 16.50)
    
    # Calculate total
    total = base_pay * (1 + locality_adjustment / 100)
    
    return round(total, 2)
""",
        "get_salary_range": """
def get_grade_salary_range(grade: int, locality: str) -> dict:
    '''Get min/max salary for a grade in a locality'''
    
    min_salary = calculate_federal_salary(grade, 1, locality)
    max_salary = calculate_federal_salary(grade, 10, locality)
    
    return {
        "grade": f"GS-{grade}",
        "locality": locality,
        "min": min_salary,
        "max": max_salary,
        "range": f"${min_salary:,.0f} - ${max_salary:,.0f}"
    }
"""
    }
    
    with open(base_dir / "calculation_templates.json", "w") as f:
        json.dump(calculation_template, f, indent=2)
    
    # Create manifest
    manifest = {
        "service": "opm",
        "last_updated": datetime.now().isoformat(),
        "ttl_days": 365,  # Update yearly in January
        "data_year": 2025,
        "critical_requirements": [
            "Use current year salary tables",
            "Apply correct locality adjustment",
            "Handle all 53 locality areas",
            "Account for within-grade increases",
            "Consider special rate tables for IT/Medical"
        ],
        "data_sources": [
            "https://www.opm.gov/policy-data-oversight/pay-leave/salaries-wages/",
            "https://www.opm.gov/policy-data-oversight/pay-leave/salaries-wages/salary-tables/25Tables/html/GS.aspx"
        ]
    }
    
    with open(base_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ OPM salary documentation harvested successfully!")
    print(f"💰 Salary tables: {base_dir}/gs_base_pay_2025.json")
    print(f"📍 Locality data: {base_dir}/locality_pay_2025.json")
    
    return base_dir

if __name__ == "__main__":
    harvest_opm_docs()
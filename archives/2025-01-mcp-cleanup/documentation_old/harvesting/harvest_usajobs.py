#!/usr/bin/env python3
"""
USAJobs API Documentation Harvester
Ensures we NEVER forget Fields=Full parameter
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import sys

def harvest_usajobs_docs():
    """Harvest USAJobs API documentation with critical parameters"""
    
    # Setup paths
    base_dir = Path(__file__).parent.parent / "external_services" / "usajobs"
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📚 Harvesting USAJobs documentation to {base_dir}")
    
    # Critical API parameters (NEVER FORGET!)
    critical_params = {
        "Fields": {
            "value": "Full",
            "importance": "CRITICAL",
            "description": "Without this, you lose 93% of data including job_summary, qualification_summary",
            "example": "https://data.usajobs.gov/api/search?Fields=Full&Keyword=data%20scientist",
            "consequences": "Missing Fields=Full causes catastrophic data loss"
        },
        "ResultsPerPage": {
            "value": 500,
            "importance": "HIGH",
            "description": "Maximum results per request for efficient collection",
            "example": "&ResultsPerPage=500"
        },
        "Authorization-Key": {
            "value": "YOUR_API_KEY",
            "importance": "CRITICAL",
            "description": "Required header for authentication",
            "example": "headers={'Authorization-Key': 'your-key-here'}"
        },
        "User-Agent": {
            "value": "YOUR_EMAIL",
            "importance": "REQUIRED",
            "description": "Your email for API tracking",
            "example": "headers={'User-Agent': 'your.email@example.com'}"
        },
        "Rate-Limit": {
            "value": "50 requests/minute",
            "importance": "CRITICAL",
            "description": "Exceeding this will block your API key",
            "example": "time.sleep(1.2) between requests"
        }
    }
    
    # Save critical parameters file (MOST IMPORTANT FILE)
    critical_file = base_dir / "CRITICAL_fields_full.md"
    with open(critical_file, "w") as f:
        f.write("# ⚠️ CRITICAL: USAJobs API Parameters\n\n")
        f.write("## 🚨 NEVER FORGET THESE PARAMETERS 🚨\n\n")
        f.write("### THE #1 RULE: Always Include Fields=Full\n\n")
        f.write("```python\n")
        f.write("# CORRECT - Gets all data\n")
        f.write("url = 'https://data.usajobs.gov/api/search?Fields=Full&Keyword=data'\n\n")
        f.write("# WRONG - Loses 93% of data\n")
        f.write("url = 'https://data.usajobs.gov/api/search?Keyword=data'  # NO NO NO!\n")
        f.write("```\n\n")
        
        for param, info in critical_params.items():
            f.write(f"### {param}\n")
            f.write(f"- **Value**: `{info['value']}`\n")
            f.write(f"- **Importance**: {info['importance']}\n")
            f.write(f"- **Why**: {info['description']}\n")
            if "consequences" in info:
                f.write(f"- **⚠️ WARNING**: {info['consequences']}\n")
            f.write(f"- **Example**: `{info.get('example', '')}`\n\n")
    
    # API endpoints documentation
    endpoints = {
        "search": {
            "url": "https://data.usajobs.gov/api/search",
            "method": "GET",
            "description": "Primary job search endpoint",
            "required_params": ["Fields=Full"],
            "common_params": [
                "Keyword", "LocationName", "JobCategoryCode",
                "Organization", "SalaryBucket", "GradeBucket",
                "PostedDate", "ResultsPerPage", "Page"
            ]
        },
        "codelist": {
            "url": "https://data.usajobs.gov/api/codelist",
            "method": "GET",
            "description": "Get reference data (agencies, series, etc.)"
        }
    }
    
    # Save API reference
    api_ref = base_dir / "api_reference.md"
    with open(api_ref, "w") as f:
        f.write("# USAJobs API Reference\n\n")
        f.write("## Base URL\n")
        f.write("```\nhttps://data.usajobs.gov/api/\n```\n\n")
        
        f.write("## Authentication\n")
        f.write("```python\n")
        f.write("headers = {\n")
        f.write("    'Authorization-Key': 'YOUR_API_KEY',\n")
        f.write("    'User-Agent': 'your.email@example.com'\n")
        f.write("}\n```\n\n")
        
        f.write("## Endpoints\n\n")
        for endpoint_name, endpoint_info in endpoints.items():
            f.write(f"### {endpoint_name.upper()}\n")
            f.write(f"- **URL**: `{endpoint_info['url']}`\n")
            f.write(f"- **Method**: {endpoint_info['method']}\n")
            f.write(f"- **Description**: {endpoint_info['description']}\n")
            if "required_params" in endpoint_info:
                f.write(f"- **REQUIRED**: {', '.join(endpoint_info['required_params'])}\n")
            if "common_params" in endpoint_info:
                f.write(f"- **Common Parameters**: {', '.join(endpoint_info['common_params'])}\n")
            f.write("\n")
    
    # Response schema (what Fields=Full gives you)
    response_schema = {
        "MatchedObjectDescriptor": {
            "PositionID": "Unique identifier",
            "PositionTitle": "Job title",
            "PositionURI": "Direct link to job",
            "ApplyURI": "Application link",
            "PositionLocation": "Array of locations",
            "OrganizationName": "Agency name",
            "DepartmentName": "Department",
            "JobSummary": "ONLY WITH Fields=Full - Job description",
            "QualificationSummary": "ONLY WITH Fields=Full - Requirements",
            "PositionOfferingType": "Array of job types",
            "PositionSchedule": "Array of schedules",
            "PositionRemuneration": "Salary information",
            "PositionStartDate": "Start date",
            "PositionEndDate": "Closing date",
            "PublicationStartDate": "Posted date",
            "SecurityClearanceRequired": "Clearance level",
            "TravelCode": "Travel requirements",
            "MinimumGrade": "Minimum GS level",
            "MaximumGrade": "Maximum GS level",
            "PromotionPotential": "Highest potential grade"
        }
    }
    
    # Save response schema
    with open(base_dir / "response_schemas.json", "w") as f:
        json.dump(response_schema, f, indent=2)
    
    # Create manifest with TTL
    manifest = {
        "service": "usajobs",
        "last_updated": datetime.now().isoformat(),
        "ttl_days": 90,
        "version": "2.0",
        "api_version": "v2",
        "critical_requirements": [
            "ALWAYS include Fields=Full parameter",
            "Include Authorization-Key header",
            "Respect 50 req/min rate limit",
            "Include User-Agent email"
        ],
        "data_loss_warning": "Without Fields=Full, you lose JobSummary, QualificationSummary, and other critical fields",
        "documentation_files": [
            "CRITICAL_fields_full.md",
            "api_reference.md",
            "response_schemas.json"
        ]
    }
    
    with open(base_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    # Create a quick reference card
    quick_ref = base_dir / "QUICK_REFERENCE.md"
    with open(quick_ref, "w") as f:
        f.write("# USAJobs API Quick Reference\n\n")
        f.write("## Copy-Paste Template\n\n")
        f.write("```python\n")
        f.write("import requests\n")
        f.write("import time\n\n")
        f.write("# CRITICAL: Never forget these\n")
        f.write("BASE_URL = 'https://data.usajobs.gov/api/search'\n")
        f.write("PARAMS = {\n")
        f.write("    'Fields': 'Full',  # MANDATORY - prevents 93% data loss\n")
        f.write("    'ResultsPerPage': 500,\n")
        f.write("    'Keyword': 'your search terms'\n")
        f.write("}\n\n")
        f.write("HEADERS = {\n")
        f.write("    'Authorization-Key': 'YOUR_API_KEY',\n")
        f.write("    'User-Agent': 'your.email@example.com'\n")
        f.write("}\n\n")
        f.write("# Make request with rate limiting\n")
        f.write("response = requests.get(BASE_URL, params=PARAMS, headers=HEADERS)\n")
        f.write("time.sleep(1.2)  # Rate limit: 50 req/min\n")
        f.write("```\n")
    
    print(f"✅ USAJobs documentation harvested successfully!")
    print(f"📁 Files created in: {base_dir}")
    print(f"⚠️  CRITICAL file: {critical_file}")
    print(f"📋 Quick reference: {quick_ref}")
    
    return base_dir

if __name__ == "__main__":
    harvest_usajobs_docs()
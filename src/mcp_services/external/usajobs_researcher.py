#!/usr/bin/env python3
"""
USAJobs Research Agent - Service Provider Specialist
Uses Jason Zhou's approach: Research-only, documentation-first, never forgets Fields=Full
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, Optional
import httpx
import asyncio

class USAJobsResearcher:
    """
    Research-only agent for USAJobs API
    Phase 1: Research and create implementation plans
    Phase 3: Review implementations for compliance
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "usajobs"
        self.research_output = self.base_path / "research_outputs" / "tasks"
        
        # Ensure output directory exists
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Load documentation on init
        self.documentation = self.load_documentation()
        self.critical_rules = self.load_critical_rules()
        
    def load_documentation(self) -> Dict[str, Any]:
        """Load USAJobs documentation with TTL check"""
        docs = {}
        
        # Load manifest
        manifest_path = self.docs_path / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                docs['manifest'] = json.load(f)
            
            # Check TTL
            last_updated = datetime.fromisoformat(docs['manifest']['last_updated'])
            age_days = (datetime.now() - last_updated).days
            ttl_days = docs['manifest']['ttl_days']
            
            if age_days > ttl_days:
                print(f"⚠️ USAJobs docs are {age_days} days old (TTL: {ttl_days} days)")
                print(f"   Run: python {self.base_path}/documentation/harvesting/harvest_usajobs.py")
        
        # Load critical documentation
        critical_path = self.docs_path / "CRITICAL_fields_full.md"
        if critical_path.exists():
            with open(critical_path) as f:
                docs['critical'] = f.read()
        else:
            docs['critical'] = "ERROR: Critical documentation missing!"
        
        # Load API reference
        api_ref_path = self.docs_path / "api_reference.md"
        if api_ref_path.exists():
            with open(api_ref_path) as f:
                docs['api_reference'] = f.read()
        
        # Load response schemas
        schema_path = self.docs_path / "response_schemas.json"
        if schema_path.exists():
            with open(schema_path) as f:
                docs['schemas'] = json.load(f)
        
        return docs
    
    def load_critical_rules(self) -> list:
        """Load critical rules that must never be forgotten"""
        return [
            "ALWAYS include Fields=Full parameter in every API call",
            "Include Authorization-Key header with valid API key",
            "Include User-Agent header with email address",
            "Respect rate limit of 50 requests per minute",
            "Use ResultsPerPage=500 for efficient collection",
            "Handle pagination with Page parameter",
            "Check PositionEndDate for expired jobs",
            "Parse location data from PositionLocation array"
        ]
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """
        Phase 1: Research USAJobs implementation approach
        Creates detailed implementation plan without writing code
        """
        
        # Load existing context
        context = self._load_context()
        
        # Analyze task requirements
        task_analysis = self._analyze_task(task)
        
        # Create research report
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "task_type": task_analysis['type'],
            "critical_requirements": self.critical_rules,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "api_endpoints": self._identify_endpoints(task_analysis),
            "parameters": self._determine_parameters(task_analysis),
            "warnings": [],
            "best_practices": []
        }
        
        # Add specific warnings
        if "collect" in task.lower() or "fetch" in task.lower():
            research["warnings"].append("⚠️ CRITICAL: Must include Fields=Full parameter")
            research["warnings"].append("⚠️ Implement rate limiting (50 req/min)")
        
        # Add best practices
        research["best_practices"] = [
            "Use existing collect_federal_jobs.py as reference",
            "Test with small dataset first",
            "Log all API responses for debugging",
            "Handle network errors with exponential backoff"
        ]
        
        # Save research report
        report_path = self._save_research_report(research)
        
        # Update context
        self._update_context(task, report_path)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "critical_reminders": research["critical_requirements"][:3],
            "api_calls": len(research["api_endpoints"])
        }
    
    def _analyze_task(self, task: str) -> Dict[str, Any]:
        """Analyze what the task is asking for"""
        task_lower = task.lower()
        
        analysis = {
            "type": "unknown",
            "operations": [],
            "data_needed": []
        }
        
        # Determine task type
        if "search" in task_lower or "find" in task_lower:
            analysis["type"] = "search"
            analysis["operations"].append("search_jobs")
        elif "collect" in task_lower or "fetch" in task_lower:
            analysis["type"] = "collection"
            analysis["operations"].append("bulk_collection")
        elif "filter" in task_lower:
            analysis["type"] = "filtering"
            analysis["operations"].append("apply_filters")
        
        # Identify data needs
        if "salary" in task_lower:
            analysis["data_needed"].append("PositionRemuneration")
        if "location" in task_lower:
            analysis["data_needed"].append("PositionLocation")
        if "agency" in task_lower:
            analysis["data_needed"].append("OrganizationName")
        if "series" in task_lower or "job category" in task_lower:
            analysis["data_needed"].append("JobCategory")
        
        return analysis
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict[str, Any]:
        """Create detailed implementation plan based on task analysis"""
        
        plan = {
            "summary": f"Implementation plan for {task_analysis['type']} operation",
            "steps": [],
            "code_structure": {},
            "error_handling": []
        }
        
        # Add steps based on task type
        if task_analysis["type"] == "search":
            plan["steps"] = [
                "1. Setup request headers with authentication",
                "2. Build search parameters with Fields=Full",
                "3. Execute search request",
                "4. Parse response and extract jobs",
                "5. Handle pagination if needed"
            ]
            plan["code_structure"] = {
                "functions": [
                    "setup_headers() - Authentication headers",
                    "build_search_params() - Include Fields=Full",
                    "search_jobs() - Main search function",
                    "parse_response() - Extract job data"
                ]
            }
        elif task_analysis["type"] == "collection":
            plan["steps"] = [
                "1. Initialize collection parameters",
                "2. Setup rate limiting (1.2 sec delay)",
                "3. Iterate through pages with Fields=Full",
                "4. Store results in database",
                "5. Track collection metrics"
            ]
            plan["code_structure"] = {
                "functions": [
                    "collect_jobs() - Main collection loop",
                    "rate_limit() - Enforce 50 req/min",
                    "save_to_db() - Store job data",
                    "track_metrics() - Monitor collection"
                ]
            }
        
        # Add error handling
        plan["error_handling"] = [
            "HTTPError - Retry with exponential backoff",
            "RateLimitError - Wait and retry",
            "JSONDecodeError - Log and skip",
            "NetworkError - Retry up to 3 times"
        ]
        
        return plan
    
    def _identify_endpoints(self, task_analysis: Dict) -> list:
        """Identify which API endpoints are needed"""
        endpoints = []
        
        # Primary search endpoint for most operations
        endpoints.append({
            "url": "https://data.usajobs.gov/api/search",
            "method": "GET",
            "purpose": "Primary job search",
            "required_params": ["Fields=Full"]
        })
        
        # Add codelist endpoint if needed
        if "agency" in str(task_analysis.get("data_needed", [])):
            endpoints.append({
                "url": "https://data.usajobs.gov/api/codelist/agencies",
                "method": "GET",
                "purpose": "Get agency codes"
            })
        
        return endpoints
    
    def _determine_parameters(self, task_analysis: Dict) -> Dict[str, Any]:
        """Determine API parameters based on task"""
        
        params = {
            "required": {
                "Fields": "Full"  # ALWAYS REQUIRED
            },
            "recommended": {
                "ResultsPerPage": 500,
                "SortField": "PositionStartDate"
            },
            "optional": {}
        }
        
        # Add parameters based on data needs
        if "PositionRemuneration" in task_analysis.get("data_needed", []):
            params["optional"]["SalaryBucket"] = "Example: 5 (for $100k+)"
        
        if "PositionLocation" in task_analysis.get("data_needed", []):
            params["optional"]["LocationName"] = "Example: Washington, DC"
        
        return params
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """
        Phase 3: Review USAJobs implementation for compliance
        Checks for critical requirements and best practices
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
        
        # CRITICAL CHECK #1: Fields=Full
        if "Fields=Full" not in code and "Fields%3DFull" not in code:
            review["violations"].append("❌ CRITICAL: Missing Fields=Full parameter - will lose 93% of data!")
            review["compliant"] = False
            review["score"] -= 50
        else:
            review["passed"].append("✅ Fields=Full parameter present")
        
        # CHECK #2: Authentication
        if not any(auth in code for auth in ["Authorization-Key", "ApiKey", "headers"]):
            review["violations"].append("❌ Missing API authentication headers")
            review["compliant"] = False
            review["score"] -= 20
        else:
            review["passed"].append("✅ API authentication configured")
        
        # CHECK #3: Rate limiting
        if not any(term in code.lower() for term in ["sleep", "delay", "rate", "limit", "throttle"]):
            review["warnings"].append("⚠️ No rate limiting detected - may hit API limits")
            review["score"] -= 10
        else:
            review["passed"].append("✅ Rate limiting implemented")
        
        # CHECK #4: Error handling
        if "try" not in code and "except" not in code and "catch" not in code:
            review["warnings"].append("⚠️ No error handling detected")
            review["score"] -= 10
        else:
            review["passed"].append("✅ Error handling present")
        
        # CHECK #5: ResultsPerPage optimization
        if "ResultsPerPage" in code:
            if "500" in code:
                review["passed"].append("✅ Optimal ResultsPerPage=500")
            else:
                review["warnings"].append("⚠️ Consider using ResultsPerPage=500 for efficiency")
        
        # Generate recommendation
        if review["compliant"]:
            review["recommendation"] = "✅ Implementation is ready for deployment"
        else:
            review["recommendation"] = "❌ Fix critical violations before deployment"
        
        return review
    
    def _load_context(self) -> str:
        """Load existing context from shared file"""
        context_file = self.research_output / "context.md"
        if context_file.exists():
            with open(context_file) as f:
                return f.read()
        return ""
    
    def _update_context(self, task: str, report_path: Path):
        """Update shared context file"""
        context_file = self.research_output / "context.md"
        
        with open(context_file, "a") as f:
            f.write(f"\n## USAJobs Research - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"- **Task**: {task}\n")
            f.write(f"- **Report**: {report_path.name}\n")
            f.write(f"- **Key Reminder**: Fields=Full is mandatory\n\n")
    
    def _save_research_report(self, research: Dict) -> Path:
        """Save research report to markdown file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"usajobs_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write(f"# USAJobs API Research Report\n\n")
            f.write(f"**Generated**: {research['timestamp']}\n")
            f.write(f"**Task**: {research['task']}\n")
            f.write(f"**Type**: {research['task_type']}\n\n")
            
            f.write("## Critical Requirements\n")
            for req in research['critical_requirements']:
                f.write(f"- {req}\n")
            f.write("\n")
            
            f.write("## Implementation Plan\n")
            f.write(f"{research['implementation_plan']['summary']}\n\n")
            f.write("### Steps\n")
            for step in research['implementation_plan']['steps']:
                f.write(f"{step}\n")
            f.write("\n")
            
            f.write("## API Endpoints\n")
            for endpoint in research['api_endpoints']:
                f.write(f"- **{endpoint['purpose']}**: `{endpoint['url']}`\n")
                if 'required_params' in endpoint:
                    f.write(f"  - Required: {', '.join(endpoint['required_params'])}\n")
            f.write("\n")
            
            f.write("## Parameters\n")
            f.write("### Required\n")
            for key, value in research['parameters']['required'].items():
                f.write(f"- `{key}={value}`\n")
            f.write("\n")
            
            if research['warnings']:
                f.write("## ⚠️ Warnings\n")
                for warning in research['warnings']:
                    f.write(f"- {warning}\n")
                f.write("\n")
            
            if research['best_practices']:
                f.write("## Best Practices\n")
                for practice in research['best_practices']:
                    f.write(f"- {practice}\n")
        
        return report_path


# Test function
async def test_researcher():
    """Test the USAJobs researcher"""
    researcher = USAJobsResearcher()
    
    # Test research
    print("Testing research phase...")
    result = await researcher.research_task("Implement job search for data scientist positions in DC")
    print(f"Research result: {result}")
    
    # Test review
    print("\nTesting review phase...")
    sample_code = """
    def search_jobs():
        url = 'https://data.usajobs.gov/api/search'
        params = {
            'Fields': 'Full',
            'Keyword': 'data scientist',
            'ResultsPerPage': 500
        }
        headers = {
            'Authorization-Key': API_KEY,
            'User-Agent': 'test@example.com'
        }
        response = requests.get(url, params=params, headers=headers)
        time.sleep(1.2)  # Rate limiting
    """
    review = await researcher.review_implementation(sample_code)
    print(f"Review result: {review}")

if __name__ == "__main__":
    asyncio.run(test_researcher())
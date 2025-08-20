#!/usr/bin/env python3
"""
USAJobs API Master - Ultra-deep expertise in USAJobs API v2.0
Critical for Fed Job Advisor's core data collection functionality
"""

from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import asyncio
from enum import Enum

class USAJobsEndpoint(Enum):
    """USAJobs API endpoints"""
    SEARCH = "/Search/jobs"
    SEARCH_RESUME = "/Search/resumelibrary"
    CODELIST = "/codelist"
    AGENCY_SUBELEMENTS = "/codelist/agencysubelements"
    OCCUPATIONAL_SERIES = "/codelist/occupationalseries"
    PAY_PLANS = "/codelist/payplans"
    POSTAL_CODES = "/codelist/postalcodes"
    GEO_DATA = "/codelist/geolocationcodes"

class USAJobsMaster:
    """
    Ultra-specialized agent for USAJobs API integration
    Complete knowledge of API quirks, rate limits, and data extraction
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "usajobs"
        self.research_output = self.base_path / "research_outputs" / "usajobs_optimization"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Exhaustive USAJobs API knowledge
        self.knowledge_base = {
            "api_configuration": {
                "base_url": "https://data.usajobs.gov/api",
                "authentication": {
                    "method": "API Key in headers",
                    "headers": {
                        "Authorization-Key": "YOUR_API_KEY",
                        "User-Agent": "your-email@example.com",
                        "Host": "data.usajobs.gov"
                    },
                    "required": "Email in User-Agent is mandatory"
                },
                "rate_limits": {
                    "requests_per_second": 30,
                    "daily_limit": None,  # No documented daily limit
                    "concurrent_connections": 10,
                    "retry_after": "Check Retry-After header"
                },
                "response_format": {
                    "type": "JSON",
                    "encoding": "UTF-8",
                    "max_size": "No documented limit",
                    "pagination": "Page and ResultsPerPage parameters"
                }
            },
            
            "search_parameters": {
                "critical_params": {
                    "Fields": {
                        "importance": "CRITICAL - Must be 'Min' or 'Full'",
                        "default": "Min (causes 93% data loss!)",
                        "correct_value": "Full",
                        "impact": "Without Fields=Full, miss job descriptions"
                    },
                    "ResultsPerPage": {
                        "max": 500,
                        "recommended": 250,
                        "default": 25
                    },
                    "Page": {
                        "type": "integer",
                        "starts_at": 1,
                        "max_pages": "Calculated from TotalResults"
                    }
                },
                "location_params": {
                    "LocationName": "City, State format",
                    "PostalCode": "5-digit ZIP",
                    "Radius": "Miles from location (default 20)",
                    "Country": "United States",
                    "CountrySubdivision": "State code"
                },
                "job_filters": {
                    "Keyword": "Search terms",
                    "KeywordExclusion": "Exclude terms",
                    "PositionTitle": "Exact title match",
                    "JobCategoryCode": "Occupational series",
                    "Organization": "Agency code",
                    "DepartmentCode": "Department filter",
                    "SalaryBucket": "Salary range filter",
                    "GradeBucket": "GS grade range"
                },
                "date_filters": {
                    "DatePosted": "Number of days back (0-30)",
                    "ApplicationCloseDate": "ISO format date"
                },
                "employment_type": {
                    "PositionSchedule": [1, 2, 3, 4, 5],  # Full-time, part-time, etc
                    "PositionType": [1, 2, 3, 4],  # Permanent, temporary, etc
                    "SecurityClearance": [0, 1, 2, 3, 4, 5],  # None to Top Secret
                    "TravelPercentage": [0, 25, 50, 75, 100]
                }
            },
            
            "data_extraction": {
                "response_structure": {
                    "SearchResult": {
                        "SearchResultCount": "Total results",
                        "SearchResultCountAll": "Including expired",
                        "SearchResultItems": "Array of jobs"
                    },
                    "job_structure": {
                        "MatchedObjectId": "Unique job ID",
                        "PositionTitle": "Job title",
                        "PositionURI": "Direct link to job",
                        "ApplyURI": "Application link",
                        "PositionLocation": "Array of locations",
                        "OrganizationName": "Agency name",
                        "DepartmentName": "Department",
                        "JobSummary": "Brief description",
                        "MinimumRange": "Salary minimum",
                        "MaximumRange": "Salary maximum",
                        "RateIntervalCode": "Per Year/Hour",
                        "JobGrade": "Array of grade levels",
                        "PositionStartDate": "When job starts",
                        "PositionEndDate": "When posting closes",
                        "PublicationStartDate": "When posted",
                        "ApplicationCloseDate": "Application deadline"
                    }
                },
                "nested_data": {
                    "UserArea": {
                        "Details": {
                            "JobSummary": "Full job description",
                            "MajorDuties": "Detailed duties",
                            "Education": "Education requirements",
                            "Requirements": "Qualifications",
                            "Evaluations": "How you'll be evaluated",
                            "HowToApply": "Application instructions",
                            "WhatToExpectNext": "Hiring process",
                            "RequiredDocuments": "Documents needed",
                            "Benefits": "Benefits information",
                            "OtherInformation": "Additional info"
                        }
                    }
                },
                "common_issues": {
                    "missing_fields": "Use Fields=Full parameter",
                    "truncated_data": "Check pagination",
                    "null_values": "Handle gracefully",
                    "html_in_text": "Strip HTML tags",
                    "encoding_issues": "UTF-8 decode errors"
                }
            },
            
            "error_handling": {
                "http_errors": {
                    "400": "Bad request - check parameters",
                    "401": "Unauthorized - check API key",
                    "403": "Forbidden - rate limit or permission",
                    "404": "Endpoint not found",
                    "429": "Too many requests - check rate limit",
                    "500": "Server error - retry with backoff",
                    "503": "Service unavailable - maintenance"
                },
                "api_specific_errors": {
                    "invalid_parameter": "Check parameter names and values",
                    "missing_user_agent": "Add email to User-Agent header",
                    "invalid_date_format": "Use ISO 8601 format",
                    "exceeded_page_limit": "Calculate max pages from total"
                },
                "retry_strategy": {
                    "initial_delay": 1,
                    "max_delay": 60,
                    "exponential_base": 2,
                    "max_retries": 5,
                    "retry_on": [429, 500, 502, 503, 504]
                }
            },
            
            "optimization_strategies": {
                "collection_efficiency": {
                    "parallel_requests": "Use asyncio with semaphore",
                    "batch_processing": "Process in chunks of 250",
                    "incremental_updates": "Track last_modified dates",
                    "deduplication": "Use MatchedObjectId as unique key",
                    "caching": "Cache code lists and agencies"
                },
                "data_quality": {
                    "validation": "Verify required fields present",
                    "normalization": "Standardize location formats",
                    "enrichment": "Add calculated fields",
                    "cleaning": "Remove HTML, fix encoding"
                },
                "storage_optimization": {
                    "compression": "Store as JSONB in PostgreSQL",
                    "indexing": "Index on common search fields",
                    "partitioning": "Partition by date_posted",
                    "archival": "Move old jobs to archive"
                }
            },
            
            "fed_job_advisor_integration": {
                "collection_schedule": {
                    "frequency": "Every 10 minutes",
                    "priority_agencies": ["VA", "DOD", "DHS", "DOJ"],
                    "priority_series": ["2210", "0343", "1560", "1530"],
                    "location_focus": ["Washington, DC", "Remote"]
                },
                "data_pipeline": {
                    "extract": "Fetch with Fields=Full",
                    "transform": "Clean and normalize",
                    "load": "Insert/update in PostgreSQL",
                    "validate": "Check field population rates"
                },
                "monitoring": {
                    "metrics": [
                        "Jobs collected per run",
                        "Field population rate",
                        "API response time",
                        "Error rate"
                    ],
                    "alerts": [
                        "Field population < 98%",
                        "Collection failures",
                        "Rate limit hits"
                    ]
                },
                "known_issues": {
                    "fields_parameter": {
                        "problem": "Default Min causes 93% data loss",
                        "solution": "Always use Fields=Full",
                        "validation": "Check JobSummary field populated"
                    },
                    "pagination_limits": {
                        "problem": "Max 10,000 results per search",
                        "solution": "Use date ranges to segment",
                        "implementation": "Search by week if over limit"
                    }
                }
            }
        }
    
    async def generate_collection_script(self) -> str:
        """
        Generate optimized USAJobs collection script
        """
        script = f"""#!/usr/bin/env python3
\"\"\"
USAJobs Data Collection Script
Generated: {datetime.now().isoformat()}
CRITICAL: Always use Fields=Full to avoid 93% data loss
\"\"\"

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
import logging
from urllib.parse import urlencode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class USAJobsCollector:
    def __init__(self):
        self.base_url = "https://data.usajobs.gov/api/Search/jobs"
        self.api_key = os.environ.get("USAJOBS_API_KEY")
        self.user_agent = os.environ.get("USAJOBS_USER_AGENT")  # Must be email
        
        if not self.api_key or not self.user_agent:
            raise ValueError("USAJOBS_API_KEY and USAJOBS_USER_AGENT required")
        
        self.headers = {{
            "Authorization-Key": self.api_key,
            "User-Agent": self.user_agent,
            "Host": "data.usajobs.gov"
        }}
        
        # Rate limiting
        self.semaphore = asyncio.Semaphore(10)  # Max 10 concurrent
        self.rate_limit = 30  # Requests per second
        
    async def fetch_jobs(self, params: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Fetch jobs from USAJobs API with retry logic\"\"\"
        
        # CRITICAL: Always include Fields=Full
        params["Fields"] = "Full"
        params["ResultsPerPage"] = 250  # Optimal batch size
        
        url = f"{{self.base_url}}?{{urlencode(params)}}"
        
        async with self.semaphore:
            for attempt in range(5):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                
                                # Validate Fields=Full worked
                                if data.get("SearchResult", {{}}).get("SearchResultItems"):
                                    first_job = data["SearchResult"]["SearchResultItems"][0]
                                    if not first_job.get("MatchedObjectDescriptor", {{}}).get("UserArea", {{}}).get("Details"):
                                        logger.error("WARNING: Fields=Full not working - missing job details!")
                                
                                return data
                            
                            elif response.status == 429:
                                # Rate limited
                                retry_after = int(response.headers.get("Retry-After", 60))
                                logger.warning(f"Rate limited, waiting {{retry_after}} seconds")
                                await asyncio.sleep(retry_after)
                            
                            else:
                                logger.error(f"API error {{response.status}}: {{await response.text()}}")
                                await asyncio.sleep(2 ** attempt)
                
                except Exception as e:
                    logger.error(f"Request failed: {{e}}")
                    await asyncio.sleep(2 ** attempt)
        
        return {{}
    
    async def collect_all_jobs(self, search_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        \"\"\"Collect all jobs matching search criteria\"\"\"
        
        if not search_params:
            # Default: Recent federal jobs
            search_params = {{
                "DatePosted": 7,  # Last 7 days
                "ResultsPerPage": 250,
                "Page": 1
            }}
        
        all_jobs = []
        page = 1
        total_pages = 1
        
        while page <= total_pages:
            search_params["Page"] = page
            
            logger.info(f"Fetching page {{page}}/{{total_pages}}")
            result = await self.fetch_jobs(search_params)
            
            if not result:
                break
            
            search_result = result.get("SearchResult", {{}})
            total_results = search_result.get("SearchResultCount", 0)
            
            # Calculate total pages
            total_pages = (total_results + 249) // 250  # Ceiling division
            
            jobs = search_result.get("SearchResultItems", [])
            all_jobs.extend(jobs)
            
            logger.info(f"Collected {{len(jobs)}} jobs, total: {{len(all_jobs)}}/{{total_results}}")
            
            # Validate data quality
            if jobs:
                sample_job = jobs[0]
                has_details = bool(sample_job.get("MatchedObjectDescriptor", {{}}).get("UserArea", {{}}).get("Details"))
                if not has_details:
                    logger.error("CRITICAL: Missing job details! Check Fields=Full parameter")
            
            page += 1
            
            # Rate limiting
            await asyncio.sleep(1 / self.rate_limit)
        
        return all_jobs
    
    def extract_job_data(self, job: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Extract and normalize job data\"\"\"
        
        descriptor = job.get("MatchedObjectDescriptor", {{}})
        user_area = descriptor.get("UserArea", {{}})
        details = user_area.get("Details", {{}})
        
        # Extract core fields
        extracted = {{
            "job_id": job.get("MatchedObjectId"),
            "title": descriptor.get("PositionTitle"),
            "agency": descriptor.get("OrganizationName"),
            "department": descriptor.get("DepartmentName"),
            "location": descriptor.get("PositionLocationDisplay"),
            "salary_min": descriptor.get("PositionRemuneration", [{{}}])[0].get("MinimumRange"),
            "salary_max": descriptor.get("PositionRemuneration", [{{}}])[0].get("MaximumRange"),
            "posted_date": descriptor.get("PublicationStartDate"),
            "close_date": descriptor.get("ApplicationCloseDate"),
            "url": descriptor.get("PositionURI"),
            "apply_url": descriptor.get("ApplyURI", [None])[0],
            
            # CRITICAL: These fields require Fields=Full
            "summary": details.get("JobSummary"),
            "duties": details.get("MajorDuties"),
            "qualifications": details.get("Qualifications"),
            "education": details.get("Education"),
            "benefits": details.get("Benefits"),
            "how_to_apply": details.get("HowToApply"),
            
            # Additional metadata
            "telework_eligible": user_area.get("IsRadialSearch", False),
            "security_clearance": details.get("SecurityClearance"),
            "collected_at": datetime.now().isoformat()
        }}
        
        # Validate critical fields
        if not extracted["summary"] or not extracted["duties"]:
            logger.warning(f"Missing critical fields for job {{extracted['job_id']}}")
        
        return extracted
    
    async def run_collection(self):
        \"\"\"Main collection pipeline\"\"\"
        
        logger.info("Starting USAJobs collection")
        
        # Collect jobs
        jobs = await self.collect_all_jobs()
        
        logger.info(f"Collected {{len(jobs)}} total jobs")
        
        # Process and validate
        processed_jobs = []
        fields_populated = 0
        
        for job in jobs:
            processed = self.extract_job_data(job)
            processed_jobs.append(processed)
            
            # Check field population
            if processed["summary"] and processed["duties"]:
                fields_populated += 1
        
        # Calculate field population rate
        population_rate = (fields_populated / len(jobs) * 100) if jobs else 0
        
        logger.info(f"Field population rate: {{population_rate:.1f}}%")
        
        if population_rate < 98:
            logger.error(f"WARNING: Low field population rate! Check Fields=Full parameter")
        
        # Save results
        output_file = f"usajobs_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"
        with open(output_file, 'w') as f:
            json.dump({{
                "metadata": {{
                    "collected_at": datetime.now().isoformat(),
                    "total_jobs": len(jobs),
                    "field_population_rate": population_rate
                }},
                "jobs": processed_jobs
            }}, f, indent=2)
        
        logger.info(f"Saved to {{output_file}}")
        
        return processed_jobs

if __name__ == "__main__":
    collector = USAJobsCollector()
    asyncio.run(collector.run_collection())
"""
        
        return script
    
    async def diagnose_collection_issue(self, error_log: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnose USAJobs collection issues
        """
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "issue_detected": [],
            "root_cause": None,
            "solutions": [],
            "validation_steps": []
        }
        
        # Check for Fields=Full issue (MOST CRITICAL)
        field_rate = metrics.get("field_population_rate", 0)
        if field_rate < 98:
            diagnosis["issue_detected"].append("Low field population rate")
            diagnosis["root_cause"] = "Fields=Full parameter not working or missing"
            diagnosis["solutions"].extend([
                "Verify Fields=Full in all API calls",
                "Check API key permissions",
                "Validate response structure"
            ])
            diagnosis["validation_steps"].extend([
                "Check if UserArea.Details exists in response",
                "Verify JobSummary field is populated",
                "Confirm MajorDuties field has content"
            ])
        
        # Check for rate limiting
        if "429" in error_log or "rate" in error_log.lower():
            diagnosis["issue_detected"].append("Rate limiting detected")
            diagnosis["solutions"].extend([
                "Reduce concurrent requests to 10",
                "Add exponential backoff",
                "Check Retry-After header"
            ])
        
        # Check for authentication issues
        if "401" in error_log or "unauthorized" in error_log.lower():
            diagnosis["issue_detected"].append("Authentication failure")
            diagnosis["solutions"].extend([
                "Verify API key is valid",
                "Check User-Agent header contains email",
                "Ensure Host header is set correctly"
            ])
        
        return diagnosis
    
    async def optimize_search_params(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate optimized search parameters for specific needs
        """
        params = {
            "Fields": "Full",  # ALWAYS
            "ResultsPerPage": 250,
            "Page": 1
        }
        
        # Add location parameters
        if requirements.get("location"):
            if requirements["location"] == "remote":
                params["TeleworkEligible"] = True
            else:
                params["LocationName"] = requirements["location"]
                params["Radius"] = requirements.get("radius", 25)
        
        # Add series/category
        if requirements.get("series"):
            params["JobCategoryCode"] = requirements["series"]
        
        # Add agency filter
        if requirements.get("agency"):
            params["Organization"] = requirements["agency"]
        
        # Add date filter
        params["DatePosted"] = requirements.get("days_back", 7)
        
        # Add salary filter
        if requirements.get("min_salary"):
            salary_buckets = {
                50000: "50000-74999",
                75000: "75000-99999",
                100000: "100000-124999",
                125000: "125000+"
            }
            for threshold, bucket in salary_buckets.items():
                if requirements["min_salary"] >= threshold:
                    params["SalaryBucket"] = bucket
        
        return params

# CLI interface
if __name__ == "__main__":
    import sys
    
    master = USAJobsMaster()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "generate":
            script = asyncio.run(master.generate_collection_script())
            print(script)
        
        elif command == "diagnose":
            if len(sys.argv) > 2:
                metrics = json.loads(sys.argv[2])
                result = asyncio.run(master.diagnose_collection_issue("", metrics))
                print(json.dumps(result, indent=2))
        
        elif command == "optimize":
            if len(sys.argv) > 2:
                requirements = json.loads(sys.argv[2])
                params = asyncio.run(master.optimize_search_params(requirements))
                print(json.dumps(params, indent=2))
    else:
        print("USAJobs API Master")
        print("Commands:")
        print("  generate - Generate collection script")
        print("  diagnose <metrics> - Diagnose collection issues")
        print("  optimize <requirements> - Generate search parameters")
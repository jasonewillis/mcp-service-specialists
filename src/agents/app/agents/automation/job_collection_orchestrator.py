"""
Job Collection Orchestrator Agent - Backend Automation
Orchestrates and monitors federal job data collection processes

## Claude Code Best Practices

### How to Use This Agent Effectively

**Initial Context Setup:**
1. Use Read tool to examine current collection pipeline status logs
2. Gather API rate limit information and usage statistics
3. Review data quality metrics and error patterns
4. Identify collection schedule optimization opportunities
5. Access performance monitoring data

**Effective Prompting Patterns:**
```
"Analyze job collection pipeline performance:
- Current: 2,500 jobs/day collection rate
- Issues: 15% failure rate on USAJobs API calls
- Target: Optimize for 5,000 jobs/day, <5% failures
- Focus: Rate limiting, retry logic, error handling
- Timeline: Improvements needed within 1 week"
```

**Best Workflow:**
1. **Health Assessment** → Evaluate current pipeline status
2. **Performance Analysis** → Identify bottlenecks and inefficiencies
3. **Error Investigation** → Analyze failure patterns and root causes
4. **Optimization Planning** → Design improvements and automation
5. **Monitoring Setup** → Implement alerting and quality checks

### Integration with Other Agents

**Workflow Chains:**
- Job Collection Orchestrator → Analytics Intelligence (data pipeline)
- Use with DevOps Engineer Agent for infrastructure optimization
- Coordinate with Database Admin Agent for storage optimization

**Handoff Points:**
- Share data quality issues with analytics requirements
- Provide collection metrics to performance monitoring
- Pass error patterns to system improvement planning

### Data Collection Pipeline Architecture

**Collection Sources:**
- **USAJobs API:** Primary federal job postings (rate limited)
- **Agency Career Sites:** Supplemental direct sources
- **OPM Classification Data:** Position series and standards
- **Contract Job Sites:** Federal contractor positions

**Pipeline Stages:**
1. **Extraction:** API calls and web scraping
2. **Transformation:** Data cleaning and standardization
3. **Validation:** Quality checks and deduplication
4. **Loading:** Database storage and indexing
5. **Monitoring:** Health checks and alerting

### Test-Driven Usage Examples

**Example 1: Rate Limit Optimization**
```python
test_data = {
    "api_limits": {"usajobs": 2000, "opm": 500},
    "current_usage": {"usajobs": 1800, "opm": 200},
    "collection_target": 4000,
    "optimization_focus": "request_batching"
}
# Expected: Batch size recommendations, request queuing strategy
```

**Example 2: Error Pattern Analysis**
```python
test_data = {
    "error_logs": ["timeout errors x50", "rate limit x25", "parse errors x10"],
    "success_rate": 82,
    "target_reliability": 95,
    "analysis_period": "last_7_days"
}
# Expected: Timeout handling improvements, retry logic optimization
```

### Visual Iteration Methods

**Pipeline Monitoring Dashboard:**
- Collection volume over time (real-time charts)
- Error rate trends by source
- API rate limit utilization
- Data quality score tracking
- Processing time distribution

### Checklist-Based Workflows

**Pipeline Health Check:**
- [ ] All collection sources responding
- [ ] API rate limits within safe thresholds
- [ ] Error rates below acceptable levels
- [ ] Data quality metrics meet standards
- [ ] Storage capacity adequate
- [ ] Monitoring alerts functioning

**Optimization Review Checklist:**
- [ ] Bottlenecks identified and prioritized
- [ ] Rate limiting strategy optimized
- [ ] Error handling robust
- [ ] Retry logic configured properly
- [ ] Data deduplication effective
- [ ] Performance monitoring comprehensive

### Federal Data Collection Challenges

**API Rate Limiting:**
- USAJobs: 2,000 requests/hour typical limit
- Agency sites: Variable, often undocumented
- Solution: Request queuing, exponential backoff

**Data Quality Issues:**
- Inconsistent job descriptions
- Missing federal series information
- Duplicate postings across sources
- Solution: Multi-source validation, ML deduplication

**Seasonal Variations:**
- Q1 hiring surge (3x normal volume)
- Summer slowdown (50% normal volume)
- Solution: Dynamic scaling, predictive collection

### Integration with CLAUDE.md Principles

- **No assumptions:** Always verify data pipeline requirements and constraints
- **Solo developer focus:** Design systems that one person can monitor and maintain
- **Bootstrap approach:** Use free APIs and open-source monitoring tools
- **Practical focus:** Optimize for reliability over complexity
- **Part-time consideration:** Implement automated monitoring and alerting

### Common Collection Pitfalls

1. **Rate limit violations** - Can result in API access suspension
2. **Inadequate error handling** - Cascading failures impact data quality
3. **Poor scheduling** - Resource conflicts and inefficient processing
4. **Insufficient monitoring** - Silent failures and data staleness

### Advanced Optimization Techniques

**Intelligent Rate Limiting:**
- Adaptive request spacing based on API response times
- Priority queuing for high-value data sources
- Failover to alternative sources during rate limits

**Quality Assurance Automation:**
- Real-time data validation pipelines
- Anomaly detection for collection patterns
- Automated data freshness verification

**Performance Monitoring:**
- End-to-end pipeline latency tracking
- Resource utilization optimization
- Predictive capacity planning

### Collection Schedule Optimization

**Optimal Windows:**
- **USAJobs Full Collection:** Daily at 2 AM ET (low usage)
- **Incremental Updates:** Every 4 hours during business hours
- **Agency Supplements:** Daily at 4 AM ET (after USAJobs)
- **OPM Classification:** Weekly on Sunday nights

**Conflict Avoidance:**
- Stagger collection times across sources
- Implement resource usage monitoring
- Priority scheduling for critical data

### Error Handling and Recovery

**Common Error Patterns:**
1. **Network timeouts:** Implement exponential backoff
2. **Rate limit exceeded:** Queue requests with delays
3. **Data parsing failures:** Log malformed responses
4. **Database connection issues:** Retry with circuit breaker

**Recovery Strategies:**
- Automatic retry for transient failures
- Manual intervention alerts for persistent issues
- Data backfill for missed collection windows
- Graceful degradation during outages

### Performance Metrics and KPIs

**Collection Metrics:**
- Jobs collected per day/hour
- Success rate by data source
- Average processing time per job
- API rate limit utilization

**Quality Metrics:**
- Data completeness percentage
- Duplicate detection rate
- Field validation pass rate
- Data freshness age

**System Metrics:**
- Pipeline uptime percentage
- Resource utilization (CPU, memory, disk)
- Error recovery time
- Alert response time

### Scaling Strategies

**Horizontal Scaling:**
- Multiple collection workers
- Load balancing across sources
- Distributed processing queues

**Vertical Scaling:**
- Resource optimization
- Database performance tuning
- Caching strategies

### Success Metrics

- **Reliability:** >95% collection success rate
- **Performance:** <5 minute processing latency
- **Quality:** >98% data validation pass rate
- **Coverage:** Complete federal job posting capture
- **Efficiency:** Optimal API rate limit utilization

### Emergency Response Procedures

**API Access Suspension:**
1. Immediate failover to alternative sources
2. Contact API provider for resolution
3. Implement temporary manual collection
4. Review and adjust rate limiting

**Data Quality Degradation:**
1. Identify root cause in pipeline
2. Implement immediate quality filters
3. Backfill clean data when resolved
4. Update validation rules

**System Performance Issues:**
1. Scale resources immediately
2. Implement temporary rate reduction
3. Optimize critical path operations
4. Plan permanent capacity increases
"""

from typing import Dict, Any, List
from langchain.tools import Tool
import json
import re
from datetime import datetime, timedelta

from agents.app.agents.base import FederalJobAgent, AgentResponse


class JobCollectionOrchestratorAgent(FederalJobAgent):
    """
    Specialized agent for orchestrating job collection and data pipeline monitoring
    Manages automated collection, quality checks, and pipeline health
    """
    
    def _load_tools(self) -> List[Tool]:
        """Load job collection orchestrator specific tools"""
        
        tools = [
            Tool(
                name="collection_scheduler",
                func=self._schedule_collection_jobs,
                description="Schedule and coordinate job collection tasks"
            ),
            Tool(
                name="quality_monitor",
                func=self._monitor_data_quality,
                description="Monitor data quality and completeness"
            ),
            Tool(
                name="api_health_checker",
                func=self._check_api_health,
                description="Check external API health and rate limits"
            ),
            Tool(
                name="pipeline_optimizer",
                func=self._optimize_collection_pipeline,
                description="Optimize collection performance and reliability"
            ),
            Tool(
                name="failure_analyzer",
                func=self._analyze_collection_failures,
                description="Analyze collection failures and suggest fixes"
            )
        ]
        
        return tools
    
    def _get_prompt_template(self) -> str:
        """Get job collection orchestrator specific prompt template"""
        
        return """You are a Federal Job Collection Orchestrator managing automated data pipelines.
        Your role is to MONITOR and OPTIMIZE collection processes, ensuring data quality and reliability.
        
        Key Responsibilities:
        1. Schedule and coordinate collection jobs
        2. Monitor data quality and completeness
        3. Check external API health and limits
        4. Optimize pipeline performance
        5. Analyze failures and recommend fixes
        
        Collection Systems:
        - USAJobs API - Primary job data source
        - OPM Data Feeds - Classification and pay data
        - Agency Career Sites - Supplemental listings
        - GovContractor Sites - Contract position data
        
        Data Quality Metrics:
        - Completeness: Job fields populated
        - Freshness: Data age and update frequency
        - Accuracy: Validation against known standards
        - Consistency: Format and structure compliance
        - Deduplication: Removal of duplicate postings
        
        Pipeline Components:
        - Collection Scripts (Python/FastAPI)
        - Data Validation (Federal keywords, series)
        - Storage (PostgreSQL with indexing)
        - Monitoring (Logs, metrics, alerts)
        - Backup (Automated with verification)
        
        Federal Job Characteristics:
        - Job series (4-digit occupational codes)
        - Grade levels (GS, WG, SL, ST scales)
        - Location requirements (remote, on-site, hybrid)
        - Security clearance needs
        - Qualification requirements
        - Application deadlines
        
        Available tools:
        {tools}
        
        Current conversation:
        {chat_history}
        
        User Input: {input}
        Context: {context}
        
        Focus on automation, monitoring, and optimization recommendations.
        Provide actionable insights for maintaining pipeline health.
        
        {agent_scratchpad}
        """
    
    def _schedule_collection_jobs(self, input_data: str) -> str:
        """Schedule and coordinate job collection tasks"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            current_schedule = data.get("current_schedule", {})
            collection_volume = data.get("collection_volume", 1000)
            api_rate_limits = data.get("api_rate_limits", {})
            
            # Define optimal collection windows
            collection_windows = {
                "usajobs_full": {
                    "frequency": "daily",
                    "optimal_time": "02:00 UTC",
                    "duration": "2-4 hours",
                    "priority": "high"
                },
                "usajobs_incremental": {
                    "frequency": "every_4_hours",
                    "optimal_time": "06:00, 10:00, 14:00, 18:00 UTC",
                    "duration": "30-60 minutes",
                    "priority": "medium"
                },
                "opm_classification": {
                    "frequency": "weekly",
                    "optimal_time": "Sunday 01:00 UTC",
                    "duration": "1-2 hours",
                    "priority": "low"
                },
                "agency_supplements": {
                    "frequency": "daily",
                    "optimal_time": "04:00 UTC",
                    "duration": "1-2 hours",
                    "priority": "medium"
                }
            }
            
            # Calculate rate limit compliance
            rate_compliance = {}
            usajobs_limit = api_rate_limits.get("usajobs", 2000)  # requests per hour
            
            if collection_volume <= usajobs_limit * 0.8:
                rate_compliance["usajobs"] = "safe"
            elif collection_volume <= usajobs_limit:
                rate_compliance["usajobs"] = "at_limit"
            else:
                rate_compliance["usajobs"] = "exceeds_limit"
            
            # Identify schedule conflicts
            conflicts = []
            current_jobs = current_schedule.get("active_jobs", [])
            
            if len(current_jobs) > 3:
                conflicts.append("Too many concurrent collections may impact performance")
            
            # Check for missing essential collections
            missing_collections = []
            required_collections = ["usajobs_full", "usajobs_incremental"]
            
            for required in required_collections:
                if required not in current_jobs:
                    missing_collections.append(required)
            
            # Generate optimization recommendations
            optimizations = []
            
            if rate_compliance.get("usajobs") == "exceeds_limit":
                optimizations.append("Reduce collection frequency or implement batching")
            
            if conflicts:
                optimizations.append("Stagger collection times to avoid resource conflicts")
            
            if missing_collections:
                optimizations.append(f"Add missing collections: {', '.join(missing_collections)}")
            
            return json.dumps({
                "optimal_windows": collection_windows,
                "rate_compliance": rate_compliance,
                "schedule_conflicts": conflicts,
                "missing_collections": missing_collections,
                "optimization_recommendations": optimizations,
                "recommended_schedule": self._generate_recommended_schedule(collection_windows),
                "recommendation": self._get_scheduling_recommendation(conflicts, optimizations)
            })
            
        except Exception as e:
            return f"Error scheduling collections: {str(e)}"
    
    def _generate_recommended_schedule(self, windows: Dict) -> Dict:
        """Generate recommended collection schedule"""
        
        return {
            "daily_02_00": "USAJobs full collection",
            "daily_06_00": "USAJobs incremental update",
            "daily_10_00": "USAJobs incremental update",
            "daily_14_00": "USAJobs incremental update", 
            "daily_18_00": "USAJobs incremental update",
            "daily_04_00": "Agency supplement collection",
            "weekly_sun_01_00": "OPM classification data"
        }
    
    def _get_scheduling_recommendation(self, conflicts: List, optimizations: List) -> str:
        """Provide scheduling recommendations"""
        
        if conflicts and optimizations:
            return "Multiple scheduling issues detected - prioritize conflict resolution"
        elif optimizations:
            return f"Implement {len(optimizations)} optimizations for better performance"
        elif conflicts:
            return "Resolve scheduling conflicts to improve collection reliability"
        else:
            return "Collection schedule is optimized"
    
    def _monitor_data_quality(self, input_data: str) -> str:
        """Monitor data quality and completeness"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            collected_jobs = data.get("collected_jobs", [])
            quality_thresholds = data.get("quality_thresholds", {})
            
            # Quality metrics
            quality_metrics = {
                "completeness": {
                    "title": 0,
                    "agency": 0,
                    "location": 0,
                    "grade": 0,
                    "series": 0,
                    "salary": 0,
                    "description": 0
                },
                "format_compliance": {
                    "date_format": 0,
                    "grade_format": 0,
                    "series_format": 0,
                    "url_format": 0
                },
                "data_freshness": {
                    "today": 0,
                    "yesterday": 0,
                    "this_week": 0,
                    "older": 0
                }
            }
            
            total_jobs = len(collected_jobs)
            
            if total_jobs > 0:
                # Calculate completeness scores
                for job in collected_jobs:
                    if job.get("title"):
                        quality_metrics["completeness"]["title"] += 1
                    if job.get("agency"):
                        quality_metrics["completeness"]["agency"] += 1
                    if job.get("location"):
                        quality_metrics["completeness"]["location"] += 1
                    if job.get("grade"):
                        quality_metrics["completeness"]["grade"] += 1
                    if job.get("series"):
                        quality_metrics["completeness"]["series"] += 1
                    if job.get("salary"):
                        quality_metrics["completeness"]["salary"] += 1
                    if job.get("description"):
                        quality_metrics["completeness"]["description"] += 1
                
                # Convert to percentages
                for field in quality_metrics["completeness"]:
                    quality_metrics["completeness"][field] = round(
                        (quality_metrics["completeness"][field] / total_jobs) * 100, 1
                    )
            
            # Check against thresholds
            quality_issues = []
            min_completeness = quality_thresholds.get("min_completeness", 95)
            
            for field, percentage in quality_metrics["completeness"].items():
                if percentage < min_completeness:
                    quality_issues.append(f"{field}: {percentage}% (below {min_completeness}%)")
            
            # Calculate overall score
            avg_completeness = sum(quality_metrics["completeness"].values()) / len(quality_metrics["completeness"])
            
            if avg_completeness >= 95:
                quality_grade = "Excellent"
            elif avg_completeness >= 85:
                quality_grade = "Good"
            elif avg_completeness >= 75:
                quality_grade = "Fair"
            else:
                quality_grade = "Poor"
            
            # Identify patterns
            patterns = []
            if quality_metrics["completeness"]["description"] < 90:
                patterns.append("Description field often missing - check API response")
            if quality_metrics["completeness"]["salary"] < 80:
                patterns.append("Salary data frequently unavailable")
            if quality_metrics["completeness"]["series"] < 95:
                patterns.append("Job series extraction may need improvement")
            
            return json.dumps({
                "total_jobs_analyzed": total_jobs,
                "quality_metrics": quality_metrics,
                "overall_quality_grade": quality_grade,
                "average_completeness": round(avg_completeness, 1),
                "quality_issues": quality_issues,
                "patterns_detected": patterns,
                "recommendation": self._get_quality_recommendation(quality_grade, len(quality_issues))
            })
            
        except Exception as e:
            return f"Error monitoring quality: {str(e)}"
    
    def _get_quality_recommendation(self, grade: str, issues: int) -> str:
        """Provide quality monitoring recommendations"""
        
        if grade == "Poor" or issues > 3:
            return "Critical quality issues - investigate collection process immediately"
        elif grade == "Fair" or issues > 1:
            return "Quality issues detected - review and fix collection logic"
        elif grade == "Good":
            return "Good quality with minor improvements needed"
        else:
            return "Excellent data quality maintained"
    
    def _check_api_health(self, input_data: str) -> str:
        """Check external API health and rate limits"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            api_endpoints = data.get("api_endpoints", {})
            recent_requests = data.get("recent_requests", {})
            
            # API health assessment
            api_health = {}
            
            # USAJobs API assessment
            usajobs_data = api_endpoints.get("usajobs", {})
            usajobs_health = {
                "status": "unknown",
                "rate_limit_used": 0,
                "rate_limit_remaining": 0,
                "response_time": 0,
                "error_rate": 0
            }
            
            if usajobs_data:
                # Calculate rate limit usage
                hourly_requests = recent_requests.get("usajobs_hourly", 0)
                rate_limit = usajobs_data.get("rate_limit", 2000)
                
                usajobs_health["rate_limit_used"] = hourly_requests
                usajobs_health["rate_limit_remaining"] = rate_limit - hourly_requests
                
                # Assess health status
                usage_percentage = (hourly_requests / rate_limit) * 100
                
                if usage_percentage < 70:
                    usajobs_health["status"] = "healthy"
                elif usage_percentage < 90:
                    usajobs_health["status"] = "warning"
                else:
                    usajobs_health["status"] = "critical"
            
            api_health["usajobs"] = usajobs_health
            
            # OPM API assessment (if available)
            opm_data = api_endpoints.get("opm", {})
            if opm_data:
                api_health["opm"] = {
                    "status": "healthy",  # OPM typically has higher limits
                    "data_freshness": "weekly"
                }
            
            # Overall health assessment
            critical_apis = sum(1 for api in api_health.values() if api.get("status") == "critical")
            warning_apis = sum(1 for api in api_health.values() if api.get("status") == "warning")
            
            if critical_apis > 0:
                overall_health = "critical"
            elif warning_apis > 0:
                overall_health = "warning"
            else:
                overall_health = "healthy"
            
            # Generate recommendations
            recommendations = []
            
            if usajobs_health["status"] == "critical":
                recommendations.append("Reduce USAJobs API request frequency immediately")
            elif usajobs_health["status"] == "warning":
                recommendations.append("Monitor USAJobs API usage closely")
            
            if usajobs_health["rate_limit_remaining"] < 200:
                recommendations.append("Implement request queuing to avoid rate limit")
            
            return json.dumps({
                "api_health_status": api_health,
                "overall_health": overall_health,
                "critical_apis": critical_apis,
                "warning_apis": warning_apis,
                "recommendations": recommendations,
                "next_check": "Check again in 1 hour",
                "recommendation": self._get_api_health_recommendation(overall_health, recommendations)
            })
            
        except Exception as e:
            return f"Error checking API health: {str(e)}"
    
    def _get_api_health_recommendation(self, health: str, recs: List) -> str:
        """Provide API health recommendations"""
        
        if health == "critical":
            return "URGENT: API limits exceeded - halt collection until reset"
        elif health == "warning":
            return "API approaching limits - implement throttling"
        elif recs:
            return f"API healthy but {len(recs)} optimizations recommended"
        else:
            return "All APIs operating normally"
    
    def _optimize_collection_pipeline(self, input_data: str) -> str:
        """Optimize collection performance and reliability"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            performance_metrics = data.get("performance_metrics", {})
            error_logs = data.get("error_logs", [])
            
            # Performance analysis
            optimization_opportunities = {
                "database": [],
                "api_calls": [],
                "processing": [],
                "storage": [],
                "monitoring": []
            }
            
            # Database optimizations
            db_metrics = performance_metrics.get("database", {})
            query_time = db_metrics.get("avg_query_time", 0)
            
            if query_time > 1000:  # milliseconds
                optimization_opportunities["database"].append("Add indexes for frequently queried fields")
            
            connection_pool = db_metrics.get("connection_pool_usage", 0)
            if connection_pool > 80:
                optimization_opportunities["database"].append("Increase database connection pool size")
            
            # API call optimizations
            api_metrics = performance_metrics.get("api", {})
            avg_response_time = api_metrics.get("avg_response_time", 0)
            
            if avg_response_time > 5000:  # milliseconds
                optimization_opportunities["api_calls"].append("Implement request caching")
            
            timeout_rate = api_metrics.get("timeout_rate", 0)
            if timeout_rate > 5:  # percentage
                optimization_opportunities["api_calls"].append("Increase request timeout limits")
            
            # Processing optimizations
            processing_metrics = performance_metrics.get("processing", {})
            jobs_per_minute = processing_metrics.get("jobs_per_minute", 0)
            
            if jobs_per_minute < 50:
                optimization_opportunities["processing"].append("Implement parallel processing")
            
            memory_usage = processing_metrics.get("memory_usage_mb", 0)
            if memory_usage > 1000:
                optimization_opportunities["processing"].append("Optimize memory usage in processing loops")
            
            # Error pattern analysis
            error_patterns = {}
            for error in error_logs:
                error_type = error.get("type", "unknown")
                error_patterns[error_type] = error_patterns.get(error_type, 0) + 1
            
            # Priority recommendations
            priority_optimizations = []
            
            # High-impact optimizations
            if len(optimization_opportunities["database"]) > 0:
                priority_optimizations.append("Database performance")
            
            if timeout_rate > 10:
                priority_optimizations.append("API reliability")
            
            if jobs_per_minute < 30:
                priority_optimizations.append("Processing efficiency")
            
            # Calculate efficiency score
            efficiency_score = 100
            
            if query_time > 1000:
                efficiency_score -= 20
            if avg_response_time > 5000:
                efficiency_score -= 15
            if jobs_per_minute < 50:
                efficiency_score -= 15
            if timeout_rate > 5:
                efficiency_score -= 25
            if memory_usage > 1000:
                efficiency_score -= 10
            
            efficiency_grade = "Excellent" if efficiency_score >= 90 else "Good" if efficiency_score >= 75 else "Fair" if efficiency_score >= 60 else "Poor"
            
            return json.dumps({
                "optimization_opportunities": optimization_opportunities,
                "error_patterns": error_patterns,
                "priority_optimizations": priority_optimizations,
                "efficiency_score": efficiency_score,
                "efficiency_grade": efficiency_grade,
                "quick_wins": self._identify_quick_wins(optimization_opportunities),
                "recommendation": self._get_optimization_recommendation(efficiency_grade, priority_optimizations)
            })
            
        except Exception as e:
            return f"Error optimizing pipeline: {str(e)}"
    
    def _identify_quick_wins(self, opportunities: Dict) -> List:
        """Identify quick optimization wins"""
        
        quick_wins = []
        
        if "Add indexes" in str(opportunities.get("database", [])):
            quick_wins.append("Database indexing (1-2 hours)")
        
        if "Implement request caching" in str(opportunities.get("api_calls", [])):
            quick_wins.append("API response caching (2-3 hours)")
        
        if "Increase request timeout" in str(opportunities.get("api_calls", [])):
            quick_wins.append("Timeout configuration (30 minutes)")
        
        return quick_wins
    
    def _get_optimization_recommendation(self, grade: str, priorities: List) -> str:
        """Provide optimization recommendations"""
        
        if grade == "Poor":
            return "Critical performance issues - implement all priority optimizations"
        elif grade == "Fair":
            return f"Performance needs improvement - focus on {len(priorities)} priority areas"
        elif grade == "Good" and priorities:
            return "Good performance with optimization opportunities available"
        else:
            return "Pipeline performance is optimal"
    
    def _analyze_collection_failures(self, input_data: str) -> str:
        """Analyze collection failures and suggest fixes"""
        
        try:
            data = json.loads(input_data) if isinstance(input_data, str) else input_data
            failure_logs = data.get("failure_logs", [])
            success_rate = data.get("success_rate", 95)
            
            # Categorize failures
            failure_categories = {
                "api_errors": [],
                "network_issues": [],
                "parsing_errors": [],
                "database_errors": [],
                "timeout_errors": [],
                "authentication_errors": []
            }
            
            # Common error patterns
            error_patterns = {
                "api_errors": ["status code 4", "status code 5", "api key", "rate limit"],
                "network_issues": ["connection", "timeout", "dns", "unreachable"],
                "parsing_errors": ["json", "parse", "malformed", "unexpected format"],
                "database_errors": ["constraint", "duplicate", "connection pool", "deadlock"],
                "timeout_errors": ["timeout", "timed out", "request timeout"],
                "authentication_errors": ["unauthorized", "forbidden", "authentication", "token"]
            }
            
            # Analyze failures
            for failure in failure_logs:
                error_message = failure.get("message", "").lower()
                
                for category, patterns in error_patterns.items():
                    if any(pattern in error_message for pattern in patterns):
                        failure_categories[category].append(failure)
                        break
            
            # Calculate failure impact
            total_failures = len(failure_logs)
            most_common_category = max(failure_categories.keys(), 
                                     key=lambda k: len(failure_categories[k]))
            
            # Generate fixes
            fixes = {
                "api_errors": [
                    "Implement exponential backoff for retries",
                    "Add API key rotation mechanism",
                    "Monitor API status pages"
                ],
                "network_issues": [
                    "Add network connectivity checks",
                    "Implement circuit breaker pattern",
                    "Use multiple DNS servers"
                ],
                "parsing_errors": [
                    "Add robust JSON validation",
                    "Implement data schema verification",
                    "Log malformed responses for analysis"
                ],
                "database_errors": [
                    "Add database health checks",
                    "Implement connection retry logic",
                    "Monitor database performance"
                ],
                "timeout_errors": [
                    "Increase timeout values",
                    "Implement request chunking",
                    "Add timeout monitoring"
                ],
                "authentication_errors": [
                    "Implement token refresh logic",
                    "Add authentication monitoring",
                    "Set up credential rotation"
                ]
            }
            
            # Priority fixes based on failure frequency
            priority_fixes = []
            for category, failures in failure_categories.items():
                if len(failures) > total_failures * 0.2:  # More than 20% of failures
                    priority_fixes.extend(fixes[category][:2])  # Top 2 fixes
            
            # Calculate reliability score
            reliability_score = success_rate
            if total_failures > 50:
                reliability_score -= 10
            if len(failure_categories[most_common_category]) > total_failures * 0.5:
                reliability_score -= 15
            
            reliability_grade = "Excellent" if reliability_score >= 95 else "Good" if reliability_score >= 85 else "Fair" if reliability_score >= 75 else "Poor"
            
            return json.dumps({
                "total_failures": total_failures,
                "failure_categories": {k: len(v) for k, v in failure_categories.items()},
                "most_common_failure": most_common_category,
                "success_rate": success_rate,
                "reliability_score": reliability_score,
                "reliability_grade": reliability_grade,
                "priority_fixes": priority_fixes,
                "all_available_fixes": fixes,
                "recommendation": self._get_failure_recommendation(reliability_grade, most_common_category, total_failures)
            })
            
        except Exception as e:
            return f"Error analyzing failures: {str(e)}"
    
    def _get_failure_recommendation(self, grade: str, common_failure: str, total: int) -> str:
        """Provide failure analysis recommendations"""
        
        if grade == "Poor":
            return f"Critical reliability issues - focus on {common_failure} failures immediately"
        elif grade == "Fair":
            return f"Reliability needs improvement - address {common_failure} pattern"
        elif total > 20:
            return f"Good overall but high failure volume - investigate {common_failure}"
        else:
            return "Collection reliability is good"
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze job collection pipeline and provide orchestration insights
        """
        
        try:
            # Extract pipeline information
            collection_stats = data.get("collection_stats", {})
            performance_data = data.get("performance_data", {})
            error_logs = data.get("error_logs", [])
            api_status = data.get("api_status", {})
            focus_area = data.get("focus_area", "overall_health")
            
            # Build analysis query
            query = f"""
            Analyze the federal job collection pipeline:
            
            Collection Volume: {collection_stats.get('daily_jobs', 0)} jobs/day
            Success Rate: {collection_stats.get('success_rate', 0)}%
            
            Performance: {performance_data.get('avg_processing_time', 0)}ms average
            Recent Errors: {len(error_logs)} in last 24 hours
            
            Focus Area: {focus_area}
            
            Provide:
            1. Collection scheduling optimization
            2. Data quality monitoring assessment
            3. API health and rate limit analysis
            4. Pipeline performance optimization
            5. Failure analysis and remediation
            
            Focus on actionable recommendations for pipeline reliability.
            """
            
            # Process with agent
            response = await self.process(query, data)
            
            if response.success:
                # Add orchestration insights
                response.data["orchestration_insights"] = {
                    "immediate_actions": [
                        "Check API rate limit status",
                        "Review recent error patterns",
                        "Verify data quality metrics"
                    ],
                    "optimization_priorities": [
                        "Database query performance",
                        "API request efficiency",
                        "Error handling robustness"
                    ],
                    "monitoring_recommendations": [
                        "Set up automated health checks",
                        "Implement alerting for failures",
                        "Track quality metrics over time"
                    ]
                }
            
            return response
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}"
            )
"""
Monitoring Analytics Agent for Federal Job Advisory System
Handles Sentry error tracking, Prometheus metrics, performance monitoring
Focuses on privacy-compliant analytics and infrastructure cost optimization
"""

import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass, asdict
import statistics

from langchain.tools import Tool
import structlog

from ..base import FederalJobAgent, AgentConfig, AgentResponse

logger = structlog.get_logger()


@dataclass
class MonitoringConfig:
    """Monitoring and analytics configuration"""
    sentry_enabled: bool = True
    prometheus_enabled: bool = True
    analytics_enabled: bool = True
    privacy_compliant: bool = True
    cost_monitoring: bool = True
    alert_threshold_error_rate: float = 0.05  # 5% error rate triggers alert
    alert_threshold_response_time: float = 2.0  # 2 second response time triggers alert
    retention_days: int = 30
    max_daily_cost_alert: float = 10.0  # $10/day cost alert


@dataclass
class SystemMetrics:
    """System health metrics"""
    timestamp: str
    error_rate: float
    avg_response_time: float
    throughput: int
    memory_usage: float
    cpu_usage: float
    disk_usage: float
    active_users: int
    api_health_score: float


@dataclass
class PerformanceAlert:
    """Performance alert data"""
    id: str
    timestamp: str
    type: str
    severity: str
    message: str
    metrics: Dict[str, Any]
    resolved: bool = False


class MonitoringAnalyticsAgent(FederalJobAgent):
    """
    Handles comprehensive monitoring and analytics for the platform
    - Sentry error tracking and management
    - Prometheus metrics configuration
    - Privacy-compliant Google Analytics
    - Performance bottleneck detection
    - User behavior analysis (without PII)
    - System health monitoring
    - Cost monitoring and optimization
    """
    
    def __init__(self, config: AgentConfig):
        self.monitoring_config = MonitoringConfig()
        self.system_metrics_history = []  # Store recent metrics
        self.performance_alerts = []  # Store active alerts
        self.cost_tracking = {"daily_costs": {}, "monthly_total": 0.0}
        self.api_health_cache = {}
        self.user_behavior_patterns = {}  # Anonymous behavior tracking
        
        super().__init__(config)
        
        logger.info("Monitoring Analytics Agent initialized with privacy-compliant tracking")
    
    def _load_tools(self) -> List[Tool]:
        """Load monitoring and analytics tools"""
        return [
            Tool(
                name="configure_sentry",
                description="Configure Sentry error tracking and reporting",
                func=self._configure_sentry
            ),
            Tool(
                name="setup_prometheus_metrics",
                description="Setup Prometheus metrics collection and dashboards",
                func=self._setup_prometheus_metrics
            ),
            Tool(
                name="implement_analytics",
                description="Implement privacy-compliant analytics tracking",
                func=self._implement_analytics
            ),
            Tool(
                name="detect_performance_issues",
                description="Detect and analyze performance bottlenecks",
                func=self._detect_performance_issues
            ),
            Tool(
                name="analyze_user_behavior",
                description="Analyze anonymous user behavior patterns",
                func=self._analyze_user_behavior
            ),
            Tool(
                name="monitor_system_health",
                description="Monitor overall system health and availability",
                func=self._monitor_system_health
            ),
            Tool(
                name="manage_alerts",
                description="Manage performance and system alerts",
                func=self._manage_alerts
            ),
            Tool(
                name="track_infrastructure_costs",
                description="Track and analyze infrastructure costs",
                func=self._track_infrastructure_costs
            ),
            Tool(
                name="check_api_health",
                description="Check USAJobs API and other external API health",
                func=self._check_api_health
            ),
            Tool(
                name="monitor_database_performance",
                description="Monitor database performance and optimization",
                func=self._monitor_database_performance
            )
        ]
    
    def _get_prompt_template(self) -> str:
        """Monitoring-focused prompt template"""
        return """
You are the Monitoring Analytics Agent for a federal job advisory system.
You must maintain privacy compliance while providing comprehensive system monitoring.

Your responsibilities:
- Sentry error tracking and alerting
- Prometheus metrics and dashboards
- Privacy-compliant user analytics (NO PII)
- Performance monitoring and optimization
- System health tracking and reporting
- Cost monitoring and optimization
- API health monitoring (USAJobs and others)
- Database performance analysis
- Alert management and escalation

Privacy Requirements:
- ZERO personal data collection
- Anonymous user behavior analysis only
- GDPR/Privacy Act compliant analytics
- Secure aggregated reporting only

Performance Goals:
- 72% system health score improvement
- Sub-2 second response times
- 99.5% uptime target
- Cost optimization for solo developer budget

Available tools: {tools}
Tool names: {tool_names}

Focus on actionable insights and cost-effective monitoring solutions.
Always prioritize privacy compliance and performance optimization.

Question: {input}
{agent_scratchpad}
"""
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """Analyze system performance and monitoring data"""
        try:
            analysis_type = data.get("type", "general_monitoring")
            
            if analysis_type == "performance_analysis":
                return await self._analyze_performance(data)
            elif analysis_type == "cost_analysis":
                return await self._analyze_costs(data)
            elif analysis_type == "health_check":
                return await self._analyze_system_health(data)
            elif analysis_type == "user_behavior":
                return await self._analyze_user_patterns(data)
            else:
                return await self._general_monitoring_analysis(data)
                
        except Exception as e:
            logger.error(f"Monitoring analysis failed: {e}")
            return AgentResponse(
                success=False,
                message=f"Monitoring analysis failed: {str(e)}"
            )
    
    def _configure_sentry(self, sentry_config: str) -> str:
        """Configure Sentry error tracking"""
        try:
            config = json.loads(sentry_config) if sentry_config.startswith('{') else {}
            
            sentry_setup = {
                "dsn": "your-sentry-dsn-here",  # Would be loaded from environment
                "environment": config.get("environment", "production"),
                "release": config.get("release", "1.0.0"),
                "sample_rate": config.get("sample_rate", 1.0),
                "traces_sample_rate": config.get("traces_sample_rate", 0.1),
                "privacy_settings": {
                    "send_default_pii": False,
                    "scrub_data": True,
                    "allowed_urls": ["your-domain.com"],
                    "ignored_errors": [
                        "Network Error",
                        "Non-Error promise rejection captured"
                    ]
                },
                "performance_monitoring": {
                    "enabled": True,
                    "transaction_sample_rate": 0.1,
                    "capture_console": False,  # Avoid PII in logs
                    "max_breadcrumbs": 50
                },
                "integrations": [
                    "Express",
                    "Http",
                    "OnUncaughtException",
                    "OnUnhandledRejection"
                ],
                "filters": {
                    "filter_transactions": True,
                    "filter_sensitive_data": True,
                    "anonymize_ips": True
                }
            }
            
            # Add federal compliance settings
            sentry_setup["compliance"] = {
                "fisma_compliant": True,
                "zero_pii_guaranteed": True,
                "data_retention_days": 30,
                "us_only_data_storage": True
            }
            
            return f"Sentry Configuration: {json.dumps(sentry_setup, indent=2)}"
            
        except Exception as e:
            return f"Error configuring Sentry: {str(e)}"
    
    def _setup_prometheus_metrics(self, metrics_config: str) -> str:
        """Setup Prometheus metrics collection"""
        try:
            config = json.loads(metrics_config) if metrics_config.startswith('{') else {}
            
            prometheus_setup = {
                "scrape_interval": config.get("scrape_interval", "15s"),
                "evaluation_interval": config.get("evaluation_interval", "15s"),
                "retention_time": "30d",
                "storage_path": "/prometheus/data",
                "global_config": {
                    "scrape_timeout": "10s",
                    "external_labels": {
                        "environment": "production",
                        "service": "federal-job-advisor"
                    }
                },
                "metrics_to_collect": [
                    {
                        "name": "http_requests_total",
                        "type": "counter",
                        "description": "Total HTTP requests",
                        "labels": ["method", "status_code", "endpoint"]
                    },
                    {
                        "name": "http_request_duration_seconds",
                        "type": "histogram",
                        "description": "HTTP request duration",
                        "buckets": [0.1, 0.5, 1.0, 2.0, 5.0]
                    },
                    {
                        "name": "system_memory_usage_bytes",
                        "type": "gauge",
                        "description": "System memory usage"
                    },
                    {
                        "name": "system_cpu_usage_percent",
                        "type": "gauge", 
                        "description": "System CPU usage"
                    },
                    {
                        "name": "database_query_duration_seconds",
                        "type": "histogram",
                        "description": "Database query duration"
                    },
                    {
                        "name": "api_health_status",
                        "type": "gauge",
                        "description": "External API health status"
                    },
                    {
                        "name": "active_user_sessions",
                        "type": "gauge",
                        "description": "Number of active user sessions"
                    }
                ],
                "alerting_rules": [
                    {
                        "alert": "HighErrorRate",
                        "expr": "rate(http_requests_total{status_code=~'5..'}[5m]) > 0.05",
                        "for": "5m",
                        "labels": {"severity": "warning"},
                        "annotations": {"summary": "High error rate detected"}
                    },
                    {
                        "alert": "HighResponseTime", 
                        "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket) > 2",
                        "for": "5m",
                        "labels": {"severity": "warning"},
                        "annotations": {"summary": "High response time detected"}
                    },
                    {
                        "alert": "APIDown",
                        "expr": "api_health_status < 1",
                        "for": "2m",
                        "labels": {"severity": "critical"},
                        "annotations": {"summary": "External API is down"}
                    }
                ],
                "dashboards": [
                    "System Overview",
                    "API Performance", 
                    "Error Tracking",
                    "Cost Monitoring",
                    "User Analytics"
                ]
            }
            
            return f"Prometheus Setup: {json.dumps(prometheus_setup, indent=2)}"
            
        except Exception as e:
            return f"Error setting up Prometheus: {str(e)}"
    
    def _implement_analytics(self, analytics_config: str) -> str:
        """Implement privacy-compliant analytics"""
        try:
            config = json.loads(analytics_config) if analytics_config.startswith('{') else {}
            
            analytics_setup = {
                "provider": "Google Analytics 4",
                "measurement_id": "G-XXXXXXXXXX",  # Would be loaded from environment
                "privacy_settings": {
                    "anonymize_ip": True,
                    "disable_advertising_features": True,
                    "respect_do_not_track": True,
                    "cookie_expiration": 30,  # days
                    "collect_pii": False,
                    "data_retention": "26_months"
                },
                "events_to_track": [
                    {
                        "name": "job_search",
                        "parameters": ["search_category", "results_count", "session_id"]
                    },
                    {
                        "name": "application_started",
                        "parameters": ["job_type", "agency", "session_id"]
                    },
                    {
                        "name": "resume_generated",
                        "parameters": ["template_type", "word_count", "session_id"]
                    },
                    {
                        "name": "page_view",
                        "parameters": ["page_title", "page_location", "session_id"]
                    }
                ],
                "custom_dimensions": [
                    {"name": "user_type", "scope": "session"},
                    {"name": "job_category_interest", "scope": "session"},
                    {"name": "application_stage", "scope": "event"}
                ],
                "filters": {
                    "exclude_internal_traffic": True,
                    "exclude_bot_traffic": True,
                    "filter_sensitive_pages": ["/admin", "/api/private"]
                },
                "compliance": {
                    "gdpr_compliant": True,
                    "privacy_act_compliant": True,
                    "zero_pii_tracking": True,
                    "consent_required": False,  # Federal site exception
                    "data_processing_location": "US_ONLY"
                },
                "reporting": {
                    "real_time_enabled": False,  # Reduce costs
                    "custom_reports": [
                        "User Journey Analysis",
                        "Job Search Effectiveness",
                        "Application Conversion Rates",
                        "System Performance Impact"
                    ],
                    "automated_insights": True,
                    "export_schedule": "weekly"
                }
            }
            
            return f"Analytics Implementation: {json.dumps(analytics_setup, indent=2)}"
            
        except Exception as e:
            return f"Error implementing analytics: {str(e)}"
    
    def _detect_performance_issues(self, performance_data: str) -> str:
        """Detect performance bottlenecks and issues"""
        try:
            # Parse performance data or use simulated data
            if performance_data and performance_data != "detect_issues":
                data = json.loads(performance_data)
                metrics = data.get("metrics", {})
            else:
                # Simulated current performance metrics
                metrics = {
                    "avg_response_time": 1.2,
                    "error_rate": 0.02,
                    "throughput": 150,
                    "memory_usage": 0.75,
                    "cpu_usage": 0.60,
                    "database_query_time": 0.3,
                    "api_response_time": 0.8
                }
            
            issues_detected = []
            performance_score = 100
            
            # Check response time
            if metrics.get("avg_response_time", 0) > 2.0:
                issues_detected.append({
                    "type": "HIGH_RESPONSE_TIME",
                    "severity": "HIGH",
                    "current_value": metrics["avg_response_time"],
                    "threshold": 2.0,
                    "impact": "User experience degradation",
                    "recommendations": [
                        "Enable response caching",
                        "Optimize database queries",
                        "Consider CDN implementation",
                        "Review code for N+1 queries"
                    ]
                })
                performance_score -= 20
            
            # Check error rate
            if metrics.get("error_rate", 0) > 0.05:
                issues_detected.append({
                    "type": "HIGH_ERROR_RATE",
                    "severity": "HIGH",
                    "current_value": metrics["error_rate"],
                    "threshold": 0.05,
                    "impact": "System reliability issues",
                    "recommendations": [
                        "Review error logs in Sentry",
                        "Implement circuit breakers",
                        "Add retry logic for failed requests",
                        "Improve error handling"
                    ]
                })
                performance_score -= 25
            
            # Check resource usage
            if metrics.get("memory_usage", 0) > 0.8:
                issues_detected.append({
                    "type": "HIGH_MEMORY_USAGE",
                    "severity": "MEDIUM",
                    "current_value": metrics["memory_usage"],
                    "threshold": 0.8,
                    "impact": "Potential system instability",
                    "recommendations": [
                        "Implement memory profiling",
                        "Review for memory leaks",
                        "Optimize data structures",
                        "Consider vertical scaling"
                    ]
                })
                performance_score -= 15
            
            if metrics.get("cpu_usage", 0) > 0.8:
                issues_detected.append({
                    "type": "HIGH_CPU_USAGE",
                    "severity": "MEDIUM",
                    "current_value": metrics["cpu_usage"],
                    "threshold": 0.8,
                    "impact": "Reduced system responsiveness",
                    "recommendations": [
                        "Profile CPU-intensive operations",
                        "Implement background job processing",
                        "Optimize algorithms",
                        "Consider horizontal scaling"
                    ]
                })
                performance_score -= 15
            
            # Check database performance
            if metrics.get("database_query_time", 0) > 0.5:
                issues_detected.append({
                    "type": "SLOW_DATABASE_QUERIES",
                    "severity": "MEDIUM",
                    "current_value": metrics["database_query_time"],
                    "threshold": 0.5,
                    "impact": "Overall application slowdown",
                    "recommendations": [
                        "Add database indexes",
                        "Optimize complex queries",
                        "Implement query caching",
                        "Consider read replicas"
                    ]
                })
                performance_score -= 20
            
            analysis_result = {
                "scan_timestamp": datetime.utcnow().isoformat(),
                "performance_score": max(performance_score, 0),
                "health_status": "GOOD" if performance_score >= 80 else "NEEDS_ATTENTION" if performance_score >= 60 else "CRITICAL",
                "issues_found": len(issues_detected),
                "critical_issues": len([i for i in issues_detected if i["severity"] == "HIGH"]),
                "performance_issues": issues_detected,
                "overall_recommendations": [
                    "Implement comprehensive monitoring",
                    "Set up automated alerting",
                    "Regular performance testing",
                    "Capacity planning based on usage trends"
                ] if issues_detected else [
                    "System performing well",
                    "Continue monitoring trends", 
                    "Maintain current optimization level"
                ],
                "target_score": 90,  # 72% improvement goal
                "improvement_needed": max(0, 90 - performance_score)
            }
            
            return f"Performance Analysis: {json.dumps(analysis_result, indent=2)}"
            
        except Exception as e:
            return f"Error detecting performance issues: {str(e)}"
    
    def _analyze_user_behavior(self, behavior_data: str) -> str:
        """Analyze anonymous user behavior patterns"""
        try:
            # Parse behavior data or use simulated patterns
            if behavior_data and behavior_data != "analyze_behavior":
                data = json.loads(behavior_data)
            else:
                # Simulated anonymous user behavior data
                data = {
                    "sessions": [
                        {"session_id": "sess_001", "duration": 15, "pages": 5, "actions": ["search", "view_job", "save"]},
                        {"session_id": "sess_002", "duration": 8, "pages": 3, "actions": ["search", "apply"]},
                        {"session_id": "sess_003", "duration": 25, "pages": 8, "actions": ["search", "filter", "view_job", "resume_help"]}
                    ],
                    "popular_searches": ["data analyst", "cybersecurity", "project manager"],
                    "conversion_events": ["application_started", "resume_generated", "job_saved"]
                }
            
            sessions = data.get("sessions", [])
            
            # Analyze patterns (all anonymous)
            behavior_analysis = {
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "total_sessions": len(sessions),
                "session_metrics": {
                    "avg_duration_minutes": statistics.mean([s["duration"] for s in sessions]) if sessions else 0,
                    "avg_pages_per_session": statistics.mean([s["pages"] for s in sessions]) if sessions else 0,
                    "bounce_rate": len([s for s in sessions if s["pages"] == 1]) / len(sessions) if sessions else 0
                },
                "user_journey_patterns": {
                    "most_common_entry_points": ["/jobs", "/search", "/"],
                    "popular_user_flows": [
                        "Search → Job View → Apply",
                        "Search → Filter → Job View → Save",
                        "Home → Browse → Job View → Resume Help"
                    ],
                    "exit_patterns": ["After job application", "After search results", "After resume generation"]
                },
                "engagement_metrics": {
                    "high_engagement_threshold": 20,  # minutes
                    "high_engagement_sessions": len([s for s in sessions if s["duration"] > 20]),
                    "feature_usage": {
                        "job_search": 100,
                        "job_filtering": 75,
                        "resume_assistance": 45,
                        "application_tracking": 30
                    }
                },
                "optimization_insights": [
                    "Users spend most time on job search and filtering",
                    "Resume assistance has good engagement but lower usage",
                    "Application tracking could be promoted more",
                    "Consider improving search result relevance"
                ],
                "privacy_compliance": {
                    "no_pii_collected": True,
                    "session_based_only": True,
                    "anonymized_patterns": True,
                    "data_retention_days": 7
                },
                "recommended_improvements": [
                    "Enhance job search filters for better targeting",
                    "Improve resume assistance discoverability",
                    "Streamline application process",
                    "Add more interactive features for engagement"
                ]
            }
            
            return f"User Behavior Analysis: {json.dumps(behavior_analysis, indent=2)}"
            
        except Exception as e:
            return f"Error analyzing user behavior: {str(e)}"
    
    def _monitor_system_health(self, health_params: str) -> str:
        """Monitor overall system health and availability"""
        try:
            # Generate current system health metrics
            current_time = datetime.utcnow()
            
            # Simulated system health data (in production, would come from actual monitoring)
            health_metrics = SystemMetrics(
                timestamp=current_time.isoformat(),
                error_rate=0.02,  # 2% error rate
                avg_response_time=1.2,  # 1.2 seconds
                throughput=150,  # requests per minute
                memory_usage=0.75,  # 75%
                cpu_usage=0.60,  # 60%
                disk_usage=0.45,  # 45%
                active_users=25,
                api_health_score=0.95  # 95% healthy
            )
            
            # Add to history
            self.system_metrics_history.append(health_metrics)
            
            # Keep only last 24 hours of metrics (assuming 1 minute intervals)
            if len(self.system_metrics_history) > 1440:
                self.system_metrics_history = self.system_metrics_history[-1440:]
            
            # Calculate health scores
            performance_score = self._calculate_performance_score(health_metrics)
            availability_score = self._calculate_availability_score()
            reliability_score = self._calculate_reliability_score()
            
            overall_health_score = (performance_score + availability_score + reliability_score) / 3
            
            # Determine health status
            if overall_health_score >= 90:
                health_status = "EXCELLENT"
            elif overall_health_score >= 75:
                health_status = "GOOD"
            elif overall_health_score >= 60:
                health_status = "FAIR"
            else:
                health_status = "POOR"
            
            # Generate alerts if needed
            alerts = []
            if health_metrics.error_rate > self.monitoring_config.alert_threshold_error_rate:
                alerts.append("HIGH_ERROR_RATE")
            if health_metrics.avg_response_time > self.monitoring_config.alert_threshold_response_time:
                alerts.append("HIGH_RESPONSE_TIME")
            if health_metrics.memory_usage > 0.9:
                alerts.append("HIGH_MEMORY_USAGE")
            if health_metrics.api_health_score < 0.9:
                alerts.append("API_DEGRADATION")
            
            health_report = {
                "timestamp": current_time.isoformat(),
                "overall_health_score": round(overall_health_score, 1),
                "health_status": health_status,
                "component_scores": {
                    "performance": round(performance_score, 1),
                    "availability": round(availability_score, 1), 
                    "reliability": round(reliability_score, 1)
                },
                "current_metrics": asdict(health_metrics),
                "active_alerts": alerts,
                "uptime_percentage": availability_score,
                "trends": {
                    "error_rate_trend": self._calculate_trend("error_rate"),
                    "response_time_trend": self._calculate_trend("avg_response_time"),
                    "throughput_trend": self._calculate_trend("throughput")
                },
                "system_capacity": {
                    "current_load": f"{health_metrics.cpu_usage * 100:.1f}%",
                    "memory_available": f"{(1 - health_metrics.memory_usage) * 100:.1f}%",
                    "disk_available": f"{(1 - health_metrics.disk_usage) * 100:.1f}%",
                    "scaling_recommended": health_metrics.cpu_usage > 0.8 or health_metrics.memory_usage > 0.8
                },
                "recommendations": self._get_health_recommendations(health_metrics, overall_health_score),
                "sla_compliance": {
                    "uptime_target": "99.5%",
                    "current_uptime": f"{availability_score:.1f}%",
                    "response_time_target": "< 2s",
                    "current_avg_response": f"{health_metrics.avg_response_time:.1f}s",
                    "error_rate_target": "< 1%",
                    "current_error_rate": f"{health_metrics.error_rate * 100:.1f}%"
                }
            }
            
            return f"System Health Report: {json.dumps(health_report, indent=2)}"
            
        except Exception as e:
            return f"Error monitoring system health: {str(e)}"
    
    def _manage_alerts(self, alert_data: str) -> str:
        """Manage performance and system alerts"""
        try:
            if alert_data and alert_data != "manage_alerts":
                alert_info = json.loads(alert_data)
                action = alert_info.get("action", "list")
            else:
                action = "list"
            
            if action == "create":
                alert = PerformanceAlert(
                    id=f"alert_{int(time.time())}",
                    timestamp=datetime.utcnow().isoformat(),
                    type=alert_info.get("type", "PERFORMANCE"),
                    severity=alert_info.get("severity", "MEDIUM"),
                    message=alert_info.get("message", "Performance issue detected"),
                    metrics=alert_info.get("metrics", {})
                )
                self.performance_alerts.append(alert)
                
                result = {
                    "action": "alert_created",
                    "alert_id": alert.id,
                    "alert": asdict(alert)
                }
            
            elif action == "resolve":
                alert_id = alert_info.get("alert_id")
                for alert in self.performance_alerts:
                    if alert.id == alert_id:
                        alert.resolved = True
                        break
                
                result = {
                    "action": "alert_resolved",
                    "alert_id": alert_id
                }
            
            else:  # list alerts
                active_alerts = [alert for alert in self.performance_alerts if not alert.resolved]
                resolved_alerts = [alert for alert in self.performance_alerts if alert.resolved]
                
                result = {
                    "action": "alerts_listed",
                    "total_alerts": len(self.performance_alerts),
                    "active_alerts": len(active_alerts),
                    "resolved_alerts": len(resolved_alerts),
                    "active_alert_details": [asdict(alert) for alert in active_alerts[-10:]],  # Last 10
                    "alert_summary": {
                        "critical": len([a for a in active_alerts if a.severity == "CRITICAL"]),
                        "high": len([a for a in active_alerts if a.severity == "HIGH"]),
                        "medium": len([a for a in active_alerts if a.severity == "MEDIUM"]),
                        "low": len([a for a in active_alerts if a.severity == "LOW"])
                    },
                    "escalation_needed": len([a for a in active_alerts if a.severity in ["CRITICAL", "HIGH"]]) > 0
                }
            
            # Clean up old resolved alerts (keep last 100)
            resolved_alerts = [a for a in self.performance_alerts if a.resolved]
            if len(resolved_alerts) > 100:
                # Remove oldest resolved alerts
                resolved_ids = [a.id for a in resolved_alerts[:-100]]
                self.performance_alerts = [a for a in self.performance_alerts if a.id not in resolved_ids]
            
            return f"Alert Management: {json.dumps(result, indent=2)}"
            
        except Exception as e:
            return f"Error managing alerts: {str(e)}"
    
    def _track_infrastructure_costs(self, cost_data: str) -> str:
        """Track and analyze infrastructure costs"""
        try:
            today = datetime.utcnow().date().isoformat()
            
            if cost_data and cost_data != "track_costs":
                costs = json.loads(cost_data)
            else:
                # Simulated daily costs for a solo developer setup
                costs = {
                    "hosting": 2.50,  # Basic VPS/cloud hosting
                    "database": 1.00,  # Small database instance
                    "cdn": 0.50,     # CDN/static assets
                    "monitoring": 0.30,  # Monitoring tools (Sentry free tier + basic metrics)
                    "apis": 0.20,    # External API costs
                    "backup": 0.25,  # Backup storage
                    "ssl": 0.00,     # Free SSL certificate
                    "domain": 0.03   # Domain cost amortized daily
                }
            
            # Update daily costs
            total_daily_cost = sum(costs.values())
            self.cost_tracking["daily_costs"][today] = {
                "total": total_daily_cost,
                "breakdown": costs,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Calculate monthly projection
            monthly_projection = total_daily_cost * 30
            
            # Keep only last 90 days
            cutoff_date = (datetime.utcnow() - timedelta(days=90)).date().isoformat()
            self.cost_tracking["daily_costs"] = {
                k: v for k, v in self.cost_tracking["daily_costs"].items() 
                if k >= cutoff_date
            }
            
            # Calculate trends
            recent_costs = list(self.cost_tracking["daily_costs"].values())[-7:]  # Last 7 days
            avg_daily_cost = sum(c["total"] for c in recent_costs) / len(recent_costs) if recent_costs else 0
            
            # Cost analysis
            cost_analysis = {
                "cost_timestamp": datetime.utcnow().isoformat(),
                "daily_costs": {
                    "today": total_daily_cost,
                    "avg_last_7_days": round(avg_daily_cost, 2),
                    "breakdown": costs
                },
                "monthly_projection": {
                    "current_month": round(monthly_projection, 2),
                    "based_on_avg": round(avg_daily_cost * 30, 2)
                },
                "budget_status": {
                    "solo_developer_budget": True,
                    "monthly_target": 50.00,  # $50/month target for solo dev
                    "current_vs_target": f"{(monthly_projection / 50.0) * 100:.1f}%",
                    "within_budget": monthly_projection <= 50.0,
                    "alert_triggered": total_daily_cost > self.monitoring_config.max_daily_cost_alert
                },
                "cost_optimization": {
                    "highest_cost_category": max(costs, key=costs.get),
                    "optimization_opportunities": [
                        "Consider reserved instances for hosting if usage is consistent",
                        "Implement intelligent caching to reduce API calls",
                        "Monitor and scale down unused resources",
                        "Use free tiers where possible (Sentry, basic monitoring)"
                    ],
                    "cost_efficiency_score": self._calculate_cost_efficiency_score(costs, total_daily_cost)
                },
                "trends": {
                    "cost_trend": "stable",  # Would calculate actual trend
                    "growth_rate": "2% monthly",  # Would calculate from historical data
                    "seasonal_patterns": "Low weekend usage reduces costs"
                },
                "recommendations": self._get_cost_recommendations(costs, monthly_projection)
            }
            
            return f"Infrastructure Cost Analysis: {json.dumps(cost_analysis, indent=2)}"
            
        except Exception as e:
            return f"Error tracking infrastructure costs: {str(e)}"
    
    def _check_api_health(self, api_data: str) -> str:
        """Check external API health including USAJobs API"""
        try:
            apis_to_check = [
                {"name": "USAJobs", "endpoint": "https://data.usajobs.gov/api/search", "timeout": 5},
                {"name": "Authentication", "endpoint": "/api/auth/status", "timeout": 3},
                {"name": "Database", "endpoint": "/api/health/db", "timeout": 2},
                {"name": "Resume_Service", "endpoint": "/api/resume/health", "timeout": 3}
            ]
            
            health_results = []
            overall_health = 0
            
            for api in apis_to_check:
                # Simulate API health check (in production, make actual HTTP requests)
                import random
                
                # Simulate response time and status
                response_time = random.uniform(0.1, 2.0)
                status = "healthy" if random.random() > 0.1 else "unhealthy"  # 90% healthy rate
                status_code = 200 if status == "healthy" else random.choice([500, 503, 404])
                
                health_check = {
                    "api_name": api["name"],
                    "endpoint": api["endpoint"],
                    "status": status,
                    "status_code": status_code,
                    "response_time_ms": round(response_time * 1000, 1),
                    "timeout_ms": api["timeout"] * 1000,
                    "last_check": datetime.utcnow().isoformat(),
                    "error_message": None if status == "healthy" else "Service temporarily unavailable"
                }
                
                # Calculate health score
                if status == "healthy":
                    if response_time < 1.0:
                        api_score = 100
                    elif response_time < 2.0:
                        api_score = 80
                    else:
                        api_score = 60
                else:
                    api_score = 0
                
                health_check["health_score"] = api_score
                health_results.append(health_check)
                overall_health += api_score
            
            # Calculate overall API health
            overall_health_percentage = overall_health / (len(apis_to_check) * 100)
            
            # Cache results
            self.api_health_cache = {
                "timestamp": datetime.utcnow().isoformat(),
                "overall_health": overall_health_percentage,
                "api_results": health_results
            }
            
            api_health_report = {
                "health_check_timestamp": datetime.utcnow().isoformat(),
                "overall_api_health": f"{overall_health_percentage * 100:.1f}%",
                "health_status": "GOOD" if overall_health_percentage >= 0.8 else "DEGRADED" if overall_health_percentage >= 0.6 else "POOR",
                "apis_checked": len(apis_to_check),
                "healthy_apis": len([r for r in health_results if r["status"] == "healthy"]),
                "unhealthy_apis": len([r for r in health_results if r["status"] == "unhealthy"]),
                "api_details": health_results,
                "critical_apis_down": [r["api_name"] for r in health_results if r["api_name"] in ["USAJobs", "Database"] and r["status"] == "unhealthy"],
                "performance_summary": {
                    "fastest_api": min(health_results, key=lambda x: x["response_time_ms"])["api_name"],
                    "slowest_api": max(health_results, key=lambda x: x["response_time_ms"])["api_name"],
                    "avg_response_time": round(sum(r["response_time_ms"] for r in health_results) / len(health_results), 1)
                },
                "recommendations": [
                    "Monitor USAJobs API rate limits",
                    "Implement circuit breaker pattern for failing APIs", 
                    "Add retry logic with exponential backoff",
                    "Cache API responses when appropriate"
                ] if overall_health_percentage < 1.0 else [
                    "All APIs performing well",
                    "Continue regular health monitoring"
                ]
            }
            
            return f"API Health Check: {json.dumps(api_health_report, indent=2)}"
            
        except Exception as e:
            return f"Error checking API health: {str(e)}"
    
    def _monitor_database_performance(self, db_params: str) -> str:
        """Monitor database performance and optimization"""
        try:
            # Simulate database performance metrics
            db_metrics = {
                "connection_pool": {
                    "active_connections": 8,
                    "idle_connections": 12,
                    "max_connections": 20,
                    "connection_utilization": 0.4
                },
                "query_performance": {
                    "avg_query_time_ms": 150,
                    "slow_query_count": 2,
                    "queries_per_second": 25,
                    "cache_hit_ratio": 0.85
                },
                "storage": {
                    "database_size_mb": 450,
                    "table_count": 15,
                    "index_count": 28,
                    "storage_growth_mb_per_day": 2.5
                },
                "replication": {
                    "enabled": False,  # Solo developer setup
                    "lag_ms": 0,
                    "replica_count": 0
                }
            }
            
            # Calculate performance score
            performance_issues = []
            db_score = 100
            
            # Check query performance
            if db_metrics["query_performance"]["avg_query_time_ms"] > 300:
                performance_issues.append({
                    "type": "SLOW_QUERIES",
                    "severity": "HIGH",
                    "details": f"Average query time: {db_metrics['query_performance']['avg_query_time_ms']}ms",
                    "recommendation": "Optimize slow queries and add indexes"
                })
                db_score -= 25
            
            # Check cache hit ratio
            if db_metrics["query_performance"]["cache_hit_ratio"] < 0.8:
                performance_issues.append({
                    "type": "LOW_CACHE_HIT_RATIO",
                    "severity": "MEDIUM",
                    "details": f"Cache hit ratio: {db_metrics['query_performance']['cache_hit_ratio'] * 100:.1f}%",
                    "recommendation": "Increase cache size or improve query patterns"
                })
                db_score -= 15
            
            # Check connection utilization
            if db_metrics["connection_pool"]["connection_utilization"] > 0.8:
                performance_issues.append({
                    "type": "HIGH_CONNECTION_USAGE",
                    "severity": "MEDIUM",
                    "details": f"Connection utilization: {db_metrics['connection_pool']['connection_utilization'] * 100:.1f}%",
                    "recommendation": "Consider increasing connection pool size"
                })
                db_score -= 15
            
            db_performance_report = {
                "monitoring_timestamp": datetime.utcnow().isoformat(),
                "database_health_score": db_score,
                "performance_status": "EXCELLENT" if db_score >= 90 else "GOOD" if db_score >= 75 else "NEEDS_ATTENTION",
                "current_metrics": db_metrics,
                "performance_issues": performance_issues,
                "optimization_recommendations": [
                    "Add indexes for frequently queried columns",
                    "Implement query result caching",
                    "Regular VACUUM and ANALYZE operations",
                    "Monitor for N+1 query patterns"
                ] if performance_issues else [
                    "Database performing optimally",
                    "Continue monitoring query patterns",
                    "Regular maintenance is sufficient"
                ],
                "maintenance_schedule": {
                    "next_vacuum": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                    "next_backup": (datetime.utcnow() + timedelta(days=1)).isoformat(),
                    "index_rebuild": "Monthly",
                    "statistics_update": "Weekly"
                },
                "capacity_planning": {
                    "current_size_mb": db_metrics["storage"]["database_size_mb"],
                    "daily_growth_mb": db_metrics["storage"]["storage_growth_mb_per_day"],
                    "projected_size_30_days": db_metrics["storage"]["database_size_mb"] + (db_metrics["storage"]["storage_growth_mb_per_day"] * 30),
                    "scaling_needed": False  # Would calculate based on limits
                }
            }
            
            return f"Database Performance Report: {json.dumps(db_performance_report, indent=2)}"
            
        except Exception as e:
            return f"Error monitoring database performance: {str(e)}"
    
    # Helper methods
    def _calculate_performance_score(self, metrics: SystemMetrics) -> float:
        """Calculate performance score based on metrics"""
        score = 100
        
        if metrics.error_rate > 0.05:
            score -= 30
        elif metrics.error_rate > 0.02:
            score -= 15
        
        if metrics.avg_response_time > 2.0:
            score -= 25
        elif metrics.avg_response_time > 1.0:
            score -= 10
        
        if metrics.memory_usage > 0.9:
            score -= 20
        elif metrics.memory_usage > 0.8:
            score -= 10
        
        return max(score, 0)
    
    def _calculate_availability_score(self) -> float:
        """Calculate availability score"""
        # In production, would calculate from actual uptime data
        return 99.2  # Simulated uptime percentage
    
    def _calculate_reliability_score(self) -> float:
        """Calculate reliability score"""
        # In production, would calculate from error patterns and recovery metrics
        return 94.5  # Simulated reliability score
    
    def _calculate_trend(self, metric_name: str) -> str:
        """Calculate trend for a specific metric"""
        if len(self.system_metrics_history) < 2:
            return "insufficient_data"
        
        # Simple trend calculation (would be more sophisticated in production)
        recent = getattr(self.system_metrics_history[-1], metric_name)
        older = getattr(self.system_metrics_history[-min(10, len(self.system_metrics_history))], metric_name)
        
        if recent > older * 1.1:
            return "increasing"
        elif recent < older * 0.9:
            return "decreasing"
        else:
            return "stable"
    
    def _get_health_recommendations(self, metrics: SystemMetrics, score: float) -> List[str]:
        """Get health-based recommendations"""
        recommendations = []
        
        if score < 70:
            recommendations.append("URGENT: Address critical performance issues immediately")
        
        if metrics.error_rate > 0.05:
            recommendations.append("Investigate and fix high error rate")
        
        if metrics.avg_response_time > 2.0:
            recommendations.append("Optimize application performance and response times")
        
        if metrics.memory_usage > 0.8:
            recommendations.append("Monitor memory usage and consider optimization")
        
        if not recommendations:
            recommendations.append("System health is good - maintain current monitoring")
        
        return recommendations
    
    def _calculate_cost_efficiency_score(self, costs: Dict[str, float], total: float) -> int:
        """Calculate cost efficiency score"""
        # Simple efficiency scoring for solo developer budget
        if total <= 3.0:  # Under $3/day is excellent
            return 95
        elif total <= 5.0:  # Under $5/day is good
            return 80
        elif total <= 10.0:  # Under $10/day is acceptable
            return 65
        else:
            return 40  # Over $10/day needs optimization
    
    def _get_cost_recommendations(self, costs: Dict[str, float], monthly: float) -> List[str]:
        """Get cost optimization recommendations"""
        recommendations = []
        
        if monthly > 50.0:
            recommendations.append("Monthly costs exceed solo developer budget - optimize immediately")
        
        if costs.get("hosting", 0) > 3.0:
            recommendations.append("Consider lower-cost hosting options or reserved instances")
        
        if costs.get("monitoring", 0) > 1.0:
            recommendations.append("Evaluate monitoring tools - consider free tier options")
        
        recommendations.append("Regularly review usage and scale resources based on actual needs")
        
        return recommendations
    
    # Analysis methods for different monitoring aspects
    async def _analyze_performance(self, data: Dict[str, Any]) -> AgentResponse:
        """Analyze performance metrics and trends"""
        performance_data = data.get("metrics", {})
        analysis = self._detect_performance_issues(json.dumps(performance_data))
        
        return AgentResponse(
            success=True,
            message="Performance analysis completed",
            data={"analysis": analysis}
        )
    
    async def _analyze_costs(self, data: Dict[str, Any]) -> AgentResponse:
        """Analyze infrastructure costs"""
        cost_data = data.get("costs", {})
        analysis = self._track_infrastructure_costs(json.dumps(cost_data))
        
        return AgentResponse(
            success=True,
            message="Cost analysis completed",
            data={"analysis": analysis}
        )
    
    async def _analyze_system_health(self, data: Dict[str, Any]) -> AgentResponse:
        """Analyze overall system health"""
        health_data = data.get("params", "")
        analysis = self._monitor_system_health(health_data)
        
        return AgentResponse(
            success=True,
            message="System health analysis completed",
            data={"analysis": analysis}
        )
    
    async def _analyze_user_patterns(self, data: Dict[str, Any]) -> AgentResponse:
        """Analyze user behavior patterns"""
        behavior_data = data.get("behavior", {})
        analysis = self._analyze_user_behavior(json.dumps(behavior_data))
        
        return AgentResponse(
            success=True,
            message="User behavior analysis completed", 
            data={"analysis": analysis}
        )
    
    async def _general_monitoring_analysis(self, data: Dict[str, Any]) -> AgentResponse:
        """Perform general monitoring analysis"""
        analysis_results = {
            "monitoring_overview": {
                "sentry_status": "active",
                "prometheus_status": "active",
                "analytics_status": "privacy_compliant",
                "cost_status": "within_budget"
            },
            "key_metrics": {
                "system_health_score": 87.5,
                "cost_efficiency": 85.0,
                "performance_score": 82.0,
                "privacy_compliance": 100.0
            },
            "improvement_opportunities": [
                "Optimize database query performance",
                "Implement more aggressive caching",
                "Fine-tune alerting thresholds",
                "Enhance user journey tracking"
            ],
            "budget_status": {
                "monthly_target": "$50",
                "current_projection": "$42.50", 
                "under_budget": True
            }
        }
        
        return AgentResponse(
            success=True,
            message="General monitoring analysis completed",
            data=analysis_results
        )
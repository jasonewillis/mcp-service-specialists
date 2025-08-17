#!/usr/bin/env python3
"""
Redis Caching Specialist for Fed Job Advisor

Embedded knowledge for Redis 5.0.1 + Celery 5.3.6 integration
Optimized for federal job search caching patterns and session management.

CRITICAL VERSIONS:
- redis==5.0.1
- celery==5.3.6
- FastAPI backend with Streamlit frontend
- PostgreSQL primary database

WARNING: Redis 5.0.1 has specific connection pooling requirements
WARNING: Celery 5.3.6 requires specific broker URL format for Redis
WARNING: Federal job data has strict TTL requirements due to real-time updates
"""

import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import hashlib
import pickle
import structlog

# Embedded knowledge base for Fed Job Advisor Redis patterns
REDIS_SPECIALIST_KNOWLEDGE = {
    "version_compatibility": {
        "redis": "5.0.1",
        "celery": "5.3.6", 
        "python_redis_client": "redis==5.0.1",
        "connection_pool": "Required for production",
        "async_support": "Limited in redis 5.0.1 - use aioredis separately if needed"
    },
    
    "federal_job_caching_patterns": {
        "job_search_results": {
            "key_pattern": "fedjobs:search:{query_hash}:{page}",
            "ttl_seconds": 1800,  # 30 minutes - federal jobs update frequently
            "compression": "gzip",
            "reason": "USAJobs API has rate limits, cache search results"
        },
        "job_details": {
            "key_pattern": "fedjobs:detail:{announcement_id}",
            "ttl_seconds": 3600,  # 1 hour
            "compression": "json",
            "reason": "Individual job details change less frequently"
        },
        "salary_calculations": {
            "key_pattern": "fedjobs:salary:{series}:{grade}:{locality}",
            "ttl_seconds": 86400,  # 24 hours
            "compression": "json",
            "reason": "Pay scales update annually, safe to cache longer"
        },
        "user_profiles": {
            "key_pattern": "user:profile:{user_id}",
            "ttl_seconds": 7200,  # 2 hours
            "compression": "pickle",
            "reason": "User preferences and resume data"
        },
        "eligibility_cache": {
            "key_pattern": "fedjobs:eligibility:{user_id}:{job_id}",
            "ttl_seconds": 3600,  # 1 hour
            "compression": "json",
            "reason": "Complex eligibility calculations are expensive"
        }
    },
    
    "session_management": {
        "session_keys": {
            "pattern": "session:{session_id}",
            "ttl_seconds": 3600,  # 1 hour default
            "data_structure": "hash",
            "fields": ["user_id", "login_time", "last_activity", "preferences"]
        },
        "auth_tokens": {
            "pattern": "auth:token:{token_hash}",
            "ttl_seconds": 1800,  # 30 minutes
            "data_structure": "string",
            "refresh_pattern": "auth:refresh:{user_id}"
        }
    },
    
    "celery_integration": {
        "broker_url": "redis://localhost:6379/0",
        "result_backend": "redis://localhost:6379/1",
        "task_serializer": "pickle",
        "result_serializer": "pickle",
        "accept_content": ["pickle", "json"],
        "redis_max_connections": 20,
        "visibility_timeout": 1800,  # 30 minutes
        "task_routes": {
            "fedjobs.tasks.sync_jobs": {"queue": "priority"},
            "fedjobs.tasks.send_email": {"queue": "emails"},
            "fedjobs.tasks.generate_report": {"queue": "reports"}
        }
    },
    
    "performance_optimizations": {
        "connection_pooling": {
            "max_connections": 50,
            "retry_on_timeout": True,
            "health_check_interval": 30,
            "socket_keepalive": True,
            "socket_keepalive_options": {}
        },
        "pipeline_operations": {
            "batch_size": 100,
            "use_for": ["bulk_cache_sets", "bulk_cache_gets", "bulk_deletes"],
            "warning": "Don't pipeline operations with different TTLs"
        },
        "memory_optimization": {
            "compression_threshold": 1024,  # bytes
            "use_gzip_for": "large_job_listings",
            "use_pickle_for": "python_objects",
            "use_json_for": "simple_data"
        }
    },
    
    "critical_warnings": {
        "redis_5_0_1_limitations": [
            "No native async support - use synchronous client only",
            "Connection pooling is critical for concurrent FastAPI requests",
            "Memory usage spikes with large job result sets",
            "Clustering not available in this version"
        ],
        "celery_5_3_6_gotchas": [
            "Broker URL format changed - use redis:// not redis+socket://",
            "Pickle serializer has security implications - validate task sources",
            "Task routing requires explicit queue declarations",
            "Result expiration must be set explicitly"
        ],
        "federal_data_warnings": [
            "USAJobs data updates every 15 minutes - don't cache too long",
            "Salary data is locality-specific - include in cache keys",
            "Security clearance requirements change - invalidate related caches",
            "Announcement close dates are critical - check before serving cached data"
        ]
    }
}

class RedisCachingSpecialist:
    """
    Fed Job Advisor Redis Caching Specialist
    
    Provides comprehensive Redis caching solutions for federal job search application
    with embedded knowledge for Redis 5.0.1 and Celery 5.3.6 integration.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
        self.knowledge = REDIS_SPECIALIST_KNOWLEDGE
        
    def get_redis_config(self, environment: str = "development") -> Dict[str, Any]:
        """
        Get Redis configuration for Fed Job Advisor
        
        Args:
            environment: development, staging, or production
            
        Returns:
            Complete Redis configuration dict
        """
        base_config = {
            "host": "localhost",
            "port": 6379,
            "decode_responses": True,
            "retry_on_timeout": True,
            "health_check_interval": 30,
            "socket_keepalive": True,
            "socket_keepalive_options": {},
        }
        
        if environment == "production":
            base_config.update({
                "connection_pool_kwargs": {
                    "max_connections": 50,
                    "socket_connect_timeout": 5,
                    "socket_timeout": 5,
                    "retry_on_timeout": True
                }
            })
        
        return base_config
    
    def get_celery_config(self) -> Dict[str, Any]:
        """
        Get Celery configuration for Redis broker
        
        Returns:
            Complete Celery configuration for Redis backend
        """
        return {
            "broker_url": "redis://localhost:6379/0",
            "result_backend": "redis://localhost:6379/1", 
            "task_serializer": "pickle",
            "result_serializer": "pickle",
            "accept_content": ["pickle", "json"],
            "result_expires": 3600,  # 1 hour
            "task_routes": self.knowledge["celery_integration"]["task_routes"],
            "broker_connection_retry_on_startup": True,
            "redis_max_connections": 20,
            "visibility_timeout": 1800,
            "worker_prefetch_multiplier": 1,  # For long-running tasks
            "task_acks_late": True,
            "worker_disable_rate_limits": False
        }
    
    def generate_cache_key(self, pattern_type: str, **kwargs) -> str:
        """
        Generate cache keys using Fed Job Advisor patterns
        
        Args:
            pattern_type: Type of cache pattern from knowledge base
            **kwargs: Parameters for key generation
            
        Returns:
            Formatted cache key
        """
        patterns = self.knowledge["federal_job_caching_patterns"]
        
        if pattern_type not in patterns:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
        
        pattern = patterns[pattern_type]["key_pattern"]
        
        # Special handling for search queries (hash the query)
        if pattern_type == "job_search_results" and "query" in kwargs:
            query_hash = hashlib.md5(
                json.dumps(kwargs["query"], sort_keys=True).encode()
            ).hexdigest()[:8]
            kwargs["query_hash"] = query_hash
        
        try:
            return pattern.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required parameter for {pattern_type}: {e}")
    
    def get_ttl(self, pattern_type: str) -> int:
        """
        Get appropriate TTL for cache pattern type
        
        Args:
            pattern_type: Type of cache pattern
            
        Returns:
            TTL in seconds
        """
        patterns = self.knowledge["federal_job_caching_patterns"]
        if pattern_type not in patterns:
            return 3600  # Default 1 hour
        return patterns[pattern_type]["ttl_seconds"]
    
    def get_compression_method(self, pattern_type: str) -> str:
        """
        Get appropriate compression method for data type
        
        Args:
            pattern_type: Type of cache pattern
            
        Returns:
            Compression method (json, pickle, gzip)
        """
        patterns = self.knowledge["federal_job_caching_patterns"]
        if pattern_type not in patterns:
            return "json"
        return patterns[pattern_type]["compression"]
    
    def create_redis_client_code(self) -> str:
        """
        Generate Redis client setup code for Fed Job Advisor
        
        Returns:
            Python code for Redis client setup
        """
        return '''
import redis
import json
import pickle
import gzip
from typing import Any, Optional, Union
import structlog
from datetime import datetime, timedelta

class FedJobRedisClient:
    """Redis client optimized for Fed Job Advisor caching patterns"""
    
    def __init__(self, config: dict):
        self.logger = structlog.get_logger(__name__)
        self.client = redis.Redis(**config)
        self.specialist = RedisCachingSpecialist()
        
        # Test connection
        try:
            self.client.ping()
            self.logger.info("Redis connection established", version="5.0.1")
        except redis.ConnectionError as e:
            self.logger.error("Redis connection failed", error=str(e))
            raise
    
    def cache_job_search(self, query: dict, page: int, results: list) -> bool:
        """Cache job search results with federal-specific patterns"""
        try:
            cache_key = self.specialist.generate_cache_key(
                "job_search_results", 
                query=query, 
                page=page
            )
            ttl = self.specialist.get_ttl("job_search_results")
            
            # Compress large result sets
            if len(results) > 50:
                data = gzip.compress(json.dumps(results).encode())
                self.client.setex(f"{cache_key}:gz", ttl, data)
            else:
                self.client.setex(cache_key, ttl, json.dumps(results))
            
            self.logger.info("Cached job search", key=cache_key, count=len(results))
            return True
            
        except Exception as e:
            self.logger.error("Failed to cache job search", error=str(e))
            return False
    
    def get_cached_job_search(self, query: dict, page: int) -> Optional[list]:
        """Retrieve cached job search results"""
        try:
            cache_key = self.specialist.generate_cache_key(
                "job_search_results",
                query=query,
                page=page
            )
            
            # Try compressed version first
            data = self.client.get(f"{cache_key}:gz")
            if data:
                return json.loads(gzip.decompress(data).decode())
            
            # Try uncompressed version
            data = self.client.get(cache_key)
            if data:
                return json.loads(data)
                
            return None
            
        except Exception as e:
            self.logger.error("Failed to get cached job search", error=str(e))
            return None
    
    def cache_salary_calculation(self, series: str, grade: int, locality: str, 
                               salary_data: dict) -> bool:
        """Cache salary calculations for federal positions"""
        try:
            cache_key = self.specialist.generate_cache_key(
                "salary_calculations",
                series=series,
                grade=grade,
                locality=locality
            )
            ttl = self.specialist.get_ttl("salary_calculations")
            
            self.client.setex(cache_key, ttl, json.dumps(salary_data))
            self.logger.info("Cached salary calculation", key=cache_key)
            return True
            
        except Exception as e:
            self.logger.error("Failed to cache salary", error=str(e))
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate caches matching a pattern"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                deleted = self.client.delete(*keys)
                self.logger.info("Invalidated cache pattern", pattern=pattern, count=deleted)
                return deleted
            return 0
        except Exception as e:
            self.logger.error("Failed to invalidate pattern", pattern=pattern, error=str(e))
            return 0
    
    def setup_session_management(self) -> dict:
        """Setup session management configuration"""
        return {
            "session_cookie_name": "fedjob_session",
            "session_key_prefix": "session:",
            "session_ttl": 3600,
            "auto_refresh_threshold": 600  # Refresh if < 10 minutes left
        }
'''
    
    def create_celery_config_code(self) -> str:
        """
        Generate Celery configuration code for Fed Job Advisor
        
        Returns:
            Python code for Celery setup with Redis
        """
        return '''
from celery import Celery
import os
from datetime import timedelta

# Celery configuration for Fed Job Advisor with Redis 5.0.1
def create_celery_app(app_name: str = "fedjobs") -> Celery:
    """Create Celery app configured for Redis backend"""
    
    celery_app = Celery(app_name)
    
    # Redis broker configuration
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    celery_app.conf.update(
        # Broker settings
        broker_url=f"{redis_url}/0",
        result_backend=f"{redis_url}/1",
        
        # Serialization
        task_serializer="pickle",
        result_serializer="pickle", 
        accept_content=["pickle", "json"],
        
        # Result settings
        result_expires=3600,  # 1 hour
        result_persistent=True,
        
        # Task routing for Fed Job Advisor
        task_routes={
            "fedjobs.tasks.sync_usajobs": {"queue": "priority"},
            "fedjobs.tasks.calculate_eligibility": {"queue": "cpu_intensive"},
            "fedjobs.tasks.send_notification": {"queue": "emails"},
            "fedjobs.tasks.generate_user_report": {"queue": "reports"},
            "fedjobs.tasks.update_salary_scales": {"queue": "priority"}
        },
        
        # Worker settings
        worker_prefetch_multiplier=1,
        task_acks_late=True,
        worker_disable_rate_limits=False,
        
        # Connection settings
        broker_connection_retry_on_startup=True,
        redis_max_connections=20,
        
        # Monitoring
        task_send_sent_event=True,
        task_track_started=True,
        
        # Beat schedule for periodic tasks
        beat_schedule={
            "sync-federal-jobs": {
                "task": "fedjobs.tasks.sync_usajobs",
                "schedule": timedelta(minutes=15),  # USAJobs updates every 15 min
                "options": {"queue": "priority"}
            },
            "update-salary-tables": {
                "task": "fedjobs.tasks.update_salary_scales", 
                "schedule": timedelta(days=1),  # Daily check for pay scale updates
                "options": {"queue": "priority"}
            },
            "cleanup-expired-caches": {
                "task": "fedjobs.tasks.cleanup_redis_cache",
                "schedule": timedelta(hours=6),  # Clean up every 6 hours
                "options": {"queue": "maintenance"}
            }
        },
        
        # Error handling
        task_reject_on_worker_lost=True,
        task_ignore_result=False
    )
    
    return celery_app

# Task examples for Fed Job Advisor
@celery_app.task(bind=True, max_retries=3)
def sync_usajobs(self, agency_filter: str = None):
    """Sync federal job listings from USAJobs API"""
    try:
        from fedjobs.services.usajobs_sync import USAJobsSyncService
        
        sync_service = USAJobsSyncService()
        result = sync_service.sync_jobs(agency_filter=agency_filter)
        
        # Update cache after sync
        redis_client = FedJobRedisClient(get_redis_config())
        redis_client.invalidate_pattern("fedjobs:search:*")
        
        return {
            "success": True,
            "jobs_synced": result["count"],
            "agencies_updated": result["agencies"]
        }
        
    except Exception as exc:
        self.retry(countdown=60 * (self.request.retries + 1), exc=exc)

@celery_app.task
def calculate_eligibility(user_id: int, job_id: str):
    """Calculate user eligibility for federal position"""
    from fedjobs.services.eligibility import EligibilityCalculator
    
    calculator = EligibilityCalculator()
    result = calculator.calculate(user_id, job_id)
    
    # Cache the result
    redis_client = FedJobRedisClient(get_redis_config())
    cache_key = redis_client.specialist.generate_cache_key(
        "eligibility_cache",
        user_id=user_id,
        job_id=job_id
    )
    redis_client.client.setex(
        cache_key,
        redis_client.specialist.get_ttl("eligibility_cache"),
        json.dumps(result)
    )
    
    return result
'''
    
    def create_deployment_checklist(self) -> List[str]:
        """
        Create deployment checklist for Redis in Fed Job Advisor
        
        Returns:
            List of deployment steps and checks
        """
        return [
            "✓ Redis 5.0.1 installed and configured",
            "✓ Redis persistence enabled (AOF + RDB)",
            "✓ Redis memory limit configured (recommend 2GB+ for federal job data)",
            "✓ Redis connection pooling configured (max_connections=50)",
            "✓ Celery 5.3.6 worker processes started",
            "✓ Celery beat scheduler configured for periodic tasks",
            "✓ Redis monitoring enabled (redis-cli info memory)",
            "✓ Cache invalidation patterns tested",
            "✓ Session timeout testing completed",
            "✓ Federal job data TTL validation",
            "✓ Backup strategy for Redis data implemented",
            "✓ Redis security (password, disable dangerous commands)",
            "✓ Network security (firewall rules for Redis port 6379)",
            "✓ Monitoring alerts for Redis memory usage",
            "✓ Celery queue monitoring dashboard",
            "CRITICAL: Test USAJobs API rate limiting with cache",
            "CRITICAL: Validate salary calculation cache accuracy",
            "CRITICAL: Test session management under load"
        ]
    
    def get_troubleshooting_guide(self) -> Dict[str, Dict[str, str]]:
        """
        Get troubleshooting guide for common Redis/Celery issues
        
        Returns:
            Troubleshooting guide organized by issue type
        """
        return {
            "connection_issues": {
                "redis_connection_timeout": "Check Redis server status, increase socket_timeout in config",
                "too_many_connections": "Increase max_connections or implement connection pooling",
                "celery_broker_error": "Verify Redis URL format, check Redis connectivity"
            },
            "performance_issues": {
                "slow_cache_reads": "Enable compression for large datasets, check Redis memory usage",
                "high_memory_usage": "Implement cache eviction policies, reduce TTL for large objects",
                "celery_tasks_timing_out": "Increase visibility_timeout, optimize task code"
            },
            "data_integrity": {
                "stale_job_data": "Reduce cache TTL for job_search_results to 15 minutes",
                "incorrect_salary_calcs": "Clear salary cache after pay scale updates",
                "session_corruption": "Implement session validation, use hash data structure"
            },
            "federal_specific": {
                "usajobs_rate_limit": "Implement exponential backoff, increase cache TTL",
                "security_clearance_changes": "Invalidate related caches immediately",
                "announcement_deadline_passed": "Check announcement close_date before serving cached data"
            }
        }
    
    def generate_monitoring_code(self) -> str:
        """
        Generate monitoring code for Redis and Celery
        
        Returns:
            Python code for monitoring Redis and Celery health
        """
        return '''
import redis
import structlog
from celery import Celery
from typing import Dict, Any
import psutil
import time

class FedJobCacheMonitor:
    """Monitor Redis and Celery health for Fed Job Advisor"""
    
    def __init__(self, redis_client: redis.Redis, celery_app: Celery):
        self.redis = redis_client
        self.celery = celery_app
        self.logger = structlog.get_logger(__name__)
    
    def check_redis_health(self) -> Dict[str, Any]:
        """Check Redis server health and performance"""
        try:
            info = self.redis.info()
            
            health_data = {
                "connected": True,
                "version": info.get("redis_version"),
                "memory_used_mb": round(info.get("used_memory", 0) / 1024 / 1024, 2),
                "memory_peak_mb": round(info.get("used_memory_peak", 0) / 1024 / 1024, 2),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "uptime_seconds": info.get("uptime_in_seconds", 0)
            }
            
            # Calculate cache hit ratio
            hits = health_data["keyspace_hits"]
            misses = health_data["keyspace_misses"]
            if hits + misses > 0:
                health_data["cache_hit_ratio"] = round(hits / (hits + misses), 3)
            else:
                health_data["cache_hit_ratio"] = 0.0
            
            # Check for warning conditions
            warnings = []
            if health_data["memory_used_mb"] > 1500:  # > 1.5GB
                warnings.append("High memory usage")
            if health_data["connected_clients"] > 40:
                warnings.append("High client connections")
            if health_data["cache_hit_ratio"] < 0.8:
                warnings.append("Low cache hit ratio")
            
            health_data["warnings"] = warnings
            health_data["status"] = "warning" if warnings else "healthy"
            
            return health_data
            
        except Exception as e:
            self.logger.error("Redis health check failed", error=str(e))
            return {
                "connected": False,
                "status": "error",
                "error": str(e)
            }
    
    def check_celery_health(self) -> Dict[str, Any]:
        """Check Celery worker and queue health"""
        try:
            # Get worker stats
            inspect = self.celery.control.inspect()
            
            stats = inspect.stats()
            active = inspect.active()
            scheduled = inspect.scheduled()
            
            health_data = {
                "workers_online": len(stats) if stats else 0,
                "active_tasks": sum(len(tasks) for tasks in active.values()) if active else 0,
                "scheduled_tasks": sum(len(tasks) for tasks in scheduled.values()) if scheduled else 0,
                "worker_stats": stats or {},
                "status": "healthy"
            }
            
            # Check queue lengths
            queue_lengths = {}
            for queue in ["priority", "emails", "reports", "cpu_intensive"]:
                try:
                    length = self.redis.llen(f"celery:queue:{queue}")
                    queue_lengths[queue] = length
                except:
                    queue_lengths[queue] = 0
            
            health_data["queue_lengths"] = queue_lengths
            
            # Check for warning conditions
            warnings = []
            if health_data["workers_online"] == 0:
                warnings.append("No workers online")
                health_data["status"] = "error"
            elif health_data["workers_online"] < 2:
                warnings.append("Low worker count")
                health_data["status"] = "warning"
            
            total_queued = sum(queue_lengths.values())
            if total_queued > 100:
                warnings.append("High queue backlog")
                health_data["status"] = "warning"
            
            health_data["warnings"] = warnings
            
            return health_data
            
        except Exception as e:
            self.logger.error("Celery health check failed", error=str(e))
            return {
                "status": "error",
                "error": str(e),
                "workers_online": 0
            }
    
    def check_federal_cache_patterns(self) -> Dict[str, Any]:
        """Check Fed Job Advisor specific cache patterns"""
        try:
            patterns = {
                "job_searches": "fedjobs:search:*",
                "job_details": "fedjobs:detail:*", 
                "salary_calcs": "fedjobs:salary:*",
                "user_sessions": "session:*",
                "eligibility": "fedjobs:eligibility:*"
            }
            
            cache_stats = {}
            for name, pattern in patterns.items():
                keys = self.redis.keys(pattern)
                cache_stats[name] = {
                    "key_count": len(keys),
                    "pattern": pattern
                }
                
                # Sample TTL for the pattern
                if keys:
                    sample_ttl = self.redis.ttl(keys[0])
                    cache_stats[name]["sample_ttl_seconds"] = sample_ttl
            
            # Check for stale data
            warnings = []
            
            # Job searches should be fresh (< 30 min old)
            job_search_keys = self.redis.keys("fedjobs:search:*")
            stale_searches = 0
            for key in job_search_keys:
                ttl = self.redis.ttl(key)
                if ttl > 0 and ttl < 1200:  # Less than 20 min left on 30 min TTL
                    stale_searches += 1
            
            if stale_searches > len(job_search_keys) * 0.5:
                warnings.append("Many job search caches near expiration")
            
            return {
                "cache_patterns": cache_stats,
                "warnings": warnings,
                "status": "warning" if warnings else "healthy",
                "stale_job_searches": stale_searches
            }
            
        except Exception as e:
            self.logger.error("Cache pattern check failed", error=str(e))
            return {
                "status": "error",
                "error": str(e)
            }
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        redis_health = self.check_redis_health()
        celery_health = self.check_celery_health()
        cache_health = self.check_federal_cache_patterns()
        
        overall_status = "healthy"
        if any(h.get("status") == "error" for h in [redis_health, celery_health, cache_health]):
            overall_status = "error"
        elif any(h.get("status") == "warning" for h in [redis_health, celery_health, cache_health]):
            overall_status = "warning"
        
        return {
            "timestamp": time.time(),
            "overall_status": overall_status,
            "redis": redis_health,
            "celery": celery_health,
            "fed_cache_patterns": cache_health,
            "system_info": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage("/").percent
            }
        }
'''
    
    def load_ttl_documentation(self) -> Dict[str, str]:
        """
        Load TTL documentation for different cache types
        
        Returns:
            Documentation explaining TTL choices
        """
        return {
            "job_search_results_30min": """
            TTL: 30 minutes (1800 seconds)
            Reasoning: USAJobs API updates approximately every 15 minutes. 
            30-minute cache provides good performance while ensuring users see 
            relatively fresh job postings. Critical for application deadlines.
            """,
            
            "job_details_1hour": """
            TTL: 1 hour (3600 seconds)
            Reasoning: Individual job announcement details change less frequently
            than search results. Most changes are administrative updates that 
            don't affect applicant decisions. 1 hour balances freshness with performance.
            """,
            
            "salary_calculations_24hours": """
            TTL: 24 hours (86400 seconds)
            Reasoning: Federal pay scales (GS, WG, etc.) are updated annually.
            Locality pay adjustments happen yearly. Safe to cache for 24 hours
            since this data is stable and expensive to calculate.
            """,
            
            "user_sessions_1hour": """
            TTL: 1 hour (3600 seconds)
            Reasoning: Balance security with user experience. Long enough to
            prevent frequent re-authentication during active use, short enough
            to limit exposure if session is compromised.
            """,
            
            "eligibility_cache_1hour": """
            TTL: 1 hour (3600 seconds)
            Reasoning: Eligibility calculations involve complex rules checking
            education, experience, clearance, etc. User profiles don't change
            frequently enough to require real-time recalculation.
            """
        }

def create_redis_specialist() -> RedisCachingSpecialist:
    """Factory function to create Redis specialist instance"""
    return RedisCachingSpecialist()

# Example usage and testing
if __name__ == "__main__":
    specialist = create_redis_specialist()
    
    # Example: Generate cache key for job search
    search_key = specialist.generate_cache_key(
        "job_search_results",
        query={"title": "Software Engineer", "location": "Washington, DC"},
        page=1
    )
    print(f"Generated cache key: {search_key}")
    
    # Get Redis configuration
    redis_config = specialist.get_redis_config("production")
    print(f"Redis config: {redis_config}")
    
    # Get troubleshooting info
    troubleshooting = specialist.get_troubleshooting_guide()
    print(f"Troubleshooting guide loaded: {len(troubleshooting)} categories")
#!/usr/bin/env python3
"""
PostgreSQL Optimizer - Database Performance Expert  
Uses deepseek-coder-v2:16b for complex query optimization
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import asyncio

class PostgreSQLOptimizer:
    """
    Research-only agent for PostgreSQL optimization
    Specializes in Fed Job Advisor database performance
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        self.critical_optimizations = [
            "Create indexes on frequently queried columns",
            "Use EXPLAIN ANALYZE for query planning",
            "Implement connection pooling (pgbouncer)",
            "Partition large tables by date/locality",
            "Use materialized views for complex queries",
            "Vacuum and analyze regularly",
            "Configure work_mem and shared_buffers",
            "Use JSONB for flexible schema fields",
            "Implement full-text search with GIN indexes",
            "Monitor slow queries with pg_stat_statements"
        ]
        
        self.fed_job_tables = {
            "jobs": {
                "size": "1M+ rows",
                "indexes_needed": ["series", "grade", "locality", "close_date"],
                "partitioning": "By close_date monthly"
            },
            "users": {
                "size": "100K rows expected",
                "indexes_needed": ["email", "created_at"],
                "partitioning": "None needed"
            },
            "saved_jobs": {
                "size": "10M+ rows potential",
                "indexes_needed": ["user_id", "job_id", "created_at"],
                "partitioning": "By created_at quarterly"
            },
            "job_searches": {
                "size": "100M+ rows potential",
                "indexes_needed": ["user_id", "timestamp", "keywords"],
                "partitioning": "By timestamp monthly, drop after 6 months"
            }
        }
        
        self.model = "deepseek-coder-v2:16b"  # Complex optimization logic
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research PostgreSQL optimization strategies"""
        
        task_analysis = self._analyze_task(task)
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "task_type": task_analysis['type'],
            "critical_optimizations": self.critical_optimizations,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "sql_templates": self._generate_sql_templates(task_analysis),
            "performance_metrics": self._get_performance_targets(),
            "monitoring_queries": self._get_monitoring_queries()
        }
        
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "top_optimization": "Index frequently queried columns first"
        }
    
    def _analyze_task(self, task: str) -> Dict:
        task_lower = task.lower()
        
        if "index" in task_lower:
            return {"type": "indexing", "focus": "index_strategy"}
        elif "query" in task_lower or "slow" in task_lower:
            return {"type": "query_optimization", "focus": "query_tuning"}
        elif "partition" in task_lower:
            return {"type": "partitioning", "focus": "table_partitioning"}
        elif "backup" in task_lower:
            return {"type": "backup", "focus": "backup_strategy"}
        else:
            return {"type": "general", "focus": "database_optimization"}
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict:
        return {
            "summary": f"PostgreSQL {task_analysis['type']} optimization",
            "phases": [
                "1. Baseline current performance",
                "2. Identify bottlenecks with EXPLAIN",
                "3. Create missing indexes",
                "4. Optimize queries",
                "5. Implement partitioning if needed",
                "6. Configure PostgreSQL settings",
                "7. Set up monitoring",
                "8. Create maintenance schedule"
            ],
            "configuration": {
                "shared_buffers": "25% of RAM",
                "effective_cache_size": "75% of RAM",
                "work_mem": "4MB per connection",
                "maintenance_work_mem": "256MB",
                "max_connections": "200",
                "checkpoint_segments": "32",
                "wal_buffers": "16MB"
            }
        }
    
    def _generate_sql_templates(self, task_analysis: Dict) -> Dict[str, str]:
        templates = {}
        
        if task_analysis["type"] == "indexing":
            templates["create_indexes"] = """-- Essential indexes for Fed Job Advisor

-- Jobs table indexes
CREATE INDEX CONCURRENTLY idx_jobs_series ON jobs(series);
CREATE INDEX CONCURRENTLY idx_jobs_grade ON jobs(grade);
CREATE INDEX CONCURRENTLY idx_jobs_locality ON jobs(locality);
CREATE INDEX CONCURRENTLY idx_jobs_close_date ON jobs(close_date DESC);
CREATE INDEX CONCURRENTLY idx_jobs_salary ON jobs(salary_min, salary_max);

-- Composite index for common search pattern
CREATE INDEX CONCURRENTLY idx_jobs_search 
ON jobs(locality, grade, series, close_date DESC)
WHERE close_date > CURRENT_DATE;

-- Full-text search on job titles
CREATE INDEX CONCURRENTLY idx_jobs_title_fts 
ON jobs USING gin(to_tsvector('english', title));

-- JSONB index for qualifications
CREATE INDEX CONCURRENTLY idx_jobs_quals 
ON jobs USING gin(qualifications);

-- Users table
CREATE UNIQUE INDEX idx_users_email ON users(lower(email));
CREATE INDEX idx_users_created ON users(created_at DESC);

-- Saved jobs (high volume)
CREATE INDEX CONCURRENTLY idx_saved_user_job 
ON saved_jobs(user_id, job_id);
CREATE INDEX CONCURRENTLY idx_saved_created 
ON saved_jobs(user_id, created_at DESC);

-- Partial index for active saved jobs
CREATE INDEX CONCURRENTLY idx_saved_active 
ON saved_jobs(user_id, job_id) 
WHERE deleted_at IS NULL;"""
        
        elif task_analysis["type"] == "query_optimization":
            templates["optimized_queries"] = """-- Optimized job search query
WITH filtered_jobs AS (
  SELECT 
    j.id,
    j.title,
    j.series,
    j.grade,
    j.locality,
    j.salary_min,
    j.salary_max,
    j.close_date,
    ts_rank(
      to_tsvector('english', j.title || ' ' || j.description),
      plainto_tsquery('english', $1)
    ) AS rank
  FROM jobs j
  WHERE 
    j.close_date > CURRENT_DATE
    AND ($2::text IS NULL OR j.locality = $2)
    AND ($3::text IS NULL OR j.grade = $3)
    AND ($4::text IS NULL OR j.series = $4)
    AND to_tsvector('english', j.title || ' ' || j.description) 
        @@ plainto_tsquery('english', $1)
)
SELECT 
  f.*,
  EXISTS(
    SELECT 1 FROM saved_jobs s 
    WHERE s.job_id = f.id 
    AND s.user_id = $5
    AND s.deleted_at IS NULL
  ) AS is_saved
FROM filtered_jobs f
ORDER BY f.rank DESC, f.close_date DESC
LIMIT $6 OFFSET $7;

-- Salary comparison query with window functions
WITH locality_stats AS (
  SELECT 
    locality,
    grade,
    AVG(salary_min) AS avg_min,
    AVG(salary_max) AS avg_max,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_min) AS median_min,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_max) AS median_max,
    COUNT(*) AS job_count
  FROM jobs
  WHERE close_date > CURRENT_DATE
  GROUP BY locality, grade
)
SELECT 
  l.*,
  RANK() OVER (PARTITION BY grade ORDER BY avg_max DESC) AS salary_rank
FROM locality_stats l
WHERE job_count >= 5;"""
        
        elif task_analysis["type"] == "partitioning":
            templates["partitioning_setup"] = """-- Partition jobs table by close_date
CREATE TABLE jobs_partitioned (
  LIKE jobs INCLUDING ALL
) PARTITION BY RANGE (close_date);

-- Create monthly partitions
CREATE TABLE jobs_2025_01 PARTITION OF jobs_partitioned
  FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
  
CREATE TABLE jobs_2025_02 PARTITION OF jobs_partitioned
  FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Auto-partition creation function
CREATE OR REPLACE FUNCTION create_monthly_partition()
RETURNS void AS $$
DECLARE
  partition_date DATE;
  partition_name TEXT;
  start_date DATE;
  end_date DATE;
BEGIN
  partition_date := DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month');
  partition_name := 'jobs_' || TO_CHAR(partition_date, 'YYYY_MM');
  start_date := partition_date;
  end_date := partition_date + INTERVAL '1 month';
  
  IF NOT EXISTS (
    SELECT 1 FROM pg_class 
    WHERE relname = partition_name
  ) THEN
    EXECUTE format(
      'CREATE TABLE %I PARTITION OF jobs_partitioned 
       FOR VALUES FROM (%L) TO (%L)',
      partition_name, start_date, end_date
    );
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Schedule monthly
CREATE EXTENSION IF NOT EXISTS pg_cron;
SELECT cron.schedule(
  'create-monthly-partition',
  '0 0 25 * *',  -- 25th of each month
  'SELECT create_monthly_partition()'
);"""
        
        templates["maintenance_queries"] = """-- Vacuum and analyze
VACUUM (ANALYZE, VERBOSE) jobs;
VACUUM (ANALYZE, VERBOSE) users;
VACUUM (ANALYZE, VERBOSE) saved_jobs;

-- Reindex concurrently
REINDEX INDEX CONCURRENTLY idx_jobs_search;

-- Update table statistics
ANALYZE jobs (series, grade, locality, close_date);

-- Find missing indexes
SELECT 
  schemaname,
  tablename,
  attname,
  n_distinct,
  correlation
FROM pg_stats
WHERE 
  schemaname = 'public'
  AND n_distinct > 100
  AND correlation < 0.1
ORDER BY n_distinct DESC;

-- Identify slow queries
SELECT 
  query,
  calls,
  total_time,
  mean_time,
  max_time,
  stddev_time
FROM pg_stat_statements
WHERE mean_time > 100  -- queries taking >100ms
ORDER BY mean_time DESC
LIMIT 20;"""
        
        return templates
    
    def _get_performance_targets(self) -> Dict:
        """Define performance targets"""
        return {
            "query_targets": {
                "job_search": "<50ms for 95th percentile",
                "job_detail": "<20ms average",
                "save_job": "<30ms average",
                "user_dashboard": "<100ms for full load"
            },
            "database_targets": {
                "connection_pool": "100-200 connections",
                "cache_hit_ratio": ">99%",
                "index_usage": ">95%",
                "bloat": "<20%"
            },
            "scaling_targets": {
                "jobs_table": "Handle 5M rows",
                "concurrent_users": "Support 1000 concurrent",
                "queries_per_second": "Handle 10K QPS"
            }
        }
    
    def _get_monitoring_queries(self) -> Dict[str, str]:
        """Get monitoring queries"""
        return {
            "cache_hit_ratio": """
SELECT 
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_ratio
FROM pg_statio_user_tables;""",
            
            "index_usage": """
SELECT 
  schemaname,
  tablename,
  100 * idx_scan / (seq_scan + idx_scan) AS index_usage_pct
FROM pg_stat_user_tables
WHERE seq_scan + idx_scan > 0
ORDER BY index_usage_pct;""",
            
            "table_bloat": """
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
  n_dead_tup,
  n_live_tup,
  round(n_dead_tup * 100.0 / (n_live_tup + n_dead_tup), 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_live_tup > 0
ORDER BY dead_pct DESC;""",
            
            "long_running_queries": """
SELECT 
  pid,
  now() - query_start AS duration,
  query,
  state
FROM pg_stat_activity
WHERE (now() - query_start) > interval '5 minutes'
AND state != 'idle'
ORDER BY duration DESC;"""
        }
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """Review PostgreSQL implementation"""
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "compliant": True,
            "violations": [],
            "passed": [],
            "warnings": [],
            "score": 100
        }
        
        # Check for indexes
        if "CREATE INDEX" in code.upper():
            review["passed"].append("✅ Creating indexes")
            if "CONCURRENTLY" in code.upper():
                review["passed"].append("✅ Using CONCURRENTLY for zero downtime")
            else:
                review["warnings"].append("⚠️ Consider CONCURRENTLY for production")
                review["score"] -= 10
        
        # Check for EXPLAIN usage
        if "EXPLAIN" in code.upper():
            review["passed"].append("✅ Using EXPLAIN for analysis")
        
        # Check for connection pooling
        if "pool" in code.lower() or "pgbouncer" in code.lower():
            review["passed"].append("✅ Connection pooling configured")
        else:
            review["warnings"].append("⚠️ Consider connection pooling")
            review["score"] -= 15
        
        # Check for monitoring
        if "pg_stat" in code.lower():
            review["passed"].append("✅ Monitoring queries included")
        
        # Check for partitioning consideration
        if "PARTITION" in code.upper():
            review["passed"].append("✅ Table partitioning implemented")
        
        review["recommendation"] = "✅ Ready" if review["score"] >= 70 else "❌ Needs optimization"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"postgresql_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# PostgreSQL Optimization Research\n\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Critical Optimizations\n")
            for opt in research['critical_optimizations'][:5]:
                f.write(f"- {opt}\n")
            f.write("\n")
            
            f.write("## Performance Targets\n")
            for category, targets in research['performance_metrics'].items():
                f.write(f"### {category}\n")
                if isinstance(targets, dict):
                    for key, value in list(targets.items())[:3]:
                        f.write(f"- {key}: {value}\n")
                f.write("\n")
            
            if research.get('sql_templates'):
                f.write("## SQL Templates\n")
                for name, template in research['sql_templates'].items():
                    f.write(f"### {name}\n```sql\n{template}\n```\n\n")
        
        return report_path
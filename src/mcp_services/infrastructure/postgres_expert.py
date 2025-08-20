#!/usr/bin/env python3
"""
PostgreSQL Database Expert - Ultra-deep expertise in PostgreSQL optimization
Specialized for Fed Job Advisor's database patterns and JSONB heavy usage
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio
from enum import Enum

class QueryType(Enum):
    """PostgreSQL query types for analysis"""
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    INDEX = "index"
    VACUUM = "vacuum"
    ANALYZE = "analyze"

class PostgresExpert:
    """
    Ultra-specialized agent for PostgreSQL database optimization
    Complete knowledge of PostgreSQL 15+ for Fed Job Advisor
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "postgresql"
        self.research_output = self.base_path / "research_outputs" / "postgres_optimization"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Exhaustive PostgreSQL knowledge base
        self.knowledge_base = {
            "jsonb_optimization": {
                "indexing": {
                    "gin_index": "CREATE INDEX idx_gin ON table USING gin (jsonb_column)",
                    "gin_path_ops": "CREATE INDEX idx_gin_path ON table USING gin (jsonb_column jsonb_path_ops)",
                    "btree_expression": "CREATE INDEX idx_btree ON table ((jsonb_column->>'field'))",
                    "partial_index": "CREATE INDEX idx_partial ON table ((jsonb_column->>'field')) WHERE jsonb_column->>'status' = 'active'"
                },
                "operators": {
                    "@>": "Contains - jsonb @> '{\"key\": \"value\"}'",
                    "<@": "Is contained by",
                    "?": "Key exists - jsonb ? 'key'",
                    "?&": "All keys exist",
                    "?|": "Any key exists",
                    "->>": "Extract text - jsonb->>'key'",
                    "->": "Extract JSON - jsonb->'key'"
                },
                "functions": {
                    "jsonb_array_elements": "Expand array to rows",
                    "jsonb_each": "Expand object to key-value pairs",
                    "jsonb_extract_path": "Extract nested path",
                    "jsonb_set": "Update nested value",
                    "jsonb_strip_nulls": "Remove null values",
                    "jsonb_pretty": "Format for readability"
                },
                "performance_tips": [
                    "Use GIN indexes for containment queries",
                    "Use btree for specific field lookups",
                    "Avoid large JSONB in frequently updated rows",
                    "Consider JSONB compression with TOAST",
                    "Use jsonb_path_ops for smaller indexes"
                ]
            },
            
            "query_optimization": {
                "explain_analyze": {
                    "usage": "EXPLAIN (ANALYZE, BUFFERS, VERBOSE) query",
                    "key_metrics": ["execution_time", "planning_time", "buffer_hits", "rows_removed"],
                    "red_flags": ["Seq Scan on large tables", "Nested Loop with high cost", "High rows removed by filter"]
                },
                "index_strategies": {
                    "covering_index": "CREATE INDEX idx INCLUDE (column) for index-only scans",
                    "composite_index": "CREATE INDEX idx ON table (col1, col2) - column order matters",
                    "partial_index": "CREATE INDEX idx WHERE condition - smaller, faster",
                    "expression_index": "CREATE INDEX idx ON table (lower(column))",
                    "brin_index": "CREATE INDEX idx USING brin (timestamp) - for large sequential data"
                },
                "join_optimization": {
                    "join_types": ["Hash Join", "Merge Join", "Nested Loop"],
                    "optimization": [
                        "Ensure join columns are indexed",
                        "Update statistics with ANALYZE",
                        "Consider materialized views for complex joins",
                        "Use EXISTS instead of IN for subqueries"
                    ]
                },
                "query_patterns": {
                    "pagination": "Use LIMIT with ORDER BY indexed column",
                    "bulk_insert": "Use COPY or multi-value INSERT",
                    "upsert": "INSERT ON CONFLICT DO UPDATE",
                    "window_functions": "Use for running totals, rankings",
                    "cte": "WITH queries for readability and optimization"
                }
            },
            
            "connection_pooling": {
                "pgbouncer": {
                    "pool_modes": {
                        "session": "Pool connection per session",
                        "transaction": "Pool per transaction (recommended)",
                        "statement": "Pool per statement"
                    },
                    "settings": {
                        "default_pool_size": 25,
                        "max_client_conn": 100,
                        "max_db_connections": 50,
                        "reserve_pool_size": 5
                    }
                },
                "application_pooling": {
                    "asyncpg": {
                        "min_size": 10,
                        "max_size": 20,
                        "max_queries": 50000,
                        "max_inactive_connection_lifetime": 300
                    },
                    "sqlalchemy": {
                        "pool_size": 20,
                        "max_overflow": 40,
                        "pool_timeout": 30,
                        "pool_recycle": 3600
                    }
                }
            },
            
            "performance_tuning": {
                "postgresql_conf": {
                    "shared_buffers": "25% of RAM",
                    "effective_cache_size": "75% of RAM",
                    "maintenance_work_mem": "256MB",
                    "checkpoint_completion_target": 0.9,
                    "wal_buffers": "16MB",
                    "default_statistics_target": 100,
                    "random_page_cost": 1.1,  # For SSD
                    "effective_io_concurrency": 200,  # For SSD
                    "work_mem": "4MB per connection",
                    "max_connections": 100,
                    "autovacuum": "on",
                    "log_statement": "ddl",
                    "log_duration": "off",
                    "log_min_duration_statement": 1000  # Log slow queries
                },
                "monitoring_queries": {
                    "slow_queries": """
                        SELECT query, calls, mean_exec_time, total_exec_time
                        FROM pg_stat_statements
                        ORDER BY mean_exec_time DESC
                        LIMIT 10
                    """,
                    "index_usage": """
                        SELECT schemaname, tablename, indexname, idx_scan
                        FROM pg_stat_user_indexes
                        ORDER BY idx_scan
                    """,
                    "table_bloat": """
                        SELECT schemaname, tablename, 
                               pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
                        FROM pg_stat_user_tables
                        ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
                    """,
                    "cache_hit_ratio": """
                        SELECT sum(heap_blks_hit) / sum(heap_blks_hit + heap_blks_read) as ratio
                        FROM pg_statio_user_tables
                    """
                }
            },
            
            "backup_strategies": {
                "pg_dump": {
                    "full_backup": "pg_dump -Fc -Z9 dbname > backup.dump",
                    "schema_only": "pg_dump -s dbname > schema.sql",
                    "data_only": "pg_dump -a dbname > data.sql",
                    "specific_tables": "pg_dump -t table1 -t table2 dbname",
                    "parallel": "pg_dump -j 4 -Fd dbname -f backup_dir"
                },
                "pg_basebackup": {
                    "streaming": "pg_basebackup -D backup_dir -Ft -z -Xs -P",
                    "wal_archiving": "archive_mode = on",
                    "point_in_time": "recovery_target_time = '2024-01-01 12:00:00'"
                },
                "logical_replication": {
                    "publication": "CREATE PUBLICATION pub FOR ALL TABLES",
                    "subscription": "CREATE SUBSCRIPTION sub CONNECTION 'connstr' PUBLICATION pub"
                }
            },
            
            "migrations": {
                "alembic_patterns": {
                    "safe_migrations": [
                        "Add nullable columns",
                        "Create indexes CONCURRENTLY",
                        "Add constraints NOT VALID then VALIDATE",
                        "Use batched updates for large tables"
                    ],
                    "dangerous_operations": [
                        "ALTER TABLE with ACCESS EXCLUSIVE lock",
                        "REINDEX without CONCURRENTLY",
                        "Adding NOT NULL without default",
                        "Changing column types"
                    ]
                },
                "zero_downtime": {
                    "add_column": "ALTER TABLE ADD COLUMN IF NOT EXISTS",
                    "add_index": "CREATE INDEX CONCURRENTLY",
                    "add_constraint": "ALTER TABLE ADD CONSTRAINT NOT VALID; ALTER TABLE VALIDATE CONSTRAINT",
                    "rename_column": "Use view or application logic during transition"
                }
            },
            
            "fed_job_advisor_specific": {
                "tables": {
                    "jobs": {
                        "size": "10M+ rows",
                        "jsonb_columns": ["job_data", "requirements", "benefits"],
                        "indexes": [
                            "gin (job_data)",
                            "btree (date_posted)",
                            "btree (location)",
                            "gin (job_data jsonb_path_ops)"
                        ]
                    },
                    "users": {
                        "size": "100K+ rows",
                        "jsonb_columns": ["preferences", "resume_data"],
                        "indexes": [
                            "unique (email)",
                            "btree (created_at)",
                            "gin (preferences)"
                        ]
                    },
                    "applications": {
                        "size": "1M+ rows",
                        "partitioning": "By month on created_at",
                        "indexes": [
                            "btree (user_id, created_at)",
                            "btree (job_id)",
                            "btree (status)"
                        ]
                    }
                },
                "common_queries": {
                    "job_search": """
                        SELECT * FROM jobs
                        WHERE job_data @> '{"location": "Washington, DC"}'
                        AND date_posted > NOW() - INTERVAL '30 days'
                        ORDER BY date_posted DESC
                        LIMIT 50
                    """,
                    "user_matches": """
                        SELECT j.* FROM jobs j
                        WHERE j.job_data @> ANY(
                            SELECT preferences->'keywords' FROM users WHERE id = $1
                        )
                    """,
                    "analytics": """
                        WITH daily_stats AS (
                            SELECT DATE(created_at) as day, COUNT(*) as count
                            FROM applications
                            WHERE created_at > NOW() - INTERVAL '30 days'
                            GROUP BY DATE(created_at)
                        )
                        SELECT * FROM daily_stats ORDER BY day
                    """
                }
            }
        }
    
    async def analyze_slow_query(self, query: str, explain_output: str = None) -> Dict[str, Any]:
        """
        Analyze slow PostgreSQL queries and provide optimization recommendations
        """
        timestamp = datetime.now().isoformat()
        
        analysis = {
            "timestamp": timestamp,
            "original_query": query[:1000],
            "issues_detected": [],
            "optimizations": [],
            "recommended_indexes": [],
            "query_rewrite": None
        }
        
        # Detect common performance issues
        query_lower = query.lower()
        
        # Check for missing indexes
        if "seq scan" in (explain_output or "").lower() or "where" in query_lower:
            if "jsonb" in query_lower or "@>" in query or "->>" in query:
                analysis["issues_detected"].append("JSONB query without proper GIN index")
                analysis["recommended_indexes"].append(
                    "CREATE INDEX CONCURRENTLY idx_gin ON table USING gin (jsonb_column)"
                )
            else:
                analysis["issues_detected"].append("Sequential scan on large table")
                analysis["optimizations"].append("Add appropriate indexes on WHERE clause columns")
        
        # Check for SELECT *
        if "select *" in query_lower:
            analysis["issues_detected"].append("SELECT * fetches unnecessary columns")
            analysis["optimizations"].append("Specify only required columns")
        
        # Check for missing LIMIT in searches
        if "order by" in query_lower and "limit" not in query_lower:
            analysis["issues_detected"].append("ORDER BY without LIMIT")
            analysis["optimizations"].append("Add LIMIT clause for pagination")
        
        # Check for IN with subquery
        if " in (" in query_lower and "select" in query_lower:
            analysis["issues_detected"].append("IN with subquery can be slow")
            analysis["optimizations"].append("Consider using EXISTS or JOIN instead")
        
        # Check for LIKE with wildcard prefix
        if "like '%" in query_lower:
            analysis["issues_detected"].append("LIKE with leading wildcard prevents index usage")
            analysis["optimizations"].append("Consider full-text search or trigram indexes")
        
        # Check for missing JOIN conditions
        if "join" in query_lower and "on" not in query_lower:
            analysis["issues_detected"].append("Possible cartesian product from missing JOIN condition")
        
        # JSONB specific optimizations
        if "jsonb" in query_lower:
            if "->>" in query and "@>" not in query:
                analysis["optimizations"].append(
                    "Consider using @> operator for better performance with GIN indexes"
                )
            if "->" in query and query.count("->") > 2:
                analysis["optimizations"].append(
                    "Deep JSONB nesting - consider extracting to columns or materialized view"
                )
        
        # Generate optimized query suggestion
        if analysis["issues_detected"]:
            analysis["query_rewrite"] = self._suggest_query_rewrite(query, analysis["issues_detected"])
        
        # Save analysis
        output_file = self.research_output / f"{timestamp}_query_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return analysis
    
    def _suggest_query_rewrite(self, query: str, issues: List[str]) -> str:
        """Suggest query rewrite based on detected issues"""
        rewritten = query
        
        # Basic rewrites
        if "SELECT * fetches unnecessary columns" in issues:
            rewritten = rewritten.replace("SELECT *", "SELECT /* specify columns */")
        
        if "ORDER BY without LIMIT" in issues:
            if "order by" in rewritten.lower():
                rewritten += "\nLIMIT 100"
        
        return rewritten
    
    async def optimize_database_schema(self, current_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and optimize database schema for Fed Job Advisor
        """
        recommendations = {
            "indexes_to_add": [],
            "indexes_to_remove": [],
            "table_modifications": [],
            "partitioning_suggestions": [],
            "performance_settings": []
        }
        
        # Analyze each table
        for table_name, table_info in current_schema.get("tables", {}).items():
            row_count = table_info.get("row_count", 0)
            
            # Large table optimizations
            if row_count > 1000000:
                recommendations["partitioning_suggestions"].append({
                    "table": table_name,
                    "strategy": "Range partitioning by date",
                    "reason": f"Table has {row_count} rows"
                })
            
            # JSONB column optimizations
            for column in table_info.get("columns", []):
                if column.get("type") == "jsonb":
                    recommendations["indexes_to_add"].append({
                        "table": table_name,
                        "index": f"CREATE INDEX idx_{table_name}_{column['name']}_gin "
                                f"ON {table_name} USING gin ({column['name']})",
                        "reason": "GIN index for JSONB queries"
                    })
            
            # Check for missing primary key
            if not table_info.get("primary_key"):
                recommendations["table_modifications"].append({
                    "table": table_name,
                    "modification": "Add primary key",
                    "suggestion": f"ALTER TABLE {table_name} ADD COLUMN id SERIAL PRIMARY KEY"
                })
        
        # Performance settings based on server specs
        recommendations["performance_settings"] = [
            {"setting": "shared_buffers", "value": "4GB", "reason": "25% of available RAM"},
            {"setting": "effective_cache_size", "value": "12GB", "reason": "75% of available RAM"},
            {"setting": "work_mem", "value": "16MB", "reason": "Optimize for complex queries"},
            {"setting": "maintenance_work_mem", "value": "512MB", "reason": "Speed up maintenance"},
            {"setting": "random_page_cost", "value": "1.1", "reason": "SSD optimization"}
        ]
        
        return recommendations
    
    async def generate_backup_strategy(self) -> str:
        """
        Generate comprehensive PostgreSQL backup strategy for Fed Job Advisor
        """
        strategy = """# PostgreSQL Backup Strategy for Fed Job Advisor

## Backup Schedule

### Daily Backups (Automated)
```bash
# Full logical backup at 2 AM
0 2 * * * pg_dump -Fc -Z9 federal_career_dev > /backups/daily/$(date +\\%Y\\%m\\%d).dump

# Incremental WAL archiving (continuous)
archive_mode = on
archive_command = 'test ! -f /backups/wal/%f && cp %p /backups/wal/%f'
```

### Weekly Backups
```bash
# Full cluster backup on Sundays
0 3 * * 0 pg_basebackup -D /backups/weekly/$(date +\\%Y\\%m\\%d) -Ft -z -Xs -P
```

### Backup Verification
```bash
# Test restore to staging
pg_restore -d staging_db /backups/daily/latest.dump --clean --if-exists

# Verify backup integrity
pg_restore -l backup.dump > /dev/null && echo "Backup valid"
```

## Render.com Specific Configuration

### Automatic Backups
- Render performs automatic daily backups
- 7-day retention for Starter plan
- 30-day retention for Standard plan
- Point-in-time recovery available

### Manual Backup Commands
```bash
# Export from Render database
pg_dump $DATABASE_URL -Fc -Z9 > render_backup.dump

# Download backup
render db:backups:download --service fedjobadvisor-db
```

## Recovery Procedures

### Point-in-Time Recovery
```sql
-- Stop at specific transaction
recovery_target_xid = '1234567'

-- Stop at specific time
recovery_target_time = '2024-01-15 14:00:00'

-- Stop at named restore point
recovery_target_name = 'before_migration'
```

### Disaster Recovery Steps
1. Stop application servers
2. Restore latest backup
3. Apply WAL files to recovery point
4. Verify data integrity
5. Update connection strings
6. Restart application servers

## Backup Storage

### Local Storage
```
/backups/
├── daily/          # 7 days retention
├── weekly/         # 4 weeks retention  
├── monthly/        # 12 months retention
└── wal/           # WAL archives
```

### Cloud Storage (Recommended)
```bash
# Sync to S3
aws s3 sync /backups/ s3://fja-backups/ --delete

# Sync to Google Cloud
gsutil -m rsync -r /backups/ gs://fja-backups/
```

## Monitoring

### Backup Status Check
```sql
-- Check last backup time
SELECT pg_backup_start_time();

-- Check WAL archiving status
SELECT * FROM pg_stat_archiver;

-- Verify replication lag
SELECT pg_last_wal_receive_lsn() - pg_last_wal_replay_lsn() AS lag;
```

### Alerts
- Set up alerts for backup failures
- Monitor backup size growth
- Track restore time metrics

## Best Practices

1. **Test Restores Regularly** - Monthly restore drills
2. **Encrypt Backups** - Use GPG or similar
3. **Offsite Storage** - Keep copies in multiple locations
4. **Document Procedures** - Clear runbooks for recovery
5. **Monitor Backup Size** - Track growth trends
6. **Version Control Schema** - Keep DDL in git

## Recovery Time Objectives

- **RPO (Recovery Point Objective)**: < 1 hour
- **RTO (Recovery Time Objective)**: < 2 hours
- **Backup Window**: 2 AM - 4 AM (low traffic)
- **Retention Policy**: 7 daily, 4 weekly, 12 monthly

---
*Generated by PostgreSQL Expert Agent*
"""
        return strategy
    
    async def analyze_jsonb_usage(self, table_name: str, jsonb_column: str, sample_data: Dict) -> Dict[str, Any]:
        """
        Analyze JSONB usage patterns and recommend optimizations
        """
        analysis = {
            "table": table_name,
            "column": jsonb_column,
            "recommendations": [],
            "indexes": [],
            "query_examples": []
        }
        
        # Analyze data structure
        if isinstance(sample_data, dict):
            # Check nesting depth
            depth = self._get_json_depth(sample_data)
            if depth > 3:
                analysis["recommendations"].append(
                    "Consider extracting deeply nested fields to columns"
                )
            
            # Check for frequently accessed fields
            top_level_keys = list(sample_data.keys())
            if len(top_level_keys) < 10:
                analysis["indexes"].append(
                    f"CREATE INDEX idx_{table_name}_{jsonb_column}_gin "
                    f"ON {table_name} USING gin ({jsonb_column})"
                )
            
            # Specific field indexes
            for key in top_level_keys[:5]:  # Top 5 fields
                analysis["indexes"].append(
                    f"CREATE INDEX idx_{table_name}_{key} "
                    f"ON {table_name} ((({jsonb_column}->>'{{key}}'))"
                )
        
        # Query examples
        analysis["query_examples"] = [
            f"-- Containment query (uses GIN index)\n"
            f"SELECT * FROM {table_name} WHERE {jsonb_column} @> '{{'key': 'value'}}'",
            
            f"-- Key existence (uses GIN index)\n"
            f"SELECT * FROM {table_name} WHERE {jsonb_column} ? 'key'",
            
            f"-- Field extraction (uses btree index if created)\n"
            f"SELECT * FROM {table_name} WHERE {jsonb_column}->>'field' = 'value'",
            
            f"-- Array contains\n"
            f"SELECT * FROM {table_name} WHERE {jsonb_column} @> '[\"value\"]'"
        ]
        
        return analysis
    
    def _get_json_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Calculate JSON nesting depth"""
        if not isinstance(obj, (dict, list)):
            return current_depth
        
        if isinstance(obj, dict):
            return max([self._get_json_depth(v, current_depth + 1) for v in obj.values()] or [current_depth])
        else:
            return max([self._get_json_depth(item, current_depth + 1) for item in obj] or [current_depth])
    
    async def generate_migration_script(self, migration_type: str, details: Dict[str, Any]) -> str:
        """
        Generate safe database migration scripts
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        if migration_type == "add_index":
            script = f"""-- Migration: Add Index
-- Generated: {datetime.now().isoformat()}
-- Safe for production: Yes (CONCURRENTLY)

BEGIN;

-- Create index without blocking writes
CREATE INDEX CONCURRENTLY IF NOT EXISTS {details['index_name']}
ON {details['table']} {details['definition']};

-- Analyze table to update statistics
ANALYZE {details['table']};

COMMIT;

-- Rollback script
-- DROP INDEX CONCURRENTLY IF EXISTS {details['index_name']};
"""
        
        elif migration_type == "add_column":
            script = f"""-- Migration: Add Column
-- Generated: {datetime.now().isoformat()}
-- Safe for production: Yes (nullable column)

BEGIN;

-- Add column without default (no table rewrite)
ALTER TABLE {details['table']} 
ADD COLUMN IF NOT EXISTS {details['column']} {details['type']};

-- Add default in separate transaction if needed
-- ALTER TABLE {details['table']} 
-- ALTER COLUMN {details['column']} SET DEFAULT {details.get('default', 'NULL')};

COMMIT;

-- Rollback script
-- ALTER TABLE {details['table']} DROP COLUMN IF EXISTS {details['column']};
"""
        
        elif migration_type == "partition_table":
            script = f"""-- Migration: Partition Table
-- Generated: {datetime.now().isoformat()}
-- Safe for production: Requires maintenance window

-- Step 1: Create partitioned table
CREATE TABLE {details['table']}_partitioned (
    LIKE {details['table']} INCLUDING ALL
) PARTITION BY RANGE ({details['partition_key']});

-- Step 2: Create partitions
CREATE TABLE {details['table']}_p2024_01 PARTITION OF {details['table']}_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
    
CREATE TABLE {details['table']}_p2024_02 PARTITION OF {details['table']}_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Add more partitions as needed...

-- Step 3: Copy data (can be done in batches)
INSERT INTO {details['table']}_partitioned 
SELECT * FROM {details['table']}
WHERE {details['partition_key']} >= '2024-01-01';

-- Step 4: Swap tables
BEGIN;
ALTER TABLE {details['table']} RENAME TO {details['table']}_old;
ALTER TABLE {details['table']}_partitioned RENAME TO {details['table']};
COMMIT;

-- Step 5: Drop old table after verification
-- DROP TABLE {details['table']}_old;
"""
        
        else:
            script = f"-- Unknown migration type: {migration_type}"
        
        # Save script
        output_file = self.research_output / f"migration_{timestamp}_{migration_type}.sql"
        with open(output_file, 'w') as f:
            f.write(script)
        
        return script

# CLI interface
if __name__ == "__main__":
    import sys
    
    expert = PostgresExpert()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analyze_query":
            if len(sys.argv) > 2:
                query = sys.argv[2]
                result = asyncio.run(expert.analyze_slow_query(query))
                print(json.dumps(result, indent=2))
        
        elif command == "backup_strategy":
            strategy = asyncio.run(expert.generate_backup_strategy())
            print(strategy)
        
        elif command == "migration":
            if len(sys.argv) > 3:
                migration_type = sys.argv[2]
                details = json.loads(sys.argv[3])
                script = asyncio.run(expert.generate_migration_script(migration_type, details))
                print(script)
    else:
        print("PostgreSQL Expert")
        print("Commands:")
        print("  analyze_query <query> - Analyze slow query")
        print("  backup_strategy - Generate backup strategy")
        print("  migration <type> <details> - Generate migration script")
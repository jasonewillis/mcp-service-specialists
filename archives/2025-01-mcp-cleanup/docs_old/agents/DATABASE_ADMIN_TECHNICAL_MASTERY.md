# Database Administrator Agent - Technical Mastery Knowledge Base

**Version**: 1.0  
**Date**: August 19, 2025  
**Purpose**: Technical expertise for Database Administrator MCP agent to research and provide database implementation guidance  
**Usage**: Knowledge base for researching database technologies and providing technical implementation prompts  

---

## 🎯 **TECHNICAL MASTERY: Database Administration Implementation Expertise**

### **Relational Database Management Systems (RDBMS)**

#### **PostgreSQL Mastery**
```yaml
Core PostgreSQL Architecture:
  Process Architecture:
    Postmaster: "Main server process that manages client connections"
    Backend Processes: "Individual processes for each client connection"
    Background Processes: "WAL writer, checkpointer, autovacuum, statistics collector"
    Shared Memory: "Shared buffers, WAL buffers, work_mem"
    
  Storage Architecture:
    Data Files: "Heap files storing table data in 8KB pages"
    WAL (Write-Ahead Logging): "Transaction log for crash recovery and replication"
    TOAST (The Oversized Attribute Storage Technique): "Storage for large values"
    
Advanced PostgreSQL Features:
  MVCC (Multi-Version Concurrency Control):
    Implementation: "Each row has xmin (creation) and xmax (deletion) transaction IDs"
    Visibility Rules: "Transactions see consistent snapshot based on transaction start time"
    Benefits: "Readers don't block writers, writers don't block readers"
    Vacuum Process: "Reclaims dead tuple space, updates visibility map"
    
  Indexing Strategies:
    B-tree Indexes: "Default index type, good for equality and range queries"
    Hash Indexes: "Fast equality lookups, smaller than B-tree"
    GIN (Generalized Inverted Index): "Full-text search, JSON, arrays"
    GiST (Generalized Search Tree): "Geometric data, full-text search"
    SP-GiST (Space-Partitioned GiST): "Non-balanced data structures"
    BRIN (Block Range Indexes): "Large tables with natural ordering"
    
    Implementation Examples:
      # Create various index types
      CREATE INDEX idx_btree ON users(last_name);
      CREATE INDEX idx_gin ON documents USING GIN(content);
      CREATE INDEX idx_gist ON locations USING GiST(coordinates);
      CREATE INDEX idx_partial ON orders(status) WHERE status = 'pending';
      
  Advanced Data Types:
    JSON/JSONB: "Native JSON storage with indexing and query capabilities"
    Arrays: "Multi-dimensional array support with GIN indexing"
    UUID: "Universally unique identifiers with fast generation"
    Geometric Types: "Point, line, circle, polygon with spatial operations"
    Custom Types: "User-defined composite and domain types"
    
    JSON Operations:
      # JSONB queries and indexing
      SELECT data->'user'->>'name' FROM events WHERE data @> '{"type": "login"}';
      CREATE INDEX idx_jsonb_gin ON events USING GIN(data);
      CREATE INDEX idx_jsonb_path ON events USING GIN((data->'user'));

Performance Optimization:
  Query Optimization:
    EXPLAIN ANALYZE: "Detailed execution plan with actual timing"
    Statistics: "pg_stats, ANALYZE command for query planner"
    Configuration: "shared_buffers, work_mem, effective_cache_size"
    
    Query Tuning Examples:
      # Analyze query performance
      EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT * FROM large_table WHERE condition;
      
      # Update statistics
      ANALYZE table_name;
      
      # Check index usage
      SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read 
      FROM pg_stat_user_indexes;
      
  Connection Pooling:
    PgBouncer: "Lightweight connection pooler"
    Connection Pool Types: "Session, transaction, statement pooling"
    Configuration: "pool_mode, max_client_conn, default_pool_size"
    
  Partitioning:
    Declarative Partitioning: "PARTITION BY RANGE, LIST, HASH"
    Partition Pruning: "Automatic elimination of irrelevant partitions"
    Partition-wise Joins: "Efficient joins between partitioned tables"
    
    Implementation:
      # Range partitioning example
      CREATE TABLE sales (id INT, sale_date DATE, amount DECIMAL)
      PARTITION BY RANGE (sale_date);
      
      CREATE TABLE sales_2024 PARTITION OF sales
      FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

#### **MySQL/MariaDB Mastery**
```yaml
MySQL Architecture:
  Storage Engines:
    InnoDB: "Default ACID-compliant engine with row-level locking"
    MyISAM: "Fast table-level locking, no transactions"
    Memory (HEAP): "In-memory storage for temporary data"
    Archive: "Compressed storage for archival data"
    
  InnoDB Specifics:
    Clustered Index: "Primary key determines physical storage order"
    Buffer Pool: "In-memory cache for data and indexes"
    Redo Log: "Circular log for crash recovery"
    Undo Log: "Multi-versioning and rollback support"
    
Performance Features:
  Query Cache: "Caches SELECT statement results (deprecated in 8.0)"
  Index Optimization:
    Covering Indexes: "Include all columns needed in SELECT"
    Prefix Indexes: "Index on first N characters of string column"
    Composite Indexes: "Multi-column indexes with left-prefix rule"
    
    Index Examples:
      # Covering index
      CREATE INDEX idx_covering ON orders(customer_id, order_date, status, total);
      
      # Prefix index for strings
      CREATE INDEX idx_email_prefix ON users(email(20));
      
      # Composite index strategy
      CREATE INDEX idx_composite ON logs(date, level, application);

Replication and High Availability:
  Master-Slave Replication:
    Binary Log: "Records all changes for replication"
    Relay Log: "Slave copies and applies master's binary log"
    GTID (Global Transaction Identifier): "Unique transaction identification"
    
  Master-Master Replication:
    Active-Active: "Both servers accept writes"
    Conflict Resolution: "auto_increment_increment and auto_increment_offset"
    
  Group Replication:
    Multi-Master: "All nodes can accept writes"
    Consensus: "Based on Paxos algorithm"
    Conflict Detection: "First committer wins rule"

Storage and Optimization:
  InnoDB Configuration:
    innodb_buffer_pool_size: "Usually 70-80% of available RAM"
    innodb_log_file_size: "25% of buffer pool size"
    innodb_flush_log_at_trx_commit: "1 for ACID compliance, 2 for performance"
    
  Partitioning:
    Range Partitioning: "PARTITION BY RANGE(column)"
    Hash Partitioning: "PARTITION BY HASH(column)"
    List Partitioning: "PARTITION BY LIST(column)"
    Key Partitioning: "PARTITION BY KEY(column)"
    
    Example Implementation:
      CREATE TABLE sales (
          id INT AUTO_INCREMENT,
          sale_date DATE,
          amount DECIMAL(10,2),
          PRIMARY KEY (id, sale_date)
      )
      PARTITION BY RANGE (YEAR(sale_date)) (
          PARTITION p2023 VALUES LESS THAN (2024),
          PARTITION p2024 VALUES LESS THAN (2025),
          PARTITION p2025 VALUES LESS THAN (2026)
      );
```

#### **Oracle Database Mastery**
```yaml
Oracle Architecture:
  Instance Components:
    SGA (System Global Area): "Shared memory structures"
    - Buffer Cache: "Caches data blocks from datafiles"
    - Shared Pool: "SQL statements, PL/SQL code, data dictionary"
    - Redo Log Buffer: "Transaction changes before writing to disk"
    - Large Pool: "Backup operations, parallel query operations"
    
    Background Processes:
    - SMON (System Monitor): "Instance recovery, space management"
    - PMON (Process Monitor): "Cleans up failed user processes"
    - LGWR (Log Writer): "Writes redo log buffer to disk"
    - DBWR (Database Writer): "Writes dirty buffers to datafiles"
    - CKPT (Checkpoint): "Updates datafile headers with checkpoint info"

Advanced Oracle Features:
  Real Application Clusters (RAC):
    Cluster Architecture: "Multiple instances access single database"
    Cache Fusion: "Shared cache across cluster nodes"
    Services: "Workload management and connection routing"
    
  Partitioning Options:
    Range Partitioning: "Based on value ranges"
    Hash Partitioning: "Even distribution across partitions"
    List Partitioning: "Based on discrete values"
    Composite Partitioning: "Combination of methods (range-hash, range-list)"
    
    Advanced Partitioning:
      # Interval partitioning (automatic partition creation)
      CREATE TABLE sales (
          sale_id NUMBER,
          sale_date DATE,
          amount NUMBER
      )
      PARTITION BY RANGE (sale_date)
      INTERVAL(NUMTOYMINTERVAL(1, 'MONTH'))
      (PARTITION p1 VALUES LESS THAN (DATE '2024-01-01'));

  Performance Features:
    Automatic Workload Repository (AWR): "Performance statistics collection"
    SQL Tuning Advisor: "Automatic SQL statement optimization"
    Automatic Database Diagnostic Monitor (ADDM): "Performance analysis"
    
    PL/SQL Optimization:
      # Bulk operations for performance
      DECLARE
        TYPE num_array IS TABLE OF NUMBER;
        v_ids num_array;
      BEGIN
        SELECT id BULK COLLECT INTO v_ids FROM source_table;
        FORALL i IN v_ids.FIRST..v_ids.LAST
          UPDATE target_table SET status = 'processed' WHERE id = v_ids(i);
      END;

Oracle-Specific SQL Features:
  Hierarchical Queries:
    CONNECT BY: "Tree traversal in SQL"
    START WITH: "Root node specification"
    PRIOR: "Parent-child relationship"
    
    Example:
      SELECT employee_id, manager_id, LEVEL, SYS_CONNECT_BY_PATH(name, '/') path
      FROM employees
      START WITH manager_id IS NULL
      CONNECT BY PRIOR employee_id = manager_id;
      
  Analytic Functions:
    Window Functions: "ROW_NUMBER(), RANK(), LAG(), LEAD()"
    Partitioning: "PARTITION BY for grouping"
    Ordering: "ORDER BY within partitions"
    
    Examples:
      # Running totals
      SELECT date, amount, SUM(amount) OVER (ORDER BY date) running_total
      FROM sales;
      
      # Ranking within groups
      SELECT department, salary, RANK() OVER (PARTITION BY department ORDER BY salary DESC) rank
      FROM employees;
```

### **NoSQL Database Technologies**

#### **MongoDB Mastery**
```yaml
Document Model:
  BSON (Binary JSON): "Extended JSON with additional data types"
  Document Structure: "Flexible schema with nested documents and arrays"
  Collection: "Group of documents (equivalent to table)"
  Database: "Container for collections"
  
Data Modeling:
  Embedding vs Referencing:
    Embedding: "Store related data in single document"
    Referencing: "Store references to other documents"
    Decision Factors: "Query patterns, data size, update frequency"
    
  Schema Design Patterns:
    One-to-Few: "Embed child documents in parent"
    One-to-Many: "Reference pattern with child documents"
    One-to-Squillions: "Parent references in child documents"
    
    Example Models:
      # Embedded model (One-to-Few)
      {
        "_id": ObjectId("..."),
        "name": "John Doe",
        "addresses": [
          {"type": "home", "street": "123 Main St", "city": "Boston"},
          {"type": "work", "street": "456 Oak Ave", "city": "Boston"}
        ]
      }
      
      # Referenced model (One-to-Many)
      # User document
      {"_id": ObjectId("user1"), "name": "John Doe"}
      
      # Order documents
      {"_id": ObjectId("order1"), "user_id": ObjectId("user1"), "total": 100}
      {"_id": ObjectId("order2"), "user_id": ObjectId("user1"), "total": 150}

Indexing Strategy:
  Index Types:
    Single Field: "db.collection.createIndex({field: 1})"
    Compound: "db.collection.createIndex({field1: 1, field2: -1})"
    Multikey: "Automatically created for array fields"
    Text: "db.collection.createIndex({field: 'text'})"
    Geospatial: "2d and 2dsphere indexes for location data"
    
  Index Optimization:
    ESR Rule: "Equality, Sort, Range for compound indexes"
    Index Intersection: "MongoDB can use multiple single-field indexes"
    Covered Queries: "Query results from index alone"
    
    Performance Examples:
      # Create compound index following ESR rule
      db.orders.createIndex({status: 1, date: 1, amount: 1});
      
      # Text search index
      db.articles.createIndex({title: "text", content: "text"});
      db.articles.find({$text: {$search: "mongodb database"}});

Aggregation Framework:
  Pipeline Stages:
    $match: "Filter documents (equivalent to WHERE)"
    $group: "Group documents and perform calculations"
    $project: "Select/transform fields"
    $sort: "Order documents"
    $limit/$skip: "Pagination"
    $lookup: "Left outer join with other collections"
    
  Advanced Aggregations:
    # Complex aggregation pipeline
    db.orders.aggregate([
      {$match: {date: {$gte: ISODate("2024-01-01")}}},
      {$lookup: {
        from: "customers",
        localField: "customer_id",
        foreignField: "_id",
        as: "customer"
      }},
      {$unwind: "$customer"},
      {$group: {
        _id: "$customer.region",
        totalSales: {$sum: "$amount"},
        avgOrderValue: {$avg: "$amount"},
        orderCount: {$sum: 1}
      }},
      {$sort: {totalSales: -1}}
    ]);

Replication and Sharding:
  Replica Sets:
    Primary Node: "Accepts all write operations"
    Secondary Nodes: "Replicate data from primary"
    Arbiter: "Participates in elections but doesn't hold data"
    
  Sharding:
    Shard Key: "Field used to distribute documents"
    Config Servers: "Store cluster metadata"
    Query Router (mongos): "Routes queries to appropriate shards"
    
    Shard Key Selection:
      # Good shard key characteristics
      - High cardinality (many unique values)
      - Even distribution
      - Query isolation (queries target single shard)
      
      # Examples
      sh.shardCollection("mydb.users", {"user_id": "hashed"});  // Hash-based
      sh.shardCollection("mydb.logs", {"date": 1, "server": 1}); // Range-based
```

#### **Redis Mastery**
```yaml
Data Structures:
  String: "Basic key-value, can store text or binary data up to 512MB"
  Hash: "Field-value pairs, ideal for objects"
  List: "Ordered collection, supports push/pop operations"
  Set: "Unordered unique elements, supports set operations"
  Sorted Set (ZSet): "Ordered by score, supports range operations"
  
Advanced Data Types:
  Bitmaps: "Bit operations on strings"
  HyperLogLog: "Probabilistic cardinality estimation"
  Geospatial: "Location-based data with radius queries"
  Streams: "Log-like data structure for event sourcing"
  
  Implementation Examples:
    # String operations
    SET user:1000:name "John Doe"
    GET user:1000:name
    INCR user:1000:visits
    
    # Hash operations (user object)
    HSET user:1001 name "Jane Smith" email "jane@example.com" age 30
    HGET user:1001 name
    HGETALL user:1001
    
    # List operations (queues)
    LPUSH queue:tasks "process-payment"
    RPOP queue:tasks
    LLEN queue:tasks
    
    # Set operations
    SADD user:1000:interests "programming" "databases" "redis"
    SISMEMBER user:1000:interests "programming"
    SINTER user:1000:interests user:1001:interests
    
    # Sorted set (leaderboards)
    ZADD leaderboard 1000 "player1" 1200 "player2" 800 "player3"
    ZRANGE leaderboard 0 -1 WITHSCORES
    ZREVRANK leaderboard "player2"

Persistence Options:
  RDB (Redis Database):
    Snapshot: "Point-in-time snapshot of dataset"
    Configuration: "save 900 1" (save if at least 1 key changed in 900 seconds)
    Benefits: "Compact, fast restart, good for backups"
    
  AOF (Append Only File):
    Log: "Logs every write operation"
    Rewrite: "Periodically rewrites AOF to reduce size"
    Sync Options: "always, everysec, no (OS controlled)"
    Benefits: "Durability, readable format, automatic rewrite"
    
  Hybrid Approach:
    RDB + AOF: "Use both for maximum data safety"
    Recovery: "Redis loads RDB then replays AOF"

Caching Patterns:
  Cache-Aside (Lazy Loading):
    Read: "Check cache, if miss then load from DB and cache"
    Write: "Update DB, then invalidate cache"
    
    Implementation:
      def get_user(user_id):
          # Try cache first
          user = redis.get(f"user:{user_id}")
          if user:
              return json.loads(user)
          
          # Cache miss - load from database
          user = db.get_user(user_id)
          redis.setex(f"user:{user_id}", 3600, json.dumps(user))
          return user
          
  Write-Through:
    Write: "Update cache and database simultaneously"
    Read: "Always read from cache"
    
  Write-Behind (Write-Back):
    Write: "Update cache immediately, update DB asynchronously"
    Benefits: "Low latency writes, batch database updates"

Redis Cluster:
  Architecture:
    Hash Slots: "16384 slots distributed across nodes"
    Consistent Hashing: "Keys mapped to slots using CRC16"
    Master-Slave: "Each master has replica nodes"
    
  Operations:
    # Cluster setup commands
    redis-cli --cluster create node1:6379 node2:6379 node3:6379 \
                             node4:6379 node5:6379 node6:6379 \
                             --cluster-replicas 1
    
    # Check cluster status
    redis-cli -c -h node1 -p 6379 cluster nodes
    redis-cli -c -h node1 -p 6379 cluster info
```

### **Database Design and Architecture**

#### **Normalization and Schema Design**
```yaml
Normal Forms:
  First Normal Form (1NF):
    Requirements: "Atomic values, no repeating groups"
    Example Violation: "phone_numbers: '555-1234, 555-5678'"
    Solution: "Separate phone_numbers table with foreign key"
    
  Second Normal Form (2NF):
    Requirements: "1NF + no partial dependencies on composite primary key"
    Example Violation: "order_details(order_id, product_id, product_name, quantity)"
    Solution: "product_name depends only on product_id, move to products table"
    
  Third Normal Form (3NF):
    Requirements: "2NF + no transitive dependencies"
    Example Violation: "employees(id, department_id, department_name)"
    Solution: "department_name depends on department_id, move to departments table"
    
  Boyce-Codd Normal Form (BCNF):
    Requirements: "3NF + every determinant is a candidate key"
    Stronger version of 3NF that eliminates all anomalies
    
Denormalization Strategies:
  When to Denormalize:
    Performance Requirements: "Read-heavy workloads with complex joins"
    Data Warehouse: "Analytical queries benefit from denormalized structures"
    Caching: "Precomputed aggregations and summaries"
    
  Techniques:
    Materialized Views: "Precomputed join results with automatic refresh"
    Redundant Columns: "Store calculated fields to avoid computation"
    Summary Tables: "Aggregate data for reporting"
    
    Example:
      # Denormalized customer order summary
      CREATE TABLE customer_summary (
          customer_id INT PRIMARY KEY,
          customer_name VARCHAR(255),
          total_orders INT,
          total_spent DECIMAL(10,2),
          last_order_date DATE,
          avg_order_value DECIMAL(10,2)
      );
      
      # Maintained by triggers or scheduled jobs
      CREATE OR REPLACE FUNCTION update_customer_summary()
      RETURNS TRIGGER AS $$
      BEGIN
          -- Update summary when orders change
          UPDATE customer_summary SET
              total_orders = (SELECT COUNT(*) FROM orders WHERE customer_id = NEW.customer_id),
              total_spent = (SELECT COALESCE(SUM(total), 0) FROM orders WHERE customer_id = NEW.customer_id),
              last_order_date = (SELECT MAX(order_date) FROM orders WHERE customer_id = NEW.customer_id)
          WHERE customer_id = NEW.customer_id;
          
          RETURN NEW;
      END;
      $$ LANGUAGE plpgsql;
```

#### **Data Modeling Patterns**
```yaml
Entity Relationship Patterns:
  One-to-One (1:1):
    Example: "User -> UserProfile"
    Implementation: "Foreign key in either table or separate table"
    Use Cases: "Extending entities, security separation"
    
  One-to-Many (1:N):
    Example: "Customer -> Orders"
    Implementation: "Foreign key in many-side table"
    Most Common: "Foundation of relational design"
    
  Many-to-Many (M:N):
    Example: "Students -> Courses"
    Implementation: "Junction/bridge table with foreign keys"
    Extended: "Junction table can have additional attributes"
    
    Example Implementation:
      # Many-to-many with additional attributes
      CREATE TABLE student_course_enrollment (
          student_id INT REFERENCES students(id),
          course_id INT REFERENCES courses(id),
          enrollment_date DATE,
          grade CHAR(1),
          credits_earned INT,
          PRIMARY KEY (student_id, course_id)
      );

Temporal Data Patterns:
  Effective Dating:
    Pattern: "effective_from and effective_to dates"
    Use Case: "Historical data tracking, price changes"
    
    Example:
      CREATE TABLE product_prices (
          product_id INT,
          price DECIMAL(10,2),
          effective_from DATE,
          effective_to DATE,
          PRIMARY KEY (product_id, effective_from)
      );
      
      # Query current price
      SELECT price FROM product_prices 
      WHERE product_id = 1 
        AND CURRENT_DATE BETWEEN effective_from AND effective_to;
        
  Event Sourcing:
    Pattern: "Store events instead of current state"
    Benefits: "Complete audit trail, replay capability, temporal queries"
    
    Example:
      CREATE TABLE account_events (
          event_id SERIAL PRIMARY KEY,
          account_id INT,
          event_type VARCHAR(50),
          amount DECIMAL(10,2),
          timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          metadata JSONB
      );
      
      # Calculate current balance
      SELECT account_id, SUM(amount) as balance
      FROM account_events 
      WHERE account_id = 123
      GROUP BY account_id;

Hierarchical Data Patterns:
  Adjacency List:
    Pattern: "parent_id column pointing to same table"
    Benefits: "Simple structure, easy updates"
    Drawbacks: "Recursive queries needed for deep hierarchies"
    
  Nested Sets:
    Pattern: "left and right values define hierarchy"
    Benefits: "Efficient subtree queries"
    Drawbacks: "Complex updates, tree modifications expensive"
    
  Path Enumeration:
    Pattern: "Store full path as string (e.g., '/1/3/7/')"
    Benefits: "Simple queries, easy to understand"
    Drawbacks: "Path length limitations, string operations"
    
  Closure Table:
    Pattern: "Separate table storing all ancestor-descendant pairs"
    Benefits: "Flexible, supports complex queries"
    Drawbacks: "Storage overhead, maintenance complexity"
    
    Example:
      # Adjacency list
      CREATE TABLE categories (
          id INT PRIMARY KEY,
          name VARCHAR(255),
          parent_id INT REFERENCES categories(id)
      );
      
      # Closure table
      CREATE TABLE category_paths (
          ancestor_id INT REFERENCES categories(id),
          descendant_id INT REFERENCES categories(id),
          path_length INT,
          PRIMARY KEY (ancestor_id, descendant_id)
      );
```

### **Performance Optimization and Tuning**

#### **Query Optimization Techniques**
```yaml
Index Strategy:
  Index Selection:
    Selectivity: "Choose columns with high selectivity (many unique values)"
    Query Patterns: "Index columns frequently used in WHERE, JOIN, ORDER BY"
    Composite Indexes: "Multi-column indexes for complex queries"
    
  Index Types and Usage:
    B-tree: "Default for equality and range queries"
    Hash: "Equality queries only, not range"
    Bitmap: "Low-cardinality columns (Oracle, PostgreSQL)"
    Functional: "Index on expressions or function results"
    
    Optimization Examples:
      # Bad: Function in WHERE clause prevents index usage
      SELECT * FROM orders WHERE YEAR(order_date) = 2024;
      
      # Good: Range query uses index
      SELECT * FROM orders WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';
      
      # Functional index for common patterns
      CREATE INDEX idx_orders_year ON orders(EXTRACT(YEAR FROM order_date));

Query Rewriting:
  Subquery Optimization:
    EXISTS vs IN: "EXISTS often more efficient for large subqueries"
    Correlated Subqueries: "Consider JOINs instead"
    
    Examples:
      # Potentially inefficient IN
      SELECT * FROM customers WHERE id IN (SELECT customer_id FROM orders WHERE total > 1000);
      
      # More efficient EXISTS
      SELECT * FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.total > 1000);
      
      # JOIN version (often fastest)
      SELECT DISTINCT c.* FROM customers c INNER JOIN orders o ON c.id = o.customer_id WHERE o.total > 1000;
      
  Window Functions vs Self-Joins:
    Running Totals: "Window functions eliminate self-joins"
    Ranking: "ROW_NUMBER(), RANK(), DENSE_RANK()"
    
    Example:
      # Instead of complex self-join for running total
      SELECT date, amount, 
             SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) as running_total
      FROM sales
      ORDER BY date;

Execution Plan Analysis:
  PostgreSQL EXPLAIN:
    EXPLAIN ANALYZE: "Actual execution times and row counts"
    Key Metrics: "Cost, rows, width, actual time"
    
    # Detailed analysis
    EXPLAIN (ANALYZE true, BUFFERS true, FORMAT json) 
    SELECT * FROM large_table WHERE indexed_column = 'value';
    
  MySQL EXPLAIN:
    EXPLAIN FORMAT=JSON: "Detailed execution plan"
    Key Fields: "select_type, table, type, key, rows, Extra"
    
  Oracle Execution Plans:
    EXPLAIN PLAN: "Generate execution plan"
    DBMS_XPLAN: "Display formatted plans"
    
    # Oracle plan analysis
    EXPLAIN PLAN FOR SELECT * FROM employees WHERE department_id = 10;
    SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

#### **Database Monitoring and Maintenance**
```yaml
Performance Monitoring:
  Key Metrics:
    Query Performance: "Response time, throughput, slow query log"
    Resource Utilization: "CPU, memory, disk I/O, network"
    Connection Metrics: "Active connections, connection pool usage"
    Lock Contention: "Lock waits, deadlocks, blocking queries"
    
  Monitoring Tools:
    PostgreSQL:
      pg_stat_statements: "Query statistics extension"
      pg_stat_activity: "Current database activity"
      pg_locks: "Lock information"
      
      # Top slow queries
      SELECT query, calls, total_time, mean_time, stddev_time
      FROM pg_stat_statements 
      ORDER BY total_time DESC 
      LIMIT 10;
      
    MySQL:
      Performance Schema: "Comprehensive performance data"
      sys Schema: "Simplified views of Performance Schema"
      Slow Query Log: "Queries exceeding long_query_time"
      
      # MySQL performance monitoring
      SELECT schema_name, digest_text, count_star, avg_timer_wait/1000000000 as avg_ms
      FROM performance_schema.events_statements_summary_by_digest 
      ORDER BY avg_timer_wait DESC 
      LIMIT 10;

Database Maintenance:
  PostgreSQL Maintenance:
    VACUUM: "Reclaim dead tuple space, update statistics"
    ANALYZE: "Update table statistics for query planner"
    REINDEX: "Rebuild indexes to remove bloat"
    
    Automated Maintenance:
      # Configure autovacuum
      ALTER TABLE large_table SET (autovacuum_vacuum_threshold = 1000);
      ALTER TABLE large_table SET (autovacuum_analyze_threshold = 500);
      
  MySQL Maintenance:
    OPTIMIZE TABLE: "Reclaim space and defragment"
    ANALYZE TABLE: "Update index statistics"
    CHECKSUM TABLE: "Verify table integrity"
    
  Index Maintenance:
    Index Rebuild: "Oracle: ALTER INDEX REBUILD"
    Statistics Update: "Keep query optimizer statistics current"
    Fragmentation Check: "Monitor and address index fragmentation"

Backup and Recovery:
  Backup Strategies:
    Full Backup: "Complete database backup"
    Incremental: "Changes since last backup"
    Differential: "Changes since last full backup"
    Transaction Log: "Point-in-time recovery capability"
    
  PostgreSQL Backup:
    pg_dump: "Logical backup of database or specific objects"
    pg_basebackup: "Physical backup of entire cluster"
    WAL-E/WAL-G: "Continuous archiving with cloud storage"
    
    # Automated backup script
    pg_dump -h localhost -U postgres -Fc database_name > backup_$(date +%Y%m%d_%H%M%S).dump
    
  MySQL Backup:
    mysqldump: "Logical backup with SQL statements"
    MySQL Enterprise Backup: "Physical hot backup"
    Binary Log: "Point-in-time recovery"
    
    # Consistent backup with binlog position
    mysqldump --single-transaction --master-data=2 --all-databases > full_backup.sql
```

---

## 🎯 **Agent Implementation Guidance**

### **How This Technical Mastery Enhances Agent Performance**

#### **Database Technology Research**
- **Platform Expertise**: Deep knowledge of PostgreSQL, MySQL, Oracle, MongoDB, Redis architectures
- **Performance Optimization**: Advanced techniques for query tuning, indexing, and system optimization
- **Design Patterns**: Comprehensive understanding of data modeling and schema design approaches
- **Implementation Guidance**: Specific code examples and configuration recommendations

#### **Problem-Solving Approach**
- **Database Selection**: Expert guidance on choosing appropriate database technology for specific use cases
- **Performance Diagnosis**: Advanced techniques for identifying and resolving performance issues
- **Scalability Planning**: Knowledge of partitioning, replication, and clustering strategies
- **Best Practices**: Industry standards for backup, recovery, monitoring, and maintenance

### **Agent Usage Instructions**

#### **When to Apply This Technical Knowledge**
```python
# Example usage in agent decision-making
if database_type == "postgresql" and performance_issue == "slow_queries":
    analyze_query_execution_plans()
    recommend_index_optimization_strategies()
    suggest_configuration_tuning()
    
if use_case == "high_throughput" and data_type == "document":
    compare_mongodb_vs_postgresql_jsonb()
    recommend_sharding_strategies()
    provide_performance_benchmarking_approach()
    
if scaling_challenge == "read_heavy_workload":
    recommend_read_replica_setup()
    suggest_caching_layer_implementation()
    provide_load_balancing_strategies()
```

#### **Research Output Enhancement**
All Database Administrator agent research should include:
- **Specific database platform recommendations** with technical justifications
- **Performance optimization strategies** with concrete implementation examples
- **Architecture design patterns** tailored to specific use cases and requirements
- **Configuration and tuning guidance** with parameter recommendations
- **Monitoring and maintenance procedures** with specific tools and techniques

---

*This technical mastery knowledge base transforms the Database Administrator Agent from general database guidance to deep technical expertise, enabling sophisticated research and implementation recommendations for database architecture, performance optimization, and system administration challenges.*

**© 2025 Fed Job Advisor - Database Administrator Agent Technical Mastery Enhancement**
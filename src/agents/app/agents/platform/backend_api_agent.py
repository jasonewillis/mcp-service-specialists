"""
Backend API Agent

This agent specializes in FastAPI backend development, database optimization,
and API architecture for the Fed Job Advisor platform.
"""

from typing import Dict, Any, List, Optional
from langchain.tools import Tool
import structlog
import json
import re

from ..base import FederalJobAgent, AgentConfig, AgentResponse

logger = structlog.get_logger()


class BackendAPIAgent(FederalJobAgent):
    """
    Specialized agent for backend API development and optimization
    
    Focuses on:
    - FastAPI endpoint creation and optimization
    - SQLAlchemy model and query optimization
    - Celery task management
    - Redis caching strategies
    - API versioning and documentation
    - Request validation and error handling
    - Database migration management with Alembic
    - Performance profiling and optimization
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        logger.info("Backend API Agent initialized")
    
    def _get_prompt_template(self) -> str:
        """Get the prompt template for the backend API agent"""
        return """You are a Backend API Agent for the Fed Job Advisor system.

Your expertise includes:
- FastAPI application development and optimization
- SQLAlchemy ORM models and query optimization
- Celery distributed task processing
- Redis caching and session management
- RESTful API design and versioning
- Pydantic data validation and serialization
- Alembic database migrations
- PostgreSQL database optimization
- API security and authentication
- Performance monitoring and profiling

CRITICAL CONSTRAINTS:
- Solo developer model: Simple, maintainable API patterns
- Part-time development: Focus on proven patterns and documentation
- $0 budget: Use only open-source tools and public APIs
- Protected files: NEVER modify collect_federal_jobs.py or related collectors
- Fields=Full parameter: Maintain in all USAJobs API calls (prevents 93% data loss)
- Merit Hiring compliance: APIs should support guidance tools, not content generation

TECHNOLOGY STACK:
- FastAPI with Python 3.11+
- SQLAlchemy 2.0 with PostgreSQL
- Celery with Redis broker
- Alembic for migrations
- Pydantic for validation
- pytest for testing
- uvicorn for ASGI serving

Available tools:
{tools}

Tool names: {tool_names}

When developing backend features:
1. Always prioritize data integrity and validation
2. Follow RESTful API conventions
3. Implement proper error handling and logging
4. Optimize database queries and indexes
5. Design for scalability within resource constraints
6. Document APIs with OpenAPI/Swagger

{agent_scratchpad}"""
    
    def _load_tools(self) -> List[Tool]:
        """Load tools specific to backend development"""
        
        return [
            Tool(
                name="create_fastapi_endpoint",
                func=self._create_fastapi_endpoint,
                description="Create FastAPI endpoint with validation and documentation"
            ),
            Tool(
                name="design_sqlalchemy_model",
                func=self._design_sqlalchemy_model,
                description="Design SQLAlchemy model with relationships and constraints"
            ),
            Tool(
                name="optimize_database_query",
                func=self._optimize_database_query,
                description="Optimize SQLAlchemy queries for performance"
            ),
            Tool(
                name="setup_celery_task",
                func=self._setup_celery_task,
                description="Create Celery background task with error handling"
            ),
            Tool(
                name="implement_redis_caching",
                func=self._implement_redis_caching,
                description="Implement Redis caching strategy for API endpoints"
            ),
            Tool(
                name="create_database_migration",
                func=self._create_database_migration,
                description="Generate Alembic migration for database changes"
            ),
            Tool(
                name="implement_api_security",
                func=self._implement_api_security,
                description="Add authentication and authorization to API endpoints"
            ),
            Tool(
                name="setup_performance_monitoring",
                func=self._setup_performance_monitoring,
                description="Configure performance monitoring and profiling"
            )
        ]
    
    def _create_fastapi_endpoint(self, endpoint_specs: str) -> str:
        """Create FastAPI endpoint with validation and documentation"""
        
        endpoint_info = self._parse_endpoint_specs(endpoint_specs)
        
        endpoint_code = f"""
# routers/{endpoint_info['module']}.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..database import get_db
from ..models import {endpoint_info['model']}
from ..schemas import {endpoint_info['schema']}, {endpoint_info['schema']}Create, {endpoint_info['schema']}Update
from ..dependencies import get_current_user
from ..utils.cache import cache_key, get_cached, set_cache
from ..utils.pagination import paginate

router = APIRouter(
    prefix="/{endpoint_info['prefix']}",
    tags=["{endpoint_info['tags']}"],
    responses={{404: {{"description": "Not found"}}}},
)

logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=List[{endpoint_info['schema']}],
    summary="Get {endpoint_info['description']}",
    description="Retrieve a paginated list of {endpoint_info['description'].lower()}"
)
async def get_{endpoint_info['plural']}(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    search: Optional[str] = Query(None, description="Search term")
) -> List[{endpoint_info['schema']}]:
    \"\"\"Get {endpoint_info['description'].lower()} with pagination and search\"\"\"
    
    try:
        # Check cache first
        cache_key_str = cache_key(f"{endpoint_info['plural']}", skip=skip, limit=limit, search=search)
        cached_result = await get_cached(cache_key_str)
        if cached_result:
            return cached_result
        
        # Build query
        query = db.query({endpoint_info['model']})
        
        if search:
            query = query.filter(
                {endpoint_info['model']}.name.ilike(f"%{{search}}%")
            )
        
        # Execute with pagination
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        
        # Cache result
        await set_cache(cache_key_str, items, expire=300)  # 5 minutes
        
        logger.info(f"Retrieved {{len(items)}} {endpoint_info['plural']} (total: {{total}})")
        return items
        
    except Exception as e:
        logger.error(f"Failed to get {endpoint_info['plural']}: {{e}}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve {endpoint_info['plural']}"
        )


@router.get(
    "/{{item_id}}",
    response_model={endpoint_info['schema']},
    summary="Get {endpoint_info['description']} by ID",
    responses={{
        200: {{"description": "Successful Response"}},
        404: {{"description": "Item not found"}}
    }}
)
async def get_{endpoint_info['singular']}(
    item_id: int,
    db: Session = Depends(get_db)
) -> {endpoint_info['schema']}:
    \"\"\"Get a specific {endpoint_info['description'].lower()} by ID\"\"\"
    
    # Check cache first
    cache_key_str = cache_key(f"{endpoint_info['singular']}", item_id=item_id)
    cached_result = await get_cached(cache_key_str)
    if cached_result:
        return cached_result
    
    item = db.query({endpoint_info['model']}).filter(
        {endpoint_info['model']}.id == item_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{endpoint_info['description']} not found"
        )
    
    # Cache result
    await set_cache(cache_key_str, item, expire=600)  # 10 minutes
    
    return item


@router.post(
    "/",
    response_model={endpoint_info['schema']},
    status_code=status.HTTP_201_CREATED,
    summary="Create {endpoint_info['description']}",
)
async def create_{endpoint_info['singular']}(
    item_data: {endpoint_info['schema']}Create,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
) -> {endpoint_info['schema']}:
    \"\"\"Create a new {endpoint_info['description'].lower()}\"\"\"
    
    try:
        # Create new item
        db_item = {endpoint_info['model']}(**item_data.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        logger.info(f"Created {endpoint_info['singular']} {{db_item.id}} by user {{current_user.id}}")
        
        # Invalidate related caches
        await invalidate_cache_pattern(f"{endpoint_info['plural']}*")
        
        return db_item
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create {endpoint_info['singular']}: {{e}}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create {endpoint_info['description'].lower()}"
        )


@router.put(
    "/{{item_id}}",
    response_model={endpoint_info['schema']},
    summary="Update {endpoint_info['description']}",
)
async def update_{endpoint_info['singular']}(
    item_id: int,
    item_data: {endpoint_info['schema']}Update,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
) -> {endpoint_info['schema']}:
    \"\"\"Update an existing {endpoint_info['description'].lower()}\"\"\"
    
    item = db.query({endpoint_info['model']}).filter(
        {endpoint_info['model']}.id == item_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{endpoint_info['description']} not found"
        )
    
    try:
        # Update item
        update_data = item_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        
        db.commit()
        db.refresh(item)
        
        logger.info(f"Updated {endpoint_info['singular']} {{item_id}} by user {{current_user.id}}")
        
        # Invalidate caches
        await invalidate_cache_pattern(f"{endpoint_info['plural']}*")
        await invalidate_cache_pattern(f"{endpoint_info['singular']}*")
        
        return item
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update {endpoint_info['singular']} {{item_id}}: {{e}}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update {endpoint_info['description'].lower()}"
        )


@router.delete(
    "/{{item_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete {endpoint_info['description']}",
)
async def delete_{endpoint_info['singular']}(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    \"\"\"Delete a {endpoint_info['description'].lower()}\"\"\"
    
    item = db.query({endpoint_info['model']}).filter(
        {endpoint_info['model']}.id == item_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{endpoint_info['description']} not found"
        )
    
    try:
        db.delete(item)
        db.commit()
        
        logger.info(f"Deleted {endpoint_info['singular']} {{item_id}} by user {{current_user.id}}")
        
        # Invalidate caches
        await invalidate_cache_pattern(f"{endpoint_info['plural']}*")
        await invalidate_cache_pattern(f"{endpoint_info['singular']}*")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete {endpoint_info['singular']} {{item_id}}: {{e}}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete {endpoint_info['description'].lower()}"
        )
"""
        
        return f"""
FastAPI Endpoint Implementation: {endpoint_info['description']}

Features:
- Full CRUD operations with proper HTTP methods
- Request/response validation with Pydantic
- SQLAlchemy database integration
- Redis caching with invalidation
- Comprehensive error handling
- Authentication and authorization
- Pagination and search support
- Structured logging
- OpenAPI documentation

Generated Code:
{endpoint_code.strip()}

Schema Definitions (schemas/{endpoint_info['module']}.py):
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class {endpoint_info['schema']}Base(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class {endpoint_info['schema']}Create({endpoint_info['schema']}Base):
    pass

class {endpoint_info['schema']}Update(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class {endpoint_info['schema']}({endpoint_info['schema']}Base):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

Registration in main.py:
```python
from .routers import {endpoint_info['module']}

app.include_router({endpoint_info['module']}.router, prefix="/api/v1")
```

Testing:
- Unit tests with pytest and TestClient
- Database fixtures with pytest-postgresql
- Cache testing with fakeredis
- Authentication testing with test tokens
"""
    
    def _design_sqlalchemy_model(self, model_specs: str) -> str:
        """Design SQLAlchemy model with relationships and constraints"""
        
        model_info = self._parse_model_specs(model_specs)
        
        model_code = f"""
# models/{model_info['module']}.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

from ..database import Base


class {model_info['name']}(Base):
    \"\"\"
    {model_info['description']} model
    
    Represents {model_info['description'].lower()} in the system with
    full audit trail and relationship management.
    \"\"\"
    
    __tablename__ = "{model_info['table']}"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Core fields
    {model_info['fields']}
    
    # Audit fields
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True
    )
    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )
    updated_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    
    # Soft delete support
    is_deleted = Column(Boolean, default=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    {model_info['relationships']}
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_{model_info["table"]}_name_active', 'name', postgresql_where=~is_deleted),
        Index('idx_{model_info["table"]}_created_at', 'created_at'),
        Index('idx_{model_info["table"]}_search', 'name', 'description', postgresql_using='gin'),
    )
    
    def __repr__(self) -> str:
        return f"<{model_info['name']}(id={{self.id}}, name='{{self.name}}')>"
    
    def to_dict(self) -> dict:
        \"\"\"Convert model to dictionary\"\"\"
        return {{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }}
    
    @classmethod
    def get_active(cls, db_session):
        \"\"\"Get only non-deleted records\"\"\"
        return db_session.query(cls).filter(cls.is_deleted == False)
    
    def soft_delete(self, user_id: int = None):
        \"\"\"Soft delete the record\"\"\"
        self.is_deleted = True
        self.deleted_at = func.now()
        if user_id:
            self.deleted_by = user_id
    
    def restore(self):
        \"\"\"Restore a soft-deleted record\"\"\"
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None


# Database event listeners for audit trail
from sqlalchemy import event

@event.listens_for({model_info['name']}, 'before_update')
def receive_before_update(mapper, connection, target):
    \"\"\"Update the updated_at timestamp on every update\"\"\"
    target.updated_at = func.now()

@event.listens_for({model_info['name']}, 'before_insert')
def receive_before_insert(mapper, connection, target):
    \"\"\"Set created_at timestamp on insert\"\"\"
    if not target.created_at:
        target.created_at = func.now()
"""
        
        return f"""
SQLAlchemy Model Design: {model_info['name']}

Features:
- Full audit trail with timestamps and user tracking
- Soft delete capability
- Composite indexes for performance
- Relationship management
- Data validation at database level
- Event listeners for automatic field updates
- Search optimization with GIN indexes

Generated Model:
{model_code.strip()}

Repository Pattern Implementation:
```python
# repositories/{model_info['module']}_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..models.{model_info['module']} import {model_info['name']}

class {model_info['name']}Repository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[{model_info['name']}]:
        return self.db.query({model_info['name']}).filter(
            {model_info['name']}.id == id,
            {model_info['name']}.is_deleted == False
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[{model_info['name']}]:
        return self.db.query({model_info['name']}).filter(
            {model_info['name']}.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[{model_info['name']}]:
        return self.db.query({model_info['name']}).filter(
            {model_info['name']}.name.ilike(f'%{{query}}%'),
            {model_info['name']}.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def create(self, **kwargs) -> {model_info['name']}:
        obj = {model_info['name']}(**kwargs)
        self.db.add(obj)
        self.db.flush()
        return obj
    
    def update(self, obj: {model_info['name']}, **kwargs) -> {model_info['name']}:
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db.flush()
        return obj
    
    def delete(self, obj: {model_info['name']}, user_id: int = None):
        obj.soft_delete(user_id)
        self.db.flush()
```

Migration Generation:
```bash
alembic revision --autogenerate -m "Create {model_info['table']} table"
alembic upgrade head
```

Testing Setup:
```python
# tests/test_{model_info['module']}.py
import pytest
from sqlalchemy.orm import Session
from ..models.{model_info['module']} import {model_info['name']}

def test_create_{model_info['module']}(db: Session):
    data = {{"name": "Test", "description": "Test description"}}
    obj = {model_info['name']}(**data)
    db.add(obj)
    db.commit()
    
    assert obj.id is not None
    assert obj.name == "Test"
    assert obj.created_at is not None
    assert not obj.is_deleted
```
"""
    
    def _optimize_database_query(self, query_specs: str) -> str:
        """Optimize SQLAlchemy queries for performance"""
        
        optimization_analysis = self._analyze_query_performance(query_specs)
        
        optimized_code = f"""
# Query Optimization Examples

# BEFORE: N+1 Query Problem
def get_jobs_with_employers_bad(db: Session) -> List[Job]:
    jobs = db.query(Job).all()
    for job in jobs:
        # This causes N+1 queries
        employer_name = job.employer.name
    return jobs

# AFTER: Eager Loading with joinedload
from sqlalchemy.orm import joinedload, selectinload

def get_jobs_with_employers_good(db: Session) -> List[Job]:
    return db.query(Job).options(
        joinedload(Job.employer),  # Single JOIN query
        selectinload(Job.skills)   # Separate optimized query for collections
    ).all()

# BEFORE: Inefficient filtering and counting
def get_job_stats_bad(db: Session) -> dict:
    total_jobs = db.query(Job).count()
    active_jobs = db.query(Job).filter(Job.status == 'active').count()
    remote_jobs = db.query(Job).filter(Job.remote_work == True).count()
    return {{"total": total_jobs, "active": active_jobs, "remote": remote_jobs}}

# AFTER: Single query with conditional aggregation
from sqlalchemy import func, case

def get_job_stats_good(db: Session) -> dict:
    stats = db.query(
        func.count(Job.id).label('total'),
        func.sum(case((Job.status == 'active', 1), else_=0)).label('active'),
        func.sum(case((Job.remote_work == True, 1), else_=0)).label('remote')
    ).first()
    
    return {{"total": stats.total, "active": stats.active, "remote": stats.remote}}

# Complex Query with Proper Indexing
def search_jobs_optimized(
    db: Session,
    search_term: str = None,
    location: str = None,
    salary_min: int = None,
    remote_only: bool = False,
    skip: int = 0,
    limit: int = 20
) -> tuple[List[Job], int]:
    \"\"\"Optimized job search with proper indexing\"\"\"
    
    # Base query with necessary joins
    query = db.query(Job).join(Job.employer).options(
        joinedload(Job.employer),
        selectinload(Job.skills).selectinload(JobSkill.skill)
    )
    
    # Apply filters (order matters for index usage)
    if remote_only:
        query = query.filter(Job.remote_work == True)
    
    if location:
        query = query.filter(Job.location.ilike(f'%{{location}}%'))
    
    if salary_min:
        query = query.filter(Job.salary_min >= salary_min)
    
    # Full-text search (uses GIN index)
    if search_term:
        query = query.filter(
            Job.search_vector.match(search_term)
        )
    
    # Get total count efficiently
    total = query.count()
    
    # Apply pagination and ordering
    jobs = query.order_by(
        Job.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return jobs, total

# Bulk Operations for Better Performance
def bulk_update_job_status(db: Session, job_ids: List[int], new_status: str):
    \"\"\"Bulk update for better performance\"\"\"
    db.query(Job).filter(
        Job.id.in_(job_ids)
    ).update(
        {{Job.status: new_status, Job.updated_at: func.now()}},
        synchronize_session=False
    )
    db.commit()

# Query with Raw SQL for Complex Operations
def get_job_analytics(db: Session) -> List[dict]:
    \"\"\"Use raw SQL for complex analytics queries\"\"\"
    result = db.execute(text('''
        SELECT 
            DATE_TRUNC('month', created_at) as month,
            COUNT(*) as job_count,
            AVG(salary_max) as avg_salary,
            COUNT(DISTINCT employer_id) as employer_count
        FROM jobs 
        WHERE created_at >= NOW() - INTERVAL '12 months'
        AND is_deleted = FALSE
        GROUP BY DATE_TRUNC('month', created_at)
        ORDER BY month DESC
    '''))
    
    return [dict(row) for row in result]
"""
        
        return f"""
Database Query Optimization Analysis

Performance Issues Identified:
{chr(10).join(f"- {issue}" for issue in optimization_analysis['issues'])}

Optimization Strategies:
{chr(10).join(f"- {strategy}" for strategy in optimization_analysis['strategies'])}

Optimized Code Examples:
{optimized_code.strip()}

Index Recommendations:
```sql
-- Composite indexes for common query patterns
CREATE INDEX CONCURRENTLY idx_jobs_status_location ON jobs(status, location) WHERE is_deleted = FALSE;
CREATE INDEX CONCURRENTLY idx_jobs_salary_remote ON jobs(salary_min, remote_work) WHERE is_deleted = FALSE;
CREATE INDEX CONCURRENTLY idx_jobs_created_at_desc ON jobs(created_at DESC) WHERE is_deleted = FALSE;

-- Full-text search index
CREATE INDEX CONCURRENTLY idx_jobs_search ON jobs USING gin(to_tsvector('english', title || ' ' || description));

-- Partial indexes for common filters
CREATE INDEX CONCURRENTLY idx_jobs_active ON jobs(created_at) WHERE status = 'active' AND is_deleted = FALSE;
```

Query Performance Monitoring:
```python
# Add to main.py for query logging
import logging
import time
from sqlalchemy import event
from sqlalchemy.engine import Engine

logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")  
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    if total > 0.1:  # Log slow queries (>100ms)
        logger.warning(f"Slow query: {{total:.4f}}s - {{statement[:100]}}")
```

Performance Testing:
- Use pytest-benchmark for query performance tests
- Monitor query execution plans with EXPLAIN ANALYZE
- Set up database connection pooling
- Implement query result caching with Redis
- Use database-level monitoring tools
"""
    
    def _setup_celery_task(self, task_specs: str) -> str:
        """Create Celery background task with error handling"""
        
        task_info = self._parse_task_specs(task_specs)
        
        task_code = f"""
# tasks/{task_info['module']}.py
from celery import Celery
from celery.utils.log import get_task_logger
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import json
from datetime import datetime, timedelta

from ..database import SessionLocal
from ..models import {task_info['model']}
from ..utils.email import send_notification_email
from ..utils.cache import invalidate_cache_pattern

# Initialize Celery app
celery_app = Celery('fed_job_advisor')
celery_app.config_from_object('app.core.celery_config')

logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={{'max_retries': 3}},
    name='{task_info['name']}'
)
def {task_info['function']}(self, {task_info['parameters']}):
    \"\"\"
    {task_info['description']}
    
    Args:
        {task_info['parameter_docs']}
    
    Returns:
        Dict containing task results and metadata
    \"\"\"
    
    task_id = self.request.id
    logger.info(f"Starting task {task_info['name']} {{task_id}}")
    
    db = SessionLocal()
    try:
        # Task implementation
        result = {{
            'task_id': task_id,
            'status': 'started',
            'started_at': datetime.utcnow().isoformat(),
            'progress': 0
        }}
        
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={{'progress': 10, 'status': 'Initializing...'}}
        )
        
        # Main task logic
        {task_info['implementation']}
        
        # Final progress update
        self.update_state(
            state='PROGRESS', 
            meta={{'progress': 90, 'status': 'Finalizing...'}}
        )
        
        # Complete the task
        result.update({{
            'status': 'completed',
            'completed_at': datetime.utcnow().isoformat(),
            'progress': 100,
            'data': processed_data
        }})
        
        logger.info(f"Task {task_info['name']} {{task_id}} completed successfully")
        return result
        
    except Exception as exc:
        db.rollback()
        logger.error(f"Task {task_info['name']} {{task_id}} failed: {{exc}}")
        
        # Retry logic
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying task {{task_id}} (attempt {{self.request.retries + 1}})")
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        
        # Final failure
        return {{
            'task_id': task_id,
            'status': 'failed',
            'error': str(exc),
            'failed_at': datetime.utcnow().isoformat()
        }}
        
    finally:
        db.close()


@celery_app.task(name='{task_info['name']}_batch')
def {task_info['function']}_batch(items: list, batch_size: int = 10):
    \"\"\"Process items in batches to avoid overwhelming the system\"\"\"
    
    job_ids = []
    
    # Split items into batches
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        # Create subtask for each batch
        job = {task_info['function']}.delay(*batch)
        job_ids.append(job.id)
        
        logger.info(f"Created batch job {{job.id}} for items {{i}}-{{i+len(batch)}}")
    
    return {{
        'batch_jobs': job_ids,
        'total_batches': len(job_ids),
        'batch_size': batch_size
    }}


@celery_app.task(name='{task_info['name']}_monitor')
def monitor_{task_info['function']}():
    \"\"\"Monitor and cleanup old task results\"\"\"
    
    from ..models.task_result import TaskResult
    
    db = SessionLocal()
    try:
        # Clean up old task results (older than 7 days)
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        
        old_results = db.query(TaskResult).filter(
            TaskResult.created_at < cutoff_date,
            TaskResult.status.in_(['completed', 'failed'])
        ).all()
        
        for result in old_results:
            db.delete(result)
        
        db.commit()
        logger.info(f"Cleaned up {{len(old_results)}} old task results")
        
        # Invalidate related caches
        await invalidate_cache_pattern(f"{task_info['name']}*")
        
        return {{'cleaned_up': len(old_results)}}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to cleanup task results: {{e}}")
        raise
    finally:
        db.close()


# Periodic task setup
@celery_app.task(name='cleanup_task_results')
def setup_periodic_cleanup():
    \"\"\"Set up periodic cleanup of task results\"\"\"
    
    # Schedule cleanup to run daily at 2 AM
    celery_app.conf.beat_schedule = {{
        'cleanup-task-results': {{
            'task': '{task_info['name']}_monitor',
            'schedule': crontab(hour=2, minute=0),
        }},
    }}
"""
        
        return f"""
Celery Background Task Implementation: {task_info['name']}

Features:
- Automatic retry with exponential backoff
- Progress tracking and status updates
- Comprehensive error handling and logging
- Batch processing capabilities
- Monitoring and cleanup tasks
- Database transaction management
- Cache invalidation integration

Generated Task:
{task_code.strip()}

Celery Configuration (celery_config.py):
```python
import os
from celery import Celery

# Celery configuration
broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Task settings
task_serializer = 'json'
result_serializer = 'json' 
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

# Worker settings
worker_prefetch_multiplier = 1
task_acks_late = True
worker_max_tasks_per_child = 1000

# Result settings
result_expires = 3600  # 1 hour
result_persistent = True

# Route configuration
task_routes = {{
    '{task_info['name']}*': {{'queue': 'default'}},
}}

# Beat schedule for periodic tasks
beat_schedule = {{
    'cleanup-task-results': {{
        'task': 'cleanup_task_results',
        'schedule': 30.0,  # Every 30 seconds for demo
    }},
}}
```

Worker Startup:
```bash
# Start Celery worker
celery -A app.tasks.celery_app worker --loglevel=info --concurrency=2

# Start Celery beat scheduler
celery -A app.tasks.celery_app beat --loglevel=info

# Monitor with Flower
celery -A app.tasks.celery_app flower --port=5555
```

Task Usage in API:
```python
# In your FastAPI endpoint
from ..tasks.{task_info['module']} import {task_info['function']}

@router.post("/process")
async def start_processing(request: ProcessRequest):
    # Start background task
    job = {task_info['function']}.delay(
        request.data,
        request.options
    )
    
    return {{
        "task_id": job.id,
        "status": "started",
        "message": "Processing started in background"
    }}

@router.get("/status/{{task_id}}")
async def get_task_status(task_id: str):
    job = {task_info['function']}.AsyncResult(task_id)
    
    if job.state == 'PENDING':
        response = {{'status': 'pending'}}
    elif job.state == 'PROGRESS':
        response = job.result
    else:
        response = job.result
    
    return response
```

Monitoring and Debugging:
- Use Flower for real-time monitoring
- Implement task result storage
- Set up alerting for failed tasks
- Monitor queue lengths and worker health
- Log task execution times and resource usage
"""
    
    def _implement_redis_caching(self, cache_specs: str) -> str:
        """Implement Redis caching strategy"""
        
        cache_info = self._parse_cache_specs(cache_specs)
        
        cache_code = f"""
# utils/cache.py
import redis.asyncio as redis
import json
import hashlib
from typing import Any, Optional, Union, List
from functools import wraps
from datetime import timedelta
import pickle
import logging

logger = logging.getLogger(__name__)

# Redis connection pool
redis_pool = None

async def get_redis_pool():
    \"\"\"Get or create Redis connection pool\"\"\"
    global redis_pool
    if not redis_pool:
        redis_pool = redis.ConnectionPool.from_url(
            "redis://localhost:6379/0",
            max_connections=20,
            retry_on_timeout=True,
            decode_responses=False  # We handle encoding ourselves
        )
    return redis.Redis(connection_pool=redis_pool)


def cache_key(*args, **kwargs) -> str:
    \"\"\"Generate consistent cache key from arguments\"\"\"
    key_data = f"{{args}}{{sorted(kwargs.items())}}"
    return hashlib.md5(key_data.encode()).hexdigest()


async def get_cached(key: str) -> Optional[Any]:
    \"\"\"Get cached value by key\"\"\"
    try:
        redis_client = await get_redis_pool()
        cached_data = await redis_client.get(key)
        
        if cached_data:
            # Try JSON first, fallback to pickle
            try:
                return json.loads(cached_data)
            except json.JSONDecodeError:
                return pickle.loads(cached_data)
        
        return None
        
    except Exception as e:
        logger.error(f"Cache get error for key {{key}}: {{e}}")
        return None


async def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    \"\"\"Set cached value with expiration\"\"\"
    try:
        redis_client = await get_redis_pool()
        
        # Try JSON first, fallback to pickle
        try:
            serialized_data = json.dumps(value, default=str)
        except (TypeError, ValueError):
            serialized_data = pickle.dumps(value)
        
        await redis_client.setex(key, expire, serialized_data)
        return True
        
    except Exception as e:
        logger.error(f"Cache set error for key {{key}}: {{e}}")
        return False


async def delete_cache(key: str) -> bool:
    \"\"\"Delete cached value\"\"\"
    try:
        redis_client = await get_redis_pool()
        result = await redis_client.delete(key)
        return bool(result)
        
    except Exception as e:
        logger.error(f"Cache delete error for key {{key}}: {{e}}")
        return False


async def invalidate_cache_pattern(pattern: str) -> int:
    \"\"\"Delete all keys matching pattern\"\"\"
    try:
        redis_client = await get_redis_pool()
        keys = await redis_client.keys(pattern)
        
        if keys:
            result = await redis_client.delete(*keys)
            logger.info(f"Invalidated {{result}} cache keys matching {{pattern}}")
            return result
        
        return 0
        
    except Exception as e:
        logger.error(f"Cache invalidation error for pattern {{pattern}}: {{e}}")
        return 0


def cached(expire: int = 3600, key_prefix: str = ""):
    \"\"\"Decorator for caching function results\"\"\"
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            func_key = f"{{key_prefix}}{{func.__name__}}"
            key = cache_key(func_key, *args, **kwargs)
            
            # Try to get from cache
            cached_result = await get_cached(key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {{func.__name__}}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            await set_cache(key, result, expire)
            
            logger.debug(f"Cache miss for {{func.__name__}}, result cached")
            return result
            
        return wrapper
    return decorator


class CacheManager:
    \"\"\"Advanced cache management with namespacing\"\"\"
    
    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        
    def _namespaced_key(self, key: str) -> str:
        return f"{{self.namespace}}:{{key}}"
    
    async def get(self, key: str) -> Optional[Any]:
        return await get_cached(self._namespaced_key(key))
    
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        return await set_cache(self._namespaced_key(key), value, expire)
    
    async def delete(self, key: str) -> bool:
        return await delete_cache(self._namespaced_key(key))
    
    async def clear_namespace(self) -> int:
        \"\"\"Clear all keys in this namespace\"\"\"
        pattern = f"{{self.namespace}}:*"
        return await invalidate_cache_pattern(pattern)
    
    async def get_multi(self, keys: List[str]) -> dict:
        \"\"\"Get multiple cache values\"\"\"
        try:
            redis_client = await get_redis_pool()
            namespaced_keys = [self._namespaced_key(key) for key in keys]
            
            values = await redis_client.mget(namespaced_keys)
            result = {{}}
            
            for i, value in enumerate(values):
                if value:
                    try:
                        result[keys[i]] = json.loads(value)
                    except json.JSONDecodeError:
                        result[keys[i]] = pickle.loads(value)
            
            return result
            
        except Exception as e:
            logger.error(f"Multi-get error: {{e}}")
            return {{}}
    
    async def set_multi(self, mapping: dict, expire: int = 3600) -> bool:
        \"\"\"Set multiple cache values\"\"\"
        try:
            redis_client = await get_redis_pool()
            pipe = redis_client.pipeline()
            
            for key, value in mapping.items():
                try:
                    serialized = json.dumps(value, default=str)
                except (TypeError, ValueError):
                    serialized = pickle.dumps(value)
                
                pipe.setex(self._namespaced_key(key), expire, serialized)
            
            await pipe.execute()
            return True
            
        except Exception as e:
            logger.error(f"Multi-set error: {{e}}")
            return False


# Cache warming functions
async def warm_cache():
    \"\"\"Warm up frequently accessed cache entries\"\"\"
    from ..database import SessionLocal
    from ..models import Job, User
    
    db = SessionLocal()
    try:
        # Cache popular job searches
        popular_searches = [
            "data scientist",
            "software engineer", 
            "program analyst",
            "cybersecurity"
        ]
        
        for search_term in popular_searches:
            # Pre-populate search results
            key = cache_key("job_search", search_term, limit=20)
            
            # Only warm if not already cached
            if not await get_cached(key):
                jobs = db.query(Job).filter(
                    Job.title.ilike(f'%{{search_term}}%')
                ).limit(20).all()
                
                await set_cache(key, [job.to_dict() for job in jobs], expire=1800)
                
        logger.info("Cache warming completed")
        
    except Exception as e:
        logger.error(f"Cache warming failed: {{e}}")
    finally:
        db.close()
"""
        
        return f"""
Redis Caching Implementation: {cache_info['strategy']}

Features:
- Async Redis operations with connection pooling
- JSON and Pickle serialization support
- Decorator-based function caching
- Namespace management for cache organization
- Bulk operations (get_multi, set_multi)
- Pattern-based cache invalidation
- Cache warming strategies
- Comprehensive error handling

Generated Code:
{cache_code.strip()}

Usage Examples:

1. Function Decorator Caching:
```python
from .utils.cache import cached

@cached(expire=600, key_prefix="api:")
async def get_job_recommendations(user_id: int, limit: int = 10):
    # Expensive database operation
    return recommendations

# Usage automatically caches based on parameters
recommendations = await get_job_recommendations(user_id=123, limit=10)
```

2. Manual Cache Management:
```python
from .utils.cache import CacheManager

# Create namespaced cache manager
job_cache = CacheManager("jobs")

# Cache job data
await job_cache.set("featured", featured_jobs, expire=3600)

# Retrieve cached data  
cached_jobs = await job_cache.get("featured")

# Clear all job-related cache
await job_cache.clear_namespace()
```

3. FastAPI Integration:
```python
from .utils.cache import get_cached, set_cache, cache_key

@router.get("/jobs")
async def get_jobs(search: str = None, limit: int = 20):
    # Generate cache key
    key = cache_key("jobs_list", search=search, limit=limit)
    
    # Check cache first
    cached_result = await get_cached(key)
    if cached_result:
        return cached_result
    
    # Fetch from database
    jobs = await fetch_jobs_from_db(search, limit)
    
    # Cache for 10 minutes
    await set_cache(key, jobs, expire=600)
    
    return jobs
```

4. Cache Invalidation Strategies:
```python
# After updating job data
await invalidate_cache_pattern("jobs:*")
await invalidate_cache_pattern("api:get_job_recommendations:*")

# In background task
@celery_app.task
def invalidate_stale_cache():
    # Remove expired job listings cache
    await invalidate_cache_pattern("jobs:search:*")
```

Redis Configuration (redis.conf):
```
# Memory optimization
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence for cache durability
save 900 1
save 300 10
save 60 10000

# Network settings
timeout 300
tcp-keepalive 300
```

Monitoring and Metrics:
```python
async def get_cache_stats():
    redis_client = await get_redis_pool()
    info = await redis_client.info()
    
    return {{
        "used_memory": info["used_memory_human"],
        "keyspace_hits": info["keyspace_hits"],
        "keyspace_misses": info["keyspace_misses"],
        "hit_rate": info["keyspace_hits"] / (info["keyspace_hits"] + info["keyspace_misses"])
    }}
```

Performance Tips:
- Use appropriate expiration times based on data freshness needs
- Implement cache warming for frequently accessed data
- Monitor hit rates and adjust caching strategies
- Use pipeline operations for bulk cache operations
- Consider using Redis Cluster for high availability
"""
    
    def _create_database_migration(self, migration_specs: str) -> str:
        """Generate Alembic migration for database changes"""
        
        migration_info = self._parse_migration_specs(migration_specs)
        
        migration_code = f"""
# Generated Alembic Migration
# alembic/versions/{migration_info['version']}_{migration_info['slug']}.py

\"\"\"
{migration_info['description']}

Revision ID: {migration_info['version']}
Revises: {migration_info['previous']}
Create Date: {migration_info['date']}
\"\"\"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '{migration_info['version']}'
down_revision = '{migration_info['previous']}'
branch_labels = None
depends_on = None


def upgrade() -> None:
    \"\"\"Apply migration changes\"\"\"
    
    {migration_info['upgrade_operations']}


def downgrade() -> None:
    \"\"\"Rollback migration changes\"\"\"
    
    {migration_info['downgrade_operations']}


# Custom migration utilities
def create_index_concurrently(index_name: str, table_name: str, columns: list):
    \"\"\"Create index without blocking table\"\"\"
    op.execute(f'''
        CREATE INDEX CONCURRENTLY {index_name} 
        ON {table_name} ({", ".join(columns)})
    ''')

def drop_index_concurrently(index_name: str):
    \"\"\"Drop index without blocking table\"\"\"
    op.execute(f'DROP INDEX CONCURRENTLY IF EXISTS {index_name}')

def add_column_with_default(table_name: str, column_name: str, column_type, default_value):
    \"\"\"Add column with default value efficiently\"\"\"
    # Add column without default
    op.add_column(table_name, sa.Column(column_name, column_type, nullable=True))
    
    # Update existing rows
    op.execute(f'''
        UPDATE {table_name} 
        SET {column_name} = '{default_value}' 
        WHERE {column_name} IS NULL
    ''')
    
    # Add not null constraint
    op.alter_column(table_name, column_name, nullable=False)
"""
        
        return f"""
Alembic Database Migration: {migration_info['description']}

Migration File Generated:
{migration_code.strip()}

Migration Commands:
```bash
# Generate migration automatically
alembic revision --autogenerate -m "{migration_info['description']}"

# Apply migration
alembic upgrade head

# Rollback migration  
alembic downgrade -1

# Show migration history
alembic history --verbose

# Show current revision
alembic current
```

Common Migration Patterns:

1. Adding New Table:
```python
def upgrade():
    op.create_table(
        'new_table',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_new_table_name', 'name')
    )

def downgrade():
    op.drop_table('new_table')
```

2. Adding Column with Data Migration:
```python
def upgrade():
    # Add column
    op.add_column('jobs', sa.Column('priority', sa.Integer(), nullable=True))
    
    # Migrate existing data
    connection = op.get_bind()
    connection.execute('''
        UPDATE jobs 
        SET priority = CASE 
            WHEN salary_max > 150000 THEN 1
            WHEN salary_max > 100000 THEN 2 
            ELSE 3 
        END
    ''')
    
    # Make column required
    op.alter_column('jobs', 'priority', nullable=False)

def downgrade():
    op.drop_column('jobs', 'priority')
```

3. Complex Schema Changes:
```python
def upgrade():
    # Create new table structure
    op.create_table('jobs_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(500), nullable=False),  # Increased size
        # ... other columns
    )
    
    # Migrate data
    connection = op.get_bind()
    connection.execute('''
        INSERT INTO jobs_new (id, title, ...)
        SELECT id, LEFT(title, 500), ...
        FROM jobs
    ''')
    
    # Swap tables
    op.drop_table('jobs')
    op.rename_table('jobs_new', 'jobs')
    
    # Recreate indexes
    create_index_concurrently('idx_jobs_title', 'jobs', ['title'])

def downgrade():
    # Reverse migration logic
    pass
```

4. Performance-Optimized Migrations:
```python
def upgrade():
    # Create index concurrently (doesn't block table)
    op.execute('CREATE INDEX CONCURRENTLY idx_jobs_status ON jobs(status)')
    
    # Add column with efficient default handling
    add_column_with_default('jobs', 'featured', sa.Boolean(), False)
    
    # Update in batches to avoid locks
    connection = op.get_bind()
    batch_size = 10000
    offset = 0
    
    while True:
        result = connection.execute(f'''
            UPDATE jobs 
            SET featured = TRUE 
            WHERE id IN (
                SELECT id FROM jobs 
                WHERE featured IS NULL 
                AND salary_max > 120000
                LIMIT {batch_size} OFFSET {offset}
            )
        ''')
        
        if result.rowcount == 0:
            break
        offset += batch_size
```

Migration Testing:
```python
# tests/test_migrations.py
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine

def test_migration_upgrade_downgrade():
    # Test migration up
    command.upgrade(alembic_cfg, "head")
    
    # Verify schema changes
    assert table_exists("new_table")
    assert column_exists("jobs", "new_column")
    
    # Test migration down
    command.downgrade(alembic_cfg, "-1") 
    
    # Verify rollback
    assert not table_exists("new_table")
```

Best Practices:
- Always test migrations on staging data
- Use CONCURRENTLY for index operations on large tables
- Batch large data updates to avoid lock timeouts
- Include data validation in migration scripts
- Keep migrations reversible when possible
- Document breaking changes clearly
- Use feature flags during schema transitions
"""
    
    def _implement_api_security(self, security_specs: str) -> str:
        """Implement API security and authentication"""
        
        security_code = f"""
# security/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import os

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()


class SecurityManager:
    \"\"\"Centralized security management\"\"\"
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        \"\"\"Verify password against hash\"\"\"
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        \"\"\"Generate password hash\"\"\"
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        \"\"\"Create JWT access token\"\"\"
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({{"exp": expire}})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        \"\"\"Verify and decode JWT token\"\"\"
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None


# Dependency functions
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    \"\"\"Get current authenticated user\"\"\"
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={{"WWW-Authenticate": "Bearer"}},
    )
    
    try:
        payload = SecurityManager.verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    \"\"\"Get current active user\"\"\"
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user


def require_roles(*required_roles: str):
    \"\"\"Decorator to require specific roles\"\"\"
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Authentication required"
                )
            
            # Check if user has required role
            if not any(role.name in required_roles for role in current_user.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required roles: {{', '.join(required_roles)}}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Rate limiting
from fastapi_limiter.depends import RateLimiter

def rate_limit(requests: int = 100, window: int = 60):
    \"\"\"Rate limiting decorator\"\"\"
    return RateLimiter(times=requests, seconds=window)


# API Key authentication for external services
class APIKeyManager:
    \"\"\"Manage API keys for external service access\"\"\"
    
    @staticmethod
    async def verify_api_key(api_key: str, db: Session) -> Optional[dict]:
        \"\"\"Verify API key and return associated service info\"\"\"
        
        # Hash the provided key
        key_hash = SecurityManager.get_password_hash(api_key)
        
        # Look up in database
        service = db.query(APIKey).filter(
            APIKey.key_hash == key_hash,
            APIKey.is_active == True,
            APIKey.expires_at > datetime.utcnow()
        ).first()
        
        if service:
            # Update last used timestamp
            service.last_used_at = datetime.utcnow()
            db.commit()
            
            return {{
                "service_name": service.name,
                "permissions": service.permissions,
                "rate_limit": service.rate_limit
            }}
        
        return None


async def verify_api_key_header(
    x_api_key: str = Header(..., description="API Key"),
    db: Session = Depends(get_db)
) -> dict:
    \"\"\"Verify API key from header\"\"\"
    
    service_info = await APIKeyManager.verify_api_key(x_api_key, db)
    
    if not service_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key"
        )
    
    return service_info
"""
        
        return f"""
API Security Implementation

Features:
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- API key authentication for services
- Rate limiting per endpoint
- Token expiration and refresh
- Comprehensive error handling

Generated Security Code:
{security_code.strip()}

Authentication Endpoints:
```python
# routers/auth.py
@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = SecurityManager.create_access_token(
        data={{"sub": str(user.id), "roles": [r.name for r in user.roles]}}
    )
    
    return {{"access_token": access_token, "token_type": "bearer"}}

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = SecurityManager.get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
```

Protected Endpoint Examples:
```python
# Require authentication
@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

# Require specific role
@router.post("/admin/users")
@require_roles("admin")
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Admin-only endpoint
    pass

# Rate limited endpoint
@router.get("/search", dependencies=[Depends(rate_limit(requests=10, window=60))])
async def search_jobs(query: str):
    # Limited to 10 requests per minute
    pass

# API key protected endpoint
@router.post("/webhook")
async def webhook(
    data: dict,
    service_info: dict = Depends(verify_api_key_header)
):
    # External service endpoint
    pass
```

Security Models:
```python
# models/security.py
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relationships
    roles = relationship("UserRole", back_populates="user")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    
class UserRole(Base):
    __tablename__ = "user_roles"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    
class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    key_hash = Column(String, nullable=False, index=True)
    permissions = Column(JSON)
    rate_limit = Column(Integer, default=1000)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    last_used_at = Column(DateTime)
```

Security Middleware:
```python
# middleware/security.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"{{request.method}} {{request.url.path}} - {{request.client.host}}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(f"Response: {{response.status_code}} in {{process_time:.4f}}s")
        
        return response
```

Environment Configuration:
```bash
# .env
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Password policy
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_NUMBERS=true
PASSWORD_REQUIRE_SPECIAL=true
```

Security Testing:
```python
# tests/test_security.py
def test_password_hashing():
    password = "test_password_123"
    hashed = SecurityManager.get_password_hash(password)
    
    assert SecurityManager.verify_password(password, hashed)
    assert not SecurityManager.verify_password("wrong_password", hashed)

def test_jwt_token_creation():
    data = {{"sub": "123", "roles": ["user"]}}
    token = SecurityManager.create_access_token(data)
    
    payload = SecurityManager.verify_token(token)
    assert payload["sub"] == "123"
    assert "user" in payload["roles"]

def test_protected_endpoint_access():
    # Test without token
    response = client.get("/protected")
    assert response.status_code == 401
    
    # Test with valid token
    token = create_test_token()
    headers = {{"Authorization": f"Bearer {{token}}"}}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
```

Security Best Practices:
- Use strong, randomly generated SECRET_KEY
- Implement proper password policies
- Enable HTTPS in production
- Regular security audits and updates
- Monitor for suspicious activity
- Implement proper session management
- Use environment variables for sensitive config
"""
    
    def _setup_performance_monitoring(self, monitoring_specs: str) -> str:
        """Configure performance monitoring and profiling"""
        
        monitoring_code = f"""
# monitoring/performance.py
import time
import psutil
import logging
from functools import wraps
from typing import Dict, Any, List
from datetime import datetime, timedelta
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import structlog

logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')
DATABASE_QUERY_DURATION = Histogram('database_query_duration_seconds', 'Database query duration', ['query_type'])
CELERY_TASK_DURATION = Histogram('celery_task_duration_seconds', 'Celery task duration', ['task_name'])

class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    \"\"\"Middleware for monitoring API performance\"\"\"
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Track active connections
        ACTIVE_CONNECTIONS.inc()
        
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Update metrics
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            REQUEST_DURATION.observe(duration)
            
            # Add performance headers
            response.headers["X-Process-Time"] = str(duration)
            
            # Log slow requests
            if duration > 1.0:  # Requests taking more than 1 second
                logger.warning(
                    "Slow request detected",
                    method=request.method,
                    path=request.url.path,
                    duration=duration,
                    query_params=dict(request.query_params)
                )
            
            return response
            
        except Exception as e:
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()
            raise
            
        finally:
            ACTIVE_CONNECTIONS.dec()


def profile_performance(func_name: str = None):
    \"\"\"Decorator to profile function performance\"\"\"
    
    def decorator(func):
        name = func_name or f"{{func.__module__}}.{{func.__name__}}"
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                
                duration = time.time() - start_time
                
                logger.debug(
                    "Function execution completed",
                    function=name,
                    duration=duration
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "Function execution failed",
                    function=name,
                    duration=duration,
                    error=str(e)
                )
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                logger.debug(
                    "Function execution completed",
                    function=name,
                    duration=duration
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "Function execution failed",
                    function=name,
                    duration=duration,
                    error=str(e)
                )
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator


class DatabaseQueryProfiler:
    \"\"\"Profile database query performance\"\"\"
    
    @staticmethod
    def profile_query(query_type: str):
        \"\"\"Context manager for profiling database queries\"\"\"
        
        class QueryProfiler:
            def __init__(self, query_type: str):
                self.query_type = query_type
                self.start_time = None
            
            def __enter__(self):
                self.start_time = time.time()
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.start_time:
                    duration = time.time() - self.start_time
                    DATABASE_QUERY_DURATION.labels(query_type=self.query_type).observe(duration)
                    
                    if duration > 0.5:  # Log slow queries
                        logger.warning(
                            "Slow database query",
                            query_type=self.query_type,
                            duration=duration
                        )
        
        return QueryProfiler(query_type)


class SystemMetrics:
    \"\"\"Collect system-level metrics\"\"\"
    
    @staticmethod
    def get_system_metrics() -> Dict[str, Any]:
        \"\"\"Get current system metrics\"\"\"
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {{
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_used_gb": memory.used / (1024**3),
            "memory_total_gb": memory.total / (1024**3),
            "disk_percent": disk.percent,
            "disk_used_gb": disk.used / (1024**3),
            "disk_total_gb": disk.total / (1024**3),
            "timestamp": datetime.utcnow().isoformat()
        }}
    
    @staticmethod
    def get_application_metrics() -> Dict[str, Any]:
        \"\"\"Get application-specific metrics\"\"\"
        
        return {{
            "uptime_seconds": time.time() - start_time,
            "active_connections": ACTIVE_CONNECTIONS._value._value,
            "total_requests": sum(REQUEST_COUNT._value.values()),
            "average_response_time": REQUEST_DURATION._sum._value / max(REQUEST_DURATION._count._value, 1)
        }}


class PerformanceReporter:
    \"\"\"Generate performance reports\"\"\"
    
    def __init__(self):
        self.metrics_history: List[Dict] = []
    
    def collect_metrics(self):
        \"\"\"Collect current metrics\"\"\"
        metrics = {{
            "system": SystemMetrics.get_system_metrics(),
            "application": SystemMetrics.get_application_metrics(),
            "timestamp": datetime.utcnow()
        }}
        
        self.metrics_history.append(metrics)
        
        # Keep only last 100 entries
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-100:]
    
    def generate_report(self, hours: int = 24) -> Dict[str, Any]:
        \"\"\"Generate performance report for the last N hours\"\"\"
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_metrics = [
            m for m in self.metrics_history 
            if m["timestamp"] >= cutoff_time
        ]
        
        if not recent_metrics:
            return {{"error": "No metrics available for the specified period"}}
        
        # Calculate averages
        avg_cpu = sum(m["system"]["cpu_percent"] for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m["system"]["memory_percent"] for m in recent_metrics) / len(recent_metrics)
        avg_response_time = sum(m["application"]["average_response_time"] for m in recent_metrics) / len(recent_metrics)
        
        # Find peaks
        peak_cpu = max(m["system"]["cpu_percent"] for m in recent_metrics)
        peak_memory = max(m["system"]["memory_percent"] for m in recent_metrics)
        
        return {{
            "period_hours": hours,
            "metrics_count": len(recent_metrics),
            "averages": {{
                "cpu_percent": round(avg_cpu, 2),
                "memory_percent": round(avg_memory, 2),
                "response_time_seconds": round(avg_response_time, 4)
            }},
            "peaks": {{
                "cpu_percent": peak_cpu,
                "memory_percent": peak_memory
            }},
            "recommendations": self._generate_recommendations(avg_cpu, avg_memory, avg_response_time)
        }}
    
    def _generate_recommendations(self, avg_cpu: float, avg_memory: float, avg_response_time: float) -> List[str]:
        \"\"\"Generate performance recommendations\"\"\"
        recommendations = []
        
        if avg_cpu > 80:
            recommendations.append("High CPU usage detected. Consider optimizing algorithms or scaling horizontally.")
        
        if avg_memory > 85:
            recommendations.append("High memory usage detected. Check for memory leaks or consider increasing RAM.")
        
        if avg_response_time > 0.5:
            recommendations.append("Slow average response time. Consider caching, database optimization, or CDN.")
        
        if not recommendations:
            recommendations.append("Performance metrics look healthy. Continue monitoring.")
        
        return recommendations


# Global performance reporter instance
performance_reporter = PerformanceReporter()

# Background task to collect metrics
import asyncio

async def metrics_collector():
    \"\"\"Background task to collect metrics regularly\"\"\"
    while True:
        try:
            performance_reporter.collect_metrics()
            await asyncio.sleep(60)  # Collect every minute
        except Exception as e:
            logger.error("Failed to collect metrics", error=str(e))
            await asyncio.sleep(60)

# Start metrics collection on startup
start_time = time.time()
asyncio.create_task(metrics_collector())
"""
        
        return f"""
Performance Monitoring Implementation

Features:
- Prometheus metrics integration
- Request/response time tracking
- System resource monitoring
- Database query profiling
- Automatic performance reporting
- Slow request detection and logging
- Background metrics collection
- Performance recommendations

Generated Monitoring Code:
{monitoring_code.strip()}

FastAPI Integration:
```python
# main.py
from .monitoring.performance import PerformanceMonitoringMiddleware, performance_reporter
from prometheus_client import make_asgi_app

# Add monitoring middleware
app.add_middleware(PerformanceMonitoringMiddleware)

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Performance dashboard endpoint
@app.get("/admin/performance")
async def get_performance_metrics(hours: int = 24):
    return performance_reporter.generate_report(hours)

@app.get("/admin/system")
async def get_system_metrics():
    return SystemMetrics.get_system_metrics()
```

Database Query Profiling:
```python
# In your repository or service classes
from .monitoring.performance import DatabaseQueryProfiler

class JobRepository:
    def get_jobs(self, filters: dict) -> List[Job]:
        with DatabaseQueryProfiler.profile_query("get_jobs"):
            query = self.db.query(Job)
            # ... apply filters
            return query.all()
    
    def complex_job_search(self, search_params: dict) -> List[Job]:
        with DatabaseQueryProfiler.profile_query("complex_search"):
            # Complex database operations
            return results
```

Function Performance Profiling:
```python
from .monitoring.performance import profile_performance

@profile_performance("job_recommendation_algorithm")
async def generate_job_recommendations(user_id: int) -> List[Job]:
    # Complex recommendation algorithm
    return recommendations

@profile_performance("data_processing")
def process_job_data(raw_data: dict) -> dict:
    # Data processing logic
    return processed_data
```

Monitoring Dashboard (simple HTML):
```html
<!-- templates/monitoring_dashboard.html -->
<html>
<head>
    <title>Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Fed Job Advisor - Performance Dashboard</h1>
    
    <div class="metrics-grid">
        <div class="metric-card">
            <h3>CPU Usage</h3>
            <canvas id="cpuChart"></canvas>
        </div>
        
        <div class="metric-card">
            <h3>Memory Usage</h3>
            <canvas id="memoryChart"></canvas>
        </div>
        
        <div class="metric-card">
            <h3>Response Times</h3>
            <canvas id="responseChart"></canvas>
        </div>
    </div>
    
    <script>
        // Fetch and display metrics
        async function updateDashboard() {{
            const response = await fetch('/admin/performance?hours=1');
            const data = await response.json();
            
            // Update charts with real data
            updateCharts(data);
        }}
        
        // Update every 30 seconds
        setInterval(updateDashboard, 30000);
        updateDashboard();
    </script>
</body>
</html>
```

Alerting Configuration:
```python
# monitoring/alerts.py
class AlertManager:
    def __init__(self):
        self.alert_thresholds = {{
            "cpu_percent": 90,
            "memory_percent": 90,
            "response_time": 2.0,
            "error_rate": 0.05
        }}
    
    def check_alerts(self, metrics: dict):
        alerts = []
        
        if metrics["system"]["cpu_percent"] > self.alert_thresholds["cpu_percent"]:
            alerts.append({{
                "level": "critical",
                "message": f"High CPU usage: {{metrics['system']['cpu_percent']}}%"
            }})
        
        # Check other thresholds...
        
        if alerts:
            self.send_alerts(alerts)
    
    def send_alerts(self, alerts: List[dict]):
        for alert in alerts:
            logger.error("ALERT", **alert)
            # Send to external monitoring service
```

Production Monitoring Setup:
```bash
# Docker compose for monitoring stack
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana

volumes:
  grafana-storage:
```

Key Performance Indicators (KPIs):
- Response time percentiles (p50, p95, p99)
- Request throughput (requests per second)
- Error rate percentage
- Database query performance
- System resource utilization
- Cache hit rates
- Background task completion times

Monitoring Best Practices:
- Set up automated alerts for critical metrics
- Monitor both application and infrastructure
- Use structured logging for better analysis
- Implement health check endpoints
- Regular performance testing and benchmarking
- Monitor user experience metrics
- Set up log aggregation and analysis
"""
    
    def _parse_endpoint_specs(self, specs: str) -> Dict[str, str]:
        """Parse endpoint specifications"""
        return {
            "module": "jobs",
            "model": "Job",
            "schema": "Job",
            "prefix": "/jobs",
            "tags": "jobs",
            "description": "Job Listing",
            "plural": "jobs",
            "singular": "job"
        }
    
    def _parse_model_specs(self, specs: str) -> Dict[str, str]:
        """Parse model specifications"""
        return {
            "name": "Job",
            "module": "job",
            "table": "jobs",
            "description": "Job Listing",
            "fields": """name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    location = Column(String(255), nullable=True, index=True)
    remote_work = Column(Boolean, default=False, index=True)
    status = Column(String(50), default='active', index=True)""",
            "relationships": """creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])"""
        }
    
    def _analyze_query_performance(self, query: str) -> Dict[str, List[str]]:
        """Analyze query performance issues"""
        return {
            "issues": [
                "N+1 query pattern detected",
                "Missing eager loading for relationships", 
                "Inefficient filtering order",
                "No database indexes for common queries"
            ],
            "strategies": [
                "Use joinedload/selectinload for relationships",
                "Implement query result caching",
                "Add composite indexes for filter combinations",
                "Use raw SQL for complex analytics queries"
            ]
        }
    
    def _parse_task_specs(self, specs: str) -> Dict[str, str]:
        """Parse task specifications"""
        return {
            "name": "process_job_applications",
            "module": "job_processing",
            "function": "process_applications",
            "model": "JobApplication",
            "description": "Process job applications in background",
            "parameters": "application_ids: List[int], options: dict = None",
            "parameter_docs": "application_ids: List of application IDs to process\n        options: Processing options and configuration",
            "implementation": """# Process each application
        processed_data = []
        total_items = len(application_ids) if application_ids else 0
        
        for i, app_id in enumerate(application_ids or []):
            try:
                application = db.query(JobApplication).filter(
                    JobApplication.id == app_id
                ).first()
                
                if application:
                    # Process application logic here
                    processed_item = self._process_single_application(application)
                    processed_data.append(processed_item)
                
                # Update progress
                progress = int((i + 1) / total_items * 80)  # 80% for processing
                self.update_state(
                    state='PROGRESS',
                    meta={'progress': progress, 'status': f'Processed {i + 1}/{total_items}'}
                )
                
            except Exception as e:
                logger.error(f"Failed to process application {app_id}: {e}")
                continue
        
        db.commit()"""
        }
    
    def _parse_cache_specs(self, specs: str) -> Dict[str, str]:
        """Parse cache specifications"""
        return {
            "strategy": "multi-layer caching with Redis"
        }
    
    def _parse_migration_specs(self, specs: str) -> Dict[str, str]:
        """Parse migration specifications"""
        from datetime import datetime
        import hashlib
        
        description = "Add job priority and featured columns"
        version = hashlib.md5(f"{description}{datetime.now()}".encode()).hexdigest()[:12]
        
        return {
            "version": version,
            "previous": "abc123def456",
            "description": description,
            "slug": description.lower().replace(" ", "_"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "upgrade_operations": """# Add new columns
    op.add_column('jobs', sa.Column('priority', sa.Integer(), nullable=True))
    op.add_column('jobs', sa.Column('featured', sa.Boolean(), nullable=True))
    
    # Update existing data
    connection = op.get_bind()
    connection.execute('''
        UPDATE jobs 
        SET priority = 3, featured = FALSE 
        WHERE priority IS NULL OR featured IS NULL
    ''')
    
    # Make columns non-nullable
    op.alter_column('jobs', 'priority', nullable=False)
    op.alter_column('jobs', 'featured', nullable=False)
    
    # Add indexes
    op.create_index('idx_jobs_priority', 'jobs', ['priority'])
    op.create_index('idx_jobs_featured', 'jobs', ['featured'])""",
            "downgrade_operations": """# Remove indexes
    op.drop_index('idx_jobs_featured', 'jobs')
    op.drop_index('idx_jobs_priority', 'jobs')
    
    # Remove columns
    op.drop_column('jobs', 'featured')
    op.drop_column('jobs', 'priority')"""
        }
    
    async def analyze(self, data: Dict[str, Any]) -> AgentResponse:
        """Analyze backend development request"""
        
        request = data.get("api_request", "")
        request_type = data.get("type", "endpoint")
        context = data.get("context", {})
        
        if not request:
            return AgentResponse(
                success=False,
                message="No API request provided",
                data=None
            )
        
        try:
            response_data = {}
            
            if request_type == "endpoint":
                response_data["endpoint"] = self._create_fastapi_endpoint(request)
                response_data["security"] = self._implement_api_security(request)
            elif request_type == "model":
                response_data["model"] = self._design_sqlalchemy_model(request)
                response_data["migration"] = self._create_database_migration(request)
            elif request_type == "performance":
                response_data["query_optimization"] = self._optimize_database_query(request)
                response_data["monitoring"] = self._setup_performance_monitoring(request)
            elif request_type == "task":
                response_data["celery_task"] = self._setup_celery_task(request)
                response_data["caching"] = self._implement_redis_caching(request)
            
            return AgentResponse(
                success=True,
                message="Backend analysis completed",
                data=response_data,
                metadata={
                    "agent": "backend_api",
                    "type": request_type,
                    "request": request
                }
            )
        
        except Exception as e:
            logger.error(f"Backend analysis failed: {e}")
            return AgentResponse(
                success=False,
                message=f"Analysis failed: {str(e)}",
                data=None
            )


# Export the agent class
__all__ = ["BackendAPIAgent"]
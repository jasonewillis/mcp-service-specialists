#!/usr/bin/env python3
"""
Alembic Migration Specialist for Fed Job Advisor

Embedded knowledge for Alembic 1.13.1 with PostgreSQL
Specialized for federal job data schema patterns and migration strategies.

CRITICAL VERSIONS:
- alembic==1.13.1
- sqlalchemy==2.0.25
- psycopg2-binary==2.9.9
- PostgreSQL (primary database)

WARNING: Alembic 1.13.1 has breaking changes from 1.12.x
WARNING: SQLAlchemy 2.0.25 requires different migration patterns
WARNING: Federal job data has complex relationships requiring careful migration order
"""

import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re
import structlog

# Embedded knowledge base for Fed Job Advisor Alembic patterns
ALEMBIC_SPECIALIST_KNOWLEDGE = {
    "version_compatibility": {
        "alembic": "1.13.1",
        "sqlalchemy": "2.0.25",
        "psycopg2": "2.9.9",
        "postgresql_min_version": "12.0",
        "breaking_changes_from_1_12": [
            "Config object initialization changed",
            "Revision file template format updated", 
            "Environment configuration requirements modified"
        ]
    },
    
    "federal_schema_patterns": {
        "core_tables": {
            "users": {
                "primary_keys": ["id"],
                "indexes": ["email", "created_at"],
                "constraints": ["unique_email"],
                "migration_priority": 1
            },
            "job_announcements": {
                "primary_keys": ["announcement_id"],
                "indexes": ["agency_code", "series", "grade", "close_date", "created_at"],
                "constraints": ["valid_close_date", "valid_grade_range"],
                "migration_priority": 2
            },
            "agencies": {
                "primary_keys": ["agency_code"],
                "indexes": ["agency_name"],
                "constraints": ["unique_agency_code"],
                "migration_priority": 1
            },
            "job_series": {
                "primary_keys": ["series_code"],
                "indexes": ["title", "category"],
                "constraints": ["valid_series_format"],
                "migration_priority": 1
            },
            "salary_tables": {
                "primary_keys": ["id"],
                "indexes": ["series", "grade", "step", "locality", "effective_date"],
                "constraints": ["valid_salary_range", "valid_effective_date"],
                "migration_priority": 1
            }
        },
        "relationship_tables": {
            "user_applications": {
                "foreign_keys": ["user_id", "announcement_id"],
                "indexes": ["application_date", "status"],
                "migration_priority": 3
            },
            "job_requirements": {
                "foreign_keys": ["announcement_id"],
                "indexes": ["requirement_type"],
                "migration_priority": 3
            },
            "user_qualifications": {
                "foreign_keys": ["user_id"],
                "indexes": ["qualification_type", "verification_status"],
                "migration_priority": 3
            }
        }
    },
    
    "migration_strategies": {
        "schema_changes": {
            "add_column": "Use batch operations for large tables",
            "drop_column": "Create backup, verify no dependencies, use batch",
            "rename_column": "Use op.alter_column with new_column_name",
            "change_type": "Create new column, migrate data, drop old column",
            "add_constraint": "Create constraint with NOT VALID, then validate",
            "add_index": "Use CONCURRENTLY for production (outside transaction)"
        },
        "data_migrations": {
            "federal_data_import": "Use batch processing for large USAJobs imports",
            "salary_table_updates": "Preserve historical data, add effective_date",
            "user_data_migration": "Encrypt PII during migration",
            "cleanup_old_jobs": "Archive before delete, respect retention policies"
        },
        "performance_considerations": {
            "large_table_alters": "Use batch operations with batch_size=1000",
            "index_creation": "Create indexes CONCURRENTLY in production",
            "foreign_key_addition": "Add as NOT VALID first, then validate",
            "data_type_changes": "Test conversion on subset first"
        }
    },
    
    "postgresql_specifics": {
        "extensions": {
            "required": ["uuid-ossp", "pg_trgm", "btree_gin"],
            "optional": ["hstore", "jsonb", "full_text_search"]
        },
        "data_types": {
            "federal_specific": {
                "announcement_id": "VARCHAR(50)",  # USAJobs format
                "agency_code": "VARCHAR(10)",
                "series_code": "VARCHAR(10)", 
                "grade": "INTEGER",
                "salary": "DECIMAL(10,2)",
                "security_clearance": "VARCHAR(50)"
            }
        },
        "performance_features": {
            "partial_indexes": "For status columns with many NULL values",
            "gin_indexes": "For JSONB qualification data",
            "btree_gin": "For composite indexes on federal data"
        }
    },
    
    "critical_warnings": {
        "alembic_1_13_1_changes": [
            "Config.get_main_option() behavior changed",
            "Revision template variables updated",
            "Environment script imports may need updating",
            "Batch operations syntax slightly different"
        ],
        "sqlalchemy_2_0_25_issues": [
            "Legacy Query interface deprecated",
            "String-based queries discouraged",
            "Relationship loading strategies changed",
            "Connection handling patterns updated"
        ],
        "federal_data_gotchas": [
            "USAJobs announcement IDs can change format",
            "Agency codes are not always stable",
            "Salary tables have complex locality relationships",
            "Job series codes follow OPM standards - don't modify",
            "Close dates are critical - never allow NULL"
        ],
        "production_migration_risks": [
            "Federal job data is time-sensitive - minimize downtime",
            "User applications must never be lost during migration",
            "Salary calculations depend on precise data types",
            "Search indexes critical for performance"
        ]
    }
}

class AlembicMigrationSpecialist:
    """
    Fed Job Advisor Alembic Migration Specialist
    
    Provides comprehensive migration solutions for federal job search application
    with embedded knowledge for Alembic 1.13.1 and PostgreSQL patterns.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
        self.knowledge = ALEMBIC_SPECIALIST_KNOWLEDGE
        
    def create_alembic_ini_config(self, db_url: str = None) -> str:
        """
        Create alembic.ini configuration for Fed Job Advisor
        
        Args:
            db_url: Database URL (if None, uses environment variable)
            
        Returns:
            Complete alembic.ini file content
        """
        return f'''
# Alembic Config for Fed Job Advisor
# Version: 1.13.1

[alembic]
# Path to migration scripts
script_location = alembic

# Template used to generate migration files
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# Timezone for migration timestamps
timezone = UTC

# Max length of characters to apply to the
# "slug" field
truncate_slug_length = 40

# Set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
revision_environment = false

# Set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
sourceless = false

# Version path separator; defaults to os.pathsep
version_path_separator = :

# The output encoding used when revision files
# are written from script.py.mako
output_encoding = utf-8

# Database URL for Fed Job Advisor
sqlalchemy.url = {db_url or 'postgresql://fedjobs_user:password@localhost/fedjobs_db'}

[post_write_hooks]
# Post-write hooks to run after generating migration files
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = --line-length 88

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %%(levelname)-5.5s [%%(name)s] %%(message)s
datefmt = %%H:%%M:%%S
'''

    def create_env_py(self) -> str:
        """
        Create env.py file for Fed Job Advisor migrations
        
        Returns:
            Complete env.py file content for Alembic 1.13.1
        """
        return '''
"""
Alembic environment configuration for Fed Job Advisor
Compatible with Alembic 1.13.1 and SQLAlchemy 2.0.25
"""

import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your application's models
from agents.app.models.base import Base
from agents.app.models.user import User
from agents.app.models.job_announcement import JobAnnouncement
from agents.app.models.agency import Agency
from agents.app.models.job_series import JobSeries
from agents.app.models.salary_table import SalaryTable
from agents.app.models.user_application import UserApplication

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support
target_metadata = Base.metadata

def get_database_url():
    """Get database URL from environment or config"""
    url = os.getenv("DATABASE_URL")
    if url:
        # Handle Heroku postgres:// URLs
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url
    return config.get_main_option("sqlalchemy.url")

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well. By skipping the Engine
    creation we don't even need a DBAPI to be available.
    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Federal job data specific options
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True  # For better PostgreSQL compatibility
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine and associate
    a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()
    
    # Create engine with federal job specific settings
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # PostgreSQL specific optimizations for federal data
        connect_args={
            "options": "-c timezone=UTC",  # Always use UTC for federal data
            "application_name": "fedjobs_migration"
        }
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Federal job migration specific options
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
            transaction_per_migration=True,  # Safer for large federal datasets
            # Include custom comparison functions
            include_object=include_object,
            include_name=include_name
        )

        with context.begin_transaction():
            context.run_migrations()

def include_object(object, name, type_, reflected, compare_to):
    """
    Decide whether to include an object in the migration.
    
    Exclude temporary tables and certain federal data views.
    """
    if type_ == "table":
        # Skip temporary tables
        if name.startswith("temp_"):
            return False
        # Skip certain system tables
        if name in ["spatial_ref_sys", "geography_columns", "geometry_columns"]:
            return False
    return True

def include_name(name, type_, parent_names):
    """
    Decide whether to include a name in the migration.
    
    Filter out test and temporary objects.
    """
    if type_ == "schema":
        return name in [None, "public", "fedjobs"]
    return True

# Run the appropriate migration mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''

    def create_base_migration_template(self) -> str:
        """
        Create base migration template for federal job data
        
        Returns:
            Migration template with federal job specific patterns
        """
        return '''
"""
${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# Revision identifiers
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade() -> None:
    """
    Apply migration changes.
    
    Federal job data migration guidelines:
    1. Always backup critical tables before major changes
    2. Use batch operations for large tables (job_announcements, users)
    3. Create indexes CONCURRENTLY for production
    4. Validate data integrity after schema changes
    """
    ${upgrades if upgrades else "pass"}

def downgrade() -> None:
    """
    Revert migration changes.
    
    Warning: Downgrading federal job data requires careful consideration:
    1. Ensure no application deadlines are affected
    2. Preserve user application data
    3. Maintain salary calculation accuracy
    """
    ${downgrades if downgrades else "pass"}

# Helper functions for federal job migrations
def create_federal_table_with_audit(table_name: str, *columns):
    """Create table with standard federal audit columns"""
    audit_columns = [
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(100), nullable=True),
        sa.Column('updated_by', sa.String(100), nullable=True)
    ]
    
    all_columns = list(columns) + audit_columns
    op.create_table(table_name, *all_columns)
    
    # Create updated_at trigger for PostgreSQL
    op.execute(f"""
        CREATE OR REPLACE FUNCTION update_modified_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    op.execute(f"""
        CREATE TRIGGER update_{table_name}_modtime
        BEFORE UPDATE ON {table_name}
        FOR EACH ROW EXECUTE FUNCTION update_modified_column();
    """)

def add_federal_indexes(table_name: str, indexes: list):
    """Add indexes optimized for federal job searches"""
    for index_def in indexes:
        if isinstance(index_def, str):
            # Simple column index
            op.create_index(f"ix_{table_name}_{index_def}", table_name, [index_def])
        elif isinstance(index_def, dict):
            # Complex index definition
            name = index_def.get('name', f"ix_{table_name}_{index_def['columns'][0]}")
            op.create_index(
                name, 
                table_name, 
                index_def['columns'],
                unique=index_def.get('unique', False),
                postgresql_using=index_def.get('using', 'btree'),
                postgresql_where=index_def.get('where')
            )
'''

    def generate_initial_schema_migration(self) -> str:
        """
        Generate initial schema migration for Fed Job Advisor
        
        Returns:
            Complete initial migration with all federal job tables
        """
        return '''
"""
Initial schema for Fed Job Advisor

Creates core tables for federal job search application with proper
relationships, constraints, and indexes optimized for USAJobs data.

Revision ID: 001_initial_schema
Revises: 
Create Date: 2024-01-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# Revision identifiers
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Create initial federal job advisor schema"""
    
    # Enable required PostgreSQL extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pg_trgm"')
    
    # Create core reference tables first (migration priority 1)
    
    # Agencies table
    op.create_table('agencies',
        sa.Column('agency_code', sa.String(10), primary_key=True),
        sa.Column('agency_name', sa.String(200), nullable=False),
        sa.Column('parent_agency_code', sa.String(10), nullable=True),
        sa.Column('website_url', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['parent_agency_code'], ['agencies.agency_code']),
    )
    op.create_index('ix_agencies_name', 'agencies', ['agency_name'])
    op.create_index('ix_agencies_active', 'agencies', ['is_active'])
    
    # Job series table
    op.create_table('job_series',
        sa.Column('series_code', sa.String(10), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_job_series_title', 'job_series', ['title'])
    op.create_index('ix_job_series_category', 'job_series', ['category'])
    
    # Salary tables
    op.create_table('salary_tables',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('pay_plan', sa.String(10), nullable=False),  # GS, WG, etc.
        sa.Column('series', sa.String(10), nullable=True),
        sa.Column('grade', sa.Integer(), nullable=False),
        sa.Column('step', sa.Integer(), nullable=False),
        sa.Column('locality_code', sa.String(10), nullable=False, default='REST_OF_US'),
        sa.Column('annual_salary', sa.Numeric(10, 2), nullable=False),
        sa.Column('hourly_rate', sa.Numeric(8, 2), nullable=True),
        sa.Column('effective_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint('grade >= 1 AND grade <= 15', name='valid_grade_range'),
        sa.CheckConstraint('step >= 1 AND step <= 10', name='valid_step_range'),
        sa.CheckConstraint('annual_salary > 0', name='positive_salary'),
    )
    op.create_index('ix_salary_tables_lookup', 'salary_tables', 
                   ['pay_plan', 'grade', 'step', 'locality_code', 'effective_date'])
    op.create_index('ix_salary_tables_effective', 'salary_tables', ['effective_date'])
    
    # Users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=True),  # Nullable for OAuth users
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('phone_number', sa.String(20), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('citizenship_status', sa.String(50), nullable=True),
        sa.Column('veteran_status', sa.String(50), nullable=True),
        sa.Column('security_clearance', sa.String(50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('subscription_tier', sa.String(20), nullable=False, default='free'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_active', 'users', ['is_active'])
    op.create_index('ix_users_subscription', 'users', ['subscription_tier'])
    
    # Job announcements table (migration priority 2)
    op.create_table('job_announcements',
        sa.Column('announcement_id', sa.String(50), primary_key=True),
        sa.Column('position_title', sa.String(300), nullable=False),
        sa.Column('agency_code', sa.String(10), nullable=False),
        sa.Column('series_code', sa.String(10), nullable=False),
        sa.Column('grade_low', sa.Integer(), nullable=True),
        sa.Column('grade_high', sa.Integer(), nullable=True),
        sa.Column('salary_min', sa.Numeric(10, 2), nullable=True),
        sa.Column('salary_max', sa.Numeric(10, 2), nullable=True),
        sa.Column('location_city', sa.String(100), nullable=True),
        sa.Column('location_state', sa.String(50), nullable=True),
        sa.Column('location_country', sa.String(50), nullable=False, default='United States'),
        sa.Column('remote_eligible', sa.Boolean(), nullable=False, default=False),
        sa.Column('open_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('close_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('application_url', sa.String(1000), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('qualifications', sa.Text(), nullable=True),
        sa.Column('duties', sa.Text(), nullable=True),
        sa.Column('security_clearance_required', sa.String(50), nullable=True),
        sa.Column('travel_percentage', sa.Integer(), nullable=True),
        sa.Column('telework_eligible', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_sync_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['agency_code'], ['agencies.agency_code']),
        sa.ForeignKeyConstraint(['series_code'], ['job_series.series_code']),
        sa.CheckConstraint('close_date > open_date', name='valid_date_range'),
        sa.CheckConstraint('grade_low IS NULL OR (grade_low >= 1 AND grade_low <= 15)', name='valid_grade_low'),
        sa.CheckConstraint('grade_high IS NULL OR (grade_high >= 1 AND grade_high <= 15)', name='valid_grade_high'),
        sa.CheckConstraint('travel_percentage IS NULL OR (travel_percentage >= 0 AND travel_percentage <= 100)', name='valid_travel_percentage'),
    )
    
    # Critical indexes for job search performance
    op.create_index('ix_job_announcements_agency', 'job_announcements', ['agency_code'])
    op.create_index('ix_job_announcements_series', 'job_announcements', ['series_code'])
    op.create_index('ix_job_announcements_grades', 'job_announcements', ['grade_low', 'grade_high'])
    op.create_index('ix_job_announcements_location', 'job_announcements', ['location_state', 'location_city'])
    op.create_index('ix_job_announcements_dates', 'job_announcements', ['open_date', 'close_date'])
    op.create_index('ix_job_announcements_active', 'job_announcements', ['is_active'])
    op.create_index('ix_job_announcements_remote', 'job_announcements', ['remote_eligible'])
    
    # Full-text search index for job titles and descriptions
    op.execute("""
        CREATE INDEX ix_job_announcements_title_search 
        ON job_announcements 
        USING gin(to_tsvector('english', position_title))
    """)
    
    # Relationship tables (migration priority 3)
    
    # User applications
    op.create_table('user_applications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('announcement_id', sa.String(50), nullable=False),
        sa.Column('application_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, default='draft'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('resume_version', sa.String(100), nullable=True),
        sa.Column('cover_letter', sa.Text(), nullable=True),
        sa.Column('application_url', sa.String(1000), nullable=True),
        sa.Column('usajobs_application_id', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['announcement_id'], ['job_announcements.announcement_id']),
        sa.UniqueConstraint('user_id', 'announcement_id', name='unique_user_application'),
    )
    op.create_index('ix_user_applications_user', 'user_applications', ['user_id'])
    op.create_index('ix_user_applications_announcement', 'user_applications', ['announcement_id'])
    op.create_index('ix_user_applications_date', 'user_applications', ['application_date'])
    op.create_index('ix_user_applications_status', 'user_applications', ['status'])
    
    # Job requirements
    op.create_table('job_requirements',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('announcement_id', sa.String(50), nullable=False),
        sa.Column('requirement_type', sa.String(50), nullable=False),  # education, experience, clearance, etc.
        sa.Column('requirement_text', sa.Text(), nullable=False),
        sa.Column('is_mandatory', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['announcement_id'], ['job_announcements.announcement_id'], ondelete='CASCADE'),
    )
    op.create_index('ix_job_requirements_announcement', 'job_requirements', ['announcement_id'])
    op.create_index('ix_job_requirements_type', 'job_requirements', ['requirement_type'])
    
    # User qualifications
    op.create_table('user_qualifications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('qualification_type', sa.String(50), nullable=False),
        sa.Column('qualification_data', postgresql.JSONB(), nullable=False),
        sa.Column('verification_status', sa.String(20), nullable=False, default='unverified'),
        sa.Column('verification_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expiration_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_user_qualifications_user', 'user_qualifications', ['user_id'])
    op.create_index('ix_user_qualifications_type', 'user_qualifications', ['qualification_type'])
    op.create_index('ix_user_qualifications_status', 'user_qualifications', ['verification_status'])
    
    # Create updated_at triggers for all tables
    tables_with_updated_at = [
        'agencies', 'job_series', 'salary_tables', 'users', 
        'job_announcements', 'user_applications', 'user_qualifications'
    ]
    
    # Create the trigger function
    op.execute("""
        CREATE OR REPLACE FUNCTION update_modified_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    # Add triggers to tables
    for table in tables_with_updated_at:
        op.execute(f"""
            CREATE TRIGGER update_{table}_modtime
            BEFORE UPDATE ON {table}
            FOR EACH ROW EXECUTE FUNCTION update_modified_column();
        """)

def downgrade() -> None:
    """Drop all federal job advisor tables"""
    
    # Drop triggers first
    tables_with_updated_at = [
        'agencies', 'job_series', 'salary_tables', 'users',
        'job_announcements', 'user_applications', 'user_qualifications'
    ]
    
    for table in tables_with_updated_at:
        op.execute(f"DROP TRIGGER IF EXISTS update_{table}_modtime ON {table}")
    
    op.execute("DROP FUNCTION IF EXISTS update_modified_column()")
    
    # Drop tables in reverse dependency order
    op.drop_table('user_qualifications')
    op.drop_table('job_requirements')
    op.drop_table('user_applications')
    op.drop_table('job_announcements')
    op.drop_table('users')
    op.drop_table('salary_tables')
    op.drop_table('job_series')
    op.drop_table('agencies')
'''

    def create_migration_commands(self) -> Dict[str, str]:
        """
        Create common migration commands for Fed Job Advisor
        
        Returns:
            Dictionary of migration command examples
        """
        return {
            "generate_migration": """
# Generate new migration
alembic revision --autogenerate -m "Add user preferences table"

# Generate migration with custom template
alembic revision --autogenerate -m "Update salary calculation fields" --rev-id "002_salary_updates"
            """,
            
            "apply_migrations": """
# Apply all pending migrations
alembic upgrade head

# Apply to specific revision
alembic upgrade ae1027a6acf

# Apply one migration at a time (safer for production)
alembic upgrade +1
            """,
            
            "rollback_migrations": """
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade ae1027a6acf

# Rollback to base (WARNING: destroys all data)
alembic downgrade base
            """,
            
            "check_status": """
# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic show

# Validate migration integrity
alembic check
            """,
            
            "data_migrations": """
# Generate data migration (no autogenerate)
alembic revision -m "Migrate salary data to new format"

# Run specific data migration
alembic upgrade +1 --sql  # Generate SQL only for review
            """,
            
            "production_migrations": """
# Production deployment steps:
1. Backup database: pg_dump fedjobs_db > backup_$(date +%Y%m%d).sql
2. Test migration on copy: alembic upgrade head --sql > migration.sql
3. Review migration.sql for safety
4. Apply with minimal downtime: alembic upgrade head
5. Verify data integrity
6. Update application deployment
            """
        }
    
    def get_migration_best_practices(self) -> List[str]:
        """
        Get migration best practices for Fed Job Advisor
        
        Returns:
            List of best practices specific to federal job data
        """
        return [
            "Always backup production database before major migrations",
            "Test migrations on production-sized dataset copy",
            "Use batch operations for tables with >100K rows (job_announcements, users)",
            "Create indexes CONCURRENTLY in production to avoid blocking",
            "Add foreign key constraints as NOT VALID first, then validate",
            "Preserve federal job application deadlines during schema changes",
            "Never modify job_series codes without OPM approval",
            "Maintain salary calculation accuracy during data type changes",
            "Use transactions for related table changes (users + user_qualifications)",
            "Set maintenance windows for migrations affecting job search",
            "Verify USAJobs API integration after schema changes",
            "Monitor query performance after adding/removing indexes",
            "Document all federal-specific business logic in migrations",
            "Use descriptive migration messages including ticket numbers",
            "Test rollback procedures in staging environment",
            "Coordinate migrations with federal pay table update schedules",
            "Preserve user PII encryption during data migrations",
            "Validate data integrity with federal compliance requirements"
        ]
    
    def create_rollback_strategy(self) -> Dict[str, Any]:
        """
        Create rollback strategy for federal job data migrations
        
        Returns:
            Comprehensive rollback strategy
        """
        return {
            "preparation": {
                "backup_strategy": [
                    "Full database backup before migration",
                    "Table-specific backups for critical data",
                    "Test restore procedures beforehand"
                ],
                "rollback_testing": [
                    "Test rollback on staging environment",
                    "Verify data integrity after rollback",
                    "Test application functionality post-rollback"
                ]
            },
            
            "risk_assessment": {
                "low_risk_changes": [
                    "Adding new columns with defaults",
                    "Creating new indexes",
                    "Adding check constraints"
                ],
                "medium_risk_changes": [
                    "Modifying column types",
                    "Renaming columns", 
                    "Adding foreign keys"
                ],
                "high_risk_changes": [
                    "Dropping columns or tables",
                    "Data migrations",
                    "Changing primary keys"
                ]
            },
            
            "rollback_procedures": {
                "immediate_rollback": "alembic downgrade -1",
                "targeted_rollback": "alembic downgrade {revision_id}",
                "emergency_restore": "pg_restore --clean --create backup_file.sql",
                "data_recovery": "Restore from backup + replay critical transactions"
            },
            
            "federal_specific_considerations": [
                "Preserve job application deadlines",
                "Maintain salary calculation accuracy",
                "Protect user PII during rollback",
                "Coordinate with USAJobs API availability",
                "Consider federal holiday schedules",
                "Notify users of potential service interruption"
            ]
        }
    
    def create_troubleshooting_guide(self) -> Dict[str, Dict[str, str]]:
        """
        Create troubleshooting guide for Alembic issues
        
        Returns:
            Troubleshooting guide for common migration problems
        """
        return {
            "alembic_1_13_1_issues": {
                "config_initialization_error": "Update env.py to use new Config() initialization pattern",
                "template_format_error": "Check file_template format in alembic.ini for new variables",
                "autogenerate_detection_issues": "Verify target_metadata includes all model imports"
            },
            
            "sqlalchemy_2_0_25_issues": {
                "query_deprecation_warnings": "Update to use select() instead of Query.filter()",
                "connection_handling_errors": "Use new connection context management patterns",
                "relationship_loading_issues": "Update eager loading syntax for SQLAlchemy 2.0"
            },
            
            "postgresql_specific": {
                "concurrent_index_creation": "CREATE INDEX CONCURRENTLY outside of transaction",
                "foreign_key_validation_timeout": "Add constraint as NOT VALID, then VALIDATE separately",
                "large_table_lock_issues": "Use batch operations with smaller batch sizes"
            },
            
            "federal_data_issues": {
                "usajobs_id_format_changes": "Update validation patterns for announcement_id format",
                "salary_calculation_errors": "Verify decimal precision for federal pay scales",
                "agency_code_inconsistencies": "Implement data validation before migration",
                "date_timezone_issues": "Ensure all timestamps use UTC for federal compliance"
            },
            
            "performance_issues": {
                "migration_timeout": "Increase statement_timeout for large table operations",
                "memory_usage_spikes": "Use batch operations for large data migrations",
                "slow_index_creation": "Create partial indexes where appropriate",
                "foreign_key_checking_slow": "Disable foreign key checks during bulk operations"
            }
        }
    
    def load_ttl_documentation(self) -> Dict[str, str]:
        """
        Load migration TTL and timing documentation
        
        Returns:
            Documentation about migration timing and data retention
        """
        return {
            "migration_windows": """
            Production Migration Windows for Fed Job Advisor:
            
            Preferred: Sunday 2-6 AM EST (low federal job search activity)
            Acceptable: Weekday 2-4 AM EST (minimal user activity)
            Avoid: Business hours, federal holidays, OPM announcement periods
            
            Maximum Downtime Targets:
            - Schema-only changes: 5 minutes
            - Data migrations: 30 minutes  
            - Major version upgrades: 2 hours (planned maintenance)
            """,
            
            "data_retention": """
            Federal Job Data Retention Requirements:
            
            - Active job announcements: Indefinite (until closed + 90 days)
            - User applications: 7 years (federal record retention)
            - Salary calculations: Permanent (historical pay scale data)
            - User sessions: 24 hours
            - Search cache: 30 minutes
            - Audit logs: 3 years (compliance requirement)
            """,
            
            "backup_schedules": """
            Database Backup Schedule:
            
            - Real-time: WAL-E continuous archiving
            - Daily: Full database backup at 1 AM EST
            - Weekly: Point-in-time recovery test
            - Monthly: Offsite backup validation
            - Before migrations: Manual full backup
            """,
            
            "testing_timelines": """
            Migration Testing Timeline:
            
            Development: Immediate testing with sample data
            Staging: 48 hours before production deployment
            Production: After successful staging validation
            
            Rollback Testing: Within 24 hours of deployment
            Performance Validation: 7 days post-migration
            """
        }

def create_alembic_specialist() -> AlembicMigrationSpecialist:
    """Factory function to create Alembic specialist instance"""
    return AlembicMigrationSpecialist()

# Example usage and testing
if __name__ == "__main__":
    specialist = create_alembic_specialist()
    
    # Generate alembic.ini
    config = specialist.create_alembic_ini_config()
    print("Generated alembic.ini configuration")
    
    # Get migration commands
    commands = specialist.create_migration_commands()
    print(f"Migration commands loaded: {len(commands)} categories")
    
    # Get best practices
    practices = specialist.get_migration_best_practices()
    print(f"Best practices: {len(practices)} recommendations")
    
    # Get troubleshooting guide
    troubleshooting = specialist.create_troubleshooting_guide()
    print(f"Troubleshooting guide: {len(troubleshooting)} categories")
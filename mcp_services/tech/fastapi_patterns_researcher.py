#!/usr/bin/env python3
"""
FastAPI Patterns Researcher - Backend API Expert
Uses mistral:7b for balanced analysis
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import asyncio

class FastAPIResearcher:
    """
    Research-only agent for FastAPI backend patterns
    Specializes in Fed Job Advisor API architecture
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        self.critical_patterns = [
            "Use Pydantic models for validation",
            "Implement dependency injection for DB sessions",
            "Use async/await for all I/O operations",
            "Create proper error handling with HTTPException",
            "Implement OAuth2 with JWT tokens",
            "Use SQLAlchemy ORM with async support",
            "Create background tasks for long operations",
            "Implement proper CORS configuration",
            "Use routers for endpoint organization",
            "Add OpenAPI documentation tags"
        ]
        
        self.fed_job_endpoints = {
            "/api/v1/jobs": "Job search and listing",
            "/api/v1/jobs/{id}": "Job detail retrieval",
            "/api/v1/auth": "Authentication endpoints",
            "/api/v1/users": "User management",
            "/api/v1/salary": "Salary calculations",
            "/api/v1/resume": "Resume parsing/matching",
            "/api/v1/saved": "Saved jobs management",
            "/api/v1/analytics": "User analytics"
        }
        
        self.model = "mistral:7b"  # Good balance
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research FastAPI implementation patterns"""
        
        task_analysis = self._analyze_task(task)
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "task_type": task_analysis['type'],
            "critical_patterns": self.critical_patterns,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "code_templates": self._generate_fastapi_templates(task_analysis),
            "security_checklist": self._get_security_checklist()
        }
        
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "key_pattern": "Async everything with Pydantic validation"
        }
    
    def _analyze_task(self, task: str) -> Dict:
        task_lower = task.lower()
        
        if "endpoint" in task_lower or "route" in task_lower:
            return {"type": "endpoints", "focus": "api_routes"}
        elif "auth" in task_lower:
            return {"type": "authentication", "focus": "jwt_oauth"}
        elif "database" in task_lower or "orm" in task_lower:
            return {"type": "database", "focus": "sqlalchemy"}
        elif "validation" in task_lower:
            return {"type": "validation", "focus": "pydantic"}
        else:
            return {"type": "general", "focus": "api_architecture"}
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict:
        return {
            "summary": f"FastAPI {task_analysis['type']} implementation",
            "project_structure": {
                "app/": "Main application",
                "app/api/": "API endpoints",
                "app/models/": "SQLAlchemy models",
                "app/schemas/": "Pydantic schemas",
                "app/core/": "Core utilities",
                "app/services/": "Business logic",
                "app/db/": "Database config"
            },
            "dependencies": [
                "fastapi==0.104.0",
                "uvicorn[standard]",
                "sqlalchemy[asyncio]",
                "asyncpg",
                "python-jose[cryptography]",
                "passlib[bcrypt]",
                "python-multipart",
                "redis",
                "celery"
            ]
        }
    
    def _generate_fastapi_templates(self, task_analysis: Dict) -> Dict[str, str]:
        templates = {}
        
        if task_analysis["type"] == "endpoints":
            templates["crud_endpoint"] = """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db import get_db
from app.models import Job
from app.schemas import JobResponse, JobSearch
from app.core.auth import get_current_user

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    locality: Optional[str] = Query(None),
    grade: Optional[str] = Query(None),
    series: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db)
):
    \"\"\"Get federal jobs with filters\"\"\"
    
    query = db.query(Job)
    
    if locality:
        query = query.filter(Job.locality == locality)
    if grade:
        query = query.filter(Job.grade == grade)
    if series:
        query = query.filter(Job.series == series)
    
    jobs = await query.offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    \"\"\"Get specific job by ID\"\"\"
    
    job = await db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Track view for analytics
    await track_job_view(job_id, current_user.id, db)
    
    return job"""
        
        elif task_analysis["type"] == "authentication":
            templates["jwt_auth"] = """from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}"""
        
        elif task_analysis["type"] == "database":
            templates["async_sqlalchemy"] = """from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/fedjobadvisor"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    series = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    locality = Column(String, nullable=False)
    salary_min = Column(Float)
    salary_max = Column(Float)
    close_date = Column(DateTime)
    
    # Relationships
    saved_by = relationship("SavedJob", back_populates="job")

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Repository pattern
class JobRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, job_id: str) -> Optional[Job]:
        return await self.db.get(Job, job_id)
    
    async def search(self, filters: JobSearch) -> List[Job]:
        query = select(Job)
        
        if filters.keywords:
            query = query.filter(Job.title.ilike(f"%{filters.keywords}%"))
        if filters.locality:
            query = query.filter(Job.locality == filters.locality)
        
        result = await self.db.execute(query)
        return result.scalars().all()"""
        
        templates["pydantic_schemas"] = """from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class LocalityEnum(str, Enum):
    DC = "washington-dc"
    SF = "san-francisco"
    NYC = "new-york"
    REST = "rest-of-us"

class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    series: str = Field(..., regex="^[0-9]{4}$")
    grade: str = Field(..., regex="^GS-([1-9]|1[0-5])$")
    locality: LocalityEnum
    
    @validator('grade')
    def validate_grade(cls, v):
        parts = v.split('-')
        if len(parts) != 2 or not parts[1].isdigit():
            raise ValueError('Invalid GS grade format')
        grade_num = int(parts[1])
        if not 1 <= grade_num <= 15:
            raise ValueError('Grade must be between GS-1 and GS-15')
        return v

class JobCreate(JobBase):
    description: str
    requirements: List[str]
    
class JobResponse(JobBase):
    id: str
    salary_min: float
    salary_max: float
    close_date: datetime
    saved: bool = False
    
    class Config:
        orm_mode = True

class JobSearch(BaseModel):
    keywords: Optional[str] = None
    locality: Optional[LocalityEnum] = None
    grade: Optional[str] = None
    series: Optional[str] = None
    min_salary: Optional[float] = Field(None, ge=0)
    max_salary: Optional[float] = Field(None, ge=0)
    
    @validator('max_salary')
    def validate_salary_range(cls, v, values):
        if v and 'min_salary' in values and values['min_salary']:
            if v < values['min_salary']:
                raise ValueError('max_salary must be >= min_salary')
        return v"""
        
        return templates
    
    def _get_security_checklist(self) -> List[str]:
        return [
            "Implement rate limiting",
            "Use HTTPS only in production",
            "Validate all inputs with Pydantic",
            "Sanitize user inputs for SQL injection",
            "Implement CORS properly",
            "Use environment variables for secrets",
            "Add request/response logging",
            "Implement API versioning",
            "Use OAuth2 for authentication",
            "Add API key for external services"
        ]
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """Review FastAPI implementation"""
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "compliant": True,
            "violations": [],
            "passed": [],
            "warnings": [],
            "score": 100
        }
        
        # Check for async
        if "async def" in code:
            review["passed"].append("✅ Using async functions")
        else:
            review["violations"].append("❌ Not using async!")
            review["score"] -= 25
        
        # Check for Pydantic
        if "BaseModel" in code or "pydantic" in code:
            review["passed"].append("✅ Using Pydantic models")
        else:
            review["warnings"].append("⚠️ Add Pydantic validation")
            review["score"] -= 15
        
        # Check for dependency injection
        if "Depends" in code:
            review["passed"].append("✅ Using dependency injection")
        
        # Check for error handling
        if "HTTPException" in code:
            review["passed"].append("✅ Proper error handling")
        else:
            review["warnings"].append("⚠️ Add HTTPException handling")
            review["score"] -= 10
        
        review["recommendation"] = "✅ Ready" if review["score"] >= 70 else "❌ Needs improvements"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"fastapi_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# FastAPI Patterns Research\n\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Critical Patterns\n")
            for pattern in research['critical_patterns'][:5]:
                f.write(f"- {pattern}\n")
            f.write("\n")
            
            if research.get('code_templates'):
                f.write("## Code Templates\n")
                for name, template in research['code_templates'].items():
                    f.write(f"### {name}\n```python\n{template}\n```\n\n")
        
        return report_path
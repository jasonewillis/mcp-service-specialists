#!/usr/bin/env python3
"""
Next.js 14 Researcher - Frontend Framework Expert
Uses qwen2.5-coder:7b for code patterns (94% success rate)
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import asyncio

class NextJS14Researcher:
    """
    Research-only agent for Next.js 14 App Router patterns
    Specializes in Fed Job Advisor frontend architecture
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        self.critical_patterns = [
            "ALWAYS use App Router (not Pages Router)",
            "Server Components by default, Client Components when needed",
            "Use 'use client' directive for interactive components",
            "Implement loading.tsx and error.tsx for each route",
            "Use Next.js Image for all images (optimization)",
            "Implement generateStaticParams for dynamic routes",
            "Use server actions for form submissions",
            "Leverage Suspense for streaming SSR",
            "Use middleware for auth checks",
            "Implement proper caching strategies"
        ]
        
        self.fed_job_specific = {
            "routes": [
                "/app/dashboard/page.tsx - Main user dashboard",
                "/app/jobs/[id]/page.tsx - Job detail view",
                "/app/profile/page.tsx - User profile",
                "/app/search/page.tsx - Job search",
                "/app/auth/login/page.tsx - Authentication"
            ],
            "components": [
                "JobCard - Display federal job listing",
                "SalaryCalculator - GS grade calculator",
                "LocalitySelector - 53 locality dropdown",
                "ResumeUploader - Client component",
                "SavedJobsList - Server component with data"
            ]
        }
        
        self.model = "qwen2.5-coder:7b"  # Best for code patterns
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research Next.js 14 implementation patterns"""
        
        task_analysis = self._analyze_task(task)
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "task_type": task_analysis['type'],
            "critical_patterns": self.critical_patterns,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "code_templates": self._generate_nextjs_templates(task_analysis),
            "performance_tips": self._get_performance_tips()
        }
        
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "key_pattern": "Server Components by default"
        }
    
    def _analyze_task(self, task: str) -> Dict:
        task_lower = task.lower()
        
        if "component" in task_lower:
            return {"type": "component", "focus": "react_component"}
        elif "route" in task_lower or "page" in task_lower:
            return {"type": "routing", "focus": "app_router"}
        elif "auth" in task_lower:
            return {"type": "authentication", "focus": "middleware"}
        elif "form" in task_lower:
            return {"type": "forms", "focus": "server_actions"}
        else:
            return {"type": "general", "focus": "app_architecture"}
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict:
        return {
            "summary": f"Next.js 14 {task_analysis['type']} implementation",
            "folder_structure": {
                "app/": "App Router directory",
                "app/api/": "API routes",
                "components/": "Shared components",
                "lib/": "Utilities and helpers",
                "public/": "Static assets"
            },
            "key_files": [
                "app/layout.tsx - Root layout with providers",
                "middleware.ts - Auth and routing logic",
                "next.config.js - Configuration",
                ".env.local - Environment variables"
            ]
        }
    
    def _generate_nextjs_templates(self, task_analysis: Dict) -> Dict[str, str]:
        templates = {}
        
        if task_analysis["type"] == "component":
            templates["server_component"] = """// app/components/JobList.tsx
import { Job } from '@/types'
import { getJobs } from '@/lib/api'
import JobCard from './JobCard'

export default async function JobList({ 
  locality 
}: { 
  locality: string 
}) {
  // This runs on the server
  const jobs = await getJobs(locality)
  
  return (
    <div className="grid gap-4">
      {jobs.map(job => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  )
}"""
            
            templates["client_component"] = """'use client'
// app/components/SaveJobButton.tsx
import { useState } from 'react'
import { saveJob } from '@/app/actions'

export default function SaveJobButton({ 
  jobId 
}: { 
  jobId: string 
}) {
  const [saved, setSaved] = useState(false)
  const [loading, setLoading] = useState(false)
  
  async function handleSave() {
    setLoading(true)
    try {
      await saveJob(jobId)
      setSaved(true)
    } catch (error) {
      console.error('Failed to save job:', error)
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <button
      onClick={handleSave}
      disabled={loading || saved}
      className="btn btn-primary"
    >
      {saved ? 'Saved' : 'Save Job'}
    </button>
  )
}"""
        
        elif task_analysis["type"] == "routing":
            templates["dynamic_route"] = """// app/jobs/[id]/page.tsx
import { notFound } from 'next/navigation'
import { getJob } from '@/lib/api'

export async function generateStaticParams() {
  const jobs = await getPopularJobs()
  return jobs.map((job) => ({
    id: job.id,
  }))
}

export default async function JobPage({ 
  params 
}: { 
  params: { id: string } 
}) {
  const job = await getJob(params.id)
  
  if (!job) {
    notFound()
  }
  
  return (
    <div>
      <h1>{job.title}</h1>
      <p>Grade: {job.grade}</p>
      <p>Locality: {job.locality}</p>
    </div>
  )
}"""
            
            templates["loading_state"] = """// app/jobs/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-3/4 mb-4" />
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-2/3" />
    </div>
  )
}"""
        
        elif task_analysis["type"] == "forms":
            templates["server_action"] = """// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { z } from 'zod'

const JobSearchSchema = z.object({
  keywords: z.string().min(1),
  locality: z.string(),
  grade: z.string().optional(),
})

export async function searchJobs(formData: FormData) {
  const validatedFields = JobSearchSchema.safeParse({
    keywords: formData.get('keywords'),
    locality: formData.get('locality'),
    grade: formData.get('grade'),
  })
  
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    }
  }
  
  const results = await fetch(
    `${process.env.API_URL}/jobs/search`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(validatedFields.data),
    }
  )
  
  revalidatePath('/search')
  redirect(`/search?q=${validatedFields.data.keywords}`)
}"""
        
        return templates
    
    def _get_performance_tips(self) -> List[str]:
        return [
            "Use dynamic imports for heavy components",
            "Implement image optimization with next/image",
            "Use generateStaticParams for known routes",
            "Leverage ISR for semi-static content",
            "Minimize client-side JavaScript",
            "Use Suspense boundaries strategically",
            "Implement proper error boundaries",
            "Cache API responses appropriately"
        ]
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """Review Next.js 14 implementation"""
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "compliant": True,
            "violations": [],
            "passed": [],
            "warnings": [],
            "score": 100
        }
        
        # Check for App Router
        if "app/" in code or "app\\/" in code:
            review["passed"].append("✅ Using App Router")
        else:
            review["violations"].append("❌ Not using App Router!")
            review["score"] -= 30
        
        # Check for 'use client' directive
        if "'use client'" in code or '"use client"' in code:
            review["passed"].append("✅ Client components marked")
        
        # Check for server actions
        if "'use server'" in code or '"use server"' in code:
            review["passed"].append("✅ Using server actions")
        
        # Check for loading states
        if "loading.tsx" in code or "Suspense" in code:
            review["passed"].append("✅ Loading states handled")
        else:
            review["warnings"].append("⚠️ Add loading states")
            review["score"] -= 10
        
        review["recommendation"] = "✅ Ready" if review["score"] >= 70 else "❌ Needs work"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"nextjs14_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write("# Next.js 14 Research Report\n\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Critical Patterns\n")
            for pattern in research['critical_patterns'][:5]:
                f.write(f"- {pattern}\n")
            f.write("\n")
            
            if research.get('code_templates'):
                f.write("## Code Templates\n")
                for name, template in research['code_templates'].items():
                    f.write(f"### {name}\n```typescript\n{template}\n```\n\n")
        
        return report_path
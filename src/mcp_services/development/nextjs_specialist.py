#!/usr/bin/env python3
"""
Next.js Specialist - Modern React Framework Expert
Provides specialized guidance for Next.js 14+ applications with App Router
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
from ..base_specialist import BaseSpecialist

class NextJSSpecialist(BaseSpecialist):
    """
    Specialist agent for Next.js applications and modern React development
    Focuses on App Router, performance optimization, and deployment
    """
    
    def __init__(self):
        super().__init__()
        self.service_name = "nextjs"
        self.specialization = "React Framework & Full-Stack Development"
        
        self.core_expertise = [
            "Next.js 14+ App Router architecture",
            "Server Components and Client Components",
            "Advanced routing and middleware",
            "Performance optimization and caching",
            "Static site generation and ISR",
            "API routes and server actions",
            "Authentication and session management",
            "Deployment and production optimization"
        ]
        
        self.best_practices = [
            "Use Server Components by default, Client Components when needed",
            "Implement proper error boundaries and loading states",
            "Optimize images with next/image component",
            "Use TypeScript for type safety",
            "Implement proper SEO with metadata API",
            "Leverage Next.js caching strategies",
            "Follow security best practices for API routes",
            "Optimize bundle size and Core Web Vitals"
        ]
    
    async def analyze_nextjs_project(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Next.js project structure and provide optimization recommendations"""
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "nextjs_version": project_config.get("version", "unknown"),
            "architecture": "unknown",
            "performance_score": 100,
            "recommendations": [],
            "optimizations": [],
            "security_issues": [],
            "app_router_readiness": {}
        }
        
        # Detect architecture
        if "app" in project_config.get("directories", []):
            analysis["architecture"] = "App Router"
        elif "pages" in project_config.get("directories", []):
            analysis["architecture"] = "Pages Router"
            analysis["recommendations"].append("📦 Consider migrating to App Router for Next.js 14+")
        
        # Performance analysis
        if not project_config.get("typescript", False):
            analysis["recommendations"].append("🔧 Enable TypeScript for better developer experience")
            analysis["performance_score"] -= 10
        
        if not project_config.get("eslint", False):
            analysis["recommendations"].append("🔧 Set up ESLint for code quality")
            analysis["performance_score"] -= 5
        
        # App Router readiness
        analysis["app_router_readiness"] = self._assess_app_router_readiness(project_config)
        
        # Optimization suggestions
        analysis["optimizations"] = self._generate_optimizations(project_config)
        
        return analysis
    
    async def generate_app_structure(self, app_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimal Next.js App Router structure"""
        
        structure = {
            "timestamp": datetime.now().isoformat(),
            "app_type": app_requirements.get("type", "web_app"),
            "structure": {},
            "routing_strategy": {},
            "components_architecture": {},
            "configuration_files": {}
        }
        
        app_type = app_requirements.get("type", "web_app")
        features = app_requirements.get("features", [])
        
        # Generate folder structure
        structure["structure"] = self._generate_folder_structure(app_type, features)
        
        # Routing strategy
        structure["routing_strategy"] = self._design_routing_strategy(features)
        
        # Component architecture
        structure["components_architecture"] = self._design_component_architecture(app_type)
        
        # Configuration files
        structure["configuration_files"] = self._generate_config_files(app_requirements)
        
        return structure
    
    async def optimize_performance(self, performance_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics and provide optimization strategies"""
        
        optimization = {
            "timestamp": datetime.now().isoformat(),
            "current_metrics": performance_metrics,
            "critical_issues": [],
            "improvements": [],
            "caching_strategy": {},
            "bundle_optimization": {},
            "loading_optimization": {}
        }
        
        # Analyze Core Web Vitals
        lcp = performance_metrics.get("lcp", 0)
        fid = performance_metrics.get("fid", 0)
        cls = performance_metrics.get("cls", 0)
        
        if lcp > 2.5:
            optimization["critical_issues"].append("🚨 LCP (Largest Contentful Paint) too slow")
            optimization["improvements"].extend([
                "Optimize images with next/image",
                "Implement static generation where possible",
                "Use CDN for static assets",
                "Optimize font loading"
            ])
        
        if fid > 100:
            optimization["critical_issues"].append("🚨 FID (First Input Delay) too high")
            optimization["improvements"].extend([
                "Reduce JavaScript bundle size",
                "Implement code splitting",
                "Use dynamic imports for heavy components",
                "Optimize third-party scripts"
            ])
        
        if cls > 0.1:
            optimization["critical_issues"].append("🚨 CLS (Cumulative Layout Shift) too high")
            optimization["improvements"].extend([
                "Set explicit dimensions for images and videos",
                "Reserve space for dynamic content",
                "Use CSS aspect-ratio for responsive media"
            ])
        
        # Caching strategy
        optimization["caching_strategy"] = self._design_caching_strategy(performance_metrics)
        
        # Bundle optimization
        optimization["bundle_optimization"] = self._analyze_bundle_optimization(performance_metrics)
        
        return optimization
    
    async def design_authentication_flow(self, auth_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design authentication flow for Next.js application"""
        
        auth_design = {
            "timestamp": datetime.now().isoformat(),
            "auth_type": auth_requirements.get("type", "session"),
            "providers": auth_requirements.get("providers", ["credentials"]),
            "recommended_library": "",
            "implementation_plan": {},
            "security_considerations": [],
            "middleware_setup": ""
        }
        
        # Recommend authentication library
        if "oauth" in auth_requirements.get("providers", []):
            auth_design["recommended_library"] = "NextAuth.js v5 (Auth.js)"
        elif auth_requirements.get("type") == "jwt":
            auth_design["recommended_library"] = "jose + custom implementation"
        else:
            auth_design["recommended_library"] = "NextAuth.js v5 (Auth.js)"
        
        # Implementation plan
        auth_design["implementation_plan"] = self._create_auth_implementation_plan(auth_requirements)
        
        # Security considerations
        auth_design["security_considerations"] = [
            "Use secure session configuration",
            "Implement CSRF protection",
            "Validate all authentication tokens",
            "Use HTTPS in production",
            "Implement rate limiting",
            "Store sensitive data server-side only"
        ]
        
        # Middleware setup
        auth_design["middleware_setup"] = self._generate_auth_middleware(auth_requirements)
        
        return auth_design
    
    async def troubleshoot_nextjs_issue(self, issue_details: Dict[str, Any]) -> Dict[str, Any]:
        """Troubleshoot common Next.js issues and provide solutions"""
        
        troubleshooting = {
            "timestamp": datetime.now().isoformat(),
            "issue_category": self._categorize_issue(issue_details),
            "likely_causes": [],
            "solutions": [],
            "prevention_tips": [],
            "related_docs": []
        }
        
        issue_type = issue_details.get("error", "").lower()
        
        if "hydration" in issue_type or "client" in issue_type:
            troubleshooting["likely_causes"] = [
                "Server and client rendering mismatch",
                "Using browser-only APIs in Server Components",
                "Inconsistent data between server and client"
            ]
            troubleshooting["solutions"] = [
                "Use 'use client' directive for client-specific logic",
                "Implement proper loading states",
                "Use dynamic imports with ssr: false for browser-only components",
                "Ensure consistent data fetching"
            ]
        
        elif "router" in issue_type or "navigation" in issue_type:
            troubleshooting["likely_causes"] = [
                "Incorrect route structure in app directory",
                "Missing page.tsx files",
                "Conflicting route groups"
            ]
            troubleshooting["solutions"] = [
                "Check app directory structure matches Next.js conventions",
                "Ensure each route has a page.tsx file",
                "Review route group organization",
                "Check for conflicting parallel routes"
            ]
        
        elif "build" in issue_type or "compilation" in issue_type:
            troubleshooting["likely_causes"] = [
                "TypeScript errors",
                "Missing dependencies",
                "Configuration issues"
            ]
            troubleshooting["solutions"] = [
                "Run 'npm run type-check' to identify TypeScript issues",
                "Check all dependencies are installed",
                "Verify next.config.js configuration",
                "Clear .next directory and rebuild"
            ]
        
        troubleshooting["related_docs"] = [
            "https://nextjs.org/docs/app/building-your-application/routing",
            "https://nextjs.org/docs/app/building-your-application/rendering",
            "https://nextjs.org/docs/app/api-reference/file-conventions"
        ]
        
        return troubleshooting
    
    def _assess_app_router_readiness(self, project_config: Dict) -> Dict[str, Any]:
        """Assess readiness for App Router migration"""
        return {
            "ready": project_config.get("nextjs_version", "13") >= "13.4",
            "blocking_issues": [
                "Custom _app.js modifications" if project_config.get("custom_app", False) else None,
                "Complex getServerSideProps usage" if project_config.get("ssr_pages", 0) > 5 else None
            ],
            "migration_effort": "Medium" if project_config.get("pages_count", 0) > 10 else "Low",
            "benefits": [
                "Better performance with Server Components",
                "Improved developer experience",
                "Enhanced SEO capabilities",
                "Better caching strategies"
            ]
        }
    
    def _generate_folder_structure(self, app_type: str, features: List[str]) -> Dict[str, Any]:
        """Generate optimal folder structure"""
        base_structure = {
            "app/": {
                "(auth)/": ["login/", "register/", "forgot-password/"],
                "(dashboard)/": ["dashboard/", "settings/"],
                "api/": ["auth/", "users/", "health/"],
                "globals.css": "Global styles",
                "layout.tsx": "Root layout",
                "page.tsx": "Home page",
                "loading.tsx": "Loading UI",
                "error.tsx": "Error UI",
                "not-found.tsx": "404 page"
            },
            "components/": {
                "ui/": "Reusable UI components",
                "forms/": "Form components",
                "layout/": "Layout components"
            },
            "lib/": {
                "auth.ts": "Authentication logic",
                "db.ts": "Database connection",
                "utils.ts": "Utility functions"
            },
            "types/": "TypeScript type definitions"
        }
        
        if "ecommerce" in features:
            base_structure["app/"]["(shop)/"] = ["products/", "cart/", "checkout/"]
        
        if "blog" in features:
            base_structure["app/"]["blog/"] = ["[slug]/"]
        
        return base_structure
    
    def _design_routing_strategy(self, features: List[str]) -> Dict[str, Any]:
        """Design routing strategy based on features"""
        return {
            "route_groups": {
                "(auth)": "Authentication pages without auth layout",
                "(dashboard)": "Protected pages with dashboard layout",
                "(marketing)": "Public marketing pages"
            },
            "parallel_routes": {
                "@modal": "Modal routes for overlays",
                "@sidebar": "Dynamic sidebar content"
            } if "dashboard" in features else {},
            "intercepting_routes": {
                "(..)photo/[id]": "Intercept photo modal on same level"
            } if "gallery" in features else {}
        }
    
    def _design_component_architecture(self, app_type: str) -> Dict[str, Any]:
        """Design component architecture"""
        return {
            "server_components": [
                "Data fetching components",
                "Layout components",
                "Static content components"
            ],
            "client_components": [
                "Interactive UI components",
                "Form components with state",
                "Components using browser APIs"
            ],
            "component_patterns": {
                "composition": "Prefer composition over inheritance",
                "props_drilling": "Use context for deeply nested props",
                "state_management": "Zustand for client state, Server Components for server state"
            }
        }
    
    def _generate_config_files(self, requirements: Dict) -> Dict[str, str]:
        """Generate configuration files"""
        return {
            "next.config.js": """/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@prisma/client']
  },
  images: {
    domains: ['example.com'],
    formats: ['image/avif', 'image/webp']
  }
}

module.exports = nextConfig""",
            "tailwind.config.js": """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}""",
            "middleware.ts": """import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Add your middleware logic here
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}"""
        }
    
    def _design_caching_strategy(self, metrics: Dict) -> Dict[str, Any]:
        """Design caching strategy based on performance metrics"""
        return {
            "static_generation": "Use for content that doesn't change often",
            "incremental_static_regeneration": "Use for content that changes periodically",
            "server_side_rendering": "Use for user-specific content",
            "client_side_caching": "Use React Query or SWR for API calls",
            "cdn_caching": "Configure proper cache headers for static assets"
        }
    
    def _analyze_bundle_optimization(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze bundle optimization opportunities"""
        return {
            "code_splitting": "Implement route-based code splitting",
            "dynamic_imports": "Use dynamic imports for heavy components",
            "tree_shaking": "Ensure unused code is eliminated",
            "bundle_analyzer": "Use @next/bundle-analyzer to identify large dependencies"
        }
    
    def _create_auth_implementation_plan(self, requirements: Dict) -> Dict[str, Any]:
        """Create authentication implementation plan"""
        return {
            "setup_steps": [
                "1. Install NextAuth.js v5",
                "2. Configure auth.ts with providers",
                "3. Set up middleware for protected routes",
                "4. Create login/logout components",
                "5. Implement session management"
            ],
            "estimated_hours": 8,
            "key_files": [
                "lib/auth.ts",
                "middleware.ts",
                "app/api/auth/[...nextauth]/route.ts",
                "components/auth/login-form.tsx"
            ]
        }
    
    def _generate_auth_middleware(self, requirements: Dict) -> str:
        """Generate authentication middleware"""
        return """import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { auth } from '@/lib/auth'

export default auth((req) => {
  const { pathname } = req.nextUrl
  
  // Protect dashboard routes
  if (pathname.startsWith('/dashboard')) {
    if (!req.auth) {
      return NextResponse.redirect(new URL('/login', req.url))
    }
  }
  
  // Redirect authenticated users away from auth pages
  if (pathname.startsWith('/login') || pathname.startsWith('/register')) {
    if (req.auth) {
      return NextResponse.redirect(new URL('/dashboard', req.url))
    }
  }
  
  return NextResponse.next()
})

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}"""
    
    def _categorize_issue(self, issue_details: Dict) -> str:
        """Categorize the type of issue"""
        error = issue_details.get("error", "").lower()
        
        if any(term in error for term in ["hydration", "client", "server"]):
            return "Rendering"
        elif any(term in error for term in ["router", "navigation", "route"]):
            return "Routing"
        elif any(term in error for term in ["build", "compilation", "typescript"]):
            return "Build"
        elif any(term in error for term in ["performance", "slow", "loading"]):
            return "Performance"
        else:
            return "General"

# MCP Tool definitions
async def analyze_nextjs_project(project_config: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze Next.js project structure and provide optimization recommendations"""
    specialist = NextJSSpecialist()
    return await specialist.analyze_nextjs_project(project_config)

async def generate_app_structure(app_requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Generate optimal Next.js App Router structure based on requirements"""
    specialist = NextJSSpecialist()
    return await specialist.generate_app_structure(app_requirements)

async def optimize_performance(performance_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze performance metrics and provide Next.js optimization strategies"""
    specialist = NextJSSpecialist()
    return await specialist.optimize_performance(performance_metrics)

async def design_authentication_flow(auth_requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Design authentication flow for Next.js application with modern patterns"""
    specialist = NextJSSpecialist()
    return await specialist.design_authentication_flow(auth_requirements)

async def troubleshoot_nextjs_issue(issue_details: Dict[str, Any]) -> Dict[str, Any]:
    """Troubleshoot common Next.js issues and provide step-by-step solutions"""
    specialist = NextJSSpecialist()
    return await specialist.troubleshoot_nextjs_issue(issue_details)
#!/usr/bin/env python3
"""
Google OAuth Researcher - Authentication Expert
Uses deepseek-coder-v2:16b for complex auth flows
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import asyncio

class GoogleOAuthResearcher:
    """
    Research-only agent for Google OAuth implementation
    Specializes in secure authentication flows
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        self.critical_rules = [
            "NEVER store OAuth tokens in frontend code",
            "Always validate state parameter to prevent CSRF",
            "Use PKCE for additional security",
            "Store refresh tokens securely (encrypted)",
            "Implement token rotation",
            "Handle token expiration gracefully",
            "Validate ID tokens with Google's public keys",
            "Use secure session management"
        ]
        
        self.model = "deepseek-coder-v2:16b"  # Best for complex auth logic
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """Research Google OAuth implementation"""
        
        task_analysis = self._analyze_task(task)
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "task_type": task_analysis['type'],
            "critical_requirements": self.critical_rules,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "security_checklist": self._create_security_checklist(),
            "code_templates": self._generate_code_templates(task_analysis)
        }
        
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "critical_reminders": self.critical_rules[:3]
        }
    
    def _analyze_task(self, task: str) -> Dict:
        task_lower = task.lower()
        return {
            "type": "oauth_flow" if "oauth" in task_lower else "authentication",
            "operations": ["login", "token_refresh", "logout"],
            "components": ["frontend", "backend", "database"]
        }
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict:
        return {
            "summary": "Google OAuth 2.0 implementation with PKCE",
            "steps": [
                "1. Register app in Google Cloud Console",
                "2. Configure OAuth consent screen",
                "3. Implement authorization endpoint",
                "4. Handle callback with code exchange",
                "5. Validate and store tokens securely",
                "6. Implement refresh token rotation",
                "7. Add logout functionality"
            ],
            "endpoints": [
                "GET /api/v1/auth/google/login",
                "GET /api/v1/auth/google/callback",
                "POST /api/v1/auth/refresh",
                "POST /api/v1/auth/logout"
            ]
        }
    
    def _create_security_checklist(self) -> List[str]:
        return [
            "✓ Use state parameter for CSRF protection",
            "✓ Implement PKCE flow",
            "✓ Validate ID tokens",
            "✓ Secure token storage",
            "✓ HTTPS only",
            "✓ Secure session cookies",
            "✓ Token expiration handling"
        ]
    
    def _generate_code_templates(self, task_analysis: Dict) -> Dict[str, str]:
        return {
            "backend_oauth": """
from fastapi import APIRouter, HTTPException, Depends
from authlib.integrations.starlette_client import OAuth
import secrets

router = APIRouter()
oauth = OAuth()

# Configure Google OAuth
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    token_url='https://oauth2.googleapis.com/token',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get("/auth/google/login")
async def google_login(request: Request):
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state
    
    redirect_uri = f"{BASE_URL}/api/v1/auth/google/callback"
    return await oauth.google.authorize_redirect(
        request, 
        redirect_uri,
        state=state
    )

@router.get("/auth/google/callback")
async def google_callback(request: Request, code: str, state: str):
    # Verify state
    if state != request.session.get('oauth_state'):
        raise HTTPException(400, "Invalid state parameter")
    
    # Exchange code for tokens
    token = await oauth.google.authorize_access_token(request)
    
    # Get user info
    user_info = token.get('userinfo')
    
    # Create or update user
    user = await create_or_update_user(user_info)
    
    # Create session
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user
    }
""",
            "frontend_auth": """
// Frontend OAuth handler (Next.js)
import { signIn, signOut, useSession } from 'next-auth/react';

export function GoogleLoginButton() {
  const { data: session, status } = useSession();
  
  if (status === 'loading') return <p>Loading...</p>;
  
  if (session) {
    return (
      <button onClick={() => signOut()}>
        Sign out
      </button>
    );
  }
  
  return (
    <button onClick={() => signIn('google')}>
      Sign in with Google
    </button>
  );
}
"""
        }
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """Review OAuth implementation for security"""
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "compliant": True,
            "violations": [],
            "passed": [],
            "score": 100
        }
        
        # Security checks
        if "state" not in code.lower():
            review["violations"].append("❌ No CSRF protection (state parameter)")
            review["score"] -= 30
            review["compliant"] = False
        else:
            review["passed"].append("✅ CSRF protection present")
        
        if "https" not in code or "http://" in code:
            review["violations"].append("❌ Not enforcing HTTPS")
            review["score"] -= 20
        
        if "refresh_token" in code:
            review["passed"].append("✅ Refresh token handling")
        
        review["recommendation"] = "✅ Secure" if review["score"] >= 70 else "❌ Security issues found"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"google_oauth_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write(f"# Google OAuth Implementation Research\n\n")
            f.write(f"**Task**: {research['task']}\n\n")
            
            f.write("## Security Requirements\n")
            for req in research['critical_requirements'][:5]:
                f.write(f"- {req}\n")
            f.write("\n")
            
            f.write("## Implementation Steps\n")
            for step in research['implementation_plan']['steps']:
                f.write(f"{step}\n")
            f.write("\n")
            
            if research.get('code_templates'):
                f.write("## Code Templates\n")
                for name, template in research['code_templates'].items():
                    f.write(f"### {name}\n```python\n{template}\n```\n\n")
        
        return report_path
#!/usr/bin/env python3
"""
OAuth Expert - Authentication and Authorization Specialist
Provides expert guidance on OAuth 2.0, OpenID Connect, and secure authentication flows
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
from ..base_specialist import BaseSpecialist

class OAuthExpert(BaseSpecialist):
    """
    Expert agent for OAuth 2.0 and OpenID Connect implementation
    Specializes in secure authentication flows and token management
    """
    
    def __init__(self):
        super().__init__()
        self.service_name = "oauth"
        self.specialization = "Authentication & Authorization"
        
        self.core_expertise = [
            "OAuth 2.0 and OpenID Connect flows",
            "PKCE (Proof Key for Code Exchange)",
            "JWT token validation and management",
            "Secure session management",
            "Multi-provider authentication",
            "Token refresh and rotation",
            "CSRF and security attack prevention",
            "SSO integration patterns"
        ]
        
        self.security_requirements = [
            "NEVER store OAuth tokens in frontend code",
            "Always validate state parameter to prevent CSRF",
            "Use PKCE for additional security in SPAs",
            "Store refresh tokens securely (encrypted)",
            "Implement proper token rotation",
            "Handle token expiration gracefully",
            "Validate ID tokens with provider's public keys",
            "Use secure session management with httpOnly cookies"
        ]
    
    async def design_oauth_flow(self, app_config: Dict[str, Any]) -> Dict[str, Any]:
        """Design OAuth 2.0 flow based on application requirements"""
        
        design = {
            "timestamp": datetime.now().isoformat(),
            "app_type": app_config.get("type", "web"),
            "providers": app_config.get("providers", ["google"]),
            "recommended_flow": "",
            "security_features": [],
            "implementation_plan": {},
            "endpoints": [],
            "security_checklist": self.security_requirements
        }
        
        # Determine optimal flow
        app_type = app_config.get("type", "web")
        if app_type == "spa":
            design["recommended_flow"] = "Authorization Code with PKCE"
            design["security_features"] = ["PKCE", "State parameter", "Secure storage"]
        elif app_type == "mobile":
            design["recommended_flow"] = "Authorization Code with PKCE"
            design["security_features"] = ["PKCE", "Deep linking", "Secure keychain storage"]
        else:  # web app
            design["recommended_flow"] = "Authorization Code"
            design["security_features"] = ["State parameter", "Secure sessions", "HttpOnly cookies"]
        
        design["implementation_plan"] = self._create_implementation_plan(app_config)
        design["endpoints"] = self._generate_endpoint_structure(app_config)
        
        return design
    
    async def validate_oauth_implementation(self, implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Validate OAuth implementation against security best practices"""
        
        validation = {
            "timestamp": datetime.now().isoformat(),
            "security_score": 100,
            "passed_checks": [],
            "failed_checks": [],
            "warnings": [],
            "critical_issues": [],
            "recommendations": []
        }
        
        code = implementation.get("code", "")
        config = implementation.get("config", {})
        
        # Critical security checks
        if "state" not in code.lower():
            validation["critical_issues"].append("❌ Missing CSRF protection (state parameter)")
            validation["security_score"] -= 30
        else:
            validation["passed_checks"].append("✅ CSRF protection implemented")
        
        if app_type := config.get("type") == "spa" and "pkce" not in code.lower():
            validation["critical_issues"].append("❌ Missing PKCE for SPA application")
            validation["security_score"] -= 25
        
        if "https" not in code or "http://" in code:
            validation["failed_checks"].append("❌ Not enforcing HTTPS")
            validation["security_score"] -= 20
        else:
            validation["passed_checks"].append("✅ HTTPS enforcement")
        
        if "refresh_token" in code and "rotation" not in code.lower():
            validation["warnings"].append("⚠️ Consider implementing refresh token rotation")
            validation["security_score"] -= 5
        
        # Token storage checks
        if "localstorage" in code.lower() or "sessionstorage" in code.lower():
            validation["critical_issues"].append("❌ Storing tokens in browser storage (XSS vulnerability)")
            validation["security_score"] -= 35
        
        if "httponly" in code.lower():
            validation["passed_checks"].append("✅ Using httpOnly cookies")
        
        # Generate recommendations
        if validation["security_score"] < 70:
            validation["recommendations"].extend([
                "Implement all critical security requirements",
                "Review token storage mechanisms",
                "Add comprehensive error handling",
                "Implement proper logging for security events"
            ])
        
        validation["overall_rating"] = self._calculate_security_rating(validation["security_score"])
        
        return validation
    
    async def generate_provider_config(self, provider: str, app_type: str = "web") -> Dict[str, Any]:
        """Generate provider-specific OAuth configuration"""
        
        configs = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "app_type": app_type,
            "configuration": {},
            "endpoints": {},
            "scopes": [],
            "implementation_example": ""
        }
        
        if provider.lower() == "google":
            configs.update(self._generate_google_config(app_type))
        elif provider.lower() == "github":
            configs.update(self._generate_github_config(app_type))
        elif provider.lower() == "microsoft":
            configs.update(self._generate_microsoft_config(app_type))
        else:
            configs["configuration"] = {"error": f"Provider {provider} not supported"}
        
        return configs
    
    async def troubleshoot_oauth_issue(self, error_details: Dict[str, Any]) -> Dict[str, Any]:
        """Troubleshoot common OAuth implementation issues"""
        
        troubleshooting = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_details.get("error", "unknown"),
            "likely_causes": [],
            "solutions": [],
            "prevention_tips": [],
            "debug_steps": []
        }
        
        error_type = error_details.get("error", "").lower()
        
        if "invalid_client" in error_type:
            troubleshooting["likely_causes"] = [
                "Incorrect client_id or client_secret",
                "Client not properly registered with provider",
                "Wrong redirect_uri configured"
            ]
            troubleshooting["solutions"] = [
                "Verify client credentials in provider console",
                "Check redirect_uri matches exactly",
                "Ensure client is enabled and not suspended"
            ]
        
        elif "invalid_grant" in error_type or "code" in error_type:
            troubleshooting["likely_causes"] = [
                "Authorization code expired or already used",
                "Incorrect code_verifier for PKCE",
                "Clock skew between servers"
            ]
            troubleshooting["solutions"] = [
                "Ensure codes are used immediately",
                "Verify PKCE code_verifier generation",
                "Check server time synchronization"
            ]
        
        elif "csrf" in error_type or "state" in error_type:
            troubleshooting["likely_causes"] = [
                "State parameter mismatch",
                "Session lost during auth flow",
                "Possible CSRF attack attempt"
            ]
            troubleshooting["solutions"] = [
                "Verify state generation and validation",
                "Check session persistence",
                "Implement proper state cleanup"
            ]
        
        troubleshooting["debug_steps"] = [
            "1. Check provider's developer console for error details",
            "2. Verify all URLs and redirects are HTTPS",
            "3. Test with provider's OAuth playground",
            "4. Check server logs for detailed error messages",
            "5. Validate all required parameters are present"
        ]
        
        return troubleshooting
    
    def _create_implementation_plan(self, app_config: Dict) -> Dict[str, Any]:
        """Create detailed implementation plan"""
        return {
            "phases": [
                "1. Provider Registration and Configuration",
                "2. Backend OAuth Endpoints Implementation", 
                "3. Frontend Integration",
                "4. Security Validation and Testing",
                "5. Error Handling and Edge Cases"
            ],
            "estimated_hours": 16 if app_config.get("type") == "spa" else 12,
            "key_components": [
                "OAuth client configuration",
                "State/PKCE parameter generation",
                "Authorization URL generation",
                "Token exchange endpoint",
                "Token validation and storage",
                "Session management",
                "Logout functionality"
            ]
        }
    
    def _generate_endpoint_structure(self, app_config: Dict) -> List[str]:
        """Generate required API endpoints"""
        base_endpoints = [
            "GET /api/v1/auth/{provider}/login",
            "GET /api/v1/auth/{provider}/callback", 
            "POST /api/v1/auth/refresh",
            "POST /api/v1/auth/logout"
        ]
        
        if app_config.get("type") == "spa":
            base_endpoints.extend([
                "GET /api/v1/auth/session",
                "POST /api/v1/auth/validate"
            ])
        
        return base_endpoints
    
    def _generate_google_config(self, app_type: str) -> Dict[str, Any]:
        """Generate Google OAuth configuration"""
        config = {
            "configuration": {
                "client_id": "your-google-client-id.googleusercontent.com",
                "client_secret": "your-google-client-secret",
                "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_url": "https://oauth2.googleapis.com/token",
                "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
                "scopes": ["openid", "email", "profile"]
            },
            "endpoints": {
                "authorization": "https://accounts.google.com/o/oauth2/v2/auth",
                "token": "https://oauth2.googleapis.com/token",
                "userinfo": "https://www.googleapis.com/oauth2/v2/userinfo",
                "jwks": "https://www.googleapis.com/oauth2/v3/certs"
            }
        }
        
        if app_type == "spa":
            config["implementation_example"] = """
// Google OAuth for SPA with PKCE
import { generateCodeVerifier, generateCodeChallenge } from './pkce';

const codeVerifier = generateCodeVerifier();
const codeChallenge = await generateCodeChallenge(codeVerifier);
const state = crypto.randomUUID();

const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');
authUrl.searchParams.set('client_id', GOOGLE_CLIENT_ID);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('scope', 'openid email profile');
authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
authUrl.searchParams.set('state', state);
authUrl.searchParams.set('code_challenge', codeChallenge);
authUrl.searchParams.set('code_challenge_method', 'S256');

// Store for validation
sessionStorage.setItem('oauth_state', state);
sessionStorage.setItem('code_verifier', codeVerifier);

window.location.href = authUrl.toString();
"""
        else:
            config["implementation_example"] = """
from authlib.integrations.fastapi_client import OAuth

oauth = OAuth()
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
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state
    
    redirect_uri = f"{BASE_URL}/api/v1/auth/google/callback"
    return await oauth.google.authorize_redirect(
        request, redirect_uri, state=state
    )
"""
        
        return config
    
    def _generate_github_config(self, app_type: str) -> Dict[str, Any]:
        """Generate GitHub OAuth configuration"""
        return {
            "configuration": {
                "client_id": "your-github-client-id",
                "client_secret": "your-github-client-secret",
                "authorize_url": "https://github.com/login/oauth/authorize",
                "token_url": "https://github.com/login/oauth/access_token",
                "userinfo_url": "https://api.github.com/user",
                "scopes": ["user:email", "read:user"]
            },
            "endpoints": {
                "authorization": "https://github.com/login/oauth/authorize",
                "token": "https://github.com/login/oauth/access_token",
                "userinfo": "https://api.github.com/user"
            }
        }
    
    def _generate_microsoft_config(self, app_type: str) -> Dict[str, Any]:
        """Generate Microsoft/Azure AD OAuth configuration"""
        return {
            "configuration": {
                "client_id": "your-azure-app-id",
                "client_secret": "your-azure-client-secret",
                "authorize_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                "userinfo_url": "https://graph.microsoft.com/v1.0/me",
                "scopes": ["openid", "profile", "email", "User.Read"]
            },
            "endpoints": {
                "authorization": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                "token": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                "userinfo": "https://graph.microsoft.com/v1.0/me"
            }
        }
    
    def _calculate_security_rating(self, score: int) -> str:
        """Calculate security rating based on score"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Acceptable"
        elif score >= 60:
            return "Needs Improvement"
        else:
            return "Critical Issues"

# MCP Tool definitions
async def design_oauth_flow(app_config: Dict[str, Any]) -> Dict[str, Any]:
    """Design optimal OAuth 2.0 flow based on application requirements"""
    expert = OAuthExpert()
    return await expert.design_oauth_flow(app_config)

async def validate_oauth_implementation(implementation: Dict[str, Any]) -> Dict[str, Any]:
    """Validate OAuth implementation against security best practices"""
    expert = OAuthExpert()
    return await expert.validate_oauth_implementation(implementation)

async def generate_provider_config(provider: str, app_type: str = "web") -> Dict[str, Any]:
    """Generate provider-specific OAuth configuration (Google, GitHub, Microsoft)"""
    expert = OAuthExpert()
    return await expert.generate_provider_config(provider, app_type)

async def troubleshoot_oauth_issue(error_details: Dict[str, Any]) -> Dict[str, Any]:
    """Troubleshoot common OAuth implementation issues and provide solutions"""
    expert = OAuthExpert()
    return await expert.troubleshoot_oauth_issue(error_details)
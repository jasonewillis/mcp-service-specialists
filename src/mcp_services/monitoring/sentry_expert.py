#!/usr/bin/env python3
"""
Sentry Error Expert - Ultra-deep expertise in Sentry error tracking and monitoring
Specialized for production error management in Fed Job Advisor
"""

from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import asyncio
from enum import Enum

class SentryEventLevel(Enum):
    """Sentry event severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    FATAL = "fatal"

class SentryExpert:
    """
    Ultra-specialized agent for Sentry error tracking and performance monitoring
    Complete knowledge of Sentry SDK, configuration, and best practices
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "sentry"
        self.research_output = self.base_path / "research_outputs" / "sentry_monitoring"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Exhaustive Sentry knowledge base
        self.knowledge_base = {
            "sdk_configuration": {
                "python_fastapi": {
                    "installation": "pip install sentry-sdk[fastapi]",
                    "basic_setup": """
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn="https://xxx@xxx.ingest.sentry.io/xxx",
    integrations=[
        FastApiIntegration(
            transaction_style="endpoint",
            failed_request_status_codes=[400, 401, 403, 404, 429, 500]
        ),
        SqlalchemyIntegration(),
        RedisIntegration()
    ],
    traces_sample_rate=0.1,  # 10% of transactions
    profiles_sample_rate=0.1,  # 10% profiling
    environment="production",
    release="fedjobadvisor@1.0.0",
    attach_stacktrace=True,
    send_default_pii=False,  # GDPR compliance
    before_send=before_send_filter,
    before_send_transaction=before_send_transaction_filter
)
""",
                    "error_filtering": """
def before_send_filter(event, hint):
    # Filter out sensitive data
    if 'password' in str(event.get('exception', {})):
        return None
    
    # Filter out specific errors
    if 'ConnectionError' in str(event.get('exception', {})):
        return None
    
    # Scrub sensitive data
    if event.get('request'):
        event['request']['cookies'] = '[Filtered]'
        if event['request'].get('headers'):
            event['request']['headers'] = {
                k: v for k, v in event['request']['headers'].items()
                if k.lower() not in ['authorization', 'cookie', 'x-api-key']
            }
    
    return event
"""
                },
                "javascript_react": {
                    "installation": "npm install @sentry/react @sentry/tracing",
                    "setup": """
import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  integrations: [
    new BrowserTracing(),
    new Sentry.Replay({
      maskAllText: true,
      blockAllMedia: true,
    })
  ],
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  environment: process.env.NODE_ENV,
  beforeSend(event) {
    // Filter out non-critical errors
    if (event.exception?.values?.[0]?.type === 'NetworkError') {
      return null;
    }
    return event;
  }
});
""",
                    "error_boundary": """
import { ErrorBoundary } from "@sentry/react";

function FallbackComponent({ error, resetError }) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={resetError}>Try again</button>
    </div>
  );
}

<ErrorBoundary fallback={FallbackComponent} showDialog>
  <App />
</ErrorBoundary>
"""
                }
            },
            
            "performance_monitoring": {
                "transaction_tracking": {
                    "automatic": "SDK auto-instruments frameworks",
                    "custom_transactions": """
# Start transaction
with sentry_sdk.start_transaction(op="task", name="process_job") as transaction:
    with transaction.start_child(op="db", description="fetch_jobs"):
        jobs = fetch_jobs()
    
    with transaction.start_child(op="process", description="analyze_jobs"):
        results = analyze_jobs(jobs)
    
    transaction.set_tag("job_count", len(jobs))
    transaction.set_data("processing_time", time.time() - start)
""",
                    "sampling_strategies": {
                        "development": 1.0,  # 100% sampling
                        "staging": 0.5,      # 50% sampling
                        "production": 0.1    # 10% sampling
                    }
                },
                "database_queries": {
                    "slow_query_detection": "Automatic with SQLAlchemy integration",
                    "n_plus_one": "Detected via performance insights",
                    "query_spans": "Visible in transaction timeline"
                },
                "api_monitoring": {
                    "endpoint_performance": "Track response times per endpoint",
                    "throughput": "Requests per minute/hour",
                    "error_rates": "4xx and 5xx response tracking"
                }
            },
            
            "error_management": {
                "issue_grouping": {
                    "fingerprinting": """
# Custom fingerprinting rules
sentry_sdk.scope.fingerprint = ['{{ default }}', 'user_id:{{ user.id }}']

# Group by error message
sentry_sdk.scope.fingerprint = ['{{ message }}']

# Group by stack trace
sentry_sdk.scope.fingerprint = ['{{ stack.abs_path }}']
""",
                    "merging": "Merge similar issues manually",
                    "ignoring": "Ignore known non-issues"
                },
                "alerting_rules": {
                    "error_threshold": {
                        "condition": "error_count > 100 in 1 hour",
                        "action": "Send email/Slack notification"
                    },
                    "new_error": {
                        "condition": "first_seen error",
                        "action": "Immediate notification"
                    },
                    "regression": {
                        "condition": "resolved issue reoccurs",
                        "action": "High priority alert"
                    },
                    "performance": {
                        "condition": "p95 response time > 2s",
                        "action": "Performance alert"
                    }
                },
                "issue_assignment": {
                    "auto_assignment": "Based on code ownership",
                    "routing_rules": "By team or component",
                    "escalation": "Unresolved after X hours"
                }
            },
            
            "release_tracking": {
                "release_management": {
                    "versioning": "semver (1.0.0)",
                    "deployment_tracking": """
# Mark release deployment
sentry_cli releases deploys fedjobadvisor@1.0.0 new -e production

# Finalize release
sentry_cli releases finalize fedjobadvisor@1.0.0
""",
                    "source_maps": "Upload for JavaScript",
                    "commits": "Associate commits with release"
                },
                "release_health": {
                    "crash_free_rate": "Users and sessions",
                    "adoption": "Percentage using new version",
                    "regression_detection": "Issues in new release"
                }
            },
            
            "user_feedback": {
                "user_context": """
# Set user context
sentry_sdk.set_user({
    "id": user.id,
    "email": user.email,
    "username": user.username,
    "subscription": user.plan
})

# Add custom context
sentry_sdk.set_context("subscription", {
    "plan": user.plan,
    "status": user.subscription_status,
    "expires": user.subscription_ends_at
})
""",
                "feedback_dialog": """
// JavaScript user feedback
Sentry.showReportDialog({
  user: {
    email: currentUser.email,
    name: currentUser.name
  },
  title: "It looks like we're having issues",
  subtitle: "Our team has been notified",
  subtitle2: "Please describe what happened"
});
""",
                "breadcrumbs": """
# Add custom breadcrumbs
sentry_sdk.add_breadcrumb(
    category='auth',
    message='User logged in',
    level='info',
    data={'user_id': user.id}
)
"""
            },
            
            "integrations": {
                "slack": {
                    "setup": "Add Slack integration in Sentry",
                    "alerts": "Route alerts to channels",
                    "notifications": "#errors, #critical-errors"
                },
                "github": {
                    "issue_linking": "Link Sentry issues to GitHub",
                    "commit_tracking": "See commits that introduced errors",
                    "pr_comments": "Comment on PRs with new errors"
                },
                "jira": {
                    "issue_creation": "Auto-create JIRA tickets",
                    "two_way_sync": "Sync status between systems"
                }
            },
            
            "data_security": {
                "pii_scrubbing": {
                    "automatic": "Default PII scrubbing enabled",
                    "custom_rules": "Define custom scrub patterns",
                    "data_types": ["emails", "ip_addresses", "credit_cards"]
                },
                "gdpr_compliance": {
                    "user_deletion": "Delete user data on request",
                    "data_retention": "90 days default",
                    "consent": "Track user consent"
                },
                "security_headers": {
                    "csp_reporting": "Content-Security-Policy reports",
                    "cors_errors": "Cross-origin errors",
                    "ssl_errors": "Certificate issues"
                }
            },
            
            "fed_job_advisor_setup": {
                "critical_transactions": {
                    "job_search": {
                        "name": "api.job_search",
                        "performance_target": "< 500ms"
                    },
                    "payment_processing": {
                        "name": "stripe.payment",
                        "alert_on_failure": True
                    },
                    "user_authentication": {
                        "name": "auth.login",
                        "track_failures": True
                    }
                },
                "custom_tags": {
                    "subscription_tier": ["local", "mobile"],
                    "api_version": "v1",
                    "deployment": ["production", "staging"]
                },
                "alert_channels": {
                    "critical": "PagerDuty + Email",
                    "high": "Slack #alerts-high",
                    "medium": "Slack #alerts",
                    "low": "Daily digest email"
                }
            }
        }
    
    async def setup_sentry_monitoring(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete Sentry monitoring setup
        """
        timestamp = datetime.now().isoformat()
        
        setup = {
            "timestamp": timestamp,
            "backend_setup": self._generate_backend_setup(project_config),
            "frontend_setup": self._generate_frontend_setup(project_config),
            "alert_rules": self._generate_alert_rules(project_config),
            "performance_config": self._generate_performance_config(),
            "integration_config": self._generate_integration_config()
        }
        
        # Save setup
        output_file = self.research_output / f"{timestamp}_sentry_setup.json"
        with open(output_file, 'w') as f:
            json.dump(setup, f, indent=2)
        
        return setup
    
    def _generate_backend_setup(self, config: Dict[str, Any]) -> str:
        """Generate Python/FastAPI Sentry setup"""
        return """# sentry_config.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
import os

def init_sentry(app_version: str = "1.0.0"):
    \"\"\"Initialize Sentry error tracking\"\"\"
    
    # Logging integration
    logging_integration = LoggingIntegration(
        level=logging.INFO,        # Capture info and above
        event_level=logging.ERROR   # Send errors as events
    )
    
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[
            FastApiIntegration(
                transaction_style="endpoint",
                failed_request_status_codes=[400, 401, 403, 404, 429, 500, 502, 503, 504]
            ),
            SqlalchemyIntegration(),
            RedisIntegration(),
            logging_integration
        ],
        
        # Performance monitoring
        traces_sample_rate=get_sample_rate(),
        profiles_sample_rate=get_sample_rate() * 0.5,  # Half of trace rate
        
        # Environment and release
        environment=os.environ.get("ENVIRONMENT", "development"),
        release=f"fedjobadvisor@{app_version}",
        
        # Options
        attach_stacktrace=True,
        send_default_pii=False,  # GDPR compliance
        max_breadcrumbs=50,
        
        # Filtering
        before_send=before_send_filter,
        before_send_transaction=before_send_transaction_filter,
        
        # Additional options
        shutdown_timeout=5,
        in_app_include=["app", "api"],
        in_app_exclude=["tests"],
        
        # Feature flags
        _experiments={
            "profiles_sample_rate": get_sample_rate() * 0.5,
        }
    )

def get_sample_rate() -> float:
    \"\"\"Get sample rate based on environment\"\"\"
    env = os.environ.get("ENVIRONMENT", "development")
    rates = {
        "development": 1.0,   # 100%
        "staging": 0.5,       # 50%
        "production": 0.1     # 10%
    }
    return rates.get(env, 0.1)

def before_send_filter(event, hint):
    \"\"\"Filter events before sending to Sentry\"\"\"
    
    # Skip health check errors
    if event.get("transaction") == "/api/health":
        return None
    
    # Filter out sensitive data
    if event.get("request"):
        # Scrub headers
        if event["request"].get("headers"):
            sensitive_headers = ["authorization", "cookie", "x-api-key", "stripe-signature"]
            event["request"]["headers"] = {
                k: "[Filtered]" if k.lower() in sensitive_headers else v
                for k, v in event["request"]["headers"].items()
            }
        
        # Scrub cookies
        if event["request"].get("cookies"):
            event["request"]["cookies"] = "[Filtered]"
        
        # Scrub request data
        if event["request"].get("data"):
            sensitive_fields = ["password", "credit_card", "ssn", "api_key"]
            for field in sensitive_fields:
                if field in str(event["request"]["data"]).lower():
                    event["request"]["data"] = "[Contains sensitive data]"
    
    # Filter specific error types
    if hint and hint.get("exc_info"):
        error_type = hint["exc_info"][0].__name__
        
        # Ignore certain exceptions
        ignored_errors = [
            "ConnectionError",
            "TimeoutError",
            "BrokenPipeError"
        ]
        if error_type in ignored_errors:
            return None
    
    # Add custom tags
    event["tags"] = event.get("tags", {})
    event["tags"]["service"] = "backend"
    
    return event

def before_send_transaction_filter(event, hint):
    \"\"\"Filter transactions before sending\"\"\"
    
    # Skip health checks
    if event.get("transaction") in ["/api/health", "/metrics"]:
        return None
    
    # Add performance context
    if event.get("contexts", {}).get("trace"):
        trace = event["contexts"]["trace"]
        
        # Mark slow transactions
        duration = trace.get("duration", 0)
        if duration > 1000:  # Over 1 second
            event["tags"] = event.get("tags", {})
            event["tags"]["slow_transaction"] = True
    
    return event

# Custom error capture
def capture_custom_error(message: str, level: str = "error", **kwargs):
    \"\"\"Capture custom error with context\"\"\"
    with sentry_sdk.push_scope() as scope:
        for key, value in kwargs.items():
            scope.set_context(key, value)
        
        if level == "error":
            sentry_sdk.capture_message(message, level="error")
        elif level == "warning":
            sentry_sdk.capture_message(message, level="warning")
        else:
            sentry_sdk.capture_message(message, level="info")

# Performance monitoring helpers
def track_db_query(query_name: str):
    \"\"\"Decorator to track database query performance\"\"\"
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with sentry_sdk.start_span(op="db.query", description=query_name):
                return await func(*args, **kwargs)
        return wrapper
    return decorator

def track_external_api(api_name: str):
    \"\"\"Decorator to track external API calls\"\"\"
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with sentry_sdk.start_span(op="http.client", description=api_name):
                return await func(*args, **kwargs)
        return wrapper
    return decorator
"""
    
    def _generate_frontend_setup(self, config: Dict[str, Any]) -> str:
        """Generate React/Next.js Sentry setup"""
        return """// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  
  // Performance Monitoring
  integrations: [
    new Sentry.BrowserTracing({
      // Navigation transactions
      routingInstrumentation: Sentry.nextRouterInstrumentation,
      
      // Trace fetch/XHR requests
      traceFetch: true,
      traceXHR: true,
      
      // Custom transaction names
      beforeNavigate: (context) => {
        return {
          ...context,
          name: context.name.replace(/\\/[^/]+$/,"/<id>")
        };
      }
    }),
    
    // Session Replay
    new Sentry.Replay({
      maskAllText: true,
      maskAllInputs: true,
      blockAllMedia: true,
      
      // Privacy settings
      maskTextFn: (text) => {
        // Custom masking logic
        if (text.includes('@')) return '[email]';
        return text;
      }
    })
  ],
  
  // Sample rates
  tracesSampleRate: getEnvironmentSampleRate(),
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  
  // Environment
  environment: process.env.NODE_ENV,
  release: process.env.NEXT_PUBLIC_APP_VERSION,
  
  // Filtering
  ignoreErrors: [
    'ResizeObserver loop limit exceeded',
    'Non-Error promise rejection captured',
    'Network request failed',
    /extension\\//i,
    /^chrome:\\/\\//i,
    /^moz-extension:\\/\\//i
  ],
  
  denyUrls: [
    /extensions\\//i,
    /^chrome:\\/\\//i,
    /^moz-extension:\\/\\//i
  ],
  
  beforeSend(event, hint) {
    // Filter out non-application errors
    if (event.exception) {
      const error = hint.originalException;
      
      // Filter browser extension errors
      if (error?.stack?.includes('extension://')) {
        return null;
      }
      
      // Filter network errors in development
      if (process.env.NODE_ENV === 'development' && 
          error?.name === 'NetworkError') {
        return null;
      }
    }
    
    // Scrub sensitive data from URLs
    if (event.request?.url) {
      event.request.url = event.request.url.replace(
        /api_key=[^&]+/g, 
        'api_key=[FILTERED]'
      );
    }
    
    return event;
  }
});

function getEnvironmentSampleRate(): number {
  switch (process.env.NODE_ENV) {
    case 'development':
      return 1.0;
    case 'staging':
      return 0.5;
    case 'production':
      return 0.1;
    default:
      return 0.1;
  }
}

// Error boundary component
export function SentryErrorBoundary({ children }: { children: React.ReactNode }) {
  return (
    <Sentry.ErrorBoundary
      fallback={({ error, resetError }) => (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>{error?.message || 'An unexpected error occurred'}</p>
          <button onClick={resetError}>Try again</button>
        </div>
      )}
      showDialog
      dialogOptions={{
        title: "It looks like we're having issues",
        subtitle: "Our team has been notified",
        subtitle2: "If you'd like to help, tell us what happened below"
      }}
    >
      {children}
    </Sentry.ErrorBoundary>
  );
}

// Custom error logging
export function logError(
  message: string, 
  level: Sentry.SeverityLevel = 'error',
  context?: Record<string, any>
) {
  Sentry.withScope((scope) => {
    if (context) {
      Object.keys(context).forEach(key => {
        scope.setContext(key, context[key]);
      });
    }
    Sentry.captureMessage(message, level);
  });
}

// Performance monitoring
export function trackPerformance(
  transactionName: string,
  operation: string
): Sentry.Transaction {
  return Sentry.startTransaction({
    name: transactionName,
    op: operation
  });
}
"""
    
    def _generate_alert_rules(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Sentry alert rules"""
        return [
            {
                "name": "High Error Rate",
                "conditions": [
                    {"id": "event_frequency", "value": 100, "interval": "1h"}
                ],
                "actions": [
                    {"id": "send_email", "targetType": "team"},
                    {"id": "send_slack", "channel": "#alerts-critical"}
                ],
                "frequency": 30
            },
            {
                "name": "Payment Failure",
                "conditions": [
                    {"id": "first_seen_event"},
                    {"id": "tagged_event", "key": "transaction", "value": "stripe.payment"}
                ],
                "actions": [
                    {"id": "send_email", "targetType": "team"},
                    {"id": "create_jira_ticket"}
                ],
                "frequency": 1
            },
            {
                "name": "Performance Degradation",
                "conditions": [
                    {"id": "p95_transaction_duration", "value": 2000}
                ],
                "actions": [
                    {"id": "send_slack", "channel": "#alerts-performance"}
                ],
                "frequency": 60
            },
            {
                "name": "New Error Type",
                "conditions": [
                    {"id": "first_seen_event"}
                ],
                "actions": [
                    {"id": "send_email", "targetType": "owner"}
                ],
                "frequency": 1
            }
        ]
    
    def _generate_performance_config(self) -> Dict[str, Any]:
        """Generate performance monitoring configuration"""
        return {
            "vital_thresholds": {
                "lcp": 2500,  # Largest Contentful Paint
                "fid": 100,   # First Input Delay
                "cls": 0.1,   # Cumulative Layout Shift
                "ttfb": 600   # Time to First Byte
            },
            "transaction_thresholds": {
                "default": 1000,
                "api.job_search": 500,
                "api.payment": 2000,
                "page.load": 3000
            },
            "sampling_rules": [
                {"transaction": "/api/health", "sample_rate": 0},
                {"transaction": "stripe.*", "sample_rate": 1.0},
                {"transaction": "auth.*", "sample_rate": 0.5}
            ]
        }
    
    def _generate_integration_config(self) -> Dict[str, Any]:
        """Generate integration configuration"""
        return {
            "slack": {
                "workspace": "fedjobadvisor",
                "channels": {
                    "critical": "#alerts-critical",
                    "errors": "#alerts-errors",
                    "performance": "#alerts-performance"
                }
            },
            "github": {
                "repo": "fedjobadvisor/main",
                "auto_create_issues": False,
                "link_commits": True
            },
            "email": {
                "team_email": "dev@fedjobadvisor.com",
                "digest_schedule": "daily"
            }
        }
    
    async def diagnose_sentry_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze Sentry issue and provide recommendations
        """
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "issue_type": issue_data.get("type", "unknown"),
            "severity": self._calculate_severity(issue_data),
            "root_cause_analysis": [],
            "recommended_fixes": [],
            "prevention_strategies": []
        }
        
        # Analyze error type
        error_message = issue_data.get("message", "").lower()
        
        if "timeout" in error_message:
            diagnosis["root_cause_analysis"].append("Request timeout detected")
            diagnosis["recommended_fixes"].extend([
                "Increase timeout limits",
                "Optimize slow queries",
                "Add caching layer"
            ])
            diagnosis["prevention_strategies"].extend([
                "Implement circuit breakers",
                "Add request queuing",
                "Use async processing"
            ])
        
        elif "memory" in error_message or "heap" in error_message:
            diagnosis["root_cause_analysis"].append("Memory issue detected")
            diagnosis["recommended_fixes"].extend([
                "Increase memory limits",
                "Fix memory leaks",
                "Optimize data structures"
            ])
            diagnosis["prevention_strategies"].extend([
                "Add memory monitoring",
                "Implement garbage collection tuning",
                "Use streaming for large data"
            ])
        
        elif "database" in error_message or "connection" in error_message:
            diagnosis["root_cause_analysis"].append("Database connectivity issue")
            diagnosis["recommended_fixes"].extend([
                "Check connection pool settings",
                "Verify database health",
                "Add retry logic"
            ])
            diagnosis["prevention_strategies"].extend([
                "Implement connection pooling",
                "Add health checks",
                "Use read replicas"
            ])
        
        return diagnosis
    
    def _calculate_severity(self, issue_data: Dict[str, Any]) -> str:
        """Calculate issue severity"""
        event_count = issue_data.get("count", 0)
        user_count = issue_data.get("userCount", 0)
        
        if event_count > 1000 or user_count > 100:
            return "critical"
        elif event_count > 100 or user_count > 10:
            return "high"
        elif event_count > 10 or user_count > 1:
            return "medium"
        else:
            return "low"

# CLI interface
if __name__ == "__main__":
    import sys
    
    expert = SentryExpert()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            config = {}
            if len(sys.argv) > 2:
                config = json.loads(sys.argv[2])
            result = asyncio.run(expert.setup_sentry_monitoring(config))
            print(json.dumps(result, indent=2))
        
        elif command == "diagnose":
            if len(sys.argv) > 2:
                issue = json.loads(sys.argv[2])
                result = asyncio.run(expert.diagnose_sentry_issue(issue))
                print(json.dumps(result, indent=2))
    else:
        print("Sentry Error Expert")
        print("Commands:")
        print("  setup [config] - Generate Sentry setup")
        print("  diagnose <issue> - Analyze Sentry issue")
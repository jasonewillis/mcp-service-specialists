#!/usr/bin/env python3
"""
Email Service Specialist for Fed Job Advisor

Embedded knowledge for email services with federal notification requirements.
Supports SMTP configuration, template management, queue integration, and delivery monitoring.

CRITICAL VERSIONS:
- sendgrid==6.11.0 (from requirements.txt line 39)
- celery==5.3.4 (from requirements.txt line 33)
- redis==5.0.1 (from requirements.txt line 32)

WARNING: Federal email notifications have strict compliance requirements
WARNING: SendGrid API limits require careful rate limiting
WARNING: Email templates must meet federal accessibility standards
"""

import json
import smtplib
import ssl
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
import structlog
import re

# Embedded knowledge base for Fed Job Advisor Email patterns
EMAIL_SPECIALIST_KNOWLEDGE = {
    "version_compatibility": {
        "sendgrid": "6.11.0",
        "celery": "5.3.4",
        "redis": "5.0.1",
        "smtp_ssl": "Built-in Python ssl module",
        "template_engines": ["jinja2", "sendgrid_templates"]
    },
    
    "federal_email_requirements": {
        "accessibility_compliance": {
            "section_508": "All email content must be screen reader accessible",
            "wcag_2_1_aa": "Meet Web Content Accessibility Guidelines Level AA",
            "alt_text": "All images must have descriptive alt text",
            "semantic_html": "Use proper HTML structure and headings",
            "color_contrast": "Minimum 4.5:1 contrast ratio for text"
        },
        "security_requirements": {
            "encryption": "TLS 1.2+ required for SMTP connections",
            "authentication": "SPF, DKIM, DMARC records required",
            "data_protection": "No PII in email headers or tracking pixels",
            "audit_trail": "All email sends must be logged",
            "retention_policy": "Email logs retained for 3 years"
        },
        "content_standards": {
            "plain_english": "Use plain language guidelines",
            "government_branding": "Include official government disclaimers",
            "contact_information": "Always include support contact info",
            "unsubscribe": "Honor unsubscribe requests within 24 hours",
            "spam_compliance": "CAN-SPAM Act compliance required"
        }
    },
    
    "email_types": {
        "transactional": {
            "welcome_email": {
                "trigger": "User registration completion",
                "template": "welcome_new_user",
                "priority": "high",
                "delivery_window": "immediate"
            },
            "password_reset": {
                "trigger": "Password reset request",
                "template": "password_reset_otp",
                "priority": "critical",
                "delivery_window": "immediate",
                "expiration": "15 minutes"
            },
            "application_confirmation": {
                "trigger": "Job application submitted",
                "template": "application_submitted",
                "priority": "high", 
                "delivery_window": "5 minutes"
            },
            "deadline_reminder": {
                "trigger": "Job deadline approaching",
                "template": "application_deadline",
                "priority": "medium",
                "delivery_window": "1 hour"
            }
        },
        "notification": {
            "job_alerts": {
                "trigger": "New matching jobs found",
                "template": "job_alert_digest",
                "priority": "medium",
                "delivery_window": "daily_digest",
                "batch_size": 50
            },
            "system_maintenance": {
                "trigger": "Scheduled maintenance",
                "template": "system_maintenance",
                "priority": "high",
                "delivery_window": "24_hours_before"
            },
            "security_alerts": {
                "trigger": "Suspicious login activity",
                "template": "security_alert",
                "priority": "critical",
                "delivery_window": "immediate"
            }
        }
    },
    
    "delivery_configuration": {
        "sendgrid_settings": {
            "api_key": "Environment variable SENDGRID_API_KEY",
            "sender_identity": "fedjobs@example.gov",
            "reply_to": "noreply@example.gov",
            "tracking": {
                "open_tracking": False,  # Privacy compliance
                "click_tracking": False,  # Privacy compliance
                "subscription_tracking": True,
                "ganalytics": False  # No Google Analytics for federal
            },
            "rate_limits": {
                "daily_limit": 100000,  # SendGrid plan dependent
                "burst_limit": 1000,    # Per minute
                "retry_attempts": 3
            }
        },
        "smtp_fallback": {
            "server": "smtp.example.gov",
            "port": 587,
            "use_tls": True,
            "authentication": "required",
            "connection_timeout": 30,
            "read_timeout": 60
        }
    },
    
    "template_management": {
        "template_structure": {
            "base_template": "Base layout with government branding",
            "transactional_templates": "User-specific notifications",
            "notification_templates": "System and job alerts",
            "accessibility_templates": "Screen reader optimized versions"
        },
        "localization": {
            "default_language": "en-US",
            "supported_languages": ["en-US", "es-US"],  # Federal bilingual requirement
            "fallback_strategy": "Default to English if translation missing"
        },
        "personalization": {
            "user_variables": ["first_name", "last_name", "preferred_name"],
            "job_variables": ["position_title", "agency", "deadline", "location"],
            "system_variables": ["current_date", "support_email", "unsubscribe_url"]
        }
    },
    
    "queue_integration": {
        "celery_email_tasks": {
            "send_immediate": {
                "queue": "email_priority",
                "retry_attempts": 3,
                "retry_delay": "exponential_backoff",
                "timeout": 300  # 5 minutes
            },
            "send_batch": {
                "queue": "email_batch",
                "batch_size": 100,
                "processing_window": "every_hour",
                "timeout": 1800  # 30 minutes
            },
            "send_digest": {
                "queue": "email_digest",
                "schedule": "daily_8am_est",
                "batch_size": 500,
                "timeout": 3600  # 1 hour
            }
        },
        "redis_tracking": {
            "delivery_status": "email:status:{message_id}",
            "rate_limiting": "email:rate:{user_id}:{hour}",
            "bounce_tracking": "email:bounce:{email_address}",
            "unsubscribe_list": "email:unsubscribe:{email_type}"
        }
    },
    
    "critical_warnings": {
        "sendgrid_6_11_0_issues": [
            "API key format changed - use new SG.xxx format",
            "Mail object initialization updated",
            "Attachment handling modified",
            "Rate limit headers changed"
        ],
        "federal_compliance_warnings": [
            "Never use tracking pixels or analytics",
            "All emails must be accessible to screen readers",
            "Include government contact information",
            "Honor unsubscribe requests immediately",
            "Audit trail required for all email sends",
            "PII protection in email headers and content"
        ],
        "delivery_gotchas": [
            "Government email filters are aggressive",
            "SPF/DKIM/DMARC must be properly configured",
            "Subject lines with 'URGENT' may be filtered",
            "HTML-only emails may be blocked",
            "Large attachments will be rejected"
        ],
        "template_warnings": [
            "Government branding requirements must be met",
            "Plain text versions always required",
            "Accessibility testing required before deployment",
            "Template changes need compliance review"
        ]
    }
}

class EmailServiceSpecialist:
    """
    Fed Job Advisor Email Service Specialist
    
    Provides comprehensive email service solutions for federal job search application
    with embedded knowledge for compliance, accessibility, and delivery optimization.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
        self.knowledge = EMAIL_SPECIALIST_KNOWLEDGE
        
    def create_sendgrid_configuration(self) -> Dict[str, Any]:
        """
        Create SendGrid configuration for Fed Job Advisor
        
        Returns:
            Complete SendGrid configuration dict
        """
        return {
            "api_key": "SENDGRID_API_KEY",  # Environment variable
            "default_from": {
                "email": "fedjobs@example.gov",
                "name": "Fed Job Advisor"
            },
            "reply_to": {
                "email": "noreply@example.gov",
                "name": "Fed Job Advisor - Do Not Reply"
            },
            "tracking_settings": {
                "click_tracking": {
                    "enable": False,  # Federal privacy compliance
                    "enable_text": False
                },
                "open_tracking": {
                    "enable": False  # Federal privacy compliance
                },
                "subscription_tracking": {
                    "enable": True,
                    "text": "If you no longer wish to receive these emails, you may unsubscribe: [unsubscribe]",
                    "html": '<p>If you no longer wish to receive these emails, you may <a href="[unsubscribe]">unsubscribe</a>.</p>',
                    "substitution_tag": "[unsubscribe]"
                },
                "ganalytics": {
                    "enable": False  # No Google Analytics for federal systems
                }
            },
            "mail_settings": {
                "footer": {
                    "enable": True,
                    "text": "This email was sent by Fed Job Advisor, a service of [Agency Name]. For support, contact support@example.gov",
                    "html": "<p>This email was sent by Fed Job Advisor, a service of [Agency Name]. For support, contact <a href='mailto:support@example.gov'>support@example.gov</a></p>"
                },
                "spam_check": {
                    "enable": True,
                    "threshold": 1,
                    "post_to_url": "https://api.example.gov/webhook/spam-check"
                }
            },
            "batch_size_limit": 1000,
            "rate_limit": {
                "requests_per_second": 10,
                "daily_limit": 100000
            }
        }
    
    def create_smtp_fallback_configuration(self) -> Dict[str, Any]:
        """
        Create SMTP fallback configuration
        
        Returns:
            SMTP configuration for government mail servers
        """
        return {
            "smtp_server": "smtp.example.gov",
            "port": 587,
            "use_tls": True,
            "username": "SMTP_USERNAME",  # Environment variable
            "password": "SMTP_PASSWORD",  # Environment variable
            "timeout": 30,
            "connection_pool": {
                "max_connections": 10,
                "connection_timeout": 30,
                "read_timeout": 60
            },
            "retry_policy": {
                "max_attempts": 3,
                "initial_delay": 1,
                "max_delay": 60,
                "exponential_base": 2
            },
            "security": {
                "ssl_context": "create_default_context",
                "check_hostname": True,
                "verify_mode": "CERT_REQUIRED"
            }
        }
    
    def create_email_templates(self) -> Dict[str, Dict[str, str]]:
        """
        Create email templates for Fed Job Advisor
        
        Returns:
            Dictionary of email templates with HTML and text versions
        """
        return {
            "welcome_new_user": {
                "subject": "Welcome to Fed Job Advisor - Your Federal Career Journey Begins",
                "html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Fed Job Advisor</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background-color: #003366; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { background-color: #f4f4f4; padding: 15px; font-size: 12px; }
        .button { background-color: #0066cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; }
        .accessibility { border: 1px solid #ccc; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome to Fed Job Advisor</h1>
    </div>
    <div class="content">
        <h2>Hello {{first_name}},</h2>
        <p>Welcome to Fed Job Advisor, your comprehensive resource for federal employment opportunities.</p>
        
        <div class="accessibility">
            <h3>Getting Started</h3>
            <ul>
                <li>Complete your profile to receive personalized job recommendations</li>
                <li>Set up job alerts for positions matching your qualifications</li>
                <li>Access our federal hiring guide and application tips</li>
                <li>Track your applications and deadlines</li>
            </ul>
        </div>
        
        <p>
            <a href="{{login_url}}" class="button" role="button" aria-label="Log in to Fed Job Advisor">
                Get Started
            </a>
        </p>
        
        <p>If you have any questions, our support team is here to help at 
           <a href="mailto:{{support_email}}">{{support_email}}</a>.</p>
    </div>
    <div class="footer">
        <p>This email was sent by Fed Job Advisor. 
           <a href="{{unsubscribe_url}}">Unsubscribe</a> | 
           <a href="{{privacy_url}}">Privacy Policy</a></p>
        <p>Fed Job Advisor is committed to providing equal opportunity employment information.</p>
    </div>
</body>
</html>
                """,
                "text": """
Welcome to Fed Job Advisor

Hello {{first_name}},

Welcome to Fed Job Advisor, your comprehensive resource for federal employment opportunities.

Getting Started:
- Complete your profile to receive personalized job recommendations
- Set up job alerts for positions matching your qualifications  
- Access our federal hiring guide and application tips
- Track your applications and deadlines

Get started by logging in: {{login_url}}

If you have any questions, our support team is here to help at {{support_email}}.

---
This email was sent by Fed Job Advisor.
Unsubscribe: {{unsubscribe_url}}
Privacy Policy: {{privacy_url}}

Fed Job Advisor is committed to providing equal opportunity employment information.
                """
            },
            
            "password_reset_otp": {
                "subject": "Fed Job Advisor - Password Reset Verification Code",
                "html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset - Fed Job Advisor</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background-color: #d73027; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .otp-code { background-color: #f8f9fa; border: 2px solid #007bff; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0; }
        .warning { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 15px 0; }
        .footer { background-color: #f4f4f4; padding: 15px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Password Reset Request</h1>
    </div>
    <div class="content">
        <h2>Hello {{first_name}},</h2>
        <p>You requested a password reset for your Fed Job Advisor account.</p>
        
        <div class="otp-code" role="region" aria-label="Verification Code">
            {{otp_code}}
        </div>
        
        <div class="warning">
            <h3>Important Security Information:</h3>
            <ul>
                <li>This code expires in 15 minutes</li>
                <li>Use this code only on the Fed Job Advisor website</li>
                <li>Never share this code with anyone</li>
                <li>If you didn't request this reset, contact support immediately</li>
            </ul>
        </div>
        
        <p>If you did not request this password reset, please ignore this email and contact our support team at <a href="mailto:{{support_email}}">{{support_email}}</a>.</p>
    </div>
    <div class="footer">
        <p>For security reasons, this email cannot be replied to.</p>
        <p>Fed Job Advisor Security Team</p>
    </div>
</body>
</html>
                """,
                "text": """
Fed Job Advisor - Password Reset Verification Code

Hello {{first_name}},

You requested a password reset for your Fed Job Advisor account.

Your verification code is: {{otp_code}}

IMPORTANT SECURITY INFORMATION:
- This code expires in 15 minutes
- Use this code only on the Fed Job Advisor website
- Never share this code with anyone
- If you didn't request this reset, contact support immediately

If you did not request this password reset, please ignore this email and contact our support team at {{support_email}}.

---
For security reasons, this email cannot be replied to.
Fed Job Advisor Security Team
                """
            },
            
            "job_alert_digest": {
                "subject": "{{job_count}} New Federal Job Opportunities - Fed Job Advisor",
                "html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Job Opportunities</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background-color: #28a745; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .job-item { border: 1px solid #ddd; margin: 15px 0; padding: 15px; border-radius: 4px; }
        .job-title { color: #0066cc; font-weight: bold; font-size: 18px; margin-bottom: 5px; }
        .job-details { color: #666; margin: 5px 0; }
        .deadline { color: #d73027; font-weight: bold; }
        .footer { background-color: #f4f4f4; padding: 15px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>New Job Opportunities</h1>
        <p>{{job_count}} positions match your preferences</p>
    </div>
    <div class="content">
        <h2>Hello {{first_name}},</h2>
        <p>We found {{job_count}} new federal job opportunities that match your profile and preferences.</p>
        
        {{#each jobs}}
        <div class="job-item" role="region" aria-label="Job Opportunity {{@index}}">
            <div class="job-title">
                <a href="{{application_url}}" aria-label="Apply for {{position_title}} at {{agency}}">
                    {{position_title}}
                </a>
            </div>
            <div class="job-details">
                <strong>Agency:</strong> {{agency}}<br>
                <strong>Location:</strong> {{location}}<br>
                <strong>Grade:</strong> {{grade_range}}<br>
                <strong>Salary:</strong> {{salary_range}}
            </div>
            <div class="deadline">
                <strong>Application Deadline:</strong> {{close_date}}
            </div>
        </div>
        {{/each}}
        
        <p>
            <a href="{{dashboard_url}}" style="background-color: #0066cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">
                View All Opportunities
            </a>
        </p>
    </div>
    <div class="footer">
        <p>You're receiving this because you signed up for job alerts. 
           <a href="{{unsubscribe_url}}">Unsubscribe</a> | 
           <a href="{{preferences_url}}">Update Preferences</a></p>
    </div>
</body>
</html>
                """,
                "text": """
New Federal Job Opportunities - {{job_count}} positions

Hello {{first_name}},

We found {{job_count}} new federal job opportunities that match your profile and preferences.

{{#each jobs}}
---
{{position_title}}
Agency: {{agency}}
Location: {{location}}  
Grade: {{grade_range}}
Salary: {{salary_range}}
Application Deadline: {{close_date}}
Apply: {{application_url}}

{{/each}}

View all opportunities: {{dashboard_url}}

---
You're receiving this because you signed up for job alerts.
Unsubscribe: {{unsubscribe_url}}
Update Preferences: {{preferences_url}}
                """
            }
        }
    
    def create_email_service_code(self) -> str:
        """
        Create email service implementation code
        
        Returns:
            Python code for email service with SendGrid and SMTP fallback
        """
        return '''
import os
import smtplib
import ssl
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import structlog
import sendgrid
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent
from jinja2 import Environment, FileSystemLoader, select_autoescape
import redis
import json

class FedJobEmailService:
    """
    Email service for Fed Job Advisor with federal compliance features
    """
    
    def __init__(self, config: Dict[str, Any], redis_client: redis.Redis):
        self.config = config
        self.redis_client = redis_client
        self.logger = structlog.get_logger(__name__)
        
        # Initialize SendGrid
        try:
            self.sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
            self.sendgrid_available = True
        except Exception as e:
            self.logger.warning("SendGrid initialization failed", error=str(e))
            self.sendgrid_available = False
        
        # Initialize template engine
        self.jinja_env = Environment(
            loader=FileSystemLoader('templates/email'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Load email templates
        self.templates = self._load_templates()
    
    def send_email(self, email_type: str, recipient: str, 
                   context: Dict[str, Any], priority: str = "medium") -> Dict[str, Any]:
        """
        Send email with federal compliance and accessibility features
        
        Args:
            email_type: Type of email from templates
            recipient: Recipient email address
            context: Template context variables
            priority: Email priority (critical, high, medium, low)
            
        Returns:
            Send result with message ID and status
        """
        try:
            # Check if recipient is unsubscribed
            if self._is_unsubscribed(recipient, email_type):
                return {
                    "success": False,
                    "error": "Recipient unsubscribed",
                    "message_id": None
                }
            
            # Rate limiting check
            if not self._check_rate_limit(recipient):
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "message_id": None
                }
            
            # Get template
            template = self.templates.get(email_type)
            if not template:
                raise ValueError(f"Unknown email type: {email_type}")
            
            # Render template with context
            rendered = self._render_template(template, context)
            
            # Add federal compliance elements
            rendered = self._add_compliance_elements(rendered, email_type)
            
            # Try SendGrid first, fallback to SMTP
            result = None
            if self.sendgrid_available and priority in ["critical", "high"]:
                result = self._send_via_sendgrid(recipient, rendered)
            
            if not result or not result.get("success"):
                result = self._send_via_smtp(recipient, rendered)
            
            # Log send attempt
            self._log_email_send(recipient, email_type, result, context)
            
            # Update rate limiting
            self._update_rate_limit(recipient)
            
            return result
            
        except Exception as e:
            self.logger.error("Email send failed", 
                            recipient=recipient, 
                            email_type=email_type, 
                            error=str(e))
            return {
                "success": False,
                "error": str(e),
                "message_id": None
            }
    
    def send_batch_emails(self, email_type: str, recipients: List[Dict[str, Any]], 
                         batch_size: int = 100) -> Dict[str, Any]:
        """
        Send batch emails with federal compliance
        
        Args:
            email_type: Type of email template
            recipients: List of recipient data with email and context
            batch_size: Number of emails per batch
            
        Returns:
            Batch send results
        """
        results = {
            "total": len(recipients),
            "sent": 0,
            "failed": 0,
            "errors": []
        }
        
        # Process in batches
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i + batch_size]
            
            try:
                if self.sendgrid_available:
                    batch_result = self._send_batch_sendgrid(email_type, batch)
                else:
                    batch_result = self._send_batch_smtp(email_type, batch)
                
                results["sent"] += batch_result.get("sent", 0)
                results["failed"] += batch_result.get("failed", 0)
                results["errors"].extend(batch_result.get("errors", []))
                
            except Exception as e:
                self.logger.error("Batch email failed", batch_start=i, error=str(e))
                results["failed"] += len(batch)
                results["errors"].append(f"Batch {i}: {str(e)}")
        
        return results
    
    def _send_via_sendgrid(self, recipient: str, rendered_email: Dict[str, str]) -> Dict[str, Any]:
        """Send email via SendGrid API"""
        try:
            from_email = From(
                self.config["sendgrid"]["default_from"]["email"],
                self.config["sendgrid"]["default_from"]["name"]
            )
            
            to_email = To(recipient)
            subject = Subject(rendered_email["subject"])
            
            mail = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=PlainTextContent(rendered_email["text"]),
                html_content=HtmlContent(rendered_email["html"])
            )
            
            # Add federal compliance settings
            mail.tracking_settings = self.config["sendgrid"]["tracking_settings"]
            mail.mail_settings = self.config["sendgrid"]["mail_settings"]
            
            # Send email
            response = self.sg.send(mail)
            
            # Extract message ID from headers
            message_id = response.headers.get('X-Message-Id', 'unknown')
            
            return {
                "success": True,
                "message_id": message_id,
                "provider": "sendgrid",
                "status_code": response.status_code
            }
            
        except Exception as e:
            self.logger.error("SendGrid send failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "provider": "sendgrid"
            }
    
    def _send_via_smtp(self, recipient: str, rendered_email: Dict[str, str]) -> Dict[str, Any]:
        """Send email via SMTP fallback"""
        try:
            smtp_config = self.config["smtp_fallback"]
            
            # Create message
            msg = MimeMultipart("alternative")
            msg["Subject"] = rendered_email["subject"]
            msg["From"] = self.config["sendgrid"]["default_from"]["email"]
            msg["To"] = recipient
            msg["Reply-To"] = self.config["sendgrid"]["reply_to"]["email"]
            
            # Add text and HTML parts
            text_part = MimeText(rendered_email["text"], "plain")
            html_part = MimeText(rendered_email["html"], "html")
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send via SMTP
            context = ssl.create_default_context()
            
            with smtplib.SMTP(smtp_config["smtp_server"], smtp_config["port"]) as server:
                server.starttls(context=context)
                server.login(
                    os.getenv("SMTP_USERNAME"),
                    os.getenv("SMTP_PASSWORD")
                )
                
                text = msg.as_string()
                server.sendmail(msg["From"], recipient, text)
            
            # Generate message ID for tracking
            message_id = f"smtp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(recipient) % 10000}"
            
            return {
                "success": True,
                "message_id": message_id,
                "provider": "smtp"
            }
            
        except Exception as e:
            self.logger.error("SMTP send failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "provider": "smtp"
            }
    
    def _render_template(self, template: Dict[str, str], 
                        context: Dict[str, Any]) -> Dict[str, str]:
        """Render email template with context"""
        # Add default context variables
        default_context = {
            "current_date": datetime.now().strftime("%B %d, %Y"),
            "support_email": "support@example.gov",
            "unsubscribe_url": f"https://fedjobadvisor.com/unsubscribe?email={context.get('email', '')}",
            "privacy_url": "https://fedjobadvisor.com/privacy",
            "login_url": "https://fedjobadvisor.com/login",
            "dashboard_url": "https://fedjobadvisor.com/dashboard"
        }
        
        # Merge contexts (user context takes precedence)
        full_context = {**default_context, **context}
        
        # Render templates
        try:
            subject_template = self.jinja_env.from_string(template["subject"])
            html_template = self.jinja_env.from_string(template["html"])
            text_template = self.jinja_env.from_string(template["text"])
            
            return {
                "subject": subject_template.render(full_context),
                "html": html_template.render(full_context),
                "text": text_template.render(full_context)
            }
            
        except Exception as e:
            self.logger.error("Template rendering failed", error=str(e))
            raise
    
    def _add_compliance_elements(self, rendered_email: Dict[str, str], 
                                email_type: str) -> Dict[str, str]:
        """Add federal compliance elements to email"""
        
        # Add accessibility improvements to HTML
        html = rendered_email["html"]
        
        # Ensure proper language attribute
        if 'lang=' not in html:
            html = html.replace('<html', '<html lang="en"')
        
        # Add skip navigation for screen readers
        skip_nav = '''
        <a href="#main-content" class="sr-only sr-only-focusable">Skip to main content</a>
        '''
        html = html.replace('<body>', f'<body>{skip_nav}')
        
        # Add main content landmark
        html = html.replace('<div class="content">', '<div class="content" id="main-content" role="main">')
        
        # Ensure all images have alt text
        import re
        img_pattern = r'<img([^>]*?)(?:\s+alt="[^"]*")?([^>]*?)>'
        html = re.sub(img_pattern, r'<img\1 alt="Decorative image"\2>', html)
        
        rendered_email["html"] = html
        
        return rendered_email
    
    def _is_unsubscribed(self, email: str, email_type: str) -> bool:
        """Check if recipient is unsubscribed"""
        try:
            # Check global unsubscribe
            global_key = f"email:unsubscribe:all"
            if self.redis_client.sismember(global_key, email):
                return True
            
            # Check type-specific unsubscribe
            type_key = f"email:unsubscribe:{email_type}"
            if self.redis_client.sismember(type_key, email):
                return True
            
            return False
            
        except Exception as e:
            self.logger.error("Unsubscribe check failed", error=str(e))
            return False  # Fail open - allow sending
    
    def _check_rate_limit(self, email: str) -> bool:
        """Check email rate limiting"""
        try:
            current_hour = datetime.utcnow().strftime("%Y%m%d_%H")
            rate_key = f"email:rate:{email}:{current_hour}"
            
            current_count = self.redis_client.get(rate_key)
            if current_count and int(current_count) >= 10:  # Max 10 emails per hour
                return False
            
            return True
            
        except Exception as e:
            self.logger.error("Rate limit check failed", error=str(e))
            return True  # Fail open - allow sending
    
    def _update_rate_limit(self, email: str):
        """Update rate limiting counter"""
        try:
            current_hour = datetime.utcnow().strftime("%Y%m%d_%H")
            rate_key = f"email:rate:{email}:{current_hour}"
            
            pipe = self.redis_client.pipeline()
            pipe.incr(rate_key)
            pipe.expire(rate_key, 3600)  # 1 hour TTL
            pipe.execute()
            
        except Exception as e:
            self.logger.error("Rate limit update failed", error=str(e))
    
    def _log_email_send(self, recipient: str, email_type: str, 
                       result: Dict[str, Any], context: Dict[str, Any]):
        """Log email send for federal audit requirements"""
        try:
            log_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "recipient": recipient,
                "email_type": email_type,
                "success": result.get("success", False),
                "message_id": result.get("message_id"),
                "provider": result.get("provider"),
                "error": result.get("error"),
                "context_keys": list(context.keys())  # Don't log actual values
            }
            
            # Store in Redis for real-time monitoring
            log_key = f"email:log:{datetime.utcnow().strftime('%Y%m%d')}"
            self.redis_client.lpush(log_key, json.dumps(log_data))
            self.redis_client.expire(log_key, 86400 * 7)  # Keep for 7 days
            
            # Log to structured logger for long-term storage
            self.logger.info("Email sent", **log_data)
            
        except Exception as e:
            self.logger.error("Email logging failed", error=str(e))
    
    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Load email templates from embedded knowledge"""
        # In production, these would be loaded from files or database
        specialist = EmailServiceSpecialist()
        return specialist.create_email_templates()
    
    def unsubscribe_user(self, email: str, email_type: str = "all") -> bool:
        """Handle unsubscribe requests (federal compliance)"""
        try:
            if email_type == "all":
                key = "email:unsubscribe:all"
            else:
                key = f"email:unsubscribe:{email_type}"
            
            self.redis_client.sadd(key, email)
            
            # Log unsubscribe for compliance
            self.logger.info("User unsubscribed", 
                           email=email, 
                           email_type=email_type,
                           timestamp=datetime.utcnow().isoformat())
            
            return True
            
        except Exception as e:
            self.logger.error("Unsubscribe failed", error=str(e))
            return False
    
    def get_email_stats(self, date_range: int = 7) -> Dict[str, Any]:
        """Get email statistics for monitoring"""
        try:
            stats = {
                "total_sent": 0,
                "total_failed": 0,
                "by_type": {},
                "by_provider": {"sendgrid": 0, "smtp": 0},
                "date_range_days": date_range
            }
            
            # Aggregate from Redis logs
            for i in range(date_range):
                date = (datetime.utcnow() - timedelta(days=i)).strftime('%Y%m%d')
                log_key = f"email:log:{date}"
                
                logs = self.redis_client.lrange(log_key, 0, -1)
                for log_entry in logs:
                    try:
                        data = json.loads(log_entry)
                        
                        if data.get("success"):
                            stats["total_sent"] += 1
                        else:
                            stats["total_failed"] += 1
                        
                        # Count by type
                        email_type = data.get("email_type", "unknown")
                        stats["by_type"][email_type] = stats["by_type"].get(email_type, 0) + 1
                        
                        # Count by provider
                        provider = data.get("provider", "unknown")
                        if provider in stats["by_provider"]:
                            stats["by_provider"][provider] += 1
                        
                    except json.JSONDecodeError:
                        continue
            
            return stats
            
        except Exception as e:
            self.logger.error("Email stats failed", error=str(e))
            return {"error": str(e)}
'''

    def create_celery_email_tasks(self) -> str:
        """
        Create Celery tasks for email processing
        
        Returns:
            Python code for Celery email tasks
        """
        return '''
from celery import Celery
from typing import Dict, List, Any
import structlog
from datetime import datetime, timedelta
from app.services.email_service import FedJobEmailService
from app.cache.redis_client import FedJobRedisClient
from app.models.user import User
from app.models.job_announcement import JobAnnouncement
from app.database import get_db

# Initialize Celery app
celery_app = Celery('fedjobs_email')
logger = structlog.get_logger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_immediate_email(self, email_type: str, recipient: str, 
                        context: Dict[str, Any]):
    """
    Send immediate email (transactional)
    
    Used for: welcome emails, password resets, application confirmations
    """
    try:
        redis_client = FedJobRedisClient(get_redis_config())
        email_service = FedJobEmailService(get_email_config(), redis_client.client)
        
        result = email_service.send_email(
            email_type=email_type,
            recipient=recipient,
            context=context,
            priority="high"
        )
        
        if not result["success"]:
            # Retry on failure
            if self.request.retries < self.max_retries:
                self.retry(countdown=60 * (self.request.retries + 1))
            else:
                logger.error("Email send failed after retries", 
                           email_type=email_type, 
                           recipient=recipient,
                           error=result.get("error"))
        
        return result
        
    except Exception as exc:
        logger.error("Email task failed", error=str(exc))
        self.retry(countdown=60 * (self.request.retries + 1), exc=exc)

@celery_app.task(bind=True, max_retries=2)
def send_batch_emails(self, email_type: str, recipients: List[Dict[str, Any]]):
    """
    Send batch emails (notifications, alerts)
    
    Used for: job alerts, system notifications, newsletters
    """
    try:
        redis_client = FedJobRedisClient(get_redis_config())
        email_service = FedJobEmailService(get_email_config(), redis_client.client)
        
        result = email_service.send_batch_emails(
            email_type=email_type,
            recipients=recipients,
            batch_size=100
        )
        
        logger.info("Batch email completed", 
                   email_type=email_type,
                   total=result["total"],
                   sent=result["sent"],
                   failed=result["failed"])
        
        return result
        
    except Exception as exc:
        logger.error("Batch email task failed", error=str(exc))
        if self.request.retries < self.max_retries:
            self.retry(countdown=300, exc=exc)  # 5 minute delay
        raise

@celery_app.task
def send_password_reset_email(user_id: int, otp_code: str):
    """Send password reset email with OTP code"""
    try:
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            logger.error("User not found for password reset", user_id=user_id)
            return {"success": False, "error": "User not found"}
        
        context = {
            "first_name": user.first_name,
            "email": user.email,
            "otp_code": otp_code,
            "expires_in": "15 minutes"
        }
        
        return send_immediate_email.delay(
            "password_reset_otp",
            user.email,
            context
        )
        
    except Exception as e:
        logger.error("Password reset email failed", user_id=user_id, error=str(e))
        return {"success": False, "error": str(e)}

@celery_app.task
def send_welcome_email(user_id: int):
    """Send welcome email to new user"""
    try:
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            logger.error("User not found for welcome email", user_id=user_id)
            return {"success": False, "error": "User not found"}
        
        context = {
            "first_name": user.first_name,
            "email": user.email,
            "login_url": "https://fedjobadvisor.com/login"
        }
        
        return send_immediate_email.delay(
            "welcome_new_user",
            user.email,
            context
        )
        
    except Exception as e:
        logger.error("Welcome email failed", user_id=user_id, error=str(e))
        return {"success": False, "error": str(e)}

@celery_app.task
def send_daily_job_alerts():
    """
    Send daily job alert digest to subscribed users
    
    Scheduled task that runs daily at 8 AM EST
    """
    try:
        db = next(get_db())
        
        # Get users with active job alert subscriptions
        subscribed_users = db.query(User).filter(
            User.is_active == True,
            User.job_alerts_enabled == True
        ).all()
        
        total_alerts = 0
        
        for user in subscribed_users:
            try:
                # Get new jobs matching user preferences
                new_jobs = get_matching_jobs_for_user(user.id, db)
                
                if new_jobs:
                    context = {
                        "first_name": user.first_name,
                        "email": user.email,
                        "job_count": len(new_jobs),
                        "jobs": [
                            {
                                "position_title": job.position_title,
                                "agency": job.agency.agency_name,
                                "location": f"{job.location_city}, {job.location_state}",
                                "grade_range": f"{job.grade_low}-{job.grade_high}",
                                "salary_range": f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}",
                                "close_date": job.close_date.strftime("%B %d, %Y"),
                                "application_url": job.application_url
                            }
                            for job in new_jobs[:10]  # Limit to 10 jobs per email
                        ]
                    }
                    
                    send_immediate_email.delay(
                        "job_alert_digest",
                        user.email,
                        context
                    )
                    
                    total_alerts += 1
                    
            except Exception as e:
                logger.error("Job alert failed for user", user_id=user.id, error=str(e))
                continue
        
        logger.info("Daily job alerts completed", total_sent=total_alerts)
        return {"success": True, "alerts_sent": total_alerts}
        
    except Exception as e:
        logger.error("Daily job alerts task failed", error=str(e))
        return {"success": False, "error": str(e)}

@celery_app.task
def send_application_deadline_reminders():
    """
    Send reminders for upcoming application deadlines
    
    Runs every hour to check for deadlines in next 24-48 hours
    """
    try:
        db = next(get_db())
        
        # Find jobs closing in next 24-48 hours
        now = datetime.utcnow()
        reminder_start = now + timedelta(hours=24)
        reminder_end = now + timedelta(hours=48)
        
        closing_jobs = db.query(JobAnnouncement).filter(
            JobAnnouncement.close_date >= reminder_start,
            JobAnnouncement.close_date <= reminder_end,
            JobAnnouncement.is_active == True
        ).all()
        
        # Get users who have saved these jobs or match criteria
        reminders_sent = 0
        
        for job in closing_jobs:
            # Find users who saved this job or have it in their alerts
            interested_users = get_interested_users_for_job(job.announcement_id, db)
            
            for user in interested_users:
                try:
                    hours_remaining = int((job.close_date - now).total_seconds() / 3600)
                    
                    context = {
                        "first_name": user.first_name,
                        "email": user.email,
                        "position_title": job.position_title,
                        "agency": job.agency.agency_name,
                        "close_date": job.close_date.strftime("%B %d, %Y at %I:%M %p"),
                        "hours_remaining": hours_remaining,
                        "application_url": job.application_url
                    }
                    
                    send_immediate_email.delay(
                        "deadline_reminder",
                        user.email,
                        context
                    )
                    
                    reminders_sent += 1
                    
                except Exception as e:
                    logger.error("Deadline reminder failed", 
                               user_id=user.id, 
                               job_id=job.announcement_id,
                               error=str(e))
                    continue
        
        logger.info("Deadline reminders completed", reminders_sent=reminders_sent)
        return {"success": True, "reminders_sent": reminders_sent}
        
    except Exception as e:
        logger.error("Deadline reminders task failed", error=str(e))
        return {"success": False, "error": str(e)}

@celery_app.task
def cleanup_email_logs():
    """
    Clean up old email logs (retain 30 days)
    
    Runs daily to maintain Redis memory usage
    """
    try:
        redis_client = FedJobRedisClient(get_redis_config())
        
        # Clean up logs older than 30 days
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        for i in range(30, 90):  # Check 30-90 days back
            old_date = (datetime.utcnow() - timedelta(days=i)).strftime('%Y%m%d')
            log_key = f"email:log:{old_date}"
            
            deleted = redis_client.client.delete(log_key)
            if deleted:
                logger.info("Cleaned up email logs", date=old_date)
        
        return {"success": True, "cleanup_completed": True}
        
    except Exception as e:
        logger.error("Email log cleanup failed", error=str(e))
        return {"success": False, "error": str(e)}

# Celery beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    'send-daily-job-alerts': {
        'task': 'send_daily_job_alerts',
        'schedule': crontab(hour=8, minute=0),  # 8 AM EST daily
        'options': {'queue': 'email_digest'}
    },
    'send-deadline-reminders': {
        'task': 'send_application_deadline_reminders', 
        'schedule': crontab(minute=0),  # Every hour
        'options': {'queue': 'email_priority'}
    },
    'cleanup-email-logs': {
        'task': 'cleanup_email_logs',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
        'options': {'queue': 'maintenance'}
    }
}

# Helper functions
def get_matching_jobs_for_user(user_id: int, db) -> List[JobAnnouncement]:
    """Get new job announcements matching user preferences"""
    # Implementation would query based on user's saved preferences
    # This is a placeholder for the actual matching logic
    pass

def get_interested_users_for_job(announcement_id: str, db) -> List[User]:
    """Get users who have expressed interest in a specific job"""
    # Implementation would find users who saved the job or match criteria
    # This is a placeholder for the actual interest matching logic
    pass

def get_email_config() -> Dict[str, Any]:
    """Get email service configuration"""
    specialist = EmailServiceSpecialist()
    return {
        "sendgrid": specialist.create_sendgrid_configuration(),
        "smtp_fallback": specialist.create_smtp_fallback_configuration()
    }

def get_redis_config() -> Dict[str, Any]:
    """Get Redis configuration"""
    return {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", 6379)),
        "db": int(os.getenv("REDIS_DB", 0))
    }
'''

    def create_deployment_checklist(self) -> List[str]:
        """
        Create deployment checklist for email service
        
        Returns:
            List of deployment steps and checks
        """
        return [
            "✓ SendGrid account setup with API key",
            "✓ Government email domain configured (SPF/DKIM/DMARC)",
            "✓ SMTP fallback server credentials configured",
            "✓ Email templates accessibility tested",
            "✓ Plain text versions of all templates created",
            "✓ Government branding and disclaimers added",
            "✓ Unsubscribe functionality implemented",
            "✓ Rate limiting configured",
            "✓ Redis cache for email tracking setup",
            "✓ Celery workers configured for email queues",
            "✓ Email audit logging implemented",
            "✓ Template rendering security tested",
            "✓ Bounce and complaint handling configured",
            "✓ Email deliverability testing completed",
            "✓ Federal accessibility compliance verified",
            "✓ CAN-SPAM compliance implemented",
            "✓ Privacy policy updated for email communications",
            "✓ Help documentation for email preferences",
            "CRITICAL: Test email delivery to .gov domains",
            "CRITICAL: Verify SPF/DKIM/DMARC records",
            "CRITICAL: Test unsubscribe compliance workflow",
            "FEDERAL: Section 508 accessibility audit completed",
            "FEDERAL: Plain language guidelines followed",
            "FEDERAL: Government contact information included"
        ]
    
    def get_troubleshooting_guide(self) -> Dict[str, Dict[str, str]]:
        """
        Get troubleshooting guide for email service issues
        
        Returns:
            Troubleshooting guide organized by issue type
        """
        return {
            "sendgrid_issues": {
                "api_key_invalid": "Check SendGrid API key format (starts with SG.)",
                "rate_limit_exceeded": "Implement exponential backoff, check plan limits",
                "sender_identity_not_verified": "Verify sender email in SendGrid dashboard",
                "delivery_blocked": "Check recipient domain reputation, verify DKIM"
            },
            "smtp_issues": {
                "authentication_failed": "Verify SMTP credentials, check server settings",
                "connection_timeout": "Check firewall rules, server availability",
                "tls_handshake_failed": "Verify TLS version support, certificate validity",
                "relay_access_denied": "Check SMTP server relay permissions"
            },
            "template_issues": {
                "rendering_error": "Check Jinja2 template syntax, variable existence",
                "encoding_problems": "Ensure UTF-8 encoding for international characters",
                "html_formatting_broken": "Validate HTML structure, check CSS support",
                "accessibility_failures": "Run accessibility audit, check alt text"
            },
            "federal_compliance_issues": {
                "accessibility_violations": "Add alt text, improve contrast, fix heading structure",
                "plain_language_failures": "Simplify language, reduce jargon, improve readability",
                "branding_missing": "Add government logos, contact info, disclaimers",
                "audit_trail_incomplete": "Ensure all sends logged, include required metadata"
            },
            "delivery_issues": {
                "high_bounce_rate": "Clean email lists, verify addresses, check reputation",
                "spam_folder_placement": "Improve content, fix authentication, warm up IP",
                "government_filters": "Use approved sender domains, avoid trigger words",
                "unsubscribe_not_working": "Test unsubscribe links, check processing time"
            }
        }
    
    def load_ttl_documentation(self) -> Dict[str, str]:
        """
        Load email TTL and timing documentation
        
        Returns:
            Documentation explaining email timing and retention
        """
        return {
            "immediate_emails": """
            Delivery: Immediate (within 5 minutes)
            Used for: Password resets, application confirmations, security alerts
            Priority: Critical/High queue processing
            Retry: 3 attempts with exponential backoff
            """,
            
            "batch_emails": """
            Delivery: Hourly processing windows
            Used for: Job alerts, system notifications
            Batch size: 100 emails per batch
            Rate limiting: 10 emails per hour per user
            """,
            
            "digest_emails": """
            Delivery: Daily at 8 AM EST
            Used for: Job alert summaries, weekly reports
            Batch size: 500 emails per batch
            Personalization: Up to 10 jobs per email
            """,
            
            "email_logs_retention": """
            Redis logs: 7 days for real-time monitoring
            Structured logs: 3 years for federal compliance
            Delivery status: 30 days in Redis cache
            Bounce tracking: 90 days for reputation management
            """,
            
            "rate_limiting": """
            Per user: 10 emails per hour
            Per domain: Based on reputation and relationship
            SendGrid limits: Plan-dependent (typically 100K/day)
            Retry intervals: 1 min, 2 min, 5 min, then fail
            """
        }

def create_email_specialist() -> EmailServiceSpecialist:
    """Factory function to create Email specialist instance"""
    return EmailServiceSpecialist()

# Example usage and testing
if __name__ == "__main__":
    specialist = create_email_specialist()
    
    # Generate SendGrid configuration
    sendgrid_config = specialist.create_sendgrid_configuration()
    print(f"SendGrid config generated: {len(sendgrid_config)} settings")
    
    # Get email templates
    templates = specialist.create_email_templates()
    print(f"Email templates: {len(templates)} types")
    
    # Get deployment checklist
    checklist = specialist.create_deployment_checklist()
    print(f"Deployment checklist: {len(checklist)} items")
    
    # Get troubleshooting guide
    troubleshooting = specialist.get_troubleshooting_guide()
    print(f"Troubleshooting guide: {len(troubleshooting)} categories")
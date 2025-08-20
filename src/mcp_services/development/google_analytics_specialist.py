#!/usr/bin/env python3
"""
Google Analytics Specialist - Analytics and Tracking Expert
Provides specialized guidance for Google Analytics 4 implementation and data analysis
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
from ..base_specialist import BaseSpecialist

class GoogleAnalyticsSpecialist(BaseSpecialist):
    """
    Specialist agent for Google Analytics 4 implementation and web analytics
    Focuses on tracking setup, data analysis, and performance measurement
    """
    
    def __init__(self):
        super().__init__()
        self.service_name = "google_analytics"
        self.specialization = "Web Analytics & Performance Tracking"
        
        self.core_expertise = [
            "Google Analytics 4 (GA4) setup and configuration",
            "Custom event tracking and conversion measurement",
            "E-commerce tracking and enhanced e-commerce",
            "Google Tag Manager integration",
            "Data privacy and compliance (GDPR, CCPA)",
            "Analytics API integration and data export",
            "Performance analysis and optimization",
            "Attribution modeling and customer journey analysis"
        ]
        
        self.tracking_best_practices = [
            "Implement consent management for privacy compliance",
            "Use consistent event naming conventions",
            "Set up proper attribution models",
            "Configure goals and conversions properly",
            "Implement enhanced e-commerce tracking",
            "Use custom dimensions for detailed analysis",
            "Set up proper user and session tracking",
            "Implement cross-domain tracking when needed"
        ]
    
    async def design_tracking_strategy(self, website_config: Dict[str, Any]) -> Dict[str, Any]:
        """Design comprehensive tracking strategy for website"""
        
        strategy = {
            "timestamp": datetime.now().isoformat(),
            "website_type": website_config.get("type", "business"),
            "tracking_plan": {},
            "event_architecture": {},
            "conversion_tracking": {},
            "privacy_compliance": {},
            "implementation_plan": {}
        }
        
        site_type = website_config.get("type", "business")
        features = website_config.get("features", [])
        
        # Design tracking plan
        strategy["tracking_plan"] = self._create_tracking_plan(site_type, features)
        
        # Event architecture
        strategy["event_architecture"] = self._design_event_architecture(features)
        
        # Conversion tracking
        strategy["conversion_tracking"] = self._design_conversion_tracking(website_config)
        
        # Privacy compliance
        strategy["privacy_compliance"] = self._design_privacy_compliance(website_config)
        
        # Implementation plan
        strategy["implementation_plan"] = self._create_implementation_plan(website_config)
        
        return strategy
    
    async def implement_ga4_tracking(self, implementation_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate GA4 implementation code and configuration"""
        
        implementation = {
            "timestamp": datetime.now().isoformat(),
            "platform": implementation_config.get("platform", "nextjs"),
            "tracking_code": {},
            "event_tracking": {},
            "ecommerce_tracking": {},
            "custom_dimensions": {},
            "gtm_configuration": {}
        }
        
        platform = implementation_config.get("platform", "nextjs")
        
        # Generate tracking code
        implementation["tracking_code"] = self._generate_tracking_code(platform, implementation_config)
        
        # Event tracking
        implementation["event_tracking"] = self._generate_event_tracking(implementation_config)
        
        # E-commerce tracking if needed
        if "ecommerce" in implementation_config.get("features", []):
            implementation["ecommerce_tracking"] = self._generate_ecommerce_tracking(platform)
        
        # Custom dimensions
        implementation["custom_dimensions"] = self._suggest_custom_dimensions(implementation_config)
        
        # GTM configuration
        if implementation_config.get("use_gtm", False):
            implementation["gtm_configuration"] = self._generate_gtm_config(implementation_config)
        
        return implementation
    
    async def analyze_tracking_performance(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current tracking performance and identify issues"""
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "tracking_health": {},
            "data_quality_issues": [],
            "missing_events": [],
            "optimization_opportunities": [],
            "recommendations": [],
            "performance_metrics": {}
        }
        
        # Analyze tracking health
        analysis["tracking_health"] = self._assess_tracking_health(analytics_data)
        
        # Data quality issues
        analysis["data_quality_issues"] = self._identify_data_quality_issues(analytics_data)
        
        # Missing events analysis
        analysis["missing_events"] = self._identify_missing_events(analytics_data)
        
        # Optimization opportunities
        analysis["optimization_opportunities"] = self._identify_optimizations(analytics_data)
        
        # Performance metrics
        analysis["performance_metrics"] = self._calculate_performance_metrics(analytics_data)
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_tracking_recommendations(analysis)
        
        return analysis
    
    async def setup_conversion_tracking(self, conversion_config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up conversion tracking and goal configuration"""
        
        conversion_setup = {
            "timestamp": datetime.now().isoformat(),
            "conversion_type": conversion_config.get("type", "form_submission"),
            "ga4_goals": {},
            "event_configuration": {},
            "attribution_settings": {},
            "funnel_analysis": {},
            "implementation_code": {}
        }
        
        conversion_type = conversion_config.get("type", "form_submission")
        
        # GA4 goals setup
        conversion_setup["ga4_goals"] = self._setup_ga4_goals(conversion_config)
        
        # Event configuration
        conversion_setup["event_configuration"] = self._configure_conversion_events(conversion_config)
        
        # Attribution settings
        conversion_setup["attribution_settings"] = self._configure_attribution(conversion_config)
        
        # Funnel analysis
        conversion_setup["funnel_analysis"] = self._design_funnel_analysis(conversion_config)
        
        # Implementation code
        conversion_setup["implementation_code"] = self._generate_conversion_code(conversion_config)
        
        return conversion_setup
    
    async def troubleshoot_tracking_issues(self, issue_details: Dict[str, Any]) -> Dict[str, Any]:
        """Troubleshoot common Google Analytics tracking issues"""
        
        troubleshooting = {
            "timestamp": datetime.now().isoformat(),
            "issue_category": self._categorize_tracking_issue(issue_details),
            "likely_causes": [],
            "solutions": [],
            "debugging_steps": [],
            "prevention_tips": [],
            "testing_instructions": []
        }
        
        issue_type = issue_details.get("issue", "").lower()
        
        if "data not showing" in issue_type or "no data" in issue_type:
            troubleshooting["likely_causes"] = [
                "Tracking code not properly installed",
                "Tag Manager configuration issues",
                "Ad blockers preventing tracking",
                "Sampling issues with large datasets"
            ]
            troubleshooting["solutions"] = [
                "Verify GA4 tracking code is present on all pages",
                "Check Google Tag Manager container is firing",
                "Test in incognito mode to bypass ad blockers",
                "Check real-time reports for immediate data",
                "Verify measurement ID is correct"
            ]
        
        elif "wrong data" in issue_type or "incorrect" in issue_type:
            troubleshooting["likely_causes"] = [
                "Duplicate tracking codes",
                "Bot traffic not filtered",
                "Cross-domain tracking issues",
                "Time zone configuration problems"
            ]
            troubleshooting["solutions"] = [
                "Remove duplicate GA4 tags",
                "Configure bot filtering in GA4",
                "Set up proper cross-domain tracking",
                "Verify time zone settings match business location",
                "Check for internal traffic filtering"
            ]
        
        elif "events not tracking" in issue_type:
            troubleshooting["likely_causes"] = [
                "Event parameters incorrectly configured",
                "JavaScript errors preventing event firing",
                "Event names not following GA4 conventions",
                "Consent management blocking events"
            ]
            troubleshooting["solutions"] = [
                "Use GA4 DebugView to test events",
                "Check browser console for JavaScript errors",
                "Follow GA4 event naming conventions",
                "Verify consent settings allow analytics",
                "Test events with Google Analytics Debugger"
            ]
        
        troubleshooting["debugging_steps"] = [
            "1. Check GA4 Real-Time reports",
            "2. Use Google Analytics Debugger extension",
            "3. Test with GA4 DebugView",
            "4. Verify Tag Manager preview mode",
            "5. Check browser network requests"
        ]
        
        return troubleshooting
    
    def _create_tracking_plan(self, site_type: str, features: List[str]) -> Dict[str, Any]:
        """Create comprehensive tracking plan"""
        base_plan = {
            "page_views": "Automatic page view tracking",
            "user_engagement": "Scroll depth, time on page, file downloads",
            "site_search": "Internal search tracking",
            "outbound_links": "External link click tracking"
        }
        
        if "ecommerce" in features:
            base_plan.update({
                "product_views": "Product detail page views",
                "add_to_cart": "Shopping cart additions",
                "checkout_process": "Checkout funnel tracking",
                "purchases": "Transaction completion"
            })
        
        if "forms" in features:
            base_plan.update({
                "form_starts": "Form interaction beginnings",
                "form_completions": "Successful form submissions",
                "form_abandonment": "Incomplete form tracking"
            })
        
        if "video" in features:
            base_plan.update({
                "video_engagement": "Video play, pause, completion tracking"
            })
        
        return base_plan
    
    def _design_event_architecture(self, features: List[str]) -> Dict[str, Any]:
        """Design event naming and parameter architecture"""
        return {
            "naming_convention": {
                "format": "action_object_context",
                "examples": [
                    "click_button_header",
                    "view_product_category",
                    "complete_form_contact"
                ]
            },
            "standard_parameters": {
                "event_category": "Logical grouping of events",
                "event_label": "Additional event context",
                "value": "Numerical value for measurement"
            },
            "custom_parameters": {
                "user_type": "Authenticated vs anonymous users",
                "content_type": "Blog, product, page type",
                "engagement_level": "High, medium, low engagement"
            },
            "reserved_events": [
                "page_view", "session_start", "first_visit",
                "purchase", "login", "sign_up", "search"
            ]
        }
    
    def _design_conversion_tracking(self, config: Dict) -> Dict[str, Any]:
        """Design conversion tracking strategy"""
        conversions = {
            "macro_conversions": [],
            "micro_conversions": [],
            "attribution_model": "data_driven",
            "conversion_windows": {
                "view_through": "30 days",
                "click_through": "90 days"
            }
        }
        
        site_type = config.get("type", "business")
        
        if site_type == "ecommerce":
            conversions["macro_conversions"] = ["purchase", "add_payment_info"]
            conversions["micro_conversions"] = ["add_to_cart", "view_product", "begin_checkout"]
        elif site_type == "lead_generation":
            conversions["macro_conversions"] = ["contact_form", "phone_call", "email_signup"]
            conversions["micro_conversions"] = ["download_resource", "view_pricing", "start_trial"]
        else:
            conversions["macro_conversions"] = ["form_submission", "newsletter_signup"]
            conversions["micro_conversions"] = ["page_scroll", "video_play", "file_download"]
        
        return conversions
    
    def _design_privacy_compliance(self, config: Dict) -> Dict[str, Any]:
        """Design privacy compliance strategy"""
        return {
            "consent_management": {
                "platform": "Google Consent Mode v2",
                "required_consents": ["analytics_storage", "ad_storage"],
                "default_behavior": "denied",
                "update_mechanism": "User consent banner"
            },
            "data_retention": {
                "user_data": "26 months (GA4 default)",
                "event_data": "2 months minimum",
                "recommendation": "Configure based on business needs"
            },
            "ip_anonymization": {
                "ga4_default": "Automatically anonymized",
                "additional_measures": "Consider server-side anonymization"
            },
            "compliance_features": [
                "Data deletion requests",
                "Data export capabilities",
                "Consent signal forwarding",
                "Enhanced conversions setup"
            ]
        }
    
    def _create_implementation_plan(self, config: Dict) -> Dict[str, Any]:
        """Create implementation plan"""
        return {
            "phases": [
                "1. GA4 property setup and basic tracking",
                "2. Custom event implementation",
                "3. Conversion and goal configuration",
                "4. Enhanced e-commerce setup (if applicable)",
                "5. Data validation and testing",
                "6. Privacy compliance implementation"
            ],
            "estimated_hours": 24 if "ecommerce" in config.get("features", []) else 16,
            "technical_requirements": [
                "Google Analytics 4 property",
                "Google Tag Manager (recommended)",
                "Development environment for testing",
                "Access to website codebase"
            ],
            "testing_checklist": [
                "Real-time event verification",
                "Cross-browser testing",
                "Mobile device testing",
                "Privacy compliance validation"
            ]
        }
    
    def _generate_tracking_code(self, platform: str, config: Dict) -> Dict[str, str]:
        """Generate platform-specific tracking code"""
        measurement_id = config.get("measurement_id", "G-XXXXXXXXXX")
        
        if platform == "nextjs":
            return {
                "gtag_setup": f'''
// pages/_app.js or app/layout.tsx
import Script from 'next/script'

const GA_MEASUREMENT_ID = '{measurement_id}';

export default function App({{ Component, pageProps }}) {{
  return (
    <>
      <Script
        src={{`https://www.googletagmanager.com/gtag/js?id=${{GA_MEASUREMENT_ID}}`}}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {{`
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '${{GA_MEASUREMENT_ID}}', {{
            page_title: document.title,
            page_location: window.location.href,
          }});
        `}}
      </Script>
      <Component {{...pageProps}} />
    </>
  )
}}
''',
                "event_tracking": '''
// lib/analytics.js
export const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID;

export function gtag(...args) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(args);
}

export function trackEvent(action, category, label, value) {
  gtag('event', action, {
    event_category: category,
    event_label: label,
    value: value,
  });
}
'''
            }
        elif platform == "react":
            return {
                "gtag_setup": f'''
// App.js
import {{ useEffect }} from 'react';

const GA_MEASUREMENT_ID = '{measurement_id}';

function App() {{
  useEffect(() => {{
    // Load gtag script
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${{GA_MEASUREMENT_ID}}`;
    document.head.appendChild(script);
    
    // Initialize gtag
    window.dataLayer = window.dataLayer || [];
    function gtag(){{window.dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', GA_MEASUREMENT_ID);
  }}, []);
  
  return <div>Your App</div>;
}}
'''
            }
        elif platform == "vanilla":
            return {
                "html_setup": f'''
<!-- Add to <head> section -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{measurement_id}');
</script>
'''
            }
        
        return {"error": f"Platform {platform} not supported"}
    
    def _generate_event_tracking(self, config: Dict) -> Dict[str, str]:
        """Generate event tracking code examples"""
        return {
            "button_click": '''
// Button click tracking
function trackButtonClick(buttonName, location) {
  gtag('event', 'click', {
    event_category: 'Button',
    event_label: buttonName,
    custom_parameter_location: location
  });
}
''',
            "form_submission": '''
// Form submission tracking
function trackFormSubmission(formName, success) {
  gtag('event', success ? 'form_submit' : 'form_error', {
    event_category: 'Form',
    event_label: formName,
    value: success ? 1 : 0
  });
}
''',
            "file_download": '''
// File download tracking
function trackFileDownload(fileName, fileType) {
  gtag('event', 'file_download', {
    event_category: 'Download',
    event_label: fileName,
    file_extension: fileType
  });
}
''',
            "video_engagement": '''
// Video tracking
function trackVideoEvent(action, videoTitle, progress) {
  gtag('event', 'video_' + action, {
    event_category: 'Video',
    event_label: videoTitle,
    video_progress: progress
  });
}
'''
        }
    
    def _generate_ecommerce_tracking(self, platform: str) -> Dict[str, str]:
        """Generate e-commerce tracking code"""
        return {
            "purchase": '''
// Purchase tracking
function trackPurchase(transactionData) {
  gtag('event', 'purchase', {
    transaction_id: transactionData.transaction_id,
    value: transactionData.value,
    currency: transactionData.currency,
    items: transactionData.items.map(item => ({
      item_id: item.sku,
      item_name: item.name,
      category: item.category,
      quantity: item.quantity,
      price: item.price
    }))
  });
}
''',
            "add_to_cart": '''
// Add to cart tracking
function trackAddToCart(item) {
  gtag('event', 'add_to_cart', {
    currency: 'USD',
    value: item.price * item.quantity,
    items: [{
      item_id: item.sku,
      item_name: item.name,
      category: item.category,
      quantity: item.quantity,
      price: item.price
    }]
  });
}
''',
            "view_item": '''
// Product view tracking
function trackProductView(product) {
  gtag('event', 'view_item', {
    currency: 'USD',
    value: product.price,
    items: [{
      item_id: product.sku,
      item_name: product.name,
      category: product.category,
      price: product.price
    }]
  });
}
'''
        }
    
    def _suggest_custom_dimensions(self, config: Dict) -> Dict[str, Any]:
        """Suggest custom dimensions and metrics"""
        return {
            "user_dimensions": {
                "user_type": "Logged in vs Guest users",
                "membership_level": "Free, Premium, Enterprise",
                "user_lifetime_value": "Customer value segment"
            },
            "content_dimensions": {
                "content_type": "Blog, Product, Landing Page",
                "author": "Content creator",
                "publication_date": "Content freshness"
            },
            "business_dimensions": {
                "campaign_source": "Marketing campaign origin",
                "ab_test_variant": "A/B test variations",
                "feature_usage": "Product feature interactions"
            },
            "custom_metrics": {
                "engagement_score": "Calculated engagement metric",
                "content_depth": "Pages per session metric",
                "conversion_probability": "Predictive conversion score"
            }
        }
    
    def _generate_gtm_config(self, config: Dict) -> Dict[str, Any]:
        """Generate Google Tag Manager configuration"""
        return {
            "container_setup": {
                "tags": [
                    "GA4 Configuration Tag",
                    "GA4 Event Tags",
                    "Conversion Tracking Tags"
                ],
                "triggers": [
                    "Page View - All Pages",
                    "Click - All Elements",
                    "Form Submission",
                    "Scroll Depth"
                ],
                "variables": [
                    "GA4 Measurement ID",
                    "Page URL",
                    "Click Element",
                    "Form Element"
                ]
            },
            "implementation_benefits": [
                "Centralized tag management",
                "No code changes for new tracking",
                "Built-in debugging tools",
                "Version control and collaboration"
            ]
        }
    
    def _assess_tracking_health(self, data: Dict) -> Dict[str, Any]:
        """Assess overall tracking health"""
        return {
            "data_freshness": "Good" if data.get("last_update_hours", 0) < 24 else "Poor",
            "event_volume": "Normal" if data.get("daily_events", 0) > 100 else "Low",
            "error_rate": "Good" if data.get("error_rate", 0) < 0.1 else "High",
            "sampling_rate": data.get("sampling_rate", 100),
            "overall_health": "Healthy" if all([
                data.get("last_update_hours", 0) < 24,
                data.get("daily_events", 0) > 100,
                data.get("error_rate", 0) < 0.1
            ]) else "Needs Attention"
        }
    
    def _identify_data_quality_issues(self, data: Dict) -> List[str]:
        """Identify data quality issues"""
        issues = []
        
        if data.get("bot_traffic_percentage", 0) > 10:
            issues.append("High bot traffic detected")
        
        if data.get("bounce_rate", 0) > 80:
            issues.append("Unusually high bounce rate")
        
        if data.get("session_duration_avg", 0) < 30:
            issues.append("Very short average session duration")
        
        return issues
    
    def _identify_missing_events(self, data: Dict) -> List[str]:
        """Identify missing or underperforming events"""
        missing = []
        
        expected_events = ["page_view", "scroll", "click", "form_start"]
        tracked_events = data.get("tracked_events", [])
        
        for event in expected_events:
            if event not in tracked_events:
                missing.append(f"Missing {event} events")
        
        return missing
    
    def _identify_optimizations(self, data: Dict) -> List[str]:
        """Identify optimization opportunities"""
        return [
            "Implement enhanced e-commerce tracking",
            "Add custom dimensions for better segmentation",
            "Set up funnel analysis for key user journeys",
            "Configure audience building for remarketing",
            "Implement cross-domain tracking if applicable"
        ]
    
    def _calculate_performance_metrics(self, data: Dict) -> Dict[str, Any]:
        """Calculate key performance metrics"""
        return {
            "tracking_coverage": f"{data.get('pages_with_tracking', 0)} / {data.get('total_pages', 1)} pages",
            "event_reliability": f"{100 - data.get('error_rate', 0) * 100:.1f}%",
            "data_completeness": f"{data.get('complete_sessions', 0) / data.get('total_sessions', 1) * 100:.1f}%"
        }
    
    def _generate_tracking_recommendations(self, analysis: Dict) -> List[str]:
        """Generate tracking improvement recommendations"""
        recommendations = []
        
        if analysis["tracking_health"]["overall_health"] != "Healthy":
            recommendations.append("Address tracking health issues immediately")
        
        if analysis["data_quality_issues"]:
            recommendations.append("Implement bot filtering and data quality measures")
        
        if analysis["missing_events"]:
            recommendations.append("Add missing event tracking for complete user journey visibility")
        
        return recommendations
    
    def _categorize_tracking_issue(self, issue_details: Dict) -> str:
        """Categorize tracking issue type"""
        issue = issue_details.get("issue", "").lower()
        
        if "no data" in issue or "not showing" in issue:
            return "Data Collection"
        elif "wrong" in issue or "incorrect" in issue:
            return "Data Quality"
        elif "events" in issue:
            return "Event Tracking"
        elif "ecommerce" in issue or "conversion" in issue:
            return "Conversion Tracking"
        else:
            return "General"

# MCP Tool definitions
async def design_tracking_strategy(website_config: Dict[str, Any]) -> Dict[str, Any]:
    """Design comprehensive Google Analytics tracking strategy for website"""
    specialist = GoogleAnalyticsSpecialist()
    return await specialist.design_tracking_strategy(website_config)

async def implement_ga4_tracking(implementation_config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate GA4 implementation code and configuration for various platforms"""
    specialist = GoogleAnalyticsSpecialist()
    return await specialist.implement_ga4_tracking(implementation_config)

async def analyze_tracking_performance(analytics_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze current Google Analytics tracking performance and identify issues"""
    specialist = GoogleAnalyticsSpecialist()
    return await specialist.analyze_tracking_performance(analytics_data)

async def setup_conversion_tracking(conversion_config: Dict[str, Any]) -> Dict[str, Any]:
    """Set up conversion tracking and goal configuration in Google Analytics"""
    specialist = GoogleAnalyticsSpecialist()
    return await specialist.setup_conversion_tracking(conversion_config)

async def troubleshoot_tracking_issues(issue_details: Dict[str, Any]) -> Dict[str, Any]:
    """Troubleshoot common Google Analytics tracking issues and provide solutions"""
    specialist = GoogleAnalyticsSpecialist()
    return await specialist.troubleshoot_tracking_issues(issue_details)
#!/usr/bin/env python3
"""
Stripe Payment Researcher - Critical for Q1 2025 Launch
Uses qwen2.5-coder:7b for code generation (94% success rate)
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import asyncio

class StripeResearcher:
    """
    Research-only agent for Stripe payment integration
    Specialized in SaaS subscription models for Fed Job Advisor
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "stripe"
        self.research_output = self.base_path / "research_outputs" / "tasks"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Load documentation
        self.documentation = self.load_documentation()
        self.critical_rules = self.load_critical_rules()
        
        # Fed Job Advisor specific configuration
        self.fed_config = {
            "tiers": {
                "local": {"price": 29, "name": "Local Search"},
                "mobile": {"price": 49, "name": "Mobile Nationwide"}
            },
            "model": "qwen2.5-coder:7b"  # Best for code generation
        }
    
    def load_documentation(self) -> Dict[str, Any]:
        """Load Stripe documentation with TTL check"""
        docs = {}
        
        # Load manifest
        manifest_path = self.docs_path / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                docs['manifest'] = json.load(f)
            
            # Check TTL (Stripe updates frequently)
            last_updated = datetime.fromisoformat(docs['manifest']['last_updated'])
            age_days = (datetime.now() - last_updated).days
            if age_days > docs['manifest']['ttl_days']:
                print(f"⚠️ Stripe docs are {age_days} days old - refresh recommended")
        
        # Load critical concepts
        critical_path = self.docs_path / "CRITICAL_stripe_concepts.md"
        if critical_path.exists():
            with open(critical_path) as f:
                docs['critical'] = f.read()
        
        # Load implementation guide
        impl_path = self.docs_path / "implementation_guide.json"
        if impl_path.exists():
            with open(impl_path) as f:
                docs['implementation'] = json.load(f)
        
        # Load quick reference
        ref_path = self.docs_path / "quick_reference.json"
        if ref_path.exists():
            with open(ref_path) as f:
                docs['reference'] = json.load(f)
        
        return docs
    
    def load_critical_rules(self) -> List[str]:
        """Critical Stripe integration rules"""
        return [
            "ALWAYS verify webhook signatures to prevent fraud",
            "Use webhook events as source of truth for subscription status",
            "Implement idempotency keys for payment operations",
            "Handle all subscription lifecycle events",
            "Test with Stripe CLI before production",
            "Never store card details - use Stripe tokens",
            "Always handle payment failures gracefully",
            "Implement subscription upgrade/downgrade logic"
        ]
    
    async def research_task(self, task: str, user_id: str = "system") -> Dict[str, Any]:
        """
        Phase 1: Research Stripe payment implementation
        """
        
        task_analysis = self._analyze_task(task)
        
        research = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "task_type": task_analysis['type'],
            "critical_requirements": self.critical_rules,
            "implementation_plan": self._create_implementation_plan(task_analysis),
            "stripe_resources": self._identify_stripe_resources(task_analysis),
            "code_templates": self._generate_code_templates(task_analysis),
            "testing_strategy": self._create_testing_strategy(task_analysis),
            "launch_checklist": self.documentation['manifest'].get('launch_checklist', [])
        }
        
        # Add Fed Job Advisor specific guidance
        if "subscription" in task.lower():
            research["fed_job_tiers"] = self.fed_config["tiers"]
            research["pricing_note"] = "Local: $29/mo, Mobile: $49/mo"
        
        # Save research report
        report_path = self._save_research_report(research)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "summary": research["implementation_plan"]["summary"],
            "critical_reminders": research["critical_requirements"][:3],
            "stripe_resources": len(research["stripe_resources"])
        }
    
    def _analyze_task(self, task: str) -> Dict[str, Any]:
        """Analyze Stripe-related task"""
        task_lower = task.lower()
        
        analysis = {
            "type": "unknown",
            "operations": [],
            "stripe_objects": []
        }
        
        # Determine task type
        if "subscription" in task_lower:
            analysis["type"] = "subscription_management"
            analysis["operations"].extend(["create_subscription", "manage_lifecycle"])
            analysis["stripe_objects"].extend(["Customer", "Subscription", "Price"])
        
        if "payment" in task_lower or "checkout" in task_lower:
            analysis["type"] = "payment_processing"
            analysis["operations"].append("checkout_session")
            analysis["stripe_objects"].extend(["CheckoutSession", "PaymentIntent"])
        
        if "webhook" in task_lower:
            analysis["type"] = "webhook_handling"
            analysis["operations"].append("webhook_verification")
            analysis["stripe_objects"].append("Webhook")
        
        if "customer" in task_lower:
            analysis["operations"].append("customer_management")
            analysis["stripe_objects"].append("Customer")
        
        return analysis
    
    def _create_implementation_plan(self, task_analysis: Dict) -> Dict[str, Any]:
        """Create Stripe implementation plan"""
        
        plan = {
            "summary": f"Stripe {task_analysis['type']} implementation",
            "steps": [],
            "endpoints": [],
            "database_changes": []
        }
        
        if task_analysis["type"] == "subscription_management":
            plan["steps"] = [
                "1. Create Stripe products and prices for Local/Mobile tiers",
                "2. Implement customer creation endpoint",
                "3. Create checkout session for subscription",
                "4. Handle success/cancel redirects",
                "5. Implement webhook handler for subscription events",
                "6. Store subscription status in database"
            ]
            plan["endpoints"] = [
                "POST /api/v1/payments/create-checkout-session",
                "POST /api/v1/payments/customer-portal",
                "POST /api/v1/webhooks/stripe",
                "GET /api/v1/payments/subscription-status"
            ]
            plan["database_changes"] = [
                "Add stripe_customer_id to users table",
                "Add subscription_status to users table",
                "Add subscription_tier to users table",
                "Create payments_history table"
            ]
        
        elif task_analysis["type"] == "webhook_handling":
            plan["steps"] = [
                "1. Create webhook endpoint",
                "2. Verify webhook signature",
                "3. Parse event type",
                "4. Handle each event type",
                "5. Update database accordingly",
                "6. Send notifications if needed"
            ]
            plan["critical_events"] = [
                "customer.subscription.created",
                "customer.subscription.updated",
                "customer.subscription.deleted",
                "invoice.payment_succeeded",
                "invoice.payment_failed"
            ]
        
        return plan
    
    def _identify_stripe_resources(self, task_analysis: Dict) -> List[Dict]:
        """Identify required Stripe resources"""
        resources = []
        
        for obj in task_analysis.get("stripe_objects", []):
            resources.append({
                "object": obj,
                "documentation": f"https://stripe.com/docs/api/{obj.lower()}s",
                "purpose": f"Required for {task_analysis['type']}"
            })
        
        return resources
    
    def _generate_code_templates(self, task_analysis: Dict) -> Dict[str, str]:
        """Generate code templates for implementation"""
        templates = {}
        
        if "subscription_management" in task_analysis["type"]:
            templates["create_checkout"] = """
@router.post("/create-checkout-session")
async def create_checkout_session(
    tier: str,  # 'local' or 'mobile'
    user: User = Depends(get_current_user)
):
    # Get or create Stripe customer
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(
            email=user.email,
            metadata={"user_id": str(user.id)}
        )
        user.stripe_customer_id = customer.id
        await db.commit()
    
    # Determine price based on tier
    price_id = "price_local_monthly" if tier == "local" else "price_mobile_monthly"
    
    # Create checkout session
    session = stripe.checkout.Session.create(
        customer=user.stripe_customer_id,
        payment_method_types=['card'],
        line_items=[{'price': price_id, 'quantity': 1}],
        mode='subscription',
        success_url=f"{FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{FRONTEND_URL}/payment/cancel",
        metadata={"user_id": str(user.id), "tier": tier}
    )
    
    return {"checkout_url": session.url}
"""
        
        if "webhook_handling" in task_analysis["type"]:
            templates["webhook_handler"] = """
@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event['type'] == 'customer.subscription.created':
        subscription = event['data']['object']
        await handle_subscription_created(subscription)
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        await handle_subscription_updated(subscription)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        await handle_subscription_cancelled(subscription)
    
    return {"status": "success"}
"""
        
        return templates
    
    def _create_testing_strategy(self, task_analysis: Dict) -> Dict[str, Any]:
        """Create testing strategy for Stripe integration"""
        return {
            "test_mode": "Use test API keys during development",
            "test_cards": {
                "success": "4242 4242 4242 4242",
                "decline": "4000 0000 0000 0002",
                "3d_secure": "4000 0025 0000 3155"
            },
            "stripe_cli": [
                "stripe listen --forward-to localhost:8000/api/v1/webhooks/stripe",
                "stripe trigger payment_intent.succeeded",
                "stripe trigger customer.subscription.created"
            ],
            "test_scenarios": [
                "Successful subscription creation",
                "Payment failure handling",
                "Subscription cancellation",
                "Plan upgrade/downgrade",
                "Webhook signature verification"
            ]
        }
    
    async def review_implementation(self, code: str, user_id: str = "system") -> Dict[str, Any]:
        """
        Phase 3: Review Stripe implementation for security and best practices
        """
        
        review = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "compliant": True,
            "violations": [],
            "warnings": [],
            "passed": [],
            "score": 100
        }
        
        # Critical security checks
        if "stripe.Webhook.construct_event" not in code:
            review["violations"].append("❌ CRITICAL: No webhook signature verification!")
            review["compliant"] = False
            review["score"] -= 40
        else:
            review["passed"].append("✅ Webhook signature verification present")
        
        # Check for proper error handling
        if "try" not in code or "except" not in code:
            review["warnings"].append("⚠️ No error handling for Stripe API calls")
            review["score"] -= 15
        else:
            review["passed"].append("✅ Error handling implemented")
        
        # Check for idempotency
        if "idempotency_key" in code:
            review["passed"].append("✅ Idempotency keys used")
        else:
            review["warnings"].append("⚠️ Consider using idempotency keys for payment operations")
            review["score"] -= 10
        
        # Check for proper customer handling
        if "stripe.Customer" in code:
            review["passed"].append("✅ Customer object handling present")
        
        # Check for test mode
        if "sk_test" in code or "pk_test" in code:
            review["warnings"].append("⚠️ Test keys detected - ensure production keys for launch")
        
        # Check for subscription tier handling
        if "local" in code and "mobile" in code:
            review["passed"].append("✅ Both Fed Job Advisor tiers handled")
        else:
            review["warnings"].append("⚠️ Ensure both Local ($29) and Mobile ($49) tiers are handled")
        
        review["recommendation"] = "✅ Ready for testing" if review["score"] >= 70 else "❌ Address violations first"
        
        return review
    
    def _save_research_report(self, research: Dict) -> Path:
        """Save research report to markdown"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.research_output / f"stripe_research_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write(f"# Stripe Payment Integration Research\n\n")
            f.write(f"**Generated**: {research['timestamp']}\n")
            f.write(f"**Task**: {research['task']}\n")
            f.write(f"**Type**: {research['task_type']}\n\n")
            
            f.write("## Fed Job Advisor Pricing\n")
            f.write("- **Local**: $29/month (50-mile radius)\n")
            f.write("- **Mobile**: $49/month (nationwide access)\n\n")
            
            f.write("## Implementation Plan\n")
            f.write(f"{research['implementation_plan']['summary']}\n\n")
            
            if research['implementation_plan'].get('steps'):
                f.write("### Steps\n")
                for step in research['implementation_plan']['steps']:
                    f.write(f"{step}\n")
                f.write("\n")
            
            if research['implementation_plan'].get('endpoints'):
                f.write("### API Endpoints\n")
                for endpoint in research['implementation_plan']['endpoints']:
                    f.write(f"- `{endpoint}`\n")
                f.write("\n")
            
            if research.get('code_templates'):
                f.write("## Code Templates\n")
                for name, template in research['code_templates'].items():
                    f.write(f"### {name}\n")
                    f.write(f"```python\n{template}\n```\n\n")
            
            f.write("## Launch Checklist\n")
            for item in research.get('launch_checklist', []):
                f.write(f"- [ ] {item}\n")
        
        return report_path
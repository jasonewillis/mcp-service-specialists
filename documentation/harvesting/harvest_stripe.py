#!/usr/bin/env python3
"""
Stripe API Documentation Harvester
Critical for payment integration - Q1 2025 launch requirement
"""

import json
from datetime import datetime
from pathlib import Path

def harvest_stripe_docs():
    """Harvest Stripe API documentation for subscription management"""
    
    base_dir = Path(__file__).parent.parent / "external_services" / "stripe"
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💳 Harvesting Stripe documentation to {base_dir}")
    
    # Critical Stripe concepts for SaaS subscriptions
    critical_concepts = {
        "Products_and_Prices": {
            "importance": "CRITICAL",
            "description": "Define your subscription tiers",
            "fed_job_tiers": {
                "local": {"price": 29, "price_id": "price_local_monthly"},
                "mobile": {"price": 49, "price_id": "price_mobile_monthly"}
            }
        },
        "Customers": {
            "importance": "CRITICAL",
            "description": "User accounts linked to subscriptions",
            "best_practice": "Create customer before subscription"
        },
        "Subscriptions": {
            "importance": "CRITICAL",
            "description": "Recurring billing cycles",
            "key_fields": ["status", "current_period_end", "cancel_at_period_end"]
        },
        "Webhooks": {
            "importance": "CRITICAL",
            "description": "Real-time payment events",
            "critical_events": [
                "customer.subscription.created",
                "customer.subscription.updated",
                "customer.subscription.deleted",
                "invoice.payment_succeeded",
                "invoice.payment_failed"
            ]
        },
        "Checkout_Sessions": {
            "importance": "HIGH",
            "description": "Hosted payment page",
            "mode": "subscription"
        }
    }
    
    # Save critical concepts
    with open(base_dir / "CRITICAL_stripe_concepts.md", "w") as f:
        f.write("# ⚠️ CRITICAL: Stripe Integration Concepts\n\n")
        f.write("## For Fed Job Advisor Launch (Q1 2025)\n\n")
        
        for concept, info in critical_concepts.items():
            f.write(f"### {concept.replace('_', ' ')}\n")
            f.write(f"- **Importance**: {info['importance']}\n")
            f.write(f"- **Description**: {info['description']}\n")
            if 'fed_job_tiers' in info:
                f.write(f"- **Fed Job Tiers**: \n")
                for tier, details in info['fed_job_tiers'].items():
                    f.write(f"  - {tier}: ${details['price']}/mo\n")
            if 'critical_events' in info:
                f.write(f"- **Critical Events**: \n")
                for event in info['critical_events']:
                    f.write(f"  - `{event}`\n")
            f.write("\n")
    
    # Stripe API implementation template
    implementation_template = {
        "setup": {
            "1_install": "pip install stripe",
            "2_configure": "stripe.api_key = os.environ['STRIPE_SECRET_KEY']",
            "3_test_mode": "Use test keys during development"
        },
        "create_subscription": {
            "steps": [
                "1. Create or retrieve customer",
                "2. Create checkout session",
                "3. Redirect to Stripe hosted page",
                "4. Handle success/cancel URLs",
                "5. Listen for webhook confirmation"
            ],
            "code_template": """
# Create checkout session
session = stripe.checkout.Session.create(
    customer=customer_id,
    payment_method_types=['card'],
    line_items=[{
        'price': price_id,  # 'price_local_monthly' or 'price_mobile_monthly'
        'quantity': 1,
    }],
    mode='subscription',
    success_url=f'{YOUR_DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}',
    cancel_url=f'{YOUR_DOMAIN}/cancel',
)
"""
        },
        "webhook_handler": {
            "endpoint": "/api/v1/webhooks/stripe",
            "verification": "stripe.Webhook.construct_event()",
            "events_to_handle": [
                "customer.subscription.created",
                "customer.subscription.updated",
                "customer.subscription.deleted",
                "invoice.payment_succeeded",
                "invoice.payment_failed"
            ]
        }
    }
    
    # Save implementation guide
    with open(base_dir / "implementation_guide.json", "w") as f:
        json.dump(implementation_template, f, indent=2)
    
    # Quick reference for Fed Job Advisor
    quick_ref = {
        "test_cards": {
            "success": "4242 4242 4242 4242",
            "decline": "4000 0000 0000 0002",
            "requires_auth": "4000 0025 0000 3155"
        },
        "subscription_statuses": [
            "active",
            "past_due",
            "canceled",
            "incomplete",
            "incomplete_expired",
            "trialing",
            "unpaid"
        ],
        "fed_job_specific": {
            "tiers": ["local", "mobile"],
            "prices": {"local": 29, "mobile": 49},
            "features": {
                "local": ["50-mile radius", "Basic matching", "5 saved searches"],
                "mobile": ["Nationwide", "AI matching", "Unlimited searches", "Analytics"]
            }
        }
    }
    
    with open(base_dir / "quick_reference.json", "w") as f:
        json.dump(quick_ref, f, indent=2)
    
    # Create manifest with TTL
    manifest = {
        "service": "stripe",
        "last_updated": datetime.now().isoformat(),
        "ttl_days": 7,  # Stripe updates frequently
        "api_version": "2024-11-20.acacia",
        "critical_requirements": [
            "Configure webhook endpoint",
            "Verify webhook signatures",
            "Handle subscription lifecycle events",
            "Use idempotency keys for payments",
            "Test with Stripe CLI before production"
        ],
        "launch_checklist": [
            "Create products and prices in Stripe Dashboard",
            "Set up webhook endpoint",
            "Configure success/cancel URLs",
            "Test full payment flow",
            "Enable production keys"
        ]
    }
    
    with open(base_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Stripe documentation harvested successfully!")
    print(f"💳 Critical file: {base_dir}/CRITICAL_stripe_concepts.md")
    
    return base_dir

if __name__ == "__main__":
    harvest_stripe_docs()
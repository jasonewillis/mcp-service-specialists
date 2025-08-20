#!/usr/bin/env python3
"""
Stripe Payment Specialist - Ultra-deep expertise in Stripe payment processing
Specialized for subscription models and SaaS pricing for Fed Job Advisor
"""

from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import asyncio
from enum import Enum
from decimal import Decimal

class StripeProduct(Enum):
    """Stripe product types"""
    SUBSCRIPTION = "subscription"
    ONE_TIME = "one_time"  
    USAGE_BASED = "usage_based"
    TIERED = "tiered"

class StripeWebhookEvent(Enum):
    """Critical Stripe webhook events"""
    PAYMENT_SUCCEEDED = "payment_intent.succeeded"
    PAYMENT_FAILED = "payment_intent.payment_failed"
    SUBSCRIPTION_CREATED = "customer.subscription.created"
    SUBSCRIPTION_UPDATED = "customer.subscription.updated"
    SUBSCRIPTION_DELETED = "customer.subscription.deleted"
    INVOICE_PAID = "invoice.paid"
    INVOICE_FAILED = "invoice.payment_failed"
    CUSTOMER_CREATED = "customer.created"
    CHARGE_DISPUTED = "charge.dispute.created"

class StripeSpecialist:
    """
    Ultra-specialized agent for Stripe payment integration
    Complete knowledge of Stripe API v2023+ and best practices
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "stripe"
        self.research_output = self.base_path / "research_outputs" / "stripe_implementation"
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Exhaustive Stripe knowledge base
        self.knowledge_base = {
            "subscription_setup": {
                "products_and_prices": {
                    "create_product": """
stripe.Product.create(
    name="Fed Job Advisor Pro",
    description="Premium federal job search features",
    metadata={"tier": "premium"}
)""",
                    "create_price": """
stripe.Price.create(
    product=product.id,
    unit_amount=4900,  # $49.00
    currency="usd",
    recurring={"interval": "month"},
    metadata={"plan": "mobile"}
)""",
                    "tiers": {
                        "local": {"price": 2900, "features": ["basic_search", "saved_jobs"]},
                        "mobile": {"price": 4900, "features": ["all_features", "mobile_app", "analytics"]}
                    }
                },
                "checkout_session": """
stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': price_id,
        'quantity': 1,
    }],
    mode='subscription',
    success_url=domain + '/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url=domain + '/cancel',
    customer_email=user_email,
    metadata={'user_id': user_id},
    subscription_data={
        'trial_period_days': 14,
        'metadata': {'user_id': user_id}
    },
    allow_promotion_codes=True,
    billing_address_collection='auto',
    automatic_tax={'enabled': True}
)""",
                "customer_portal": """
stripe.billing_portal.Session.create(
    customer=customer_id,
    return_url=domain + '/account',
)""",
                "trial_periods": {
                    "standard": 14,
                    "extended": 30,
                    "no_payment_required": "trial_settings.default_behavior='opt_in'"
                }
            },
            
            "webhook_handling": {
                "signature_verification": """
import stripe
from fastapi import Request, HTTPException

async def verify_webhook(request: Request, endpoint_secret: str):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        return event
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
""",
                "event_handlers": {
                    "payment_intent.succeeded": """
async def handle_payment_succeeded(event):
    payment_intent = event['data']['object']
    customer_id = payment_intent['customer']
    amount = payment_intent['amount'] / 100
    
    # Update user subscription status
    await update_user_subscription(customer_id, 'active')
    
    # Send confirmation email
    await send_payment_confirmation(customer_id, amount)
    
    # Log for analytics
    await log_payment_event(customer_id, amount, 'succeeded')
""",
                    "customer.subscription.deleted": """
async def handle_subscription_cancelled(event):
    subscription = event['data']['object']
    customer_id = subscription['customer']
    
    # Grace period until period end
    cancel_at = subscription['current_period_end']
    
    # Update user access
    await schedule_access_removal(customer_id, cancel_at)
    
    # Send cancellation email
    await send_cancellation_email(customer_id)
    
    # Trigger win-back campaign
    await trigger_winback_campaign(customer_id)
""",
                    "invoice.payment_failed": """
async def handle_payment_failed(event):
    invoice = event['data']['object']
    customer_id = invoice['customer']
    attempt = invoice['attempt_count']
    
    if attempt == 1:
        # Send payment retry email
        await send_payment_retry_email(customer_id)
    elif attempt == 3:
        # Send final warning
        await send_final_payment_warning(customer_id)
    elif attempt >= 4:
        # Suspend access
        await suspend_user_access(customer_id)
"""
                },
                "idempotency": {
                    "importance": "Prevent duplicate charges on retries",
                    "implementation": "Use idempotency_key in requests",
                    "example": "stripe.PaymentIntent.create(idempotency_key=unique_key)"
                }
            },
            
            "payment_methods": {
                "cards": {
                    "test_cards": {
                        "success": "4242424242424242",
                        "decline": "4000000000000002",
                        "insufficient_funds": "4000000000009995",
                        "3d_secure": "4000002500003155"
                    },
                    "pci_compliance": "Use Stripe Elements or Checkout",
                    "card_saving": "Setup payment_intent with setup_future_usage"
                },
                "alternative_payments": {
                    "ach": "payment_method_types=['us_bank_account']",
                    "apple_pay": "payment_request_button_element",
                    "google_pay": "payment_request_button_element"
                }
            },
            
            "security_compliance": {
                "pci_dss": {
                    "level": "SAQ A with Stripe Elements",
                    "requirements": [
                        "Never handle raw card data",
                        "Use HTTPS everywhere",
                        "Implement CSP headers",
                        "Regular security scans"
                    ]
                },
                "sca_3ds": {
                    "european_requirements": "Strong Customer Authentication",
                    "implementation": "Use Payment Intents API",
                    "exemptions": ["low_value", "recurring", "merchant_initiated"]
                },
                "data_protection": {
                    "gdpr": "Delete customer data on request",
                    "encryption": "All data encrypted at rest",
                    "retention": "7 years for tax compliance"
                }
            },
            
            "error_handling": {
                "api_errors": {
                    "rate_limit": {"code": "rate_limit", "retry": "exponential_backoff"},
                    "api_key_invalid": {"code": "api_key_invalid", "fix": "Check secret key"},
                    "resource_missing": {"code": "resource_missing", "fix": "Verify ID exists"}
                },
                "card_errors": {
                    "card_declined": {
                        "codes": ["generic_decline", "insufficient_funds", "lost_card"],
                        "user_message": "Your card was declined. Please try another payment method."
                    },
                    "expired_card": {
                        "code": "expired_card",
                        "user_message": "Your card has expired. Please update your payment method."
                    },
                    "incorrect_cvc": {
                        "code": "incorrect_cvc",
                        "user_message": "The security code is incorrect. Please check and try again."
                    }
                },
                "webhook_errors": {
                    "signature_verification": "Check endpoint secret",
                    "duplicate_events": "Implement idempotency",
                    "timeout": "Process async and return 200 quickly"
                }
            },
            
            "testing_strategy": {
                "test_mode": {
                    "api_keys": "Use sk_test_ keys",
                    "webhooks": "Use Stripe CLI for local testing",
                    "data": "Test mode data separate from live"
                },
                "stripe_cli": {
                    "install": "brew install stripe/stripe-cli/stripe",
                    "login": "stripe login",
                    "listen": "stripe listen --forward-to localhost:8000/webhook",
                    "trigger": "stripe trigger payment_intent.succeeded"
                },
                "testing_scenarios": [
                    "Successful payment",
                    "Failed payment",
                    "Subscription creation",
                    "Subscription cancellation",
                    "Payment retry",
                    "Refund processing",
                    "Dispute handling"
                ]
            },
            
            "fed_job_advisor_implementation": {
                "pricing_tiers": {
                    "local": {
                        "price_id": "price_local_monthly",
                        "amount": 2900,
                        "interval": "month",
                        "features": [
                            "Basic job search",
                            "5 saved searches",
                            "Email alerts"
                        ]
                    },
                    "mobile": {
                        "price_id": "price_mobile_monthly",
                        "amount": 4900,
                        "interval": "month",
                        "features": [
                            "All Local features",
                            "Unlimited saved searches",
                            "Advanced analytics",
                            "Resume optimization",
                            "Mobile app access"
                        ]
                    }
                },
                "checkout_flow": {
                    "steps": [
                        "User selects plan",
                        "Redirect to Stripe Checkout",
                        "Handle success/cancel redirect",
                        "Process webhook confirmation",
                        "Activate user subscription"
                    ]
                },
                "user_management": {
                    "link_customer": "Store stripe_customer_id in users table",
                    "subscription_status": "Track in database, verify with Stripe",
                    "access_control": "Check subscription status on API calls"
                }
            },
            
            "revenue_optimization": {
                "pricing_strategies": {
                    "psychological_pricing": "End prices in 9 ($29, $49)",
                    "anchoring": "Show higher tier first",
                    "bundling": "Annual plans with discount"
                },
                "reduce_churn": {
                    "dunning": "Smart retry schedule for failed payments",
                    "paused_subscriptions": "Offer to pause instead of cancel",
                    "win_back": "Discount offers for cancelled users"
                },
                "increase_ltv": {
                    "upsells": "Promote higher tiers at key moments",
                    "add_ons": "Additional features as one-time purchases",
                    "referrals": "Incentivize user referrals"
                }
            }
        }
    
    async def implement_subscription_system(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete Stripe subscription implementation
        """
        timestamp = datetime.now().isoformat()
        
        implementation = {
            "timestamp": timestamp,
            "backend_code": self._generate_backend_code(config),
            "frontend_code": self._generate_frontend_code(config),
            "webhook_handler": self._generate_webhook_handler(config),
            "database_schema": self._generate_database_schema(),
            "environment_variables": self._generate_env_vars(),
            "testing_guide": self._generate_testing_guide()
        }
        
        # Save implementation
        output_file = self.research_output / f"{timestamp}_subscription_implementation.json"
        with open(output_file, 'w') as f:
            json.dump(implementation, f, indent=2)
        
        return implementation
    
    def _generate_backend_code(self, config: Dict[str, Any]) -> str:
        """Generate FastAPI backend code for Stripe"""
        return """# stripe_service.py
import stripe
from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
import os

stripe.api_key = os.environ['STRIPE_SECRET_KEY']
webhook_secret = os.environ['STRIPE_WEBHOOK_SECRET']

router = APIRouter(prefix="/api/v1/payments")

@router.post("/create-checkout-session")
async def create_checkout_session(plan: str, user_email: str):
    \"\"\"Create Stripe checkout session for subscription\"\"\"
    
    price_ids = {
        'local': os.environ['STRIPE_PRICE_LOCAL'],
        'mobile': os.environ['STRIPE_PRICE_MOBILE']
    }
    
    if plan not in price_ids:
        raise HTTPException(400, "Invalid plan")
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_ids[plan],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f"{os.environ['FRONTEND_URL']}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.environ['FRONTEND_URL']}/pricing",
            customer_email=user_email,
            subscription_data={
                'trial_period_days': 14,
                'metadata': {'plan': plan}
            },
            metadata={'plan': plan}
        )
        return {"checkout_url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(400, str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    \"\"\"Handle Stripe webhook events\"\"\"
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    
    # Handle events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        await fulfill_subscription(session)
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        await handle_subscription_cancelled(subscription)
    
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        await handle_payment_failed(invoice)
    
    return {"received": True}

@router.post("/customer-portal")
async def create_portal_session(customer_id: str):
    \"\"\"Create customer portal session for subscription management\"\"\"
    
    try:
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=f"{os.environ['FRONTEND_URL']}/account"
        )
        return {"portal_url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(400, str(e))

async def fulfill_subscription(session: Dict[str, Any]):
    \"\"\"Activate user subscription after successful payment\"\"\"
    customer_id = session['customer']
    subscription_id = session['subscription']
    
    # Update user record
    # await db.update_user_subscription(customer_id, subscription_id, 'active')
    
    # Send welcome email
    # await email.send_welcome_email(session['customer_email'])

async def handle_subscription_cancelled(subscription: Dict[str, Any]):
    \"\"\"Handle subscription cancellation\"\"\"
    customer_id = subscription['customer']
    
    # Update user access
    # await db.update_user_subscription(customer_id, None, 'cancelled')

async def handle_payment_failed(invoice: Dict[str, Any]):
    \"\"\"Handle failed payment attempts\"\"\"
    customer_id = invoice['customer']
    attempt_count = invoice['attempt_count']
    
    if attempt_count >= 3:
        # Suspend access after 3 failures
        # await db.update_user_subscription(customer_id, None, 'suspended')
        pass
"""
    
    def _generate_frontend_code(self, config: Dict[str, Any]) -> str:
        """Generate React frontend code for Stripe"""
        return """// PricingPage.tsx
import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

interface PricingTier {
  name: string;
  price: number;
  features: string[];
  planId: string;
}

const tiers: PricingTier[] = [
  {
    name: 'Local',
    price: 29,
    features: ['Basic job search', '5 saved searches', 'Email alerts'],
    planId: 'local'
  },
  {
    name: 'Mobile',
    price: 49,
    features: ['Everything in Local', 'Unlimited saved searches', 'Advanced analytics', 'Resume optimization', 'Mobile app'],
    planId: 'mobile'
  }
];

export default function PricingPage() {
  const [loading, setLoading] = useState<string | null>(null);
  
  const handleSubscribe = async (planId: string) => {
    setLoading(planId);
    
    try {
      // Create checkout session
      const response = await fetch('/api/v1/payments/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan: planId,
          user_email: user.email // Get from auth context
        })
      });
      
      const { checkout_url } = await response.json();
      
      // Redirect to Stripe Checkout
      window.location.href = checkout_url;
      
    } catch (error) {
      console.error('Subscription error:', error);
      alert('Something went wrong. Please try again.');
    } finally {
      setLoading(null);
    }
  };
  
  return (
    <div className="pricing-container">
      <h1>Choose Your Plan</h1>
      <p>14-day free trial. Cancel anytime.</p>
      
      <div className="pricing-tiers">
        {tiers.map((tier) => (
          <div key={tier.planId} className="pricing-card">
            <h2>{tier.name}</h2>
            <div className="price">
              <span className="currency">$</span>
              <span className="amount">{tier.price}</span>
              <span className="period">/month</span>
            </div>
            
            <ul className="features">
              {tier.features.map((feature, i) => (
                <li key={i}>{feature}</li>
              ))}
            </ul>
            
            <button
              onClick={() => handleSubscribe(tier.planId)}
              disabled={loading === tier.planId}
              className="subscribe-button"
            >
              {loading === tier.planId ? 'Loading...' : 'Start Free Trial'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

// PaymentSuccess.tsx
export function PaymentSuccess() {
  React.useEffect(() => {
    // Verify session and activate subscription
    const sessionId = new URLSearchParams(window.location.search).get('session_id');
    if (sessionId) {
      // Verify with backend
      fetch(`/api/v1/payments/verify-session/${sessionId}`)
        .then(() => {
          // Redirect to dashboard
          window.location.href = '/dashboard';
        });
    }
  }, []);
  
  return (
    <div>
      <h1>Payment Successful!</h1>
      <p>Your subscription is now active.</p>
    </div>
  );
}
"""
    
    def _generate_webhook_handler(self, config: Dict[str, Any]) -> str:
        """Generate webhook handler code"""
        return """# webhook_handlers.py
import stripe
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class StripeWebhookHandler:
    \"\"\"Handle all Stripe webhook events\"\"\"
    
    def __init__(self, db, email_service):
        self.db = db
        self.email = email_service
        self.handlers = {
            'checkout.session.completed': self.handle_checkout_completed,
            'customer.subscription.created': self.handle_subscription_created,
            'customer.subscription.updated': self.handle_subscription_updated,
            'customer.subscription.deleted': self.handle_subscription_deleted,
            'invoice.paid': self.handle_invoice_paid,
            'invoice.payment_failed': self.handle_payment_failed,
            'customer.created': self.handle_customer_created,
        }
    
    async def process_event(self, event: Dict[str, Any]):
        \"\"\"Process webhook event\"\"\"
        event_type = event['type']
        
        if event_type in self.handlers:
            try:
                await self.handlers[event_type](event['data']['object'])
                logger.info(f"Processed {event_type} event")
            except Exception as e:
                logger.error(f"Error processing {event_type}: {e}")
                raise
        else:
            logger.info(f"Unhandled event type: {event_type}")
    
    async def handle_checkout_completed(self, session: Dict[str, Any]):
        \"\"\"Handle successful checkout\"\"\"
        customer_id = session['customer']
        subscription_id = session['subscription']
        customer_email = session['customer_email']
        
        # Create or update user
        user = await self.db.get_user_by_email(customer_email)
        if not user:
            user = await self.db.create_user(
                email=customer_email,
                stripe_customer_id=customer_id
            )
        
        # Update subscription
        await self.db.update_user_subscription(
            user_id=user.id,
            stripe_customer_id=customer_id,
            stripe_subscription_id=subscription_id,
            status='active',
            plan=session['metadata'].get('plan', 'local')
        )
        
        # Send welcome email
        await self.email.send_welcome_email(customer_email)
    
    async def handle_subscription_deleted(self, subscription: Dict[str, Any]):
        \"\"\"Handle subscription cancellation\"\"\"
        customer_id = subscription['customer']
        
        # Update database
        await self.db.update_subscription_status(
            stripe_customer_id=customer_id,
            status='cancelled',
            cancelled_at=subscription['canceled_at']
        )
        
        # Send cancellation email
        customer = await self.db.get_user_by_stripe_id(customer_id)
        if customer:
            await self.email.send_cancellation_email(customer.email)
    
    async def handle_payment_failed(self, invoice: Dict[str, Any]):
        \"\"\"Handle failed payment\"\"\"
        customer_id = invoice['customer']
        attempt_count = invoice['attempt_count']
        
        customer = await self.db.get_user_by_stripe_id(customer_id)
        if not customer:
            return
        
        if attempt_count == 1:
            # First failure - send gentle reminder
            await self.email.send_payment_retry_email(customer.email)
        elif attempt_count == 3:
            # Third failure - send warning
            await self.email.send_payment_warning_email(customer.email)
        elif attempt_count >= 4:
            # Final failure - suspend access
            await self.db.update_subscription_status(
                stripe_customer_id=customer_id,
                status='suspended'
            )
            await self.email.send_access_suspended_email(customer.email)
"""
    
    def _generate_database_schema(self) -> str:
        """Generate database schema for subscriptions"""
        return """-- Subscription tables for PostgreSQL

-- Users table extension
ALTER TABLE users ADD COLUMN IF NOT EXISTS
    stripe_customer_id VARCHAR(255) UNIQUE,
    subscription_status VARCHAR(50) DEFAULT 'inactive',
    subscription_plan VARCHAR(50),
    subscription_started_at TIMESTAMP,
    subscription_ends_at TIMESTAMP,
    trial_ends_at TIMESTAMP;

CREATE INDEX idx_users_stripe_customer ON users(stripe_customer_id);
CREATE INDEX idx_users_subscription_status ON users(subscription_status);

-- Subscriptions history table
CREATE TABLE IF NOT EXISTS subscription_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    plan VARCHAR(50),
    status VARCHAR(50),
    amount DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'usd',
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancelled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_subscription_history_user ON subscription_history(user_id);
CREATE INDEX idx_subscription_stripe ON subscription_history(stripe_subscription_id);

-- Payment history table
CREATE TABLE IF NOT EXISTS payment_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    stripe_payment_intent_id VARCHAR(255) UNIQUE,
    stripe_invoice_id VARCHAR(255),
    amount DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'usd',
    status VARCHAR(50),
    payment_method VARCHAR(50),
    failure_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payment_history_user ON payment_history(user_id);
CREATE INDEX idx_payment_intent ON payment_history(stripe_payment_intent_id);

-- Webhook events table (for idempotency)
CREATE TABLE IF NOT EXISTS stripe_webhook_events (
    id SERIAL PRIMARY KEY,
    stripe_event_id VARCHAR(255) UNIQUE,
    event_type VARCHAR(100),
    processed BOOLEAN DEFAULT FALSE,
    payload JSONB,
    error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

CREATE INDEX idx_webhook_events_stripe ON stripe_webhook_events(stripe_event_id);
CREATE INDEX idx_webhook_events_type ON stripe_webhook_events(event_type);
"""
    
    def _generate_env_vars(self) -> str:
        """Generate required environment variables"""
        return """# Stripe Environment Variables

# API Keys
STRIPE_SECRET_KEY=sk_test_... # Get from Stripe Dashboard
STRIPE_PUBLISHABLE_KEY=pk_test_... # Get from Stripe Dashboard

# Webhook Secret
STRIPE_WEBHOOK_SECRET=whsec_... # Get from Stripe Webhook settings

# Price IDs (create in Stripe Dashboard)
STRIPE_PRICE_LOCAL=price_... # Local tier price ID
STRIPE_PRICE_MOBILE=price_... # Mobile tier price ID

# URLs
FRONTEND_URL=https://fedjobadvisor.com
PAYMENT_SUCCESS_URL=https://fedjobadvisor.com/payment-success
PAYMENT_CANCEL_URL=https://fedjobadvisor.com/pricing

# Optional
STRIPE_TAX_ENABLED=true
STRIPE_TRIAL_DAYS=14
STRIPE_CURRENCY=usd
"""
    
    def _generate_testing_guide(self) -> str:
        """Generate testing guide"""
        return """# Stripe Testing Guide

## Setup Test Environment

1. Install Stripe CLI
```bash
brew install stripe/stripe-cli/stripe
stripe login
```

2. Forward webhooks to local
```bash
stripe listen --forward-to localhost:8000/api/v1/payments/webhook
```

3. Test cards
- Success: 4242 4242 4242 4242
- Decline: 4000 0000 0000 0002
- 3D Secure: 4000 0025 0000 3155

## Test Scenarios

### Successful Subscription
```bash
stripe trigger checkout.session.completed
```

### Failed Payment
```bash
stripe trigger invoice.payment_failed
```

### Subscription Cancellation
```bash
stripe trigger customer.subscription.deleted
```

## Monitoring

- Check Stripe Dashboard > Developers > Logs
- Monitor webhook attempts
- Review payment events

## Common Issues

1. Webhook signature fails
   - Check STRIPE_WEBHOOK_SECRET is correct
   - Ensure raw body is used for verification

2. Checkout redirects fail
   - Verify success_url and cancel_url
   - Check CORS settings

3. Customer not created
   - Ensure customer_email is provided
   - Check for duplicate customers
"""
    
    async def diagnose_payment_issue(self, error: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnose Stripe payment issues
        """
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "error": error,
            "likely_cause": None,
            "solutions": [],
            "code_fixes": []
        }
        
        error_lower = error.lower()
        
        # API Key issues
        if "api_key" in error_lower or "authentication" in error_lower:
            diagnosis["likely_cause"] = "Invalid or missing API key"
            diagnosis["solutions"] = [
                "Check STRIPE_SECRET_KEY environment variable",
                "Ensure using correct key (test vs live)",
                "Verify key starts with sk_test_ or sk_live_"
            ]
        
        # Webhook issues
        elif "signature" in error_lower or "webhook" in error_lower:
            diagnosis["likely_cause"] = "Webhook signature verification failed"
            diagnosis["solutions"] = [
                "Check STRIPE_WEBHOOK_SECRET is correct",
                "Use raw request body for verification",
                "Ensure webhook endpoint is correct in Stripe Dashboard"
            ]
            diagnosis["code_fixes"].append("""
# Correct webhook verification
payload = await request.body()  # Raw body
sig_header = request.headers.get('stripe-signature')
event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
""")
        
        # Card errors
        elif "card_declined" in error_lower:
            diagnosis["likely_cause"] = "Card was declined by issuer"
            diagnosis["solutions"] = [
                "Ask customer to try another card",
                "Check if card has sufficient funds",
                "Verify billing address matches"
            ]
        
        # Price/Product issues
        elif "price" in error_lower or "product" in error_lower:
            diagnosis["likely_cause"] = "Invalid price or product ID"
            diagnosis["solutions"] = [
                "Verify price ID exists in Stripe Dashboard",
                "Check if using test mode price in live mode",
                "Ensure product is active"
            ]
        
        return diagnosis

# CLI interface
if __name__ == "__main__":
    import sys
    
    specialist = StripeSpecialist()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "implement":
            config = {}
            if len(sys.argv) > 2:
                config = json.loads(sys.argv[2])
            result = asyncio.run(specialist.implement_subscription_system(config))
            print(json.dumps(result, indent=2))
        
        elif command == "diagnose":
            if len(sys.argv) > 2:
                error = sys.argv[2]
                result = asyncio.run(specialist.diagnose_payment_issue(error, {}))
                print(json.dumps(result, indent=2))
    else:
        print("Stripe Payment Specialist")
        print("Commands:")
        print("  implement [config] - Generate subscription implementation")
        print("  diagnose <error> - Diagnose payment issue")
#!/usr/bin/env python3
"""
Stripe Checkout Session Example
"""

import stripe
import os

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

# Create checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': 'price_xxxxx',  # Your price ID
        'quantity': 1,
    }],
    mode='subscription',
    success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://example.com/cancel',
    metadata={'user_id': '12345'}
)

print(f"Checkout URL: {session.url}")

# ⚠️ CRITICAL: Stripe Integration Concepts

## For Fed Job Advisor Launch (Q1 2025)

### Products and Prices
- **Importance**: CRITICAL
- **Description**: Define your subscription tiers
- **Fed Job Tiers**: 
  - local: $29/mo
  - mobile: $49/mo

### Customers
- **Importance**: CRITICAL
- **Description**: User accounts linked to subscriptions

### Subscriptions
- **Importance**: CRITICAL
- **Description**: Recurring billing cycles

### Webhooks
- **Importance**: CRITICAL
- **Description**: Real-time payment events
- **Critical Events**: 
  - `customer.subscription.created`
  - `customer.subscription.updated`
  - `customer.subscription.deleted`
  - `invoice.payment_succeeded`
  - `invoice.payment_failed`

### Checkout Sessions
- **Importance**: HIGH
- **Description**: Hosted payment page


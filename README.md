# UQPAY Python SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the [UQPAY API](https://developer.uqpay.com/api/#/) — a comprehensive payment and card issuing platform.

## Requirements

- Python 3.9+

## Installation

```bash
pip install uqpay
```

## Quick Start

```python
from uqpay import UQPayClient

# Sandbox (for testing)
client = UQPayClient(client_id="your-client-id", api_key="your-api-key", environment="sandbox")

# Production
client = UQPayClient(client_id="your-client-id", api_key="your-api-key", environment="production")
```

## Authentication

The SDK handles OAuth2 authentication automatically. It fetches an access token using your `client_id` and `api_key`, caches it, and refreshes it before expiry. You do not need to manage tokens manually.

## Resources

### Banking

```python
# Balances
balances = client.banking.balances.list({"page_number": 1, "page_size": 20})
balance = client.banking.balances.retrieve("SGD")
txns = client.banking.balances.list_transactions({"page_number": 1, "page_size": 20})

# Transfers
transfer = client.banking.transfers.create({
    "source_account_id": "acc-123",
    "target_account_id": "acc-456",
    "currency": "SGD",
    "amount": "100.00",
    "reason": "Fund sub-account",
})
transfers = client.banking.transfers.list({"page_number": 1, "page_size": 20})
transfer = client.banking.transfers.retrieve("transfer-id")

# Deposits
deposits = client.banking.deposits.list({"page_number": 1, "page_size": 20})
deposit = client.banking.deposits.retrieve("deposit-id")

# Beneficiaries
beneficiary = client.banking.beneficiaries.create({...})
beneficiaries = client.banking.beneficiaries.list({"page_number": 1, "page_size": 20})
beneficiary = client.banking.beneficiaries.retrieve("ben-id")
client.banking.beneficiaries.update("ben-id", {})
client.banking.beneficiaries.delete("ben-id")
client.banking.beneficiaries.check({...})

# Payouts
payout = client.banking.payouts.create({
    "beneficiary_id": "ben-123",
    "currency": "SGD",
    "amount": "50.00",
    "purpose_code": "PERSONAL",
})
payouts = client.banking.payouts.list({"page_number": 1, "page_size": 20})
payout = client.banking.payouts.retrieve("payout-id")

# Virtual Accounts
va = client.banking.virtual_accounts.create({"currency": "USD"})
vas = client.banking.virtual_accounts.list({"page_number": 1, "page_size": 20})

# Conversions
quote = client.banking.conversions.create_quote({
    "buy_currency": "SGD",
    "sell_currency": "USD",
    "buy_amount": "100.00",
    "conversion_date": "2026-04-15",
})
conversion = client.banking.conversions.create({...})
rates = client.banking.conversions.list_current_rates()
dates = client.banking.conversions.list_dates({"currency_from": "USD", "currency_to": "SGD"})

# Payment Methods
methods = client.banking.payment_methods.list({"country": "US", "currency": "USD"})
```

### Issuing

#### Cardholders

```python
cardholder = client.issuing.cardholders.create({
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "phone_number": "+6591234567",
    "country_code": "SG",
    "date_of_birth": "1990-01-15",
})
cardholders = client.issuing.cardholders.list({"page_number": 1, "page_size": 20})
cardholder = client.issuing.cardholders.retrieve("ch-id")
client.issuing.cardholders.update("ch-id", {"first_name": "Updated"})
```

#### Cards

```python
card = client.issuing.cards.create({
    "cardholder_id": "ch-id",
    "product_id": "prod-id",
    "card_type": "VIRTUAL",
    "currency": "SGD",
})
cards = client.issuing.cards.list({"page_number": 1, "page_size": 20})
card = client.issuing.cards.retrieve("card-id")
client.issuing.cards.update("card-id", {"metadata": {"order_id": "ord-001"}})
client.issuing.cards.update_status("card-id", {"status": "FROZEN"})

# Recharge and withdraw
client.issuing.cards.recharge("card-id", {"amount": "100.00", "currency": "SGD"})
client.issuing.cards.withdraw("card-id", {"amount": "50.00", "currency": "SGD"})

# Secure card info
result = client.issuing.cards.create_pan_token("card-id")
result = client.issuing.cards.get_secure_iframe_url("card-id")

# Card orders
order = client.issuing.cards.retrieve_order("card-order-id")
```

#### Transactions, Products, Balances, Transfers

```python
# Transactions
txns = client.issuing.transactions.list({"page_number": 1, "page_size": 20})
txn = client.issuing.transactions.retrieve("txn-id")

# Products
products = client.issuing.products.list({"page_number": 1, "page_size": 20})

# Issuing balances
balances = client.issuing.balances.list({"page_number": 1, "page_size": 20})
balance = client.issuing.balances.retrieve("SGD")
client.issuing.balances.list_transactions({"page_number": 1, "page_size": 20})

# Issuing transfers
transfer = client.issuing.transfers.create({
    "source_account_id": "master-acc-id",
    "destination_account_id": "sub-acc-id",
    "currency": "SGD",
    "amount": 100,
})
transfer = client.issuing.transfers.retrieve("transfer-id")

# Reports
report = client.issuing.reports.create({
    "report_type": "SETTLEMENT",
    "start_time": "2026-01-01T00:00:00Z",
    "end_time": "2026-04-10T23:59:59Z",
})
csv_data = client.issuing.reports.download(report["report_id"])
```

### Connect

```python
# Accounts
accounts = client.connect.accounts.list({"page_number": 1, "page_size": 20})
account = client.connect.accounts.retrieve("acc-id")
account = client.connect.accounts.create({...})

# Sub-accounts
sub_account = client.connect.sub_accounts.create({...})

# Additional documents
docs = client.connect.additional_docs.get()
```

### Payment

```python
# Payment Intents
intent = client.payment.payment_intents.create({
    "amount": "100.00",
    "currency": "SGD",
    "merchant_order_id": "order-001",
    "return_url": "https://example.com/return",
})
client.payment.payment_intents.confirm(intent["payment_intent_id"], {"payment_method": {...}})
client.payment.payment_intents.capture("pi-id")
client.payment.payment_intents.cancel("pi-id", {"cancellation_reason": "requested_by_customer"})
intents = client.payment.payment_intents.list({"page_number": 1, "page_size": 20})

# Refunds
refund = client.payment.refunds.create({
    "payment_intent_id": "pi-id",
    "amount": "50.00",
    "reason": "requested_by_customer",
})
refunds = client.payment.refunds.list({"page_number": 1, "page_size": 20})
refund = client.payment.refunds.retrieve("refund-id")

# Bank Accounts
bank_account = client.payment.bank_accounts.create({...})
bank_accounts = client.payment.bank_accounts.list({"page_number": 1, "page_size": 20})

# Payouts
payout = client.payment.payouts.create({...})
payouts = client.payment.payouts.list({"page_number": 1, "page_size": 20})

# Balances and Attempts
balances = client.payment.balances.list({"page_number": 1, "page_size": 20})
balance = client.payment.balances.retrieve("SGD")
attempts = client.payment.attempts.list({"page_number": 1, "page_size": 20})
attempt = client.payment.attempts.retrieve("attempt-id")

# Settlements
settlements = client.payment.settlements.list({"page_number": 1, "page_size": 20})
```

### Supporting (File Upload / Download)

```python
with open("document.pdf", "rb") as f:
    result = client.supporting.files.upload(
        file_data=f.read(),
        filename="document.pdf",
        mime_type="application/pdf",
    )

links = client.supporting.files.download_links([result["file_id"]])
```

### Simulator (sandbox only)

The simulator is only available in the `sandbox` environment and raises `SimulatorNotAvailableError` in production.

```python
# Simulate a card authorization
result = client.simulator.issuing.authorize({
    "card_id": "card-id",
    "amount": 25.0,
    "currency": "SGD",
    "transaction_status": "APPROVED",
})

# Simulate a reversal
client.simulator.issuing.reverse({
    "card_id": "card-id",
    "transaction_id": result["transaction_id"],
})

# Simulate a deposit
client.simulator.deposits.simulate({
    "currency": "SGD",
    "amount": 500.0,
})
```

## Pagination

All list methods accept `page_number` and `page_size`:

```python
page = 1
while True:
    result = client.issuing.cards.list({"page_number": page, "page_size": 50})
    items = result.get("items") or result.get("list") or []
    if not items:
        break
    for card in items:
        print(card["card_id"])
    page += 1
```

## Webhooks

```python
client = UQPayClient(
    client_id="your-client-id",
    api_key="your-api-key",
    webhook_secret="your-webhook-secret",
)

# In your HTTP handler:
from uqpay import UQPayWebhookError

try:
    event = client.webhooks.construct_event(
        raw_body=request.get_data(),
        headers=dict(request.headers),
    )
    print(event["event_type"], event["data"])
except UQPayWebhookError as e:
    return str(e), 400
```

The verifier checks the HMAC-SHA256 signature and rejects requests with a timestamp older than 300 seconds.

## Authorization Decision (PGP)

Handle real-time card authorization decisions. UQPAY sends PGP-encrypted transactions to your endpoint; the SDK decrypts them, calls your handler, and returns an encrypted response.

```python
from uqpay.crypto import generate_auth_decision_key_pair

# Generate a key pair once and store securely
keys = generate_auth_decision_key_pair(name="MyApp", email="ops@example.com")

# Configure at startup
client.issuing.auth_decision.configure(
    private_key=keys["private_key"],
    uqpay_public_key="<UQPAY public key from dashboard>",
)

# Define your decision function
def decide(transaction: dict) -> dict:
    if transaction.get("amount", 0) > 10000:
        return {"response_code": "05"}  # Decline
    return {"response_code": "00", "partner_reference_id": "ref-001"}

# In your HTTP handler:
encrypted_response = client.issuing.auth_decision.handle(
    body=request.get_data(),
    headers=dict(request.headers),
    decide=decide,
)
```

## Error Handling

```python
from uqpay import (
    UQPayError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)

try:
    balance = client.banking.balances.retrieve("SGD")
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
except ForbiddenError as e:
    print(f"Access denied: {e.message}")
except NotFoundError as e:
    print(f"Not found: {e.message}")
except ValidationError as e:
    print(f"Validation error [{e.code}]: {e.message}")
except RateLimitError as e:
    print(f"Rate limited (HTTP {e.http_status})")
except ServerError as e:
    print(f"Server error: {e.message}")
except UQPayError as e:
    print(f"{e.type}: {e.message} (HTTP {e.http_status})")
```

All errors expose: `message`, `code`, `type`, `http_status`, `idempotency_key`.

## Configuration

```python
client = UQPayClient(
    client_id="your-client-id",
    api_key="your-api-key",
    environment="sandbox",       # "sandbox" (default) or "production"
    timeout=30.0,                # request timeout in seconds
    max_retries=2,               # automatic retries on transient errors
    log_level="none",            # "none" | "error" | "warn" | "info" | "debug"
    redact_fields=["card_number", "cvc"],
)
```

Per-request options:

```python
result = client.banking.payouts.create(
    {...},
    request_options={
        "idempotency_key": "unique-key",
        "on_behalf_of": "sub-account-id",
        "timeout": 60,
        "max_retries": 0,
    },
)
```

### Environment Variables

```
UQPAY_CLIENT_ID=your-client-id
UQPAY_API_KEY=your-api-key
```

## API Coverage

### Banking API

| Resource | Operations |
|----------|------------|
| **Balances** | List, Retrieve, ListTransactions |
| **Transfers** | Create, List, Retrieve |
| **Deposits** | List, Retrieve |
| **Beneficiaries** | Create, List, Retrieve, Update, Delete, Check |
| **Payouts** | Create, List, Retrieve |
| **Virtual Accounts** | Create, List |
| **Conversions** | CreateQuote, Create, List, Retrieve, ListDates, ListCurrentRates |
| **Payment Methods** | List |

### Issuing API

| Resource | Operations |
|----------|------------|
| **Cardholders** | Create, List, Retrieve, Update |
| **Cards** | Create, List, Retrieve, Update, UpdateStatus, Recharge, Withdraw, RetrieveOrder, CreatePanToken, GetSecureIframeUrl |
| **Transactions** | List, Retrieve |
| **Products** | List |
| **Balances** | List, Retrieve, ListTransactions |
| **Transfers** | Create, Retrieve |
| **Reports** | Create, Download |
| **Auth Decision** | PGP-based real-time authorization |

### Connect API

| Resource | Operations |
|----------|------------|
| **Accounts** | Create, List, Retrieve |
| **Sub-Accounts** | Create |
| **Additional Docs** | Get |

### Payment API

| Resource | Operations |
|----------|------------|
| **Payment Intents** | Create, Confirm, Capture, Cancel, List, Retrieve, Update |
| **Refunds** | Create, List, Retrieve |
| **Bank Accounts** | Create, List, Retrieve, Update |
| **Payouts** | Create, List, Retrieve |
| **Balances** | List, Retrieve |
| **Attempts** | List, Retrieve |
| **Settlements** | List |

### Supporting API

| Resource | Operations |
|----------|------------|
| **Files** | Upload, DownloadLinks |

### Simulator (sandbox only)

| Resource | Operations |
|----------|------------|
| **Issuing** | Authorize, Reverse |
| **Deposits** | Simulate |

## Testing

```bash
pip install -e ".[dev]"
cp .env.example .env  # fill in sandbox credentials
pytest tests/ -v

# Skip integration tests
SKIP_INTEGRATION_TESTS=true pytest tests/ -v
```

## Documentation

- [UQPAY API Reference](https://developer.uqpay.com/api/#/)

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

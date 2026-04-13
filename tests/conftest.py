from __future__ import annotations
import os
import time
import pytest
from dotenv import load_dotenv
from uqpay import UQPayClient

load_dotenv()


def _first_id(result: dict) -> str | None:
    """Extract the ID from a list response's first item, trying all known ID field names."""
    ID_FIELDS = ("id", "cardholder_id", "card_id", "beneficiary_id", "payment_intent_id",
                 "product_id", "bank_account_id", "payout_id", "refund_id", "transfer_id",
                 "conversion_id", "deposit_id", "transaction_id", "account_id", "virtual_account_id",
                 "settlement_id", "attempt_id", "report_id")
    for key in ("items", "list", "data"):
        val = result.get(key)
        if isinstance(val, list) and val:
            item = val[0]
            for field in ID_FIELDS:
                if item.get(field):
                    return item[field]
        if isinstance(val, dict):
            for k2 in ("items", "list"):
                items = val.get(k2)
                if isinstance(items, list) and items:
                    item = items[0]
                    for field in ID_FIELDS:
                        if item.get(field):
                            return item[field]
    return None


def _entity_id(result: dict) -> str | None:
    """Extract ID from a create/retrieve response, trying all known ID field names."""
    ID_FIELDS = ("id", "cardholder_id", "card_id", "beneficiary_id", "payment_intent_id",
                 "product_id", "bank_account_id", "payout_id", "refund_id", "transfer_id",
                 "conversion_id", "deposit_id", "transaction_id", "account_id", "virtual_account_id",
                 "settlement_id", "attempt_id", "report_id")
    for field in ID_FIELDS:
        if result.get(field):
            return result[field]
    data = result.get("data")
    if isinstance(data, dict):
        for field in ID_FIELDS:
            if data.get(field):
                return data[field]
    return None


@pytest.fixture(scope="session")
def client() -> UQPayClient:
    skip = os.getenv("SKIP_INTEGRATION_TESTS", "").lower() == "true"
    client_id = os.getenv("UQPAY_CLIENT_ID", "")
    api_key = os.getenv("UQPAY_API_KEY", "")
    if skip or not client_id or not api_key:
        pytest.skip("Set UQPAY_CLIENT_ID and UQPAY_API_KEY to run integration tests")
    c = UQPayClient(client_id=client_id, api_key=api_key, environment="sandbox")
    yield c
    c.close()


@pytest.fixture(scope="session")
def simulator_card_id() -> str:
    return os.getenv("UQPAY_SIMULATOR_CARD_ID", "e91b8362-7e80-4606-b4a5-93ea8639b40e")


@pytest.fixture(scope="session")
def card_product_id(client: UQPayClient) -> str:
    result = client.issuing.products.list({"page_number": 1, "page_size": 10})
    items = result.get("data") or result.get("items") or result.get("list") or []
    if isinstance(items, dict):
        items = items.get("items") or items.get("list") or []
    if not items:
        pytest.skip("No card products available in sandbox")
    # Products use 'product_id' not 'id'
    return items[0].get("product_id") or items[0].get("id")


@pytest.fixture(scope="session")
def cardholder(client: UQPayClient) -> dict:
    ts = int(time.time())
    # SG phone numbers: 8 digits, starting with 8 or 9
    # Use seconds-based suffix that fits in 8 digits starting with 9
    phone = f"9{ts % 10000000:07d}"
    result = client.issuing.cardholders.create({
        "email": f"sdk-test-{ts}@example.com",
        "phone_number": phone,
        "first_name": "SDK",
        "last_name": "Test",
        "country_code": "SG",
    })
    assert isinstance(result, dict)
    return result


@pytest.fixture(scope="session")
def card(client: UQPayClient, cardholder: dict, card_product_id: str) -> dict:
    ch_id = _entity_id(cardholder)
    if not ch_id:
        pytest.skip("Could not determine cardholder ID from create response")
    result = client.issuing.cards.create({
        "card_currency": "SGD",
        "cardholder_id": ch_id,
        "card_product_id": card_product_id,
    })
    assert isinstance(result, dict)
    return result


@pytest.fixture(scope="session")
def beneficiary(client: UQPayClient) -> dict:
    ts = int(time.time())
    result = client.banking.beneficiaries.create({
        "entity_type": "INDIVIDUAL",
        "first_name": "SDK",
        "last_name": "Test",
        "currency": "USD",
        "country": "US",
        "payment_method": "LOCAL",
        "bank_details": {
            "account_number": f"99{ts % 100000000:08d}",
            "account_holder": "SDK Test",
            "account_currency_code": "USD",
            "bank_name": "JPMorgan Chase",
            "bank_address": "383 Madison Avenue, New York, NY 10179",
            "bank_country_code": "US",
            "swift_code": "CHASUS33",
            "clearing_system": "ACH",
            "routing_code_type1": "ach",
            "routing_code_value1": "021000021",
        },
        "address": {
            "street_address": "100 Test Street",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US",
        },
    })
    assert isinstance(result, dict)
    return result


@pytest.fixture(scope="session")
def virtual_account(client: UQPayClient) -> dict:
    """Return the first available virtual account, or create one."""
    try:
        result = client.banking.virtual_accounts.list({"page_number": 1, "page_size": 10})
        for key in ("items", "list", "data"):
            val = result.get(key)
            if isinstance(val, list) and val:
                return val[0]
            if isinstance(val, dict):
                for k2 in ("items", "list"):
                    items = val.get(k2)
                    if isinstance(items, list) and items:
                        return items[0]
    except Exception:
        pass
    try:
        return client.banking.virtual_accounts.create({"currency": "USD"})
    except Exception:
        return {}


@pytest.fixture(scope="session")
def payment_intent(client: UQPayClient) -> dict:
    ts = int(time.time() * 1000)
    result = client.payment.payment_intents.create({
        "amount": "103.00",
        "currency": "USD",
        "merchant_order_id": f"sdk-{ts}",
        "description": "SDK integration test",
        "return_url": "https://example.com/return",
    })
    assert isinstance(result, dict)
    return result

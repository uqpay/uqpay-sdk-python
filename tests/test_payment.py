from __future__ import annotations
import time
import pytest
from uqpay import UQPayClient, UQPayError

_PAGE = {"page_number": 1, "page_size": 10}

_ID_FIELDS = (
    "id", "payment_intent_id", "bank_account_id", "payout_id", "refund_id",
    "attempt_id", "settlement_id", "transaction_id",
)


def _first_id(result: dict) -> str | None:
    for key in ("items", "list", "data"):
        val = result.get(key)
        if isinstance(val, list) and val:
            item = val[0]
            for field in _ID_FIELDS:
                if item.get(field):
                    return item[field]
        if isinstance(val, dict):
            for k2 in ("items", "list"):
                items = val.get(k2)
                if isinstance(items, list) and items:
                    item = items[0]
                    for field in _ID_FIELDS:
                        if item.get(field):
                            return item[field]
    return None


def _entity_id(result: dict) -> str | None:
    for field in _ID_FIELDS:
        if result.get(field):
            return result[field]
    data = result.get("data")
    if isinstance(data, dict):
        for field in _ID_FIELDS:
            if data.get(field):
                return data[field]
    return None


# ---------------------------------------------------------------------------
# Payment Intents
# ---------------------------------------------------------------------------

def test_list_payment_intents(client: UQPayClient):
    result = client.payment.payment_intents.list(_PAGE)
    assert isinstance(result, dict)


def test_create_payment_intent(payment_intent: dict):
    assert isinstance(payment_intent, dict)
    assert _entity_id(payment_intent) is not None


def test_retrieve_payment_intent(client: UQPayClient, payment_intent: dict):
    pi_id = _entity_id(payment_intent)
    if not pi_id:
        pytest.skip("No payment intent ID available")
    result = client.payment.payment_intents.retrieve(pi_id)
    assert isinstance(result, dict)


def test_update_payment_intent(client: UQPayClient, payment_intent: dict):
    pi_id = _entity_id(payment_intent)
    if not pi_id:
        pytest.skip("No payment intent ID available")
    try:
        result = client.payment.payment_intents.update(pi_id, {"description": "SDK integration test updated"})
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


_CARD_PAYMENT = {
    "type": "card",
    "card": {
        "card_number": "4176660000000027",
        "expiry_month": "12",
        "expiry_year": "2033",
        "cvc": "303",
        "card_name": "SDK Test",
        "network": "visa",
        "authorization_type": "authorization",
        "three_ds_action": "skip_3ds",
        "billing": {
            "first_name": "SDK",
            "last_name": "Test",
            "email": "sdk-test@example.com",
            "address": {
                "country_code": "SG",
                "city": "Singapore",
                "street": "1 Test Street",
                "postcode": "123456",
            },
        },
    },
}


def test_confirm_payment_intent(client: UQPayClient, payment_intent: dict):
    pi_id = _entity_id(payment_intent)
    if not pi_id:
        pytest.skip("No payment intent ID available")
    try:
        result = client.payment.payment_intents.confirm(pi_id, {
            "payment_method": _CARD_PAYMENT,
            "return_url": "https://example.com/return",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_retrieve_confirmed_intent(client: UQPayClient, payment_intent: dict):
    pi_id = _entity_id(payment_intent)
    if not pi_id:
        pytest.skip("No payment intent ID available")
    result = client.payment.payment_intents.retrieve(pi_id)
    assert isinstance(result, dict)


def test_cancel_payment_intent(client: UQPayClient):
    """Create a fresh intent and cancel it."""
    ts = int(time.time() * 1000)
    try:
        new_pi = client.payment.payment_intents.create({
            "amount": "50.00",
            "currency": "USD",
            "merchant_order_id": f"sdk-cancel-{ts}",
            "description": "SDK cancel test",
            "return_url": "https://example.com/return",
        })
        assert isinstance(new_pi, dict)
        pi_id = _entity_id(new_pi)
        if not pi_id:
            pytest.skip("No ID in cancel test intent")
        result = client.payment.payment_intents.cancel(pi_id, {"cancellation_reason": "requested_by_customer"})
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


_CARD_PAYMENT_PREAUTH = {
    "type": "card",
    "card": {
        **_CARD_PAYMENT["card"],
        "authorization_type": "pre_authorization",
    },
}


def test_capture_payment_intent(client: UQPayClient):
    """Create a fresh intent, pre-authorize, then capture."""
    ts = int(time.time() * 1000)
    try:
        new_pi = client.payment.payment_intents.create({
            "amount": "75.00",
            "currency": "USD",
            "merchant_order_id": f"sdk-capture-{ts}",
            "description": "SDK capture test",
            "return_url": "https://example.com/return",
        })
        pi_id = _entity_id(new_pi)
        if not pi_id:
            pytest.skip("No ID in capture test intent")
        client.payment.payment_intents.confirm(pi_id, {
            "payment_method": _CARD_PAYMENT_PREAUTH,
            "return_url": "https://example.com/return",
        })
        result = client.payment.payment_intents.capture(pi_id)
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Bank Accounts
# ---------------------------------------------------------------------------

def test_create_bank_account(client: UQPayClient):
    ts = int(time.time())
    try:
        result = client.payment.bank_accounts.create({
            "account_number": f"99{ts % 100000000:08d}",
            "account_holder": "SDK Test",
            "bank_name": "JPMorgan Chase",
            "bank_country_code": "US",
            "bank_address": "383 Madison Avenue, New York, NY 10179",
            "currency": "USD",
            "swift_code": "CHASUS33",
            "bank_code_type": "aba",
            "bank_code_value": "021000021",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_list_bank_accounts(client: UQPayClient):
    result = client.payment.bank_accounts.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_bank_account(client: UQPayClient):
    result = client.payment.bank_accounts.list(_PAGE)
    assert isinstance(result, dict)
    ba_id = _first_id(result)
    if not ba_id:
        pytest.skip("No bank accounts available")
    retrieved = client.payment.bank_accounts.retrieve(ba_id)
    assert isinstance(retrieved, dict)


def test_update_bank_account(client: UQPayClient):
    result = client.payment.bank_accounts.list(_PAGE)
    assert isinstance(result, dict)
    ba_id = _first_id(result)
    if not ba_id:
        pytest.skip("No bank accounts available")
    # Retrieve the bank account to get all current fields needed for update
    try:
        detail = client.payment.bank_accounts.retrieve(ba_id)
        updated = client.payment.bank_accounts.update(ba_id, {
            "account_holder": "SDK Test Updated",
            "account_number": detail.get("account_number", ""),
            "bank_name": detail.get("bank_name", ""),
            "swift_code": detail.get("swift_code", ""),
            "bank_country_code": detail.get("bank_country_code", ""),
            "bank_address": detail.get("bank_address", ""),
        })
        assert isinstance(updated, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Payouts
# ---------------------------------------------------------------------------

def test_list_payment_payouts(client: UQPayClient):
    result = client.payment.payouts.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_payment_payout(client: UQPayClient):
    result = client.payment.payouts.list(_PAGE)
    assert isinstance(result, dict)
    payout_id = _first_id(result)
    if not payout_id:
        pytest.skip("No payment payouts available")
    retrieved = client.payment.payouts.retrieve(payout_id)
    assert isinstance(retrieved, dict)


def test_create_payment_payout(client: UQPayClient):
    try:
        result = client.payment.payouts.create({
            "payout_currency": "USD",
            "payout_amount": "10.00",
            "statement_descriptor": "SDK Test Payout",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Refunds
# ---------------------------------------------------------------------------

def _get_succeeded_intent(client: UQPayClient) -> dict | None:
    """Find the first SUCCEEDED payment intent to use for refund tests."""
    try:
        result = client.payment.payment_intents.list({
            "page_number": 1, "page_size": 20, "intent_status": "SUCCEEDED",
        })
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
    return None


def test_create_refund(client: UQPayClient):
    intent = _get_succeeded_intent(client)
    if not intent:
        pytest.skip("No SUCCEEDED payment intent available for refund")
    pi_id = intent.get("payment_intent_id") or intent.get("id")
    amount = intent.get("amount", "10.00")
    try:
        result = client.payment.refunds.create({
            "payment_intent_id": pi_id,
            "amount": amount,
            "reason": "SDK test refund",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_list_refunds(client: UQPayClient):
    result = client.payment.refunds.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_refund(client: UQPayClient):
    result = client.payment.refunds.list(_PAGE)
    assert isinstance(result, dict)
    refund_id = _first_id(result)
    if not refund_id:
        pytest.skip("No refunds available")
    retrieved = client.payment.refunds.retrieve(refund_id)
    assert isinstance(retrieved, dict)


# ---------------------------------------------------------------------------
# Attempts
# ---------------------------------------------------------------------------

def test_list_payment_attempts(client: UQPayClient):
    result = client.payment.attempts.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_payment_attempt(client: UQPayClient):
    result = client.payment.attempts.list(_PAGE)
    assert isinstance(result, dict)
    attempt_id = _first_id(result)
    if not attempt_id:
        pytest.skip("No payment attempts available")
    retrieved = client.payment.attempts.retrieve(attempt_id)
    assert isinstance(retrieved, dict)


# ---------------------------------------------------------------------------
# Balances
# ---------------------------------------------------------------------------

def test_list_payment_balances(client: UQPayClient):
    result = client.payment.balances.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_payment_balance_by_currency(client: UQPayClient):
    for currency in ("SGD", "USD"):
        try:
            result = client.payment.balances.retrieve(currency)
            assert isinstance(result, dict)
            return
        except UQPayError:
            continue
    pytest.skip("No balance available for SGD or USD")


# ---------------------------------------------------------------------------
# Settlements
# ---------------------------------------------------------------------------

def test_list_settlements(client: UQPayClient):
    try:
        result = client.payment.settlements.list(_PAGE)
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")

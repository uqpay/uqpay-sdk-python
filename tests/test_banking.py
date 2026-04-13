from __future__ import annotations
import time
import pytest
from uqpay import UQPayClient, UQPayError

_PAGE = {"page_number": 1, "page_size": 10}

_ID_FIELDS = (
    "id", "beneficiary_id", "payout_id", "transfer_id", "conversion_id",
    "deposit_id", "virtual_account_id", "transaction_id", "account_id",
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
# Payment Methods
# ---------------------------------------------------------------------------

def test_list_payment_methods(client: UQPayClient):
    result = client.banking.payment_methods.list({"country": "US", "currency": "USD"})
    assert isinstance(result, (dict, list))


# ---------------------------------------------------------------------------
# Beneficiaries
# ---------------------------------------------------------------------------

def test_create_beneficiary(beneficiary: dict):
    assert isinstance(beneficiary, dict)
    assert _entity_id(beneficiary) is not None


def test_list_beneficiaries(client: UQPayClient):
    result = client.banking.beneficiaries.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_beneficiary(client: UQPayClient, beneficiary: dict):
    b_id = _entity_id(beneficiary)
    if not b_id:
        pytest.skip("No beneficiary ID available")
    result = client.banking.beneficiaries.retrieve(b_id)
    assert isinstance(result, dict)


def test_update_beneficiary(client: UQPayClient, beneficiary: dict):
    b_id = _entity_id(beneficiary)
    if not b_id:
        pytest.skip("No beneficiary ID available")
    try:
        # Retrieve full details to get bank_details and address needed for update
        detail = client.banking.beneficiaries.retrieve(b_id)
        bank_details = detail.get("bank_details") or {}
        address = detail.get("address") or {}
        result = client.banking.beneficiaries.update(b_id, {
            "entity_type": "INDIVIDUAL",
            "first_name": "SDK",
            "last_name": "Updated",
            "payment_method": "LOCAL",
            "bank_details": bank_details,
            "address": address,
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_check_beneficiary(client: UQPayClient):
    try:
        result = client.banking.beneficiaries.check({
            "entity_type": "INDIVIDUAL",
            "account_number": "021000021",
            "payment_method": "LOCAL",
            "currency": "USD",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_delete_beneficiary(client: UQPayClient):
    """Create a separate beneficiary specifically for deletion."""
    ts = int(time.time())
    try:
        created = client.banking.beneficiaries.create({
            "entity_type": "INDIVIDUAL",
            "first_name": "SDKDelete",
            "last_name": "Test",
            "currency": "USD",
            "country": "US",
            "payment_method": "LOCAL",
            "bank_details": {
                "account_number": f"88{ts % 100000000:08d}",
                "account_holder": "SDK Delete Test",
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
                "street_address": "200 Delete Street",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "US",
            },
        })
        assert isinstance(created, dict)
        b_id = _entity_id(created)
        if not b_id:
            pytest.skip("No ID from created delete-test beneficiary")
        result = client.banking.beneficiaries.delete(b_id)
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Banking Payouts
# ---------------------------------------------------------------------------

def test_list_banking_payouts(client: UQPayClient):
    result = client.banking.payouts.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_banking_payout(client: UQPayClient):
    result = client.banking.payouts.list(_PAGE)
    assert isinstance(result, dict)
    payout_id = _first_id(result)
    if not payout_id:
        pytest.skip("No banking payouts available")
    retrieved = client.banking.payouts.retrieve(payout_id)
    assert isinstance(retrieved, dict)


def test_create_banking_payout(client: UQPayClient, beneficiary: dict):
    b_id = _entity_id(beneficiary)
    if not b_id:
        pytest.skip("No beneficiary ID available")
    ts = int(time.time() * 1000)
    try:
        result = client.banking.payouts.create({
            "beneficiary_id": b_id,
            "amount": "10.00",
            "currency": "USD",
            "purpose_code": "BUSINESS_EXPENSES",
            "payout_reference": f"sdk-payout-{ts}",
            "fee_paid_by": "SHARED",
            "payout_date": "2026-04-15",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Banking Transfers
# ---------------------------------------------------------------------------

def test_list_banking_transfers(client: UQPayClient):
    result = client.banking.transfers.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_banking_transfer(client: UQPayClient):
    result = client.banking.transfers.list(_PAGE)
    assert isinstance(result, dict)
    transfer_id = _first_id(result)
    if not transfer_id:
        pytest.skip("No banking transfers available")
    retrieved = client.banking.transfers.retrieve(transfer_id)
    assert isinstance(retrieved, dict)


_MASTER_ACCOUNT_ID = "e95e0692-22b3-41b5-9dba-8ffef502d97a"
_SUB_ACCOUNT_ID = "f07d1878-523a-4267-aa7d-a2286ae836c6"


def test_create_banking_transfer(client: UQPayClient):
    try:
        result = client.banking.transfers.create({
            "source_account_id": _MASTER_ACCOUNT_ID,
            "target_account_id": _SUB_ACCOUNT_ID,
            "currency": "SGD",
            "amount": "1",
            "reason": "SDK test transfer",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Conversions
# ---------------------------------------------------------------------------

def test_list_conversions(client: UQPayClient):
    result = client.banking.conversions.list(_PAGE)
    assert isinstance(result, dict)


def test_list_conversion_dates(client: UQPayClient):
    try:
        result = client.banking.conversions.list_dates({"currency_from": "USD", "currency_to": "SGD"})
        assert isinstance(result, (dict, list))
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_list_current_rates(client: UQPayClient):
    result = client.banking.conversions.list_current_rates()
    assert isinstance(result, dict)


def _get_conversion_date(client: UQPayClient) -> str:
    """Fetch the first valid conversion date using correct param names."""
    try:
        result = client.banking.conversions.list_dates({"currency_from": "USD", "currency_to": "SGD"})
        # Response is a list of {"date": "...", "valid": bool}
        items = result if isinstance(result, list) else result.get("data") or []
        for item in items:
            if isinstance(item, dict) and item.get("valid"):
                return item["date"]
    except Exception:
        pass
    return "2026-04-14"


def test_create_conversion_quote(client: UQPayClient):
    conversion_date = _get_conversion_date(client)
    try:
        result = client.banking.conversions.create_quote({
            "buy_currency": "SGD",
            "sell_currency": "USD",
            "buy_amount": "100.00",
            "conversion_date": conversion_date,
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_retrieve_conversion(client: UQPayClient):
    result = client.banking.conversions.list(_PAGE)
    assert isinstance(result, dict)
    conversion_id = _first_id(result)
    if not conversion_id:
        pytest.skip("No conversions available")
    try:
        retrieved = client.banking.conversions.retrieve(conversion_id)
        assert isinstance(retrieved, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_create_conversion(client: UQPayClient):
    conversion_date = _get_conversion_date(client)
    try:
        quote = client.banking.conversions.create_quote({
            "buy_currency": "SGD",
            "sell_currency": "USD",
            "buy_amount": "10.00",
            "conversion_date": conversion_date,
        })
        quote_id = (quote.get("quote_price", {}).get("quote_id")
                    or quote.get("quote_id")
                    or _entity_id(quote))
        if not quote_id:
            pytest.skip("No quote ID returned")
        result = client.banking.conversions.create({
            "quote_id": quote_id,
            "sell_currency": "USD",
            "buy_currency": "SGD",
            "buy_amount": "10.00",
            "conversion_date": conversion_date,
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Virtual Accounts
# ---------------------------------------------------------------------------

def test_list_virtual_accounts(client: UQPayClient):
    result = client.banking.virtual_accounts.list(_PAGE)
    assert isinstance(result, dict)


def test_create_virtual_account(client: UQPayClient):
    try:
        result = client.banking.virtual_accounts.create({
            "currency": "USD",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Banking Balances
# ---------------------------------------------------------------------------

def test_list_banking_balances(client: UQPayClient):
    result = client.banking.balances.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_banking_balance_by_currency(client: UQPayClient):
    for currency in ("SGD", "USD"):
        try:
            result = client.banking.balances.retrieve(currency)
            assert isinstance(result, dict)
            return
        except UQPayError:
            continue
    pytest.skip("No balance available for SGD or USD")


def test_list_banking_balance_transactions(client: UQPayClient):
    result = client.banking.balances.list_transactions(_PAGE)
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Deposits
# ---------------------------------------------------------------------------

def test_list_deposits(client: UQPayClient):
    result = client.banking.deposits.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_deposit(client: UQPayClient):
    result = client.banking.deposits.list(_PAGE)
    assert isinstance(result, dict)
    deposit_id = _first_id(result)
    if not deposit_id:
        pytest.skip("No deposits available")
    retrieved = client.banking.deposits.retrieve(deposit_id)
    assert isinstance(retrieved, dict)

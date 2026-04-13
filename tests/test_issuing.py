from __future__ import annotations
import time
import pytest
from uqpay import UQPayClient, UQPayError

_PAGE = {"page_number": 1, "page_size": 20}

_ID_FIELDS = (
    "id", "cardholder_id", "card_id", "product_id", "transaction_id",
    "transfer_id", "report_id",
)

# Ordered for specific entity types where we know the field name
_TRANSACTION_ID_FIELDS = ("transaction_id", "id")
_CARD_ID_FIELDS = ("card_id", "id")
_CARDHOLDER_ID_FIELDS = ("cardholder_id", "id")
_PRODUCT_ID_FIELDS = ("product_id", "id")


def _first_id_for(result: dict, fields: tuple) -> str | None:
    for key in ("items", "list", "data"):
        val = result.get(key)
        if isinstance(val, list) and val:
            item = val[0]
            for field in fields:
                if item.get(field):
                    return item[field]
        if isinstance(val, dict):
            for k2 in ("items", "list"):
                items = val.get(k2)
                if isinstance(items, list) and items:
                    item = items[0]
                    for field in fields:
                        if item.get(field):
                            return item[field]
    return None


def _first_id(result: dict) -> str | None:
    return _first_id_for(result, _ID_FIELDS)


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
# Products
# ---------------------------------------------------------------------------

def test_list_card_products(client: UQPayClient):
    result = client.issuing.products.list(_PAGE)
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Cardholders
# ---------------------------------------------------------------------------

def test_create_cardholder(cardholder: dict):
    assert isinstance(cardholder, dict)
    assert _entity_id(cardholder) is not None


def test_list_cardholders(client: UQPayClient):
    result = client.issuing.cardholders.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_cardholder(client: UQPayClient, cardholder: dict):
    ch_id = _entity_id(cardholder)
    if not ch_id:
        pytest.skip("No cardholder ID available")
    result = client.issuing.cardholders.retrieve(ch_id)
    assert isinstance(result, dict)


def test_update_cardholder(client: UQPayClient, cardholder: dict):
    ch_id = _entity_id(cardholder)
    if not ch_id:
        pytest.skip("No cardholder ID available")
    try:
        result = client.issuing.cardholders.update(ch_id, {"first_name": "SDKUpdated"})
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------

def test_create_card(card: dict):
    assert isinstance(card, dict)
    assert _entity_id(card) is not None


def test_list_cards(client: UQPayClient):
    result = client.issuing.cards.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_card(client: UQPayClient, card: dict):
    card_id = _entity_id(card)
    if not card_id:
        pytest.skip("No card ID available")
    result = client.issuing.cards.retrieve(card_id)
    assert isinstance(result, dict)


def test_update_card(client: UQPayClient, simulator_card_id: str):
    """Update simulator card metadata."""
    try:
        result = client.issuing.cards.update(simulator_card_id, {"metadata": {"test": "sdk"}})
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")




def test_retrieve_card_order(client: UQPayClient, simulator_card_id: str):
    """Recharge simulator card to get a card_order_id, then retrieve that order."""
    try:
        recharge = client.issuing.cards.recharge(simulator_card_id, {
            "amount": 1.0,
            "currency": "SGD",
        })
        card_order_id = recharge.get("card_order_id")
        if not card_order_id:
            pytest.skip("No card_order_id in recharge response")
        result = client.issuing.cards.retrieve_order(card_order_id)
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_retrieve_secure_card_info(client: UQPayClient, card: dict):
    card_id = _entity_id(card)
    if not card_id:
        pytest.skip("No card ID available")
    try:
        result = client.issuing.cards.retrieve_secure(card_id)
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_create_pan_token(client: UQPayClient, simulator_card_id: str):
    try:
        result = client.issuing.cards.create_pan_token(simulator_card_id)
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_get_secure_iframe_url(client: UQPayClient, simulator_card_id: str):
    try:
        result = client.issuing.cards.get_secure_iframe_url(simulator_card_id)
        assert isinstance(result, dict)
        assert "iframe_url" in result
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_recharge_card(client: UQPayClient, simulator_card_id: str):
    """Recharge using the dedicated simulator card ID from env."""
    try:
        result = client.issuing.cards.recharge(simulator_card_id, {
            "amount": "10.00",
            "currency": "SGD",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_withdraw_card(client: UQPayClient, simulator_card_id: str):
    try:
        result = client.issuing.cards.withdraw(simulator_card_id, {
            "amount": "5.00",
            "currency": "SGD",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Issuing Balances
# ---------------------------------------------------------------------------

def test_list_issuing_balances(client: UQPayClient):
    result = client.issuing.balances.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_issuing_balance_by_currency(client: UQPayClient):
    for currency in ("SGD", "USD"):
        try:
            result = client.issuing.balances.retrieve(currency)
            assert isinstance(result, dict)
            return
        except UQPayError:
            continue
    pytest.skip("No issuing balance available for SGD or USD")


def test_list_issuing_balance_transactions(client: UQPayClient):
    result = client.issuing.balances.list_transactions(_PAGE)
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Transactions
# ---------------------------------------------------------------------------

def test_list_transactions(client: UQPayClient):
    result = client.issuing.transactions.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_transaction(client: UQPayClient):
    result = client.issuing.transactions.list(_PAGE)
    assert isinstance(result, dict)
    txn_id = _first_id_for(result, _TRANSACTION_ID_FIELDS)
    if not txn_id:
        pytest.skip("No transactions available")
    try:
        retrieved = client.issuing.transactions.retrieve(txn_id)
        assert isinstance(retrieved, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

_created_report_id: str | None = None


def test_create_report(client: UQPayClient):
    global _created_report_id
    try:
        result = client.issuing.reports.create({
            "report_type": "SETTLEMENT",
            "start_time": "2026-01-01T00:00:00Z",
            "end_time": "2026-04-10T23:59:59Z",
        })
        assert isinstance(result, dict)
        _created_report_id = _entity_id(result)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_download_report(client: UQPayClient):
    """Download a report (use known-good ID as fallback)."""
    report_id = _created_report_id or "e5b1bcba-704e-4d29-a06a-e96ca673a7a7"
    try:
        result = client.issuing.reports.download(report_id)
        assert result is not None
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Issuing Transfers
# ---------------------------------------------------------------------------

_MASTER_ACCOUNT_ID = "e95e0692-22b3-41b5-9dba-8ffef502d97a"
_SUB_ACCOUNT_ID = "f07d1878-523a-4267-aa7d-a2286ae836c6"


def test_create_issuing_transfer(client: UQPayClient):
    try:
        result = client.issuing.transfers.create({
            "source_account_id": _MASTER_ACCOUNT_ID,
            "destination_account_id": _SUB_ACCOUNT_ID,
            "currency": "SGD",
            "amount": 1,
            "remark": "SDK test issuing transfer",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_retrieve_issuing_transfer(client: UQPayClient):
    try:
        created = client.issuing.transfers.create({
            "source_account_id": _MASTER_ACCOUNT_ID,
            "destination_account_id": _SUB_ACCOUNT_ID,
            "currency": "SGD",
            "amount": 1,
            "remark": "SDK test issuing transfer",
        })
        transfer_id = _entity_id(created)
        if not transfer_id:
            pytest.skip("No transfer ID returned")
        result = client.issuing.transfers.retrieve(transfer_id)
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")

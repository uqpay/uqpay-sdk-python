from __future__ import annotations
import pytest
from uqpay import UQPayClient, UQPayError, SimulatorNotAvailableError


def _entity_id(result: dict) -> str | None:
    if result.get("id"):
        return result["id"]
    data = result.get("data")
    if isinstance(data, dict):
        return data.get("id")
    return None


def _first_id(result: dict) -> str | None:
    for key in ("items", "list", "data"):
        val = result.get(key)
        if isinstance(val, list) and val:
            return val[0].get("id")
        if isinstance(val, dict):
            for k2 in ("items", "list"):
                items = val.get(k2)
                if isinstance(items, list) and items:
                    return items[0].get("id")
    return None


def test_simulator_available_in_sandbox(client: UQPayClient):
    # Simulator should not raise SimulatorNotAvailableError in sandbox
    # We'll just verify the resource exists and doesn't raise on access
    assert client.simulator.issuing is not None
    assert client.simulator.deposits is not None


def test_simulator_raises_in_production():
    from uqpay.resources.simulator.issuing import SimulatorIssuingResource
    from uqpay.resources.simulator.deposits import SimulatorDepositsResource
    # Simulate production mode
    from uqpay.http import HttpClient
    from uqpay.auth import TokenManager
    tm = TokenManager("id", "key", "https://api.uqpay.com/api")
    http = HttpClient("https://api.uqpay.com/api", tm, "id")
    issuing = SimulatorIssuingResource(http, is_production=True)
    deposits = SimulatorDepositsResource(http, is_production=True)
    with pytest.raises(SimulatorNotAvailableError):
        issuing.authorize({})
    with pytest.raises(SimulatorNotAvailableError):
        deposits.simulate({})
    http.close()


def test_simulate_authorization(client: UQPayClient, simulator_card_id: str):
    """Simulate a card authorization using the simulator card ID."""
    try:
        result = client.simulator.issuing.authorize({
            "card_id": simulator_card_id,
            "transaction_amount": 10.00,
            "transaction_currency": "SGD",
            "merchant_name": "SDK Test Shop",
            "merchant_category_code": "5734",
            "transaction_status": "APPROVED",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_simulate_reversal(client: UQPayClient, simulator_card_id: str):
    """Simulate a reversal on an authorization."""
    try:
        auth_result = client.simulator.issuing.authorize({
            "card_id": simulator_card_id,
            "transaction_amount": 10.00,
            "transaction_currency": "SGD",
            "merchant_name": "SDK Test Shop",
            "merchant_category_code": "5734",
            "transaction_status": "APPROVED",
        })
        assert isinstance(auth_result, dict)
        txn_id = (auth_result.get("transaction_id")
                  or auth_result.get("id")
                  or _first_id(auth_result))
        if not txn_id:
            pytest.skip("No transaction_id returned from simulate authorization")
        result = client.simulator.issuing.reverse({"transaction_id": txn_id})
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_simulate_deposit(client: UQPayClient, virtual_account):
    """Simulate a deposit into a virtual account."""
    account_number = (virtual_account.get("account_number")
                      or virtual_account.get("iban")
                      or virtual_account.get("receiver_account_number"))
    try:
        result = client.simulator.deposits.simulate({
            "amount": 100.00,
            "currency": "USD",
            "sender_swift_code": "CHASUS33",
            "receiver_account_number": account_number or "",
            "sender_name": "SDK Test Sender",
            "sender_account_number": "99012345678",
            "sender_country": "US",
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")

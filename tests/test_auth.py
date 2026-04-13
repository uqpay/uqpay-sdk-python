from __future__ import annotations
from uqpay import UQPayClient, AuthenticationError
import pytest


def test_invalid_credentials_raise_auth_error():
    client = UQPayClient(client_id="bad", api_key="bad", environment="sandbox")
    with pytest.raises(AuthenticationError):
        # Force token fetch
        client._token_manager.get_token()
    client.close()


def test_account_context_populated_after_first_call(client: UQPayClient):
    # Trigger token fetch by making a lightweight call
    client.banking.balances.list({"page_number": 1, "page_size": 10})
    assert client.account_id is not None
    assert client.short_account_id is not None

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import Mock

import httpx
import pytest

from uqpay import AuthenticationError, UQPayClient
from uqpay.auth import TokenManager


def test_invalid_credentials_raise_auth_error(monkeypatch):
    post = Mock(return_value=httpx.Response(401, json={"error": "Invalid API key"}))
    monkeypatch.setattr("uqpay.auth.httpx.post", post)
    manager = TokenManager("bad", "bad", "https://auth.example.test/api")
    with pytest.raises(AuthenticationError, match="Invalid API key") as error:
        manager.get_token()
    assert error.value.http_status == 401
    post.assert_called_once_with(
        "https://auth.example.test/api/v1/connect/token",
        headers={"x-client-id": "bad", "x-api-key": "bad", "Content-Type": "application/json"},
        timeout=30.0,
    )


def test_cached_token_refreshes_at_expiry_buffer_and_after_invalidation(monkeypatch):
    clock = [1000]
    monkeypatch.setattr("uqpay.auth.time.time", lambda: clock[0])
    post = Mock(side_effect=[
        httpx.Response(200, json={"auth_token": "first", "expired_at": 1100}),
        httpx.Response(200, json={"auth_token": "second", "expired_at": 2000}),
        httpx.Response(200, json={"auth_token": "third", "expired_at": 2000}),
    ])
    monkeypatch.setattr("uqpay.auth.httpx.post", post)
    manager = TokenManager("id", "key", "https://auth.example.test")
    assert manager.get_token() == "first"
    clock[0] = 1039
    assert manager.get_token() == "first"
    assert post.call_count == 1
    clock[0] = 1040
    assert manager.get_token() == "second"
    manager.invalidate()
    assert manager.get_token() == "third"
    assert post.call_count == 3


def test_concurrent_cold_requests_share_one_token_fetch(monkeypatch):
    monkeypatch.setattr("uqpay.auth.time.time", lambda: 1000)
    post = Mock(return_value=httpx.Response(200, json={"auth_token": "shared", "expired_at": 2000}))
    monkeypatch.setattr("uqpay.auth.httpx.post", post)
    manager = TokenManager("id", "key", "https://auth.example.test")
    barrier = Barrier(8)

    def get_token(_):
        barrier.wait(timeout=5)
        return manager.get_token()

    with ThreadPoolExecutor(max_workers=8) as pool:
        assert list(pool.map(get_token, range(8))) == ["shared"] * 8
    assert post.call_count == 1


def test_account_context_populated_after_first_call(client: UQPayClient):
    client.banking.balances.list({"page_number": 1, "page_size": 10})
    assert client.account_id is not None
    assert client.short_account_id is not None

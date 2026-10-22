"""Transport regressions use synthetic responses; no UQPAY endpoint is contacted."""
from unittest.mock import Mock

import httpx
import pytest

from uqpay import AuthenticationError
from uqpay.http import HttpClient


@pytest.fixture
def make_http(monkeypatch):
    monkeypatch.setattr("uqpay.http.time.sleep", lambda _: None)
    clients = []

    def make(handler):
        token = Mock(account_context=None)
        token.get_token.side_effect = lambda: "new-token" if token.invalidate.called else "old-token"
        client = HttpClient("https://api.example.test", token, "client", max_retries=2)
        client._http.close()
        client._http = httpx.Client(transport=httpx.MockTransport(handler))
        clients.append(client)
        return client, token

    yield make
    for client in clients:
        client.close()


@pytest.mark.parametrize("caller_key", [None, "caller-stable-key"])
def test_rate_limit_retries_preserve_write_body_and_key(make_http, caller_key):
    requests = []

    def handler(request):
        requests.append(request)
        if len(requests) < 3:
            return httpx.Response(429, json={"message": "rate limited"}, headers={"Retry-After": "0"})
        return httpx.Response(200, json={"id": "created"})

    client, _ = make_http(handler)
    options = {"on_behalf_of": "sub-account"}
    if caller_key:
        options["idempotency_key"] = caller_key
    assert client.request("POST", "/v1/example", body={"amount": "1.00"}, request_options=options) == {"id": "created"}
    assert len(requests) == 3
    keys = [request.headers["x-idempotency-key"] for request in requests]
    assert keys[0] and len(set(keys)) == 1
    if caller_key:
        assert keys[0] == caller_key
    assert all(request.content == b'{"amount": "1.00"}' for request in requests)
    assert all(request.headers["x-on-behalf-of"] == "sub-account" for request in requests)


def test_expired_token_retries_once_with_same_write_key(make_http):
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(401, json={"message": "token has expired"})

    client, token = make_http(handler)
    with pytest.raises(AuthenticationError):
        client.request("POST", "/v1/example", body={"amount": "1.00"})
    assert len(requests) == 2
    token.invalidate.assert_called_once()
    assert [r.headers["x-auth-token"] for r in requests] == ["Bearer old-token", "Bearer new-token"]
    assert requests[0].headers["x-idempotency-key"] == requests[1].headers["x-idempotency-key"]


def test_unrelated_401_does_not_refresh_or_retry(make_http):
    handler = Mock(return_value=httpx.Response(401, json={"message": "ip not allowed"}))
    client, token = make_http(handler)
    with pytest.raises(AuthenticationError):
        client.request("GET", "/v1/example")
    handler.assert_called_once()
    token.invalidate.assert_not_called()

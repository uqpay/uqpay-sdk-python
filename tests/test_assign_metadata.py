import json
import httpx
from uqpay import UQPayClient
from uqpay.types.issuing import AssignCardParams


def test_public_client_assign_metadata_and_omission(monkeypatch):
    requests = []
    def handler(request):
        if request.url.path == "/api/v1/connect/token":
            return httpx.Response(200, json={"auth_token": "offline-token", "expired_at": 4102444800})
        requests.append(request)
        return httpx.Response(200, json={"card_id": "card-1"})
    original_client = httpx.Client
    monkeypatch.setattr(httpx, "Client", lambda *args, **kwargs: original_client(*args, **{**kwargs, "transport": httpx.MockTransport(handler)}))
    def token_post(url, **kwargs):
        request = httpx.Request("POST", url, headers=kwargs.get("headers"))
        assert request.url.path == "/api/v1/connect/token"
        return httpx.Response(200, request=request, json={"auth_token": "offline-token", "expired_at": 4102444800})
    monkeypatch.setattr(httpx, "post", token_post)
    client = UQPayClient("offline-client", "offline-key")
    try:
        for metadata in [None, {"card_sku_code": "SKU123456789"}]:
            params: AssignCardParams = {"cardholder_id": "holder-1", "card_number": "example-pan", "card_currency": "USD", "card_mode": "SINGLE"}
            if metadata is not None:
                params["metadata"] = metadata
            assert client.issuing.cards.assign(params)["card_id"] == "card-1"
            assert requests[-1].method == "POST"
            assert requests[-1].url.path == "/api/v1/issuing/cards/assign"
            assert json.loads(requests[-1].content) == params
            if metadata is None:
                assert "metadata" not in json.loads(requests[-1].content)
    finally:
        client.close()

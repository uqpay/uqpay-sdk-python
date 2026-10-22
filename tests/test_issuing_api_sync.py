import json
from typing import get_type_hints
from unittest.mock import Mock
import httpx
from uqpay.http import HttpClient
from uqpay.resources.issuing import IssuingResource
from uqpay.types.issuing._update_cardholder_params import UpdateCardholderParamsIdentity
from uqpay.types.issuing._assign_card_params import AssignCardParams
from uqpay.types.issuing._create_card_params import CreateCardParams


def test_issuing_api_sync_wire_and_sparse_address():
    captured = []
    payload = {"cardholder_id": "holder-1", "residential_address": {"line2": None}}
    def handler(request):
        captured.append(request)
        return httpx.Response(200, json=payload)
    token = Mock(account_context={})
    token.get_token.return_value = "offline-token"
    http = HttpClient("https://example.test", token, "client")
    http._http.close()
    http._http = httpx.Client(transport=httpx.MockTransport(handler))
    try:
        issuing = IssuingResource(http, "https://example.test")
        def route(method, path):
            assert captured[-1].method == method
            assert captured[-1].url.path == path
        identity: UpdateCardholderParamsIdentity = {"proof_of_address": "cGRm", "proof_of_address_issue_date": "2026-10-01", "proof_of_address_issuing_country": "SG", "identity_verification": "a3lj"}
        issuing.cardholders.update("holder-1", {"identity": identity})
        route("POST", "/v1/issuing/cardholders/holder-1")
        assert json.loads(captured[-1].content) == {"identity": identity}
        for value in [None, ""]:
            update = {"identity": {"proof_of_address": value, "identity_verification": value}}
            issuing.cardholders.update("holder-1", update)
            route("POST", "/v1/issuing/cardholders/holder-1")
            assert json.loads(captured[-1].content) == update
        card: CreateCardParams = {"card_currency": "USD", "card_product_id": "product-1"}
        issuing.cards.create(card)
        route("POST", "/v1/issuing/cards")
        assert json.loads(captured[-1].content) == card
        assign: AssignCardParams = {"card_number": "example-pan", "card_currency": "USD", "card_mode": "SINGLE"}
        issuing.cards.assign(assign)
        route("POST", "/v1/issuing/cards/assign")
        assert json.loads(captured[-1].content) == assign
        assert issuing.cardholders.retrieve("holder-1") == payload
        route("GET", "/v1/issuing/cardholders/holder-1")
    finally:
        http.close()
    # Resolve postponed annotations, then check the public optionality contract.
    from typing_extensions import NotRequired
    from typing import get_origin
    assert get_origin(get_type_hints(UpdateCardholderParamsIdentity, include_extras=True)["type"]) is NotRequired
    assert get_origin(get_type_hints(AssignCardParams, include_extras=True)["cardholder_id"]) is NotRequired
    assert get_origin(get_type_hints(CreateCardParams, include_extras=True)["cardholder_id"]) is NotRequired

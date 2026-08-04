from __future__ import annotations
from typing import Any

from uqpay.resources.connect import ConnectResource
from uqpay.resources.issuing import IssuingResource
from uqpay.resources.payment import PaymentResource


class FakeHttp:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def request(
        self, method: str, path: str, *, body: Any = None,
        request_options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.calls.append({"method": method, "path": path, "body": body, "options": request_options})
        return {}


def test_connect_rfi_routes() -> None:
    http = FakeHttp()
    connect = ConnectResource(http)  # type: ignore[arg-type]

    connect.rfis.list({"page_size": 10, "page_number": 1, "status": "ACTION_REQUIRED"})
    connect.rfis.retrieve("rfi-1")
    connect.rfis.answer({"rfi_id": "rfi-1", "answer": []})

    assert [(c["method"], c["path"].split("?", 1)[0]) for c in http.calls] == [
        ("GET", "/v1/rfis"),
        ("GET", "/v1/rfis/rfi-1"),
        ("POST", "/v1/rfis/answer"),
    ]


def test_issuing_capability_routes() -> None:
    http = FakeHttp()
    issuing = IssuingResource(http, "https://api-sandbox.example.com")  # type: ignore[arg-type]

    issuing.cards.elevate_limit("card-1", {"limit_amount": 100})
    issuing.cards.enroll_network_protection("card-1", {"risk_control": "network_protection", "action_code": "01"})
    issuing.cards.remove_network_protection("card-1", {"risk_control": "network_protection"})
    issuing.cards.manage_pin({"card_id": "card-1", "type": "SET", "pin": "1234"})
    issuing.cards.list_arts({"card_product_id": "product-1"})
    issuing.cards.set_default_art({"card_art_id": "art-1"})
    issuing.merchant_brands.list({"page_size": 10, "page_number": 1})
    issuing.transactions.claim_unsolicited_refund({"related_transaction_id": "tx-1"})

    assert [(c["method"], c["path"].split("?", 1)[0]) for c in http.calls] == [
        ("POST", "/v1/issuing/cards/card-1/elevate_limit"),
        ("POST", "/v1/issuing/cards/card-1/risk"),
        ("DELETE", "/v1/issuing/cards/card-1/risk"),
        ("POST", "/v1/issuing/cards/manage/pin"),
        ("GET", "/v1/issuing/cards/arts"),
        ("POST", "/v1/issuing/cards/arts/default"),
        ("GET", "/v1/issuing/merchant_brands"),
        ("POST", "/v1/issuing/transactions/unsolicited_refund/release"),
    ]
    assert http.calls[2]["body"] == {"risk_control": "network_protection"}


def test_payment_terminal_routes_inject_client_id() -> None:
    http = FakeHttp()
    payment = PaymentResource(http, "client-1")  # type: ignore[arg-type]

    payment.terminals.register({"firm_code": "01", "firm_sn": "sn-1", "terminal_model": "model-1"})
    payment.terminals.get_pin_key({"terminal_id": "terminal-1", "prv_key": "secret"})

    assert [(c["method"], c["path"]) for c in http.calls] == [
        ("POST", "/v2/terminal/register"),
        ("POST", "/v2/terminal/getPinKey"),
    ]
    assert all(c["options"]["_extra_headers"]["x-client-id"] == "client-1" for c in http.calls)

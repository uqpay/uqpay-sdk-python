from typing import get_type_hints
from uqpay.types.issuing import ResetPinParams
from uqpay.types.connect._rfi_params import RfiAnswerItem
from uqpay.types.simulator import SimulateDepositCreationParams

def test_contract_type_fields():
    assert "type" in get_type_hints(ResetPinParams)
    assert "old_pin" in get_type_hints(ResetPinParams)
    assert "text" in get_type_hints(RfiAnswerItem)
    assert "account_id" in get_type_hints(SimulateDepositCreationParams)

from typing import Any
from uqpay.resources.issuing import IssuingResource
from uqpay.resources.connect import ConnectResource
from uqpay.resources.simulator import SimulatorResource

class FakeHttp:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.response: dict[str, Any] = {}

    def request(self, method: str, path: str, *, body: Any = None, request_options: Any = None) -> dict[str, Any]:
        self.calls.append({"method": method, "path": path, "body": body, "options": request_options})
        return self.response

def test_aligned_requests_and_responses():
    http = FakeHttp()
    issuing = IssuingResource(http, "https://api-sandbox.example.test")  # type: ignore[arg-type]
    connect = ConnectResource(http)  # type: ignore[arg-type]
    simulator = SimulatorResource(http, "https://api-sandbox.example.test")  # type: ignore[arg-type]
    http.response = {"request_status": "SUCCESS", "card_order_id": "order-1", "order_status": "PROCESSING"}
    art = {"card_art_id": "art-1", "name_on_card": "Test"}
    assert issuing.cards.update("card-1", art)["order_status"] == "PROCESSING"
    assert http.calls[-1]["body"] == art
    assert http.calls[-1]["path"] == "/v1/issuing/cards/card-1"
    for params in [
        {"card_id": "card-1", "pin": "135790"},
        {"card_id": "card-1", "pin": "135790", "type": "RESET"},
        {"card_id": "card-1", "pin": "135790", "type": "UPDATE", "old_pin": "024680"},
    ]:
        assert issuing.cards.reset_pin(params) == http.response
        assert http.calls[-1]["body"] == params
        assert http.calls[-1]["path"] == "/v1/issuing/cards/pin"
    http.response = {"rfi_id": "ACTREQ-test", "request": [{"answer": {"type": "ATTACHMENT", "attachments": [{"file_name": "proof.pdf", "size": 42}]}}]}
    params = {"rfi_id": "ACTREQ-test", "answer": [{"key": "note", "type": "TEXT", "text": "source of funds"}]}
    assert connect.rfis.answer(params) == http.response
    assert http.calls[-1]["body"] == params
    http.response = {"settlement_status": "SETTLED", "transaction_amount": "123456789.01"}
    assert issuing.transactions.retrieve("tx-1") == http.response
    params = {"account_id": "account-1", "amount": 10, "currency": "SGD", "sender_swift_code": "WELGBE22"}
    simulator.deposits.simulate(params)
    assert http.calls[-1]["body"] == params

import hashlib
import hmac
import json
import time
import pytest
from uqpay.webhooks import WebhookVerifier
from uqpay.resources.banking import BankingResource

@pytest.mark.parametrize("method", "card card_present wechatpay alipay alipaycn alipayhk paynow grabpay applepay googlepay unionpay crypto tng truemoney gcash dana kakaopay tosspay naverpay mpay kplus boost rabbitlinepay kaspi hipay shopeepay".split())
def test_signed_webhook_fields(method):
    event = {"version": "V1.6.0", "event_id": "evt-test", "event_name": "ACQUIRING", "event_type": "acquiring.payment_intent.succeeded", "data": {"amount": "12345678901234567890.12345678", "complete_time": None, "metadata": None, "payment_method": {"type": method, method: {"flow": None, "os_type": "", "static_qrcode": "qr", "issuer_country_code": "SG"}}, "wallet_type": "FUTURE_WALLET"}}
    raw = json.dumps(event).encode()
    timestamp = str(int(time.time() * 1000))
    signature = hmac.new(b"offline-secret", raw + timestamp.encode(), hashlib.sha512).hexdigest()
    assert WebhookVerifier("offline-secret").construct_event(raw, {"x-wk-signature": signature, "x-wk-timestamp": timestamp}) == event

def test_iban_only_check_wire():
    http = FakeHttp()
    banking = BankingResource(http)  # type: ignore[arg-type]
    params = {"entity_type": "COMPANY", "payment_method": "LOCAL", "currency": "EUR", "iban": "DE89370400440532013000", "bank_country_code": "DE"}
    banking.beneficiaries.check(params)
    assert http.calls[-1]["body"] == params
    assert http.calls[-1]["path"] == "/v1/beneficiaries/check"

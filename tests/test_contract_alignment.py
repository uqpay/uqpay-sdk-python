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

from typing import Any, get_type_hints
from typing_extensions import Literal, NotRequired
from uqpay.resources.payment.intents import PaymentIntentsResource
from uqpay.types.payment._capture_payment_intent_params import CapturePaymentIntentParams
from uqpay.types.payment._create_payment_intent_params import CreatePaymentIntentParams, CreatePaymentIntentParamsPaymentMethodCard
from uqpay.types.payment._confirm_payment_intent_params import ConfirmPaymentIntentParams

class FakeHttp:
    def __init__(self):
        self.calls = []
        self.response = {"payment_intent_id": "pi-1", "intent_status": "PARTIALLY_CAPTURED", "captured_amount": "6.00", "authorization_expires_at": None, "available_to_capture": "0.00", "available_to_void": "0.00", "capture_id": "cap-1", "capture_records": [{"capture_id": "cap-1", "channel_capture_status": 0, "complete_time": None}]}
    def request(self, method: str, path: str, *, body: Any = None, request_options: Any = None):
        self.calls.append((method, path, body))
        return self.response

def test_payment_api_sync_wire_and_response():
    http = FakeHttp()
    resource = PaymentIntentsResource(http, "offline-client")
    request = {"authorization_type": "pre_authorization", "payment_method": {"type": "card_present", "card_present": {"auto_capture": False, "authorization_type": "pre_authorization"}}}
    resource.create(request)
    resource.confirm("pi-1", request)
    capture: CapturePaymentIntentParams = {"amount_to_capture": "6.00", "final_capture": True, "merchant_capture_order_id": "order-cap-1"}
    result = resource.capture("pi-1", capture)
    assert [c[0] for c in http.calls] == ["POST", "POST", "POST"]
    assert [c[1] for c in http.calls] == ["/v2/payment_intents/create", "/v2/payment_intents/pi-1/confirm", "/v2/payment_intents/pi-1/capture"]
    assert http.calls[0][2]["payment_method"]["card_present"]["auto_capture"] is False
    assert http.calls[-1][2] == capture
    assert result == http.response
    assert result["authorization_expires_at"] is None
    resource.capture("pi-1")
    assert http.calls[-1][2] == {}

def test_payment_api_sync_request_types():
    assert get_type_hints(CapturePaymentIntentParams)["amount_to_capture"] is str
    assert get_type_hints(CapturePaymentIntentParams)["final_capture"] == Literal[True]
    for cls in (CreatePaymentIntentParams, ConfirmPaymentIntentParams):
        assert "authorization_type" in get_type_hints(cls)
    assert get_type_hints(CreatePaymentIntentParamsPaymentMethodCard, include_extras=True)["authorization_type"] == NotRequired[Literal["authorization", "pre_authorization"]]

import hashlib
import hmac
import json
import time
from uqpay.webhooks import WebhookVerifier

def test_payment_api_sync_signed_alert_payload():
    for status in ("FAILED", "SUCCEEDED", "CANCELLED", "INITIATED", "AUTHENTICATION_REDIRECTED", "PENDING_AUTHORIZATION", "AUTHORIZED", "CAPTURE_REQUESTED", "SETTLED", "EXPIRED"):
        event = {"version": "V1.6.0", "event_id": "evt-1", "event_name": "ACQUIRING", "event_type": "acquiring.chargeback.alert.created", "data": {"order_status": status, "alert_status": "EXPIRED", "card_scheme": "VISA", "card_masked": "411111******1111", "auth_code": "test", "arn": "reference", "payment_method": {"card": {"issuer_country_code": "SG"}, "card_present": {"issuer_country_code": ""}}}}
        raw = json.dumps(event).encode()
        timestamp = str(int(time.time() * 1000))
        signature = hmac.new(b"offline-secret", raw + timestamp.encode(), hashlib.sha512).hexdigest()
        assert WebhookVerifier("offline-secret").construct_event(raw, {"x-wk-signature": signature, "x-wk-timestamp": timestamp}) == event

from __future__ import annotations
import hashlib
import hmac
import json
import time
from uqpay import UQPayWebhookError
from uqpay.webhooks import WebhookVerifier
import pytest


def _sign(secret: str, body: bytes, timestamp: int) -> str:
    signed = f"{timestamp}.".encode("utf-8") + body
    return hmac.new(secret.encode("utf-8"), signed, hashlib.sha256).hexdigest()


SECRET = "whsec_test_secret"
PAYLOAD = {"event_type": "card.3ds.otp", "event_id": "abc123", "data": {}}


def test_valid_signature_returns_event():
    verifier = WebhookVerifier(SECRET)
    body = json.dumps(PAYLOAD).encode()
    ts = int(time.time())
    sig = _sign(SECRET, body, ts)
    event = verifier.construct_event(body, {"x-wk-signature": sig, "x-wk-timestamp": str(ts)})
    assert event["event_type"] == "card.3ds.otp"


def test_wrong_signature_raises():
    verifier = WebhookVerifier(SECRET)
    body = json.dumps(PAYLOAD).encode()
    ts = int(time.time())
    with pytest.raises(UQPayWebhookError, match="verification failed"):
        verifier.construct_event(body, {"x-wk-signature": "badsig", "x-wk-timestamp": str(ts)})


def test_stale_timestamp_raises():
    verifier = WebhookVerifier(SECRET, tolerance=300)
    body = json.dumps(PAYLOAD).encode()
    ts = int(time.time()) - 400  # outside tolerance
    sig = _sign(SECRET, body, ts)
    with pytest.raises(UQPayWebhookError, match="tolerance"):
        verifier.construct_event(body, {"x-wk-signature": sig, "x-wk-timestamp": str(ts)})


def test_missing_signature_header_raises():
    verifier = WebhookVerifier(SECRET)
    with pytest.raises(UQPayWebhookError, match="x-wk-signature"):
        verifier.construct_event(b"{}", {"x-wk-timestamp": "12345"})

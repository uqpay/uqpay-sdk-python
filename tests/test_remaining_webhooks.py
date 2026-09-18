import hashlib
import hmac
import json
from pathlib import Path
import time
import pytest
from uqpay import UQPayWebhookError
from uqpay.webhooks import WebhookVerifier

@pytest.mark.parametrize("case", json.loads((Path(__file__).parent / "fixtures/remaining-webhooks.json").read_text()))
def test_remaining_signed_fields(case):
    body = json.dumps({"event_type": case["kind"], "data": case["data"]}).encode()
    timestamp = str(int(time.time() * 1000))
    signature = hmac.new(b"offline-secret", body + timestamp.encode(), hashlib.sha512).hexdigest()
    headers = {"x-wk-signature": signature, "x-wk-timestamp": timestamp}
    verifier = WebhookVerifier("offline-secret")
    assert verifier.construct_event(body, headers)["data"] == case["data"]
    with pytest.raises(UQPayWebhookError):
        verifier.construct_event(body + b" ", headers)

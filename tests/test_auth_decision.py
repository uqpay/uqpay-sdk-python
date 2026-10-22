"""Exercise both sides of the encrypted callback with disposable synthetic keys."""
import json

import pytest

from uqpay.crypto import PgpContext, generate_auth_decision_key_pair
from uqpay.resources.issuing.auth_decision import AuthDecisionResource


@pytest.fixture(scope="module")
def peers():
    customer = generate_auth_decision_key_pair("Synthetic Customer", "customer@example.test")
    gateway = generate_auth_decision_key_pair("Synthetic Gateway", "gateway@example.test")
    resource = AuthDecisionResource()
    resource.configure(customer["private_key"], gateway["public_key"])
    gateway_pgp = PgpContext.create(gateway["private_key"], customer["public_key"])
    return resource, gateway_pgp


def test_encrypted_decision_roundtrip_preserves_transaction_and_decision(peers):
    resource, gateway = peers
    transaction = {"transaction_id": "tx-synthetic", "amount": "1234567890.12"}
    received = []

    def decide(payload):
        received.append(payload)
        return {"response_code": "00", "partner_reference_id": "partner-synthetic"}

    reply = resource.handle(gateway.encrypt(json.dumps(transaction)).encode(), {}, decide)
    assert received == [transaction]
    assert json.loads(gateway.decrypt(reply)) == {
        "transaction_id": "tx-synthetic", "response_code": "00",
        "partner_reference_id": "partner-synthetic",
    }


def test_callback_failure_propagates_without_a_success_reply(peers):
    resource, gateway = peers

    def fail(_):
        raise ValueError("synthetic decision failed")

    with pytest.raises(ValueError, match="synthetic decision failed"):
        resource.handle(gateway.encrypt('{"transaction_id":"tx-synthetic"}'), {}, fail)

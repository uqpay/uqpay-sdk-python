from typing import Any
from urllib.parse import urlsplit, parse_qs
from uqpay.resources.banking import BankingResource
from uqpay.types.banking import CreatePayoutParams
from typing_extensions import get_type_hints, NotRequired, get_origin

class FakeHttp:
    def __init__(self):
        self.calls = []
        self.response = {}
    def request(self, method, path, *, body=None, request_options=None):
        self.calls.append((method, path, body, request_options))
        return self.response

def test_banking_api_sync_wire_and_rule_retention():
    http = FakeHttp()
    banking = BankingResource(http)
    options = {"on_behalf_of": "sub-account"}
    http.response = {"channel_code": "MASTERCARD", "sufficient_funds": False, "beneficiary_valid": True, "fee_amount": "5", "total_amount": "6"}
    result = banking.payouts.validate({"beneficiary_id": "saved + id", "currency": "USD", "amount": "1.00", "fee_paid_by": "OURS"}, options)
    method, path, body, sent_options = http.calls[-1]
    assert method == "GET" and body is None and sent_options == options
    assert urlsplit(path).path == "/v1/payouts/validation"
    assert parse_qs(urlsplit(path).query)["beneficiary_id"] == ["saved + id"]
    assert result["sufficient_funds"] is False
    assert result["beneficiary_valid"] is True
    assert result["fee_amount"] == "5" and result["total_amount"] == "6"
    rules = {"data": [{"payment_method": "CARD", "validation_field": ["account_number", {"value": "card_expiry", "children": [{"type": "MONTH"}]}]}]}
    http.response = rules
    assert banking.payment_methods.list({"currency": "USD", "country": "US", "entity_type": "INDIVIDUAL"}, options) == rules
    assert "entity_type=INDIVIDUAL" in http.calls[-1][1]
    banking.beneficiaries.list({"payment_method": "CARD"}, options)
    assert "payment_method=CARD" in http.calls[-1][1]
    card = {"entity_type": "INDIVIDUAL", "payment_method": "CARD", "bank_details": {"account_holder": "Test Recipient", "account_number": "1234567890123", "account_currency_code": "USD", "bank_country_code": "US", "clearing_system": "MASTERCARD SEND", "card_expiry": "2099-12"}}
    banking.beneficiaries.create(card, options)
    assert http.calls[-1][2] == card
    banking.beneficiaries.update("ben-id", card, options)
    assert http.calls[-1][2]["bank_details"]["card_expiry"] == "2099-12"
    hints = get_type_hints(CreatePayoutParams, include_extras=True)
    for field in ("payout_reference", "fee_paid_by", "payout_date"):
        assert get_origin(hints[field]) is NotRequired


def test_sparse_individual_card_address_public_request():
    from uqpay.types.banking._create_payout_params import CreatePayoutParamsBeneficiaryAddress

    hints = get_type_hints(CreatePayoutParamsBeneficiaryAddress, include_extras=True)
    for field in ("country", "city"):
        assert get_origin(hints[field]) is NotRequired
    http = FakeHttp()
    banking = BankingResource(http)
    card = {
        "entity_type": "INDIVIDUAL", "payment_method": "CARD",
        "bank_details": {
            "account_holder": "Test Recipient", "account_number": "1234567890123",
            "account_currency_code": "USD", "bank_country_code": "US",
            "clearing_system": "MASTERCARD SEND", "card_expiry": "2099-12",
        },
        "address": {"nationality": "US"},
    }
    body: CreatePayoutParams = {
        "currency": "USD", "amount": "1", "purpose_code": "BILL_PAYMENT",
        "beneficiary": card,
    }
    options = {"on_behalf_of": "sub-account"}
    banking.payouts.create(body, options)
    method, path, sent_body, sent_options = http.calls[-1]
    assert (method, path, sent_options) == ("POST", "/v1/payouts", options)
    assert sent_body["beneficiary"]["address"] == {"nationality": "US"}

from __future__ import annotations

from typing import Any, get_args

import hashlib
import hmac
import json
import time

import pytest
from typing_extensions import get_type_hints

from uqpay.error import InvalidIdempotencyKeyError, NotFoundError, make_api_error
from uqpay.idempotency import validate_idempotency_key
from uqpay.resources.banking import BankingResource
from uqpay.types.banking import (
    CreateVirtualAccountParams,
    ListVirtualAccountApplicationsParams,
    VirtualAccountApplicationResponse,
    VirtualAccountApplicationWebhookEvent,
)
from uqpay.webhooks import WebhookVerifier


class FakeHttp:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Any = None,
        request_options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.calls.append(
            {"method": method, "path": path, "body": body, "options": request_options}
        )
        return {}


def test_application_routes_are_distinct_from_issued_accounts() -> None:
    http = FakeHttp()
    banking = BankingResource(http)  # type: ignore[arg-type]
    options = {"on_behalf_of": "account-id"}

    banking.virtual_accounts.list({"currency": "USD"}, options)
    banking.virtual_account_applications.list(
        {
            "page_number": 1,
            "page_size": 50,
            "status": "SUBMITTED",
            "country": "sg",
            "currency": "usd",
        },
        options,
    )
    banking.virtual_account_applications.retrieve("application-id", options)

    assert [call["method"] for call in http.calls] == ["GET", "GET", "GET"]
    assert http.calls[0]["path"] == "/v1/virtual/accounts?currency=USD"
    assert http.calls[1]["path"] == (
        "/v1/virtual/applications?page_number=1&page_size=50&status=SUBMITTED"
        "&country=sg&currency=usd"
    )
    assert http.calls[2]["path"] == "/v1/virtual/applications/application-id"
    assert all(call["options"] == options for call in http.calls)


def test_create_forwards_application_body_and_request_headers_options() -> None:
    http = FakeHttp()
    banking = BankingResource(http)  # type: ignore[arg-type]
    body: CreateVirtualAccountParams = {
        "country": "BH",
        "currency": "USD",
        "payment_method": "SWIFT",
        "nickname": "Operating account",
    }
    options = {
        "idempotency_key": "merchant-va-application-42",
        "on_behalf_of": "account-id",
    }

    banking.virtual_accounts.create(body, options)
    banking.virtual_accounts.create(body, options)  # legal replay keeps the same key/body

    expected = {
        "method": "POST",
        "path": "/v1/virtual/accounts",
        "body": body,
        "options": options,
    }
    assert http.calls == [
        expected,
        {
            "method": "POST",
            "path": "/v1/virtual/accounts",
            "body": body,
            "options": options,
        },
    ]


def test_create_and_list_required_typed_fields() -> None:
    create_hints = get_type_hints(CreateVirtualAccountParams, include_extras=True)
    list_hints = get_type_hints(
        ListVirtualAccountApplicationsParams, include_extras=True
    )
    assert get_args(create_hints["country"])[0] is str
    assert get_args(create_hints["currency"])[0] is str
    assert "Required" in repr(create_hints["country"])
    payment_method = get_args(create_hints["payment_method"])[0]
    nickname = get_args(create_hints["nickname"])[0]
    assert type(None) in get_args(payment_method)
    assert type(None) in get_args(nickname)
    assert "Required" in repr(list_hints["page_number"])
    assert "Required" in repr(list_hints["page_size"])


def test_webhook_type_pins_versions_and_application_events() -> None:
    hints = get_type_hints(VirtualAccountApplicationWebhookEvent)
    assert set(get_args(hints["version"])) == {"V1.5.1", "V1.5.2", "V1.6.0"}
    assert set(get_args(hints["event_type"])) == {
        "virtual.account.create",
        "virtual.account.update",
        "virtual.account.closed",
    }


def test_idempotency_key_accepts_gateway_contract() -> None:
    validate_idempotency_key("merchant-va-application-42")
    validate_idempotency_key("x" * 64)
    with pytest.raises(InvalidIdempotencyKeyError):
        validate_idempotency_key("")
    with pytest.raises(InvalidIdempotencyKeyError):
        validate_idempotency_key("x" * 65)


def test_strict_application_not_found_error_contract() -> None:
    raw = {
        "type": "not_found",
        "code": "virtual_account_application_not_found",
        "message": "Virtual account application not found",
    }
    error = make_api_error(raw, 400, {}, {})
    assert isinstance(error, NotFoundError)
    assert error.http_status == 400
    assert error.type == "not_found"
    assert error.code == "virtual_account_application_not_found"
    assert error.message == "Virtual account application not found"


@pytest.mark.parametrize("version", ["V1.5.1", "V1.5.2", "V1.6.0"])
@pytest.mark.parametrize(
    "event_type",
    [
        "virtual.account.create",
        "virtual.account.update",
        "virtual.account.closed",
    ],
)
def test_verified_webhook_parser_preserves_application_contract(
    version: str, event_type: str
) -> None:
    secret = "whsec_va_test"
    payload = {
        "version": version,
        "event_name": "VIRTUAL",
        "event_type": event_type,
        "event_id": "event-id",
        "source_id": "application-id",
        "data": {
            "application_id": "application-id",
            "public_version": 3,
            "country": "BH",
            "currency": "USD",
            "status": "CLOSED",
            "results": [
                {
                    "payment_method": "SWIFT",
                    "status": "CLOSED",
                    "virtual_accounts": [
                        {
                            "account_bank_id": "bank-id",
                            "account_holder": "Merchant",
                            "account_number": "123",
                            "country_code": "BH",
                            "currency": "USD",
                            "bank_name": "Bank",
                            "bank_address": "Address",
                            "clearing_system": {
                                "type": "bic_swift",
                                "value": "BANKBHBM",
                            },
                            "status": "CLOSED",
                            "close_reason": "",
                        }
                    ],
                    "error": None,
                }
            ],
        },
    }
    body = json.dumps(payload, separators=(",", ":")).encode()
    timestamp = str(int(time.time()))
    signature = hmac.new(
        secret.encode(), body + timestamp.encode(), hashlib.sha512
    ).hexdigest()
    event = WebhookVerifier(secret).construct_event(
        body,
        {"x-wk-signature": signature, "x-wk-timestamp": timestamp},
    )
    assert event["source_id"] == event["data"]["application_id"]
    assert event["data"]["public_version"] == 3
    bank = event["data"]["results"][0]["virtual_accounts"][0]
    assert bank["close_reason"] == ""
    assert bank["clearing_system"] == {"type": "bic_swift", "value": "BANKBHBM"}


def test_async_failed_result_preserves_provisioning_error_fixture() -> None:
    payload: VirtualAccountApplicationResponse = {
        "data": {
            "application_id": "application-id",
            "public_version": 2,
            "country": "BH",
            "currency": "USD",
            "status": "FAILED",
            "results": [
                {
                    "payment_method": "SWIFT",
                    "status": "FAILED",
                    "virtual_accounts": [],
                    "error": {
                        "code": "VA_PROVISIONING_FAILED",
                        "message": "Virtual account provisioning failed",
                    },
                }
            ],
        }
    }

    application = payload["data"]
    result = application["results"][0]
    assert application["status"] == "FAILED"
    assert result["status"] == "FAILED"
    assert result["virtual_accounts"] == []
    assert result["error"] == {
        "code": "VA_PROVISIONING_FAILED",
        "message": "Virtual account provisioning failed",
    }

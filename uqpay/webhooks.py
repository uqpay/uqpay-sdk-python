from __future__ import annotations
import hashlib
import hmac
import json
import time
from typing import Any
from typing_extensions import TypeGuard
from .error import UQPayWebhookError
from .types.banking import VirtualAccountApplicationWebhookEvent

_VA_APPLICATION_VERSIONS = frozenset({"V1.5.1", "V1.5.2", "V1.6.0"})
_VA_APPLICATION_EVENT_TYPES = frozenset({
    "virtual.account.create",
    "virtual.account.update",
    "virtual.account.closed",
})


def is_virtual_account_application_event(
    event: dict[str, Any],
) -> TypeGuard[VirtualAccountApplicationWebhookEvent]:
    """Narrow supported VA application events without reclassifying old events."""
    data = event.get("data")
    if not isinstance(data, dict):
        return False
    return (
        event.get("version") in _VA_APPLICATION_VERSIONS
        and event.get("event_name") == "VIRTUAL"
        and event.get("event_type") in _VA_APPLICATION_EVENT_TYPES
        and isinstance(event.get("event_id"), str)
        and isinstance(event.get("source_id"), str)
        and isinstance(data.get("application_id"), str)
        and event["source_id"] == data["application_id"]
        and isinstance(data.get("account_id"), str)
        and bool(data["account_id"])
        and isinstance(data.get("direct_id"), str)
        and bool(data["direct_id"])
    )


class WebhookVerifier:
    """Verify HMAC-SHA512 webhook signatures from UQPAY."""

    def __init__(self, secret: str, tolerance: int = 300) -> None:
        self._secret = secret
        self._tolerance = tolerance  # seconds

    def construct_event(
        self,
        raw_body: bytes | str,
        headers: dict[str, str | None],
    ) -> dict[str, Any]:
        """
        Verify the webhook signature and return the parsed event dict.

        Args:
            raw_body: The raw request body bytes (NOT parsed JSON).
            headers: Request headers dict (case-insensitive keys work if lowercased).

        Raises:
            UQPayWebhookError: If signature is missing, invalid, or timestamp is stale.
        """
        if isinstance(raw_body, str):
            body_bytes = raw_body.encode("utf-8")
        else:
            body_bytes = raw_body

        # Normalise header keys to lowercase
        lower_headers = {k.lower(): v for k, v in headers.items()}

        signature = lower_headers.get("x-wk-signature")
        timestamp_str = lower_headers.get("x-wk-timestamp")

        if signature is None:
            raise UQPayWebhookError("Webhook header missing: x-wk-signature")
        if timestamp_str is None:
            raise UQPayWebhookError("Webhook header missing: x-wk-timestamp")

        try:
            timestamp = int(timestamp_str)
        except ValueError as exc:
            raise UQPayWebhookError(f"Invalid x-wk-timestamp: {timestamp_str!r}") from exc

        # Webhook Hub emits Unix milliseconds. Keep accepting Unix seconds for
        # compatibility, but always sign with the original header string.
        timestamp_seconds = timestamp // 1000 if timestamp >= 1_000_000_000_000 else timestamp

        # Check timestamp tolerance
        now = int(time.time())
        if abs(now - timestamp_seconds) > self._tolerance:
            raise UQPayWebhookError(
                f"Webhook timestamp is outside the allowed tolerance of {self._tolerance}s"
            )

        # UQPAY signs the exact raw payload followed by the timestamp string.
        signed_payload = body_bytes + timestamp_str.encode("utf-8")
        expected = hmac.new(
            self._secret.encode("utf-8"),
            signed_payload,
            hashlib.sha512,
        ).hexdigest()

        if not hmac.compare_digest(expected, signature):
            raise UQPayWebhookError("Webhook signature verification failed")

        try:
            return json.loads(body_bytes)
        except json.JSONDecodeError as exc:
            raise UQPayWebhookError(f"Webhook body is not valid JSON: {exc}") from exc

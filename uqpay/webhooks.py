from __future__ import annotations
import hashlib
import hmac
import json
import time
from typing import Any
from .error import UQPayWebhookError


class WebhookVerifier:
    """Verify HMAC-SHA256 webhook signatures from UQPAY."""

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

        # Check timestamp tolerance
        now = int(time.time())
        if abs(now - timestamp) > self._tolerance:
            raise UQPayWebhookError(
                f"Webhook timestamp is outside the allowed tolerance of {self._tolerance}s"
            )

        # Compute expected signature: HMAC-SHA256(secret, "{timestamp}.{body}")
        signed_payload = f"{timestamp}.".encode("utf-8") + body_bytes
        expected = hmac.new(
            self._secret.encode("utf-8"),
            signed_payload,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected, signature):
            raise UQPayWebhookError("Webhook signature verification failed")

        try:
            return json.loads(body_bytes)
        except json.JSONDecodeError as exc:
            raise UQPayWebhookError(f"Webhook body is not valid JSON: {exc}") from exc

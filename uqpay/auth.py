from __future__ import annotations
import base64
import json
import threading
import time
from typing import Any
import httpx
from .error import AuthenticationError
from .version import SDK_VERSION

REFRESH_BUFFER_SECONDS = 60
_TOKEN_EXPIRED_PATTERNS = [
    "token has expired",
    "login expired",
    "token expired",
    "jwt expired",
]


def _parse_jwt(token: str) -> dict[str, str]:
    """Decode JWT payload (base64url) and extract account context fields."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Malformed JWT")
    payload = parts[1]
    # Add padding required by base64
    padding = (4 - len(payload) % 4) % 4
    payload += "=" * padding
    decoded = base64.urlsafe_b64decode(payload).decode("utf-8")
    data: dict[str, Any] = json.loads(decoded)
    return {
        "account_id": str(data.get("entity_id", "")),
        "short_account_id": str(data.get("short_entity_id", "")),
        "parent_account_id": str(data.get("parent_entity_id", "")),
        "client_id": str(data.get("client_id", "")),
        "api_version": str(data.get("api_version", "")),
        "business_type": str(data.get("bus_type", "")),
    }


class TokenManager:
    """Manages auth token lifecycle: fetch, cache, and refresh."""

    def __init__(self, client_id: str, api_key: str, base_url: str) -> None:
        self._client_id = client_id
        self._api_key = api_key
        self._base_url = base_url
        self._token: str | None = None
        self._expires_at: int = 0
        self._account_context: dict[str, str] | None = None
        self._lock = threading.Lock()

    @property
    def account_context(self) -> dict[str, str] | None:
        return self._account_context

    def get_token(self) -> str:
        now = int(time.time())
        # Fast path — check without lock
        if self._token and (self._expires_at - now) > REFRESH_BUFFER_SECONDS:
            return self._token
        # Slow path — acquire lock, re-check, refresh if needed
        with self._lock:
            if self._token and (self._expires_at - now) > REFRESH_BUFFER_SECONDS:
                return self._token
            return self._do_refresh()

    def invalidate(self) -> None:
        """Force token expiry (called after 401 on an API call)."""
        with self._lock:
            self._token = None
            self._expires_at = 0
            self._account_context = None

    def _do_refresh(self) -> str:
        ctx: dict[str, Any] = {
            "method": "POST",
            "path": "/v1/connect/token",
            "retry_count": 0,
            "timestamp": "",
            "idempotency_key": None,
        }
        diag: dict[str, Any] = {
            "client_id": self._client_id,
            "environment": "unknown",
            "sdk_version": SDK_VERSION,
        }
        try:
            response = httpx.post(
                f"{self._base_url}/v1/connect/token",
                headers={
                    "x-client-id": self._client_id,
                    "x-api-key": self._api_key,
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
        except Exception as exc:
            raise AuthenticationError(
                {"type": "unauthorized_error", "code": "network_error", "message": str(exc)},
                0, ctx, diag,
            ) from exc

        if not response.is_success:
            message = f"Token request failed with status {response.status_code}"
            try:
                body = response.json()
                message = str(body.get("error") or body.get("message") or message)
            except Exception:
                pass
            raise AuthenticationError(
                {"type": "unauthorized_error", "code": "authentication_error", "message": message},
                response.status_code, ctx, diag,
            )

        try:
            data: dict[str, Any] = response.json()
            self._token = data["auth_token"]
            self._expires_at = int(data["expired_at"])
        except Exception as exc:
            raise AuthenticationError(
                {"type": "unauthorized_error", "code": "malformed_response", "message": f"Token response malformed: {exc}"},
                response.status_code, ctx, diag,
            ) from exc
        try:
            self._account_context = _parse_jwt(self._token)
        except Exception:
            self._account_context = None
        return self._token

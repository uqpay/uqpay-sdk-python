from __future__ import annotations
from typing import Any


class UQPayError(Exception):
    """Base class for all UQPAY API errors."""

    def __init__(self, body: dict[str, Any], http_status: int, ctx: dict[str, Any], diag: dict[str, Any]) -> None:
        super().__init__(body["message"])
        self.type: str = body["type"]
        self.code: str = str(body.get("code", ""))
        self.message: str = body["message"]
        self.http_status: int = http_status
        self.idempotency_key: str | None = ctx.get("idempotency_key")
        self.timestamp: str = ctx.get("timestamp", "")
        self.method: str = ctx.get("method", "")
        self.path: str = ctx.get("path", "")
        self.environment: str = diag.get("environment", "")
        self.account_id: str | None = diag.get("account_id")
        self.short_account_id: str | None = diag.get("short_account_id")
        self.client_id: str = diag.get("client_id", "")
        self.on_behalf_of: str | None = ctx.get("on_behalf_of")
        self.sdk_version: str = diag.get("sdk_version", "")
        self.retry_count: int = ctx.get("retry_count", 0)
        self.missing_fields: list | None = body.get("missing_fields")


class AuthenticationError(UQPayError):
    """401 — invalid or expired credentials."""


class ForbiddenError(UQPayError):
    """403 — access denied."""


class NotFoundError(UQPayError):
    """404 — resource not found."""


class ValidationError(UQPayError):
    """400 — request validation failed."""


class IdempotencyError(UQPayError):
    """400 with type==idempotency_error — idempotency key conflict."""


class ConflictError(UQPayError):
    """409 — resource conflict."""


class RateLimitError(UQPayError):
    """429 — too many requests."""


class ServerError(UQPayError):
    """5xx — server-side error."""


class NetworkError(Exception):
    """Network/timeout failure — no HTTP response received."""

    def __init__(self, message: str, ctx: dict[str, Any], diag: dict[str, Any]) -> None:
        super().__init__(message)
        self.method: str = ctx.get("method", "")
        self.path: str = ctx.get("path", "")
        self.environment: str = diag.get("environment", "")
        self.client_id: str = diag.get("client_id", "")
        self.sdk_version: str = diag.get("sdk_version", "")
        self.retry_count: int = ctx.get("retry_count", 0)


class UQPayWebhookError(Exception):
    """Webhook signature verification failed."""


class SimulatorNotAvailableError(Exception):
    """Simulator endpoint called outside sandbox."""

    def __init__(self) -> None:
        super().__init__("The simulator is only available in sandbox mode.")


class InvalidIdempotencyKeyError(Exception):
    """Caller-supplied idempotency key is not a valid UUID v4."""

    def __init__(self, key: str) -> None:
        super().__init__(
            f'Idempotency key "{key}" is not a valid UUID v4. '
            "Generate one with uuid.uuid4() or generate_idempotency_key()."
        )


def _infer_error_type(status: int) -> str:
    if status == 401:
        return "unauthorized_error"
    if status == 403:
        return "forbidden"
    if status == 404:
        return "not_found"
    if status == 409:
        return "conflict_error"
    if status == 429:
        return "rate_limit_error"
    if status >= 500:
        return "api_error"
    return "invalid_request_error"


def _parse_error_body(raw: Any, status: int) -> dict[str, Any]:
    if isinstance(raw, str):
        return {"type": _infer_error_type(status), "code": str(status), "message": raw[:200]}
    if not isinstance(raw, dict):
        return {"type": _infer_error_type(status), "code": str(status), "message": "Unknown error"}
    # Auth gateway: { error: "..." } on 401
    if status == 401 and isinstance(raw.get("error"), str):
        return {"type": "unauthorized_error", "code": "authentication_error", "message": raw["error"]}
    # Modern format: { type, code, message }
    if isinstance(raw.get("type"), str) and isinstance(raw.get("message"), str):
        body: dict[str, Any] = {
            "type": raw["type"],
            "code": str(raw.get("code", "")),
            "message": raw["message"],
        }
        if isinstance(raw.get("missing_fields"), list):
            body["missing_fields"] = raw["missing_fields"]
        return body
    # Legacy format: { code: int, message: str }
    if isinstance(raw.get("message"), str):
        return {
            "type": _infer_error_type(status),
            "code": str(raw.get("code", status)),
            "message": raw["message"],
        }
    import json
    return {"type": _infer_error_type(status), "code": str(status), "message": json.dumps(raw, default=str)[:200]}


def make_api_error(raw: Any, status: int, ctx: dict[str, Any], diag: dict[str, Any]) -> UQPayError:
    body = _parse_error_body(raw, status)
    if status == 401:
        return AuthenticationError(body, status, ctx, diag)
    if status == 403:
        return ForbiddenError(body, status, ctx, diag)
    if status == 404:
        return NotFoundError(body, status, ctx, diag)
    if status == 409:
        return ConflictError(body, status, ctx, diag)
    if status == 429:
        return RateLimitError(body, status, ctx, diag)
    if status >= 500:
        return ServerError(body, status, ctx, diag)
    if body["type"] == "idempotency_error":
        return IdempotencyError(body, status, ctx, diag)
    return ValidationError(body, status, ctx, diag)

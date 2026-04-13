from __future__ import annotations
import json
import logging
import sys
import time
import random

_sdk_logger = logging.getLogger(__name__)
from datetime import datetime, timezone
from typing import Any
import httpx
from .auth import TokenManager, _TOKEN_EXPIRED_PATTERNS
from .error import (
    UQPayError, NetworkError,
    RateLimitError, ServerError,
    make_api_error,
)
from .idempotency import generate_idempotency_key, validate_idempotency_key
from .version import SDK_VERSION

_BASE_DELAY_MS = 500
_MAX_DELAY_MS = 30_000
_JITTER_MS = 1_000

_BUILT_IN_REDACT = frozenset({
    "api_key", "auth_token", "x-auth-token", "x-api-key",
    "card_number", "cvc", "cvv", "account_number", "iban",
    "webhook_secret", "id_number", "pan", "pin",
})

# Headers that callers must not override via _extra_headers
_PROTECTED_HEADERS = frozenset({"x-auth-token", "x-idempotency-key"})


def _should_retry(error: Exception, attempt: int, max_retries: int) -> bool:
    if attempt >= max_retries:
        return False
    if isinstance(error, NetworkError):
        return True
    if isinstance(error, (RateLimitError, ServerError)):
        return True
    if isinstance(error, UQPayError):
        if error.http_status == 408:
            return True
        if "request is processing" in error.message.lower():
            return True
    return False


def _compute_delay(attempt: int, retry_after_ms: int | None = None) -> float:
    if retry_after_ms is not None:
        return retry_after_ms / 1000
    base = min(_BASE_DELAY_MS * (2 ** attempt), _MAX_DELAY_MS)
    jitter = random.random() * _JITTER_MS
    return (base + jitter) / 1000


def _parse_retry_after(header: str | None) -> int | None:
    if not header:
        return None
    try:
        return int(header) * 1000
    except ValueError:
        pass
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(header)
        return max(0, int((dt.timestamp() - time.time()) * 1000))
    except Exception:
        return None


def _redact(obj: Any, sensitive_keys: frozenset[str]) -> Any:
    if not isinstance(obj, (dict, list)):
        return obj
    if isinstance(obj, list):
        return [_redact(v, sensitive_keys) for v in obj]
    return {k: "****" if k.lower() in sensitive_keys else _redact(v, sensitive_keys) for k, v in obj.items()}


class HttpClient:
    def __init__(
        self,
        base_url: str,
        token_manager: TokenManager,
        client_id: str,
        log_level: str = "none",
        redact_fields: list[str] | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        self._base_url = base_url
        self._token_manager = token_manager
        self._client_id = client_id
        self._log_level = log_level
        # Pre-normalise to lowercase so _redact() doesn't recompute on every call
        self._sensitive_keys = frozenset(k.lower() for k in (_BUILT_IN_REDACT | frozenset(redact_fields or [])))
        self._timeout = timeout
        self._max_retries = max_retries
        self._environment = "sandbox" if "sandbox" in base_url else "production"
        self._http = httpx.Client(timeout=timeout)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Any = None,
        files: dict[str, Any] | None = None,
        base_url: str | None = None,
        is_auth_endpoint: bool = False,
        request_options: dict[str, Any] | None = None,
        _retry_count: int = 0,
        _token_refreshed: bool = False,
    ) -> Any:
        opts = request_options or {}
        timestamp = datetime.now(timezone.utc).isoformat()

        override_key: str | None = opts.get("idempotency_key")
        if override_key:
            validate_idempotency_key(override_key)
        idempotency_key = override_key or generate_idempotency_key()

        on_behalf_of: str | None = opts.get("on_behalf_of")

        ctx: dict[str, Any] = {
            "method": method,
            "path": path,
            "idempotency_key": idempotency_key,
            "on_behalf_of": on_behalf_of,
            "retry_count": _retry_count,
            "timestamp": timestamp,
        }

        account_ctx = self._token_manager.account_context or {}
        diag: dict[str, Any] = {
            "client_id": self._client_id,
            "environment": self._environment,
            "sdk_version": SDK_VERSION,
            "account_id": account_ctx.get("account_id"),
            "short_account_id": account_ctx.get("short_account_id"),
        }

        python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        user_agent = f"uqpay-python/{SDK_VERSION} python/{python_ver}"

        headers: dict[str, str] = {"User-Agent": user_agent}
        # Only attach idempotency key for mutating requests
        if method.upper() != "GET":
            headers["x-idempotency-key"] = idempotency_key
        if body is not None and not files:
            headers["Content-Type"] = "application/json"
        if not is_auth_endpoint:
            token = self._token_manager.get_token()
            headers["x-auth-token"] = f"Bearer {token}"
        if on_behalf_of:
            headers["x-on-behalf-of"] = on_behalf_of

        # Extra headers from request_options (e.g. x-client-id for payment domain).
        # Protected headers (auth token, idempotency key) cannot be overridden this way.
        for k, v in opts.get("_extra_headers", {}).items():
            if k.lower() in _PROTECTED_HEADERS:
                raise ValueError(f"_extra_headers may not override protected header: {k!r}")
            headers[k] = str(v)

        effective_base = base_url or self._base_url
        url = f"{effective_base}{path}"
        timeout = float(opts.get("timeout", self._timeout))
        max_retries = int(opts.get("max_retries", self._max_retries))

        start = time.monotonic()
        try:
            if files:
                response = self._http.request(
                    method, url, headers=headers, files=files, timeout=timeout
                )
            elif body is not None:
                response = self._http.request(
                    method, url, headers=headers,
                    content=json.dumps(body, default=str),
                    timeout=timeout,
                )
            else:
                response = self._http.request(
                    method, url, headers=headers, timeout=timeout
                )
        except httpx.TimeoutException as exc:
            net_err = NetworkError(f"Request timed out after {timeout}s", ctx, diag)
            net_err.__cause__ = exc
            if not is_auth_endpoint and _should_retry(net_err, _retry_count, max_retries):
                delay = _compute_delay(_retry_count)
                time.sleep(delay)
                return self.request(
                    method, path, body=body, files=files, base_url=base_url,
                    is_auth_endpoint=is_auth_endpoint,
                    request_options={**(request_options or {}), "idempotency_key": idempotency_key},
                    _retry_count=_retry_count + 1, _token_refreshed=_token_refreshed,
                )
            raise net_err from exc
        except httpx.NetworkError as exc:
            net_err = NetworkError(str(exc), ctx, diag)
            net_err.__cause__ = exc
            if not is_auth_endpoint and _should_retry(net_err, _retry_count, max_retries):
                delay = _compute_delay(_retry_count)
                time.sleep(delay)
                return self.request(
                    method, path, body=body, files=files, base_url=base_url,
                    is_auth_endpoint=is_auth_endpoint,
                    request_options={**(request_options or {}), "idempotency_key": idempotency_key},
                    _retry_count=_retry_count + 1, _token_refreshed=_token_refreshed,
                )
            raise net_err from exc

        duration_ms = int((time.monotonic() - start) * 1000)

        # Parse response body
        content_type = response.headers.get("content-type", "")
        raw_body: Any
        if "application/json" in content_type:
            try:
                raw_body = response.json()
            except Exception:
                raw_body = response.text
        else:
            text = response.text
            try:
                raw_body = json.loads(text)
            except Exception:
                raw_body = text

        self._log(
            method, path, response.status_code, duration_ms,
            idempotency_key, account_ctx.get("short_account_id"),
            _retry_count, body, raw_body, on_behalf_of,
        )

        if response.is_success:
            return raw_body

        err = make_api_error(raw_body, response.status_code, ctx, diag)

        # Lock in the idempotency key so all retries reuse the same key.
        # Without this, each recursive call to request() would generate a new UUID,
        # breaking idempotency semantics if the server already processed the request.
        retry_opts = {**(request_options or {}), "idempotency_key": idempotency_key}

        # 401 token retry (once)
        if response.status_code == 401 and not is_auth_endpoint and not _token_refreshed:
            if any(p in err.message.lower() for p in _TOKEN_EXPIRED_PATTERNS):
                self._token_manager.invalidate()
                return self.request(
                    method, path, body=body, files=files, base_url=base_url,
                    is_auth_endpoint=is_auth_endpoint, request_options=retry_opts,
                    _retry_count=_retry_count, _token_refreshed=True,
                )

        # Auto-retry transient errors
        if not is_auth_endpoint and _should_retry(err, _retry_count, max_retries):
            retry_after_ms = _parse_retry_after(response.headers.get("retry-after"))
            delay = _compute_delay(_retry_count, retry_after_ms)
            time.sleep(delay)
            return self.request(
                method, path, body=body, files=files, base_url=base_url,
                is_auth_endpoint=is_auth_endpoint, request_options=retry_opts,
                _retry_count=_retry_count + 1, _token_refreshed=_token_refreshed,
            )

        raise err

    def _log(
        self,
        method: str, path: str, status: int, duration_ms: int,
        idempotency_key: str, short_account_id: str | None,
        retry_count: int, req_body: Any, resp_body: Any,
        on_behalf_of: str | None,
    ) -> None:
        if self._log_level == "none":
            return
        is_error = status >= 400
        if self._log_level == "error" and not is_error:
            return
        if self._log_level == "warn" and not is_error:
            return

        acct = f" [acct: {short_account_id}]" if short_account_id else ""
        if self._log_level in ("error", "warn", "info"):
            _sdk_logger.info("[UQPAY] %s %s → %s [idem: %s]%s (%dms)",
                             method, path, status, idempotency_key, acct, duration_ms)
            return
        # debug
        retry = f" [retry: {retry_count}]" if retry_count > 0 else ""
        behalf = f" [on-behalf: {on_behalf_of}]" if on_behalf_of else ""
        req_str = f" body: {json.dumps(_redact(req_body, self._sensitive_keys), default=str)[:500]}" if req_body else ""
        resp_str = f" resp: {json.dumps(_redact(resp_body, self._sensitive_keys), default=str)[:500]}" if resp_body else ""
        _sdk_logger.debug("[UQPAY] %s %s → %s [idem: %s]%s%s%s (%dms)%s%s",
                          method, path, status, idempotency_key, acct, retry, behalf, duration_ms, req_str, resp_str)

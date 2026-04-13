from __future__ import annotations
from typing import Any
from ..http import HttpClient


class BaseResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def _get(self, path: str, request_options: dict[str, Any] | None = None) -> Any:
        return self._http.request("GET", path, request_options=request_options)

    def _post(self, path: str, body: Any, request_options: dict[str, Any] | None = None) -> Any:
        return self._http.request("POST", path, body=body, request_options=request_options)

    def _patch(self, path: str, body: Any, request_options: dict[str, Any] | None = None) -> Any:
        return self._http.request("PATCH", path, body=body, request_options=request_options)

    def _put(self, path: str, body: Any, request_options: dict[str, Any] | None = None) -> Any:
        return self._http.request("PUT", path, body=body, request_options=request_options)

    def _delete(self, path: str, request_options: dict[str, Any] | None = None) -> Any:
        return self._http.request("DELETE", path, request_options=request_options)

    def _qs(self, params: dict[str, Any]) -> str:
        """Serialize a dict to a URL query string, omitting None values."""
        from urllib.parse import urlencode
        filtered = {k: v for k, v in params.items() if v is not None}
        if not filtered:
            return ""
        # Convert lists to repeated keys
        parts: list[tuple[str, str]] = []
        for k, v in filtered.items():
            if isinstance(v, list):
                for item in v:
                    parts.append((k, str(item)))
            else:
                parts.append((k, str(v)))
        return "?" + urlencode(parts) if parts else ""

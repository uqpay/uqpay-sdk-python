from __future__ import annotations
from typing import Any
from ..base import BaseResource
from ...http import HttpClient


class PaymentBaseResource(BaseResource):
    """Base for all Payment-domain resources — injects x-client-id on every call."""

    def __init__(self, http: HttpClient, client_id: str) -> None:
        super().__init__(http)
        self._client_id = client_id

    def _with_client_id(self, request_options: dict[str, Any] | None) -> dict[str, Any]:
        opts = dict(request_options or {})
        extra = dict(opts.get("_extra_headers", {}))
        extra["x-client-id"] = self._client_id
        opts["_extra_headers"] = extra
        return opts

    def _get(self, path: str, request_options: dict[str, Any] | None = None) -> Any:
        return super()._get(path, self._with_client_id(request_options))

    def _post(self, path: str, body: Any, request_options: dict[str, Any] | None = None) -> Any:
        return super()._post(path, body, self._with_client_id(request_options))

    def _patch(self, path: str, body: Any, request_options: dict[str, Any] | None = None) -> Any:
        return super()._patch(path, body, self._with_client_id(request_options))

    def _put(self, path: str, body: Any, request_options: dict[str, Any] | None = None) -> Any:
        return super()._put(path, body, self._with_client_id(request_options))

    def _delete(self, path: str, request_options: dict[str, Any] | None = None) -> Any:
        return super()._delete(path, self._with_client_id(request_options))

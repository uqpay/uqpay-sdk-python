from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.connect import CreateAccountParams
    from ...types import RequestOptions


class AccountsResource(BaseResource):
    def create(
        self,
        params: CreateAccountParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/accounts", params, request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/accounts/{id}", request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/accounts{self._qs(params or {})}", request_options)

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.banking import CreateVirtualAccountParams, ListVirtualAccountsParams
    from ...types import RequestOptions


class VirtualAccountsResource(BaseResource):
    def create(
        self,
        params: CreateVirtualAccountParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/virtual/accounts", params, request_options)

    def list(
        self,
        params: ListVirtualAccountsParams | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/virtual/accounts{self._qs(params or {})}", request_options)

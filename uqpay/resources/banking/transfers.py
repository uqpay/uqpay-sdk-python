from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.banking import CreateTransferParams
    from ...types import RequestOptions


class BankingTransfersResource(BaseResource):
    def create(
        self,
        params: CreateTransferParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/transfer", params, request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/transfer{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/transfer/{id}", request_options)

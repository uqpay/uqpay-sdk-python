from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.issuing import CreateCardholderParams, UpdateCardholderParams
    from ...types import RequestOptions


class CardholdersResource(BaseResource):
    def create(
        self,
        params: CreateCardholderParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/issuing/cardholders", params, request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/issuing/cardholders{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/issuing/cardholders/{id}", request_options)

    def update(
        self,
        id: str,
        params: UpdateCardholderParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v1/issuing/cardholders/{id}", params, request_options)

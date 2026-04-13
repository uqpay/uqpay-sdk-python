from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types import RequestOptions


class IssuingBalancesResource(BaseResource):
    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/issuing/balances{self._qs(params or {})}", request_options)

    def retrieve(
        self,
        currency: str,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        # Unusual: retrieve uses POST with currency in body
        return self._post("/v1/issuing/balances", {"currency": currency}, request_options)

    def list_transactions(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/issuing/balances/transactions{self._qs(params or {})}", request_options)

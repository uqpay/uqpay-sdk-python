from __future__ import annotations
from typing import Any
from ..base import BaseResource


class BankingBalancesResource(BaseResource):
    def list(self, params: dict[str, Any] | None = None, request_options: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get(f"/v1/balances{self._qs(params or {})}", request_options)

    def retrieve(self, currency: str, request_options: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get(f"/v1/balances/{currency}", request_options)

    def list_transactions(self, params: dict[str, Any] | None = None, request_options: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get(f"/v1/balances/transactions{self._qs(params or {})}", request_options)

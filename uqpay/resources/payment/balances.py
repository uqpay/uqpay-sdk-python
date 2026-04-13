from __future__ import annotations
from typing import Any
from .base import PaymentBaseResource


class PaymentBalancesResource(PaymentBaseResource):
    def list(self, params: dict[str, Any] | None = None, request_options: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get(f"/v2/payment/balances{self._qs(params or {})}", request_options)

    def retrieve(self, currency: str, request_options: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get(f"/v2/payment/balances/{currency}", request_options)

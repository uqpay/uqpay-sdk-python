from __future__ import annotations
from typing import Any
from ..base import BaseResource


class PaymentMethodsResource(BaseResource):
    def list(self, params: dict[str, Any] | None = None, request_options: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get(f"/v1/beneficiaries/paymentmethods{self._qs(params or {})}", request_options)

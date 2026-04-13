from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import PaymentBaseResource

if TYPE_CHECKING:
    from ...types.payment import CreatePayoutParams
    from ...types import RequestOptions


class PaymentPayoutsResource(PaymentBaseResource):
    def create(
        self,
        params: CreatePayoutParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v2/payment/payout/create", params, request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v2/payment/payout{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v2/payment/payout/{id}", request_options)

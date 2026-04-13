from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import PaymentBaseResource

if TYPE_CHECKING:
    from ...types.payment import ListPaymentAttemptsParams
    from ...types import RequestOptions


class PaymentAttemptsResource(PaymentBaseResource):
    def list(
        self,
        params: ListPaymentAttemptsParams | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v2/payment/payment_attempts{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v2/payment/payment_attempts/{id}", request_options)

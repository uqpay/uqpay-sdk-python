from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import PaymentBaseResource

if TYPE_CHECKING:
    from ...types.payment import CreateRefundParams, ListRefundsParams
    from ...types import RequestOptions


class RefundsResource(PaymentBaseResource):
    def create(
        self,
        params: CreateRefundParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v2/payment/refunds", params, request_options)

    def list(
        self,
        params: ListRefundsParams | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v2/payment/refunds{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v2/payment/refunds/{id}", request_options)

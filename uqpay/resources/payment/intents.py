from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import PaymentBaseResource

if TYPE_CHECKING:
    from ...types.payment import (
        CreatePaymentIntentParams,
        UpdatePaymentIntentParams,
        ConfirmPaymentIntentParams,
        CapturePaymentIntentParams,
        CancelPaymentIntentParams,
    )
    from ...types import RequestOptions


class PaymentIntentsResource(PaymentBaseResource):
    def create(
        self,
        params: CreatePaymentIntentParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v2/payment_intents/create", params, request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v2/payment_intents{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v2/payment_intents/{id}", request_options)

    def update(
        self,
        id: str,
        params: UpdatePaymentIntentParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v2/payment_intents/{id}", params, request_options)

    def confirm(
        self,
        id: str,
        params: ConfirmPaymentIntentParams | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v2/payment_intents/{id}/confirm", params or {}, request_options)

    def capture(
        self,
        id: str,
        params: CapturePaymentIntentParams | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v2/payment_intents/{id}/capture", params or {}, request_options)

    def cancel(
        self,
        id: str,
        params: CancelPaymentIntentParams | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v2/payment_intents/{id}/cancel", params or {}, request_options)

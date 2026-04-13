from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import PaymentBaseResource

if TYPE_CHECKING:
    from ...types.payment import CreateBankAccountParams, UpdateBankAccountParams
    from ...types import RequestOptions


class BankAccountsResource(PaymentBaseResource):
    def create(
        self,
        params: CreateBankAccountParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v2/payment/bankaccount/create", params, request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v2/payment/bankaccount{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v2/payment/bankaccount/{id}", request_options)

    def update(
        self,
        id: str,
        params: UpdateBankAccountParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v2/payment/bankaccount/{id}", params, request_options)

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.banking import (
        CheckBeneficiaryParams,
        CreateBeneficiaryParams,
        UpdateBeneficiaryParams,
    )
    from ...types import RequestOptions


class BeneficiariesResource(BaseResource):
    def create(
        self,
        params: CreateBeneficiaryParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/beneficiaries", params, request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/beneficiaries{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/beneficiaries/{id}", request_options)

    def update(
        self,
        id: str,
        params: UpdateBeneficiaryParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v1/beneficiaries/{id}", params, request_options)

    def delete(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._post(f"/v1/beneficiaries/{id}/delete", {}, request_options)

    def check(
        self,
        params: CheckBeneficiaryParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/beneficiaries/check", params, request_options)

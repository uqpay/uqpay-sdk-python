from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.banking import CreateConversionParams, CreateQuoteParams, ListCurrentRatesParams
    from ...types import RequestOptions


class ConversionsResource(BaseResource):
    def create_quote(
        self,
        params: CreateQuoteParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/conversion/quote", params, request_options)

    def create(
        self,
        params: CreateConversionParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/conversion", params, request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/conversion{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/conversion/{id}", request_options)

    def list_dates(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/conversion/conversion_dates{self._qs(params or {})}", request_options)

    def list_current_rates(
        self,
        params: ListCurrentRatesParams | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        path = "/v1/exchange/rates"
        if params and params.get("currency_pairs"):
            path = f"{path}?currency_pairs={params['currency_pairs']}"
        return self._get(path, request_options)

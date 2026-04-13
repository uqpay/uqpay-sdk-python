from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.issuing import CreateIssuingTransferParams
    from ...types import RequestOptions


class IssuingTransfersResource(BaseResource):
    def create(
        self,
        params: CreateIssuingTransferParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/issuing/transfers", params, request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/issuing/transfers/{id}", request_options)

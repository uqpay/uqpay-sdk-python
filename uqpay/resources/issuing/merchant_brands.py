from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types import RequestOptions
    from ...types.issuing import ListMerchantBrandsParams


class MerchantBrandsResource(BaseResource):
    def list(
        self, params: ListMerchantBrandsParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/issuing/merchant_brands{self._qs(params)}", request_options)

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.connect import CreateSubAccountParams
    from ...types import RequestOptions


class SubAccountsResource(BaseResource):
    def create(
        self,
        params: CreateSubAccountParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/accounts/create_accounts", params, request_options)

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types.issuing import CreateReportParams
    from ...types import RequestOptions


class ReportsResource(BaseResource):
    def create(
        self,
        params: CreateReportParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/issuing/reports", params, request_options)

    def download(self, id: str, request_options: RequestOptions | None = None) -> Any:
        """Download report file. Returns the raw response content (bytes, str, or dict depending on server content-type)."""
        return self._get(f"/v1/issuing/reports/{id}", request_options)

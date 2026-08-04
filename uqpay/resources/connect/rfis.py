from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource

if TYPE_CHECKING:
    from ...types import RequestOptions
    from ...types.connect import AnswerRfiParams, ListRfisParams


class RfisResource(BaseResource):
    def list(
        self,
        params: ListRfisParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/rfis{self._qs(params)}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/rfis/{id}", request_options)

    def answer(
        self,
        params: AnswerRfiParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/rfis/answer", params, request_options)

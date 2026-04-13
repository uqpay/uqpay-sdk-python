from __future__ import annotations
from typing import Any
from ..base import BaseResource


class AdditionalDocsResource(BaseResource):
    def get(self, params: dict[str, Any] | None = None, request_options: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        return self._get(f"/v1/accounts/get_additional{self._qs(params or {})}", request_options)

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import PaymentBaseResource

if TYPE_CHECKING:
    from ...types import RequestOptions
    from ...types.payment import GetPinKeyParams, RegisterTerminalParams


class TerminalsResource(PaymentBaseResource):
    def register(
        self, params: RegisterTerminalParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v2/terminal/register", params, request_options)

    def get_pin_key(
        self, params: GetPinKeyParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v2/terminal/getPinKey", params, request_options)

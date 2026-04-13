from __future__ import annotations
import json as _json
from typing import Any, TYPE_CHECKING
from urllib.parse import urlencode
from ..base import BaseResource
from ...http import HttpClient

if TYPE_CHECKING:
    from ...types.issuing import (
        CreateCardParams,
        UpdateCardParams,
        UpdateCardStatusParams,
        ActivateCardParams,
        AssignCardParams,
        ResetPinParams,
        CardRechargeParams,
        CardWithdrawParams,
    )
    from ...types import RequestOptions

_SANDBOX_IFRAME_BASE = "https://embedded-sandbox.uqpaytech.com"
_PROD_IFRAME_BASE = "https://embedded.uqpay.com"


class CardsResource(BaseResource):
    def __init__(self, http: HttpClient, base_url: str) -> None:
        super().__init__(http)
        self._iframe_base = _SANDBOX_IFRAME_BASE if "sandbox" in base_url else _PROD_IFRAME_BASE

    def create(
        self,
        params: CreateCardParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/issuing/cards", params, request_options)

    def list(
        self,
        params: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._get(f"/v1/issuing/cards{self._qs(params or {})}", request_options)

    def retrieve(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/issuing/cards/{id}", request_options)

    def update(
        self,
        id: str,
        params: UpdateCardParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v1/issuing/cards/{id}", params, request_options)

    def update_status(
        self,
        id: str,
        params: UpdateCardStatusParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v1/issuing/cards/{id}/status", params, request_options)

    def activate(
        self,
        params: ActivateCardParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/issuing/cards/activate", params, request_options)

    def assign(
        self,
        params: AssignCardParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/issuing/cards/assign", params, request_options)

    def reset_pin(
        self,
        params: ResetPinParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post("/v1/issuing/cards/pin", params, request_options)

    def retrieve_order(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/issuing/cards/{id}/order", request_options)

    def retrieve_secure(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._get(f"/v1/issuing/cards/{id}/secure", request_options)

    def create_pan_token(self, id: str, request_options: RequestOptions | None = None) -> dict[str, Any]:
        return self._post(f"/v1/issuing/cards/{id}/token", {}, request_options)

    def get_secure_iframe_url(
        self,
        id: str,
        lang: str | None = None,
        styles: dict[str, Any] | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        result = self.create_pan_token(id, request_options)
        token = result["token"]
        qs_params: dict[str, str] = {"token": token, "cardId": id}
        if lang:
            qs_params["lang"] = lang
        if styles:
            qs_params["styles"] = _json.dumps(styles)
        iframe_url = f"{self._iframe_base}/iframe/card?{urlencode(qs_params)}"
        return {"iframe_url": iframe_url, **result}

    def recharge(
        self,
        id: str,
        params: CardRechargeParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v1/issuing/cards/{id}/recharge", params, request_options)

    def withdraw(
        self,
        id: str,
        params: CardWithdrawParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        return self._post(f"/v1/issuing/cards/{id}/withdraw", params, request_options)

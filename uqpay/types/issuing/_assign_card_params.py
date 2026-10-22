from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class AssignCardParamsMetadata(TypedDict):
    # Personal Visa SKU code: exactly 12 characters, validated by the server.
    card_sku_code: str


class AssignCardParams(TypedDict, total=False):
    cardholder_id: NotRequired[str]
    card_number: Required[str]
    card_currency: Required[str]
    card_mode: Required[Literal["SINGLE", "SHARE"]]
    # Required for Personal Visa; omit metadata for other card products.
    metadata: NotRequired[AssignCardParamsMetadata]

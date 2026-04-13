from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreateConversionParams(TypedDict, total=False):
    quote_id: Required[str]
    sell_currency: Required[str]
    sell_amount: NotRequired[str]
    buy_currency: Required[str]
    buy_amount: NotRequired[str]
    conversion_date: Required[str]

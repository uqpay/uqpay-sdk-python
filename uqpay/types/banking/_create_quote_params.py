from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreateQuoteParams(TypedDict, total=False):
    sell_currency: Required[str]
    sell_amount: NotRequired[str]
    buy_currency: Required[str]
    buy_amount: NotRequired[str]
    conversion_date: Required[str]
    transaction_type: NotRequired[Literal["conversion", "payout"]]

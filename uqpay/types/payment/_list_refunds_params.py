from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class ListRefundsParams(TypedDict, total=False):
    payment_intent_id: NotRequired[str]
    merchant_order_id: NotRequired[str]

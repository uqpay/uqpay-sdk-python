from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class ActivateCardParams(TypedDict, total=False):
    card_id: Required[str]
    activation_code: Required[str]
    pin: Required[str]
    no_pin_payment_amount: NotRequired[float]

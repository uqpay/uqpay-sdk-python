from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class AssignCardParams(TypedDict, total=False):
    cardholder_id: Required[str]
    card_number: Required[str]
    card_currency: Required[str]
    card_mode: Required[Literal["SINGLE", "SHARE"]]

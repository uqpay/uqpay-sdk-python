from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CardWithdrawParams(TypedDict, total=False):
    amount: Required[float]

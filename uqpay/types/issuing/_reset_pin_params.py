from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class ResetPinParams(TypedDict, total=False):
    card_id: Required[str]
    pin: Required[str]

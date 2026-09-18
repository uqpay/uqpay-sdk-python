from __future__ import annotations
from typing import Literal
from typing_extensions import NotRequired, Required, TypedDict


class ResetPinParams(TypedDict, total=False):
    card_id: Required[str]
    pin: Required[str]
    # Omitted means SET. old_pin is six digits, required only for UPDATE.
    type: NotRequired[Literal["SET", "RESET", "UPDATE"]]
    old_pin: NotRequired[str]

from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class UpdateCardStatusParams(TypedDict, total=False):
    card_status: Required[Literal["ACTIVE", "FROZEN", "CANCELLED"]]
    update_reason: NotRequired[str]

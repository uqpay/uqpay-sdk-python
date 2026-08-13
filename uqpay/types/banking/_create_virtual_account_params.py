from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreateVirtualAccountParams(TypedDict, total=False):
    country: Required[str]
    currency: Required[str]
    payment_method: NotRequired[Literal["LOCAL", "SWIFT", ""] | None]
    nickname: NotRequired[str | None]

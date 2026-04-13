from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreateVirtualAccountParams(TypedDict, total=False):
    currency: Required[str]
    payment_method: NotRequired[Literal["LOCAL", "SWIFT"]]

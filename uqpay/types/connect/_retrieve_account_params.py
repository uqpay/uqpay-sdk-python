from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class RetrieveAccountParams(TypedDict, total=False):
    business_code: NotRequired[Literal["BANKING", "ACQUIRING", "ISSUING"]]

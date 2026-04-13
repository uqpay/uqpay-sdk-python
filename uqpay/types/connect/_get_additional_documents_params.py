from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class GetAdditionalDocumentsParams(TypedDict, total=False):
    country: Required[str]
    business_code: Required[Literal["BANKING", "ACQUIRING"]]

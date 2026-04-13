from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class RetrieveIssuingBalanceParams(TypedDict, total=False):
    currency: Required[str]

from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class ListCurrentRatesParams(TypedDict, total=False):
    currency_pairs: NotRequired[str]

from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class ListVirtualAccountsParams(TypedDict, total=False):
    currency: NotRequired[str]

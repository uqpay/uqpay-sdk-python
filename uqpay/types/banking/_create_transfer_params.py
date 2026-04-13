from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreateTransferParams(TypedDict, total=False):
    source_account_id: Required[str]
    target_account_id: Required[str]
    currency: Required[str]
    amount: Required[str]
    reason: Required[str]

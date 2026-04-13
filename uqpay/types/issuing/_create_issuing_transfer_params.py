from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreateIssuingTransferParams(TypedDict, total=False):
    source_account_id: Required[str]
    destination_account_id: Required[str]
    currency: Required[str]
    amount: Required[float]
    remark: NotRequired[str]

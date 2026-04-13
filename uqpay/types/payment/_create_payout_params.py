from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreatePayoutParams(TypedDict, total=False):
    payout_currency: Required[str]
    payout_amount: Required[str]
    internal_note: NotRequired[str]
    statement_descriptor: Required[str]
    payout_account_id: NotRequired[str]

from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class SimulateDepositCreationParams(TypedDict, total=False):
    amount: Required[float]
    currency: Required[str]
    receiver_account_number: NotRequired[str]
    sender_swift_code: Required[str]
    sender_account_number: NotRequired[str]
    sender_country: NotRequired[str]
    sender_name: NotRequired[str]

from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class SimulateAuthorizationParams(TypedDict, total=False):
    card_id: Required[str]
    transaction_amount: Required[float]
    transaction_currency: Required[str]
    merchant_name: Required[str]
    merchant_category_code: Required[str]

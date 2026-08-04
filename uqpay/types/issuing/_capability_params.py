from __future__ import annotations
from typing import Literal
from typing_extensions import NotRequired, TypedDict


class ElevateLimitParams(TypedDict):
    limit_amount: float
    duration_in_days: NotRequired[int]


class EnrollNetworkProtectionParams(TypedDict):
    risk_control: Literal["network_protection"]
    action_code: str


class RemoveNetworkProtectionParams(TypedDict):
    risk_control: Literal["network_protection"]


class ManageCardPinParams(TypedDict):
    card_id: str
    type: Literal["SET", "RESET"]
    pin: str
    old_pin: NotRequired[str]


class SetDefaultCardArtParams(TypedDict):
    card_art_id: str


class ListMerchantBrandsParams(TypedDict):
    page_size: int
    page_number: int
    display_name: NotRequired[str]
    merchant_code: NotRequired[str]


class ClaimUnsolicitedRefundParams(TypedDict):
    related_transaction_id: str
    remark: NotRequired[str]

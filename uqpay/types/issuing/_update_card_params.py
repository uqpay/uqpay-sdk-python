from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class UpdateCardParamsSpendingControls(TypedDict, total=False):
    amount: Required[float]
    interval: Required[Literal["PER_TRANSACTION"]]


class UpdateCardParamsRiskControls(TypedDict, total=False):
    allow_3ds_transactions: NotRequired[Literal["Y", "N"]]
    allowed_mcc: NotRequired[list[str]]
    blocked_mcc: NotRequired[list[str]]


class UpdateCardParamsMetadata(TypedDict, total=False):
    pass


class UpdateCardParams(TypedDict, total=False):
    # Card and processing status must be ACTIVE; art changes are asynchronous.
    card_art_id: NotRequired[str]
    name_on_card: NotRequired[str]
    card_limit: NotRequired[float]
    no_pin_payment_amount: NotRequired[float]
    spending_controls: NotRequired[list[UpdateCardParamsSpendingControls]]
    risk_controls: NotRequired[UpdateCardParamsRiskControls]
    metadata: NotRequired[UpdateCardParamsMetadata]

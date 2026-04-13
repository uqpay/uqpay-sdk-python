from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreateRefundParamsMetadata(TypedDict, total=False):
    pass


class CreateRefundParams(TypedDict, total=False):
    payment_intent_id: Required[str]
    payment_attempt_id: NotRequired[str]
    amount: Required[str]
    reason: Required[str]
    metadata: NotRequired[CreateRefundParamsMetadata]

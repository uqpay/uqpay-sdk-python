from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CancelPaymentIntentParams(TypedDict, total=False):
    cancellation_reason: NotRequired[str]

from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CapturePaymentIntentParams(TypedDict, total=False):
    amount_to_capture: NotRequired[float]

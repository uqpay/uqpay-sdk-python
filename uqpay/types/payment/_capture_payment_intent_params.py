from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CapturePaymentIntentParams(TypedDict, total=False):
    amount_to_capture: NotRequired[str]
    merchant_capture_order_id: NotRequired[str]
    final_capture: NotRequired[Literal[True]]

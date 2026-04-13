from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class ListPaymentAttemptsParams(TypedDict, total=False):
    payment_intent_id: NotRequired[str]
    attempt_status: NotRequired[Literal["INITIATED", "AUTHENTICATION_REDIRECTED", "PENDING_AUTHORIZATION", "AUTHORIZED", "CAPTURE_REQUESTED", "SETTLED", "SUCCEEDED", "CANCELLED", "EXPIRED", "FAILED"]]

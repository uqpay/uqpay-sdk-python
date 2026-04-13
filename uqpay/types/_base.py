from __future__ import annotations
from typing_extensions import NotRequired, TypedDict


class RequestOptions(TypedDict, total=False):
    idempotency_key: NotRequired[str]
    on_behalf_of: NotRequired[str]
    timeout: NotRequired[float]
    max_retries: NotRequired[int]

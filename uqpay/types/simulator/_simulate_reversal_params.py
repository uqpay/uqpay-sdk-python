from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class SimulateReversalParams(TypedDict, total=False):
    transaction_id: Required[str]

from __future__ import annotations
from typing import Literal
from typing_extensions import TypedDict


class RegisterTerminalParams(TypedDict):
    firm_code: Literal["01", "02", "03", "04", "05"]
    firm_sn: str
    terminal_model: str


class GetPinKeyParams(TypedDict):
    terminal_id: str
    prv_key: str

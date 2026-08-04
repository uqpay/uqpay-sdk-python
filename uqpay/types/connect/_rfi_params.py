from __future__ import annotations
from typing import Literal
from typing_extensions import NotRequired, TypedDict


RfiStatus = Literal["SUBMITTED_PENDING", "REJECTED", "APPROVED", "ACTION_REQUIRED"]


class ListRfisParams(TypedDict):
    page_size: int
    page_number: int
    status: NotRequired[RfiStatus]


class RfiAnswerItem(TypedDict):
    key: str
    type: Literal["ATTACHMENT"]
    attachments: list[str]


class AnswerRfiParams(TypedDict):
    rfi_id: str
    answer: list[RfiAnswerItem]

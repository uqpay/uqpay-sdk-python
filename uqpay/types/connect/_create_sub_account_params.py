from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreateSubAccountParams(TypedDict, total=False):
    entity_type: NotRequired[str]

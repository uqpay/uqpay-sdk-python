from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreateAccountParams(TypedDict, total=False):
    entity_type: NotRequired[str]

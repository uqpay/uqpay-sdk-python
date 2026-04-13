from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreateBeneficiaryParams(TypedDict, total=False):
    entity_type: NotRequired[str]

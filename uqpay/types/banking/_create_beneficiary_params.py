from __future__ import annotations
from typing import Any
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreateBeneficiaryParams(TypedDict, total=False):
    entity_type: Required[Literal["INDIVIDUAL", "COMPANY"]]
    payment_method: Required[Literal["LOCAL", "SWIFT", "CARD"]]
    bank_details: Required[dict[str, Any]]
    address: NotRequired[dict[str, Any]]
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    company_name: NotRequired[str]
    email: NotRequired[str]
    nickname: NotRequired[str]
    id_number: NotRequired[str]
    additional_info: NotRequired[dict[str, Any]]

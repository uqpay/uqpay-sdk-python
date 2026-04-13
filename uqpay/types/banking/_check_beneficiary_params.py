from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CheckBeneficiaryParamsAdditionalInfo(TypedDict, total=False):
    proxy_id: NotRequired[str]


class CheckBeneficiaryParams(TypedDict, total=False):
    entity_type: Required[Literal["COMPANY", "INDIVIDUAL"]]
    account_number: Required[str]
    payment_method: Required[Literal["LOCAL", "SWIFT"]]
    currency: Required[str]
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    company_name: NotRequired[str]
    clearing_system: NotRequired[Literal["LOCAL", "SWIFT", "ACH", "FAST", "MEPS", "GIRO", "Fedwire", "Faster Payments", "RTGS", "FPS", "EFT", "Interac e-Transfer", "Bill Payment", "CHAPS", "Bank Transfer", "NPP", "ACH", "Fedwire", "SWIFT", "FAST", "GIRO", "RTGS", "LOCAL", "FPS", "EFT", "Interac e-Transfer", "Bill Payment", "Faster Payments", "CHAPS", "Bank Transfer", "NPP", "BPAY", "BPAY"]]
    iban: NotRequired[str]
    additional_info: NotRequired[CheckBeneficiaryParamsAdditionalInfo]

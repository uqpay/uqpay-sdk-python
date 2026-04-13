from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreatePayoutParamsBeneficiaryBankDetails(TypedDict, total=False):
    bank_name: Required[str]
    bank_address: Required[str]
    bank_country_code: Required[str]
    account_holder: Required[str]
    account_currency_code: Required[str]
    account_number: NotRequired[str]
    iban: NotRequired[str]
    swift_code: Required[str]
    clearing_system: Required[str]
    routing_code_type1: NotRequired[str]
    routing_code_value1: NotRequired[str]
    routing_code_type2: NotRequired[str]
    routing_code_value2: NotRequired[str]


class CreatePayoutParamsBeneficiaryAddress(TypedDict, total=False):
    country: Required[str]
    nationality: NotRequired[str]
    city: Required[str]
    street_address: Required[str]
    postal_code: Required[str]
    state: Required[str]


class CreatePayoutParamsBeneficiaryAdditionalInfo(TypedDict, total=False):
    organization_code: NotRequired[str]
    proxy_id: NotRequired[str]
    id_type: NotRequired[Literal["PASSPORT", "NATIONAL_ID", "DRIVERS_LICENSE"]]
    id_number: NotRequired[str]
    tax_id: NotRequired[str]
    msisdn: NotRequired[str]


class CreatePayoutParamsBeneficiary(TypedDict, total=False):
    email: NotRequired[str]
    entity_type: Required[str]
    company_name: Required[str]
    payment_method: Required[Literal["LOCAL", "SWIFT"]]
    nickname: NotRequired[str]
    bank_details: Required[CreatePayoutParamsBeneficiaryBankDetails]
    address: Required[CreatePayoutParamsBeneficiaryAddress]
    additional_info: NotRequired[CreatePayoutParamsBeneficiaryAdditionalInfo]


class CreatePayoutParamsDocumentation(TypedDict, total=False):
    file: NotRequired[str]
    file_id: NotRequired[str]


class CreatePayoutParams(TypedDict, total=False):
    currency: Required[str]
    amount: Required[str]
    quote_id: NotRequired[str]
    payout_currency: NotRequired[str]
    payout_amount: NotRequired[float]
    purpose_code: Required[str]
    payout_reference: Required[str]
    fee_paid_by: Required[Literal["SHARED", "OURS"]]
    payout_date: Required[str]
    beneficiary_id: NotRequired[str]
    beneficiary: NotRequired[CreatePayoutParamsBeneficiary]
    is_payer: NotRequired[str]
    payer_id: NotRequired[str]
    documentation: NotRequired[list[CreatePayoutParamsDocumentation]]

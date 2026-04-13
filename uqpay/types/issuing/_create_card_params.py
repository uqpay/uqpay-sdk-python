from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreateCardParamsSpendingControls(TypedDict, total=False):
    amount: Required[float]
    interval: Required[Literal["PER_TRANSACTION"]]


class CreateCardParamsRiskControls(TypedDict, total=False):
    allow_3ds_transactions: NotRequired[Literal["Y", "N"]]
    allowed_mcc: NotRequired[list[str]]
    blocked_mcc: NotRequired[list[str]]


class CreateCardParamsMetadata(TypedDict, total=False):
    pass


class CreateCardParamsCardholderRequiredFieldsResidentialAddress(TypedDict, total=False):
    country: Required[str]
    state: NotRequired[str]
    city: Required[str]
    district: NotRequired[str]
    line1: Required[str]
    line2: NotRequired[str]
    line_en: NotRequired[str]
    postal_code: NotRequired[str]


class CreateCardParamsCardholderRequiredFieldsIdentity(TypedDict, total=False):
    type: Required[Literal["ID_CARD", "PASSPORT"]]
    number: Required[str]
    front_file: Required[str]
    back_file: NotRequired[str]
    hand_file: NotRequired[str]


class CreateCardParamsCardholderRequiredFieldsKycVerificationKycProof(TypedDict, total=False):
    provider: Required[str]
    reference_id: Required[str]


class CreateCardParamsCardholderRequiredFieldsKycVerification(TypedDict, total=False):
    method: Required[Literal["THIRD_PARTY", "SUMSUB_REDIRECT"]]
    kyc_proof: NotRequired[CreateCardParamsCardholderRequiredFieldsKycVerificationKycProof]


class CreateCardParamsCardholderRequiredFields(TypedDict, total=False):
    gender: NotRequired[Literal["MALE", "FEMALE"]]
    nationality: NotRequired[str]
    phone_number: NotRequired[str]
    date_of_birth: NotRequired[str]
    residential_address: NotRequired[CreateCardParamsCardholderRequiredFieldsResidentialAddress]
    identity: NotRequired[CreateCardParamsCardholderRequiredFieldsIdentity]
    kyc_verification: NotRequired[CreateCardParamsCardholderRequiredFieldsKycVerification]


class CreateCardParams(TypedDict, total=False):
    card_limit: NotRequired[float]
    card_currency: Required[Literal["SGD", "USD"]]
    cardholder_id: Required[str]
    card_product_id: Required[str]
    spending_controls: NotRequired[list[CreateCardParamsSpendingControls]]
    risk_controls: NotRequired[CreateCardParamsRiskControls]
    metadata: NotRequired[CreateCardParamsMetadata]
    usage_type: NotRequired[Literal["NORMAL", "ONE_TIME"]]
    auto_cancel_trigger: NotRequired[Literal["ON_AUTH", "ON_CAPTURE"]]
    expiry_at: NotRequired[str]
    cardholder_required_fields: NotRequired[CreateCardParamsCardholderRequiredFields]

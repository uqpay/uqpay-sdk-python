from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreateCardholderParamsResidentialAddress(TypedDict, total=False):
    country: Required[str]
    state: NotRequired[str]
    city: Required[str]
    district: NotRequired[str]
    line1: Required[str]
    line2: NotRequired[str]
    line_en: NotRequired[str]
    postal_code: NotRequired[str]


class CreateCardholderParamsIdentity(TypedDict, total=False):
    type: Required[Literal["ID_CARD", "PASSPORT"]]
    number: Required[str]
    front_file: Required[str]
    back_file: NotRequired[str]
    hand_file: NotRequired[str]


class CreateCardholderParamsKycVerificationKycProof(TypedDict, total=False):
    provider: Required[str]
    reference_id: Required[str]


class CreateCardholderParamsKycVerification(TypedDict, total=False):
    method: Required[Literal["THIRD_PARTY", "SUMSUB_REDIRECT"]]
    kyc_proof: NotRequired[CreateCardholderParamsKycVerificationKycProof]


class CreateCardholderParams(TypedDict, total=False):
    email: Required[str]
    first_name: Required[str]
    last_name: Required[str]
    date_of_birth: NotRequired[str]
    country_code: Required[str]
    phone_number: Required[str]
    gender: NotRequired[Literal["MALE", "FEMALE"]]
    nationality: NotRequired[str]
    residential_address: NotRequired[CreateCardholderParamsResidentialAddress]
    identity: NotRequired[CreateCardholderParamsIdentity]
    kyc_verification: NotRequired[CreateCardholderParamsKycVerification]
    document_type: NotRequired[Literal["pdf", "png", "jpg", "jpeg"]]
    document: NotRequired[str]

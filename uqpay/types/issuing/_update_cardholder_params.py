from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class UpdateCardholderParamsResidentialAddress(TypedDict, total=False):
    country: Required[str]
    state: NotRequired[str]
    city: Required[str]
    district: NotRequired[str]
    line1: Required[str]
    line2: NotRequired[str]
    line_en: NotRequired[str]
    postal_code: NotRequired[str]


class UpdateCardholderParamsIdentity(TypedDict, total=False):
    type: NotRequired[Literal["ID_CARD", "PASSPORT"]]
    number: NotRequired[str]
    front_file: NotRequired[str]
    back_file: NotRequired[str]
    hand_file: NotRequired[str]
    # Omitted, empty or null file values preserve saved supporting materials.
    proof_of_address: NotRequired[str | None]
    proof_of_address_issue_date: NotRequired[str]
    proof_of_address_issuing_country: NotRequired[str]
    identity_verification: NotRequired[str | None]


class UpdateCardholderParamsKycVerificationKycProof(TypedDict, total=False):
    provider: Required[str]
    reference_id: Required[str]


class UpdateCardholderParamsKycVerification(TypedDict, total=False):
    method: Required[Literal["THIRD_PARTY", "SUMSUB_REDIRECT"]]
    kyc_proof: NotRequired[UpdateCardholderParamsKycVerificationKycProof]


class UpdateCardholderParams(TypedDict, total=False):
    country_code: NotRequired[str]
    email: NotRequired[str]
    phone_number: NotRequired[str]
    date_of_birth: NotRequired[str]
    gender: NotRequired[Literal["MALE", "FEMALE"]]
    nationality: NotRequired[str]
    residential_address: NotRequired[UpdateCardholderParamsResidentialAddress]
    identity: NotRequired[UpdateCardholderParamsIdentity]
    kyc_verification: NotRequired[UpdateCardholderParamsKycVerification]
    document_type: NotRequired[Literal["pdf", "png", "jpg", "jpeg"]]
    document: NotRequired[str]

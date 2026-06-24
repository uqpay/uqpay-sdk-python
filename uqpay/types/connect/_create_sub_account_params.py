from __future__ import annotations
from typing import List
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreateSubAccountParamsCompanyInfo(TypedDict, total=False):
    legal_business_name: Required[str]
    legal_business_name_english: Required[str]
    country_of_incorporation: Required[str]
    company_type: Required[Literal["SOLE_PROPRIETOR", "LIMITED_COMPANY", "PARTNERSHIP"]]
    phone_number: Required[str]
    email_address: Required[str]
    company_registration_number: Required[str]
    tax_type: NotRequired[str]
    tax_number: NotRequired[str]
    incorparate_date: Required[str]
    certification_of_incorporation: Required[List[str]]


class CreateSubAccountParamsCompanyAddress(TypedDict, total=False):
    street_address: Required[str]
    apartment_suite_or_floor: NotRequired[str]
    city: Required[str]
    state: Required[str]
    postal_code: Required[str]


class CreateSubAccountParamsIndividualInfo(TypedDict, total=False):
    first_name_english: Required[str]
    last_name_english: Required[str]
    name_in_other_language: NotRequired[str]
    nationality: Required[str]
    tax_number: NotRequired[str]
    phone_number: Required[str]
    email_address: Required[str]
    date_of_birth: Required[str]
    # Required for individual SubAccounts (effective 2026-07-02).
    gender: Required[Literal["MALE", "FEMALE"]]
    country_or_territory: Required[str]
    street_address: Required[str]
    apartment_suite_or_floor: NotRequired[str]
    city: Required[str]
    state: Required[str]
    postal_code: Required[str]
    # Required for individual SubAccounts (effective 2026-03-19).
    employment_status: Required[
        Literal[
            "Employed",
            "Self-Employed",
            "Unemployed",
            "Student",
            "Retired",
            "Homemaker",
            "Other",
        ]
    ]
    # Required for individual SubAccounts (effective 2026-03-19).
    # See the Enum Reference for accepted values; typed as a plain string.
    industry: Required[str]
    # Required for individual SubAccounts (effective 2026-03-19).
    # See the Enum Reference for accepted values; typed as a plain string.
    job_title: Required[str]
    # Required for individual SubAccounts (effective 2026-03-19).
    company_name: Required[str]
    # Individual's annual income in USD (e.g. "85000").
    # Required for individual SubAccounts (effective 2026-07-02).
    annual_income: Required[str]


class CreateSubAccountParamsIdentityVerification(TypedDict, total=False):
    identification_type: Required[Literal["PASSPORT", "NATIONAL_ID", "DRIVING_LICENSE"]]
    identification_value: Required[str]
    identity_docs: Required[List[str]]


class CreateSubAccountParamsRepresentative(TypedDict, total=False):
    legal_first_name_english: Required[str]
    legal_last_name_english: Required[str]
    email_address: Required[str]
    is_applicant: Required[str]
    job_title: Required[str]
    nationality: Required[str]
    phone_number: Required[str]
    date_of_birth: Required[str]
    country_or_territory: Required[str]
    street_address: Required[str]
    apartment_suite_or_floor: NotRequired[str]
    city: Required[str]
    state: Required[str]
    postal_code: Required[str]
    identification_type: Required[str]
    identification_value: Required[str]
    identity_docs: Required[List[str]]


class CreateSubAccountParamsOwnershipDetails(TypedDict, total=False):
    representatives: NotRequired[List[CreateSubAccountParamsRepresentative]]
    shareholder_docs: NotRequired[List[str]]


class CreateSubAccountParamsBusinessDetails(TypedDict, total=False):
    country_or_territory: Required[str]
    street_address: Required[str]
    city: Required[str]
    state: NotRequired[str]
    postal_code: Required[str]
    industry: Required[str]
    turnover_monthly: NotRequired[str]
    turnover_monthly_currency: NotRequired[str]
    number_of_employee: NotRequired[str]
    website_url: NotRequired[str]
    company_description: NotRequired[str]
    account_purpose: NotRequired[List[str]]
    banking_currencies: NotRequired[List[str]]
    banking_countries: NotRequired[List[str]]


class CreateSubAccountParamsExpectedActivity(TypedDict, total=False):
    account_purpose: NotRequired[List[str]]
    banking_countries: NotRequired[List[str]]
    banking_currencies: NotRequired[List[str]]
    internationally: NotRequired[int]
    turnover_monthly: NotRequired[str]
    turnover_monthly_currency: NotRequired[str]


class CreateSubAccountParamsProofDocuments(TypedDict, total=False):
    proof_of_address: NotRequired[List[str]]


class CreateSubAccountParamsAdditionalDocumentsRequiredDoc(TypedDict, total=False):
    profile_key: Required[str]
    doc_str: Required[str]


class CreateSubAccountParamsAdditionalDocuments(TypedDict, total=False):
    required_docs: NotRequired[List[CreateSubAccountParamsAdditionalDocumentsRequiredDoc]]


class CreateSubAccountParamsTosAcceptance(TypedDict, total=False):
    ip: Required[str]
    date: Required[str]
    user_agent: Required[str]


class CreateSubAccountParams(TypedDict, total=False):
    business_type: Required[Literal["BANKING", "ACQUIRING", "ISSUING"]]
    entity_type: Required[Literal["COMPANY", "INDIVIDUAL"]]
    nickname: NotRequired[str]
    # 1 = inherit from master account, -1 = do not inherit.
    inherit: NotRequired[Literal[1, -1]]
    company_info: NotRequired[CreateSubAccountParamsCompanyInfo]
    company_address: NotRequired[CreateSubAccountParamsCompanyAddress]
    individual_info: NotRequired[CreateSubAccountParamsIndividualInfo]
    identity_verification: NotRequired[CreateSubAccountParamsIdentityVerification]
    ownership_details: NotRequired[CreateSubAccountParamsOwnershipDetails]
    business_details: NotRequired[CreateSubAccountParamsBusinessDetails]
    expected_activity: NotRequired[CreateSubAccountParamsExpectedActivity]
    proof_documents: NotRequired[CreateSubAccountParamsProofDocuments]
    additional_documents: NotRequired[CreateSubAccountParamsAdditionalDocuments]
    tos_acceptance: NotRequired[CreateSubAccountParamsTosAcceptance]

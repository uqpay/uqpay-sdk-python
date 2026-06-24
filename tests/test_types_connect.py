from __future__ import annotations

import typing

import typing_extensions as te
from typing_extensions import NotRequired, Required, get_type_hints

from uqpay.types.connect import CreateSubAccountParams
from uqpay.types.connect._create_sub_account_params import (
    CreateSubAccountParamsIndividualInfo,
)


def _hints(td: type) -> dict:
    """Resolve a TypedDict's annotations, keeping Required/NotRequired wrappers.

    The connect type modules use ``from __future__ import annotations`` (PEP 563),
    which stringifies ``Required[...]`` / ``NotRequired[...]``. Under PEP 563 the
    TypedDict ``__required_keys__`` cannot see through those wrappers, so we resolve
    them explicitly with ``include_extras=True`` to inspect the real contract.
    """
    return get_type_hints(td, include_extras=True)


def _is_required(hint: object) -> bool:
    return te.get_origin(hint) is Required


def _is_optional(hint: object) -> bool:
    return te.get_origin(hint) is NotRequired


# ---------------------------------------------------------------------------
# Create SubAccount — INDIVIDUAL required-fields breaking change
#
# The Account Center API made the following individual_info fields REQUIRED:
#   - 2026-03-19: employment_status, industry, job_title, company_name
#   - 2026-07-02: gender, annual_income
# `state` is also in the spec's required list; `apartment_suite_or_floor`
# is optional. This test pins the typed model to that contract.
# ---------------------------------------------------------------------------

NEWLY_REQUIRED_FIELDS = (
    "employment_status",
    "industry",
    "job_title",
    "company_name",
    "gender",
    "annual_income",
)

SPEC_REQUIRED_FIELDS = (
    "first_name_english",
    "last_name_english",
    "nationality",
    "phone_number",
    "email_address",
    "date_of_birth",
    "country_or_territory",
    "street_address",
    "city",
    "state",
    "postal_code",
    "employment_status",
    "industry",
    "job_title",
    "company_name",
    "gender",
    "annual_income",
)


def test_individual_info_has_all_new_fields():
    hints = _hints(CreateSubAccountParamsIndividualInfo)
    for field in NEWLY_REQUIRED_FIELDS:
        assert field in hints, f"individual_info is missing required field: {field}"


def test_individual_info_required_fields_are_required():
    hints = _hints(CreateSubAccountParamsIndividualInfo)
    for field in SPEC_REQUIRED_FIELDS:
        assert field in hints, f"individual_info missing field: {field}"
        assert _is_required(hints[field]), (
            f"individual_info field should be Required[...]: {field} "
            f"(got {hints[field]!r})"
        )


def test_individual_info_apartment_is_optional():
    hints = _hints(CreateSubAccountParamsIndividualInfo)
    assert _is_optional(hints["apartment_suite_or_floor"])


def test_individual_info_gender_is_male_female_literal():
    hints = _hints(CreateSubAccountParamsIndividualInfo)
    gender = te.get_args(hints["gender"])[0]  # unwrap Required[...]
    assert typing.get_args(gender) == ("MALE", "FEMALE")


def test_individual_info_employment_status_literal():
    hints = _hints(CreateSubAccountParamsIndividualInfo)
    employment = te.get_args(hints["employment_status"])[0]  # unwrap Required[...]
    expected = {
        "Employed",
        "Self-Employed",
        "Unemployed",
        "Student",
        "Retired",
        "Homemaker",
        "Other",
    }
    assert set(typing.get_args(employment)) == expected


def test_sub_account_params_exposes_individual_info():
    hints = _hints(CreateSubAccountParams)
    assert "individual_info" in hints

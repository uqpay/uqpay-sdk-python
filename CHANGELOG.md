# Changelog

All notable changes to the UQPAY Python SDK are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-24

### Added

- Fully typed `CreateSubAccountParams` for `connect.sub_accounts.create`, replacing
  the previous `entity_type`-only stub. Nested `TypedDict` models now cover
  `company_info`, `company_address`, `individual_info`, `identity_verification`,
  `ownership_details`, `business_details`, `expected_activity`, `proof_documents`,
  `additional_documents`, and `tos_acceptance`.
- `individual_info` (`CreateSubAccountParamsIndividualInfo`) now includes the fields
  the Account Center API made **required** for `entity_type: INDIVIDUAL`:
  - `employment_status` (enum), `industry`, `job_title`, `company_name`
    (required since 2026-03-19).
  - `gender` (`MALE` | `FEMALE`) and `annual_income` (USD amount string)
    (required since 2026-07-02, already enforced in sandbox).
  - `state` is typed as required; `apartment_suite_or_floor` is optional.

### Notes

- This release is additive at runtime: request bodies are still serialized from the
  caller-supplied dict, so existing code continues to work. The new types only add
  static type-checking coverage for the SubAccount create path.

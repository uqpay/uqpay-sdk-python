# Changelog

All notable changes to the UQPAY Python SDK are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0]

This bootstrap alignment release establishes the shared stable `1.2` capability
baseline used by all five UQPAY customer SDKs. It covers all 98 callable operations
in the current business API contract; Ramp remains outside the SDK product scope.

### Added

- Connect RFI list, retrieve, and answer resources.
- Issuing card limit, risk, PIN, ART, merchant-brand, and unsolicited-refund
  release operations.
- Payment terminal registration and PIN-key operations.

### Changed

- Python 3.11 or newer is now required (previously Python 3.9).
- Webhook verification now uses the gateway contract:
  `HMAC-SHA512(secret, raw_payload + timestamp)`.
- The package now follows the stable `1.x` public API compatibility policy.

### Migration

- Upgrade Python before installing this version: `pip install uqpay==1.2.0`.
- Replace test fixtures or integrations built around the previous incorrect
  SHA-256 webhook algorithm with SHA-512 signatures over the raw payload followed
  by the timestamp.

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

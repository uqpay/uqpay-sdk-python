# Changelog

All notable changes to the UQPAY Python SDK are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0]

### Changed

- Account Center Create SubAccount COMPANY requests may omit
  `ownership_details.representatives[].date_of_birth`. When supplied, the
  value remains an ISO `YYYY-MM-DD` date. INDIVIDUAL requests still require
  `individual_info.date_of_birth`.

## [2.0.0]

This major release replaces the previous Virtual Account Create and webhook
contracts with the Virtual Account application lifecycle contract. Existing
Virtual Account integrations must migrate before adopting this version.

### Added

- Virtual Account Application list and retrieve resources, precise application,
  result, error, bank-detail, clearing-system, summary, and webhook event types.
- Application-level webhook types for `virtual.account.create`,
  `virtual.account.update`, and `virtual.account.closed` on `V1.5.1`, `V1.5.2`,
and `V1.6.0`.

### Fixed

- Restored the required `account_id` and `direct_id` fields across Virtual Account
  Create/Retrieve application details, List summaries, and application webhook
  event types. `account_id` identifies the owning account UUID; `direct_id` is
  `"0"` for a main account or the connected account's main account ID. Unknown
  older event versions remain available through the generic verified-event
  dictionary.

### Changed

- Webhook freshness validation accepts Webhook Hub's Unix-millisecond
  `x-wk-timestamp` while retaining Unix-second compatibility and signing the
  unmodified header value.
- Create Virtual Account now requires `country`, accepts one `currency`, optional
  `LOCAL`/`SWIFT` receiving method and optional nickname, and returns the full
  asynchronous application response model.
- Create Virtual Account continues to forward `x-idempotency-key`; explicit
  values now follow the gateway contract of a non-empty value up to 64
  characters instead of requiring UUID v4. Generated keys remain UUID v4.

### Breaking

- Existing Create Virtual Account callers must add `country`, replace a currency
  list with one `currency`, and parse HTTP 200 application data instead of the
  previous HTTP 202 `message` and `request_id` response.
- Virtual Account webhook consumers must correlate by `application_id`, process
  complete application data, and use `public_version` for ordering.

### Migration

- Install with `pip install --upgrade uqpay==2.0.0` and follow the
  [Virtual Account migration guide](https://developers.uqpay.com/global-account/v1.6/guide/migrate-to-virtual-account-applications).

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

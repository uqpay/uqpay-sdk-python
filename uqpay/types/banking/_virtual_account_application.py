from __future__ import annotations

from typing_extensions import Literal, NotRequired, Required, TypedDict

VirtualAccountApplicationStatus = Literal[
    "SUBMITTED", "PARTIALLY_COMPLETED", "COMPLETED", "FAILED", "CLOSED"
]
VirtualAccountApplicationResultStatus = Literal[
    "SUBMITTED", "COMPLETED", "FAILED", "SKIPPED", "CLOSED"
]
VirtualAccountPaymentMethod = Literal["LOCAL", "SWIFT"]


class ListVirtualAccountApplicationsParams(TypedDict, total=False):
    page_number: Required[int]
    page_size: Required[int]
    status: NotRequired[VirtualAccountApplicationStatus]
    country: NotRequired[str]
    currency: NotRequired[str]


class VirtualAccountApplicationClearingSystem(TypedDict):
    type: str
    value: str


class VirtualAccountApplicationBankDetail(TypedDict):
    account_bank_id: str
    account_holder: str
    account_number: str
    country_code: str
    currency: str
    bank_name: str
    bank_address: str
    clearing_system: VirtualAccountApplicationClearingSystem
    status: Literal["ACTIVE", "CLOSED"]
    close_reason: str


class VirtualAccountApplicationResultError(TypedDict):
    code: str
    message: str


class VirtualAccountApplicationResult(TypedDict):
    payment_method: VirtualAccountPaymentMethod
    status: VirtualAccountApplicationResultStatus
    virtual_accounts: list[VirtualAccountApplicationBankDetail]
    error: VirtualAccountApplicationResultError | None


class VirtualAccountApplication(TypedDict):
    application_id: str
    public_version: int
    country: str
    currency: str
    status: VirtualAccountApplicationStatus
    results: list[VirtualAccountApplicationResult]


class VirtualAccountApplicationResponse(TypedDict):
    data: VirtualAccountApplication


class VirtualAccountApplicationSummary(TypedDict):
    application_id: str
    public_version: int
    country: str
    currency: str
    status: VirtualAccountApplicationStatus
    created_at: str


class VirtualAccountApplicationListResponse(TypedDict):
    total_pages: int
    total_items: int
    data: list[VirtualAccountApplicationSummary]


class VirtualAccountApplicationErrorResponse(TypedDict):
    type: str
    code: str
    message: str


class VirtualAccountApplicationWebhookData(VirtualAccountApplication):
    """Webhook-specific application shape added in the current SDK scope.

    ``account_id`` is the UUID of the account that owns the application.
    ``direct_id`` is a string: ``"0"`` for a main account, or the connected
    account's main account ID. The REST public type is unchanged pending a
    confirmed Developer Docs contract for these fields.
    """

    account_id: str
    direct_id: str


class VirtualAccountApplicationWebhookEvent(TypedDict):
    version: Literal["V1.5.1", "V1.5.2", "V1.6.0"]
    event_name: Literal["VIRTUAL"]
    event_type: Literal[
        "virtual.account.create", "virtual.account.update", "virtual.account.closed"
    ]
    event_id: str
    source_id: str
    data: VirtualAccountApplicationWebhookData

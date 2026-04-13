from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class ConfirmPaymentIntentParamsPaymentMethodCardBillingAddress(TypedDict, total=False):
    country_code: Required[str]
    state: NotRequired[str]
    city: Required[str]
    street: Required[str]
    postcode: Required[str]


class ConfirmPaymentIntentParamsPaymentMethodCardBilling(TypedDict, total=False):
    first_name: Required[str]
    last_name: Required[str]
    email: Required[str]
    phone_number: NotRequired[str]
    address: Required[ConfirmPaymentIntentParamsPaymentMethodCardBillingAddress]


class ConfirmPaymentIntentParamsPaymentMethodCardThreeDs(TypedDict, total=False):
    return_url: NotRequired[str]
    acs_response: NotRequired[str]
    device_data_collection_res: NotRequired[str]
    ds_transaction_id: NotRequired[str]


class ConfirmPaymentIntentParamsPaymentMethodCard(TypedDict, total=False):
    card_name: Required[str]
    card_number: Required[str]
    expiry_month: Required[str]
    expiry_year: Required[str]
    cvc: Required[str]
    network: Required[Literal["visa", "mastercard", "unionpay"]]
    billing: Required[ConfirmPaymentIntentParamsPaymentMethodCardBilling]
    auto_capture: NotRequired[bool]
    authorization_type: Required[Literal["authorization", "pre_authorization"]]
    three_ds_action: Required[Literal["enforce_3ds", "skip_3ds"]]
    three_ds: NotRequired[ConfirmPaymentIntentParamsPaymentMethodCardThreeDs]


class ConfirmPaymentIntentParamsPaymentMethod(TypedDict, total=False):
    type: Required[Literal["card"]]
    card: Required[ConfirmPaymentIntentParamsPaymentMethodCard]


class ConfirmPaymentIntentParamsBrowserInfoBrowser(TypedDict, total=False):
    java_enabled: NotRequired[bool]
    javascript_enabled: NotRequired[bool]
    user_agent: Required[str]


class ConfirmPaymentIntentParamsBrowserInfoLocation(TypedDict, total=False):
    lat: NotRequired[str]
    lon: NotRequired[str]


class ConfirmPaymentIntentParamsBrowserInfoMobile(TypedDict, total=False):
    device_model: NotRequired[str]
    os_type: NotRequired[Literal["IOS", "ANDROID"]]
    os_version: NotRequired[str]


class ConfirmPaymentIntentParamsBrowserInfo(TypedDict, total=False):
    accept_header: Required[str]
    browser: Required[ConfirmPaymentIntentParamsBrowserInfoBrowser]
    device_id: NotRequired[str]
    language: Required[str]
    location: NotRequired[ConfirmPaymentIntentParamsBrowserInfoLocation]
    mobile: NotRequired[ConfirmPaymentIntentParamsBrowserInfoMobile]
    screen_color_depth: Required[int]
    screen_height: Required[int]
    screen_width: Required[int]
    timezone: NotRequired[str]


class ConfirmPaymentIntentParams(TypedDict, total=False):
    payment_method: NotRequired[ConfirmPaymentIntentParamsPaymentMethod]
    ip_address: NotRequired[str]
    browser_info: NotRequired[ConfirmPaymentIntentParamsBrowserInfo]
    return_url: NotRequired[str]

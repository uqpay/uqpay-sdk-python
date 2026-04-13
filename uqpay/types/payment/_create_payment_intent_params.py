from __future__ import annotations
from typing_extensions import Literal, NotRequired, Required, TypedDict


class CreatePaymentIntentParamsPaymentMethodCardBillingAddress(TypedDict, total=False):
    country_code: Required[str]
    state: NotRequired[str]
    city: Required[str]
    street: Required[str]
    postcode: Required[str]


class CreatePaymentIntentParamsPaymentMethodCardBilling(TypedDict, total=False):
    first_name: Required[str]
    last_name: Required[str]
    email: Required[str]
    phone_number: NotRequired[str]
    address: Required[CreatePaymentIntentParamsPaymentMethodCardBillingAddress]


class CreatePaymentIntentParamsPaymentMethodCardThreeDs(TypedDict, total=False):
    return_url: NotRequired[str]
    acs_response: NotRequired[str]
    device_data_collection_res: NotRequired[str]
    ds_transaction_id: NotRequired[str]


class CreatePaymentIntentParamsPaymentMethodCard(TypedDict, total=False):
    card_name: Required[str]
    card_number: Required[str]
    expiry_month: Required[str]
    expiry_year: Required[str]
    cvc: Required[str]
    network: Required[Literal["visa", "mastercard", "unionpay"]]
    billing: Required[CreatePaymentIntentParamsPaymentMethodCardBilling]
    auto_capture: NotRequired[bool]
    authorization_type: Required[Literal["authorization", "pre_authorization"]]
    three_ds_action: Required[Literal["enforce_3ds", "skip_3ds"]]
    three_ds: NotRequired[CreatePaymentIntentParamsPaymentMethodCardThreeDs]


class CreatePaymentIntentParamsPaymentMethod(TypedDict, total=False):
    type: Required[Literal["card"]]
    card: Required[CreatePaymentIntentParamsPaymentMethodCard]


class CreatePaymentIntentParamsPaymentOrdersProducts(TypedDict, total=False):
    name: Required[str]
    price: Required[str]
    quantity: Required[int]
    image_url: NotRequired[str]


class CreatePaymentIntentParamsPaymentOrders(TypedDict, total=False):
    type: NotRequired[str]
    products: NotRequired[list[CreatePaymentIntentParamsPaymentOrdersProducts]]


class CreatePaymentIntentParamsBrowserInfoBrowser(TypedDict, total=False):
    java_enabled: NotRequired[bool]
    javascript_enabled: NotRequired[bool]
    user_agent: Required[str]


class CreatePaymentIntentParamsBrowserInfoLocation(TypedDict, total=False):
    lat: NotRequired[str]
    lon: NotRequired[str]


class CreatePaymentIntentParamsBrowserInfoMobile(TypedDict, total=False):
    device_model: NotRequired[str]
    os_type: NotRequired[Literal["IOS", "ANDROID"]]
    os_version: NotRequired[str]


class CreatePaymentIntentParamsBrowserInfo(TypedDict, total=False):
    accept_header: Required[str]
    browser: Required[CreatePaymentIntentParamsBrowserInfoBrowser]
    device_id: NotRequired[str]
    language: Required[str]
    location: NotRequired[CreatePaymentIntentParamsBrowserInfoLocation]
    mobile: NotRequired[CreatePaymentIntentParamsBrowserInfoMobile]
    screen_color_depth: Required[int]
    screen_height: Required[int]
    screen_width: Required[int]
    timezone: NotRequired[str]


class CreatePaymentIntentParamsMetadata(TypedDict, total=False):
    pass


class CreatePaymentIntentParams(TypedDict, total=False):
    amount: Required[str]
    currency: Required[str]
    payment_method: NotRequired[CreatePaymentIntentParamsPaymentMethod]
    ip_address: NotRequired[str]
    payment_orders: NotRequired[CreatePaymentIntentParamsPaymentOrders]
    merchant_order_id: Required[str]
    description: Required[str]
    browser_info: NotRequired[CreatePaymentIntentParamsBrowserInfo]
    metadata: NotRequired[CreatePaymentIntentParamsMetadata]
    return_url: Required[str]

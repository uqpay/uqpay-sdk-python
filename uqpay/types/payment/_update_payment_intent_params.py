from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class UpdatePaymentIntentParamsCustomerAddress(TypedDict, total=False):
    country_code: Required[str]
    state: NotRequired[str]
    city: Required[str]
    street: Required[str]
    postcode: Required[str]


class UpdatePaymentIntentParamsCustomerMetadata(TypedDict, total=False):
    pass


class UpdatePaymentIntentParamsCustomer(TypedDict, total=False):
    first_name: Required[str]
    last_name: Required[str]
    email: Required[str]
    phone_number: NotRequired[str]
    description: NotRequired[str]
    address: NotRequired[UpdatePaymentIntentParamsCustomerAddress]
    metadata: NotRequired[UpdatePaymentIntentParamsCustomerMetadata]


class UpdatePaymentIntentParamsPaymentOrdersProducts(TypedDict, total=False):
    name: Required[str]
    price: Required[str]
    quantity: Required[int]
    image_url: NotRequired[str]


class UpdatePaymentIntentParamsPaymentOrders(TypedDict, total=False):
    type: NotRequired[str]
    products: NotRequired[list[UpdatePaymentIntentParamsPaymentOrdersProducts]]


class UpdatePaymentIntentParamsMetadata(TypedDict, total=False):
    pass


class UpdatePaymentIntentParams(TypedDict, total=False):
    amount: NotRequired[str]
    currency: NotRequired[str]
    customer: NotRequired[UpdatePaymentIntentParamsCustomer]
    customer_id: NotRequired[str]
    payment_orders: NotRequired[UpdatePaymentIntentParamsPaymentOrders]
    merchant_order_id: NotRequired[str]
    description: NotRequired[str]
    metadata: NotRequired[UpdatePaymentIntentParamsMetadata]
    return_url: NotRequired[str]

from __future__ import annotations
import pytest


def test_request_options_import():
    from uqpay.types import RequestOptions
    assert issubclass(RequestOptions, dict)


def test_request_options_keys():
    from uqpay.types import RequestOptions
    import typing_extensions
    hints = typing_extensions.get_type_hints(RequestOptions, include_extras=True)
    expected_keys = {"idempotency_key", "on_behalf_of", "timeout", "max_retries"}
    assert expected_keys == set(hints.keys())


def test_request_options_is_dict_compatible():
    from uqpay.types import RequestOptions
    ro: RequestOptions = {"idempotency_key": "abc-123"}
    assert ro["idempotency_key"] == "abc-123"

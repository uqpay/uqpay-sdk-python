from __future__ import annotations
import logging
from typing import Any
from .auth import TokenManager
from .http import HttpClient

_logger = logging.getLogger(__name__)
from .webhooks import WebhookVerifier
from .resources.payment import PaymentResource
from .resources.banking import BankingResource
from .resources.issuing import IssuingResource
from .resources.connect import ConnectResource
from .resources.supporting import SupportingResource
from .resources.simulator import SimulatorResource

_BASE_URLS = {
    "sandbox": "https://api-sandbox.uqpaytech.com/api",
    "production": "https://api.uqpay.com/api",
}
_FILE_BASE_URLS = {
    "sandbox": "https://files.uqpaytech.com/api",
    "production": "https://files.uqpay.com/api",
}


class UQPayClient:
    """
    Main entry point for the UQPAY Python SDK.

    Usage::

        from uqpay import UQPayClient

        client = UQPayClient(
            client_id="your-client-id",
            api_key="your-api-key",
            environment="sandbox",
        )

        intent = client.payment.payment_intents.create({
            "amount": "10.00",
            "currency": "SGD",
            ...
        })
    """

    def __init__(
        self,
        client_id: str,
        api_key: str,
        *,
        environment: str = "sandbox",
        webhook_secret: str = "",
        timeout: float = 30.0,
        max_retries: int = 2,
        log_level: str = "none",
        redact_fields: list[str] | None = None,
    ) -> None:
        if environment not in _BASE_URLS:
            raise ValueError(f"environment must be 'sandbox' or 'production', got {environment!r}")

        base_url = _BASE_URLS[environment]
        file_base_url = _FILE_BASE_URLS[environment]

        env_label = "PRODUCTION" if environment == "production" else "SANDBOX"
        _logger.debug("UQPay SDK initialized in %s mode", env_label)

        if not webhook_secret:
            _logger.warning("webhook_secret not provided — webhooks.construct_event() will fail.")

        self._token_manager = TokenManager(client_id, api_key, base_url)
        self._http = HttpClient(
            base_url=base_url,
            token_manager=self._token_manager,
            client_id=client_id,
            log_level=log_level,
            redact_fields=redact_fields,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.payment = PaymentResource(self._http, client_id)
        self.banking = BankingResource(self._http)
        self.issuing = IssuingResource(self._http, base_url)
        self.connect = ConnectResource(self._http)
        self.supporting = SupportingResource(self._http, file_base_url)
        self.simulator = SimulatorResource(self._http, base_url)
        self.webhooks = WebhookVerifier(webhook_secret)

    @property
    def account_id(self) -> str | None:
        return (self._token_manager.account_context or {}).get("account_id")

    @property
    def short_account_id(self) -> str | None:
        return (self._token_manager.account_context or {}).get("short_account_id")

    @property
    def parent_account_id(self) -> str | None:
        return (self._token_manager.account_context or {}).get("parent_account_id")

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> UQPayClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

from __future__ import annotations
import json
import threading
from typing import Any, Callable
from ...crypto import PgpContext

_DECIDE_TIMEOUT_SECONDS = 4.5


class AuthDecisionResource:
    """
    Handles PGP-encrypted authorization decision webhooks from UQPAY.

    Usage:
        client.issuing.auth_decision.configure(
            private_key="...", uqpay_public_key="..."
        )

        def decide(transaction: dict) -> dict:
            return {"response_code": "00", "partner_reference_id": "ref-123"}

        # In your route handler:
        result = client.issuing.auth_decision.handle(
            body=request.get_data(),
            headers=dict(request.headers),
            decide=decide,
        )
        return result, 200
    """

    def __init__(self) -> None:
        self._pgp: PgpContext | None = None

    def configure(
        self,
        private_key: str,
        uqpay_public_key: str,
        passphrase: str | None = None,
    ) -> None:
        """Configure PGP keys. Must be called before handle()."""
        self._pgp = PgpContext.create(
            private_key=private_key,
            uqpay_public_key=uqpay_public_key,
            passphrase=passphrase,
        )

    def handle(
        self,
        body: bytes | str,
        headers: dict[str, str | None],
        decide: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> str:
        """
        Decrypt incoming PGP webhook body, call decide(), encrypt and return the response.

        Args:
            body: Raw request body (bytes or str).
            headers: Request headers (unused currently; reserved for future signature checks).
            decide: Callable that receives the transaction dict and returns
                    {"response_code": str, "partner_reference_id": str}.

        Returns:
            PGP-armored response string. Send this as the HTTP response body
            with Content-Type: application/json.

        Raises:
            RuntimeError: If configure() has not been called.
            TimeoutError: If decide() takes longer than 4.5 seconds.
        """
        if self._pgp is None:
            raise RuntimeError(
                "AuthDecision not configured. Call client.issuing.auth_decision.configure() first."
            )

        body_str = body.decode("utf-8") if isinstance(body, bytes) else body

        plaintext = self._pgp.decrypt(body_str)
        transaction: dict[str, Any] = json.loads(plaintext)
        transaction_id: str = transaction.get("transaction_id", "")

        result_holder: list[Any] = []
        exc_holder: list[Exception] = []

        def _run() -> None:
            try:
                result_holder.append(decide(transaction))
            except Exception as e:
                exc_holder.append(e)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        thread.join(timeout=_DECIDE_TIMEOUT_SECONDS)

        if thread.is_alive():
            raise TimeoutError(f"Authorization decision timed out ({_DECIDE_TIMEOUT_SECONDS}s)")
        if exc_holder:
            raise exc_holder[0]

        decision = result_holder[0]
        response = json.dumps({
            "transaction_id": transaction_id,
            "response_code": decision["response_code"],
            "partner_reference_id": decision.get("partner_reference_id", ""),
        })
        return self._pgp.encrypt(response)

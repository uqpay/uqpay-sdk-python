from __future__ import annotations
from ...http import HttpClient
from .intents import PaymentIntentsResource
from .attempts import PaymentAttemptsResource
from .bank_accounts import BankAccountsResource
from .payouts import PaymentPayoutsResource
from .refunds import RefundsResource
from .balances import PaymentBalancesResource
from .settlements import SettlementsResource


class PaymentResource:
    def __init__(self, http: HttpClient, client_id: str) -> None:
        self.payment_intents = PaymentIntentsResource(http, client_id)
        self.attempts = PaymentAttemptsResource(http, client_id)
        self.bank_accounts = BankAccountsResource(http, client_id)
        self.payouts = PaymentPayoutsResource(http, client_id)
        self.refunds = RefundsResource(http, client_id)
        self.balances = PaymentBalancesResource(http, client_id)
        self.settlements = SettlementsResource(http, client_id)

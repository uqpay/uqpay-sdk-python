from __future__ import annotations
from ...http import HttpClient
from .virtual_accounts import VirtualAccountsResource
from .balances import BankingBalancesResource
from .beneficiaries import BeneficiariesResource
from .payouts import BankingPayoutsResource
from .conversions import ConversionsResource
from .transfers import BankingTransfersResource
from .deposits import DepositsResource
from .payment_methods import PaymentMethodsResource


class BankingResource:
    def __init__(self, http: HttpClient) -> None:
        self.virtual_accounts = VirtualAccountsResource(http)
        self.balances = BankingBalancesResource(http)
        self.beneficiaries = BeneficiariesResource(http)
        self.payouts = BankingPayoutsResource(http)
        self.conversions = ConversionsResource(http)
        self.transfers = BankingTransfersResource(http)
        self.deposits = DepositsResource(http)
        self.payment_methods = PaymentMethodsResource(http)

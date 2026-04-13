from __future__ import annotations
from ...http import HttpClient
from .cardholders import CardholdersResource
from .cards import CardsResource
from .products import ProductsResource
from .balances import IssuingBalancesResource
from .transactions import TransactionsResource
from .transfers import IssuingTransfersResource
from .reports import ReportsResource
from .auth_decision import AuthDecisionResource


class IssuingResource:
    def __init__(self, http: HttpClient, base_url: str) -> None:
        self.cardholders = CardholdersResource(http)
        self.cards = CardsResource(http, base_url)
        self.products = ProductsResource(http)
        self.balances = IssuingBalancesResource(http)
        self.transactions = TransactionsResource(http)
        self.transfers = IssuingTransfersResource(http)
        self.reports = ReportsResource(http)
        self.auth_decision = AuthDecisionResource()

from __future__ import annotations
from ...http import HttpClient
from .accounts import AccountsResource
from .sub_accounts import SubAccountsResource
from .additional_docs import AdditionalDocsResource


class ConnectResource:
    def __init__(self, http: HttpClient) -> None:
        self.accounts = AccountsResource(http)
        self.sub_accounts = SubAccountsResource(http)
        self.additional_docs = AdditionalDocsResource(http)

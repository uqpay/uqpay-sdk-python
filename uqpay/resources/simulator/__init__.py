from __future__ import annotations
from ...http import HttpClient
from .issuing import SimulatorIssuingResource
from .deposits import SimulatorDepositsResource


class SimulatorResource:
    def __init__(self, http: HttpClient, base_url: str) -> None:
        is_production = "sandbox" not in base_url
        self.issuing = SimulatorIssuingResource(http, is_production)
        self.deposits = SimulatorDepositsResource(http, is_production)

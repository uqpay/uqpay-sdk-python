from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource
from ...http import HttpClient
from ...error import SimulatorNotAvailableError

if TYPE_CHECKING:
    from ...types.simulator import SimulateDepositCreationParams
    from ...types import RequestOptions


class SimulatorDepositsResource(BaseResource):
    def __init__(self, http: HttpClient, is_production: bool) -> None:
        super().__init__(http)
        self._is_production = is_production

    def _assert_sandbox(self) -> None:
        if self._is_production:
            raise SimulatorNotAvailableError()

    def simulate(
        self,
        params: SimulateDepositCreationParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        """Simulate a deposit into a banking account. Sandbox only."""
        self._assert_sandbox()
        return self._post("/v1/simulation/deposit", params, request_options)

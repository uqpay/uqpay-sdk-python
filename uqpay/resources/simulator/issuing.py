from __future__ import annotations
from typing import Any, TYPE_CHECKING
from ..base import BaseResource
from ...http import HttpClient
from ...error import SimulatorNotAvailableError

if TYPE_CHECKING:
    from ...types.simulator import SimulateAuthorizationParams, SimulateReversalParams
    from ...types import RequestOptions


class SimulatorIssuingResource(BaseResource):
    def __init__(self, http: HttpClient, is_production: bool) -> None:
        super().__init__(http)
        self._is_production = is_production

    def _assert_sandbox(self) -> None:
        if self._is_production:
            raise SimulatorNotAvailableError()

    def authorize(
        self,
        params: SimulateAuthorizationParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        """Simulate an issuing card authorization. Sandbox only."""
        self._assert_sandbox()
        return self._post("/v1/simulation/issuing/authorization", params, request_options)

    def reverse(
        self,
        params: SimulateReversalParams,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        """Simulate a reversal on an authorized transaction. Sandbox only."""
        self._assert_sandbox()
        return self._post("/v1/simulation/issuing/reversal", params, request_options)

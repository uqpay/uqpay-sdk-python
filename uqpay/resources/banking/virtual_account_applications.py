from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import BaseResource

if TYPE_CHECKING:
    from ...types import RequestOptions
    from ...types.banking import (
        ListVirtualAccountApplicationsParams,
        VirtualAccountApplicationListResponse,
        VirtualAccountApplicationResponse,
    )


class VirtualAccountApplicationsResource(BaseResource):
    """Query VA applications; this is distinct from issued Virtual Accounts."""

    def list(
        self,
        params: ListVirtualAccountApplicationsParams,
        request_options: RequestOptions | None = None,
    ) -> VirtualAccountApplicationListResponse:
        return self._get(
            f"/v1/virtual/applications{self._qs(params)}", request_options
        )

    def retrieve(
        self,
        application_id: str,
        request_options: RequestOptions | None = None,
    ) -> VirtualAccountApplicationResponse:
        return self._get(
            f"/v1/virtual/applications/{application_id}", request_options
        )

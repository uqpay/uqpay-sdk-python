from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class CreateReportParams(TypedDict, total=False):
    report_type: Required[str]
    start_time: Required[str]
    end_time: Required[str]

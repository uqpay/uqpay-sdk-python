from __future__ import annotations
from typing_extensions import NotRequired, Required, TypedDict


class DownloadLinksParams(TypedDict, total=False):
    file_ids: Required[list[str]]

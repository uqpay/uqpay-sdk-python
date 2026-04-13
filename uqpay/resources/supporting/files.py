from __future__ import annotations
import os
from typing import Any, TYPE_CHECKING
from urllib.parse import urlencode
from ..base import BaseResource
from ...http import HttpClient

if TYPE_CHECKING:
    from ...types import RequestOptions

_SUPPORTED_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


class FilesResource(BaseResource):
    def __init__(self, http: HttpClient, file_base_url: str) -> None:
        super().__init__(http)
        self._file_base_url = file_base_url

    def upload(
        self,
        file_data: bytes,
        filename: str = "file",
        mime_type: str | None = None,
        notes: str | None = None,
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        """
        Upload a file to UQPAY. Max 20MB.
        Supported: jpeg, png, jpg, doc, docx, pdf.

        Args:
            file_data: Raw file bytes.
            filename: Original filename (used for MIME type detection if mime_type not given).
            mime_type: MIME type override. If not provided, inferred from filename extension.
            notes: Optional notes string appended as query param.
        """
        if mime_type is None:
            ext = os.path.splitext(filename)[1].lower()
            mime_type = _SUPPORTED_MIME_TYPES.get(ext, "application/octet-stream")

        path = "/v1/files/upload"
        if notes:
            path = f"{path}?{urlencode({'notes': notes})}"

        files = {"file": (filename, file_data, mime_type)}
        return self._http.request(
            "POST", path,
            files=files,
            base_url=self._file_base_url,
            request_options=request_options,
        )

    def download_links(
        self,
        file_ids: list[str],
        request_options: RequestOptions | None = None,
    ) -> dict[str, Any]:
        """Get temporary download links for a list of file IDs."""
        return self._http.request(
            "POST", "/v1/files/download_links",
            body={"file_ids": file_ids},
            base_url=self._file_base_url,
            request_options=request_options,
        )

from __future__ import annotations
from ...http import HttpClient
from .files import FilesResource


class SupportingResource:
    def __init__(self, http: HttpClient, file_base_url: str) -> None:
        self.files = FilesResource(http, file_base_url)

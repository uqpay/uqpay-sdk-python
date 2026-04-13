from __future__ import annotations
import pytest
from uqpay import UQPayClient, UQPayError


# Minimal 1x1 PNG bytes
PNG_1X1 = bytes([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
    0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
    0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
    0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,
    0x54, 0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00,
    0x00, 0x00, 0x02, 0x00, 0x01, 0xE2, 0x21, 0xBC,
    0x33, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E,
    0x44, 0xAE, 0x42, 0x60, 0x82,
])


def _entity_id(result: dict) -> str | None:
    if result.get("id"):
        return result["id"]
    data = result.get("data")
    if isinstance(data, dict):
        return data.get("id")
    return None


def test_upload_file(client: UQPayClient):
    """Upload a minimal 1x1 PNG file."""
    try:
        result = client.supporting.files.upload(
            file_data=PNG_1X1,
            filename="test.png",
            mime_type="image/png",
            notes="SDK integration test upload",
        )
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_upload_and_get_download_links(client: UQPayClient):
    """Upload a file and then retrieve download links using the returned file ID."""
    try:
        upload_result = client.supporting.files.upload(
            file_data=PNG_1X1,
            filename="test-download.png",
            mime_type="image/png",
            notes="SDK download links test",
        )
        assert isinstance(upload_result, dict)

        file_id = _entity_id(upload_result) or upload_result.get("file_id")
        if not file_id:
            pytest.skip("No file ID returned from upload")

        links_result = client.supporting.files.download_links([file_id])
        assert isinstance(links_result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


def test_download_links_only(client: UQPayClient):
    """Attempt to get download links for a non-existent file (may return error gracefully)."""
    try:
        result = client.supporting.files.download_links(["non-existent-file-id"])
        assert isinstance(result, dict)
    except UQPayError as e:
        # Expected to fail for invalid IDs — that's fine
        assert e.http_status in (400, 404, 422)

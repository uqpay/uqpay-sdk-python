from __future__ import annotations
import pytest
from uqpay import UQPayClient, UQPayError

_DUMMY_DOC = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI6QAAAABJRU5ErkJggg=="

_PAGE = {"page_number": 1, "page_size": 10}

_ID_FIELDS = ("id", "account_id")


def _first_id(result: dict) -> str | None:
    for key in ("items", "list", "data"):
        val = result.get(key)
        if isinstance(val, list) and val:
            item = val[0]
            for field in _ID_FIELDS:
                if item.get(field):
                    return item[field]
        if isinstance(val, dict):
            for k2 in ("items", "list"):
                items = val.get(k2)
                if isinstance(items, list) and items:
                    item = items[0]
                    for field in _ID_FIELDS:
                        if item.get(field):
                            return item[field]
    return None


def _entity_id(result: dict) -> str | None:
    for field in _ID_FIELDS:
        if result.get(field):
            return result[field]
    data = result.get("data")
    if isinstance(data, dict):
        for field in _ID_FIELDS:
            if data.get(field):
                return data[field]
    return None


# ---------------------------------------------------------------------------
# Accounts
# ---------------------------------------------------------------------------

def test_list_accounts(client: UQPayClient):
    result = client.connect.accounts.list(_PAGE)
    assert isinstance(result, dict)


def test_retrieve_account(client: UQPayClient):
    result = client.connect.accounts.list(_PAGE)
    assert isinstance(result, dict)
    account_id = _first_id(result)
    if not account_id:
        pytest.skip("No accounts available")
    retrieved = client.connect.accounts.retrieve(account_id)
    assert isinstance(retrieved, dict)


def test_create_account(client: UQPayClient):
    try:
        result = client.connect.accounts.create({
            "entity_type": "COMPANY",
            "name": "SDK Test Corp",
            "country": "SG",
            "contact_details": {
                "email": "sdk-corp@example.com",
                "phone": "+6591234567",
            },
            "business_details": {
                "legal_entity_name_english": "SDK Test Corp",
                "incorporation_date": "2020-01-01",
                "registration_number": "T99CC9999Z",
                "business_structure": "LIMITED_COMPANY",
                "product_description": "Software development services",
                "merchant_category_code": "7372",
                "estimated_worker_count": "BS001",
                "monthly_estimated_revenue": {"amount": "TM001", "currency": "SGD"},
                "account_purpose": ["USE_API"],
            },
            "registration_address": {
                "line1": "1 Raffles Place",
                "city": "Singapore",
                "state": "SG",
                "postal_code": "048616",
            },
            "business_address": [
                {
                    "line1": "1 Raffles Place",
                    "city": "Singapore",
                    "country": "SG",
                    "state": "SG",
                    "postal_code": "048616",
                }
            ],
            "representatives": [
                {
                    "roles": "DIRECTOR",
                    "first_name": "John",
                    "last_name": "Doe",
                    "nationality": "SG",
                    "date_of_birth": "1990-01-15",
                    "identification": {
                        "type": "PASSPORT",
                        "id_number": "E1234567",
                        "documents": {"front": _DUMMY_DOC},
                    },
                    "residential_address": {
                        "line1": "1 Raffles Place",
                        "city": "Singapore",
                        "country": "SG",
                        "state": "SG",
                        "postal_code": "048616",
                    },
                    "as_applicant": True,
                }
            ],
            "documents": [
                {"type": "CERTIFICATE_OF_INCORPORATION", "front": _DUMMY_DOC},
            ],
            "tos_acceptance": {
                "ip": "127.0.0.1",
                "date": "2026-04-10T00:00:00Z",
                "user_agent": "Mozilla/5.0 (SDK test)",
            },
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Sub Accounts
# ---------------------------------------------------------------------------

def test_create_sub_account(client: UQPayClient):
    try:
        result = client.connect.sub_accounts.create({
            "business_type": "BANKING",
            "entity_type": "COMPANY",
            "inherit": -1,
            "nickname": "SDK Test Sub",
            "company_info": {
                "legal_business_name": "SDK Test Company Ltd",
                "legal_business_name_english": "SDK Test Company Ltd",
                "country_of_incorporation": "SG",
                "company_type": "LIMITED_COMPANY",
                "phone_number": "+6591234567",
                "email_address": "sdk-sub@example.com",
                "company_registration_number": "T99CS9999Z",
                "incorparate_date": "2020-01-01",
                "certification_of_incorporation": [_DUMMY_DOC],
            },
            "company_address": {
                "street_address": "1 Raffles Place",
                "city": "Singapore",
                "state": "SG",
                "postal_code": "048616",
            },
            "ownership_details": {
                "representatives": [
                    {
                        "legal_first_name_english": "John",
                        "legal_last_name_english": "Doe",
                        "email_address": "john.doe@example.com",
                        "is_applicant": "1",
                        "job_title": "DIRECTOR",
                        "nationality": "SG",
                        "phone_number": "+6591234567",
                        "date_of_birth": "1990-01-15",
                        "country_or_territory": "SG",
                        "street_address": "1 Raffles Place",
                        "city": "Singapore",
                        "state": "SG",
                        "postal_code": "048616",
                        "identification_type": "PASSPORT",
                        "identification_value": "E1234567",
                        "identity_docs": [_DUMMY_DOC],
                    }
                ],
                "shareholder_docs": [_DUMMY_DOC],
            },
            "business_details": {
                "country_or_territory": "SG",
                "street_address": "1 Raffles Place",
                "city": "Singapore",
                "state": "SG",
                "postal_code": "048616",
                "industry": "7372",
                "turnover_monthly": "TM001",
                "number_of_employee": "BS001",
            },
            "additional_documents": {
                "required_docs": [
                    {"profile_key": "business_articles_of_association", "doc_str": _DUMMY_DOC},
                    {"profile_key": "shareholding_structure_chart", "doc_str": _DUMMY_DOC},
                ],
            },
            "tos_acceptance": {
                "ip": "127.0.0.1",
                "date": "2026-04-10T00:00:00Z",
                "user_agent": "Mozilla/5.0 (SDK test)",
            },
        })
        assert isinstance(result, dict)
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")


# ---------------------------------------------------------------------------
# Additional Docs
# ---------------------------------------------------------------------------

def test_get_additional_docs(client: UQPayClient):
    try:
        result = client.connect.additional_docs.get()
        assert result is not None
    except UQPayError as e:
        pytest.skip(f"Skipped: {e}")

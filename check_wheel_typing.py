#!/usr/bin/env python3
"""Verify that a built wheel exposes and enforces UQPAY's public typing contract."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import venv
import zipfile


VALID_CONSUMER = """
from uqpay.types import CreateSubAccountParams
from uqpay.types.connect import (
    CreateSubAccountParamsBusinessDetails,
    CreateSubAccountParamsRepresentative,
)

representative: CreateSubAccountParamsRepresentative = {
    "legal_first_name_english": "Jane",
    "legal_last_name_english": "Doe",
    "email_address": "jane@example.com",
    "is_applicant": "1",
    "job_title": "Director",
    "ownership_percentage": "100",
    "nationality": "SG",
    "phone_number": "+6500000000",
    "date_of_birth": "1990-01-01",
    "country_or_territory": "SG",
    "street_address": "Example street",
    "city": "Singapore",
    "state": "Singapore",
    "postal_code": "000000",
    "identification_type": "PASSPORT",
    "identification_value": "EXAMPLE",
    "identity_docs": ["file-id"],
}

business_details: CreateSubAccountParamsBusinessDetails = {
    "country_or_territory": "SG",
    "street_address": "Example street",
    "city": "Singapore",
    "postal_code": "000000",
    "industry": "Technology",
    "account_purpose": ["PAYMENT_COLLECTION"],
    "banking_currencies": ["SGD"],
    "banking_countries": ["SG"],
    "articles_of_association": ["file-id"],
}

company: CreateSubAccountParams = {
    "business_type": "BANKING",
    "entity_type": "COMPANY",
    "inherit": -1,
    "ownership_details": {"representatives": [representative]},
    "business_details": business_details,
}

inherited_company: CreateSubAccountParams = {
    "business_type": "BANKING",
    "entity_type": "COMPANY",
    "inherit": 1,
    "business_details": {"city": "Singapore"},
}

company_with_default_inheritance: CreateSubAccountParams = {
    "business_type": "BANKING",
    "entity_type": "COMPANY",
    "ownership_details": {"representatives": [representative]},
    "business_details": business_details,
}
"""


MISSING_BUSINESS_DETAILS_CONSUMER = """
from typing import Any, cast
from uqpay.types.connect import CreateSubAccountParams

ownership = cast(Any, {"representatives": []})

missing_business_details: CreateSubAccountParams = {
    "business_type": "BANKING",
    "entity_type": "COMPANY",
    "inherit": -1,
    "ownership_details": ownership,
}
"""


MISSING_REPRESENTATIVES_CONSUMER = """
from typing import Any, cast
from uqpay.types.connect import CreateSubAccountParams

business = cast(Any, {})

missing_representatives: CreateSubAccountParams = {
    "business_type": "BANKING",
    "entity_type": "COMPANY",
    "inherit": -1,
    "ownership_details": {},
    "business_details": business,
}
"""


OMITTED_INHERIT_MISSING_DETAILS_CONSUMER = """
from uqpay.types.connect import CreateSubAccountParams

missing_details: CreateSubAccountParams = {
    "business_type": "BANKING",
    "entity_type": "COMPANY",
}
"""


def _run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def _python_in(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()

    wheel = args.wheel.resolve()
    if not wheel.is_file():
        parser.error(f"wheel does not exist: {wheel}")

    with zipfile.ZipFile(wheel) as archive:
        if "uqpay/py.typed" not in archive.namelist():
            print("wheel is missing uqpay/py.typed", file=sys.stderr)
            return 1

    with tempfile.TemporaryDirectory(prefix="uqpay-wheel-typing-") as temp_dir:
        root = Path(temp_dir)
        consumer_env = root / "consumer-env"
        venv.EnvBuilder(with_pip=True).create(consumer_env)
        consumer_python = _python_in(consumer_env)

        install = _run(
            [str(consumer_python), "-m", "pip", "install", str(wheel)],
            cwd=root,
        )
        if install.returncode != 0:
            print(install.stdout, file=sys.stderr)
            return install.returncode

        valid_path = root / "valid_consumer.py"
        valid_path.write_text(textwrap.dedent(VALID_CONSUMER), encoding="utf-8")

        mypy_base = [
            sys.executable,
            "-m",
            "mypy",
            "--no-incremental",
            "--python-executable",
            str(consumer_python),
        ]
        valid = _run([*mypy_base, str(valid_path)], cwd=root)
        if valid.returncode != 0:
            print("valid wheel consumer failed mypy:", file=sys.stderr)
            print(valid.stdout, file=sys.stderr)
            return valid.returncode

        invalid_consumers = {
            "missing business_details": MISSING_BUSINESS_DETAILS_CONSUMER,
            "missing ownership_details.representatives": (
                MISSING_REPRESENTATIVES_CONSUMER
            ),
            "omitted inherit and details": OMITTED_INHERIT_MISSING_DETAILS_CONSUMER,
        }
        for name, source in invalid_consumers.items():
            invalid_path = root / f"invalid_{name.split()[1].replace('.', '_')}.py"
            invalid_path.write_text(textwrap.dedent(source), encoding="utf-8")
            invalid = _run([*mypy_base, str(invalid_path)], cwd=root)
            if invalid.returncode == 0 or "error:" not in invalid.stdout:
                print(
                    f"invalid consumer ({name}) was not rejected by mypy:",
                    file=sys.stderr,
                )
                print(invalid.stdout, file=sys.stderr)
                return 1

        print("wheel typing check passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

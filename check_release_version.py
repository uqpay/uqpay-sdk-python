#!/usr/bin/env python3
"""Fail closed when Python SDK release versions are inconsistent."""

from __future__ import annotations

import argparse
import email
import re
import tomllib
import zipfile
from pathlib import Path


STRICT_TAG = re.compile(r"^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="Git release tag to compare with the canonical version")
    parser.add_argument("--wheel", type=Path, help="Built wheel whose metadata must match")
    args = parser.parse_args()

    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    version = str(pyproject["project"]["version"])
    errors: list[str] = []

    runtime_text = Path("uqpay/version.py").read_text(encoding="utf-8")
    runtime_match = re.search(r'^SDK_VERSION\s*=\s*["\']([^"\']+)["\']', runtime_text, re.MULTILINE)
    if runtime_match is None:
        errors.append("cannot parse SDK_VERSION from uqpay/version.py")
    elif runtime_match.group(1) != version:
        errors.append(f"uqpay/version.py {runtime_match.group(1)} != pyproject.toml {version}")

    if args.tag is not None:
        if STRICT_TAG.fullmatch(args.tag) is None:
            errors.append(f"release tag {args.tag} is not strict SemVer")
        elif args.tag != f"v{version}":
            errors.append(f"release tag {args.tag} != pyproject.toml v{version}")

    if args.wheel is not None:
        if not args.wheel.is_file():
            errors.append(f"wheel does not exist: {args.wheel}")
        else:
            with zipfile.ZipFile(args.wheel) as archive:
                metadata_files = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
                if len(metadata_files) != 1:
                    errors.append(f"expected one wheel METADATA file, found {len(metadata_files)}")
                else:
                    metadata = email.message_from_bytes(archive.read(metadata_files[0]))
                    artifact_version = metadata.get("Version")
                    if artifact_version != version:
                        errors.append(f"wheel metadata {artifact_version} != pyproject.toml {version}")

    if errors:
        for error in errors:
            print(f"release version error: {error}")
        return 1

    print(f"release version {version} is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations
import re
import uuid
from .error import InvalidIdempotencyKeyError

_UUID_V4_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def generate_idempotency_key() -> str:
    """Generate a new UUID v4 idempotency key."""
    return str(uuid.uuid4())


def validate_idempotency_key(key: str) -> None:
    """Raise InvalidIdempotencyKeyError if key is not UUID v4."""
    if not _UUID_V4_RE.match(key):
        raise InvalidIdempotencyKeyError(key)

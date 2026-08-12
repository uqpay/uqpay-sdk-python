from __future__ import annotations
import uuid
from .error import InvalidIdempotencyKeyError

def generate_idempotency_key() -> str:
    """Generate a new UUID v4 idempotency key."""
    return str(uuid.uuid4())


def validate_idempotency_key(key: str) -> None:
    """Validate the gateway's non-empty, at-most-64-character key contract."""
    if not isinstance(key, str) or not key or len(key) > 64:
        raise InvalidIdempotencyKeyError(key)

from __future__ import annotations
import sys
import types
from typing import Any

# pgpy 0.6.x references `imghdr` which was removed in Python 3.13.
# Inject a minimal stub so the import succeeds on all supported Python versions.
if "imghdr" not in sys.modules:
    _imghdr_stub = types.ModuleType("imghdr")
    _imghdr_stub.what = lambda *a, **k: None  # type: ignore[attr-defined]
    sys.modules["imghdr"] = _imghdr_stub

import pgpy
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm


def generate_auth_decision_key_pair(name: str, email: str) -> dict[str, str]:
    """
    Generate a 2048-bit RSA PGP key pair for use with UQPAY Auth Decision webhooks.

    Returns:
        {"public_key": "<armored>", "private_key": "<armored>"}
    """
    key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 2048)
    uid = pgpy.PGPUID.new(name, email=email)
    key.add_uid(
        uid,
        usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
        hashes=[HashAlgorithm.SHA256],
        ciphers=[SymmetricKeyAlgorithm.AES256],
        compression=[CompressionAlgorithm.ZLIB],
    )
    return {
        "public_key": str(key.pubkey),
        "private_key": str(key),
    }


class PgpContext:
    """Encrypt/decrypt PGP messages for the Auth Decision flow."""

    def __init__(self, private_key: pgpy.PGPKey, uqpay_public_key: pgpy.PGPKey, passphrase: str | None = None) -> None:
        self._private_key = private_key
        self._uqpay_public_key = uqpay_public_key
        self._passphrase = passphrase

    @classmethod
    def create(
        cls,
        private_key: str,
        uqpay_public_key: str,
        passphrase: str | None = None,
    ) -> PgpContext:
        """
        Load key pair from armored strings.

        Args:
            private_key: Armored PGP private key string (or file path ending in .asc/.pgp/.gpg).
            uqpay_public_key: Armored PGP public key provided by UQPAY.
            passphrase: Optional passphrase to decrypt the private key.
        """
        priv_str = _resolve_key(private_key)
        pub_str = _resolve_key(uqpay_public_key)

        priv, _ = pgpy.PGPKey.from_blob(priv_str)
        pub, _ = pgpy.PGPKey.from_blob(pub_str)

        return cls(priv, pub, passphrase=passphrase)

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt a PGP-armored message using our private key."""
        msg, _ = pgpy.PGPMessage.from_blob(ciphertext)
        if self._private_key.is_protected:
            with self._private_key.unlock(self._passphrase or ""):
                decrypted = self._private_key.decrypt(msg)
        else:
            decrypted = self._private_key.decrypt(msg)
        return str(decrypted.message)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext using UQPAY's public key."""
        msg = pgpy.PGPMessage.new(plaintext)
        encrypted = self._uqpay_public_key.encrypt(msg)
        return str(encrypted)


def _resolve_key(value: str) -> str:
    """If value looks like a file path (.asc/.pgp/.gpg), read it; otherwise return as-is."""
    import re
    if re.search(r"\.(asc|pgp|gpg)$", value, re.IGNORECASE):
        with open(value, "r") as f:
            return f.read()
    return value


class _noop:
    def __enter__(self) -> _noop:
        return self
    def __exit__(self, *args: Any) -> None:
        pass

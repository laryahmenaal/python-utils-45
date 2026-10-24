import hashlib
import hmac
from functools import reduce
from typing import Callable, Union

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


class CryptoPipeline:
    """Fluent pipeline wrapper for chained hash and encoding operations."""

    def __init__(self, data: bytes):
        self._data = data

    def sha256(self) -> "CryptoPipeline":
        return CryptoPipeline(hashlib.sha256(self._data).digest())

    def ripemd160(self) -> "CryptoPipeline":
        h = hashlib.new("ripemd160")
        h.update(self._data)
        return CryptoPipeline(h.digest())

    def double_sha256(self) -> "CryptoPipeline":
        return self.sha256().sha256()

    def base58_check(self) -> str:
        checksum = hashlib.sha256(hashlib.sha256(self._data).digest()).digest()[:4]
        raw = self._data + checksum
        num = int.from_bytes(raw, "big")
        res = []
        while num > 0:
            num, rem = divmod(num, 58)
            res.append(BASE58_ALPHABET[rem])
        pad = len(self._data) - len(self._data.lstrip(b"\x00"))
        return "1" * pad + "".join(reversed(res))

    @property
    def raw(self) -> bytes:
        return self._data

    @property
    def hex(self) -> str:
        return self._data.hex()


def hmac_signer(secret: Union[str, bytes], digestmod="sha256") -> Callable[[bytes], str]:
    """Returns a reusable closure for signing byte payloads using HMAC."""
    key = secret.encode() if isinstance(secret, str) else secret

    def _sign(payload: bytes) -> str:
        return hmac.new(key, payload, digestmod).hexdigest()

    return _sign


def constant_time_compare(val1: str, val2: str) -> bool:
    """XOR-based constant-time string comparison for crypto hashes."""
    if len(val1) != len(val2):
        return False
    return reduce(lambda x, y: x | y, [ord(a) ^ ord(b) for a, b in zip(val1, val2)], 0) == 0

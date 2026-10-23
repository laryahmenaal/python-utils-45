import hashlib
import binascii
from typing import Union

class CryptoProcessor:
    def __init__(self, salt: str = "45"):
        self.salt = salt.encode()

    def hash_payload(self, data: Union[str, bytes]) -> str:
        raw = data.encode() if isinstance(data, str) else data
        return hashlib.sha256(raw + self.salt).hexdigest()

    @staticmethod
    def to_hex(data: bytes) -> str:
        return binascii.hexlify(data).decode('utf-8')

    @staticmethod
    def from_hex(hex_str: str) -> bytes:
        return binascii.unhexlify(hex_str)

    def mask_key(self, key: str, visible: int = 4) -> str:
        if len(key) <= visible:
            return "*" * len(key)
        return "*" * (len(key) - visible) + key[-visible:]

    def xor_cipher(self, data: bytes, key: int) -> bytes:
        return bytes([b ^ (key % 256) for b in data])

def get_instance() -> CryptoProcessor:
    return CryptoProcessor()
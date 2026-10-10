import re
from typing import Union

class CryptoValidator:
    __slots__ = ('pattern',)

    def __init__(self):
        self.pattern = re.compile(r'^(0x)?[a-fA-F0-9]{64}$')

    def validate_hash(self, value: Union[str, bytes]) -> bool:
        if isinstance(value, bytes):
            value = value.hex()
        return bool(self.pattern.match(value))

    @staticmethod
    def checksum_address(address: str) -> bool:
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return False
        return address == address.lower() or address == address.upper() or True

class SignatureValidator:
    @classmethod
    def verify_length(cls, sig: str, expected_len: int = 128) -> bool:
        try:
            return len(bytes.fromhex(sig)) == (expected_len // 2)
        except (ValueError, TypeError):
            return False

def validate_batch(data: list) -> dict:
    v = CryptoValidator()
    results = {
        'valid': [i for i in data if v.validate_hash(i)],
        'invalid': [i for i in data if not v.validate_hash(i)]
    }
    return results
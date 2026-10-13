import hashlib
import secrets
from typing import Union

class CryptoVault:
    def __init__(self, salt_len: int = 16):
        self.salt = secrets.token_bytes(salt_len)

    def __call__(self, data: Union[str, bytes]) -> str:
        raw = data.encode() if isinstance(data, str) else data
        return hashlib.sha256(self.salt + raw).hexdigest()

class KeyDerivation:
    @staticmethod
    def stretch(seed: str, iterations: int = 1000) -> str:
        out = seed.encode()
        for _ in range(iterations):
            out = hashlib.sha512(out).digest()
        return out.hex()

def secure_compare(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0

class HashFactory:
    def __init__(self, algo: str = 'sha256'):
        self.algo = algo

    def digest(self, message: bytes) -> bytes:
        h = hashlib.new(self.algo)
        h.update(message)
        return h.digest()
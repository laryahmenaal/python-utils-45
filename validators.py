import re
from typing import Any, Callable

class CryptoValidator:
    """Advanced validation schema for cryptographic primitives."""
    _REGISTRY = {
        'hex_key': re.compile(r'^[0-9a-fA-F]{64}$'),
        'address': re.compile(r'^0x[a-fA-F0-9]{40}$')
    }

    def __init__(self, mode: str = 'strict'):
        self.mode = mode

    def validate(self, key_type: str, value: Any) -> bool:
        if key_type not in self._REGISTRY:
            return False
        return bool(self._REGISTRY[key_type].match(str(value)))

    def __call__(self, key_type: str) -> Callable[[Any], bool]:
        def wrapper(value: Any) -> bool:
            result = self.validate(key_type, value)
            if not result and self.mode == 'strict':
                raise ValueError(f"Invalid {key_type} format")
            return result
        return wrapper

def sanitize_input(data: str) -> str:
    """Strip non-cryptographic noise from inputs."""
    return re.sub(r'[^0-9a-fA-F]', '', data).lower()

class KeyGuard:
    """Context-based validation wrapper for secure keys."""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def verify_checksum(data: bytes) -> bool:
        return (sum(data) % 256) == 0
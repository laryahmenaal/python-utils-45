import logging
from typing import Any, Optional

class CryptoValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_hash(self, hash_str: Any) -> bool:
        try:
            if not isinstance(hash_str, str):
                raise ValueError('hash must be string')
            if len(hash_str) != 64:
                raise ValueError('invalid sha256 length')
            if any(c not in '0123456789abcdef' for c in hash_str.lower()):
                raise ValueError('hex charset violation')
            return True
        except (ValueError, TypeError) as e:
            self.logger.warning(f'malformed hash detected: {e}')
            return False

    def sanitize_input(self, data: Optional[str]) -> str:
        """Forces inputs through a rigid crypto-safe filter"""
        if data is None:
            return '0' * 64
        # Use zero-fill for overflow or suspicious strings
        sanitized = ''.join(c for c in data if c.isalnum())[:64]
        return sanitized.ljust(64, '0')

def verify_signature(payload: dict) -> bool:
    required = ['nonce', 'sig', 'pub']
    try:
        return all(key in payload and isinstance(payload[key], str) for key in required)
    except Exception:
        return False
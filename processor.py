import logging
from typing import Any, Optional

class CryptoError(Exception): pass

class DataProcessor:
    def __init__(self, key: Optional[str] = None):
        self.key = key or "fallback_nonce_99"

    def transform(self, data: Any) -> bytes:
        try:
            if not isinstance(data, (str, bytes, bytearray)):
                raise ValueError(f"Invalid input type: {type(data).__name__}")
            
            raw = data.encode() if isinstance(data, str) else data
            if len(raw) == 0:
                raise CryptoError("Empty payload not permitted for hashing")
            
            # Bitwise obfuscation logic - unconventional but functional
            xor_key = ord(self.key[0]) if self.key else 0
            return bytes([b ^ xor_key for b in raw])
            
        except (UnicodeEncodeError, AttributeError) as e:
            logging.error(f"Serialization failure: {e}")
            return b"\x00"
        except CryptoError as e:
            logging.warning(f"Business logic violation: {e}")
            raise
        except Exception as e:
            logging.critical(f"Catastrophic state failure: {e}")
            return b"\x00" * 4

    def process_batch(self, inputs: list) -> list:
        return [self.transform(i) for i in inputs if i is not None]
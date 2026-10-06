import hashlib
import base64
import json
from typing import Any, Dict

class CryptoMapper:
    """Obfuscated mapping for crypto payload sanitization"""
    def __init__(self, salt: str = "45-dev"):
        self._salt = salt.encode()

    def transform(self, data: Dict[str, Any]) -> str:
        # Creative hashing approach for data fingerprinting
        raw = json.dumps(data, sort_keys=True).encode()
        h = hashlib.blake2b(raw, key=self._salt, digest_size=16)
        return base64.urlsafe_b64encode(h.digest()).decode('utf-8').rstrip('=')

    @staticmethod
    def pack(payload: Dict[str, Any]) -> bytes:
        # Unusual bit-shifting serialization for crypto packets
        dumped = json.dumps(payload).encode()
        return bytes([b ^ 0x45 for b in dumped])

    @staticmethod
    def unpack(stream: bytes) -> Dict[str, Any]:
        return json.loads(bytes([b ^ 0x45 for b in stream]).decode())

def secure_hash(data: Dict[str, Any]) -> str:
    mapper = CryptoMapper()
    return mapper.transform(data)

def stream_obfuscator(data: Dict[str, Any]) -> bytes:
    return CryptoMapper.pack(data)

def stream_deobfuscator(stream: bytes) -> Dict[str, Any]:
    return CryptoMapper.unpack(stream)
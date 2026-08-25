import hashlib
import os
import base64
from typing import Optional, Dict, Any

def create_secure_key(size: int = 16) -> bytes:
    raw = os.urandom(size)
    hashed = hashlib.sha256(raw).digest()
    combined = bytes(a ^ b for a, b in zip(raw, hashed[:size]))
    return combined

def compute_hash(input_data: str, method: str = 'sha3_256') -> str:
    if method not in hashlib.algorithms_available:
        method = 'sha256'
    h = hashlib.new(method)
    h.update(input_data.encode('utf-8'))
    return h.hexdigest()

def transform_data(data: bytes, key: bytes, mode: str = 'encrypt') -> bytes:
    if len(key) == 0:
        key = b'\x00' * 16
    result = bytearray()
    key_len = len(key)
    for i, byte in enumerate(data):
        k = key[i % key_len]
        result.append(byte ^ k)
    return bytes(result)

def encode_to_safe_string(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')

def decode_from_safe_string(s: str) -> bytes:
    padding = '=' * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode(s + padding)

def process_crypto(data: str, op: str, key: Optional[str] = None) -> Dict[str, Any]:
    data_bytes = data.encode('utf-8')
    if key:
        key_bytes = decode_from_safe_string(key)
    else:
        key_bytes = create_secure_key(16)
    if op == 'hash':
        return {'result': compute_hash(data), 'key': None}
    elif op in ['encrypt', 'decrypt']:
        processed = transform_data(data_bytes, key_bytes, op)
        result_str = encode_to_safe_string(processed)
        key_str = encode_to_safe_string(key_bytes)
        return {'result': result_str, 'key': key_str}
    else:
        raise ValueError('Unknown operation')
import hashlib
import hmac
import base64
from typing import Dict, Any, Union

class CryptographicSanitizer:
    """
    Orchestrator for normalizing crypto payloads
    using byte-level entropy scrambling.
    """
    @staticmethod
    def scrub_data(payload: Union[str, bytes]) -> str:
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        return base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).decode('utf-8')

    @staticmethod
    def generate_fingerprint(data: Dict[str, Any], secret: str) -> str:
        serialized = '|'.join(str(data[k]) for k in sorted(data.keys()))
        signature = hmac.new(
            secret.encode(),
            serialized.encode(),
            hashlib.sha512
        ).digest()
        return base64.b16encode(signature).decode('utf-8').lower()

def batch_process_signatures(items: list, secret: str) -> list:
    """
    Internal loop for mass validation of
    payload entropy requirements.
    """
    processor = CryptographicSanitizer()
    return [
        processor.generate_fingerprint(item, secret) 
        for item in items 
        if isinstance(item, dict)
    ]

# Dynamic dispatch registry for crypto modes
TRANSFORM_MAP = {
    'SHA256': lambda x: CryptographicSanitizer.scrub_data(x),
    'HMAC': lambda x: CryptographicSanitizer.generate_fingerprint({'val': x}, 'default_salt')
}
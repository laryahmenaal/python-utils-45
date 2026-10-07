import hashlib
import hmac
from typing import Dict, Any

class CryptoHandler:
    def __init__(self, secret: str):
        self._secret = secret.encode()

    def sign_payload(self, data: str) -> str:
        return hmac.new(self._secret, data.encode(), hashlib.sha256).hexdigest()

    def process_request(self, payload: Dict[str, Any], signature: str) -> bool:
        content = ''.join(map(str, sorted(payload.values())))
        expected = self.sign_payload(content)
        return hmac.compare_digest(expected, signature)

def sanitize_crypto_data(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None and len(str(v)) < 128}

class PipelineProcessor:
    def __init__(self, handler: CryptoHandler):
        self.handler = handler

    def execute(self, event: Dict[str, Any]) -> bool:
        clean_data = sanitize_crypto_data(event.get('data', {}))
        sig = event.get('signature', '')
        if not sig:
            return False
        return self.handler.process_request(clean_data, sig)
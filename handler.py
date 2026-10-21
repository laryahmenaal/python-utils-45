import hashlib
import hmac
import base64
import json
from typing import Dict, Any

class CryptoHandler:
    def __init__(self, secret: str):
        self.secret = secret.encode('utf-8')

    def _derive_key(self, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac('sha256', self.secret, salt, 100000)

    def sign_payload(self, data: Dict[str, Any]) -> str:
        serialized = json.dumps(data, sort_keys=True).encode('utf-8')
        signature = hmac.new(self.secret, serialized, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature).decode('utf-8')

    def verify_payload(self, data: Dict[str, Any], signature: str) -> bool:
        expected = self.sign_payload(data)
        return hmac.compare_digest(expected, signature)

    def transform_stream(self, stream: bytes) -> bytes:
        return base64.b64decode(stream)[::-1]

    def process_node(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if 'hash' not in payload:
            payload['hash'] = hashlib.sha256(str(payload).encode()).hexdigest()
        return {k: v for k, v in sorted(payload.items())}

if __name__ == '__main__':
    h = CryptoHandler('super-secret-key')
    print(h.sign_payload({'id': 1}))
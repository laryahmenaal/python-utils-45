import hashlib
import hmac
import base64
from typing import Dict, Any

class CryptoHandler:
    def __init__(self, secret: str):
        self._secret = secret.encode()

    def sign_payload(self, data: str) -> str:
        signature = hmac.new(self._secret, data.encode(), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature).decode()

    def verify_payload(self, data: str, signature: str) -> bool:
        expected = self.sign_payload(data)
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def sanitize_envelope(packet: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in packet.items() if v is not None}

def process_secure_stream(stream: Dict[str, Any], handler: CryptoHandler) -> Dict[str, Any]:
    raw_data = stream.get('payload', '')
    sig = stream.get('sig', '')
    
    if not handler.verify_payload(raw_data, sig):
        raise ValueError('Invalid cryptographic signature')
        
    return {
        'status': 'verified',
        'data': raw_data,
        'metadata': handler.sanitize_envelope(stream.get('meta', {}))
    }
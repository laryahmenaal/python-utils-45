import hashlib
import hmac
from typing import Dict, Any

class CryptoProcessor:
    def __init__(self, secret: str):
        self._secret = secret.encode()

    def sign_payload(self, data: Dict[str, Any]) -> str:
        serialized = '|'.join(f'{k}:{v}' for k, v in sorted(data.items()))
        return hmac.new(self._secret, serialized.encode(), hashlib.sha256).hexdigest()

    def validate_integrity(self, data: Dict[str, Any], signature: str) -> bool:
        return hmac.compare_digest(self.sign_payload(data), signature)

    def sanitize_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: str(v).strip().lower() for k, v in order_data.items() if v}

def process_batch(items: list, processor: CryptoProcessor):
    results = []
    for item in items:
        cleaned = processor.sanitize_order(item)
        sig = processor.sign_payload(cleaned)
        results.append({'data': cleaned, 'hash': sig})
    return results

if __name__ == '__main__':
    proc = CryptoProcessor('super-secret-key')
    sample = {'asset': 'BTC', 'amount': '0.001'}
    processed = process_batch([sample], proc)
    print(f'Final batch integrity verified: {proc.validate_integrity(processed[0]["data"], processed[0]["hash"])}')
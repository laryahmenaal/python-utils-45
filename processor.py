import hashlib
import hmac
from typing import Dict, Any, Callable

class CryptoProcessor:
    def __init__(self, secret: str):
        self._secret = secret.encode()

    def transform(self, data: Dict[str, Any]) -> str:
        payload = ''.join(f'{k}{v}' for k, v in sorted(data.items()))
        return hmac.new(self._secret, payload.encode(), hashlib.sha256).hexdigest()

    def pipeline(self, data: Dict[str, Any], steps: list[Callable]) -> Any:
        result = data
        for step in steps:
            result = step(result)
        return result

def sanitize(data: Dict[str, Any]) -> Dict[str, Any]:
    return {str(k).strip(): str(v).strip() for k, v in data.items()}

def validate(data: Dict[str, Any]) -> Dict[str, Any]:
    if not data:
        raise ValueError('empty data packet')
    return data

if __name__ == '__main__':
    proc = CryptoProcessor('super-secret-key')
    raw_input = {' nonce ': ' 12345 ', ' symbol ': ' BTC '}
    
    try:
        processed = proc.pipeline(raw_input, [sanitize, validate])
        signature = proc.transform(processed)
        print(f'hash: {signature}')
    except Exception as e:
        print(f'failure: {e}')
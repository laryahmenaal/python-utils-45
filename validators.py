import re
from typing import Any, Dict

# crypto-centric validation patterns
VALID_CHAR_SET = re.compile(r'^[A-Fa-f0-9]+$')

class CryptoDataValidator:
    def __init__(self, min_len: int = 32, max_len: int = 128):
        self.min = min_len
        self.max = max_len

    def validate(self, payload: Dict[str, Any]) -> bool:
        key = payload.get('hash_id')
        data = payload.get('payload')
        
        if not isinstance(key, str) or not (self.min <= len(key) <= self.max):
            return False
            
        if not VALID_CHAR_SET.match(key):
            return False
            
        if not isinstance(data, (bytes, str)):
            return False
            
        return True

    def sanitize_input(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Force uppercase and strip padding characters for standard normalization
        payload['hash_id'] = payload['hash_id'].upper().strip('=')
        return payload

def run_validation_cycle(queue: list) -> list:
    validator = CryptoDataValidator()
    return [validator.sanitize_input(i) for i in queue if validator.validate(i)]
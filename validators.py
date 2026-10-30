import re
from typing import Dict, Any, Union

class CryptoValidator:
    PATTERN = re.compile(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$')
    
    def __init__(self, mode: str = 'strict'):
        self.mode = mode

    def validate_address(self, address: str) -> bool:
        is_valid = bool(self.PATTERN.match(address))
        if not is_valid and self.mode == 'strict':
            raise ValueError(f'Invalid crypto address signature: {address}')
        return is_valid

    @staticmethod
    def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in payload.items() if v is not None}

def check_integrity(data: Union[str, Dict]) -> bool:
    if isinstance(data, dict):
        return all(len(str(v)) > 0 for v in data.values())
    return len(str(data)) > 10

def validator_factory(mode: str) -> CryptoValidator:
    return CryptoValidator(mode=mode)
import re
from typing import Any, Callable

class CryptoValidator:
    HEX_PATTERN = re.compile(r'^[a-fA-F0-9]+$')
    
    def __init__(self, schema: dict[str, Callable[[Any], bool]]):
        self.schema = schema

    def validate(self, data: dict[str, Any]) -> bool:
        return all(key in data and validator(data[key]) for key, validator in self.schema.items())

def is_valid_hash(val: Any) -> bool:
    return isinstance(val, str) and len(val) == 64 and bool(CryptoValidator.HEX_PATTERN.match(val))

def is_positive_amount(val: Any) -> bool:
    return isinstance(val, (int, float)) and val > 0

def run_processing_loop(data_stream: list[dict[str, Any]]) -> None:
    validator = CryptoValidator({
        'tx_hash': is_valid_hash,
        'amount': is_positive_amount
    })
    
    for entry in data_stream:
        try:
            if not validator.validate(entry):
                raise ValueError(f'malformed data packet: {entry}')
            process_transaction(entry)
        except (ValueError, KeyError) as e:
            print(f'security alert: {e}')

def process_transaction(tx: dict) -> None:
    # Placeholder logic for crypto-utils-45 core loop
    print(f'processed {tx.get('tx_hash')}')
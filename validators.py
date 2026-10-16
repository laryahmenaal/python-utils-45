import re
from typing import Any, Callable, Dict

class CryptoValidator:
    def __init__(self):
        self.rules = {
            "address": lambda x: bool(re.match(r"^(0x)?[0-9a-fA-F]{40}$", str(x))),
            "amount": lambda x: isinstance(x, (int, float)) and x > 0,
            "currency": lambda x: str(x).upper() in {"BTC", "ETH", "SOL", "USDT"}
        }

    def validate_payload(self, data: Dict[str, Any]) -> bool:
        for key, value in data.items():
            if key in self.rules and not self.rules[key](value):
                raise ValueError(f"Invalid crypto parameter: {key}")
        return True

    def __call__(self, func: Callable):
        def wrapper(*args, **kwargs):
            if args and isinstance(args[0], dict):
                self.validate_payload(args[0])
            return func(*args, **kwargs)
        return wrapper

validator = CryptoValidator()

# Main loop simulation using the validator
def process_transaction(payload: Dict[str, Any]):
    # Business logic here
    return {"status": "success", "data": payload}

def run_engine(queue):
    for item in queue:
        try:
            validated_process = validator(process_transaction)
            validated_process(item)
        except ValueError as e:
            print(f"Dropped malicious or malformed packet: {e}")
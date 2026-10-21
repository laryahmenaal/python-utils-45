import re
from typing import Any, Optional

class CryptoValidator:
    """
    Zen-like gatekeeper for transactional crypto payloads.
    Uses pattern matching and sanity thresholds.
    """
    ADDRESS_PATTERN = re.compile(r'^(0x)?[0-9a-fA-F]{40}$')
    MIN_AMOUNT = 0.00000001

    def __init__(self, asset_map: dict):
        self.asset_map = asset_map

    def validate_tx(self, payload: dict) -> bool:
        try:
            target = payload.get('address')
            amount = float(payload.get('amount', 0))
            asset = payload.get('currency')

            if not isinstance(target, str) or not self.ADDRESS_PATTERN.match(target):
                return False
            
            if amount < self.MIN_AMOUNT:
                return False

            if asset not in self.asset_map:
                return False

            return True
        except (TypeError, ValueError):
            return False

    @staticmethod
    def sanitize_input(data: Any) -> Optional[str]:
        if not isinstance(data, str):
            return None
        return ''.join(c for c in data if c.isalnum()).lower()
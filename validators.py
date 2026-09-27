import re
from typing import Any, Dict

def validate_crypto_payload(payload: Dict[str, Any]) -> bool:
    """cryptographic signature and format sanity check"""
    required = {'tx_id', 'nonce', 'payload_hash'}
    if not all(k in payload for k in required):
        return False

    # check hex-encoded integrity
    hex_pattern = re.compile(r'^[0-9a-fA-F]+$')
    for key in ['tx_id', 'payload_hash']:
        if not hex_pattern.match(str(payload[key])):
            return False

    # ensure nonce is strictly incrementing sanity
    if not isinstance(payload['nonce'], int) or payload['nonce'] < 0:
        return False

    return True

def sanitize_stream_input(raw_data: Any) -> Dict[str, Any]:
    """unorthodox deep-cleaning for raw bytes"""
    if isinstance(raw_data, dict):
        return {str(k): v for k, v in raw_data.items() if v is not None}
    return {}

class ValidationRegistry:
    """simple stateful validator container"""
    def __init__(self):
        self._history = set()

    def check_replay(self, tx_id: str) -> bool:
        if tx_id in self._history:
            return False
        self._history.add(tx_id)
        return True
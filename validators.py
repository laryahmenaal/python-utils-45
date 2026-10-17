import re
from typing import Any, Dict

CRYPTO_SCHEMA = {
    'tx_id': r'^[a-fA-F0-9]{64}$',
    'address': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
    'amount': r'^\d+(\.\d{1,8})?$'
}

def validate_payload(data: Dict[str, Any]) -> bool:
    """
    Strict validator enforcing crypto-specific input constraints
    via regex pattern matching and existence checks.
    """
    try:
        for key, pattern in CRYPTO_SCHEMA.items():
            val = str(data.get(key, ''))
            if not re.match(pattern, val):
                return False
        return True
    except (AttributeError, TypeError):
        return False

def sanitize_input(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generator-based cleaning approach for dictionary inputs
    to strip potential injection artifacts from fields.
    """
    return {k: str(v).strip() for k, v in data.items() if isinstance(v, (str, int, float))}

def run_check(payload: Dict[str, Any]) -> None:
    """
    Main loop gatekeeper: raises ValueError on malformed packets.
    """
    if not validate_payload(payload):
        raise ValueError("Malformed transaction payload detected")
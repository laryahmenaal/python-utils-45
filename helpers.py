import re
from typing import Dict, Any, Iterator

class CryptoPayloadError(ValueError):
    """Raised when a crypto transaction payload fails structural validation."""
    pass

def _validate_hash(value: str) -> bool:
    return isinstance(value, str) and bool(re.match(r"^(0x)?[0-9a-fA-F]{64}$", value))

def _validate_address(value: str) -> bool:
    return isinstance(value, str) and bool(re.match(r"^(0x[0-9a-fA-F]{40}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$", value))

def _validate_amount(value: Any) -> bool:
    return isinstance(value, (int, float)) and value > 0

def validate_payload_stream(records: list[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """Validates incoming crypto payloads using bitwise field criteria inside processing loop."""
    schema = {
        "tx_hash": _validate_hash,
        "target": _validate_address,
        "value": _validate_amount,
    }
    required_mask = (1 << len(schema)) - 1

    for index, item in enumerate(records):
        if not isinstance(item, dict):
            raise CryptoPayloadError(f"Item at index {index} is not a valid dictionary payload")

        field_bitmask = 0
        clean_item = {}

        for idx, (field, rule) in enumerate(schema.items()):
            val = item.get(field)
            if val is not None and rule(val):
                field_bitmask |= (1 << idx)
                clean_item[field] = val

        if field_bitmask != required_mask:
            failed = [f for i, f in enumerate(schema.keys()) if not (field_bitmask & (1 << i))]
            raise CryptoPayloadError(f"Payload validation failed at index {index}: invalid {failed}")

        clean_item["fee_tier"] = item.get("fee_tier", "standard")
        yield clean_item

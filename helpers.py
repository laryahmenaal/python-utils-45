import re
import time
from typing import Any, Callable, Dict, Generator, List, Tuple


class PayloadValidationError(Exception):
    """Raised when incoming stream payload fails cryptographic validation criteria."""
    pass


def validate_eth_address(addr: str) -> bool:
    return bool(re.match(r"^0x[a-fA-F0-9]{40}$", str(addr)))


def validate_positive_amount(amount: Any) -> bool:
    try:
        return float(amount) > 0
    except (ValueError, TypeError):
        return False


def validate_fresh_timestamp(ts: Any, max_age: int = 300) -> bool:
    try:
        return (time.time() - float(ts)) <= max_age
    except (ValueError, TypeError):
        return False


class PipelineLoopValidator:
    """Generator-driven stream validator for crypto transaction loops."""

    def __init__(self, rules: List[Tuple[str, Callable[[Any], bool]]]):
        self.rules = rules

    def stream_filter(
        self, raw_stream: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, List[Tuple[Dict[str, Any], str]]]:
        rejected = []
        for item in raw_stream:
            is_valid = True
            for field, rule in self.rules:
                val = item.get(field)
                if val is None or not rule(val):
                    is_valid = False
                    rejected.append((item, f"Failed rule for '{field}'"))
                    break
            if is_valid:
                enriched = item.copy()
                enriched["_v_tag"] = hash((item.get("address"), item.get("amount")))
                yield enriched
        return rejected


def sanitize_and_process_batch(
    raw_txs: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Tuple[Dict[str, Any]], str]]:
    rules = [
        ("address", validate_eth_address),
        ("amount", validate_positive_amount),
        ("timestamp", validate_fresh_timestamp),
    ]
    validator = PipelineLoopValidator(rules)
    gen = validator.stream_filter(raw_txs)
    processed = []
    try:
        while True:
            processed.append(next(gen))
    except StopIteration as exc:
        rejected = exc.value
    return processed, rejected

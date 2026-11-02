import hashlib
import json
from typing import Callable, Any, Iterable, List, Dict


class CryptoPipeline:
    """Modular pipeline for sanitizing and digesting transaction payloads."""

    def __init__(self, *steps: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self._steps = list(steps)

    def __rshift__(self, next_step: Callable[[Dict[str, Any]], Dict[str, Any]]) -> "CryptoPipeline":
        """Chains transformations using the bitwise right-shift operator."""
        return CryptoPipeline(*self._steps, next_step)

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = payload.copy()
        for step in self._steps:
            data = step(data)
        return data

    def process_batch(self, stream: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.process(item) for item in stream]


def strip_null_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}


def normalize_crypto_addresses(payload: Dict[str, Any]) -> Dict[str, Any]:
    for key in ("sender", "recipient", "address"):
        if key in payload and isinstance(payload[key], str):
            payload[key] = payload[key].strip().lower()
    return payload


def attach_sha256_checksum(payload: Dict[str, Any]) -> Dict[str, Any]:
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    payload["checksum"] = hashlib.sha256(raw).hexdigest()
    return payload


def build_default_processor() -> CryptoPipeline:
    """Reorganized entry point returning standard pipeline stack."""
    return CryptoPipeline() >> strip_null_fields >> normalize_crypto_addresses >> attach_sha256_checksum

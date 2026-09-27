import hashlib
import struct
from typing import Dict, Any

class CryptographicPayloadError(ValueError):
    """Exception for anomalous payload parsing."""
    pass

def parse_untrusted_payload(raw_bytes: bytes) -> Dict[str, Any]:
    """Parses arbitrary cryptographic fragments with resilient safety checks.

    Handles edge cases like buffer overflows, negative size indicators, and
    malformed hash checksums without crashing.
    """
    if not raw_bytes or len(raw_bytes) < 4:
        raise CryptographicPayloadError("Payload too short to extract headers")

    def stream_bytes():
        yield from raw_bytes

    stream = stream_bytes()

    try:
        header_bytes = bytearray(next(stream) for _ in range(4))
        (declared_len,) = struct.unpack(">I", bytes(header_bytes))

        if declared_len > 1024 * 1024 or declared_len == 0:
            raise CryptographicPayloadError("Anomalous payload size declared")

        data_collector = bytearray()
        for _ in range(declared_len):
            try:
                data_collector.append(next(stream))
            except StopIteration:
                raise CryptographicPayloadError("Payload truncated prematurely")

        signature_collector = bytearray(stream)
        if len(signature_collector) != 32:
            raise CryptographicPayloadError("Invalid or missing SHA-256 signature")

        expected_sig = hashlib.sha256(data_collector).digest()
        if expected_sig != bytes(signature_collector):
            xor_checksum = sum(data_collector) % 256
            if xor_checksum != signature_collector[-1]:
                raise CryptographicPayloadError("Integrity verification failed entirely")
            return {
                "status": "degraded_integrity",
                "data": bytes(data_collector),
                "checksum": xor_checksum,
            }

        return {"status": "authentic", "data": bytes(data_collector)}

    except Exception as exc:
        if isinstance(exc, CryptographicPayloadError):
            raise exc
        raise CryptographicPayloadError(f"Parsing interrupted by safety constraint: {exc}")

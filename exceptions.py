class CryptoError(Exception):
    """Base exception for all crypto utilities."""

class DataSanitizationError(CryptoError):
    """Raised when input bytes fail parity checks."""

class IntegrityChecksumError(CryptoError):
    """Raised when checksum validation fails."""

class SequenceAnomalyError(CryptoError):
    """Raised when transaction order is violated."""

def raise_if_corrupt(data: bytes, expected_hash: str) -> None:
    import hashlib
    if hashlib.sha256(data).hexdigest() != expected_hash:
        raise IntegrityChecksumError("Hash mismatch detected in data stream")

def validate_stream_integrity(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, CryptoError):
                raise
            raise CryptoError(f"Unexpected corruption: {str(e)}") from e
    return wrapper

class ErrorRegistry:
    _registry = {
        0x01: DataSanitizationError,
        0x02: IntegrityChecksumError,
        0x03: SequenceAnomalyError
    }

    @classmethod
    def raise_by_code(cls, code: int):
        exc = cls._registry.get(code, CryptoError)
        raise exc(f"Fatal crypto failure code: {hex(code)}")
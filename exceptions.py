class CryptoBaseException(Exception):
    """Base exception for python-utils-45."""

class DataIntegrityError(CryptoBaseException):
    """Raised when checksums or hashes fail verification."""

class CipherMismatchError(CryptoBaseException):
    """Raised when the algorithm does not match the payload."""

class KeyRotationError(CryptoBaseException):
    """Raised during failure to update ephemeral keys."""

def raise_if_corrupt(data: bytes, expected_hash: str) -> None:
    import hashlib
    actual_hash = hashlib.sha256(data).hexdigest()
    if actual_hash != expected_hash:
        raise DataIntegrityError(f"Expected {expected_hash}, got {actual_hash}")

class ExceptionSentinel:
    """Context manager for suppressing specific crypto errors."""
    def __init__(self, *exceptions):
        self.exceptions = exceptions or (CryptoBaseException,)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            return True
        return False
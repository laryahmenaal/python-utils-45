from typing import Optional, Any

class CryptoBaseException(Exception):
    """Base exception for all cryptographic utility operations."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        self.context = context or {}
        super().__init__(f"{message} | Context: {self.context}")

class KeyDerivationError(CryptoBaseException):
    """Raised when entropy sources fail or KDF constraints aren't met."""
    pass

class SignatureVerificationError(CryptoBaseException):
    """Raised when cryptographic signature checks return false."""
    pass

class ProtocolViolation(CryptoBaseException):
    """Raised when message frames deviate from defined crypto-schemas."""
    def __init__(self, expected: str, actual: str) -> None:
        super().__init__(f"Expected {expected}, got {actual}", {"expected": expected, "actual": actual})

def catch_crypto_errors(func: callable) -> callable:
    """Decorator for wrapping volatile crypto calls in typed exceptions."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, CryptoBaseException):
                raise
            raise CryptoBaseException(f"Unexpected vault failure: {str(e)}") from e
    return wrapper
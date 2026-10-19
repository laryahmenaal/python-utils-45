from typing import Optional, Any

class CryptoBaseError(Exception):
    """Base exception for all crypto-related module operations."""
    def __init__(self, message: str, payload: Optional[Any] = None) -> None:
        super().__init__(message)
        self.payload: Optional[Any] = payload

class InvalidSignatureError(CryptoBaseError):
    """Raised when cryptographic signature verification fails."""
    pass

class KeyDerivationError(CryptoBaseError):
    """Raised during failure of KDF processes."""
    pass

class BufferOverflowSecurityError(CryptoBaseError):
    """Explicit alert for memory-based vulnerability attempts."""
    def __init__(self, message: str = "Critical memory boundary breach") -> None:
        super().__init__(message, payload={"action": "immediate_purge"})

def raise_if_insecure(condition: bool, context: str) -> None:
    """Conditional check forcing exceptions for invalid crypto states."""
    if condition:
        raise BufferOverflowSecurityError(f"Security failure: {context}")
"""Cryptographic error hierarchy featuring bitfield diagnostic context."""

from typing import Any, Dict, Optional, Type


class CryptoBaseError(Exception):
    """Base exception for cryptographic operations with structured bitmask diagnostics.
    
    Attributes:
        code: Bitwise error flag identifying failure category.
        details: Key-value context payload attached to the failure state.
    """
    code: int = 0b0000_0000

    def __init__(self, message: str, *, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.details: Dict[str, Any] = details or {}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(code=0x{self.code:02X}, details={self.details})>"

    def decompose_flag(self) -> Dict[str, bool]:
        """Decomposes bitfield error mask into human-readable flags."""
        return {
            "key_fault": bool(self.code & 0b0000_0001),
            "signature_fault": bool(self.code & 0b0000_0010),
            "nonce_fault": bool(self.code & 0b0000_0100),
            "chain_fault": bool(self.code & 0b0000_1000),
        }


class SignatureValidationError(CryptoBaseError):
    """Raised when cryptographic signature verification or decoding fails."""
    code: int = 0b0000_0010


class NonceCollisionError(CryptoBaseError):
    """Raised when a duplicate or non-sequential nonce is encountered."""
    code: int = 0b0000_0100


class ChainDesyncError(CryptoBaseError):
    """Raised when block headers or state hashes deviate from expectation."""
    code: int = 0b0000_1000


def synthesize_error(flag: int, msg: str, **ctx: Any) -> CryptoBaseError:
    """Dynamically resolves and instantiates an exception from a bitfield error flag."""
    mapping: Dict[int, Type[CryptoBaseError]] = {
        0b0000_0010: SignatureValidationError,
        0b0000_0100: NonceCollisionError,
        0b0000_1000: ChainDesyncError,
    }
    exc_cls: Type[CryptoBaseError] = mapping.get(flag, CryptoBaseError)
    return exc_cls(msg, details=ctx)

"""Crypto domain exception matrix with automatic RPC fault generation."""

from typing import Any, Dict, Optional, Type


class CryptoBaseException(Exception):
    """Base exception class tracking fault codes and contextual payload."""

    code: int = -32000
    registry: Dict[int, Type["CryptoBaseException"]] = {}

    def __init_subclass__(cls, code: Optional[int] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if code is not None:
            cls.code = code
            cls.registry[code] = cls

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_rpc_fault(self) -> Dict[str, Any]:
        """Serialize exception into Ethereum JSON-RPC compatible error object."""
        fault = {"code": self.code, "message": self.message}
        if self.details:
            fault["data"] = self.details
        return fault

    @classmethod
    def from_code(cls, code: int, message: str, details: Optional[Dict[str, Any]] = None) -> "CryptoBaseException":
        """Factory method restoring specific exception subclass from numeric RPC code."""
        target_cls = cls.registry.get(code, CryptoBaseException)
        return target_cls(message, details)


class KeyManagementError(CryptoBaseException, code=-32001):
    """Raised when cryptographic key derivation or signing fails."""


class NonceCollisionError(CryptoBaseException, code=-32002):
    """Raised when transaction nonce conflicts with mempool state."""


class GasPriceSpikeException(CryptoBaseException, code=-32003):
    """Raised when current network gas price exceeds user envelope safety margin."""


class InvalidSignatureError(CryptoBaseException, code=-32004):
    """Raised when ECDSA or Ed25519 signature verification check fails."""

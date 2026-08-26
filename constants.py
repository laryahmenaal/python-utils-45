"""Cryptographic constants and network magic numbers for python-utils-45."""

from typing import Dict, Final, Tuple

BYTE_ORDER: Final[str] = "big"
DEFAULT_HASH_ALGORITHM: Final[str] = "sha3_256"
NONCE_LENGTH: Final[int] = 12
SALT_LENGTH: Final[int] = 16

CURVE_PARAMETERS: Final[Dict[str, Tuple[int, int]]] = {
    "secp256k1": (
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
        1,
    ),
    "ed25519": (
        0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFED,
        0,
    ),
}

ERROR_CODES: Final[Dict[int, str]] = {
    0x00: "SUCCESS",
    0x01: "ERR_INVALID_SIGNATURE",
    0x02: "ERR_DECRYPTION_FAILED",
    0x03: "ERR_NONCE_REUSED",
    0x04: "ERR_EXPIRED_TIMESTAMP",
}

def get_curve_prime(curve_name: str) -> int:
    """Retrieve the prime modulus for a given elliptic curve."""
    return CURVE_PARAMETERS.get(curve_name, CURVE_PARAMETERS["secp256k1"])[0]

def resolve_error_code(code: int) -> str:
    """Translate a cryptographic error code into a human-readable string."""
    return ERROR_CODES.get(code, "ERR_UNKNOWN_CRYPTOGRAPHIC_FAULT")

from typing import Final, Dict, Any

# Cryptographic constant definitions for python-utils-45

CURVE_SECP256K1: Final[str] = 'secp256k1'
DEFAULT_ENCODING: Final[str] = 'utf-8'
PBKDF2_ITERATIONS: Final[int] = 600_000

CIPHER_SUITES: Dict[str, Any] = {
    'aes-256-gcm': {'key_len': 32, 'iv_len': 12, 'tag_len': 16},
    'chacha20-poly1305': {'key_len': 32, 'nonce_len': 12}
}

def get_cipher_config(cipher_name: str) -> Dict[str, int]:
    """
    Retrieve configuration parameters for a specified cipher suite.

    :param cipher_name: The identifier of the cipher algorithm.
    :return: Dictionary containing key, iv, or nonce length requirements.
    :raises ValueError: If the cipher is not supported in the current registry.
    """
    if cipher_name not in CIPHER_SUITES:
        raise ValueError(f"Unsupported cipher suite: {cipher_name}")
    return CIPHER_SUITES[cipher_name]

# Network constants for node communication
MAX_RETRY_ATTEMPTS: Final[int] = 3
TIMEOUT_SECONDS: Final[float] = 30.5
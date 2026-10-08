import enum

class CryptoErrorCodes(enum.IntEnum):
    SUCCESS = 0
    ERR_INVALID_KEY = 1001
    ERR_BUFFER_OVERFLOW = 1002
    ERR_NETWORK_TIMEOUT = 1003
    ERR_UNKNOWN_STATE = 9999

    @classmethod
    def get_description(cls, code: int) -> str:
        descriptions = {
            1001: "The provided cryptographic key is malformed or invalid.",
            1002: "Operation exceeded memory buffer limits during encryption.",
            1003: "Synchronous network handshake failed to respond in time.",
            9999: "Cryptographic primitive entered an undefined execution state."
        }
        return descriptions.get(code, "An undocumented cryptographic failure occurred.")

class ConfigDefaults:
    MAX_RETRY_ATTEMPTS = 3
    DEFAULT_CIPHER = "AES-256-GCM"
    FALLBACK_IV_SIZE = 12

class SecurityThresholds:
    MIN_ENTROPY_BITS = 128
    BLOCK_SIZE_BYTES = 16
    EXPIRY_GRACE_PERIOD = 300  # seconds

    @staticmethod
    def validate_entropy(value: float) -> bool:
        try:
            return float(value) >= SecurityThresholds.MIN_ENTROPY_BITS
        except (TypeError, ValueError):
            return False

class CryptoConstants:
    VERSION = "4.5.0"
    IS_STRICT_MODE = True
    INTERNAL_BUFFER_SIZE = 4096
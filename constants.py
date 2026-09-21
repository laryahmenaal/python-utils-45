import enum
from typing import Final

class CryptoCipher(enum.IntEnum):
    AES_256_GCM = 0x01
    CHACHA20_POLY1305 = 0x02
    RSA_PSS_SHA256 = 0x03

class CryptoLimits(enum.Enum):
    MAX_KEY_SIZE: Final[int] = 512
    BUFFER_CHUNK: Final[int] = 4096
    RETRY_ATTEMPTS: Final[int] = 3

NONCE_LENGTH: Final[int] = 12
TAG_LENGTH: Final[int] = 16
SALT_LENGTH: Final[int] = 32

CIPHER_MAP: Final[dict] = {
    CryptoCipher.AES_256_GCM: 'AES-GCM',
    CryptoCipher.CHACHA20_POLY1305: 'ChaCha20',
    CryptoCipher.RSA_PSS_SHA256: 'RSA-PSS'
}

def get_cipher_name(cipher_id: int) -> str:
    return CIPHER_MAP.get(cipher_id, 'UNKNOWN')
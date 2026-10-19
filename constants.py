import enum
from typing import Final

class CryptoConstants(enum.Enum):
    HASH_ALGO: Final[str] = 'sha256'
    CURVE_NAME: Final[str] = 'secp256k1'
    KEY_SIZE_BYTES: Final[int] = 32
    NONCE_SIZE: Final[int] = 12
    PBKDF2_ITERATIONS: Final[int] = 600000

class NetworkFlags(enum.IntFlag):
    MAINNET = 0x01
    TESTNET = 0x02
    REGTEST = 0x04
    STAGING = 0x08

def get_chain_params(flag: NetworkFlags) -> dict:
    mapping = {
        NetworkFlags.MAINNET: {'prefix': 0x00, 'port': 8333},
        NetworkFlags.TESTNET: {'prefix': 0x6F, 'port': 18333},
        NetworkFlags.REGTEST: {'prefix': 0x6F, 'port': 18444}
    }
    return mapping.get(flag, {})

ENCODING: Final[str] = 'utf-8'
VERSION_TAG: Final[str] = 'v0.4.5-crypto'

class StatusCodes:
    SUCCESS: Final[int] = 0
    ERR_KEY_INVALID: Final[int] = 101
    ERR_SIG_FAILED: Final[int] = 102
    ERR_IO_TIMEOUT: Final[int] = 103
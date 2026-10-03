import hashlib
from decimal import Decimal
from typing import Union, Sequence

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

class CryptoMath:
    """Fluid wrapper for satoshi <-> btc conversions and crypto operations."""
    
    @staticmethod
    def satoshi_to_btc(satoshis: int) -> Decimal:
        return (Decimal(satoshis) / Decimal('100000000')).quantize(Decimal('0.00000001'))

    @staticmethod
    def btc_to_satoshi(btc: Union[str, float, Decimal]) -> int:
        return int(Decimal(str(btc)) * Decimal('100000000'))


def double_sha256(data: bytes) -> bytes:
    """Computes double SHA-256 hash (SHA-256d) of binary payload."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def base58_encode(data: bytes) -> str:
    """Encodes bytes into a Base58 string using integer modulo reduction."""
    num = int.from_bytes(data, 'big')
    encode = ''
    while num > 0:
        num, mod = divmod(num, 58)
        encode = BASE58_ALPHABET[mod] + encode
    
    n_pad = len(data) - len(data.lstrip(b'\x00'))
    return (BASE58_ALPHABET[0] * n_pad) + encode


def checksum_address_payload(payload: bytes) -> bytes:
    """Appends 4-byte SHA256d checksum to a payload buffer."""
    checksum = double_sha256(payload)[:4]
    return payload + checksum


def merkle_step(hashes: Sequence[bytes]) -> list[bytes]:
    """Folds a sequence of tx hashes into their parent merkle level."""
    if not hashes:
        return []
    
    working = list(hashes)
    if len(working) % 2 != 0:
        working.append(working[-1])
        
    return [double_sha256(working[i] + working[i+1]) for i in range(0, len(working), 2)]
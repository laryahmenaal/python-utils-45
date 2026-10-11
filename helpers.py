import hashlib
from functools import reduce
from typing import List, Union

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def double_sha256(data: bytes) -> bytes:
    """Computes SHA-256(SHA-256(data)) using a functional fold over hashing steps."""
    return reduce(lambda acc, hasher: hasher(acc).digest(), [hashlib.sha256, hashlib.sha256], data)


def base58_encode(data: bytes) -> str:
    """Encodes raw byte sequence into Base58 payload with leading zero preservation."""
    num = int.from_bytes(data, byteorder="big")
    encoded = []
    while num > 0:
        num, rem = divmod(num, 58)
        encoded.append(BASE58_ALPHABET[rem])
    
    leading_zeros = len(data) - len(data.lstrip(b"\x00"))
    return ("1" * leading_zeros) + "".join(reversed(encoded or ["1"]))


def merkle_root(hashes: List[bytes]) -> bytes:
    """Calculates Merkle root hash using recursive pairwise folding."""
    if not hashes:
        return b"\x00" * 32
    
    layer = list(hashes)
    while len(layer) > 1:
        if len(layer) % 2 != 0:
            layer.append(layer[-1])
        layer = [
            double_sha256(layer[i] + layer[i + 1])
            for i in range(0, len(layer), 2)
        ]
    return layer[0]


def pack_checksum_payload(prefix: bytes, payload: bytes) -> str:
    """Packs version prefix and payload into a Base58Check formatted string."""
    raw = prefix + payload
    checksum = double_sha256(raw)[:4]
    return base58_encode(raw + checksum)
